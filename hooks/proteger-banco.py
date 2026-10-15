"""Trava do banco e do n8n: leitura livre; na produção, só o que apaga pergunta.

Gancho PreToolUse do Claude Code. Recebe a chamada de ferramenta em JSON pela
entrada padrão e responde:
- produção, execute_sql e apply_migration: PASSA o que só acrescenta ou ajusta
  (inserir, mudar linhas com filtro, criar tabela, coluna, função, regra de
  acesso fechada) e o que apaga só dentro da empresa de teste (campo
  empresa_teste do `.claude/konoha.local.json`). PERGUNTA, em português, o que apaga
  dado ou estrutura, muda todas as linhas, abre acesso, ou a trava não sabe
  traduzir (bloco DO, select que grava). Decisão do dono em 14/10/2026: ele não
  lê SQL, então o "pode" dele só vale onde ele consegue julgar ("apaga isto");
- deploy_edge_function e publicar pelo comando oficial: PASSA se a função exige
  login como o projeto declara; PERGUNTA se não;
- outras ferramentas do Supabase que alteram algo (branches, pausar, restaurar):
  PERGUNTA;
- terminal: comando que altera o Supabase remoto, ou psql fora do banco local:
  PERGUNTA; psql no banco local (Docker, localhost) passa;
- MCP do n8n: ferramentas de leitura passam; qualquer outra (executar, publicar,
  criar, editar, testar, apagar) PERGUNTA;
- n8n pelo terminal: só olha o trecho do comando que chama um endereço de n8n;
  leitura passa; escrita, chamada de webhook e comandos de escrita da CLI do n8n
  PERGUNTAM;
- select que chama função do banco que grava (achada nas migrations do projeto),
  gravação pela API do Supabase e script que grava no Supabase: PERGUNTA;
- toda pergunta diz em português o que a mudança faz, com ⚠️ no que é grave
  (traduzir.py). O dono não lê SQL: a tela é o que ele avalia;
- projeto ESPELHO (campo banco_espelho do `.claude/konoha.local.json`: cópia da
  estrutura de produção, sem dado de cliente): consulta que grava, migration e
  publicar função pelas ferramentas do Supabase passam sem perguntar. É lá que os
  agentes mudam e testam o banco. Pelo terminal, o espelho pergunta como produção;
- ferramenta de banco de qualquer servidor MCP (execute_sql, apply_migration,
  deploy_edge_function) é tratada como Supabase, mesmo sem "supabase" no nome
  (o conector da conta aparece com um código no lugar do nome em algumas conversas);
  no conector com código, as outras ações do Supabase que alteram também;
- o gancho só roda se o `matcher` do ~/.claude/settings.json pegar o nome da
  ferramenta. O matcher certo está em MATCHER abaixo; o testar-trava.py confere
  que o instalado pega todo nome que a trava trata (furo de 15/10/2026: o conector
  com código e o n8n ficavam de fora e iam à produção sem a trava);
- qualquer outra coisa: não interfere.

Buracos que continuam: `npm run <script>` (a trava não vê o que roda), função
criada fora das migrations, script que usa endereço local como reserva.

Se este arquivo quebrar, a trava deixa de funcionar em silêncio. Depois de
qualquer mudança, rode `python testar-trava.py` nesta pasta.
"""

import json
import os
import re
import sys

MATCHER = (
    r"^mcp__.*([Ss]upabase|[Nn]8[Nn]|__(execute_sql|apply_migration|deploy_edge_function|"
    r"create_branch|delete_branch|merge_branch|reset_branch|rebase_branch|restore_project|"
    r"pause_project|create_project|update_storage_config|create_storage_bucket|delete_storage_bucket)$)"
    r"|^Bash$|^PowerShell$"
)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import projeto  # noqa: E402
import traduzir  # noqa: E402

# ---------------------------------------------------------------- comum


def trechos(comando: str):
    """Quebra o comando nos pedaços que o terminal roda separados."""
    comando = re.sub(r"\\\r?\n", " ", comando)
    return [trecho for trecho in re.split(r"&&|\|\||;|\n|\|", comando) if trecho.strip()]


# ---------------------------------------------------------------- Supabase

