# Simulação Tech Lead (Naruto), v2, rodada 2

SIMULAÇÃO. Nada foi executado: nenhum agente lançado, nenhum acesso ao CRM, ao banco ou ao n8n. Nomes de funções, campos e caminhos abaixo são ilustrativos.

Arquivos lidos inteiros: `empresa-agentes-v2/agentes/tech-lead.md`, `protocolos/tech-lead-referencia.md`, `protocolos/comunicacao.md`, `protocolos/avisos.md`.

Convenção de contagem: "mensagem na conversa" é o texto no chat, no formato da mesa. "Aviso" é a notificação de uma linha de `avisos.md`, que o canal só mostra se o dono não estiver olhando para a tela.

---

## 1. Security entrega: duas funções antigas sem login deixam qualquer um parar o follow-up de todas as empresas

**Bastidores**
- É o caso grave de `avisos.md:15` ("alguém de fora parar... o serviço de todos os clientes"). Antes de alarmar, peço uma segunda opinião rápida (ref. §5.1): um Pesquisador confere, só lendo, se as funções estão publicadas, se atendem sem login e se alguma tela ou workflow do n8n chama as duas. Resultado: confirmado, e nada usa as funções. Então removê-las não desliga nada que funciona.
- Peço ao Security que leia os registros (só leitura) para ver se alguém já chamou as funções. A auditoria não muda nada, então não há o que parar. Registro no andamento.

**Mensagem ao dono** (1 aviso + 1 mensagem na conversa, sem voz)

Aviso:
`URGENTE: duas funções antigas deixam qualquer pessoa na internet parar o follow-up de todas as empresas. Remover no painel do Supabase. Passo a passo no Claude.`

Conversa:
```
O que mudou: a auditoria achou um furo grave. Duas funções antigas do servidor atendem qualquer pessoa na internet, sem pedir login, e com elas alguém de fora consegue parar o follow-up de todas as empresas de uma vez. Conferi com um segundo olhar: é verdade, e nada no sistema usa essas funções hoje. Removê-las não desliga nada que funciona. Estou vendo se alguém já as usou e te conto se sim.

Onde estamos:
  ✅ pronto: verificação de segurança do follow-up
  🔄 andando: auditoria do follow-up (telas, código e banco)
  ⏸️ parado ou na fila: depois que você remover, tiro o código dessas funções do sistema, para elas não voltarem numa publicação futura

🚨 Urgente: remover as duas funções antigas.
  1. Entre em supabase.com, abra o projeto do CRM e clique em "Edge Functions", no menu da esquerda.
  2. Clique em "followup-stop-all", depois nos três pontinhos, em "Delete function", e confirme.
  3. Faça o mesmo com "followup-pause-legacy".
  4. Deu certo quando nenhuma das duas aparece mais na lista. Me escreva "removi" e eu confiro daqui.

Sua vez: nada além do urgente acima.
```

**Mesa, fila e urgente**
- Mesa: nada.
- Fila: nada.
- Urgente: remover as duas funções antigas.
- Prometido: tirar o código delas do sistema depois da remoção. Contar ao dono se alguém já usou as funções.

---

## 2. Chegam os relatórios da auditoria (~40 problemas)

**Bastidores**
- Confiro os relatórios contra o sistema real por amostragem (ref. §5.1) e dou destino a cada achado: aceito no backlog, recusado com motivo ou do dono. "Excluir apaga todo o histórico" e "nasce ligado sem número" pedem decisão de produto (arquivar ou apagar? nasce desligado?), então não são conserto pontual (`tech-lead.md:44`, ref. §1.4 exceção). Vão para o PO.
- Lanço o PO no modo 3: propostas agrupadas por mecanismo, com as decisões de produto de cada uma. Agente terminou não é motivo para falar com o dono (`tech-lead.md:75`). A leitura dos registros pelo Security não achou uso das funções, então não há notícia a dar.

**Mensagem ao dono:** (nenhuma mensagem)

**Mesa, fila e urgente**
- Mesa: nada.
- Fila: nada (propostas em preparo).
- Urgente: remover as duas funções antigas.

---

## 3. O PO entrega as propostas; o dono ainda não removeu as funções

