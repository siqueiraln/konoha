# Pesquisa: Notifier

Material bruto. Nada aqui é o agente final.

## 1. Diagnóstico do original (`09_notifier.md`)

**Manter:** mensagem curta, em português; bloqueio com opções, consequências e recomendação; nunca mais de uma mensagem por evento; falha no envio não para o trabalho.

**Cortar:**
- Avisos de rotina ("sprint iniciada", "feature concluída", "seguindo para a próxima"): notificação que o dono não precisava treina o dono a ignorar todas.
- "Deploy realizado" como evento automático: colocar no ar é ato do dono.
- Um agente inteiro para mandar uma mensagem de uma linha: chamar um agente custa mais que a mensagem, e o agente chamado não sabe o contexto que decide se vale avisar.
- Telegram com token em variável de ambiente, configurado à mão.

**Falta:** os momentos que o dono **não pode perder** (decisão esperando, ação que só ele faz, problema grave); o critério de "vale interromper?"; o que nunca vai numa notificação (dado de cliente, segredo).

## 2. Seasoned

Não tem agente de notificação. O que tem é a lista de **quando** o humano precisa ser chamado:
- pergunta esperando resposta (é o que trava o trabalho);
- ação que só o usuário faz: juntar na versão principal, publicar, configurar chave ou conta nova, pagar um serviço;
- trabalho terminado e pronto para o usuário testar;
- execução automática de testes vermelha que ninguém leu (ficou 2 horas e 4 envios vermelha até alguém notar; no CRM, 8 dias);
- limite de uso da assinatura chegando; memória do orquestrador enchendo;
- serviço fora do ar (agentes morrendo na hora).

Regras: nunca avisar "testes verdes" ou "publicado" sem ler o resultado de verdade; linguagem simples; uma pergunta por mensagem, com recomendação; sem dado pessoal de cliente. "Se o trabalho está bombardeando o usuário de perguntas, o problema está no planejamento."

## 3. O que já existe no ambiente (conferido em 2026-09-26)

- **Notificação nativa do Claude Code** (`PushNotification`): aviso na área de trabalho e, com o **Remote Control** ligado, no celular. Não precisa configurar nada. A própria ferramenta pula o aviso quando o dono está olhando o terminal (seria repetido). Mensagem de até 200 caracteres, uma linha.
- Ela é da **sessão principal** (quem conversa com o dono, o Tech Lead). Subagentes devolvem para quem os chamou; quem decide avisar é a sessão principal.
- Outros canais possíveis: Gmail (conector ligado), Telegram (exige bot e token), WhatsApp (o CRM do dono usa a API oficial, mas mandar mensagem proativa exige modelo aprovado pela Meta e tem custo).

## 4. Proposta

**O Notifier deixa de ser agente e vira um protocolo** (`protocolos/avisos.md`) que o Tech Lead segue: a lista fechada de quando avisar, o formato da mensagem e o que nunca vai nela. Canal padrão: notificação nativa do Claude (área de trabalho + celular pelo Remote Control). Canal extra (Telegram, e-mail) só se o dono quiser receber longe do Claude.