ESCRITA_SQL = [
    r"\b(insert|update|delete|merge|upsert|truncate|create|alter|drop|grant|revoke)\b",
    r"\b(copy|call|vacuum|reindex|cluster|refresh|listen|notify|prepare|execute|discard|import|into)\b",
    r"\bcomment\s+on\b",
    r"\bsecurity\s+label\b",
    r"(^|;)\s*(do|set|reset|lock|begin|commit|rollback|savepoint|release|start)\b",
    r"\bset\s+(role|session|local)\b",
    r"\b(set_config|setval|nextval|pg_notify|pg_terminate_backend|pg_cancel_backend|pg_reload_conf|pg_switch_wal|lo_import|lo_unlink|dblink\w*)\s*\(",
    r"\bpg_advisory\w*\s*\(",
    r"\bcron\s*\.\s*(schedule|unschedule|alter_job)\b",
    r"\bnet\s*\.\s*http_\w+",
    r"\bvault\s*\.\s*(create|update)_secret\b",
]

# Ajustes de sessão que não gravam nada. São tirados do SQL antes da checagem.
AJUSTES_SEM_ESCRITA = [
    r"\bset\s+(local\s+)?(statement_timeout|lock_timeout|idle_in_transaction_session_timeout|search_path|work_mem)\s*(=|to)\s*[^;]*",
    r"\bset\s+(local\s+)?role\s+(anon|authenticated)\b",
    r"\bset\s+(local\s+)?\"?request\.jwt\.[\w.]+\"?\s*(=|to)\s*[^;]*",
    r"\bset_config\s*\(\s*'request\.jwt\.[\w.]+'\s*,\s*'(?:[^']|'')*'\s*,\s*(true|false)\s*\)",
    r"\bset_config\s*\(\s*'role'\s*,\s*'(anon|authenticated)'\s*,\s*(true|false)\s*\)",
    r"\bcreate\s+(or\s+replace\s+)?function\s+pg_temp\.",
    r"(^|;)\s*(begin|commit|rollback|start\s+transaction)\s*(?=;|$)",
]

FERRAMENTAS_SUPABASE_QUE_ALTERAM = re.compile(
    r"__(apply_migration|deploy_edge_function|create_branch|delete_branch|merge_branch|"
    r"reset_branch|rebase_branch|restore_project|pause_project|create_project|"
    r"update_storage_config|create_storage_bucket|delete_storage_bucket)$"
)

# Ferramentas de banco: valem pelo nome da ação, venham do servidor que vierem.
FERRAMENTAS_DE_BANCO = ("__execute_sql", "__apply_migration", "__deploy_edge_function")


# Conector da conta com código no lugar do nome (mcp__1abde08f-...__): as ações do
# Supabase que alteram valem por ele também.
SERVIDOR_COM_CODIGO = re.compile(r"^mcp__[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}__")


def ferramenta_supabase(ferramenta: str, entrada: dict | None = None) -> bool:
    entrada = entrada or {}
    return ferramenta.startswith("mcp__") and (
        "supabase" in ferramenta.lower()
        or ferramenta.endswith(FERRAMENTAS_DE_BANCO)
        # outros conectores com código (Vercel) têm ações de mesmo nome; as do Supabase
        # dizem o projeto ou a organização
        or bool(
            SERVIDOR_COM_CODIGO.match(ferramenta)
            and FERRAMENTAS_SUPABASE_QUE_ALTERAM.search(ferramenta)
            and ("project_id" in entrada or "organization_id" in entrada)
        )
    )


def alvo_e_espelho(ferramenta: str, entrada: dict, cwd: str) -> bool:
    """A chamada vai para o projeto espelho do `.claude/konoha.local.json`?

    Campo `banco_espelho`: {"ref": "<código do projeto>", "mcp": "<nome do servidor MCP ligado só nele>"}.
    Vale o nome do servidor (ferramentas `mcp__<mcp>__*`) ou o `project_id` da chamada,
    quando a ferramenta é do conector da conta e escolhe o projeto a cada chamada.
    """
    espelho = projeto.config(cwd).get("banco_espelho")
    if not isinstance(espelho, dict):
        return False
    mcp, ref = espelho.get("mcp"), espelho.get("ref")
    if mcp and ferramenta.startswith(f"mcp__{mcp}__"):
        return True
    return bool(ref) and entrada.get("project_id") == ref