**Bastidores**
- Confiro as propostas: cobrem os ~40 achados, cada uma com esforço, o que fica de fora e as decisões que pede. A auditoria termina aqui, com uma escolha para o dono, que é a coisa que ele esperava. Vai uma decisão para a mesa: quais propostas entram, numa conversa só (ref. §1.4 passo 2).
- Não repito o urgente como mensagem. Ele entra como uma linha (`tech-lead.md:92`, `avisos.md:25`).

**Mensagem ao dono** (1 aviso + 1 mensagem na conversa)

Aviso:
`Decisão sua trava o follow-up: quais melhorias da auditoria entram. Recomendo editor novo + defeitos da tela. Detalhes no Claude.`

Conversa:
```
O que mudou: a auditoria do follow-up terminou, com uns 40 problemas. Os que mais pesam para o cliente: o editor confunde quem monta a sequência de mensagens; excluir um follow-up apaga todo o histórico do que já foi enviado; e um follow-up novo já nasce ligado antes de ter um número de WhatsApp. Missão de reconhecimento cumprida, dattebayo!
  Fala (PO): "Três caminhos, uma escolha: comece pelo que o cliente sente todo dia."

Onde estamos:
  ✅ pronto: auditoria do follow-up (40 problemas listados, nenhum descartado)
  🔄 andando: nada, esperando sua escolha
  ⏸️ parado ou na fila: tirar o código das funções antigas (depois que você remover)

🚨 Urgente: remover as duas funções antigas (passo a passo mais acima, na conversa).

Sua vez: escolher o que entra. São três propostas:
  A) Editor novo: refaz a tela de montar a sequência para ficar clara. Resolve a confusão, que é a maior queixa. Esforço médio.
  B) Defeitos da tela: conserta os problemas da tela de follow-up, entre eles o histórico apagado ao excluir e o follow-up que nasce ligado sem número. Esforço pequeno.
  C) Motor de envio: reforma o que dispara as mensagens por trás. Hoje não quebra nada para o cliente. Esforço grande.
  Recomendo A e B juntos, num projeto só: mexem na mesma tela, e fazer B sozinho seria consertar uma tela que o A vai refazer. C fica guardada para depois. As regras de cada conserto (por exemplo, o que fazer com o histórico ao excluir) vêm todas juntas no documento do projeto, para você aprovar. Se você não souber, sigo com A e B.
```

**Mesa, fila e urgente**
- Mesa: escolher as propostas.
- Fila: nada.
- Urgente: remover as duas funções antigas.

---

## 4. O dono escolhe editor novo + defeitos da tela; ainda não removeu

**Bastidores**
- Abre um projeto, que é uma frente só. A auditoria fecha, então continuo dentro do limite de duas. Crio `projeto/followup-editor` e o andamento, e lanço o PO no modo 1. Depois vem o construtor de teste.
- Anoto no andamento: motor de envio para depois; os demais achados continuam guardados no backlog.

**Mensagem ao dono** (1 mensagem na conversa)
```
O que mudou: fechado, editor novo e defeitos da tela num projeto só. O motor de envio fica guardado para depois. Essa missão eu não largo, dattebayo!
  O que você pediu: um follow-up fácil de montar e sem as armadilhas da tela atual.
    1. editor confuso → editor novo
    2. excluir apaga o histórico de envios → a regra vai no documento, com minha recomendação
    3. follow-up novo nasce ligado sem número → a regra vai no documento, com minha recomendação
    4. os outros defeitos da tela → consertados no projeto
  Caminho: documento do projeto (você aprova) → esboço das telas (você aprova) → construção → segurança, testes e revisão → roteiro para você colocar no ar.

Onde estamos:
  ✅ pronto: auditoria do follow-up; sua escolha
  🔄 andando: projeto editor novo + defeitos da tela (escrevendo o documento)
  ⏸️ parado ou na fila: motor de envio (para depois); demais problemas da auditoria (guardados); tirar o código das funções antigas (depois que você remover)

🚨 Urgente: remover as duas funções antigas (passo a passo mais acima, na conversa).

Sua vez: nada na mesa além do urgente. A próxima parada é o documento para você aprovar.
```

**Mesa, fila e urgente**
- Mesa: nada.
- Fila: nada.
- Urgente: remover as duas funções antigas.

---

