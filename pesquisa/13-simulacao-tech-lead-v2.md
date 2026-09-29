# Simulação: Tech Lead (Naruto), instruções v2, módulo follow-up

Convenções da simulação: `[N]`, `[hora]`, `[função antiga 1]` etc. são números e nomes reais que o Tech Lead teria em mãos e que o roteiro não fornece. Nada foi executado.

---

## 1. Dono: "Amigão, quero fazer um overclock do follow-up. Olha os problemas de UX e as falhas de desenvolvimento da tela."

**Bastidores:** Classifico como **auditoria** (1.4), apesar da palavra "overclock": ele pede para achar problemas, não pesquisa de mercado. Rodada de arquitetura: o follow-up tem quatro camadas (tela, banco, motor novo, fluxo antigo no n8n); confiro branches e PRs abertos que tocam o módulo (nenhum, na simulação). Nada a pedir ao dono agora. Lanço em paralelo, uma frente só: Designer modo 2 (tela do follow-up), Revisor lendo o código da tela, Revisor lendo o banco do follow-up, Security modo 3 na área do follow-up. Registro no andamento.

**Mensagem ao dono:**

```
O que mudou: Entendi o pedido e o time já está olhando o follow-up. Missão aceita, dattebayo!

O que você pediu: um pente-fino no follow-up: onde a tela confunde quem usa e onde ela falha.

Problemas/objetivos que você trouxe:
  1. Problemas de uso da tela → levantados pela designer
  2. Falhas de funcionamento (a tela e o que fica guardado por trás dela) → levantadas por dois revisores de código
O que eu decidi sozinho:
  - Nesta etapa só levantamos. Ninguém mexe em nada ainda.
  - Incluí uma checagem de segurança do follow-up, que roda junto sem custo extra.
  - Tratei como pente-fino, não como pesquisa de mercado. Se você queria também ver o que os concorrentes fazem, é só pedir.

Caminho:
  1. Levantamento (agora)
  2. Propostas organizadas: o que resolver, para quem, quanto esforço
  3. Você escolhe o que entra, numa conversa só
  4. O escolhido vira projeto: documento para você aprovar, construção, revisão
  5. Roteiro passo a passo para você colocar no ar

Onde estamos:
  ✅ pronto: nada ainda
  🔄 andando: levantamento do follow-up
  ⏸️ parado ou na fila: nada

Sua vez: nada agora, pode cuidar de outra coisa.
```

**Mesa e fila:** Mesa: nada. Fila: nada.

---

## 2. Chegam 3 relatórios (designer, revisor da tela, revisor do banco): ~40 problemas

**Bastidores:** Confiro cada relatório contra o código (amostra dos graves: salvar com erro fechando a janela, follow-up nascendo ligado, exclusão levando junto o histórico de envios). Decido cada achado (aceito / recusado com motivo / do dono) e monto o backlog do projeto. Espero o Security para lançar o PO uma vez só, com tudo. Agente terminou não é motivo para falar com o dono.

**Mensagem ao dono:** (nenhuma mensagem)

**Mesa e fila:** Mesa: nada. Fila: nada.

---

## 3. Relatório do Security: duas funções antigas, abertas sem login, deixam qualquer um encerrar o follow-up de todas as empresas

**Bastidores:** Antes de alarmar, peço uma segunda opinião rápida (outro Security confere no sistema real se as funções estão publicadas e abertas) e um Pesquisador confirma que nada usa essas funções (tela, motor, fluxo do n8n). Confirmado. Trato como emergência (exceção da mesa). Mando o aviso de notificação e a mensagem. Lanço o PO modo 3 com os quatro relatórios (a emergência fica fora das propostas). A retirada do código das funções no repositório fica na fila, para depois da remoção.

**Mensagem ao dono:**

Aviso (notificação):
```
URGENTE: duas funções antigas deixam qualquer pessoa desligar o follow-up de todas as empresas. Remover leva 5 min. Passo a passo no Claude.
```

