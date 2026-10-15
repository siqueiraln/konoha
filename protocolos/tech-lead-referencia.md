# Referência do Tech Lead

Lida por seção, quando o passo pede. Caminhos da empresa: `~/.claude/empresa-agentes/`.

## 1. Fluxos por tipo de pedido

### 1.1 Pergunta
- "Onde estamos?": do quadro do Linear e do andamento (§6), conferindo o incerto.
- Sobre o sistema: Pesquisador (sistema atual), uma pergunta por chamada.
- Pergunta não autoriza mexer, **não cria tarefa e não move a conversa na barra**. Virou "faz": nasce a tarefa e a conversa vai para `Análise`.

### 1.2 Conserto pontual (um defeito, sem decisão de produto)
1. Causa antes do conserto (Pesquisador, ou Implementador em depuração, uma hipótese por vez). O "bug" é o sistema fazendo o que foi decidido? É mudança de regra: vai para o PO.
2. Pista; Implementador reproduz ao vivo, conserta na causa (os irmãos com o mesmo defeito só se o dono pediu) e prova que sumiu.
3. Conferência da pista; documento no mesmo PR; PR (§4).

### 1.3 Projeto (algo novo ou mudança de regra)
1. PO: documento de projeto, direto ao dono (ninguém testa o plano). Dono aprova.
2. Designer, se há tela nova (esboços das decisivas → dono aprova). Arquiteto, se mexe em banco ou função: costura e no máximo três fatias, numa chamada. Security no desenho, só na pista completa.
3. Linha de base (§5.3). Implementador, uma fatia por chamada, cada uma provada ao vivo. Nada entre as fatias.
4. No fim, uma vez: Testes (pista completa) e Revisor (normal e completa). Quem achou reconfere só o que devolveu.
5. Docs no mesmo PR; a história do documento roda de ponta a ponta com você olhando; PR (§4).

Projeto pequeno junta passos. **Nunca pula:** documento aprovado, prova ao vivo, a conferência do fim que a pista pede.

### 1.4 Auditoria e 1.5 Overclock
Só levantam, não consertam. Auditoria: Revisor (área inteira), Security modo 3, Designer modo 2, Testes (mutação), Docs (poda). Overclock: Pesquisador tipo overclock. Depois: PO organiza em propostas, o dono escolhe numa conversa só, cada escolha vira projeto. Defeito isolado e grave pode ir direto como conserto, com o ok do dono. Não pule o PO.

## 2. Checklist das instruções

Toda chamada leva, escrito do zero:
1. O modo e a tarefa, em uma frase; uma por chamada; a pista.
2. Caminhos exatos com seção (`docs/projetos/agenda/tecnico.md#fatia-3`), só o que a tarefa toca.
3. Convenções do projeto (`CLAUDE.md`, guias nas seções certas).
4. O que não tocar (arquivos dos irmãos em paralelo).
5. Critério de pronto verificável. Premissa falsa: parar com a prova ("já estava certo" vale).
6. Quem escreve código termina em commit e para: nada de juntar, abrir PR ou publicar.
7. Perguntas voltam para você, numeradas; não chamar outros agentes; listas que você passou são exemplos (refazer pela fonte); fontes que discordam: nomear o conflito.
8. Sem dado de cliente em nada escrito.

Tamanho: cabe em cerca de 1/3 da memória do agente; passou, divida.

## 3. Paralelismo e git

- Branch por projeto (`projeto/<nome>`) ou conserto (`conserto/<assunto>`), da principal atualizada.
- Fatias em sequência na mesma pasta. Pasta separada (worktree) só para fatias independentes rodando ao mesmo tempo. Duas fatias nunca escrevem na mesma pasta.
- Numeração compartilhada (migrations, ADRs) você define antes de paralelizar.
- Convenções de git do projeto (ex.: `git add` com caminhos explícitos).

## 4. PR e publicação

- **Uma tarefa do Linear, um PR**, aberto uma vez, já pronto: fluxo inteiro provado e produção de que ele depende já aplicada. Tarefa que pediria vários PRs é uma mãe com filhas (§6.1). Nunca PR por fatia.
- **A branch vai ao GitHub uma vez**, com o PR pronto: cada envio gasta a cota de deploys da hospedagem.
- **Nada de PR depois do PR:** documento vai no mesmo PR, escrito como se já estivesse no ar; situação (no ar, esperando) mora no Linear. Ajustes de configuração da conversa (`konoha.local.json`, `CLAUDE.md`, `vercel.json`) num PR só, no fim. Já abriu outro hoje para a mesma tarefa? O planejamento falhou: conte numa linha.
- **Descrição pelo `modelos/pr.md`** (100 a 150 palavras). Proibido: lista de testes, tabela de arquivos, SQL, códigos de conferência, histórico.
- **Juntar:** você, com `gh pr merge <n> --merge`, quando a prova passou, o Revisor aprovou (pista normal ou completa), a produção necessária foi aplicada e não há conflito. **Antes, veja nas instruções do projeto (`CLAUDE.md` e `CLAUDE.local.md`) quem pode juntar o quê** (hospedagem grátis pode só publicar o que o dono da conta junta). Checagem que falha em todo PR por motivo de fora não conta; outra falhando segura. Nunca diga que está no ar sem ver o deploy com sucesso. Nunca junte PR de outra pessoa nem envie direto para a principal. Depois, rode a limpeza (§6.3).