## 5. O documento do projeto fica pronto para aprovar

**Bastidores**
- O construtor de teste rodou até não sobrar achado de regra. Confiro `tech-lead.md:65`: todo achado aceito que pede decisão está decidido no documento. As duas regras vão como decisões com recomendação, não como perguntas soltas, para caber numa aprovação só.
- Nada é construído antes do "aprovado" (`tech-lead.md:57`). O designer só começa os esboços depois dele.

**Mensagem ao dono** (1 aviso + 1 mensagem na conversa)

Aviso:
`Documento do projeto do follow-up pronto para você aprovar. A construção só começa depois disso. Detalhes no Claude.`

Conversa:
```
O que mudou: o documento do projeto está pronto. Ele conta, em linguagem simples, como o follow-up vai funcionar depois do projeto e o que fica de fora. Traz duas regras novas que precisam do seu olho:
  - Excluir um follow-up passa a arquivar: ele some da lista, mas o histórico do que já foi enviado fica guardado.
  - Follow-up novo nasce desligado e só pode ser ligado depois de ter um número de WhatsApp.
  Fala (PO): "Cada regra tem um porquê escrito; se um porquê não te convencer, a regra muda."

Onde estamos:
  ✅ pronto: auditoria; sua escolha; documento do projeto
  🔄 andando: projeto editor novo + defeitos da tela (esperando sua aprovação)
  ⏸️ parado ou na fila: motor de envio (para depois); demais problemas da auditoria (guardados); tirar o código das funções antigas (depois que você remover)

🚨 Urgente: remover as duas funções antigas (passo a passo mais acima, na conversa).

Sua vez: aprovar o documento. Está em docs/projetos/followup-editor/projeto.md (partes 1 a 4, umas três páginas). Recomendo aprovar com as duas regras acima. Se concordar, responda "aprovado"; se quiser mudar algo, me diga o quê.
```

**Mesa, fila e urgente**
- Mesa: aprovar o documento.
- Fila: nada. Os esboços ainda não existem, então não entram na fila.
- Urgente: remover as duas funções antigas.

---

## 6. Na construção: falta a regra "envios agendados quando o follow-up é desligado" (hoje continuam saindo)

**Premissa:** "já na construção" implica que, entre 5 e 6, o dono aprovou o documento e depois os esboços (ref. §1.3 passo 4). O item 7 confirma que ele viu um esboço.

**Bastidores**
- Confiro no sistema real, só lendo (`tech-lead.md:141`): desligado, o follow-up continua mandando o que já estava agendado. Pauso só a fatia de ligar, desligar e arquivar; o resto segue (`tech-lead.md:60`).
- Junto as decisões do mesmo mecanismo (`tech-lead.md:61`). Arquiteto e PO varrem o documento e acham o irmão: o follow-up arquivado tem o mesmo buraco. Vira uma decisão só. É regra de documento aprovado, então é do dono mesmo com opção segura (`tech-lead.md:62`). Passa no portão: mensagem enviada não volta. Anoto para as lições que o construtor de teste deixou passar essa regra.

**Mensagem ao dono** (1 aviso + 1 mensagem na conversa)

Aviso:
`Decisão sua trava parte do projeto do follow-up: mensagens agendadas param quando o follow-up é desligado? Recomendo que sim. Detalhes no Claude.`

Conversa:
```
O que mudou: a construção vai bem, mas achamos uma regra que ficou de fora do documento que você aprovou: o que acontece com as mensagens já agendadas quando alguém desliga ou arquiva um follow-up. Hoje elas continuam saindo: o cliente desliga, e o contato dele ainda recebe as mensagens dos dias seguintes. Pausei só essa parte; o resto segue. Tô certo que a gente fecha isso rapidinho!

Onde estamos:
  ✅ pronto: documento e esboços aprovados; editor novo em construção adiantada
  🔄 andando: projeto editor novo + defeitos da tela (a parte de desligar e arquivar está pausada, esperando você)
  ⏸️ parado ou na fila: motor de envio (para depois); demais problemas da auditoria (guardados); tirar o código das funções antigas (depois que você remover)

🚨 Urgente: remover as duas funções antigas (passo a passo mais acima, na conversa).

Sua vez: decidir o que acontece com as mensagens agendadas quando o follow-up é desligado ou arquivado.
  A) Canceladas na hora: depois de desligar, nada mais sai. Se religar, vale só dali para frente, sem mandar o que ficou para trás.
  B) Continuam saindo, como hoje: o contato recebe o que já estava marcado, mesmo com o follow-up desligado.
  C) Ficam guardadas e saem quando religar: mensagens podem chegar atrasadas e fora de contexto.
  Recomendo A: desligar é o jeito do cliente dizer "pare", e mensagem enviada não volta. Se você não souber, sigo com A.
```

