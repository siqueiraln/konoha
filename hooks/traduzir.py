"""Tradução para o dono e os furos que a trava não enxergava.

Usado por proteger-banco.py. Três partes:
- resumo_migration / resumo_funcao: dizem em português o que uma mudança em
  produção faz, com ⚠️ no que apaga dados ou abre acesso. É o que o dono lê
  na pergunta de autorização; ele não lê SQL.
- funcoes_que_gravam: acha, nas migrations do projeto, as funções do banco que
  gravam algo. Um "select funcao()" parece leitura, mas altera produção.
- http_supabase_grava / script_grava_supabase: gravação pela API do Supabase e
  scripts (Python, Node...) que gravam no Supabase.
"""

import glob
import json
import os
import re

# ---------------------------------------------------------------- limpeza


def _limpar(sql: str) -> str:
    """Tira comentários, corpos entre $$ e textos entre aspas simples; tira aspas de nomes."""
    sql = re.sub(r"--[^\n]*", " ", sql or "")
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)
    sql = re.sub(r"\$(\w*)\$.*?\$\1\$", " $corpo$ ", sql, flags=re.S)
    sql = re.sub(r"'(?:[^']|'')*'", " '' ", sql)
    sql = sql.replace('"', "")
    return re.sub(r"\s+", " ", sql).strip().lower()


def _nome(n: str) -> str:
    n = n.strip().rstrip(",;(")
    return n[7:] if n.startswith("public.") else n


def _partes(texto: str):
    """Quebra por vírgula fora de parênteses (ações de um ALTER TABLE)."""
    partes, nivel, atual = [], 0, ""
    for ch in texto:
        nivel += ch == "("
        nivel -= ch == ")"
        if ch == "," and nivel == 0:
            partes.append(atual.strip())
            atual = ""
        else:
            atual += ch
    if atual.strip():
        partes.append(atual.strip())
    return partes


PAPEIS = {
    "anon": "quem não está logado",
    "public": "todo mundo",
    "authenticated": "usuários logados",
    "service_role": "o próprio sistema",
    "postgres": "o administrador",
}


def _papeis(texto: str) -> str:
    nomes = [p.strip() for p in texto.split(",") if p.strip()]
    return ", ".join(PAPEIS.get(n, n) for n in nomes)


def _objeto(texto: str) -> str:
    """'function public.f(uuid, text)' -> 'a função f'; 'table public.x' -> 'a tabela x'."""
    texto = re.sub(r"\(.*?\)", "", texto).strip()
    if m := re.match(r"(?:all )?(function|functions|table|tables|sequence|sequences|schema) (?:in schema )?(.+)", texto):
        tipo = {"function": "a função", "functions": "as funções", "table": "a tabela", "tables": "as tabelas",
                "sequence": "a sequência", "sequences": "as sequências", "schema": "o esquema"}[m.group(1)]
        return f"{tipo} {', '.join(_nome(n) for n in m.group(2).split(','))}"
    return f"a tabela {', '.join(_nome(n) for n in texto.split(','))}"


def _com_a(objeto: str) -> str:
    """'a função f' -> 'à função f'; 'o esquema x' -> 'ao esquema x'."""
    artigo, resto = objeto.split(" ", 1)
    return {"a": "à", "as": "às", "o": "ao", "os": "aos"}.get(artigo, artigo) + " " + resto


IE = r"(?:if (?:not )?exists )?"
N = r"([\w.]+)"
PAPEIS_ABERTOS = ("anon", "public")

# ---------------------------------------------------------------- migration


def _alter_table(t: str, acoes: str):
    linhas = []
    for a in _partes(acoes):
        if m := re.match(r"drop (?:column )?" + IE + N, a):
            if not a.startswith("drop constraint"):
                linhas.append(f"⚠️ APAGA a coluna {m.group(1)} da tabela {t} (os dados dela somem)")
                continue
        if a.startswith("drop constraint"):
            linhas.append(f"tira uma regra de validação da tabela {t}")
        elif a.startswith("add constraint") or re.match(r"add (primary key|unique|foreign key|check)", a):
            linhas.append(f"acrescenta uma regra de validação na tabela {t}")
        elif m := re.match(r"add (?:column )?" + IE + N, a):
            linhas.append(f"acrescenta a coluna {m.group(1)} na tabela {t}")
        elif m := re.match(r"alter (?:column )?" + N + r" (?:set data )?type", a):
            linhas.append(f"⚠️ muda o tipo da coluna {m.group(1)} na tabela {t} (pode perder ou converter dados)")
        elif m := re.match(r"alter (?:column )?" + N, a):
            linhas.append(f"ajusta a coluna {m.group(1)} na tabela {t}")
        elif m := re.match(r"rename (?:column )?" + N + r" to " + N, a):
            if m.group(1) == "to":
                continue
            linhas.append(f"⚠️ renomeia a coluna {m.group(1)} para {m.group(2)} na tabela {t} (o que usa o nome velho quebra)")
        elif m := re.match(r"rename to " + N, a):
            linhas.append(f"⚠️ renomeia a tabela {t} para {_nome(m.group(1))} (o que usa o nome velho quebra)")
        elif "disable row level security" in a:
            linhas.append(f"⚠️ DESLIGA a proteção por empresa da tabela {t} (qualquer usuário logado passa a ver tudo)")
        elif "enable row level security" in a or "force row level security" in a:
            linhas.append(f"liga a proteção por empresa na tabela {t}")
        else:
            linhas.append(f"muda a tabela {t}")
    return linhas


