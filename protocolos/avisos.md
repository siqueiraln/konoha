# Protocolo de avisos ao dono

Quem segue: **o Tech Lead**. Subagentes não avisam o dono: devolvem a quem os chamou.

Aviso que o dono não precisava ensina a ignorar todos. A lista é fechada: **fora dela, não se avisa.**

## Quando avisar

Só nestes casos, e só quando o dono pode não estar olhando:

1. **Uma decisão dele trava o trabalho:** a pergunta passou pelo portão do protocolo de comunicação e nada anda sem a resposta.
2. **Uma ação que só ele faz:** juntar na versão principal, colocar no ar, criar conta, colocar chave de acesso, pagar um serviço, trocar um segredo vazado.
3. **Algo ficou pronto para ele testar:** projeto ou etapa que termina na mão dele (não cada fatia).
4. **Algo grave, agora:** emergência de segurança (segredo exposto, dado de cliente acessível por quem não devia, alguém de fora consegue parar ou alterar o serviço de todos; tudo em produção); testes automáticos vermelhos na versão principal; cliente vendo erro, deixando de receber ou recebendo algo errado **agora** (não "pode acontecer um dia").
5. **Limite de uso** da assinatura perto de acabar, com trabalho em andamento.

**Não se avisa:** início de trabalho, fatia concluída, teste passando, progresso.

## Antes de avisar

- Confira que o fato é verdade agora (a saída do teste, o registro da publicação, o banco).
- Um evento, um aviso. Já avisou e nada mudou: não repita.

## Como escrever

Uma linha, até 200 caracteres, sem formatação, em linguagem de negócio, começando pelo que o dono vai fazer. Detalhes e recomendação ficam na conversa.

- `Decisão sua trava o projeto Agenda: aceitar horário duplo? Recomendo não. Detalhes no Claude.`
- `URGENTE: chave do WhatsApp legível por qualquer usuário logado. Trocar a chave primeiro. Passo a passo no Claude.`

**Nunca num aviso:** dado de cliente, senha, chave, token.

Canal: notificação nativa do Claude Code (área de trabalho e, com Remote Control, celular). Se o envio falhar, o trabalho segue e o aviso fica na resposta ao dono.