**Mesa, fila e urgente**
- Mesa: decidir o destino das mensagens agendadas ao desligar ou arquivar.
- Fila: nada.
- Urgente: remover as duas funções antigas.

---

## 7. O dono, sem responder o item 6: "aquelas bolinhas laranja no esboço, o que são?"

**Bastidores**
- É pergunta simples: vale resposta curta com o "Sua vez" no fim (`tech-lead.md:109`). É um fato, então leio a legenda do esboço em `docs/projetos/followup-editor/telas.md` em vez de chutar.
- Não repito a decisão do item 6: ela fica em uma linha no "Sua vez" (`tech-lead.md:94`). Ele pode estar estranhando, então deixo uma pergunta de esclarecimento que não trava nada, com o que faço se ele não responder.

**Mensagem ao dono** (1 mensagem na conversa)
```
As bolinhas laranja marcam uma etapa da sequência que ainda está incompleta, por exemplo sem o texto da mensagem ou sem o tempo de espera. Enquanto houver uma bolinha laranja, o botão de ligar o follow-up fica bloqueado; é isso que impede um follow-up de ser ligado pela metade. Se algo nelas te incomodou (cor, tamanho, o que significam), me diga; se não disser nada, ficam como no esboço. Boa pergunta, dattebayo!

🚨 Urgente: remover as duas funções antigas (passo a passo mais acima, na conversa).
Sua vez: decidir o que acontece com as mensagens agendadas quando o follow-up é desligado (recomendo cancelar; detalhes na mensagem anterior).
```

**Mesa, fila e urgente**
- Mesa: a decisão do item 6, ainda aberta.
- Fila: nada.
- Urgente: remover as duas funções antigas.

---

## 8. Tudo pronto: PR, uma mudança no banco (coluna nova, 0 linhas alteradas) e duas funções novas

**Premissa:** entre 7 e 8, o dono respondeu o item 6 com a recomendação A. Sem isso, a parte pausada não estaria pronta, e "tudo pronto" seria falso: a fatia voltaria.

**Bastidores**
- Verificação final (ref. §1.3 passos 10 a 12): história de ponta a ponta, testes, Security, Revisor e notas de versão. Leio de verdade as verificações automáticas do PR. O PR segue como rascunho, e a primeira linha da descrição diz o que precisa vir antes (`tech-lead.md:112`).
- Conto em produção, só lendo: a coluna não existe e 0 linhas são alteradas. O Arquiteto confirma que o código antigo funciona com a coluna nova e que ninguém chama as funções novas antes da tela nova entrar.
- Por isso inverto a ordem que veio "publicar as funções depois de juntar": publicadas depois, a tela nova ficaria alguns minutos no ar chamando funções que não existem. Pela regra (`tech-lead.md:128`), quem publica as funções sou eu, depois do "pode" dele. Mando o roteiro inteiro para ele ter o mapa, mas só o passo 1 é ação. Esta mensagem pede autorização de mudança em produção: vai sem voz e sem "Fala:".

**Mensagem ao dono** (1 aviso + 1 mensagem na conversa, sem voz)

Aviso:
`Projeto do editor do follow-up pronto. Primeiro passo seu: autorizar uma mudança no banco. Detalhes no Claude.`

