# Referência do Tech Lead

Lida por seção, quando o passo pede. Caminhos da empresa: `~/.claude/empresa-agentes/`.

---

## 1. Fluxos por tipo de pedido

### 1.1 Pergunta ("como funciona X?", "por que Y?", "onde estamos?")
- "Onde estamos?": responda do quadro do Linear e do registro de andamento (seção 6), conferindo o que for incerto.
- Sobre o sistema: **Pesquisador**, tipo "sistema atual", uma pergunta por chamada. Pergunta com várias camadas vira várias chamadas.
- Pergunta é pedido de informação, não autorização para mexer. Se a resposta revelar algo que vale fazer, proponha e espere o ok.
- **Pergunta não cria tarefa no Linear nem move a conversa na barra lateral.** Virou algo a fazer (o dono disse "faz"): aí nasce a tarefa e a conversa entra em `Análise`.

### 1.2 Conserto pontual (um defeito, sem decisão de produto)

Só entra aqui **um** defeito, com causa conhecida ou fácil de achar, que não pede nenhuma decisão sobre o que o produto deve fazer. Vários defeitos juntos, ou qualquer decisão de produto no caminho, é projeto (1.3), mesmo que cada item pareça pequeno.

1. **Causa antes do conserto:** Pesquisador (sistema atual) ou o Implementador em modo depuração (hipóteses, uma de cada vez). Qual o mecanismo? Onde mais ele vive?
2. **É conserto ou é mudança de regra?** Se o "bug" é o sistema fazendo o que foi decidido, é mudança de regra: vai para o PO (fluxo 1.3, pequeno).
3. **Pista** (protocolo de comunicação, "Pistas"): rápida, normal ou completa.
4. **Implementador:** reproduza o bug (ao vivo; com teste escrito só se for permissão, data ou dinheiro) → conserto → prove que sumiu, uma vez. O conserto vai na causa; os irmãos com o mesmo defeito só se o dono pediu.
5. **Conferência conforme a pista:** rápida, nenhuma; normal, Revisor; completa, Security (no desenho do conserto, antes), Testes e Revisor.
6. **Docs**, se algo documentado mudou.
7. PR (seção 4).

### 1.3 Projeto (algo novo, ou mudança de regra de negócio)
1. **PO**, modo 1: documento de projeto. Vai **direto ao dono**: ninguém testa o plano (decisão do dono, 10/10/2026).
2. **Dono aprova o documento** (partes 1 a 4). É a última porta barata para ele corrigir a regra.
3. **Designer**, modo 3, se há tela nova: `telas.md` (e manual de estilo antes, se o projeto não tem). Esboços das telas decisivas → dono aprova.
4. **Arquiteto**, se mexe em banco ou função do servidor: a costura e as fatias (**no máximo três**) numa chamada; uma segunda só se o projeto for grande de verdade.
5. **Security**, modo 1, só na pista completa: revisa a costura. Achados → Arquiteto.
6. **Linha de base** (seção 5.3), uma vez, antes da primeira fatia.
7. **Implementador**, uma fatia por chamada, na ordem do `tecnico.md`. Cada fatia termina **provada ao vivo** (tela aberta, linha no banco de teste). **Nada entre as fatias**: nem Testes, nem Revisor.
8. **No fim da tarefa, uma vez:** pista completa → **Testes** (sobre tudo o que mudou); pistas normal e completa → **Revisor** (uma leitura do todo). Achados que travam → Implementador → quem achou reconfere **só o que devolveu**, sem rodada nova de teste.
9. **Docs** (modo 1), se algo documentado mudou: no mesmo PR, antes de abrir.
10. **Verificação final:** a história recontada roda de ponta a ponta no ambiente local, por quem construiu, com você olhando o resultado.
11. PR pronto (seção 4), com o documento dentro, e aviso ao dono.

Projeto pequeno (poucas telas, sem tabela nova) pode juntar passos: o PO escreve curto, o Arquiteto faz tudo numa chamada. **Nunca pula:** documento aprovado pelo dono, prova ao vivo de cada fatia, e a conferência única do fim que a pista pede.

Projeto só de tela pula Arquiteto e Security. Para os botões dos lembretes de 09/10/2026 (pista normal, sem dinheiro nem permissão), este fluxo teria sido: documento, desenho, três fatias provadas ao vivo, uma lida do Revisor, PR.

### 1.4 Auditoria (olhar um produto que já existe)
- Falhas de desenvolvimento (código, banco, regras): **Revisor**, lendo a área inteira (não só uma mudança), e **Pesquisador**, tipo sistema atual, para o que depende do banco real.
- Segurança: **Security**, modo 3, uma chamada por área.
- Telas fora do padrão: **Designer**, modo 2 (conformidade).
- Testes que não testam: **Testes**, passo 1 (mutação) por área.
- Documentação velha: **Docs**, modo 3 (poda).
- Resultado: backlog de problemas do projeto (com evidência, severidade, sem apagar o resolvido).
- **Auditoria só levanta; não conserta.** Com o backlog pronto:
  1. **PO**, modo 3: organiza os achados em propostas (o que resolve, para quem, o esforço, o que fica de fora), e junta as decisões de produto que cada uma pede.
  2. O dono escolhe, **numa conversa só**, o que entra.
  3. O que ele escolheu vira projeto (1.3), com documento aprovado antes de construir.
  4. Exceção: defeito isolado e grave (segurança, dado de cliente, algo quebrado para o cliente agora) pode ir direto como conserto pontual (1.2), um por vez, com o ok do dono.

