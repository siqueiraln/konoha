"""Testes da trava. Rode depois de qualquer mudança em proteger-banco.py:

    python testar-trava.py

Sai com código 1 se algum caso falhar. Caso novo que escapou da trava vira linha aqui.
"""

import importlib.util
import pathlib
import sys

caminho = pathlib.Path(__file__).with_name("proteger-banco.py")
especificacao = importlib.util.spec_from_file_location("trava", caminho)
trava = importlib.util.module_from_spec(especificacao)
especificacao.loader.exec_module(trava)

LIVRE, PERGUNTA, NEGA = None, "ask", "deny"

CASOS = [
    # Supabase: leitura
    ("mcp__supabase__execute_sql", {"query": "select id, updated_at from contatos where nome = 'drop table x' limit 5"}, LIVRE),
    ("mcp__supabase__execute_sql", {"query": "select * from pg_policies -- update aqui é comentário"}, LIVRE),
    ("mcp__supabase__execute_sql", {"query": "with x as (select 1) select * from x"}, LIVRE),
    ("mcp__supabase__list_tables", {}, LIVRE),
    # Supabase: gravação
    ("mcp__supabase__execute_sql", {"query": "UPDATE contatos SET nome = 1"}, NEGA),
    ("mcp__supabase__execute_sql", {"query": "with d as (delete from x returning *) select * from d"}, NEGA),
    ("mcp__supabase__execute_sql", {"query": "select cron.schedule('a','* * * * *','select 1')"}, NEGA),
    ("mcp__supabase__execute_sql", {"query": "DO $$ BEGIN PERFORM 1; END $$"}, NEGA),
    ("mcp__supabase__execute_sql", {"query": "select 1; drop table contatos"}, NEGA),
    ("mcp__claude_ai_Supabase__execute_sql", {"query": "insert into x values (1)"}, NEGA),
    ("mcp__claude_ai_Supabase__apply_migration", {"name": "x", "query": "create table t()"}, PERGUNTA),
    ("mcp__supabase__deploy_edge_function", {}, PERGUNTA),
    # Supabase: terminal
    ("Bash", {"command": "npx supabase db push"}, PERGUNTA),
    ("Bash", {"command": "supabase db reset"}, LIVRE),
    ("Bash", {"command": "supabase db reset --linked"}, PERGUNTA),
    ("Bash", {"command": "psql $DATABASE_URL -c 'select 1'"}, PERGUNTA),
    ("Bash", {"command": "npm run test"}, LIVRE),
    # n8n: MCP
    ("mcp__n8n__search_workflows", {}, LIVRE),
    ("mcp__claude_ai_n8n__get_workflow_details", {}, LIVRE),
    ("mcp__n8n__get_workflow_versions_diff", {}, LIVRE),
    ("mcp__n8n__validate_workflow", {}, LIVRE),
    ("mcp__n8n-docs__searchDocumentation", {"query": "error trigger"}, LIVRE),
    ("mcp__n8n-docs__getPage", {"url": "https://docs.n8n.io/"}, LIVRE),
    ("mcp__n8n__execute_workflow", {}, PERGUNTA),
    ("mcp__n8n__publish_workflow", {}, PERGUNTA),
    ("mcp__n8n__test_workflow", {}, PERGUNTA),
    ("mcp__n8n__delete_data_table_rows", {}, PERGUNTA),
    # n8n: terminal
    ("Bash", {"command": 'curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" https://app.automacao.exemplo.com.br/api/v1/workflows/abc'}, LIVRE),
    ("Bash", {"command": 'curl -X PUT -H "X-N8N-API-KEY: $N8N_API_KEY" https://app.automacao.exemplo.com.br/api/v1/workflows/abc -d @w.json'}, PERGUNTA),
    ("Bash", {"command": 'curl -s -X POST https://app.automacao.exemplo.com.br/api/v1/workflows/abc/activate -H "X-N8N-API-KEY: k"'}, PERGUNTA),
    ("Bash", {"command": "curl https://app.automacao.exemplo.com.br/webhook/enviozap"}, PERGUNTA),
    ("PowerShell", {"command": "Invoke-RestMethod -Uri https://n8n.cliente.com/api/v1/executions/5/retry -Method Post"}, PERGUNTA),
    ("Bash", {"command": "n8n-cli workflow list"}, LIVRE),
    ("Bash", {"command": "n8n-cli workflow update abc --file w.json"}, PERGUNTA),
    ("Bash", {"command": "npm run dev -- --data x"}, LIVRE),
    # Alarmes falsos reais (28/09): não podem pedir confirmação
    ("Bash", {"command": "docker exec supabase_db_lembretes-local psql -U postgres -At -c \"select count(*) from public.whatsapp_instances\""}, LIVRE),
    ("Bash", {"command": "psql postgresql://postgres:postgres@127.0.0.1:54322/postgres -c 'delete from x'"}, LIVRE),
    ("Bash", {"command": 'S="C:/Users/x/Temp/claude/C--Users-dono-Projetos-meu-projeto/4cacbeb6"; grep -rn "N8N" "$S" | head -d 5'}, LIVRE),
    ("Bash", {"command": 'cd wt-lembretes; F=supabase/tests/x.sql; grep -F "n8n" "$F"'}, LIVRE),
    ("Bash", {"command": 'K="sb_publishable_chave_de_exemplo"; curl -s -X POST "https://abcdefghijklmnopqrst.supabase.co/graphql/v1" -H "apikey: $K" -d "{}"'}, LIVRE),
    ("Bash", {"command": 'cd "$(mktemp -d)"; curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "https://app.automacao.exemplo.com.br/api/v1/executions/1?includeData=true" -o e.json; python -c "import json; print(1)" -d'}, LIVRE),
    ("Bash", {"command": 'M="$LOCALAPPDATA/meu-projeto/n8n-mirror"; grep -l "abc" "$M"/*.json | while read f; do python -c "import json"; done'}, LIVRE),
    ("Bash", {"command": 'cat >> docs/plano.md <<EOF\nO workflow do n8n vai executar o update e delete da fila.\nEOF'}, LIVRE),
    ("mcp__supabase__execute_sql", {"query": "set statement_timeout='110s'; with v as (select company_id, count(*) n from chat_conversa group by 1) select * from v"}, LIVRE),
    ("mcp__supabase__execute_sql", {"query": "begin; set local role anon; select count(*) from follow_ups; rollback;"}, LIVRE),
    ("mcp__supabase__execute_sql", {"query": "select set_config('request.jwt.claims', '{\"sub\":\"abc\"}', true); select count(*) from follow_ups"}, LIVRE),
    ("mcp__supabase__execute_sql", {"query": "create or replace function pg_temp.j(t text) returns jsonb language sql as $$ select t::jsonb $$; select pg_temp.j('{}')"}, LIVRE),
    ("Bash", {"command": "which python psql docker 2>&1"}, LIVRE),
    ("Bash", {"command": 'echo "psql=${PIPESTATUS[1]}"'}, LIVRE),
    # ...e os perigosos parecidos continuam presos
    ("Bash", {"command": "psql \\\n  -h db.abcdefghijklmnopqrst.supabase.co -U postgres -c 'select 1'"}, PERGUNTA),
    ("Bash", {"command": "PGPASSWORD=x psql -h db.abc.supabase.co -c 'drop table x'"}, PERGUNTA),
    ("Bash", {"command": "psql \"$DATABASE_URL\" -c 'select 1'"}, PERGUNTA),
    ("Bash", {"command": "cd x && psql -h db.abcdefghijklmnopqrst.supabase.co -U postgres -c 'delete from x'"}, PERGUNTA),
    ("Bash", {"command": "npx supabase functions deploy followup-motor"}, PERGUNTA),
    ("Bash", {"command": "cd wt && npx supabase migration up --linked"}, PERGUNTA),
    ("Bash", {"command": 'curl -s "https://app.automacao.exemplo.com.br/webhook/enviozap?to=5582"'}, PERGUNTA),
    ("Bash", {"command": 'curl -s -X POST -H "X-N8N-API-KEY: $K" "$N8N_URL/api/v1/workflows/abc/activate"'}, PERGUNTA),
    ("Bash", {"command": "npx n8n-cli workflow activate abc"}, PERGUNTA),
    ("mcp__supabase__execute_sql", {"query": "set statement_timeout='60s'; delete from follow_ups where id = 1"}, NEGA),
    ("mcp__supabase__execute_sql", {"query": "set local role service_role; select 1"}, NEGA),
    ("mcp__supabase__execute_sql", {"query": "select set_config('role', 'service_role', true)"}, NEGA),
    ("mcp__supabase__execute_sql", {"query": "begin; insert into x values (1); commit;"}, NEGA),
    ("mcp__supabase__execute_sql", {"query": "create or replace function public.x() returns int language sql as $$ select 1 $$"}, NEGA),    # Furos fechados em 29/09 (função que grava, API do Supabase, scripts)
    ("mcp__supabase__execute_sql", {"query": "select public.funcao_teste_que_grava(1)"}, PERGUNTA),
    ("mcp__supabase__execute_sql", {"query": "select public.funcao_teste_que_le(1)"}, LIVRE),
    ("mcp__supabase__execute_sql", {"query": "select count(*), now() from contatos"}, LIVRE),
    ("Bash", {"command": "curl -X POST https://abc.supabase.co/rest/v1/contatos -H 'apikey: x' -d '{}'"}, PERGUNTA),
    ("Bash", {"command": "curl -X DELETE 'https://abc.supabase.co/rest/v1/contatos?id=eq.1'"}, PERGUNTA),
    ("Bash", {"command": "curl -s 'https://abc.supabase.co/rest/v1/contatos?select=id' -H 'apikey: x'"}, LIVRE),
    ("Bash", {"command": "curl -X POST http://127.0.0.1:54321/rest/v1/contatos -d '{}'"}, LIVRE),
    ("Bash", {"command": "curl -X POST \"$SUPABASE_URL/functions/v1/followup-motor\" -d '{}'"}, PERGUNTA),
    ("Bash", {"command": "python -c \"import requests; requests.delete('https://abc.supabase.co/rest/v1/x')\""}, PERGUNTA),
    ("Bash", {"command": "node _script_teste_grava.js"}, PERGUNTA),
    ("Bash", {"command": "node _script_teste_le.js"}, LIVRE),
    ("Bash", {"command": "node scripts/nao-existe.js"}, LIVRE),
]