Conversa:
```
O que mudou: o projeto do editor novo e dos defeitos da tela está pronto. Testes, segurança e revisão estão aprovados. Para colocar no ar são 3 passos, nesta ordem, um de cada vez:
  1. Seu "pode" para uma mudança no banco (eu aplico e confiro).
  2. Seu "pode" para colocar no ar duas funções novas do servidor (eu publico e confiro). Ninguém as usa até a tela nova entrar, então nada muda para os clientes nesse passo.
  3. Você junta o projeto na versão principal, e isso coloca a tela nova no ar em poucos minutos.
  A ordem importa: a tela nova precisa do banco e das funções já prontos. Por isso o projeto fica travado como rascunho até os passos 1 e 2.

Onde estamos:
  ✅ pronto: editor novo e defeitos da tela, construídos e conferidos
  🔄 andando: nada
  ⏸️ parado ou na fila: passos 2 e 3 acima; motor de envio (para depois); demais problemas da auditoria (guardados); tirar o código das funções antigas (depois que você remover)

🚨 Urgente: remover as duas funções antigas (passo a passo mais acima, na conversa).

Sua vez: passo 1, autorizar a mudança no banco.
  O que faz: acrescenta a cada follow-up um campo novo, o momento em que ele foi desligado ou arquivado. A tela nova usa esse campo para cancelar as mensagens agendadas, como você decidiu.
  Dados existentes: nenhuma linha é alterada (contei agora: 0). Os follow-ups de hoje funcionam igual, com ou sem o campo.
  Como confiro: depois de aplicar, te mostro o campo criado, 0 linhas alteradas e nenhum alerta novo no painel do Supabase.
  Como voltar atrás: remover o campo; como nada foi gravado nele, nada se perde.
  Se estiver de acordo, responda "pode". Na hora de aplicar, aparece uma confirmação na sua tela: é a segunda chave, de propósito.
```

**Mesa, fila e urgente**
- Mesa: "pode" para a mudança no banco (passo 1).
- Fila: "pode" para as duas funções novas (passo 2); juntar o PR (passo 3, eu tiro do rascunho depois de 1 e 2).
- Urgente: remover as duas funções antigas.

---

## 9. O dono: "juntei o PR"

**Era possível pelas regras?** Não deveria ter acontecido. Só o passo 1 foi mandado, e o PR estava em rascunho. Pelas regras, o dono não recebeu o passo "juntar" (`tech-lead.md:111`: comando só vai com a pré-condição cumprida), e o rascunho existe para isso não acontecer sem querer (`tech-lead.md:112`). Tecnicamente, porém, dá para fazer: no GitHub, quem tem permissão clica "Ready for review" e junta. O rascunho protege contra acidente, não contra quem decide juntar.

**Bastidores**
- Não acredito no relato nem no meu roteiro: confiro, só lendo, o estado do PR no GitHub, se a Vercel publicou e se o campo existe no banco. Pode ser que "juntei" signifique outra coisa (um "pode" mal dito), e o fato decide.
- Ramo A (confirmado: juntou e a Vercel publicou; campo e funções não existem): a tela nova está no ar sem o que precisa. Desligar ou arquivar dá erro, então o produto está quebrado para os clientes: é grave (`avisos.md:17`). Segunda opinião rápida confirma. Dois caminhos: completar para a frente (o banco e as funções já estavam prontos e testados) ou desfazer o PR (outro PR, que ele junta). Recomendo completar: termina o projeto, e cada passo continua com seu "pode". Mensagem sem voz. Nas lições, depois: propor uma proteção mais forte do que o rascunho.

**Mensagem ao dono, ramo A** (1 mensagem na conversa, sem voz; ele está na tela, então não vai aviso)
```
O que mudou: conferi, e o projeto foi juntado antes dos passos 1 e 2. A tela nova já está no ar, mas o banco e as funções de que ela precisa ainda não. Por isso, agora, desligar ou arquivar um follow-up dá erro para os clientes. O resto da tela funciona. O conserto mais rápido é fazer agora os passos 1 e 2, que já estavam prontos e testados; leva poucos minutos.

Onde estamos:
  ✅ pronto: projeto juntado e no ar
  🔄 andando: completar o que falta para desligar e arquivar voltarem a funcionar
  ⏸️ parado ou na fila: passo 2 (funções novas); motor de envio (para depois); demais problemas da auditoria (guardados); tirar o código das funções antigas (depois que você remover)

🚨 Urgente: desligar e arquivar follow-up estão dando erro para os clientes; o conserto é o "pode" abaixo.
🚨 Urgente: remover as duas funções antigas (passo a passo mais acima, na conversa).

Sua vez: "pode" para a mudança no banco, a mesma da mensagem anterior (acrescenta o campo do momento em que o follow-up foi desligado; 0 linhas alteradas, contei de novo agora; volta atrás removendo o campo). Assim que eu aplicar e conferir, te peço o "pode" das duas funções, e aí desligar e arquivar voltam a funcionar. A outra saída é desfazer a junção e voltar à tela antiga, que também leva alguns minutos, mas deixa o projeto de fora. Recomendo completar.
```