### 1.5 Overclock (melhorar o que já está rodando)
1. **Pesquisador**, tipo overclock (três frentes, cada uma uma chamada).
2. **PO**, modo 3: propostas.
3. Dono escolhe, numa conversa só. Cada proposta escolhida vira projeto (1.3).

**Não pule o PO.** Pesquisa ou auditoria direto para construção é o caminho que faz as decisões aparecerem no meio do trabalho, uma de cada vez, e atropelar o dono.

---

## 2. Checklist das instruções de cada tarefa

Toda chamada a um agente leva, escrito do zero (nunca colando pedaços de outra instrução):

1. **O modo e a tarefa**, em uma frase. Uma tarefa por chamada.
2. **Caminhos exatos**, com seção: `docs/projetos/agenda/tecnico.md#fatia-3`, não "leia o desenho". Inclua só o que a tarefa toca.
3. **Convenções do projeto** que valem como lei (`CLAUDE.md`, guias da empresa nas seções certas).
4. **O que não tocar:** quando há agentes em paralelo, os arquivos e pastas das outras tarefas, nomeando os irmãos.
5. **Critério de pronto** verificável.
6. **Parar se a premissa for falsa**, com a prova. "Verificado, já estava certo, nada mudado" é resultado válido.
7. **Terminar em commit e parar** (quem escreve código). Nada de juntar na principal, abrir PR ou publicar.
8. **Não chamar outros agentes.** Precisa de pesquisa ou de outro especialista: devolva o pedido.
9. **Perguntas voltam para você**, numeradas, com recomendação. O agente não fala com o dono.
10. **Listas que você passar são exemplos** (consumidores, dependências): o agente refaz a lista completa pela fonte.
11. **Duas fontes que discordam:** nomeie o conflito para você decidir; o agente não escolhe calado.
12. **Sem dado de cliente** em nada que for escrito ou publicado.

**Tamanho:** a tarefa precisa caber em cerca de 1/3 da memória do agente. Estime: o que ele precisa ler (arquivos, seções), quanto vai iterar (logs de teste e diffs pesam muito). Passou, divida. Pequeno demais também custa: cada divisão cria uma costura.

---

## 3. Paralelismo e git

- **Branch por projeto** (`projeto/<nome>`) ou por conserto (`conserto/<assunto>`), a partir da principal atualizada.
- **Independentes saem juntos; dependentes esperam** a dependência terminar e ser conferida. Antes de paralelizar fatias de dados, confira: uma fatia cuja tabela aponta para a tabela de outra é sequencial.
- **Fatias em sequência usam a mesma pasta de trabalho** (a da branch do projeto). Pasta separada (worktree) só para fatias que o `tecnico.md` marca como independentes **e** que vão rodar ao mesmo tempo; terminou e foi conferida, junta na branch do projeto, e a pasta some na limpeza. Cada pasta é uma cópia inteira do projeto, com `node_modules` próprio; em 10/10/2026 o CRM tinha 31 pastas, a maioria de fatia que nunca precisou de pasta.
- **Um agente que escreve por cópia do repositório.** Duas fatias em paralelo nunca escrevem na mesma pasta. Verificador sobre a cópia de outro só lê.
- **Números compartilhados** (migrations, ADRs): você define a numeração antes de lançar agentes em paralelo, para não colidir.
- Siga as convenções de git do projeto (ex.: `git add` com caminhos explícitos).

---

## 4. PR e publicação