Conversa:
```
O que mudou: Achamos uma falha de segurança séria no follow-up. Existem duas funções antigas no servidor, que ninguém usa mais, abertas na internet sem pedir login. Qualquer pessoa que descubra o endereço delas consegue desligar o follow-up de todas as empresas de uma vez. Nos últimos 14 dias ninguém chamou essas funções, então não há sinal de uso. Elas não mostram dados de clientes; o risco é parar os envios de todo mundo. Um segundo olhar confirmou o furo e confirmou que nada no sistema depende delas.

Onde estamos:
  ✅ pronto: levantamento de uso e de funcionamento (cerca de 40 problemas)
  🔄 andando: propostas sendo organizadas a partir do levantamento
  ⏸️ parado ou na fila: tirar o código dessas funções do sistema (depois que você remover)

Sua vez: remover as duas funções (cerca de 5 minutos)
  1. Entre em supabase.com e abra o projeto do CRM.
  2. No menu da esquerda, clique em "Edge Functions".
  3. Clique em [função antiga 1]. Na página dela, procure "Delete function" (fica no fim das configurações) e confirme digitando o nome.
  4. Repita com [função antiga 2].
  Deu certo quando: as duas não aparecem mais na lista de "Edge Functions".
  Para voltar atrás: o código delas continua guardado; se algo precisar, colocamos de volta.
  Me avise quando terminar, que eu confiro se o follow-up segue funcionando.
```

**Mesa e fila:** Mesa: remover as duas funções (emergência). Fila: escolher as propostas (quando o PO entregar); juntar a retirada do código das funções (virá num PR).

---

## 4. Dono (sem responder o item 3): "Li por cima. O editor é muito ruim, queria focar só na parte da tela."

**Bastidores:** Registro a diretiva: foco na tela, editor primeiro; o motor sai do foco mas não some. Mando ao PO (que está rodando) a ordem de prioridade: editor, depois defeitos da tela, e o motor como pacote separado "para depois". A pergunta da emergência não se repete: só uma linha no "Sua vez". Não pergunto "tô certo?" sobre o editor: ele concorda com o levantamento, não estranha algo que entregamos, e a escolha fina vem nas propostas.

**Mensagem ao dono:**

```
O que mudou: Anotado: foco na tela, com o editor em primeiro lugar. Pedi que as propostas venham nessa ordem; o que é só do motor de envios fica listado à parte, para depois. Editor confuso tem os dias contados, tô certo, tô certo!
  Fala (designer): "O editor pede cinco cliques para uma coisa de um."
  Fala (revisor da tela): "Quando salvar dá erro, a janela fecha como se tivesse dado certo."
  Fala (revisor do banco): "Excluir um follow-up leva junto o histórico de envios."
  Fala (Security): "Duas portas antigas abertas; o resto está trancado."

Onde estamos:
  ✅ pronto: levantamento (cerca de 40 problemas)
  🔄 andando: propostas, com o editor primeiro
  ⏸️ parado ou na fila: motor de envios (5 defeitos que não afetam ninguém hoje, mas travam liberar a próxima empresa), para depois, por decisão sua; tirar o código das funções antigas do sistema

Sua vez: remover as duas funções antigas (passo a passo na mensagem anterior). Não é da tela, mas é o único item urgente.
```

**Mesa e fila:** Mesa: remover as duas funções. Fila: escolher as propostas; juntar a retirada do código das funções.

---

## 5. O PO entrega as propostas

**Bastidores:** Confiro as propostas contra o backlog: todo achado aceito está em alguma proposta ou em "fica de fora" com motivo. Três pacotes: editor novo; defeitos da tela; motor (para depois). A mesa está ocupada pela emergência, então a escolha das propostas entra na fila. Falo com ele porque é o resultado que ele está esperando, mas sem abrir a decisão.

**Mensagem ao dono:**

