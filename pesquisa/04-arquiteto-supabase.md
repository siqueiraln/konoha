# Pesquisa: regras de arquitetura para apps React + Vite + Supabase

Data da pesquisa: 2026-09-26. Todas as páginas abaixo foram abertas nesta data.
Legenda: **[fato]** = está na página linkada. **[dedução]** = conclusão minha a partir dos fatos, não escrita literalmente na fonte.

---

## 1. RLS: segurança e desempenho

### Segurança
- [fato] Uma tabela em schema exposto **sem RLS** pode ser lida e escrita por qualquer role que tenha grant nela. ([RLS](https://supabase.com/docs/guides/database/postgres/row-level-security))
- [fato] Grants e policies são camadas separadas: o grant decide **se** a role pode executar a operação na tabela; a policy decide **quais linhas**. ([RLS](https://supabase.com/docs/guides/database/postgres/row-level-security), [changelog 45329](https://supabase.com/changelog/45329-breaking-change-tables-not-exposed-to-data-and-graphql-api-automatically))
- [fato] Sempre declare a role da policy com `to` (ex.: `to authenticated`) para a policy não rodar para roles como `anon`. ([RLS](https://supabase.com/docs/guides/database/postgres/row-level-security))
- [fato] Crie **uma policy por operação** (SELECT, INSERT, UPDATE, DELETE) em vez de combinar. ([RLS](https://supabase.com/docs/guides/database/postgres/row-level-security))
- [fato] Em UPDATE, use `using` (linhas existentes) **e** `with check` (linha resultante) para impedir, por exemplo, que o usuário transfira a linha para outro dono. ([RLS](https://supabase.com/docs/guides/database/postgres/row-level-security), [agent skill supabase](https://raw.githubusercontent.com/supabase/agent-skills/main/skills/supabase/SKILL.md))
- [fato] UPDATE precisa também de uma policy de SELECT; sem ela o update falha em silêncio. ([agent skill supabase](https://raw.githubusercontent.com/supabase/agent-skills/main/skills/supabase/SKILL.md))
- [fato] `to authenticated` sozinho é autenticação, não autorização: coloque o predicado de dono no `using`. ([agent skill supabase](https://raw.githubusercontent.com/supabase/agent-skills/main/skills/supabase/SKILL.md))
- [fato] Não use `user_metadata` / `raw_user_meta_data` em policies, porque o próprio usuário pode alterá-lo; use `app_metadata`. ([RLS](https://supabase.com/docs/guides/database/postgres/row-level-security), [agent skill](https://raw.githubusercontent.com/supabase/agent-skills/main/skills/supabase/SKILL.md))
- [fato] `auth.role()` está depreciado; use a cláusula `TO`. ([agent skill](https://raw.githubusercontent.com/supabase/agent-skills/main/skills/supabase/SKILL.md))
- [fato] Views ignoram RLS por padrão; no Postgres 15+ crie com `with (security_invoker = true)`. ([RLS](https://supabase.com/docs/guides/database/postgres/row-level-security), [agent skill](https://raw.githubusercontent.com/supabase/agent-skills/main/skills/supabase/SKILL.md))
- [fato] Não adicione `SECURITY DEFINER` para "consertar" permissão: isso remove o controle de acesso em silêncio. Prefira `SECURITY INVOKER`. Funções SECURITY DEFINER em `public` podem ser chamadas por todas as roles; mantenha-as em schema não exposto e com checagem de `auth.uid()`. ([agent skill](https://raw.githubusercontent.com/supabase/agent-skills/main/skills/supabase/SKILL.md))
- [fato] Excluir um usuário não invalida os tokens dele; para apps sensíveis, faça sign out e use expiração curta do JWT. As claims do JWT só se atualizam no refresh do token. ([agent skill](https://raw.githubusercontent.com/supabase/agent-skills/main/skills/supabase/SKILL.md))
- [fato] Escreva testes pgTAP para cada tabela protegida, verificando tanto as operações permitidas quanto as negadas, para todas as roles. ([RLS](https://supabase.com/docs/guides/database/postgres/row-level-security))

### Desempenho ([guia oficial de desempenho de RLS](https://supabase.com/docs/guides/troubleshooting/rls-performance-and-best-practices-Z5Jjwv))
- [fato] **Crie índice** nas colunas usadas pela policy que não sejam PK nem unique. No exemplo da doc, `auth.uid() = user_id` passou de 171 ms para menos de 0,1 ms.
- [fato] **Envolva a função em select**: `(select auth.uid()) = user_id`. Isso gera um initPlan que faz cache do resultado por statement. Ganhos citados: de 179 ms para 9 ms e de 178.000 ms para 12 ms. Só vale quando o resultado não depende da linha.
- [fato] **Repita o filtro na query** do cliente (ex.: `.eq('user_id', userId)`), além da RLS: de 171 ms para 9 ms.
- [fato] Use **funções security definer** para consultar outras tabelas sem disparar a RLS delas: de 11.000 ms para 7 ms.
- [fato] **Evite joins na policy**: reescreva como `coluna IN (select ... )` / `ANY`. No exemplo, `team_id in (select team_id from team_user where ...)` foi de 9.000 ms para 20 ms.
- [fato] **Especifique `TO authenticated`**: para usuários anon, a query caiu de 170 ms para menos de 0,1 ms.
- [dedução] Existe uma tensão: o guia de desempenho recomenda security definer para joins, mas o agent skill proíbe usá-lo para "consertar permissão". Regra para o Arquiteto: security definer só como helper de leitura, em schema **não exposto** (ex.: `private`), com `set search_path = ''`, `revoke execute ... from public/anon` e checagem de `auth.uid()` dentro da função.

### Tabelas expostas pela API (mudança recente)
- [fato] Breaking change anunciada em 2026-04-28: tabelas novas em `public` deixam de ser expostas automaticamente às APIs Data e GraphQL. Cronograma: opt-in disponível em 2026-04-28, padrão para projetos novos em **2026-05-30** e aplicado a **todos os projetos existentes em 2026-10-30**. ([changelog 45329](https://supabase.com/changelog/45329-breaking-change-tables-not-exposed-to-data-and-graphql-api-automatically))
- [fato] Toda tabela exposta precisa de `grant` explícito para `anon` / `authenticated` / **`service_role`** (o service_role também deixa de herdar), mais `enable row level security` e as policies, **na mesma migration**. Sem o grant, o PostgREST retorna o erro `42501 permission denied`, com um hint indicando o GRANT que falta. ([changelog 45329](https://supabase.com/changelog/45329-breaking-change-tables-not-exposed-to-data-and-graphql-api-automatically))
- [fato] Em projetos existentes, as tabelas novas ainda recebem SELECT/INSERT/UPDATE/DELETE automaticamente para anon, authenticated e service_role, e a Supabase está tornando essa exposição opt-in. Um schema dedicado para a API facilita a auditoria, e um schema `private` não fica acessível pela Data API. ([Securing your API](https://supabase.com/docs/guides/api/securing-your-api))
- [fato] Desde a mudança de 2026-02-17, a Data API deixou de devolver o spec OpenAPI via chave anon (2026-03-11 para projetos novos, 2026-04-08 para todos). ([changelog](https://supabase.com/changelog))

---

## 2. Onde colocar a lógica

- [fato] Para operações com muitos dados, use Database Functions, que rodam dentro do banco e podem ser chamadas via REST/GraphQL. Para baixa latência, use Edge Functions, que são distribuídas globalmente e escritas em TypeScript. ([Database Functions](https://supabase.com/docs/guides/database/functions))
- [fato] O padrão das funções é `security invoker`, e essa é a boa prática. Com definer, é obrigatório fixar o `search_path`. Com `search_path = ''`, qualifique todos os objetos (ex.: `public.tabela`). ([Database Functions](https://supabase.com/docs/guides/database/functions))
- [fato] O Postgres recomenda, em funções SECURITY DEFINER, excluir do search_path os schemas graváveis, colocar `pg_temp` por último e fazer `REVOKE ALL ... FROM PUBLIC` + `GRANT EXECUTE` só para quem precisa. ([Postgres 18 CREATE FUNCTION](https://www.postgresql.org/docs/current/sql-createfunction.html))
- [fato] Chamada do cliente: `supabase.rpc('fn')`; para funções somente leitura, use a opção `{ get: true }`. ([ref rpc](https://supabase.com/docs/reference/javascript/rpc))
- [fato] **Transações**: um mantenedor do PostgREST (steve-chavez, 2025-02-13) disse que uma interface genérica de transação no cliente "não é prioridade", porque o `rpc` funciona bem. A alternativa citada é Edge Function com ORM. ([discussion #526](https://github.com/orgs/supabase/discussions/526))
- [dedução] Cada chamada `supabase.from(...)` é uma requisição HTTP independente. Uma operação que precisa ser tudo-ou-nada em várias tabelas deve virar uma função Postgres chamada por `rpc` (a função roda numa única transação; [Postgres](https://www.postgresql.org/docs/current/sql-createfunction.html)). A página de referência do `rpc` não fala de transações.
- [fato] Casos de uso oficiais das Edge Functions: endpoints HTTP de baixa latência, recebimento de webhooks (Stripe, GitHub), geração de imagens/OG, orquestração de chamadas a LLMs externos, e-mails transacionais e bots. Elas devem ser curtas e idempotentes, tratar o Postgres como serviço remoto com pool, e jobs longos e pesados devem ir para workers. ([Edge Functions](https://supabase.com/docs/guides/functions))
- [dedução] Heurística para o Arquiteto:
  - CRUD de um único recurso com regra por linha: cliente direto + RLS.
  - Várias escritas atômicas ou regra de negócio sobre dados: função Postgres (`security invoker`) via `rpc`.
  - Segredo de terceiro, webhook, chamada externa ou LLM: Edge Function.
  - Tarefa agendada: Cron.

---

## 3. Security Advisor / Performance Advisor (linter)
Fonte: [Database Advisors](https://supabase.com/docs/guides/database/database-advisors). [fato] Checagens:
- 0001 unindexed_foreign_keys: FK sem índice.
- 0002 auth_users_exposed: view expõe `auth.users`.
- 0003 auth_rls_initplan: policy reavalia a função por linha (falta o `select`).
- 0004 no_primary_key: tabela sem PK.
- 0005 unused_index: índice nunca usado.
- 0006 multiple_permissive_policies: várias policies permissivas.
- 0007 policy_exists_rls_disabled: policy existe, mas a RLS está desligada.
- 0008 rls_enabled_no_policy: RLS ligada sem nenhuma policy.
- 0009 duplicate_index: índice duplicado.
- 0010 security_definer_view: view security definer.
- 0011 function_search_path_mutable: função sem search_path fixo.
- 0012 auth_allow_anonymous_sign_ins: sign-in anônimo habilitado.
- 0013 rls_disabled_in_public: tabela em `public` sem RLS.
- 0014 extension_in_public: extensão instalada em `public`.
- 0015 rls_references_user_metadata: policy usa user_metadata.
- 0016 materialized_view_in_api: materialized view exposta na API.
- 0017 foreign_table_in_api: foreign table exposta na API.
- 0018 unsupported_reg_types: tipos reg* que bloqueiam upgrade.
- 0019 insecure_queue_exposed_in_api: fila exposta sem controle de acesso.
- 0020 table_bloat: inchaço de tabela.
- 0021 fkey_to_auth_unique: FK para constraint unique de `auth`.
- 0022 extension_versions_outdated: extensão desatualizada.
- 0023 sensitive_columns_exposed: colunas sensíveis expostas.
- 0024 permissive_rls_policy: policy com `using (true)`.
- 0025 public_bucket_allows_listing: bucket público permite listagem.
- 0026 e 0027: tabela visível na introspecção do pg_graphql para anon / authenticated.
- 0028 e 0029: função SECURITY DEFINER executável por anon / authenticated.
- 0030 autovacuum_disabled: autovacuum desligado.
- [fato] Como rodar: `supabase db advisors` (CLI), Dashboard (Security/Performance Advisor), MCP `get_advisors` (type security/performance) ou Management API `/v1/projects/{ref}/security-advisors` e `/performance-advisors`. ([Database Advisors](https://supabase.com/docs/guides/database/database-advisors))
- [fato] Em 2026-09-18 foram lançados os Health Check Advisors, com taxa de erro de Auth, Storage, Edge Functions e Data APIs. ([changelog](https://supabase.com/changelog))

---

## 4. Migrations, ambientes e tipos

- [fato] Fluxo com a CLI: `supabase migration new <nome>`, `supabase db diff -f <nome>` (captura mudanças feitas no Dashboard local), `supabase db reset` (reaplica as migrations e o `seed.sql`), `supabase link` e `supabase db push` (com `--include-seed` opcional). Para recuperar sincronia: `migration list`, `db pull` e `migration repair`. ([Database migrations](https://supabase.com/docs/guides/deployment/database-migrations))
- [fato] Em equipe: "Never change the remote database directly". Cada dev cria migrations na sua branch, testa com `db reset` e commita, e **só uma pessoa** roda `db push`. ([Database migrations](https://supabase.com/docs/guides/deployment/database-migrations))
- [fato] Schemas declarativos: edite `supabase/schemas/` e rode `supabase db schema declarative sync` (engine pg-delta). O changelog trata o pg-delta como alpha público. ([Database migrations](https://supabase.com/docs/guides/deployment/database-migrations), [changelog edge/CLI](https://supabase.com/changelog?tags=edge+functions))
- [fato] Regras do agent skill:
  - Crie o arquivo com `supabase migration new`; não invente nomes de arquivo.
  - Itere com `execute_sql` / `supabase db query` e depois faça `db pull`.
  - Não use `apply_migration` para iterar.
  - Descubra comandos com `--help`.
  - Na CI, use `SUPABASE_ACCESS_TOKEN` com escopo reduzido.
  ([agent skill](https://raw.githubusercontent.com/supabase/agent-skills/main/skills/supabase/SKILL.md))
- [fato] Branching: *preview branches* são efêmeras e apagadas ao fazer merge/fechar o PR. *Persistent branches* servem para staging/QA. A integração com GitHub faz deploy a cada commit, e a criação pelo Dashboard está em beta. Branches novas **não copiam dados nem objetos de Storage** por padrão (há seed ou a opção "Include data"). ([Branching](https://supabase.com/docs/guides/deployment/branching))
- [fato] Tipos: `npx supabase gen types typescript --project-id "$PROJECT_REF" --schema public > database.types.ts` ou `--local`. Use com `createClient<Database>(url, PUBLISHABLE_KEY)`. Helpers disponíveis: `Tables<'x'>`, `Enums` e `QueryData` (para queries com join). A doc sugere uma GitHub Action diária para atualizar. ([Generating types](https://supabase.com/docs/guides/api/rest/generating-types))

---

## 5. Chaves de API

- [fato] Existem quatro tipos:
  - publishable (`sb_publishable_...`): pode ser exposta e respeita a RLS.
  - secret (`sb_secret_...`): só no backend e ignora a RLS.
  - legados `anon` e `service_role`, baseados em JWT.
  ([API keys](https://supabase.com/docs/guides/api/api-keys))
- [fato] Cronograma: preview em junho de 2025. Desde 2025-11-01, projetos novos e restaurados não têm mais anon/service_role. Os legados serão removidos no fim de 2026 (a discussão diz "TBC"). ([discussion #29260](https://github.com/orgs/supabase/discussions/29260), [API keys](https://supabase.com/docs/guides/api/api-keys))
- [fato] O que muda na prática:
  - Publishable e secret **não são JWT** e não podem ir no header `Authorization: Bearer`; vão no header `apikey`.
  - A secret key retorna 401 no navegador (detecção por User-Agent).
  - Conexões Realtime sem usuário logado duram no máximo 24 h.
  - Database Webhooks e `pg_net` devem mandar a secret no header `apikey`.
  ([discussion #29260](https://github.com/orgs/supabase/discussions/29260), [Migrating to new keys](https://supabase.com/docs/guides/getting-started/migrating-to-new-api-keys), [API keys](https://supabase.com/docs/guides/api/api-keys))
- [fato] Nas Edge Functions, com as chaves novas: `verify_jwt = false` + SDK `@supabase/server`. As env vars `SUPABASE_PUBLISHABLE_KEYS` e `SUPABASE_SECRET_KEYS` são objetos JSON. ([Migrating to new keys](https://supabase.com/docs/guides/getting-started/migrating-to-new-api-keys))
- [fato] Para CLI, MCP e scripts, use tokens pessoais com escopo reduzido. ([agent skill](https://raw.githubusercontent.com/supabase/agent-skills/main/skills/supabase/SKILL.md))

---

## 6. Edge Functions

- [fato] Limites:
  - Memória: 256 MB.
  - Wall clock: 150 s no Free e 400 s nos planos pagos.
  - CPU: 2 s por requisição.
  - Idle timeout: 150 s (depois disso, 504).
  - Tamanho do bundle: 20 MB (CLI) ou 5 MB (bundle no servidor).
  - Quantidade de funções: 100 (Free), 1.000 (Pro), 2.000 (Team).
  - Secrets: até 100, com no máximo 48 KiB cada.
  - Portas 25 e 587 bloqueadas.
  - Sem Web Workers e sem `vm`; sem libs multithread (sharp, libvips).
  - Chamadas recursivas: 30 por trace em 60 s.
  ([Limits](https://supabase.com/docs/guides/functions/limits))
- [fato] Auth: `@supabase/server` (beta público, anunciado em 2026-05-06) traz o `withSupabase({ auth: 'user' | 'secret' | 'publishable' | 'none' })`, que entrega `ctx.supabase` (respeita RLS), `ctx.supabaseAdmin` (ignora RLS) e `ctx.userClaims`. Também aceita chave nomeada, como `'secret:automations'`, e já trata CORS. ([Functions auth](https://supabase.com/docs/guides/functions/auth), [blog @supabase/server](https://supabase.com/blog/introducing-supabase-server))
- [fato] Não leia a chave do ambiente dentro da Edge Function; use `@supabase/server`. ([API keys](https://supabase.com/docs/guides/api/api-keys))
- [fato] `verify_jwt` vem ligado por padrão. Desligue para endpoints públicos e webhooks, mas nesse caso a verificação passa a ser responsabilidade sua. ([Functions auth](https://supabase.com/docs/guides/functions/auth), [discussion #29260](https://github.com/orgs/supabase/discussions/29260))
- [fato] Segredos:
  - Local: `supabase/functions/.env`, que deve estar no `.gitignore`.
  - Produção: `supabase secrets set` ou o Dashboard.
  - Nomes que começam com `SUPABASE_` são reservados.
  - Já vêm disponíveis: `SUPABASE_URL`, `SUPABASE_DB_URL`, `SUPABASE_PUBLISHABLE_KEYS`, `SUPABASE_SECRET_KEYS` e `SUPABASE_JWKS`.
  ([Secrets](https://supabase.com/docs/guides/functions/secrets))
- [fato] Background tasks: `EdgeRuntime.waitUntil(promise)`, sem `await`, continuam sujeitas aos limites de wall clock, CPU e memória. ([Background tasks](https://supabase.com/docs/guides/functions/background-tasks))
- [fato] O runtime é compatível com Deno 2.1 em todas as regiões (fallback `forceDenoVersion=1`) e aceita `deno.json` por função. ([changelog edge](https://supabase.com/changelog?tags=edge+functions))

### Cron, Realtime, Storage (complementos)
- [fato] Cron (pg_cron) roda SQL, funções ou HTTP (ex.: chamar uma Edge Function). Recomendação oficial: no máximo 8 jobs simultâneos e até 10 min por job. ([Cron](https://supabase.com/docs/guides/cron))
- [fato] Realtime: canais privados exigem desligar "Allow public access", criar RLS em `realtime.messages` e usar `private: true` no cliente. Postgres Changes respeita a RLS da tabela. RLS complexa aumenta a latência de conexão, e as policies ficam em cache durante a conexão. ([Realtime authorization](https://supabase.com/docs/guides/realtime/authorization))
- [fato] Storage: RLS em `storage.objects`; sem policy, nenhum upload é permitido. Upload precisa de INSERT; upsert precisa de INSERT + SELECT + UPDATE. Helpers: `storage.foldername()`. A service key ignora tudo. ([Storage access control](https://supabase.com/docs/guides/storage/security/access-control))

---

## 7. Supabase Agent Skills / orientação para IA

- [fato] Instalação: `npx skills add supabase/agent-skills` (ou `--skill supabase` / `--skill supabase-postgres-best-practices`, `--global`, `--all`), ou como plugin do Claude Code (`claude plugin install supabase@supabase-agent-skills`). A doc pede para rodar `npx skills update` com frequência. ([AI skills](https://supabase.com/docs/guides/getting-started/ai-skills.md), [repo](https://github.com/supabase/agent-skills))
- [fato] São duas skills:
  - **supabase**: cobre todos os produtos. Use em tarefas com Supabase, auth/JWT/RLS e debugging.
  - **supabase-postgres-best-practices**: carregue **antes** de desenhar schema, criar tabelas/colunas, policies, índices, triggers e funções, ou diagnosticar desempenho.
  ([AI skills](https://supabase.com/docs/guides/getting-started/ai-skills.md))
- [fato] Categorias do best-practices, por prioridade: Query Performance (CRITICAL), Connection Management (CRITICAL), Security & RLS (CRITICAL), Schema Design (HIGH), Concurrency & Locking (MEDIUM-HIGH), Data Access (MEDIUM), Monitoring (LOW-MEDIUM), Advanced (LOW). ([SKILL.md best practices](https://raw.githubusercontent.com/supabase/agent-skills/main/skills/supabase-postgres-best-practices/SKILL.md))
- [fato] As 34 referências incluem, por exemplo, `schema-foreign-key-indexes`, `schema-primary-keys`, `schema-lowercase-identifiers`, `data-n-plus-one`, `data-pagination`, `lock-short-transactions`, `lock-skip-locked`, `security-rls-basics`, `security-rls-performance` e `security-privileges`. ([pasta references](https://github.com/supabase/agent-skills/tree/main/skills/supabase-postgres-best-practices/references))
- [fato] Regras da skill `supabase` ([SKILL.md](https://raw.githubusercontent.com/supabase/agent-skills/main/skills/supabase/SKILL.md)):
  - Verifique na doc e no changelog atuais antes de implementar.
  - Teste com uma query antes de dar como pronto.
  - Se falhar 2–3 vezes, mude de abordagem.
  - Tabelas novas podem não estar expostas: confira os grants.
  - Ligue RLS em toda tabela de schema exposto.
  - Passe o checklist de segurança sempre que a tarefa tocar em auth, RLS, views, storage ou dados de usuário.
  - Fixe as versões dos pacotes e commite o lockfile.
  - Consulte a doc nesta ordem: MCP `search_docs`, depois URLs `.md`, depois busca na web.
  - Antes de diagnosticar, busque a doc de Monitoring & Debugging.
  - As regras de segurança listadas nas seções 1, 4 e 5 também vêm desta skill.
- [fato] O próprio changelog dos grants recomenda que ferramentas de IA adotem os agent skills, que "handle grants correctly". ([changelog 45329](https://supabase.com/changelog/45329-breaking-change-tables-not-exposed-to-data-and-graphql-api-automatically))

---

## 8. Novidades dos últimos 12 meses (datas conforme o [changelog](https://supabase.com/changelog))
- [fato] 2025-11-01: projetos novos e restaurados sem chaves legadas. ([#29260](https://github.com/orgs/supabase/discussions/29260))
- [fato] 2026-02-17: fim do spec OpenAPI via chave anon.
- [fato] 2026-04-28: breaking change que torna a exposição de tabelas opt-in; **enforcement em todos os projetos em 2026-10-30**. ([45329](https://supabase.com/changelog/45329-breaking-change-tables-not-exposed-to-data-and-graphql-api-automatically))
- [fato] 2026-05-06: `@supabase/server` (beta). ([blog](https://supabase.com/blog/introducing-supabase-server))
- [fato] 2026-05-12: fim do suporte ao Postgres 14 em 2026-07-01. 2026-05-08: Node 20 deixa de ser suportado pelas libs em 2026-06-30.
- [fato] 2026-05-28: Passkeys no Auth (beta).
- [fato] 2026-07-10: supabase-js encerra o suporte a TS 4.7–4.9 em 2027-01-31.
- [fato] 2026-07-14: o schema `realtime` passa a ser bloqueado para alterações.
- [fato] 2026-07-22: pin de versão de extensão depreciado (a versão passa a ser ignorada a partir de 2026-08-05).
- [fato] 2026-09-18: Health Check Advisors. 2026-09-25: Postgres 15.19/17.11 exige ação em índices ltree/btree_gist e em dados pgcrypto com cifra legada.
- [fato] Datas não confirmadas nesta pesquisa: pg-delta (schema declarativo) em alpha, OAuth 2.1 server (beta, 2025-08-19) e Deno 2.1 em todas as regiões. ([changelog edge](https://supabase.com/changelog?tags=edge+functions))

---

## Onde procurei e não achei
- Na [referência do `rpc`](https://supabase.com/docs/reference/javascript/rpc) e na [doc de Database Functions](https://supabase.com/docs/guides/database/functions) não há uma frase explícita de que "supabase-js não tem transação multi-chamada". A posição oficial está só na [discussion #526](https://github.com/orgs/supabase/discussions/526), e a atomicidade da função vem da doc do Postgres.
- Na [página de Branching](https://supabase.com/docs/guides/deployment/branching): nada sobre preço, limites ou "Branching 2.0".
- Na [página de AI skills](https://supabase.com/docs/guides/getting-started/ai-skills.md): nenhuma data de lançamento.
- Data exata da remoção das chaves legadas: as fontes dizem só "end of 2026" / "TBC".
- O conteúdo de cada arquivo `references/*.md` do best-practices não foi aberto; li só os nomes e o SKILL.md.
- Na [doc de Cron](https://supabase.com/docs/guides/cron) não fica claro se jobs com intervalo abaixo de 1 minuto são suportados na prática.
- A página de funções não traz uma matriz oficial de decisão do tipo "quando usar RLS direto vs RPC vs Edge Function". A heurística da seção 2 é dedução.