TERMINAL_SUPABASE_QUE_ALTERA = re.compile(
    r"\bsupabase\s+(db\s+push|migration\s+(up|repair|squash)|functions\s+(deploy|delete)|"
    r"secrets\s+(set|unset)|link\b|branches\s+(create|delete))"
    r"|\bsupabase\b[^\n]*(--linked|--db-url)\b"
    r"|\bpg_restore\b|\bpg_dump\b[^\n]*--clean",
    re.IGNORECASE,
)

# psql sendo o programa que roda (não "which psql", nem o nome dentro de um texto).
PSQL = re.compile(
    r"^\s*[({]?\s*(\w+=\S*\s+)*(sudo\s+)?psql(\.exe)?(\s|$)|\bdocker\s+exec\b[^\n]*\bpsql\b",
    re.IGNORECASE,
)
BANCO_LOCAL = re.compile(r"docker\s+exec|localhost|127\.0\.0\.1|:54322\b|supabase_db_", re.IGNORECASE)


def terminal_supabase_altera(comando: str) -> bool:
    for trecho in trechos(comando):
        if TERMINAL_SUPABASE_QUE_ALTERA.search(trecho):
            return True
        if PSQL.search(trecho) and not BANCO_LOCAL.search(trecho):
            return True
    return False


# ---------------------------------------------------------------- n8n

# Endereços de instâncias n8n que não têm "n8n" no nome vêm do projeto:
# campo n8n_hosts do `.claude/konoha.local.json` (projeto.py).

N8N_LEITURA_MCP = re.compile(r"__(search_|get_|list_|validate_|explore_)\w*$")

# Servidores MCP só de documentação pública: nunca alteram nada.
MCP_SO_DOCUMENTACAO = ("mcp__n8n-docs__",)

def endereco_n8n(hosts=()):
    return re.compile(
        r"https?://[^\s\"']*(" + "|".join(["n8n"] + [re.escape(h) for h in hosts]) + r")[^\s\"']*"
        r"|\$\{?N8N_\w*(URL|HOST)",
        re.IGNORECASE,
    )

CLIENTE_HTTP = re.compile(
    r"\b(curl|wget|Invoke-RestMethod|Invoke-WebRequest|irm|iwr)\b|\brequests\.\w+\s*\(|\bfetch\s*\(",
    re.IGNORECASE,
)

WEBHOOK_N8N = re.compile(
    r"/(webhook|webhook-test|webhook-waiting|form|form-test|mcp|mcp-server)/",
    re.IGNORECASE,
)

ESCRITA_HTTP = re.compile(
    r"(-X|--request)\s*['\"]?(POST|PUT|PATCH|DELETE)\b"
    r"|\s(-d|--data\S*|-F|--form|--json|-T|--upload-file)\b"
    r"|--method[= ]\s*['\"]?(POST|PUT|PATCH|DELETE)"
    r"|-Method\s+['\"]?(Post|Put|Patch|Delete)\b|\s-Body\b"
    r"|\brequests\.(post|put|patch|delete)\b"
    r"|method\s*:\s*['\"](POST|PUT|PATCH|DELETE)",
    re.IGNORECASE,
)

CLI_N8N_ESCRITA = re.compile(
    r"^\s*(npx\s+(-y\s+)?)?(@n8n/)?n8n(-cli)?\s+[^\n]*\b(create|update|delete|activate|deactivate|"
    r"publish|unpublish|execute|run|retry|stop|import|transfer|archive)\b"
    r"|^\s*(npx\s+)?n8n\s+(import|update|execute)\s*:",
    re.IGNORECASE,
)


def n8n_terminal_altera(comando: str, hosts=()) -> bool:
    endereco = endereco_n8n(hosts)
    for trecho in trechos(comando):
        if CLI_N8N_ESCRITA.search(trecho):
            return True
        if CLIENTE_HTTP.search(trecho) and endereco.search(trecho):
            if WEBHOOK_N8N.search(trecho) or ESCRITA_HTTP.search(trecho):
                return True
    return False


# ---------------------------------------------------------------- SQL

