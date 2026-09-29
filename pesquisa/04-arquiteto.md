# Pesquisa: Arquiteto

Material bruto para construir o agente. Nada aqui é o agente final.

Decisão do dono (2026-09-26): Backend e Frontend viram **um Arquiteto só**, que desenha a feature inteira (dados, permissões, contrato entre tela e banco) e não implementa. Trabalho grande se divide **por parte da solução**, começando pela **costura**. A memória fica no documento. O conhecimento de cada camada fica em **guias** consultados por seção.

Fontes detalhadas:
- `pesquisa/04-arquiteto-skills-bruto.md` — skills instaladas e diagnóstico dos dois arquitetos originais.
- `pesquisa/04-arquiteto-supabase.md` — documentação oficial do Supabase, conferida em 2026-09-26, com links.
- O caso real que alimentou esta pesquisa (um CRM com 4.610 commits e ~150 anomalias catalogadas) mora no repositório daquele projeto, não aqui.
- `pesquisa/seasoned-skills.md` §1.4, §1.5 e §3.1.

## 1. Diagnóstico dos originais (`03_backend-architect.md`, `04_frontend-architect.md`)

**Manter:** spec executável sem perguntas; tabelas e regras de acesso como SQL pronto e comentado; fluxos como sequência numerada; catálogo de erros com a reação da tela; variáveis de ambiente listadas; decisão com alternativa descartada e motivo.

**Cortar:** cardápio genérico (GraphQL, Kafka, Redis, microsserviços, Redux); "sempre considere escalabilidade horizontal"; specs separadas de back e front; rotas REST `/api/v1` quando o app fala direto com o Supabase.

**Falta:** matriz de permissões; onde mora cada regra; caminho único de escrita; varredura de quem lê cada dado; proteção contra repetição (clique duplo, webhook reentregue); restrições no banco; migrations em sincronia; critério de quando registrar decisão; proporcionalidade.

## 2. Lições do CRM (o que já custou caro)

~20% dos commits são correção. Os problemas se concentram em quatro classes, e cada uma vira regra:

1. **Mais de um caminho de escrita para a mesma coisa.** O contato era criado por 5 caminhos com validações diferentes; etiquetas em dois lugares, cada tela escrevendo num lado (72% invisíveis onde importava); estado da conversa gravado em 23 pontos do front. → **Toda entidade tem um caminho único de escrita, decidido antes da tela.**
2. **Permissão decidida na tela, não no banco.** Senha de integração sumiu da tela mas continuou legível pelo banco; 19 de 32 funções do servidor sem checagem de quem chama; funções privilegiadas aceitando o id de empresa sem conferir. → **Permissão se garante no banco; a tela só reflete. Toda operação declara quem pode, onde isso é garantido e como a empresa é conferida.**
3. **Banco que aceita dado errado.** Telefone sem forma única (~12% da base duplicada), status sem lista fechada, agenda sem impedir dois compromissos no mesmo horário, hora sem fuso (envio saindo 3h depois). → **O banco impede o dado errado com restrições; não depende da disciplina de quem escreve.**
4. **Efeitos escondidos e migrations fora de sincronia.** Gatilho no banco mudando status de outra coisa; campo obrigatório que um fluxo externo não preenchia parou o follow-up de todas as empresas por 2 dias; 362 migrations no repositório contra 330 no banco, só 25 coincidindo; funções rodando em produção sem código no repositório; 15 tabelas nascidas sem regra de acesso. → **Todo efeito colateral está escrito no contrato; o repositório é a verdade do banco.**

Também: modelar pela forma real do dado e medir antes de supor (uma consulta de 16,5 s caiu para 5 ms com o índice certo; uma decisão foi revertida depois de teste de carga). E o que funcionou no CRM: as três perguntas antes de construir ("que conceito isto estende? já foi decidido? onde mora?"), a varredura de consumidores antes de mexer em coluna, e a regra de onde escrever (direto se não há efeito colateral; função no banco se há; função no servidor se envolve segredo ou serviço externo).

## 3. Supabase (conferido em 2026-09-26)

**Fontes a usar, nesta ordem:** o **MCP oficial do Supabase**, que está instalado. Ele tem `search_docs` (busca na documentação atual; testado em 2026-09-26, funciona), `list_tables`, `list_migrations`, `list_edge_functions` e `get_advisors` (o banco real e os verificadores). Depois a web, para o que a busca da documentação não cobre: changelog de mudanças com data e discussões no GitHub. Cuidado: o mesmo MCP também grava (`apply_migration`, `execute_sql`, `deploy_edge_function`). O Arquiteto e a Rita usam só as ferramentas de leitura, e confirmam antes a qual projeto o MCP está ligado.