```
O que mudou: As propostas estão prontas, em três pacotes:
  1. Editor novo: montar a sequência de mensagens num lugar só, e acabar com o erro que fecha a janela como se tivesse salvado.
  2. Defeitos da tela: follow-up novo que nasce ligado sem número de WhatsApp, excluir que leva o histórico, e cerca de 15 ajustes menores.
  3. Motor de envios: os 5 defeitos que travam liberar a próxima empresa (para depois, como você pediu).
  A escolha é a próxima coisa da sua mesa, logo depois da remoção das funções.
  Fala (PO): "Três pacotes, cada um cabe numa decisão."

Onde estamos:
  ✅ pronto: levantamento; propostas
  🔄 andando: nada; esperando você
  ⏸️ parado ou na fila: escolher as propostas; motor de envios (para depois); tirar o código das funções antigas do sistema

Sua vez: remover as duas funções antigas (passo a passo duas mensagens acima).
```

**Mesa e fila:** Mesa: remover as duas funções. Fila: escolher as propostas; juntar a retirada do código das funções.

---

## 6. Dono aprova editor novo e defeitos da tela; motor depois. Pergunta: "dá pra ter variáveis tipo {primeiro_nome} no follow-up?"

**Bastidores:** Aceito a escolha dele mesmo tendo vindo da fila (ele resolveu, o item sai da fila). Registro: entram os pacotes 1 e 2 como um projeto; o pacote 3 fica parado. Lanço o PO modo 1 (documento de projeto) e, em paralelo, um Pesquisador tipo "sistema atual": "o follow-up aceita variáveis de contato nas mensagens, no motor novo e no fluxo antigo?". A pergunta dele é pedido de informação: respondo quando souber.

**Mensagem ao dono:**

```
O que mudou: Fechado: entram o editor novo e os defeitos da tela; o motor fica para depois. O documento do projeto já está sendo escrito e vem para você aprovar antes de qualquer construção. Bora, dattebayo!
Sobre variáveis tipo {primeiro_nome}: ainda não sei se o follow-up de hoje consegue. Pedi para conferirem e te respondo assim que souber.

Onde estamos:
  ✅ pronto: levantamento; propostas escolhidas
  🔄 andando: documento do projeto (editor novo + defeitos da tela); resposta sobre variáveis
  ⏸️ parado ou na fila: motor de envios (para depois); tirar o código das funções antigas do sistema

Sua vez: remover as duas funções antigas (passo a passo na minha mensagem do alerta).
```

**Mesa e fila:** Mesa: remover as duas funções. Fila: aprovar o documento do projeto (quando pronto); juntar a retirada do código das funções.

---

## 7. Dono: "removi as duas funções antigas, confere se nada quebrou."

**Bastidores:** Confiro no sistema real, só lendo: as duas funções não estão mais na lista publicada; registros do follow-up desde a remoção sem erro novo; envios automáticos rodando no ritmo dos dias anteriores; a tela abre. Lanço o conserto pontual de limpeza (Implementador tira o código das funções do repositório, para nenhuma publicação futura trazê-las de volta; depois Revisor), que termina em PR. Segunda frente: projeto + limpeza.

**Mensagem ao dono:**

```
O que mudou: Conferido: as duas funções sumiram do servidor e nada quebrou. Desde a remoção, saíram [N] mensagens automáticas, no ritmo dos dias anteriores, e a tela abre sem erro. O furo está fechado. Missão cumprida, dattebayo!
Também vou tirar o código delas do sistema, para ninguém colocar de volta sem querer. Isso vira uma revisão para você juntar junto com o resto, no fim.

Onde estamos:
  ✅ pronto: furo de segurança fechado; propostas escolhidas
  🔄 andando: documento do projeto (editor novo + defeitos da tela); limpeza do código das funções antigas
  ⏸️ parado ou na fila: resposta sobre variáveis (sendo conferida); motor de envios (para depois)

Sua vez: nada agora, pode cuidar de outra coisa.
```