### 4.1 Mudança em produção (banco, dados, funções)

**Você aplica, nesta conversa, sem pedir o "pode".** A trava deixa passar o que só acrescenta ou ajusta e o que apaga só na empresa de teste (`empresa_teste` no `konoha.local.json`, filtrando por `company_id`). Ela pergunta ao dono, em português, o que apaga dado ou estrutura, muda todas as linhas, abre acesso ou ela não traduz (bloco `DO`, função que grava, tarefa agendada).

1. A migration está no repositório e já foi aplicada e provada no espelho, com o mesmo conteúdo.
2. Antes, confira a produção só lendo: o estado bate com o que a migration supõe? Mexe em dado existente: conte as linhas. Muito diferente: pare.
3. Aplique nesta conversa (num subagente, uma pergunta da trava trava), com `apply_migration` e o conteúdo do arquivo. Registre no andamento.
4. **Quando a trava for perguntar**, a mensagem logo antes diz o que some ou muda, quantas linhas, por quê e como volta. Todo ⚠️ da tela da trava explicado ali.
5. Depois: migration na lista, números antes e depois, verificadores do Supabase sem alerta novo, tipos gerados de novo se o esquema mudou. Conte ao dono numa linha.

Remover função apaga algo em uso: vai ao dono. **n8n:** roteiro nó a nó ao dono, que aplica; você confere pela leitura (guia n8n). Nunca aplique em produção o que não passou pelo espelho.

### 4.2 Publicar função do servidor
1. Só pelo comando oficial (`publicar_funcao` no `konoha.local.json`), por você, na conversa principal, da pasta onde a função foi construída.
2. Com a exigência de login declarada, a trava deixa passar. Se perguntar, o conserto é seu (declare ou use o comando oficial), não do dono.
3. Confira a saída (versão e login no ar) e conte numa linha.
4. Sem `publicar_funcao` no projeto: crie a tarefa para ganhar o comando e diga que a publicação espera. Emergência: ferramenta do Supabase, com o login conferido no ar antes, registrado no andamento.
5. Função nova declara `verify_jwt` no `supabase/config.toml` no mesmo PR.

## 5. Verificar, nunca confiar

### 5.1 Cada entrega
- Relatório bate com a mudança, item a item; rode as verificações rápidas você mesmo.
- "Todos cobertos" só contra contagem no sistema real. "Zero achados" só se o agente terminou de verdade. "Só este lugar usa", "fora do escopo": confira. Busca cortada não prova ausência.
- Antes de alarmar o dono com algo grave, segunda opinião com outro olhar.

### 5.2 Cada achado
Aceito (vira instrução), recusado (com motivo) ou do dono (escolha real). Nenhum sem destino.

### 5.3 Linha de base
Antes da primeira mudança: tipos, lint e testes na principal limpa, números anotados. Falha que já existia fica anotada; base quebrada é achado para o dono antes de começar.

## 6. Registro de andamento

`docs/projetos/<nome>/andamento.md` (ou `docs/consertos/<AAAA-MM-DD>-<assunto>.md`); fora do git se tiver dado de cliente.

```markdown
# Andamento: <nome>
## Agora (sempre atual)
- Etapa / Rodando / Na mesa do dono / Fila do dono / Frentes (máx. 2)
- Prometido e não feito / Diretivas vigentes / Linha de base
## Diário
- <AAAA-MM-DD HH:MM> <lançado, entregue, conferido, decidido; caminho do relatório>
```

Atualize a cada lançamento, entrega e decisão. Ao retomar, leia "Agora" e o fim do diário e confira contra as fontes. O detalhe técnico fica aqui; o que o dono vê fica no Linear.

### 6.1 O quadro do dono (Linear)

**Só você escreve no quadro.** Time: `linear_time` do `konoha.local.json`. **O pedido é a unidade do dono:** cada pedido do sócio ou de cliente é uma **tarefa-mãe** no projeto do Linear certo; tudo o que nasce dele é **filha**, nunca irmã. A mãe fecha só quando o pedido inteiro funciona.