def _comando(s: str):
    """Uma linha em português para um comando SQL, ou None para ignorar."""
    if re.match(r"(begin|commit|rollback|set |reset |comment on|notify pgrst|select pg_notify)", s) or s in ("", "end"):
        return None
    if "cron.unschedule" in s:
        return "tira uma tarefa automática agendada"
    if "cron.schedule" in s:
        return "agenda uma tarefa automática no banco"
    if m := re.match(r"drop table " + IE + r"(.+?)(?: cascade| restrict)?$", s):
        nomes = ", ".join(_nome(n) for n in m.group(1).split(","))
        return f"⚠️ APAGA a tabela {nomes} inteira, com todos os dados"
    if m := re.match(r"truncate (?:table )?(?:only )?" + N, s):
        return f"⚠️ APAGA todos os dados da tabela {_nome(m.group(1))}"
    if m := re.match(r"delete from (?:only )?" + N + r"(.*)", s):
        t = _nome(m.group(1))
        return f"⚠️ apaga linhas da tabela {t} (com filtro)" if " where " in m.group(2) + " " else f"⚠️ APAGA TODAS as linhas da tabela {t}"
    if m := re.match(r"update (?:only )?" + N + r" (?:as \w+ )?set (.*)", s):
        t = _nome(m.group(1))
        return f"muda dados de algumas linhas da tabela {t} (com filtro)" if " where " in m.group(2) else f"⚠️ MUDA TODAS as linhas da tabela {t}"
    if m := re.match(r"insert into " + N, s):
        return f"acrescenta linhas na tabela {_nome(m.group(1))}"
    if m := re.match(r"alter table " + IE + r"(?:only )?" + N + r" (.*)", s):
        return _alter_table(_nome(m.group(1)), m.group(2))
    if m := re.match(r"create (?:unlogged )?table " + IE + N, s):
        return f"cria a tabela {_nome(m.group(1))}"
    if m := re.match(r"create (?:unique )?index (?:concurrently )?" + IE + r"(?:[\w.]+ )?on (?:only )?" + N, s):
        return f"cria um índice na tabela {_nome(m.group(1))} (deixa as buscas mais rápidas)"
    if s.startswith("drop index"):
        return "apaga um índice (as buscas podem ficar mais lentas)"
    if m := re.match(r"create (?:or replace )?function " + N, s):
        return f"cria ou troca a função {_nome(m.group(1))} do banco"
    if m := re.match(r"drop function " + IE + N, s):
        return f"⚠️ apaga a função {_nome(m.group(1))} do banco (o que chama ela quebra)"
    if m := re.match(r"create (?:or replace )?(?:materialized )?view " + IE + N, s):
        return f"cria ou troca a visão {_nome(m.group(1))}"
    if m := re.match(r"drop (?:materialized )?view " + IE + N, s):
        return f"⚠️ apaga a visão {_nome(m.group(1))}"
    if m := re.match(r"create policy " + N + r" on " + N + r"(.*)", s):
        aberta = any(re.search(rf"\bto [^;]*\b{p}\b", m.group(3)) for p in PAPEIS_ABERTOS) or re.search(r"using \(\s*true\s*\)", m.group(3))
        texto = f"cria uma regra de acesso na tabela {_nome(m.group(2))}"
        return ("⚠️ " + texto + " que vale para qualquer um") if aberta else ("🔐 " + texto)
    if m := re.match(r"drop policy " + IE + N + r" on " + N, s):
        return f"⚠️ apaga uma regra de acesso da tabela {_nome(m.group(2))} (pode abrir ou fechar o acesso)"
    if m := re.match(r"alter policy " + N + r" on " + N, s):
        return f"🔐 muda uma regra de acesso da tabela {_nome(m.group(2))}"
    if m := re.match(r"grant (.+?) on (.+?) to (.+)", s):
        quem = m.group(3)
        texto = f"deixa {_papeis(quem)} usar {_objeto(m.group(2))}"
        aberto = any(re.search(rf"\b{p}\b", quem) for p in PAPEIS_ABERTOS)
        return ("⚠️ " + texto) if aberto else ("🔐 " + texto)
    if m := re.match(r"revoke (.+?) on (.+?) from (.+)", s):
        return f"🔐 tira de {_papeis(m.group(3))} o acesso {_com_a(_objeto(m.group(2)))}"
    if m := re.match(r"create (?:or replace )?(?:constraint )?trigger " + N + r" .*? on " + N, s):
        return f"cria um gatilho automático na tabela {_nome(m.group(2))}"
    if m := re.match(r"drop trigger " + IE + N + r" on " + N, s):
        return f"apaga um gatilho automático da tabela {_nome(m.group(2))}"
    if m := re.match(r"create (type|schema|extension|sequence) " + IE + N, s):
        tipos = {"type": "o tipo", "schema": "o esquema", "extension": "a extensão", "sequence": "a sequência"}
        return f"cria {tipos[m.group(1)]} {_nome(m.group(2))}"
    if m := re.match(r"drop (type|schema|extension|sequence) " + IE + N, s):
        return f"⚠️ apaga {m.group(1)} {_nome(m.group(2))}"
    if m := re.match(r"alter (function|type|view|sequence) " + N, s):
        return f"ajusta {m.group(1)} {_nome(m.group(2))}"
    if s.startswith("select") or s.startswith("do "):
        return "roda um comando do banco (a trava não traduz o que ele faz)"
    return f"outro comando que a trava não traduz: {' '.join(s.split()[:3])}"


