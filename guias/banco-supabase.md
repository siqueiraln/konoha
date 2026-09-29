# Guia: banco de dados e Supabase

Lido por seção. O Arquiteto e o Implementador leem só a seção que a tarefa toca.
Fontes: `pesquisa/04-arquiteto*.md`. Fatos do Supabase conferidos em 2026-09-26; antes de decidir algo que dependa deles, confira de novo pelo MCP do Supabase (`search_docs`), porque a plataforma muda.

**Sobre o MCP do Supabase:** a busca na documentação (`search_docs`) e a leitura do banco real (`list_tables`, `list_migrations`, `list_edge_functions`, `get_advisors`) são as fontes principais. Leitura é livre. **Qualquer alteração em produção só com autorização do dono, para aquela mudança** (referência do Tech Lead §4.1), aplicada pelo Tech Lead na conversa principal com `apply_migration` (o Implementador prepara). Uma **trava automática** (`~/.claude/empresa-agentes/hooks/proteger-banco.py`) garante isso: `execute_sql` que grava é bloqueado; `apply_migration`, `deploy_edge_function` e comandos que alteram o Supabase remoto sempre pedem a confirmação do dono. Antes de qualquer uso, confirme a qual projeto o MCP está ligado.

---

## 1. Modelagem

- **Modele pela forma real do dado e pelas consultas que a tela faz.** Em projeto existente, consulte o banco antes de supor ("1 linha por mensagem" não é "1 linha por conversa").
- **Tabela comum, com atualização, é o padrão.** Histórico imutável só onde o negócio precisa saber o passado: mudança de etapa, de status, de responsável. Nesses casos, uma tabela de eventos (`<entidade>_<acao_no_passado>`, ex.: `negocio_etapas_alteradas`) com quem, quando, de onde e para onde.
- **O banco impede o dado errado.** Toda regra que dá para escrever como restrição vira restrição:
  - `not null` no que é obrigatório;
  - lista fechada de valores com `check` (ou tabela de referência) em todo status, tipo e origem;
  - `unique` no que não pode repetir (inclusive compostos: empresa + telefone, profissional + horário);
  - chave estrangeira em toda referência, com a regra de exclusão escolhida de propósito (nunca `cascade` sem pensar no que some junto).
- **Forma canônica na entrada.** Telefone, e-mail, documento e similares são normalizados antes de gravar (ex.: telefone em E.164), por uma função única no banco, e a coluna canônica tem índice único.
- **Tempo sempre com fuso:** `timestamptz`. Data sem hora (`date`) só para o que é de fato um dia do calendário. Comparações de tempo no banco, não na tela.
- **Um campo, um significado.** Coluna reaproveitada para outra coisa perde dado.
- **Sem colunas que dá para calcular** (total, contagem, status derivado), a menos que uma medição mostre que calcular é lento demais. Valor guardado que dá para calcular fica desatualizado.
- **Localizador completo** de arquivo e recurso externo (bucket + caminho; id + pasta).
- **Empresa em toda tabela de dados de cliente** (`empresa_id`, ou o nome do `CONTEXT.md`), com índice. É o que as regras de acesso usam.

## 2. Caminho único de escrita

Cada entidade tem **um** caminho de gravação, declarado no desenho. Todas as telas e integrações usam o mesmo.

Onde colocar a escrita:

| Situação | Onde |
|---|---|
| Gravação simples, sem efeito em outras tabelas | Direto do cliente, protegida pela regra de acesso |
| Tudo-ou-nada em várias tabelas, efeito colateral, validação que depende de outros dados | **Função no banco**, chamada por `rpc` (o cliente JS não tem transação entre chamadas) |
| Segredo, serviço externo, webhook, IA | **Função no servidor** (Edge Function), curta e à prova de repetição |
| Trabalho longo (mais de alguns segundos de processamento) | Fila ou agendamento; nunca dentro de uma Edge Function (limite de 2 s de processamento por chamada) |

Duas telas gravando a mesma entidade por caminhos diferentes é defeito, mesmo que as duas funcionem.

## 3. Permissões

**O banco é a autoridade.** A tela esconde o que a pessoa não pode fazer, mas é o banco que impede. Tirar um botão da tela não protege nada.