PASTA_TESTE = pathlib.Path(__file__).with_name("_pasta_teste")


def montar_pasta_teste():
    """Projeto falso: uma função que grava, uma que lê e dois scripts."""
    (PASTA_TESTE / "supabase" / "migrations").mkdir(parents=True, exist_ok=True)
    (PASTA_TESTE / ".claude").mkdir(exist_ok=True)
    (PASTA_TESTE / ".claude" / "konoha.json").write_text('{"n8n_hosts": ["automacao.exemplo.com.br"]}', encoding="utf-8")
    (PASTA_TESTE / "supabase" / "migrations" / "0001_teste.sql").write_text(
        "create or replace function public.funcao_teste_que_grava(x int) returns void language plpgsql as $$\n"
        "begin delete from contatos where id = x; end $$;\n"
        "create function public.funcao_teste_que_le(x int) returns int language sql stable as $f$ select 1 $f$;\n",
        encoding="utf-8",
    )
    (PASTA_TESTE / "_script_teste_grava.js").write_text(
        "const s = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);\n"
        "await s.from('contatos').delete().eq('id', 1);\n", encoding="utf-8")
    (PASTA_TESTE / "_script_teste_le.js").write_text(
        "const s = createClient(process.env.SUPABASE_URL, k);\n"
        "await s.from('contatos').select('*');\n", encoding="utf-8")