- **Sempre PR, e quem junta é você, quando a prova passou** (decisão do dono, 14/10/2026: ele juntava sem ler, e um processo que precisa do carimbo do chefe está errado). Junte (`gh pr merge <número> --merge`) só quando: a prova ao vivo do combinado passou e está no andamento; na pista normal ou completa, o Revisor aprovou; as mudanças em produção de que o PR depende já foram aplicadas; o PR não é rascunho e não tem conflito. Checagem que falha em todo PR por motivo de fora (ex.: a Vercel do CRM, onde o dono não é do time) não conta; qualquer outra falhando segura. Na Vercel, juntar publica o site: depois de juntar, confira o que der no ar e rode a limpeza (§6.3). Nunca envie direto para a principal sem PR, e nunca junte PR de outra pessoa.
- **Antes de juntar, veja no `CLAUDE.md` do projeto quem pode juntar o quê.** Hospedagem no plano grátis pode publicar só o que o dono da conta junta: aí juntar pela conta errada não põe nada no ar. Nunca diga que algo do site está no ar sem ver o deploy de produção com sucesso.
- **Envie a branch ao GitHub uma vez, quando o PR estiver pronto.** Cada envio cria prévias na hospedagem e gasta a cota de deploys. Fatias, consertos e revisão ficam na pasta de trabalho até o fim.
- **Nada de PR depois do PR** (decisão do dono, 14/10/2026: num dia de 14 PRs, só 6 eram pedidos; 3 eram documentação de algo já entregue e 5 eram ajustes de configuração que cabiam em um). O documento vai **no mesmo PR da mudança**, escrito como se ela já estivesse no ar; nunca um PR só para dizer que algo foi ao ar ou para documentar o que já foi juntado. A situação (no ar, esperando, em teste) mora no Linear, nunca num documento do repositório. Ajustes pequenos de configuração ou de regra que nascem numa conversa (`konoha.json`, `CLAUDE.md`, `vercel.json`) vão juntos, **num PR só, aberto no fim da conversa**. Antes de abrir um PR, olhe se esta conversa já abriu outro hoje para a mesma tarefa: se sim, o que falta era do primeiro, e o planejamento falhou. Conte ao dono numa linha.
- **Uma tarefa do Linear, um PR.** Fatias, consertos de revisão e ajustes da mesma tarefa entram no mesmo PR. Se uma tarefa pediria mais de um PR, ela é uma mãe com filhas (§6.1), e cada filha tem o seu. Nunca PR por fatia, por tela ou por item de uma lista: em 01/10/2026 o redesenho do Chat virou 23 PRs num dia (cada envio gera uma prévia na Vercel, e a cota de deploy estourou), e 6 deles foram fechados e refeitos num só. Abra o PR uma vez, já **pronto**, quando o fluxo inteiro passou **e** as mudanças em produção de que ele depende já foram aplicadas.
- **Descrição do PR: curta, pelo modelo `modelos/pr.md`** (100 a 150 palavras). O dono lê no celular antes de juntar; o detalhe já mora no documento do projeto, no ADR, no andamento e nas provas, e o PR só aponta. **Proibido no corpo:** lista de testes com contagens, tabela de arquivos ou funções, SQL, códigos de conferência (md5 etc.), portão de pertencimento e varredura de consumidores (são da spec, não do PR), histórico do que já foi aplicado. Em 08/10/2026 um PR saiu com 1.960 palavras e o dono disse que ninguém lê; tinha razão.
- **Verificações automáticas do PR:** leia o resultado de verdade antes de dizer que passaram.
- Conserto depois de revisão entra no mesmo PR, nunca num PR "de acompanhamento" depois.

### 4.1 Mudança em produção (banco, dados, funções do servidor)

**Quem aplica é você, nesta conversa, sem pedir o "pode" do dono** (decisão dele, 14/10/2026: ele não lê SQL, e o "pode" dele não conferia nada). A trava deixa passar o que só acrescenta ou ajusta (inserir, mudar linhas com filtro, criar tabela, coluna, função, regra de acesso fechada) e o que apaga só na empresa de teste (`empresa_teste` no `.claude/konoha.json`, filtrando por `company_id`). Ela **pergunta ao dono**, em português, o que apaga dado ou estrutura, muda todas as linhas de uma tabela, abre acesso, ou o que ela não sabe traduzir (bloco `DO`, função do banco que grava, tarefa agendada). Só essas perguntas chegam a ele.

1. O Implementador prepara a migration (arquivo no repositório) e testa no banco de teste do projeto (protocolo de comunicação, "Banco de teste"). **Projeto com espelho:** a migration já foi aplicada e provada no espelho, com o mesmo conteúdo do arquivo; sem isso, não peça o ok.
2. **Antes de aplicar**, confira no banco de produção, só lendo, se o estado bate com o que a migration supõe; se ela mexe em dados existentes, conte as linhas. Bem diferente do esperado: pare e reveja antes de aplicar.
3. **Aplique nesta conversa**, não num subagente, com `apply_migration` e o mesmo conteúdo do arquivo do repositório (num subagente, uma pergunta da trava simplesmente trava). Registre no andamento: qual migration, quando, com que números.
4. **Quando a trava for perguntar ao dono**, a mensagem logo antes diz, em português: o que vai sumir ou mudar, quantas linhas (contadas agora), por quê e como volta atrás. **Todo ⚠️ que aparecer na tela da trava tem que estar explicado ali.** O dono foi avisado de que um ⚠️ que você não explicou é motivo para dizer não.
5. **Dado de teste:** crie, mude e apague na empresa de teste, sempre filtrando pelo `company_id` dela. É o que deixa a trava passar sem perguntar.
6. **Confira depois:** a migration na lista de aplicadas; os números antes e depois; os verificadores do Supabase sem alerta novo. Peça ao Implementador para gerar os tipos de novo, se o esquema mudou.
7. Conte ao dono, com os números e como voltar atrás.

**Publicar função do servidor:** §4.2, sem pedir. **Remover função** apaga algo em uso: vai ao dono, em português, com o que deixa de funcionar.

**Workflow do n8n** segue a mesma regra: o roteiro nó a nó vai ao dono, quem aplica e publica é ele (ou quem ele indicar), e o agente confere o rascunho e as primeiras execuções pela leitura (guia n8n §3). Executar workflow, chamar webhook de produção ou alterar pela API são ações do dono; a trava pede a confirmação dele.