def limpar_sql(sql: str) -> str:
    """Tira comentários, ajustes de sessão e textos entre aspas, para não confundir texto com comando."""
    sql = re.sub(r"--[^\n]*", " ", sql)
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)
    for padrao in AJUSTES_SEM_ESCRITA:
        sql = re.sub(padrao, " ", sql, flags=re.IGNORECASE)
    sql = re.sub(r"\$(\w*)\$.*?\$\1\$", " '' ", sql, flags=re.S)
    sql = re.sub(r"'(?:[^']|'')*'", " '' ", sql)
    sql = re.sub(r'"(?:[^"]|"")*"', " x ", sql)
    return sql.lower()


def sql_grava(sql: str) -> bool:
    limpo = limpar_sql(sql)
    return any(re.search(padrao, limpo) for padrao in ESCRITA_SQL)


def comandos(sql: str):
    """Quebra o SQL nos comandos, por ";" fora de textos e de corpos $$. Tira comentários fora de textos."""
    partes, atual, i, n = [], "", 0, len(sql or "")
    while i < n:
        c = sql[i]
        if c == "'":
            j = i + 1
            while j < n and not (sql[j] == "'" and sql[j + 1:j + 2] != "'"):
                j += 2 if sql[j] == "'" else 1
            atual += sql[i:j + 1]
            i = j + 1
        elif m := re.match(r"\$(\w*)\$", sql[i:]):
            fim = sql.find(m.group(0), i + len(m.group(0)))
            fim = n if fim < 0 else fim + len(m.group(0))
            atual += sql[i:fim]
            i = fim
        elif sql.startswith("--", i):
            fim = sql.find("\n", i)
            i = n if fim < 0 else fim
        elif sql.startswith("/*", i):
            fim = sql.find("*/", i + 2)
            i = n if fim < 0 else fim + 2
        elif c == ";":
            partes.append(atual)
            atual, i = "", i + 1
        else:
            atual += c
            i += 1
    partes.append(atual)
    return [p.strip() for p in partes if p.strip()]


def so_empresa_teste(bruto: str, limpo: str, empresa: str) -> bool:
    """Apagar ou mudar linhas filtrando só pela empresa de teste, sem "or" que alargue o filtro."""
    if not re.match(r"(delete|update)\b", limpo) or " or " in f" {limpo} ":
        return False
    return bool(re.search(r"\bcompany_id\s*=\s*'" + re.escape(empresa.lower()) + "'", bruto.lower()))


def so_explain(sql: str) -> bool:
    """Tudo é EXPLAIN sem ANALYZE: o banco só descreve o plano e não executa nada (autorizado pelo dono em 15/10/2026)."""
    limpos = [l for l in (traduzir._limpar(c) for c in comandos(sql)) if l]
    return bool(limpos) and all(
        re.match(r"explain\b", l) and not re.search(r"\banaly[sz]e\b", l) for l in limpos
    )


def mudanca_comum(sql: str, cwd: str) -> bool:
    """Só acrescenta ou ajusta, ou só apaga na empresa de teste? Então não precisa do dono."""
    empresa = (projeto.config(cwd).get("empresa_teste") or {}).get("id") or ""
    algum = False
    for bruto in comandos(sql):
        sessao = bruto
        for padrao in AJUSTES_SEM_ESCRITA:
            sessao = re.sub(padrao, " ", sessao, flags=re.IGNORECASE)
        limpo = traduzir._limpar(sessao)
        if not limpo:
            continue
        if re.match(r"(set|reset|do|call|copy|lock|execute|prepare|security label)\b", limpo):
            return False
        if re.match(r"(select|with|values|table|explain)\b", limpo):
            if sql_grava(bruto) or traduzir.funcoes_chamadas_que_gravam(bruto, cwd):
                return False
            continue
        linha = traduzir._comando(limpo)
        if linha is None:
            continue
        for texto in linha if isinstance(linha, list) else [linha]:
            if "não traduz" in texto or "tarefa automática" in texto:
                return False
            if texto.startswith("⚠️") and not (empresa and so_empresa_teste(bruto, limpo, empresa)):
                return False
        algum = True
    return algum


# ---------------------------------------------------------------- decisão

