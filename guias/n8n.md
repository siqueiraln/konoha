# Guia: n8n

Lido por seção. Quem toca o n8n (Pesquisador, Arquiteta, Implementador, Security, Testes) lê só a seção que a tarefa pede.
Fontes: `pesquisa/12-n8n.md` (documentação oficial, conferida em 2026-09-26, com links) e as lições de um projeto real (o detalhe fica no repositório dele). O n8n muda rápido: antes de afirmar comportamento de versão, confira pela documentação (MCP de documentação, seção 2).

**Regra de fundo:** workflow é código do produto. Erro num workflow é incidente em produção, não bug de tela. Mapear antes de mexer, mudança passa pelo mesmo fluxo de projeto ou conserto do resto, e nada muda no ar sem o dono.

---

## 1. O n8n é parte do desenho, não uma caixa à parte

- **O n8n grava direto no banco.** Todo workflow que escreve numa tabela é um **caminho de escrita** dela. No desenho (guia banco §2), ele entra na lista de caminhos da entidade, com o que envia e o que o banco completa.
- **Campo obrigatório novo, restrição nova ou coluna renomeada** numa tabela que o n8n escreve: antes, liste os workflows que escrevem nela e confira que cada ramo envia o campo. Um campo obrigatório que um ramo do n8n não preenchia parou o follow-up de todas as empresas de um projeto real por 2 dias.
- **Contrato explícito** para cada fronteira n8n ↔ banco ↔ app: direção, gatilho, dados essenciais e formato (ex.: telefone `55+DDD+número`), quem é dono de cada lado. O contrato mora no repositório do projeto (ex.: `docs/<area>/fronteiras/n8n.md`), apontado pelo `CLAUDE.md` dele.
- **Webhook chamado pelo app** (ex.: enviar mensagem) é uma dependência externa (guia banco §4): o que acontece se falhar, se demorar, se for chamado duas vezes.

## 2. Ferramentas e o que cada agente pode fazer

**Leitura é livre. Qualquer alteração ou disparo passa pelo dono.** Uma trava automática (`~/.claude/empresa-agentes/hooks/proteger-banco.py`) garante isso, porque regra escrita se esquece.

| Ferramenta | Serve para | Trava |
|---|---|---|
| **MCP de documentação** do n8n (`https://docs.n8n.io/~gitbook/mcp`) | Consultar a documentação oficial atual | Só lê |
| **MCP oficial da instância** (conectado com permissão só de leitura) | Ver workflows, execuções, histórico e diferença entre versões, credenciais sem segredo, uso de nós; validar workflow | Busca, leitura e validação passam; executar, testar, publicar, criar, editar e apagar pedem o dono |
| **API pública** (`/api/v1`, chave `X-N8N-API-KEY`) | Ler workflows e execuções quando o MCP não cobre | GET passa; POST, PUT, PATCH e DELETE pedem o dono |
| **Webhooks de produção** (`/webhook/...`) | — | **Toda** chamada pede o dono: webhook dispara o workflow de verdade (ex.: manda WhatsApp para cliente) |
| **CLI do n8n** (`n8n-cli`) | Listar e ler | Comandos que criam, alteram, ativam, executam ou importam pedem o dono |

**Versão importa.** Antes de usar o MCP da instância, confira a versão do n8n (aparece em Settings). Na **1.x** o MCP é um beta limitado: só enxerga workflows liberados um a um e quase só serve para executar; histórico, diferença entre versões e edição de rascunho vieram na 2.x (2.13 a 2.36). **Na 1.x, a leitura é pela API** e o MCP da instância fica desligado.

Cuidados:
- **A chave da API não é "só leitura".** Fora do plano Enterprise, ela tem acesso total à instância. O "só ler" dos agentes é garantido pela trava, não pela chave. Trate a chave como credencial de escrita: nunca em arquivo versionado, nunca em log.
- **`execute_workflow` roda em produção** (a versão publicada) por padrão. `test_workflow` usa dados fixados, mas nós sem dados fixados podem chamar serviços de verdade. Os dois pedem o dono.
- **Editar pela API republica sozinho** se o workflow estiver ativo (`PUT /workflows/{id}` substitui o workflow inteiro), a menos que se passe `publishIfActive=false`.
- O projeto da comunidade `n8n-mcp` só é usado **sem** a chave da instância (modo documentação e validação). Com a chave, ele escreve.

## 3. Mudar um workflow

Hoje, a mudança é **manual e feita por uma pessoa**:

1. **Mapear:** o workflow atual (pelo MCP ou pela API, só leitura), quem o chama (sub-workflows, webhooks, agendamentos) e as tabelas que ele lê e escreve.
2. **Roteiro nó a nó** no documento do projeto ou do conserto: o que muda em cada nó, na ordem, com os valores exatos. Inclui o tratamento de erro (seção 4) e a deduplicação (seção 6) quando o workflow grava ou envia algo.
3. **O dono (ou quem ele indicar) aplica** no editor do n8n, como rascunho.
4. **O agente confere o rascunho** pela leitura: a diferença entre versões (`get_workflow_versions_diff`) bate com o roteiro, nó a nó; `validate_workflow` sem erro.
5. **O dono publica.** Publicar é colocar no ar.
6. **O agente confere a vida real:** as primeiras execuções depois da publicação (seção 5), com os dados gravados no banco.

Desde o n8n 2.0, editar gera **rascunho** e só "Publicar" leva ao ar. Isso permite, no futuro, o agente editar o rascunho e o dono só revisar e publicar; hoje o dono escolheu manter a edição manual.

## 4. Erro que ninguém vê é o pior erro

- **Todo workflow crítico tem um workflow de erro** (configurações do workflow → Error workflow), que começa com o nó Error Trigger e avisa alguém (ou grava num registro). O Error Trigger só dispara em execução automática, não em manual.
- **"On Error: Continue" sem tratar a saída de erro é proibido em workflow crítico.** Ele segue em frente como se nada tivesse acontecido. Num projeto real, um nó falhava em **200 de 200** execuções e gravava dados nulos, sem ninguém ver. Use "Continue (using error output)" com a saída de erro ligada a algo que registra ou avisa, ou deixe falhar e o workflow de erro avisar.
- **Nó Stop And Error** para falhar de propósito quando o dado está errado (melhor falhar alto que gravar lixo).
- **Retry On Fail** só em chamada que pode repetir sem efeito duplicado (seção 6).

## 5. Provar que um workflow roda (ou não roda)

- **"Inativo" não prova que parou.** Um sub-workflow chamado por outro (Execute Workflow) roda mesmo marcado como inativo. A prova de vida é a lista de **execuções**, não o botão.
- **"Não achei execução" também não prova nada.** A retenção padrão é de 14 dias ou 10.000 execuções, o que vier primeiro; numa instância com centenas de workflows e volume de WhatsApp, isso pode cobrir só algumas horas. Antes de concluir, confira a política de retenção da instância e a janela que a lista cobre.
- Para saber quem chama um sub-workflow, procure nos outros workflows o nó Execute Workflow que aponta para ele, não pelo nome.

## 6. Webhooks e repetição

- **Autenticação em todo webhook** que recebe dado de fora (Header, Basic ou JWT; lista de IPs quando der). Webhook da Meta: conferir o token no GET e a assinatura `X-Hub-Signature-256` no POST (Security, classe 5).
- **Responder rápido** e processar depois: provedor que não recebe resposta a tempo reenvia (a Meta reenvia por até 7 dias).
- **Deduplicar** por um identificador da mensagem ou do evento: nó Remove Duplicates, ou chave única no banco (preferível quando o dado vai para o banco).
- URL de teste (`/webhook-test/`) só escuta com "Listen for Test Event"; a de produção só existe com o workflow publicado.

## 7. Credenciais e versões

- **Segredo mora no cofre de credenciais do n8n**, nunca escrito numa expressão ou num nó. Token escrito no nó vaza em todo export e impede guardar o workflow no git. Achou token em nó: é achado de segurança.
- **Versionamento:** no plano gratuito, o histórico de versões guarda só 24 horas. Guarde os workflows críticos no repositório exportando **sem credenciais** (`n8n export:workflow` ou pela API), e compare antes e depois de cada mudança. Só é possível quando os tokens já estão no cofre de credenciais.

## 8. Atualizar o n8n

- **n8n 3.0 (previsto para outubro de 2026)**: só instalação por Docker em self-hosted; saem mais de 20 nós antigos (Function, Cron, Item Lists, entre outros); o Execute Sub-workflow perde algumas opções. Antes de atualizar, **inventário** dos workflows que usam o que sai (pelo MCP: `get_node_usage`), e plano de troca de cada um.
- Atualização de versão é projeto, não tarefa rápida: roda com a lista de workflows críticos conferidos depois.

## 9. Portão antes de declarar pronto

- O roteiro bate com a diferença entre versões, nó a nó.
- Workflow crítico tem workflow de erro; nenhum "Continue" engolindo erro.
- Webhook novo com autenticação e deduplicação.
- Nenhum segredo em nó ou expressão.
- As primeiras execuções reais depois da publicação conferidas, com o dado gravado no banco.
- Contrato da fronteira atualizado (`docs/**/fronteiras/` ou equivalente).