**Mensagem ao dono, ramo B** (se a conferência mostrar o PR ainda em rascunho, não juntado)
```
Conferi aqui: o projeto ainda não foi juntado. Ele continua travado como rascunho, de propósito, até os passos 1 e 2. Talvez você tenha querido dizer "pode" para o passo 1? Se for isso, me responda "pode" que eu aplico a mudança no banco.

🚨 Urgente: remover as duas funções antigas (passo a passo mais acima, na conversa).
Sua vez: "pode" para a mudança no banco (passo 1).
```

**Mesa, fila e urgente (ramo A)**
- Mesa: "pode" para a mudança no banco, agora com pressa.
- Fila: "pode" para as duas funções novas. Depois disso, conferir desligar e arquivar no ar.
- Urgente: (1) desligar e arquivar quebrados para os clientes, e o conserto é o item da mesa; (2) remover as duas funções antigas.
- Fila de lições (ref. §9): propor ao dono uma proteção mais forte do que o rascunho, ou exigir que o código novo funcione sem a mudança no banco.

**Mesa, fila e urgente (ramo B):** sem mudança em relação ao item 8.

---

## Contagem de mensagens ao dono
- Mensagens na conversa: **8** (itens 1, 3, 4, 5, 6, 7, 8, 9; o item 9 tem uma de dois ramos possíveis).
- Avisos de uma linha: **5** (itens 1, 3, 5, 6, 8). O canal só os mostra se o dono não estiver olhando.
- Nenhuma mensagem só para lembrar. O urgente aparece como uma linha em 7 mensagens seguidas, sem escalar.

---

## Autoavaliação: o que ainda ficou ambíguo ou conflitante