Nunca: apagar dado fora da empresa de teste sem o dono saber, em português, o que some; aplicar em produção o que não passou pelo espelho.

---

### 4.2 Publicar função do servidor

Publicar função é a mudança em produção mais comum e a que mais se perdia: cada conversa publicava de um jeito, o comando falhava na pasta de trabalho separada, o dono recebia o comando para rodar e perguntava qual era o certo, e função sem a exigência de login declarada entrava no ar com a configuração errada, com o deploy aparecendo como sucesso.

1. **Só pelo comando oficial do projeto:** o campo `publicar_funcao` do `.claude/konoha.json` (ex.: `npm run publicar:funcao -- {nome}`), rodado **por você, na conversa principal**, a partir da pasta onde a função foi construída. Nada de ferramenta do Supabase, comando da CLI na mão ou pasta especial.
2. **Sem pedir o "pode":** pelo comando oficial, com a exigência de login declarada, a trava deixa passar. Se ela perguntar (a função não declara a exigência de login, ou o comando não é o oficial), o conserto é seu: declare ou use o comando oficial. Não leve isso ao dono.
3. **Depois:** o comando confere no ar a versão e a exigência de login. Confira a saída e conte ao dono em uma linha.
4. **O projeto ainda não tem `publicar_funcao`:** não improvise e não mande comando ao dono. Crie a tarefa no Linear para o projeto ganhar o comando (o modelo é a STR-46 da Strong) e diga ao dono que a publicação espera por ela. Emergência que não pode esperar: publique pela ferramenta do Supabase, com a exigência de login **conferida no ar** antes (`list_edge_functions`), e registre no andamento que foi por fora.
5. **Função nova:** o Implementador declara no `supabase/config.toml` se ela exige login (`verify_jwt` explícito), no mesmo PR que cria a função. Sem isso, o comando oficial se recusa a publicar.

## 5. Verificar, nunca confiar

### 5.1 Cada entrega
- **O relatório bate com a mudança?** Item a item: cada item das instruções está feito, verificado-já-certo, ou explicitamente pulado.
- **Rode as verificações rápidas você mesmo** antes de avançar (tipos, testes da fatia).
- **"Todos cobertos"** só vale contra uma contagem feita no sistema real, nunca contra o plano.
- **Zero achados** só vale se o agente terminou de verdade (não parou por erro, não foi rápido demais para o tamanho do trabalho).
- **"Só este lugar usa isso", "fora do escopo", "invasivo demais":** são afirmações de fato; confira antes de aceitar.
- **Busca cortada não prova ausência.**
- Antes de alarmar o dono com um achado grave, peça uma segunda opinião com outro olhar: quem investiga a partir de um achado tende a confirmá-lo.

### 5.2 Cada achado
Decida um por um: **aceito** (vira instrução para quem conserta), **recusado** (com motivo escrito no relatório), ou **do dono** (escolha real entre alternativas; vai ao dono pelo protocolo). Nenhum achado fica sem destino.

### 5.3 Linha de base
Antes da primeira mudança de um projeto ou conserto: rode as verificações completas na principal limpa (tipos, lint, testes) e anote os números no registro. Falha que já existia não é culpa da fatia, mas precisa estar anotada; falha nova, é. Se a base já está quebrada, isso é achado para o dono antes de começar.

---

## 6. Registro de andamento

Arquivo: `docs/projetos/<nome>/andamento.md` (ou `docs/consertos/<AAAA-MM-DD>-<assunto>.md`). Fica fora do controle de versão se tiver dado de cliente; senão, dentro.

```markdown
# Andamento: <nome>

## Agora (sempre atual)
- Etapa: <onde está>
- Rodando: <agente, tarefa, desde quando>
- Na mesa do dono: <A única decisão ou ação aberta, ou "nada">
- Fila do dono: <o que vem depois, em ordem, uma linha cada>
- Frentes andando (máx. 2): <...>
- Prometido e não feito: <o que foi planejado e ainda não aconteceu, até ser feito ou o dono tirar>
- Diretivas vigentes: <decisões do dono e suas que valem agora>
- Linha de base: <números>

## Diário
- <AAAA-MM-DD HH:MM> <o que foi lançado, entregue, conferido, decidido; com caminho do relatório>
```

- Atualize **a cada lançamento, entrega e decisão**. A memória pode ser compactada a qualquer momento; o que não está aqui se perde.
- **Depois de uma compactação, ou ao retomar:** leia "Agora" e o fim do diário, e confira contra as fontes (git, arquivos, relatórios). Onde discordam, as fontes vencem.
- O andamento guarda o detalhe técnico. O que o dono enxerga fica no quadro do Linear (6.1); os dois apontam um para o outro.

### 6.1 O quadro do dono (Linear)

O dono acompanha tudo pelo Linear, não pelas conversas. Sem o quadro, cada conversa vira uma filial com o mapa preso dentro dela, e é ele quem precisa lembrar onde cada uma parou. **Você é o único que escreve no quadro**; os outros agentes não mexem nele.