- **Toda tabela nova, na mesma migration:** permissão explícita (`grant`) para os papéis que usam a tabela, incluindo `service_role` quando o servidor usa; regra de acesso ligada (`enable row level security`); e as regras por operação. Desde 30/10/2026 isso é obrigatório também em projetos antigos: sem o `grant`, a tela recebe erro de permissão.
- **Uma regra por operação** (leitura, criação, alteração, exclusão), com o papel declarado (`to authenticated`) **e** o teste de dono ou empresa. Papel sozinho não autoriza nada.
- **Alteração** leva `using` (quais linhas pode alterar) e `with check` (como pode ficar depois), e precisa também de regra de leitura, senão falha sem mostrar erro.
- **Nunca** `using (true)` em dado de cliente. **Nunca** `user_metadata` para decidir permissão (o próprio usuário altera); use `app_metadata` ou uma tabela de papéis.
- **Desempenho:** `(select auth.uid())`, não `auth.uid()` solto; índice em toda coluna usada pelas regras; `coluna in (select …)` em vez de junção dentro da regra; a consulta da tela repete o filtro da empresa.
- **Views** com `security_invoker = true`.
- **Funções privilegiadas** (`security definer`) só como exceção, e sempre: fora do schema exposto, com `set search_path = ''`, sem permissão de execução para `public` e `anon`, e conferindo dentro dela quem chama e a empresa.
- **Todo id recebido numa escrita é conferido contra a empresa de quem chama**, inclusive em criação. Função que recebe `empresa_id` como parâmetro e confia nele é furo.
- **Edge Function confere identidade sempre**, exceto webhook de terceiro, que confere a assinatura ou o token do terceiro.
- **Segredo nunca fica legível pelo navegador**, nem por regra de acesso de leitura ampla. Segredos de integração ficam em tabela sem acesso pela API ou nos segredos das funções.

### Matriz de permissões (formato do desenho)

| Papel | Entidade | Ler | Criar | Alterar | Excluir | Onde é garantido | Como confere a empresa |
|---|---|---|---|---|---|---|---|
| vendedor | lead | os seus | sim | os seus | não | regra de acesso | `empresa_id` do usuário |

## 4. Efeitos colaterais e repetição

- **Gatilho no banco é efeito escondido.** Todo gatilho está no desenho: o que dispara, o que muda, em quais tabelas. Gatilho que muda outra entidade precisa de motivo escrito.
- **À prova de repetição:** clique duplo, webhook reentregue, job que roda de novo. O primeiro passo de toda escrita que pode repetir é verificar, no próprio banco, se já foi feita (chave natural única + "não faz nada se já existe").
- **Campo obrigatório novo** num dado que um sistema externo grava (n8n, webhook, integração): confira que todos os caminhos preenchem, antes. Um campo obrigatório esquecido parou o follow-up de todas as empresas de um projeto real por 2 dias.

## 5. Varredura de consumidores

Antes de mudar ou remover coluna, função, gatilho ou regra de acesso: liste **todos** que leem ou dependem dela: telas, hooks, funções do banco, Edge Functions, jobs, integrações externas, relatórios. Busque pelo nome em `src/`, `supabase/functions/`, `supabase/migrations/` e no banco real. O desenho lista o que muda em cada um.

## 6. Migrations e ambientes

- **O repositório é a verdade do banco.** Toda mudança no banco é uma migration no repositório, criada pela ferramenta oficial (`supabase migration new`), testada localmente (`supabase db reset`) e aplicada por um caminho só. Nunca mexer direto no banco de produção.
- **Mudança compatível com as duas versões do código.** O site e o banco não mudam no mesmo instante. Acrescente primeiro (coluna nova com valor padrão ou opcional para o código antigo), publique o código que usa, e só remova o velho numa mudança seguinte. Se não der, a ordem obrigatória fica escrita no desenho e na descrição do PR.
- **Função com assinatura nova:** `create or replace` com parâmetros diferentes cria uma **segunda** função e deixa a antiga viva e executável. Remova a antiga (`drop function` com a assinatura exata) na mesma migration.
- **Numeração:** confira a última migration existente antes de criar, para não colidir com outra linha de trabalho.
- **Migration que muda dado existente** (preencher coluna nova, converter formato): diga quantas linhas afeta, como conferir o resultado e como voltar.
- **Edge Function** só existe se o código está no repositório.
- **Tipos TypeScript** gerados do banco (`supabase gen types typescript`) depois de cada migration; nunca editados à mão.
- **Variáveis de ambiente:** listadas no desenho (nome, para que serve, onde vive: `VITE_` pública na tela, segredo só no servidor). Variável nova chega a todos os ambientes antes do código que a usa.

## 7. Chaves de acesso

- Tela: chave publicável (`sb_publishable_…`). Servidor: chave secreta (`sb_secret_…`), nunca no navegador.
- As chaves antigas (`anon`, `service_role`) serão desligadas no fim de 2026 (data exata não publicada em 2026-09-26). Projeto novo usa só as novas.

## 8. Desempenho, na medida

- **Meça antes de otimizar.** `explain analyze` na consulta real, com volume real.
- Índice em toda chave estrangeira e em toda coluna usada por regra de acesso, filtro frequente ou ordenação da tela.
- Nada de índice, paginação ou cache "para o futuro" em tabela pequena. Escalar só com gargalo medido: índice → particionamento → visão materializada.
- Ordenação que a tela mostra tem desempate estável (ex.: data, depois id).

## 9. Portão antes de declarar pronto

- Verificadores oficiais sem alerta novo (`get_advisors` segurança e desempenho). Atenção especial: tabela sem regra de acesso, regra que libera tudo, função privilegiada exposta, `search_path` mutável, `auth.uid()` sem `select`, chave estrangeira sem índice.
- Toda tabela nova com `grant`, regra ligada e regras por operação.
- Teste de permissão com um usuário de outra empresa: não vê, não altera.