**Mesa e fila:** Mesa: nada. Fila: aprovar o documento do projeto (quando pronto); juntar as revisões (no fim, em lote).

*(Entre 7 e 8, fora do roteiro: o PO entregou o documento, o construtor de teste leu, o dono aprovou o documento e depois os esboços do designer; Arquiteto, Security e linha de base feitos; construção começou pelas fatias 1 e 2.)*

---

## 8. Implementador: "excluir" apaga o histórico e o documento não decidiu; Pesquisador: variáveis só no motor novo

**Bastidores:** Falha de planejamento minha: o achado estava no levantamento e o documento não trouxe a decisão. Pauso só a parte "excluir" da fatia 1 (o resto segue). Passo a decisão pelo portão: arquivar é a opção mais segura e dá para voltar atrás (excluir de verdade pode ser acrescentado depois), então decido arquivar, registro em `docs/suposicoes.md` e mando o PO atualizar o documento (modo 2) e o Arquiteto definir a migration (numerada por mim). Como isso muda o documento aprovado, conto ao dono ("mudei X porque Y"). A resposta das variáveis é o que ele esperava: falo agora. Variáveis vão para o pacote do motor, sem abrir frente.

**Mensagem ao dono:**

```
O que mudou:
  - Variáveis tipo {primeiro_nome}: dá, mas só no motor de envios novo. O fluxo que envia as mensagens hoje não aceita. Como o motor ficou para depois, anotei as variáveis junto com ele: quando o motor entrar, elas podem entrar também.
  - Mudei uma coisa no documento aprovado: o botão "Excluir" vai virar "Arquivar". Hoje, excluir um follow-up apaga também todo o histórico de mensagens que ele já mandou, sem volta. Arquivar tira o follow-up da lista e guarda o histórico. Se um dia você quiser apagar de verdade, dá para acrescentar depois. Essa decisão devia ter aparecido no documento; falha minha no planejamento. Se preferir que continue apagando tudo, me fala.
  Fala (pesquisador): "Variável tem casa no motor novo, no antigo não."
  Não desisto de uma missão, e essa tá andando firme!

Onde estamos:
  ✅ pronto: furo de segurança fechado; documento e esboços aprovados
  🔄 andando: construção do projeto (defeitos da tela e editor novo); limpeza do código das funções antigas
  ⏸️ parado ou na fila: motor de envios + variáveis (para depois); ver e restaurar follow-ups arquivados (fora deste projeto)

Sua vez: nada agora, pode cuidar de outra coisa.
```

**Mesa e fila:** Mesa: nada. Fila: juntar e colocar no ar (lote, no fim).

---

## 9. Fatia 1 (defeitos da tela) pronta e conferida, com PR aberto

**Bastidores:** Confiro relatório contra a mudança, rodo tipos e testes da fatia; Security, Testes, Revisor e Docs passaram. PR do projeto aberto como rascunho. Fatia concluída não se avisa.

**Mensagem ao dono:** (nenhuma mensagem)

**Mesa e fila:** Mesa: nada. Fila: juntar e colocar no ar (lote, no fim).

---

## 10. Dono: "o que são aquelas bolinhas laranja embaixo de 'Enviar depois de' no esboço? achei estranho."

**Bastidores:** Fato antes de responder: leio o `telas.md` do projeto e o esboço (na simulação: é um marcador de passos da sequência). Ele estranhou algo: regra de conferir o que entendi antes de mandar mudar. Aviso o Implementador da fatia 2 para deixar esse elemento por último; o resto segue.

**Mensagem ao dono:**

