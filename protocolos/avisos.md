# Protocolo de avisos ao dono

Quem segue: **o Tech Lead** (a sessão que conversa com o dono). Subagentes não avisam o dono: devolvem para quem os chamou, que decide.

Aviso interrompe o dono onde ele estiver. Aviso que ele não precisava ensina o dono a ignorar todos, e o importante se perde. Por isso a lista é fechada: **fora dela, não se avisa.** Para acompanhar o andamento, o dono pergunta ao Tech Lead quando quiser.

## Quando avisar

Só nestes casos, e só quando o dono pode não estar olhando:

1. **Uma decisão dele trava o trabalho.** Uma pergunta passou pelo portão do protocolo de comunicação e nada mais pode andar sem a resposta.
2. **Uma ação que só ele faz:** juntar na versão principal, colocar no ar, criar conta, colocar chave de acesso, pagar um serviço, trocar um segredo vazado.
3. **Algo ficou pronto para ele testar:** um projeto ou uma etapa que termina na mão dele (não cada fatia).
4. **Algo grave:**
   - emergência de segurança (segredo exposto; dados de clientes acessíveis por quem não devia; furo que deixa alguém de fora parar ou alterar o serviço de todos os clientes; tudo em produção);
   - testes automáticos do produto vermelhos na versão principal;
   - produto fora do ar ou quebrado para os clientes: um cliente vê erro, deixa de receber o que devia, ou recebe algo errado **agora** (não "pode acontecer um dia").
5. **Limite de uso** da assinatura perto de acabar, com trabalho em andamento.

**Não se avisa:** início de trabalho, fatia concluída, "seguindo para a próxima", teste passando, progresso. Isso o dono pergunta quando quiser.

## Antes de avisar, confira

- **O fato é verdade agora?** Nunca avise "testes verdes", "publicado" ou "consertado" sem ler o resultado de verdade (a saída do teste, o registro da publicação, o banco).
- **É um evento, um aviso.** Se já avisou e nada mudou, não repita.

## Como escrever

Uma linha, até 200 caracteres, sem formatação. Comece pelo que o dono vai fazer.

- Decisão: `Decisão sua trava o projeto Agenda: aceitar horário duplo? Recomendo não. Detalhes no Claude.`
- Ação: `Projeto Agenda pronto para juntar na versão principal. Testes, segurança e revisão aprovados.`
- Pronto: `Importação de contatos pronta para você testar no ambiente local.`
- Grave: `URGENTE: chave do WhatsApp legível por qualquer usuário logado. Trocar a chave primeiro. Passo a passo no Claude.`

Linguagem de negócio (protocolo de comunicação, seção 2). Os detalhes, as opções e a recomendação ficam na conversa, no formato do protocolo de comunicação; o aviso só chama o dono até lá.

**Nunca num aviso:** dado de cliente (nome, telefone, conteúdo de mensagem), senha, chave, token.

## Canal

Notificação nativa do Claude Code: na área de trabalho e, com o Remote Control ligado, no celular. Ela pula o aviso quando o dono já está olhando a tela; isso é esperado.

Se o envio falhar, o trabalho continua; o aviso fica registrado na resposta ao dono.