def casos_de_traducao() -> int:
    """O que o dono lê na pergunta: o grave aparece e vem marcado."""
    falhas = 0
    exemplos = [
        ("drop table public.contatos", True, "APAGA a tabela contatos inteira"),
        ("alter table contatos drop column telefone", True, "APAGA a coluna telefone da tabela contatos"),
        ("alter table contatos add column apelido text", False, "acrescenta a coluna apelido na tabela contatos"),
        ("delete from follow_ups", True, "APAGA TODAS as linhas da tabela follow_ups"),
        ("delete from follow_ups where id = 1", True, "apaga linhas da tabela follow_ups (com filtro)"),
        ("alter table x disable row level security", True, "DESLIGA a proteção por empresa"),
        ("create policy p on x for select to anon using (true)", True, "vale para qualquer um"),
        ("create table public.novas (id uuid primary key); create index on novas (id);", False, "cria a tabela novas"),
        ("create or replace function public.f() returns int language sql as $$ delete from x $$", False, "cria ou troca a função f"),
        ("grant select on public.x to anon", True, "deixa quem não está logado usar a tabela x"),
        ("revoke execute on function public.f(uuid, text) from public, anon, authenticated", False, "tira de todo mundo, quem não está logado, usuários logados o acesso à função f"),
    ]
    for sql, grave_esperado, trecho in exemplos:
        texto, grave = trava.traduzir.resumo_migration(sql, "teste")
        if grave != grave_esperado or trecho not in texto:
            falhas += 1
            print(f"FALHOU tradução: {sql!r} -> grave={grave}\n{texto}")
    texto, grave = trava.traduzir.resumo_funcao({"name": "webhook-x", "verify_jwt": False})
    if not grave or "ABERTA" not in texto:
        falhas += 1
        print("FALHOU tradução: função aberta sem login")
    print(f"{len(exemplos) + 1 - falhas}/{len(exemplos) + 1} traduções certas")
    return falhas


def main() -> int:
    montar_pasta_teste()
    falhas = casos_de_traducao()
    for ferramenta, entrada, esperado in CASOS:
        resultado = trava.decidir({"tool_name": ferramenta, "tool_input": entrada, "cwd": str(PASTA_TESTE)})
        obtido = resultado[0] if resultado else None
        if obtido != esperado:
            falhas += 1
            print(f"FALHOU: {ferramenta} {entrada} -> esperado {esperado}, obtido {obtido}")
    print(f"{len(CASOS) - falhas}/{len(CASOS)} casos passaram")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