```
São um marcador de passos: cada bolinha é uma mensagem da sequência do follow-up, e a laranja mostra qual você está editando (por exemplo, a 2ª de 4). Ficaram logo abaixo de "Enviar depois de", por isso parecem fazer parte desse campo.

Se entendi bem, o que te incomodou é que elas parecem ligadas ao "Enviar depois de" e não dizem o que significam. Tô certo? Se for isso, recomendo trocar por um texto simples no topo ("Mensagem 2 de 4"). O editor ainda está sendo construído, então ajustar agora não atrasa nada.

Onde estamos:
  ✅ pronto: defeitos da tela corrigidos e conferidos (inclui o Arquivar)
  🔄 andando: editor novo; limpeza do código das funções antigas
  ⏸️ parado ou na fila: motor de envios + variáveis (para depois); ver e restaurar arquivados (fora deste projeto)

Sua vez: me dizer se entendi certo o incômodo das bolinhas.
```

**Mesa e fila:** Mesa: confirmar o incômodo das bolinhas. Fila: juntar e colocar no ar (lote, no fim).

---

## 11. Fatia 2 (editor) pronta, PR aberto; migration de arquivar pronta (0 linhas hoje); duas funções novas a publicar depois de juntar

**Bastidores:** Confiro a fatia 2 e a verificação final do projeto; PR do projeto passa a pronto; PR da limpeza também pronto. O lote está completo, mas a mesa tem a dúvida das bolinhas, e a resposta pode mudar o editor: o roteiro fica na fila. Ordem do roteiro: 1) mudança no banco (com "pode"), 2) juntar, 3) publicar as duas funções, 4) testar. Falo porque o que ele espera ficou pronto, e deixo claro que a ordem importa.

**Mensagem ao dono:**

```
O que mudou: O follow-up novo está pronto e conferido: editor novo, defeitos da tela corrigidos e "Arquivar" no lugar de "Excluir". Testes, segurança e revisão passaram. Para colocar no ar são 4 passos, em ordem. Te mando o roteiro assim que a dúvida das bolinhas estiver resolvida, porque a resposta pode mudar o editor.
Importante: não junte as revisões ainda. Se o site novo entrar antes da mudança no banco, a tela de follow-up quebra.
  Fala (implementador): "Editor novo de pé, cada passo num lugar só."

Onde estamos:
  ✅ pronto: defeitos da tela; editor novo; limpeza do código das funções antigas
  🔄 andando: nada; esperando você
  ⏸️ parado ou na fila: roteiro para colocar no ar (4 passos); motor de envios + variáveis (para depois); ver e restaurar arquivados (fora deste projeto)

Sua vez: me dizer se entendi certo o incômodo das bolinhas (mensagem anterior).
```

**Mesa e fila:** Mesa: confirmar o incômodo das bolinhas. Fila: roteiro de colocar no ar (mudança no banco → juntar → publicar funções → testar).

---

## 12. Dono: "juntei os PRs."

**Bastidores:** Ele juntou antes da mudança no banco e das funções. Confiro no sistema real, só lendo: o site novo entrou no ar às [hora]; a lista de follow-ups dá erro (falta a marcação de arquivado no banco); salvar no editor falha (funções novas não publicadas); envios automáticos seguem normais. É produto quebrado para os clientes: mensagem direta, sem voz. Conto as linhas em produção agora, só lendo, e apresento a mudança no banco antes de pedir o "pode". A dúvida das bolinhas vai para a fila (o editor já está no ar como no esboço aprovado).

**Mensagem ao dono:**