def decidir(chamada: dict):
    """Devolve (decisão, motivo), ou None quando a trava não interfere."""
    ferramenta = chamada.get("tool_name", "")
    entrada = chamada.get("tool_input", {}) or {}
    cwd = chamada.get("cwd", "")

    if ferramenta_supabase(ferramenta, entrada):
        no_espelho = alvo_e_espelho(ferramenta, entrada, cwd)
        if no_espelho and ferramenta.endswith(FERRAMENTAS_DE_BANCO):
            return None
        if ferramenta.endswith("__execute_sql"):
            if so_explain(entrada.get("query", "")):
                return None
            if sql_grava(entrada.get("query", "")):
                if mudanca_comum(entrada.get("query", ""), cwd):
                    return None
                return ("ask", traduzir.resumo_migration(entrada.get("query", ""))[0])
            funcoes = traduzir.funcoes_chamadas_que_gravam(entrada.get("query", ""), cwd)
            if funcoes:
                return (
                    "ask",
                    "🔒 Roda em PRODUÇÃO " + ", ".join(funcoes) + ", função do banco que GRAVA dados "
                    "(parece uma consulta, mas altera). Aprove só se o Tech Lead explicou, logo acima, "
                    "o que ela faz e em qual empresa.",
                )
            return None
        if ferramenta.endswith("__apply_migration"):
            if mudanca_comum(entrada.get("query", ""), cwd):
                return None
            return ("ask", traduzir.resumo_migration(entrada.get("query", ""), entrada.get("name", ""))[0])
        if ferramenta.endswith("__deploy_edge_function"):
            texto, grave = traduzir.resumo_funcao(entrada)
            return ("ask", texto) if grave else None
        if FERRAMENTAS_SUPABASE_QUE_ALTERAM.search(ferramenta):
            acao = ferramenta.rsplit("__", 1)[-1]
            if no_espelho:
                onde = "no projeto ESPELHO (não é produção)"
            elif "supabase" in ferramenta.lower():
                onde = "no Supabase de PRODUÇÃO"
            else:
                onde = "num serviço conectado (Supabase de PRODUÇÃO ou outro)"
            return (
                "ask",
                f"🔒 Mudança {onde} ({acao}). Não é uma mudança de dados comum: "
                "aprove só se o Tech Lead explicou, logo acima, o que é e por quê.",
            )
        return None

    if ferramenta.startswith(MCP_SO_DOCUMENTACAO):
        return None

    if ferramenta.startswith("mcp__") and "n8n" in ferramenta.lower():
        if not N8N_LEITURA_MCP.search(ferramenta):
            return (
                "ask",
                "Trava do n8n: esta ação altera ou dispara algo no n8n. Só roda com a "
                "autorização do dono.",
            )
        return None

    if ferramenta in ("Bash", "PowerShell"):
        comando = entrada.get("command", "")
        oficial = projeto.config(cwd).get("publicar_funcao") or ""
        for trecho in trechos(comando):
            pergunta = traduzir.publicacao_funcao(trecho, cwd, oficial)
            if pergunta and "GRAVE" in pergunta:
                return ("ask", pergunta)
        if terminal_supabase_altera(comando):
            return (
                "ask",
                "🔒 Comando que mexe no Supabase de PRODUÇÃO pelo terminal. A trava não consegue "
                "traduzir o que ele faz: aprove só se o Tech Lead explicou, logo acima, em português.",
            )
        for trecho in trechos(comando):
            if traduzir.http_supabase_grava(trecho, CLIENTE_HTTP, ESCRITA_HTTP):
                return (
                    "ask",
                    "🔒 Grava no Supabase de PRODUÇÃO pela internet (API), por fora das migrations. "
                    "Aprove só se o Tech Lead explicou, logo acima, o que muda e em quais dados.",
                )
            script = traduzir.script_grava_supabase(trecho, cwd)
            if script:
                return (
                    "ask",
                    f"🔒 Roda um script ({script}) que grava no Supabase. Se ele aponta para "
                    "produção, altera dados reais. Aprove só se o Tech Lead explicou, logo acima, "
                    "o que o script muda e onde.",
                )
        if n8n_terminal_altera(comando, projeto.config(cwd).get("n8n_hosts") or ()):
            return (
                "ask",
                "Trava do n8n: este comando altera o n8n ou dispara um workflow (webhook). "
                "Só roda com a autorização do dono.",
            )
    return None


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        chamada = json.load(sys.stdin)
    except Exception:
        return
    resultado = decidir(chamada)
    if resultado:
        decisao, motivo = resultado
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": decisao,
                "permissionDecisionReason": motivo,
            }
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