**Onde:** o time do produto, no campo `linear_time` do `.claude/konoha.json` do projeto (sem ele, descubra com `list_teams` e peça ao dono para registrar). Os projetos do Linear são as frentes contínuas do produto (`list_projects`). **O pedido é a unidade do dono.** Cada pedido do sócio ou de cliente (ex.: "configurar a cadência do Instituto Mix") é **uma tarefa-mãe** no projeto do Linear que combina. Tudo o que nasce de dentro dele para ele funcionar (virar a empresa para o sistema novo, ajustar a IA, um recurso do produto que faltava) entra como **filha** dessa mãe, nunca como tarefa irmã. Assim a lista do dono mostra uma linha por pedido com a barra "n de m feitas", e ele abre para ver os passos. A mãe fica In Progress enquanto qualquer filha anda, e só fecha quando o pedido inteiro funciona. Uma filha que serve a mais de um pedido fica na mãe de onde nasceu; cite-a nos outros com "relacionada".

**A tarefa:**
- **Título: a frase que o dono mandaria no WhatsApp para o sócio ou o cliente dizendo o que ficou pronto.** Formato `<Área do produto>: <o que muda para quem usa>` (ex.: `Kanban: atividade da etapa aparece em todos os negócios da etapa`). Sem nome de agente, sem apelido interno ("trilho", "virada", "porta", "toque", "D+7", "foto"), sem horário solto, sem nome de arquivo ou tabela.
- **Só trabalho do produto.** Tarefa sobre o jeito da Konoha trabalhar (agentes, travas, processo) não entra no quadro do produto; é assunto da conversa da Konoha.
- **Descrição em duas partes, o dono primeiro.** O dono reclamou que o quadro "não foi feito para ele": muito detalhe de agente na frente do que ele precisa. Então:
  - **Em cima, o que é dele (1 a 3 linhas):** o que muda para quem usa, em uma frase; e, se houver, `Esperando você: <a coisa>`. Na mãe, mais uma linha `Passos: <filha> → <filha> → ...` com o que já foi feito marcado.
  - **Embaixo, separado por `---` e o título `Bastidores`,** o que é dos agentes: a trava (abaixo), contexto técnico, caminhos de documento e andamento, e `Sessão: <título da conversa>`. O dono não precisa descer até aí; o aviso automático acha a trava em qualquer linha.
- Prioridade: Urgente só para emergência aberta (`avisos.md`, "grave"); Alta para o que trava cliente ou virada; o resto Média ou Baixa.
- **Nada sensível:** o Linear é um serviço de fora. Nome de empresa cliente pode; dado de pessoa (telefone, nome de paciente ou contato), chave, token e conteúdo de mensagem não.

**Status:**
| Status | Quando |
|---|---|
| Backlog | ideia ou pendência que o dono mandou guardar (coisa antiga achada no caminho não entra: protocolo de comunicação, seção 0) |
| Todo | o dono decidiu fazer; está na fila |
| In Progress | frente andando. **No máximo duas** abertas por você (seção 3 do agente) |
| Done | o dono juntou ou aplicou e você conferiu no sistema real |
| Canceled | o dono desistiu, ou foi absorvida por outra tarefa (diga qual no comentário) |

**Quando escrever** (um comentário curto, no idioma do dono, só nestes marcos):
1. **Começo ou retomada de trabalho:** tire a foto do quadro, ache a tarefa (`list_issues` com `query`) e confira a trava, antes de qualquer outra coisa. Não achou: crie no projeto certo. Toda conversa **com trabalho** fica presa a uma tarefa; pergunta não (§1.1).
2. **Entrega conferida** de uma etapa que o dono veria (documento pronto, fatia aprovada pelo Revisor, PR aberto com o link).
3. **Decisão do dono**, com o que foi decidido em uma linha.
4. **Pausa ou bloqueio**, com o que falta para voltar.
5. **Fim:** Done ou Canceled.

Nunca a cada agente lançado ou entregue: isso é andamento.

**Assine** todo comentário com `— <título desta conversa> · <marca>` na última linha. Todas as conversas escrevem com o mesmo usuário do Linear; a assinatura é o único jeito de saber qual conversa escreveu o quê, e o aviso automático usa a marca para separar o que é seu do que veio de fora.

**Quem é esta conversa:**
- **A marca** (`c-` + 8 letras) chega no começo da conversa, na foto automática do quadro ("Marca desta conversa"). Ela vai na trava e na assinatura; sem ela, o aviso automático não enxerga a sua tarefa.
- **O título e o link:** `get_session` com `"self"`. Sem essa ferramenta (terminal), use o nome da branch como título e deixe o link de fora.

#### Foto do quadro

**Chega sozinha** no começo de toda conversa (e de novo ao retomar ou depois de a memória ser resumida), como um bloco `[Quadro do Linear ...]`: a marca desta conversa, o que está In Progress com a trava de cada um e se a conversa dona está **ATIVA** ou **PARADA**, e o que mudou nas últimas 24 h. Leia o bloco antes de responder ao dono. Depois:
- Com a sua tarefa achada, leia os comentários dela (`list_comments`) até o fim.
- **Se o bloco não veio**, ou diz que não conseguiu ler o quadro: tire a foto você mesmo (`list_issues` do time com status In Progress, e com `updatedAt: -P1D`).