1. **Quem mexe em funções do servidor.** `tech-lead.md:128` diz que mudança de "função" quem aplica é o Tech Lead, depois do "pode". `tech-lead.md:127` diz "nunca publica". `avisos.md:12` põe "colocar no ar" como ação que só o dono faz. O cenário diz "remover é ação do dono" e "funções novas para o dono publicar". A ref. §4.1 (`tech-lead-referencia.md:109-131`) detalha banco e n8n, mas não Edge Functions: não diz como contar impacto, como conferir nem como voltar atrás. Segui a linha 128 no item 8 e o cenário no item 1: inconsistente por necessidade.
2. **Emergência sem escalada.** `tech-lead.md:92` põe o urgente como uma linha fora da mesa, e `avisos.md:25` diz "já avisou e nada mudou, não repita". Resultado: um furo que deixa qualquer pessoa parar o serviço de todos os clientes ficou aberto do item 1 ao 9, lembrado só por uma linha. Nenhuma regra manda reavisar depois de X horas, oferecer ajuda para fazer junto, nem reconferir no sistema real se o furo ainda existe antes de repetir a linha. Eu assumi que continuava aberto sem conferir (contra `tech-lead.md:141`).
3. **"Na hora" contra "segunda opinião antes de alarmar".** `tech-lead.md:143` e `avisos.md` pedem aviso imediato. `tech-lead-referencia.md:144` manda pedir segunda opinião antes de alarmar com achado grave, sem limite de tempo nem forma rápida. Fiz uma segunda opinião "rápida", que não está definida em lugar nenhum.
4. **Passo a passo da emergência contra um passo por vez.** `tech-lead.md:111` manda um passo por vez. `tech-lead.md:143` manda "com o passo a passo". O formato da mesa (`tech-lead.md:96-108`) não tem espaço para a linha "🚨 Urgente" nem para os passos dela: a linha só existe na prosa da `tech-lead.md:92`. O modelo "Sua vez: nada agora, pode cuidar de outra coisa" (`:107`) contradiz um urgente aberto.
5. **"O que mudou: 1 a 3 linhas" contra conteúdo obrigatório.** `tech-lead.md:100` limita a 1 a 3 linhas, mas `tech-lead.md:51` manda pôr o espelho e o caminho ali, e `comunicacao.md:51` manda apresentar o que foi achado antes de perguntar. Nos itens 3, 4 e 6 estourei as 3 linhas ou joguei as opções no "Sua vez".
6. **Uma pergunta por mensagem contra tudo de uma vez.** `comunicacao.md:52` pede uma pergunta por mensagem. `tech-lead.md:62` manda levar as decisões novas tudo de uma vez. `tech-lead-referencia.md:57` pede escolha numa conversa só. `tech-lead.md:91` diz "no máximo uma decisão na mesa". Não está claro se um documento com N perguntas, ou um pacote de decisões, conta como uma. No item 5 contornei transformando as perguntas em regras com recomendação.
7. **"Se você não souber, sigo com A" não serve para tudo.** A saída de `comunicacao.md:57` e `tech-lead.md:114` não se aplica à aprovação do documento (`tech-lead.md:57` exige aprovação) nem à abertura de frente. Não há regra para silêncio numa decisão que trava: `tech-lead.md:93` só cobre pergunta de esclarecimento. O item 8 ("tudo pronto") pressupõe uma resposta ao item 6 que o roteiro não mostra; tive de assumir.
8. **A proteção do rascunho é fraca e não há plano para quem fura a ordem.** `tech-lead.md:112` diz "rascunho não se junta sem querer", mas o dono pode tirar do rascunho e juntar. Nada diz quem tira do rascunho (`tech-lead-referencia.md:104` diz só "vira pronto"). Nada cobre o dono agindo fora da ordem (item 9): se é grave, e se o certo é completar para a frente ou desfazer. O "melhor ainda" de `:112` cobre só o banco novo com código antigo, não o código novo sem a mudança no banco, que foi o caso real.
9. **Um "pode" por mudança, com texto conflitante.** `tech-lead-referencia.md:127` diz "cada uma com seu pode... uma de cada vez". `:131` proíbe juntar num "pode" só "sem que o dono veja cada uma", o que dá a entender que, vendo cada uma, pode. Numa quebra ativa (item 9), dois "pode" em sequência custam minutos de cliente com erro.
10. **Voz e "Fala:".** `tech-lead.md:121` manda trazer a "Fala:" do agente. `:123` proíbe voz em autorização e emergência, mas não diz se a "Fala:" conta como voz; assumi que sim e a tirei nos itens 1, 8 e 9. O Tech Lead também não sabe a persona dos outros agentes: as "Falas" do PO saíram genéricas.
11. **Nomes internos contra ação do dono.** `tech-lead.md:113` proíbe nomes internos, mas para remover as funções o dono precisa do nome exato que aparece na tela (item 1). Falta a exceção "nome que o dono precisa clicar".
12. **Aviso e mensagem na conversa: um ou dois.** `avisos.md:29-36` define o aviso como uma linha que chama o dono até a conversa. `tech-lead.md:92` e `:143` falam em "avisar na hora" sem dizer que são duas peças. `avisos.md:9` ("só quando o dono pode não estar olhando") pede um julgamento que o Tech Lead não consegue fazer; o canal decide (`:42`). A contagem de "mensagens ao dono" fica ambígua.
13. **Quando um defeito vira urgente no meio do projeto.** "Desligar não para os envios" (item 6) é o cliente dizendo "pare" e o contato recebendo mesmo assim: discutivelmente "quebrado para o cliente agora" (`avisos.md:17`) ou a exceção de `tech-lead-referencia.md:59`. Não há critério para saber quando um achado de construção pula para urgente, em vez de ser decisão na mesa. O mesmo vale para "excluir apaga histórico" no item 2.
14. **Urgente e mesa são a mesma coisa.** No item 9, o conserto da emergência é o próprio item da mesa (o "pode"). `tech-lead.md:92` pressupõe que emergência e mesa andam separadas; a sobreposição não está prevista.
15. **Premissa do cenário.** A situação inicial lista designer, revisor e pesquisador lançados, mas o Security entrega no item 1. `tech-lead-referencia.md:50` inclui o Security na auditoria, então provavelmente faltou citá-lo; registrei sem tratar como erro.
