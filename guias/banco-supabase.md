# Guia: banco de dados e Supabase

Lido por seção: leia só a que a tarefa toca. Fatos do Supabase de 2026-09-26; antes de decidir algo que dependa deles, confira com `search_docs`.

**MCP do Supabase:** `search_docs` e a leitura do banco real (`list_tables`, `list_migrations`, `list_edge_functions`, `get_advisors`) são as fontes principais; leitura é livre. Confirme a qual projeto o MCP está ligado antes de usar. Alteração em produção só com autorização do dono para aquela mudança (referência do Tech Lead §4.1), aplicada pelo Tech Lead na conversa principal; o Implementador prepara. A trava `~/.claude/empresa-agentes/hooks/proteger-banco.py` bloqueia `execute_sql` que grava e pede o dono em `apply_migration`, `deploy_edge_function` e comandos que alteram o remoto.

## 1. Modelagem
- Modele pela forma real do dado: em projeto existente, consulte o banco antes de supor ("1 linha por mensagem" não é "1 linha por conversa").
- Tabela comum com atualização é o padrão. Histórico só onde o negócio precisa do passado (etapa, status, responsável): tabela de eventos `<entidade>_<acao_no_passado>` com quem, quando, de onde e para onde.
- Regra que dá para escrever como restrição vira restrição: `not null`, `check` em status, tipo e origem, `unique` (inclusive composto: empresa + telefone), chave estrangeira com regra de exclusão escolhida (nunca `cascade` sem pensar no que some junto).
- Telefone, e-mail e documento normalizados antes de gravar (telefone em E.164) por uma função única no banco, com índice único na coluna canônica.
- Tempo em `timestamptz`; `date` só para dia do calendário. Comparação de tempo no banco, não na tela. Nada de coluna que dá para calcular, salvo lentidão medida.
- `empresa_id` (ou o nome do `CONTEXT.md`) em toda tabela de dado de cliente, com índice.

## 2. Caminho único de escrita
Cada entidade tem um caminho de gravação, declarado no desenho e usado por todas as telas e integrações. Dois caminhos é defeito, mesmo que os dois funcionem.
- Gravação simples, sem efeito em outras tabelas: direto do cliente, protegida pela regra de acesso.
- Tudo-ou-nada em várias tabelas, efeito colateral, validação que depende de outros dados: **função no banco** via `rpc` (o cliente JS não tem transação entre chamadas).
- Segredo, serviço externo, webhook, IA: **Edge Function** curta e à prova de repetição. Trabalho longo vai para fila ou agendamento, nunca dentro dela (limite de 2 s de processamento por chamada).

## 3. Permissões
O banco é a autoridade; tirar o botão da tela não protege nada.
- **Tabela nova, na mesma migration:** `grant` para os papéis que a usam (inclusive `service_role` se o servidor usa), `enable row level security` e as regras por operação. Sem o `grant`, a tela recebe erro de permissão (obrigatório também em projeto antigo desde 30/10/2026).
- Uma regra por operação, com o papel (`to authenticated`) **e** o teste de dono ou empresa. Alteração leva `using` e `with check`, e precisa de regra de leitura, senão falha sem mostrar erro.
- Nunca `using (true)` em dado de cliente. Nunca `user_metadata` para permissão (o usuário altera); use `app_metadata` ou tabela de papéis.
- Desempenho: `(select auth.uid())`, não `auth.uid()` solto; índice nas colunas das regras; `coluna in (select …)` em vez de junção na regra; a consulta da tela repete o filtro da empresa.
- Views com `security_invoker = true`. `security definer` só como exceção: fora do schema exposto, `set search_path = ''`, sem execução para `public` e `anon`, conferindo dentro quem chama e a empresa.
- Todo id recebido numa escrita é conferido contra a empresa de quem chama, inclusive na criação. Confiar no `empresa_id` vindo por parâmetro é furo.
- Edge Function confere identidade sempre; webhook de terceiro confere a assinatura ou o token dele. Segredo nunca legível pelo navegador.

Matriz de permissões (formato do desenho):

| Papel | Entidade | Ler | Criar | Alterar | Excluir | Onde é garantido | Como confere a empresa |
|---|---|---|---|---|---|---|---|
| vendedor | lead | os seus | sim | os seus | não | regra de acesso | `empresa_id` do usuário |

## 4. Efeitos colaterais e repetição
- Todo gatilho está no desenho (o que dispara, o que muda). Gatilho que muda outra entidade precisa de motivo escrito.
- Escrita que pode repetir (clique duplo, webhook reentregue, job) começa conferindo no banco se já foi feita: chave natural única + "não faz nada se já existe".
- Campo obrigatório novo em dado que um sistema externo grava (n8n, webhook): antes, confira que todos os caminhos preenchem.

## 5. Varredura de consumidores
Antes de mudar ou remover coluna, função, gatilho ou regra de acesso, liste todos que dependem dela (telas, hooks, funções, Edge Functions, jobs, integrações, relatórios), buscando em `src/`, `supabase/functions/`, `supabase/migrations/` e no banco real. O desenho diz o que muda em cada um.

## 6. Migrations e ambientes
- Toda mudança no banco é migration no repositório (`supabase migration new`), aplicada e testada no espelho (protocolo de comunicação, "Banco de teste"). Nunca banco local, nunca direto em produção.
- Compatível com as duas versões do código: acrescente, publique o código que usa, remova o velho depois. Se não der, a ordem fica no desenho e no PR.
- `create or replace` com parâmetros diferentes cria uma segunda função e deixa a antiga viva: `drop function` com a assinatura antiga na mesma migration.
- Confira o número da última migration antes de criar. Migration que muda dado existente diz quantas linhas, como conferir e como voltar.
- Tipos TypeScript gerados (`supabase gen types typescript`) depois de cada migration, nunca à mão. Variável de ambiente nova fica listada no desenho (`VITE_` é pública; segredo só no servidor) e chega a todos os ambientes antes do código.
- **Edge Function:** só existe se o código está no repositório. Declara `verify_jwt = true` ou `false` em `[functions.<nome>]` do `supabase/config.toml`, no PR que a cria; sem isso, função aberta (retorno de OAuth, webhook) passa a exigir login na próxima publicação e para sem erro. Função aberta confere quem chama de outro jeito, e o desenho diz qual. Publicar só pelo comando oficial do projeto, rodado pelo Tech Lead (referência do Tech Lead §4.2).

## 7. Chaves de acesso
Tela: `sb_publishable_…`. Servidor: `sb_secret_…`, nunca no navegador. As antigas (`anon`, `service_role`) serão desligadas no fim de 2026; projeto novo usa só as novas.

## 8. Desempenho, na medida
Meça antes (`explain analyze`, volume real). Índice em chave estrangeira e em coluna de regra de acesso, filtro frequente ou ordenação. Nada "para o futuro". Ordenação da tela com desempate estável (data, depois id).

## 9. Portão antes de declarar pronto
- `get_advisors` (segurança e desempenho) sem alerta novo.
- Toda tabela nova com `grant`, regra ligada e regras por operação.
- Teste de permissão com usuário de outra empresa: não vê, não altera.