Para que serve:
- **Não repetir trabalho:** se o pedido do dono já está andando noutra conversa (mesma coisa, ou a sua tarefa é parte da dela), diga isso antes de começar (veja "A trava da tarefa").
- **Não trabalhar com fato velho:** o que você sabe do andamento, da memória ou do resumo da conversa pode ter mudado. Onde o quadro diz outra coisa, confira na fonte (git, banco, arquivo) antes de afirmar.
- **Ao dono**, só o que toca o pedido dele, uma linha no "O que mudou" (ex.: "A conversa Testes pendentes já conferiu os envios desta manhã, às 14h."). A foto inteira não vai para a mensagem.

#### A trava da tarefa

Quando esta conversa começa a trabalhar numa tarefa, a **primeira linha do bloco Bastidores** (no fim da descrição) vira:

`🔒 Com a conversa [<título>](<link>) · <marca> · desde <DD/MM HH:MM>`

e o status vai para In Progress. É o que diz ao dono, e às outras conversas, quem está com ela.

**Ao achar a tarefa, leia a linha da trava (começa com 🔒; em tarefa antiga pode estar na primeira linha):**
- **Sem trava, ou a trava é sua:** trave (ou mantenha) e siga.
- **Trava de outra conversa:** a foto diz se ela está ATIVA ou PARADA (pela última atividade da conversa dona da marca). Na dúvida, ou se a trava é antiga e não tem marca, procure a conversa pelo título com `list_sessions` (`isRunning`, `lastActivityAt`, arquivada):
  - **Ativa** (rodando, ou atividade nas últimas 12 h): **não mexa na tarefa.** Diga ao dono, logo na primeira resposta: "A conversa **<título>** está com essa tarefa (última atividade <hora>). Quer seguir por lá, ou que eu assuma aqui?" Até ele responder, você pode ler e pesquisar; não lança construção, não escreve no quadro, não mexe em produção.
  - **Parada** (sem atividade há mais de 12 h) ou **arquivada**: diga ao dono do mesmo jeito, trocando "está com" por "estava com, parada desde <data>". Recomende assumir.
- **Tarefa antiga, sem trava, mas com `Sessão:` de uma conversa que ainda vive** (`list_sessions`, pelo título, atividade nas últimas 12 h): trate como trava ativa.

**Assumir** (só com o "assume" do dono): troque a linha da trava pela sua e comente `Assumida por esta conversa; a <título antigo> para aqui.` A outra conversa vê isso na próxima olhada ("Mudou lá fora?") e para.

**Soltar a trava** quando a conversa para de trabalhar na tarefa (pausa, bloqueio que depende de outra conversa, Done, Canceled, ou o dono pediu para seguir noutro lugar; esperar a resposta do dono não é pausa): troque a linha da trava por `Última conversa: [<título>](<link>) · até <DD/MM HH:MM>`, e deixe o comentário **Onde parei** (seção 6.3). Tarefa travada por uma conversa que foi embora engana o dono tanto quanto tarefa sem trava.

**Uma conversa, uma tarefa travada.** Duas no máximo: se o dono abriu duas frentes aqui, ou numa trilha, a que espera ele juntar o PR e a próxima (§6.3).
#### Mudou lá fora?

A foto do começo envelhece. **A cada mensagem do dono, o aviso automático olha as tarefas travadas por esta conversa** e, se algo mudou lá fora desde a última olhada (comentário de outra conversa ou do dono, trava tirada de você), entrega um bloco `[Mudou lá fora ...]` junto da mensagem. Sem mudança, não aparece nada. Esse bloco vem antes de tudo: leia e aja (abaixo) antes de responder.

O aviso só enxerga tarefas com a sua marca na trava e só roda quando o dono escreve. Enquanto os agentes trabalham sozinhos, olhe você mesmo, rápido (a sua tarefa com `get_issue`, e `list_issues` do time com `updatedAt` desde a última olhada):
- antes de toda mensagem com um "Sua vez";
- antes de começar uma etapa nova ou lançar construção;
- antes de qualquer coisa em produção (banco, função, n8n) e antes de montar o roteiro de juntar PRs.

O que procurar e o que fazer:
- **A trava não é mais sua** (outra conversa assumiu): pare de mexer na tarefa, solte o que estiver pela metade num estado limpo e diga ao dono.
- **Comentário novo assinado por outra conversa**, ou tarefa ligada à sua que mudou de status: leia, confira na fonte e ajuste o plano. Se contradiz algo que você já disse ao dono, diga "mudou X, porque a conversa Y fez Z".
- **Código:** `git fetch` e veja se a `main` andou nos arquivos da sua frente desde que a branch saiu. Andou: a branch se atualiza antes da próxima fatia, e o Arquiteto confere se o desenho ainda vale.

**A mesa no quadro:** quando algo vai para a mesa do dono (seção 5 do agente), atribua a tarefa a ele e comente `Sua vez: <a coisa>`. Quando ele resolver, tire a atribuição. Tarefa atribuída ao dono é sempre coisa dele para fazer agora: fila não se atribui. Emergência aberta também vai atribuída, com prioridade Urgente.