def resumo_migration(sql: str, nome: str = ""):
    """Devolve (texto para o dono, grave)."""
    linhas = []
    for s in _limpar(sql).split(";"):
        r = _comando(s.strip())
        if r:
            linhas.extend(r if isinstance(r, list) else [r])
    vistas, unicas = set(), []
    for l in linhas:
        if l not in vistas:
            vistas.add(l)
            unicas.append(l)
    grave = any(l.startswith("⚠️") for l in unicas)
    mostrar = unicas if len(unicas) <= 14 else unicas[:13] + [f"... e mais {len(unicas) - 13} itens"]
    if grave:  # o grave primeiro, para não se perder no meio
        mostrar = [l for l in mostrar if l.startswith("⚠️")] + [l for l in mostrar if not l.startswith("⚠️")]
    corpo = "\n".join("• " + l for l in mostrar) or "• (nenhum comando reconhecido)"
    titulo = f"Mudança no banco de PRODUÇÃO{f' ({nome})' if nome else ''}:"
    fecho = (
        "⚠️ TEM ITEM GRAVE (apaga dados, apaga coisa usada ou abre acesso). Só aprove se o Tech Lead "
        "explicou, logo acima, em português, por que precisa e como volta atrás."
        if grave
        else "Nada aqui apaga dados. Aprove se bate com o que o Tech Lead disse que ia fazer."
    )
    return f"🔒 {titulo}\n{corpo}\n\n{fecho}", grave


def resumo_funcao(entrada: dict):
    nome = entrada.get("name") or "(sem nome)"
    linhas = [f"• publica uma versão nova da função {nome} no ar; a anterior para de rodar na hora"]
    grave = entrada.get("verify_jwt") is False
    if grave:
        linhas.insert(0, "• ⚠️ a função fica ABERTA, sem exigir login (só pode se ela confere quem chama de outro jeito)")
    fecho = (
        "⚠️ TEM ITEM GRAVE. Só aprove se o Tech Lead explicou, logo acima, por que a função fica aberta."
        if grave
        else "Aprove se bate com o que o Tech Lead disse que ia publicar."
    )
    return "🔒 Publicação no ar (função do Supabase):\n" + "\n".join(linhas) + "\n\n" + fecho, grave


# ---------------------------------------------------------------- funções do banco que gravam

GRAVA_NO_CORPO = re.compile(
    r"\b(insert\s+into|update\s+[\w.\"]+\s+set|delete\s+from|truncate|merge\s+into|net\.http_\w+|"
    r"cron\.(schedule|unschedule)|pg_notify|nextval|setval|set_config)\b",
    re.I,
)
DEF_FUNCAO = re.compile(
    r"create\s+(?:or\s+replace\s+)?function\s+([\w.\"]+)\s*\((.*?)\bas\s+(\$\w*\$)(.*?)\3",
    re.I | re.S,
)
_cache = {}