```
O que mudou: O site novo entrou no ar antes da mudança no banco, e a tela de follow-up quebrou. Desde [hora], a lista de follow-ups não carrega para nenhuma empresa, e salvar no editor novo dá erro. Os envios automáticos não foram afetados: saíram [N] mensagens desde então, normalmente.

A saída mais rápida é completar os passos que faltam. O primeiro é a mudança no banco:
  - O que faz: acrescenta a marcação de "arquivado" aos follow-ups, que a tela nova precisa para montar a lista. Não altera nem apaga nada.
  - Quantos follow-ups mexe: 0 alterados. Os [N] que existem hoje (contei agora, só lendo) ficam todos como "não arquivado".
  - Como vou conferir: a lista volta a carregar, com os mesmos [N] follow-ups.
  - Como voltar atrás: remover essa marcação. Como nenhum dado muda, não há cópia a guardar.
Depois vem publicar as duas funções novas (passo seu, te mando o passo a passo), e o salvar volta.

A alternativa é voltar o site para a versão anterior agora e refazer tudo na ordem certa. Recomendo seguir em frente: são dois passos curtos e a mudança no banco não mexe em dados.

Onde estamos:
  ✅ pronto: revisões juntadas e no ar
  🔄 andando: consertar a tela de follow-up (lista e salvar com erro)
  ⏸️ parado ou na fila: publicar as funções novas; testar no ar; dúvida das bolinhas; motor de envios + variáveis (para depois); ver e restaurar arquivados (fora deste projeto)

Sua vez: dizer "pode" para eu aplicar a mudança no banco (acrescentar a marcação de arquivado).
```

**Mesa e fila:** Mesa: "pode" para a mudança no banco. Fila: publicar as duas funções; testar no ar; dúvida das bolinhas.

---

## 13. Dono: "pode aplicar a migration."

**Bastidores:** Registro o "pode" (qual migration, hora, [N] follow-ups, 0 alterados). Confiro de novo em produção, só lendo: a marcação ainda não existe e o número bate. Aplico nesta conversa com `apply_migration`, com o conteúdo do arquivo do repositório; a trava pede a confirmação do dono na tela. Depois: migration na lista de aplicadas, [N] antes e depois, verificadores do Supabase sem alerta novo, lista de follow-ups carregando. Peço ao Implementador para gerar os tipos de novo (se mudarem, vira PR). Mando o próximo passo do roteiro. Anoto a lição (ordem de publicação) para propor no fechamento.

**Mensagem ao dono:**

```
O que mudou: Mudança no banco aplicada e conferida. A lista de follow-ups voltou a carregar para todas as empresas: os [N] follow-ups estão lá, nenhum alterado, e nenhum alerta novo de segurança. Para voltar atrás, basta remover a marcação de arquivado. Falta o salvar do editor novo, que depende das duas funções novas.

Onde estamos:
  ✅ pronto: revisões no ar; mudança no banco; lista de follow-ups de volta
  🔄 andando: salvar do editor (esperando as funções novas)
  ⏸️ parado ou na fila: testar no ar; dúvida das bolinhas; motor de envios + variáveis (para depois); ver e restaurar arquivados (fora deste projeto)

Sua vez: publicar as duas funções novas.
  Antes: terminal aberto na pasta do projeto do CRM.
  1. Rode: git pull
     Deu certo se: aparece a lista de arquivos atualizados (ou "Already up to date").
  2. Rode: npx supabase functions deploy [função nova 1]
     Deu certo se: termina com "Deployed Function".
  3. Rode: npx supabase functions deploy [função nova 2]
     Mesmo sinal.
  Se pedir login, rode "npx supabase login" e siga a tela. Se aparecer qualquer outra pergunta, pare e me mande o que apareceu.
  Me avise quando terminar, que eu confiro se o salvar voltou.
```

**Mesa e fila:** Mesa: publicar as duas funções novas. Fila: testar no ar (último passo do roteiro); dúvida das bolinhas; proposta de lição (ordem de publicação).

---

## Autoavaliação

