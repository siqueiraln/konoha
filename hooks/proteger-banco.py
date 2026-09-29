"""Trava do banco e do n8n: leitura livre, qualquer alteração só com autorização do dono.

Gancho PreToolUse do Claude Code. Recebe a chamada de ferramenta em JSON pela
entrada padrão e responde:
- execute_sql que grava: NEGA (a alteração tem que ir por apply_migration);
  ajustes de sessão que não gravam (tempo limite, simular usuário comum) passam;
- apply_migration, deploy_edge_function e outras ferramentas do Supabase que
  alteram algo: PERGUNTA ao dono, sempre, mesmo em modo automático;
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
# campo n8n_hosts do `.claude/konoha.json` (projeto.py).

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


# ---------------------------------------------------------------- decisão

def decidir(chamada: dict):
    """Devolve (decisão, motivo), ou None quando a trava não interfere."""
    ferramenta = chamada.get("tool_name", "")
    entrada = chamada.get("tool_input", {}) or {}
    cwd = chamada.get("cwd", "")

    if ferramenta.startswith("mcp__") and "supabase" in ferramenta.lower():
        if ferramenta.endswith("__execute_sql"):
            if sql_grava(entrada.get("query", "")):
                return (
                    "deny",
                    "Trava do banco: o execute_sql só pode LER. Esta consulta altera o banco. "
                    "Para alterar, escreva uma migration e use apply_migration, que pede a "
                    "autorização do dono antes de rodar.",
                )
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
            return ("ask", traduzir.resumo_migration(entrada.get("query", ""), entrada.get("name", ""))[0])
        if ferramenta.endswith("__deploy_edge_function"):
            return ("ask", traduzir.resumo_funcao(entrada)[0])
        if FERRAMENTAS_SUPABASE_QUE_ALTERAM.search(ferramenta):
            acao = ferramenta.rsplit("__", 1)[-1]
            return (
                "ask",
                f"🔒 Mudança no Supabase de PRODUÇÃO ({acao}). Não é uma mudança de dados comum: "
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
            if pergunta:
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
