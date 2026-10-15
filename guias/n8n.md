# Guia: n8n

Lido por seção: quem toca o n8n lê só a seção que a tarefa pede. Documentação conferida em 2026-09-26; o n8n muda rápido, então confira comportamento de versão pelo MCP de documentação.

**Regra de fundo:** workflow é código do produto, e erro nele é incidente em produção. Mapear antes de mexer, e nada muda no ar sem o dono.

## 1. O n8n é parte do desenho
- Todo workflow que grava numa tabela é um **caminho de escrita** dela (guia banco §2), com o que envia e o que o banco completa.
- Campo obrigatório novo, restrição nova ou coluna renomeada numa tabela que o n8n escreve: antes, liste os workflows que escrevem nela e confira que cada ramo envia o campo.
- Cada fronteira n8n ↔ banco ↔ app tem contrato no repositório do projeto (ex.: `docs/<area>/fronteiras/n8n.md`): direção, gatilho, dados e formato (telefone `55+DDD+número`), dono de cada lado.
- Webhook chamado pelo app é dependência externa (guia banco §4): falha, demora, chamada dupla.

## 2. Ferramentas e o que cada agente pode fazer
**Leitura é livre; qualquer alteração ou disparo passa pelo dono.** A trava `~/.claude/empresa-agentes/hooks/proteger-banco.py` garante isso.

- **MCP de documentação** (`https://docs.n8n.io/~gitbook/mcp`): só lê.
- **MCP da instância** (só leitura): ver workflows, execuções, versões, uso de nós, validar. Executar, testar, publicar, criar, editar e apagar pedem o dono.
- **API pública** (`/api/v1`, `X-N8N-API-KEY`): GET passa; POST, PUT, PATCH e DELETE pedem o dono.
- **Webhooks de produção** (`/webhook/...`): toda chamada pede o dono, porque dispara o workflow de verdade.
- **CLI** (`n8n-cli`): listar e ler passam; o resto pede o dono.

Armadilhas:
- **Versão:** na 1.x o MCP da instância é beta e quase só executa; leia pela API e deixe o MCP desligado. Histórico e diferença entre versões vieram na 2.x.
- **A chave da API tem acesso total** fora do Enterprise. Trate como credencial de escrita: nunca em arquivo versionado nem em log.
- **`execute_workflow` roda a versão publicada**, em produção. `test_workflow` usa dados fixados, mas nó sem dado fixado chama serviço de verdade.
- **`PUT /workflows/{id}` republica sozinho** um workflow ativo, a menos que se passe `publishIfActive=false`.
- O `n8n-mcp` da comunidade só sem a chave da instância (com ela, ele escreve).

## 3. Mudar um workflow
O agente não edita n8n de produção. A mudança é manual:
1. **Mapear** (só leitura): o workflow, quem o chama (sub-workflows, webhooks, agendamentos) e as tabelas que lê e escreve.
2. **Roteiro nó a nó** no documento do projeto ou do conserto, com valores exatos, workflow de erro (seção 4) e deduplicação (seção 6) quando grava ou envia algo.
3. **O dono aplica** no editor, como rascunho.
4. **O agente confere o rascunho:** `get_workflow_versions_diff` bate com o roteiro nó a nó; `validate_workflow` sem erro.
5. **O dono publica.**
6. **O agente confere as primeiras execuções** (seção 5) e o dado gravado no banco.

## 4. Erro que ninguém vê
- Workflow crítico tem workflow de erro (Error Trigger que avisa ou registra). O Error Trigger só dispara em execução automática.
- "On Error: Continue" sem tratar a saída de erro é proibido em workflow crítico: segue gravando nulo sem ninguém ver. Use "Continue (using error output)" ligado a algo que avisa, ou deixe falhar.
- Stop And Error para falhar alto quando o dado está errado. Retry On Fail só em chamada que pode repetir sem duplicar.

## 5. Provar que roda (ou não roda)
- **"Inativo" não prova que parou:** sub-workflow chamado por Execute Workflow roda mesmo inativo. A prova é a lista de execuções.
- **"Não achei execução" não prova nada:** a retenção padrão (14 dias ou 10.000 execuções) pode cobrir só horas. Confira a retenção e a janela antes de concluir.
- Quem chama um sub-workflow: procure o nó Execute Workflow que aponta para ele, não pelo nome.

## 6. Webhooks e repetição
- Autenticação em todo webhook que recebe dado de fora. Meta: token no GET e assinatura `X-Hub-Signature-256` no POST.
- Responder rápido e processar depois: a Meta reenvia por até 7 dias.
- Deduplicar pelo id do evento: chave única no banco (preferível) ou Remove Duplicates.
- `/webhook-test/` só escuta com "Listen for Test Event"; a URL de produção só existe com o workflow publicado.

## 7. Credenciais e versões
- Segredo só no cofre de credenciais, nunca em nó ou expressão. Token em nó é achado de segurança.
- No plano gratuito o histórico guarda só 24 horas: exporte os workflows críticos **sem credenciais** para o repositório e compare antes e depois.

## 8. Atualizar o n8n
n8n 3.0 (previsto para outubro de 2026): só Docker em self-hosted e saem mais de 20 nós antigos (Function, Cron, Item Lists). Antes de atualizar, inventário pelo `get_node_usage` e plano de troca. Atualização é projeto, não tarefa rápida.

## 9. Portão antes de declarar pronto
- O roteiro bate com a diferença entre versões, nó a nó.
- Workflow crítico com workflow de erro; nenhum "Continue" engolindo erro.
- Webhook novo com autenticação e deduplicação. Nenhum segredo em nó.
- Primeiras execuções reais conferidas, com o dado no banco. Contrato da fronteira atualizado.