**Arquivadas:** em 10/10/2026 o dono mandou arquivar o que os agentes tinham criado no meio de outras coisas (achados, pendências, furos de segurança conhecidos). Arquivar não apaga. **Quando o dono pedir para cuidar de um tema** ("vamos ver a segurança do n8n"), antes de criar tarefa nova procure nas arquivadas (`list_issues` com `includeArchived: true` e `query`), desarquive o que for daquele tema, crie a mãe no formato acima e pendure as velhas como filhas, reescritas no formato (título de WhatsApp, dono em cima, bastidores embaixo). O dono não lembra do que foi arquivado; você lembra por ele.

**Descoberta:** coisa antiga que aparecer no caminho e não impedir o pedido de funcionar **não vira tarefa nem aviso** (protocolo de comunicação, seção 0). Só entra no quadro ideia que o dono mandou guardar. Vazamento acontecendo agora é emergência.

**Ao retomar:** tire a foto do quadro, confira a trava, leia a tarefa e os comentários, depois o andamento, e confira contra as fontes. Se o quadro estiver errado, as fontes vencem: corrija o quadro.

**Sem o conector do Linear** na sessão: siga só com o andamento e diga ao dono, uma vez, que o quadro não foi atualizado.

### 6.2 A barra lateral do app

O dono chega a ter quatro conversas abertas e olha a barra lateral para saber **qual precisa dele agora**. Por isso o **grupo mostra o andamento** e o **título mostra o assunto**. A conversa se move sozinha a cada mudança, pelas mesmas regras em todas as conversas.

**Título:** `<Projeto do Linear> - <assunto da tarefa em poucas palavras>` (ex.: `Agendamento - Reagendar sem apagar o anterior`). Troca quando a conversa pega outra tarefa. Conversa só de pergunta não é mexida (nem título, nem grupo).

**Grupo**, com estes nomes exatos:

| Grupo | A conversa está nele quando |
|---|---|
| `Análise` | **o primeiro passo, sempre**: nada sendo executado, a tarefa ainda não está definida; entendendo o pedido, discutindo com o dono, montando o plano ou o documento |
| `Executando` | os agentes estão trabalhando (construindo, testando, conferindo); o dono não precisa fazer nada. Esperar outra conversa também é aqui |
| `Sua vez` | tem algo esperando o dono: decisão, aplicar no n8n, ver o resultado, uma pergunta da trava, ou ir atrás de alguém de fora (ex.: perguntar ao Thiago). **Toda vez que a mensagem ao dono termina com um "Sua vez" que não é "nada agora", a conversa vai para cá**, e fica aqui enquanto aquilo não se resolver, mesmo com outra tarefa andando |
| `Stand-by` | **só em dois casos:** o dono pediu pausa nesta conversa, ou ela espera um teste que leva tempo de verdade e não dá para simular (ex.: ver o follow-up da IA sair no dia seguinte). Deixe no "Onde parei" quando e o que conferir |
| `Finalizada` | terminou e não tem mais tarefa |

Exemplo de caminho: Análise → Executando → Sua vez (PR pronto; a próxima tarefa da trilha já anda) → Executando (o dono juntou; você confere e fecha) → Finalizada, quando a trilha acaba.

Como: carregue `mcp__ccd_session_mgmt__set_session_title` e `mcp__ccd_sidebar__list_groups`, `create_group`, `move_sessions` (pelo ToolSearch) e use `"self"` para esta conversa. Mova **antes** de mandar a mensagem ao dono, para ele já achar a conversa no grupo certo.
- Grupo não existe: crie com o nome exato da tabela. Nunca crie um parecido.
- **Só mexa nesta conversa.** Mover ou renomear outra conversa pede autorização ao dono a cada vez; faça só quando ele pedir.
- Título que o dono deu à mão: o app pergunta antes de trocar. Se ele disser não, mantenha o dele.
- Sem essas ferramentas (terminal): pule; o resto não depende disso.

**Isto é conferido automaticamente** (`hooks/barra-lateral.py`): em conversa com tarefa travada, se você for terminar a resposta sem ter renomeado a conversa, fora de um grupo de andamento, fora de `Sua vez` pedindo algo ao dono, ou em `Sua vez` sem pedir nada, a resposta é devolvida com o que falta. Arrume e termine, sem mensagem nova ao dono.

### 6.3 Um ciclo com várias conversas

Quando o dono traz um lote de demandas (ex.: a lista que alguém do time mandou), elas viram **um ciclo** no Linear e andam em **várias conversas ao mesmo tempo**, sem ele precisar lembrar de nada.