def _pasta_migrations(cwd: str):
    atual = os.path.abspath(cwd or ".")
    for _ in range(8):
        candidata = os.path.join(atual, "supabase", "migrations")
        if os.path.isdir(candidata):
            return candidata
        pai = os.path.dirname(atual)
        if pai == atual:
            break
        atual = pai
    return None


def funcoes_que_gravam(cwd: str) -> set:
    pasta = _pasta_migrations(cwd)
    if not pasta:
        return set()
    arquivos = sorted(glob.glob(os.path.join(pasta, "*.sql")))
    chave = (pasta, len(arquivos), max((os.path.getmtime(a) for a in arquivos), default=0))
    if chave in _cache:
        return _cache[chave]
    corpos = {}
    for arquivo in arquivos:  # a definição mais nova vence
        try:
            texto = open(arquivo, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        for m in DEF_FUNCAO.finditer(texto):
            corpos[_nome(m.group(1).replace('"', "").lower())] = m.group(4)
    grava = {n for n, c in corpos.items() if GRAVA_NO_CORPO.search(c)}
    for _ in range(3):  # quem chama uma função que grava, também grava
        novas = {n for n, c in corpos.items() if n not in grava and any(re.search(rf"\b{re.escape(g)}\s*\(", c, re.I) for g in grava)}
        if not novas:
            break
        grava |= novas
    _cache[chave] = grava
    return grava


def funcoes_chamadas_que_gravam(sql: str, cwd: str):
    limpo = _limpar(sql)
    chamadas = {_nome(n) for n in re.findall(r"\b([\w.]+)\s*\(", limpo)}
    if not chamadas:
        return []
    return sorted(chamadas & funcoes_que_gravam(cwd))


# ---------------------------------------------------------------- HTTP e scripts

ENDERECO_SUPABASE = re.compile(
    r"https?://[\w-]+\.supabase\.co\b|api\.supabase\.com|\$\{?(?:VITE_|NEXT_PUBLIC_)?SUPABASE_URL",
    re.I,
)
LOCAL = re.compile(r"localhost|127\.0\.0\.1|:5432[1-4]\b", re.I)
RODA_SCRIPT = re.compile(
    r"^\s*(?:\w+=\S*\s+)*(?:npx\s+(?:-y\s+)?)?"
    r"(?:node|python3?|py|tsx|ts-node|bun(?:\s+run)?|deno\s+run(?:\s+-\S+)*)\s+(?:-\S+\s+)*"
    r"([^\s-][^\s]*\.(?:js|mjs|cjs|ts|mts|py))\b",
    re.I,
)
CODIGO_INLINE = re.compile(r"\b(?:python3?|py|node)\s+(?:-c|-e)\s+(\"(?:[^\"\\]|\\.)*\"|'[^']*')", re.I)
SUPABASE_NO_CODIGO = re.compile(r"supabase\.co|service_role|SERVICE_ROLE|SUPABASE_URL|createClient|create_client", re.I)
GRAVA_NO_CODIGO = re.compile(
    r"\.(insert|update|upsert|delete|rpc)\s*\(|requests\.(post|put|patch|delete)\s*\(|"
    r"method\s*[:=]\s*['\"](POST|PUT|PATCH|DELETE)|\b(insert\s+into|delete\s+from|truncate)\b|\bupdate\s+\w+\s+set\b",
    re.I,
)


def http_supabase_grava(trecho: str, cliente_http, escrita_http) -> bool:
    # POST que só lê: consulta graphql sem "mutation" e login de teste
    if "/graphql/v1" in trecho and "mutation" not in trecho.lower():
        return False
    if "/auth/v1/token" in trecho:
        return False
    return bool(
        cliente_http.search(trecho)
        and ENDERECO_SUPABASE.search(trecho)
        and not LOCAL.search(trecho)
        and escrita_http.search(trecho)
    )


def script_grava_supabase(trecho: str, cwd: str):
    """Devolve o nome do script (ou 'código na linha') se ele grava no Supabase; senão None."""
    if LOCAL.search(trecho):
        return None
    codigos = []
    if m := CODIGO_INLINE.search(trecho):
        codigos.append(("código na linha de comando", m.group(1)))
    if m := RODA_SCRIPT.search(trecho):
        caminho = os.path.join(cwd or ".", m.group(1))
        try:
            codigos.append((m.group(1), open(caminho, encoding="utf-8", errors="ignore").read(200_000)))
        except OSError:
            pass
    for nome, codigo in codigos:
        if SUPABASE_NO_CODIGO.search(codigo) and GRAVA_NO_CODIGO.search(codigo) and not re.search(
            r"localhost|127\.0\.0\.1", codigo
        ):
            return nome
    return None