- **Mudança com data:** tabelas novas deixaram de ser expostas automaticamente à API. Vale para projetos novos desde 30/05/2026 e **para todos os existentes a partir de 30/10/2026**. Toda tabela nova precisa, na mesma migration: permissão explícita (grant), regra de acesso ligada e as regras por operação.
- **Regras de acesso:** uma por operação, com o papel declarado e o teste de dono; na alteração, `using` e `with check`, e alteração exige regra de leitura (senão falha sem erro).
- **Desempenho das regras:** `(select auth.uid())`, índice nas colunas que as regras usam, `in (select …)` em vez de junção. Ganhos citados de 100x a 10.000x.
- **Nunca `user_metadata` para permissão** (o próprio usuário altera); views com `security_invoker = true`; funções privilegiadas (`security definer`) só como exceção controlada.
- **Onde colocar a lógica:** leitura e escrita simples direto com regra de acesso; escrita que precisa ser tudo-ou-nada em várias tabelas numa função do banco (o cliente JS não tem transação entre chamadas); segredo, webhook e serviço externo numa função do servidor, curta e à prova de repetição.
- **Chaves novas:** `sb_publishable_…` no front, `sb_secret_…` só no servidor; as chaves antigas saem no fim de 2026 (data exata não publicada).
- **Funções do servidor:** 2 s de processamento por chamada, 150–400 s de duração; trabalho longo não cabe nelas.
- **Migrations:** criadas pela ferramenta oficial, testadas localmente, aplicadas por um caminho só; nunca mexer direto no banco de produção. Tipos TypeScript gerados do banco.
- **Verificadores oficiais** (segurança e desempenho): tabela sem regra de acesso, regra que libera tudo, função privilegiada exposta, chave estrangeira sem índice. Servem de portão antes de declarar pronto.

## 4. Das skills instaladas

- **Registro de decisão (ADR) só quando as três valem:** difícil de desfazer, surpreende quem não tem o contexto, saiu de escolha real. Uma a três frases. "Nãos" explícitos contam.
- **Módulo profundo:** interface pequena, muito comportamento por trás. Teste da exclusão: apagar o módulo espalha complexidade? Então ele se paga. Um só adaptador é abstração hipotética.
- **Interface é tudo que quem chama precisa saber:** entradas, erros, pré-condições, efeitos, ordem.
- **Classificar dependências:** local, substituível em teste (banco local), remota própria (funções do servidor), externa (WhatsApp, pagamento). A classe define como cada fatia é testada.
- **O banco real vence a migration:** em projeto existente, conferir regras, índices e gatilhos no banco de verdade.
- **Leitores e escritores:** para cada tabela escrita, listar quem lê (tela e servidor) e o que cada escrita precisa atualizar na tela.
- **Fatias com "consome / produz"** e restrições globais no topo (a costura). Fatia certa: o menor pedaço que um revisor poderia rejeitar aprovando a vizinha.
- **Proporcionalidade:** só tratar o que um usuário normal encontraria numa semana; nada de índice em tabela pequena nem paginação antes da hora.

## 5. Seasoned

- **Derivar antes de escalar;** escalar só com gargalo medido (explicar a consulta e indexar → particionar → visão materializada).
- **Estado derivado de eventos** (histórico imutável, sem colunas nulas, sem `updated_at`), com variante "mutável quando não derivável". Rigor alto; ver conflito 1.
- **Jobs:** idempotência como primeiro passo, derivada do próprio banco; falha registrada fora da transação.
- **Variáveis de ambiente** validadas na subida, listando todas as faltantes; variável nova chega a todos os ambientes antes do código que a usa.
- **Datas** formatadas no servidor; comparações de tempo no banco; teste do dia exato nos dois lados de uma fronteira de fuso.
- **Todo id estrangeiro recebido numa escrita é uma checagem de empresa.**

## 6. Conflitos, resolvidos

1. **Histórico imutável (Seasoned) x tabela comum com atualização (CRUD).** Decidido: tabela comum com restrições rigorosas (obrigatório, lista fechada, unicidade), e **histórico só onde o negócio precisa** (mudança de etapa, de status, de dono). Motivo: o dono trabalha com Supabase e CRUD; o modelo 100% de eventos muda tudo e não tem incidente no CRM que o exija. Vira suposição registrada.
2. **Permissão no código (Seasoned) x no banco (Supabase).** Decidido: **no banco**, como autoridade; o código e a tela refletem. É o que as lições 2 do CRM e a documentação apontam.
3. **SQL completo na spec (original) x decisão sem implementação (nossa divisão).** Decidido: o Arquiteto escreve o **desenho** (tabelas, colunas, restrições, regras de acesso em forma de matriz e as regras em SQL quando são o contrato); a migration completa é do Implementador.

## 7. Esqueleto proposto

Entrada: documento de projeto do PO e `telas.md` do designer. Saída: a parte 5 do documento (ou `docs/projetos/<nome>/tecnico.md` citado nela).

**Chamada 1 — a costura** (sempre):
1. As três perguntas: que conceito isto estende, já foi decidido, onde mora (lê `docs/adr/`, `CONTEXT.md`; mapa do sistema atual pedido à Rita quando o projeto já existe).
2. Dados: entidades, campos, restrições, o que é histórico.
3. **Caminho único de escrita** de cada entidade.
4. **Matriz de permissões:** papel × entidade × operação, onde é garantido, como a empresa é conferida.
5. Onde mora cada regra (direto, função no banco, função no servidor), com efeitos colaterais declarados.
6. Leitores de cada dado que muda, e o que a tela atualiza.
7. Dependências externas e como cada uma é testada.
8. Divisão em fatias ponta a ponta, com consome/produz.

**Chamadas seguintes — uma por parte da solução:** detalha a parte (contrato de cada ação: entradas, validações, erros e a reação da tela, efeitos, proteção contra repetição) contra a costura já escrita.

**Portões antes de declarar pronto:** nenhum "a definir"; toda tabela nova com permissão, regra de acesso e regras por operação; toda escrita com caminho único; toda operação na matriz; varredura de consumidores feita para cada coisa alterada; decisões que passam no critério viram ADR.

**Guias por camada** (arquivos da empresa, lidos por seção): banco e Supabase; React e tela. O Arquiteto e o Implementador leem só a seção que a tarefa toca.