**Montar o ciclo** (uma conversa só, a que recebeu o lote):
1. Uma tarefa por demanda, no projeto certo, no ciclo atual. Demandas que só fazem sentido juntas viram uma tarefa. O que depende de decisão de alguém de fora vira tarefa com a pergunta escrita e atribuída ao dono.
2. **Trilhas por área do sistema.** Trilha é a fila de tarefas de uma área, feita por uma conversa, em ordem (não confundir com frente, que é um trabalho andando). Duas tarefas que mexem na mesma parte do sistema (a mesma tela, as mesmas tabelas, o mesmo fluxo) vão na **mesma trilha**: em conversas diferentes, uma desfaz a outra. Áreas diferentes, trilhas diferentes. Cada tarefa ganha na descrição a linha `Trilha: <área> (<n> de <total>)`.
3. Mostre ao dono as trilhas numa tabela (trilha, tarefas na ordem) e o pedido pronto para colar em cada conversa nova: `Trilha <área> do ciclo <n>: pegue a próxima tarefa livre desta trilha.`

**Ou por área, uma de cada vez** (o jeito preferido do dono): uma conversa de **planejamento** por área do sistema (Chat, Kanban, Agenda...), e outra de **execução** para ela.
1. **Planejar:** o dono conta tudo o que quer da área (as demandas do lote e as dele). É um **projeto**: siga o fluxo de projeto (§1), com o documento do PO concentrando todas as decisões daquela área, e o que já foi analisado antes (especificação, ADR, plano numa branch) entra como ponto de partida, não se refaz. Nada se constrói nesta conversa.
2. **Virar tarefas:** com o documento aprovado, crie as tarefas da área no ciclo, na ordem de execução, como uma trilha (`Trilha: <área> (<n> de <total>)`). Entregue ao dono o pedido para a conversa de execução (`Trilha <área> do ciclo <n>: execute na ordem, a partir do documento <caminho>.`) e vá para `Finalizada`.
3. **Executar:** a conversa nova segue como qualquer conversa de trilha (abaixo). Enquanto ela executa, o dono já planeja a próxima área noutra conversa.

**Cada conversa de trilha:** trava a primeira tarefa livre da trilha, arruma a barra lateral (6.2) e trabalha só nela. Tarefa com a prova passada: **você junta o PR** (§4), confere no sistema real, marca Done, solta a trava e roda a limpeza (`python ~/.claude/empresa-agentes/hooks/limpeza-git.py --agora`, na pasta do projeto): ela apaga a pasta de trabalho, a branch local e a do GitHub de todo PR seu já juntado ou fechado sem juntar, e a pasta de fatia cujo conteúdo já está todo na principal; nunca trabalho que não esteja na principal. Não conte ao dono, a não ser que dê erro. Tarefa que espera o dono (n8n, decisão) continua travada por esta conversa, atribuída a ele, e a conversa trava a próxima da trilha e segue; no máximo duas travadas. Trilha acabou: diz ao dono e vai para `Finalizada`.

**A fila do dono:** tudo que depende dele, de todas as conversas, fica atribuído a ele no Linear com `Sua vez: <a coisa>`. Ele vê em **My issues** do Linear. Diga isso a ele uma vez, quando montar o ciclo. **Enquanto houver algo esperando o dono, a conversa fica no grupo `Sua vez`**, mesmo com outra tarefa andando: é o que ele olha.

**Formatos fixos** (sempre iguais, para ele reconhecer de relance):

Quando ele pergunta como está o ciclo:
```
Ciclo <n>: <x> de <y> prontas.
  <Trilha>: fazendo <tarefa>. Depois: <próxima>.
  <Trilha>: esperando você (<a coisa>).
Com você: <lista curta das atribuídas a ele, ou "nada">
```

Comentário **Onde parei**, na tarefa, a cada pausa ou troca de conversa (é o que ele lê dias depois para continuar):
```
Pronto: <o que já funciona, em uma linha>
Falta: <o que falta>
Próximo passo: <a primeira coisa a fazer ao voltar>
— <título desta conversa> · <marca>
```

Achado no caminho que não impede o combinado: uma linha `Vi e não mexi`, nunca uma pergunta ao dono (protocolo de comunicação, seção 0).

## 7. Recuperação

Um agente parou no meio, ou a sessão caiu:
1. **O que ainda está vivo?** Liste antes de relançar. Relançar em cima de um agente vivo corrompe os dois.
2. **O agente "morto" pode ter terminado:** confira commits e relatórios.
3. Cópia limpa: relance as mesmas instruções. Cópia com trabalho pela metade: o novo agente começa classificando o que está feito, parcial ou intocado.
4. Agentes morrendo na hora, sem fazer nada: provável problema do serviço. Espere (10, depois 30 minutos) e teste com um agente só antes de relançar todos.

## 8. Modelos

Todos os agentes usam o mesmo modelo da conversa (`inherit`), por enquanto. Se o custo ou o limite de uso apertar, o candidato a modelo mais barato é o trabalho repetitivo (Docs, Testes passo 3); decisão, desenho, revisão e segurança ficam no mais forte. Mudança de modelo é decisão do dono.

## 9. Lições

Ao fechar um projeto ou conserto:
- Fato do projeto que o dono precisou repetir (empresa de teste, quem é quem, um jeito de fazer): uma linha no `CLAUDE.md` do projeto, no PR da tarefa.
- Regra que faltou num guia ou num agente (algo que custou caro e vai se repetir): **proponha** ao dono a mudança no arquivo da empresa, com o caso que a motivou. Não altere guias, protocolos ou agentes da empresa sem o ok dele.