1. **Overclock ou auditoria?** `tech-lead.md:43-45` e `tech-lead-referencia.md:48-63`. O dono disse "overclock" mas pediu problemas; classifiquei como auditoria. E a auditoria (§1.4, linhas 49-52) não tem agente para "falhas de desenvolvimento": usei o Revisor, cuja descrição é "último portão depois de Security e Testes".
2. **A exceção da emergência ocupa a mesa ou fura a fila?** `tech-lead.md:89` ("Exceção: emergência de segurança") não diz se a emergência conta como a única coisa aberta. Somado ao "Sua vez: UMA coisa" (`tech-lead.md:102`), deixei a escolha das propostas presa na fila atrás da emergência (evento 5). A outra leitura deixaria duas coisas abertas.
3. **Decisão nova no meio da construção: perguntar ou resolver?** `tech-lead.md:59-63` manda levar ao dono "tudo de uma vez"; `tech-lead.md:109` e `comunicacao.md:18` (portão: reversível → escolha a mais segura e registre) mandam resolver. Em "excluir → arquivar" segui o portão e só avisei ("mudei X porque Y", `tech-lead.md:82`). As regras não dizem qual das duas vence.
4. **Falas demais.** `tech-lead.md:116` ("uma `Fala:` por agente") colide com `tech-lead.md:95` ("O que mudou: 1 a 3 linhas") e `comunicacao.md:81` ("a voz é uma frase"). No evento 4, quatro agentes dariam quatro falas mais a do Naruto.
5. **Voz enquanto a emergência está na mesa.** `tech-lead.md:118` / `comunicacao.md:83` proíbem voz "em emergência de segurança". Não fica claro se isso vale só para o alerta ou para toda mensagem enquanto ela está aberta (eventos 4-6). Usei voz no "O que mudou" e deixei o "Sua vez" seco.
6. **A lista fechada de avisos não cobre o caso.** `avisos.md:14-17`: "desligar o follow-up de todos" não é "segredo exposto" nem "dados acessíveis". Pela letra, não se avisaria. Avisei com base em `tech-lead.md:138` ("Emergência de segurança (Security avisa)").
7. **"Tô certo?" sem resposta trava o lote.** `tech-lead.md:110` (conferir antes de mandar mudar) com `tech-lead.md:89` (uma coisa por vez) deixaram uma dúvida visual barata segurando o roteiro de colocar no ar (eventos 10-11). O portão (`comunicacao.md:18`) diria para não perguntar, e `comunicacao.md:59` cobre "não sei", não o silêncio. Nada diz o que fazer quando o dono não responde.
8. **Nada protege a ordem de publicação.** `tech-lead.md:107` segura o roteiro "até tudo pronto", mas os PRs ficam visíveis e o dono juntou antes (evento 12), quebrando a tela. Faltam duas coisas: exigir que o desenho aguente qualquer ordem de publicação, ou pelo menos que a descrição do PR diga "não juntar antes do passo X". `tech-lead-referencia.md:104` fala de "o que fazer antes de publicar", mas não da ordem.
9. **Decisão de produto do achado não conferida no documento.** `tech-lead.md:80` / `tech-lead-referencia.md:55` pedem que o PO junte as decisões de cada proposta. Nenhum passo manda o Tech Lead conferir que cada achado aceito que pede decisão chegou ao documento. Foi assim que "excluir" escapou (evento 8).
10. **O que é "frente".** `tech-lead.md:70-71`: responder a uma pergunta do dono (pesquisa das variáveis) e a limpeza depois da emergência contam como frente? Se a limpeza conta, abri-la exigiria perguntar ao dono. Decidi que não contam, sem base no texto.
11. **Dois modelos de mensagem para juntar.** O espelho (`comunicacao.md:32-45`, chamado em `tech-lead.md:51`) e o formato da mesa (`tech-lead.md:92-104`). Não se diz como combinar os dois, nem se o espelho vale quando não há pergunta (o título em `comunicacao.md:32` é "antes de perguntar").
12. **Tamanho do "passo" no roteiro.** `tech-lead.md:107` diz "um passo por vez". Publicar duas funções (pull + dois comandos) é um passo ou três? Agrupei em um.
13. **Um PR ou vários?** `tech-lead-referencia.md:103` fala num PR por projeto (rascunho, depois pronto). O roteiro trazia PR por fatia. Usei um do projeto mais o da limpeza.