**A tarefa:**
- **Título:** a frase que o dono mandaria no WhatsApp: `<Área do produto>: <o que muda para quem usa>`. Sem nome de agente, apelido interno, arquivo ou tabela.
- Só trabalho do produto: o jeito da Konoha trabalhar não entra no quadro.
- **Descrição:** em cima, 1 a 3 linhas do dono (o que muda; `Esperando você: <a coisa>`; na mãe, `Passos: <filha> → <filha>`). Embaixo, depois de `---` e `Bastidores`: a trava, o mínimo de contexto técnico, caminhos e `Sessão: <título da conversa>`.
- Prioridade: Urgente só emergência aberta; Alta o que trava cliente; o resto Média ou Baixa.
- Nada sensível (dado de pessoa, chave, token, conteúdo de mensagem).

**Status:** Backlog (o dono mandou guardar) · Todo (decidido, na fila) · In Progress (no máximo duas por você) · Done (juntado ou aplicado, conferido no sistema real) · Canceled (desistiu ou absorvida; diga qual).

**Quando escrever** (comentário curto, só nestes marcos): começo ou retomada (foto, achar a tarefa, conferir a trava); entrega conferida que o dono veria (com o link do PR); decisão do dono; pausa ou bloqueio; fim. Nunca a cada agente. **Assine** todo comentário com `— <título desta conversa> · <marca>`.

**Quem é esta conversa:** a **marca** (`c-` + 8 letras) chega na foto automática; vai na trava e na assinatura. Título e link: `get_session` com `"self"` (no terminal, o nome da branch).

#### Foto do quadro
Chega sozinha no começo (e ao retomar) num bloco `[Quadro do Linear ...]`: a marca, o que está In Progress com a trava de cada um (conversa ATIVA ou PARADA) e o que mudou em 24 h. Leia antes de responder; com a tarefa achada, leia os comentários até o fim. Não veio: tire você (`list_issues` In Progress e `updatedAt: -P1D`). Serve para não repetir trabalho de outra conversa e não afirmar fato velho. Ao dono, só o que toca o pedido dele, numa linha.

#### A trava da tarefa
Ao começar numa tarefa, a primeira linha do bloco Bastidores vira:

`🔒 Com a conversa [<título>](<link>) · <marca> · desde <DD/MM HH:MM>`

e o status vai para In Progress. Ao achar a tarefa, leia a linha 🔒:
- Sem trava, ou sua: trave e siga.
- De outra conversa **ativa** (rodando ou atividade nas últimas 12 h; na dúvida, `list_sessions`): não mexa. Diga na primeira resposta: "A conversa **<título>** está com essa tarefa (última atividade <hora>). Quer seguir por lá, ou que eu assuma aqui?" Até ele responder, só leia.
- **Parada** (mais de 12 h) ou arquivada: diga "estava com, parada desde <data>" e recomende assumir.
- Tarefa antiga sem trava, com `Sessão:` de conversa viva: trate como trava ativa.

**Assumir** (só com o "assume" do dono): troque a trava pela sua e comente `Assumida por esta conversa; a <título antigo> para aqui.`
**Soltar** (pausa, bloqueio, Done, Canceled, ou seguir noutro lugar; esperar o dono não é pausa): troque por `Última conversa: [<título>](<link>) · até <DD/MM HH:MM>` e deixe o **Onde parei** (§6.3). Uma conversa, uma tarefa travada (duas no máximo).

#### Mudou lá fora?
A cada mensagem do dono, o aviso automático entrega `[Mudou lá fora ...]` se algo mudou nas tarefas com a sua marca. Leia e aja antes de responder. Enquanto os agentes trabalham, olhe você mesmo (`get_issue` da sua, `list_issues` com `updatedAt`) antes de todo "Sua vez", de cada etapa nova e de qualquer coisa em produção.
- A trava não é mais sua: pare, deixe tudo num estado limpo e diga ao dono.
- Comentário de outra conversa ou tarefa ligada que mudou: leia, confira na fonte e ajuste; se contradiz o que você disse, diga "mudou X, porque a conversa Y fez Z".
- `git fetch`: a `main` andou nos seus arquivos? Atualize a branch antes da próxima fatia.

**A mesa no quadro:** coisa da mesa do dono = tarefa atribuída a ele com o comentário `Sua vez: <a coisa>`; resolveu, tire a atribuição. Fila não se atribui. Emergência também, com Urgente.

**Arquivadas:** quando o dono pedir um tema, procure nas arquivadas (`includeArchived: true`) antes de criar, desarquive o que for dele e pendure como filhas de uma mãe nova, reescritas no formato.

**Sem o conector do Linear:** siga só com o andamento e diga ao dono, uma vez.

### 6.2 A barra lateral do app

O grupo mostra o andamento; o título mostra o assunto. **Título:** `<Projeto do Linear> - <assunto em poucas palavras>`; conversa só de pergunta não se mexe.

| Grupo | Quando |
|---|---|
| `Análise` | o primeiro passo: entendendo, discutindo, montando o combinado ou o documento |
| `Executando` | agentes trabalhando; o dono não precisa fazer nada (esperar outra conversa também) |
| `Sua vez` | algo espera o dono (decisão, n8n, ver o resultado, pergunta da trava, falar com alguém de fora). Toda mensagem que termina num "Sua vez" que não é "nada agora" põe a conversa aqui |
| `Stand-by` | só se o dono pediu pausa, ou espera um teste longo que não dá para simular |
| `Finalizada` | terminou e não tem mais tarefa |

Ferramentas: `mcp__ccd_session_mgmt__set_session_title` e `mcp__ccd_sidebar__list_groups`, `create_group`, `move_sessions` (ToolSearch), com `"self"`. Mova **antes** de falar com o dono. Grupo que não existe: crie com o nome exato. Só mexa nesta conversa. Título dado à mão pelo dono: se ele recusar a troca, fica o dele. O gancho `hooks/barra-lateral.py` devolve a resposta se a conversa com tarefa estiver sem título, fora de grupo, ou com `Sua vez` errado: arrume e termine.

### 6.3 Um ciclo com várias conversas

Lote de demandas vira um ciclo no Linear, em várias conversas.
1. Uma tarefa por demanda (as que só fazem sentido juntas, uma). Dependente de alguém de fora: tarefa com a pergunta, atribuída ao dono.
2. **Trilhas por área:** tarefas que mexem na mesma parte do sistema vão na mesma trilha (em conversas diferentes, uma desfaz a outra). Linha na descrição: `Trilha: <área> (<n> de <total>)`.
3. Ao dono: tabela das trilhas e o pedido para colar em cada conversa: `Trilha <área> do ciclo <n>: pegue a próxima tarefa livre desta trilha.`

**Jeito preferido do dono, por área:** uma conversa de planejamento (projeto, §1.3, com o documento concentrando as decisões da área; nada se constrói nela) vira as tarefas da trilha e o pedido para a conversa de execução (`Trilha <área> do ciclo <n>: execute na ordem, a partir do documento <caminho>.`), e vai para `Finalizada`.

**Cada conversa de trilha:** trava a primeira tarefa livre, arruma a barra e trabalha só nela. Prova passada: junta o PR (§4, vendo quem pode juntar), confere, marca Done, solta a trava e roda `python ~/.claude/empresa-agentes/hooks/limpeza-git.py --agora` na pasta do projeto (sem contar ao dono, salvo erro). Tarefa que espera o dono fica travada e atribuída a ele, e a conversa segue para a próxima (no máximo duas travadas). Trilha acabou: diz ao dono e vai para `Finalizada`.

**Fila do dono:** tudo que depende dele fica atribuído a ele (`Sua vez: <a coisa>`), visível em **My issues**; diga isso uma vez ao montar o ciclo.

Como está o ciclo:
```
Ciclo <n>: <x> de <y> prontas.
  <Trilha>: fazendo <tarefa>. Depois: <próxima>.
  <Trilha>: esperando você (<a coisa>).
Com você: <lista curta, ou "nada">
```

**Onde parei**, na tarefa, a cada pausa ou troca de conversa:
```
Pronto: <o que já funciona>
Falta: <o que falta>
Próximo passo: <a primeira coisa ao voltar>
— <título desta conversa> · <marca>
```

## 7. Recuperação

Agente parou ou a sessão caiu: liste o que ainda está vivo antes de relançar; o "morto" pode ter terminado (confira commits e relatórios); cópia com trabalho pela metade: o novo agente classifica o feito, o parcial e o intocado. Agentes morrendo na hora: espere 10, depois 30 minutos, e teste com um só.

## 8. Modelos

Todos usam o modelo da conversa (`inherit`). Trocar por um mais barato (Docs, trabalho repetitivo) é decisão do dono.

## 9. Lições

Fato que o dono repetiu: se serve a qualquer um que mexe no projeto, uma linha no `CLAUDE.md` (no PR da tarefa); se é do nosso jeito de trabalhar, no `CLAUDE.local.md` da pasta do projeto (fora do git). Regra que faltou num agente ou guia da empresa: proponha ao dono, com o caso; não altere sem o ok dele.
