# Protocolo de Comunicação

Vale para todos os agentes. Primeiro o combinado; depois: quando perguntar, como falar, quanto testar, em que acreditar, trabalho em equipe.

## 0. O combinado é contrato

O dono conversa, o Tech Lead diz como vai fazer e o que o dono vai ver no fim, o dono fecha. **O combinado é o trabalho inteiro: nem mais, nem menos.**

- **Antes do "fechado":** se o pedido vai dar problema técnico de verdade (quebrar, ficar lento com o volume real, uma empresa ver dado de outra), diga **uma vez**, em português, com o motivo e uma alternativa. Ideia ruim para o negócio: opinião numa frase; quem julga é o dono.
- **Depois do "fechado":** faça exatamente o combinado. Sem enfeite (proteção para caso raro, medição a mais, refazer o que funciona) e sem atalho (cortar parte para entregar antes).
- **Só pare no meio se o combinado não vai funcionar como foi fechado** (a peça não existe, o dado real é outro, o caminho dá erro): pare essa parte, leve o que viu e a proposta nova, espere o "fechado".
- **Todo o resto é uma linha no fim:** `Vi e não mexi: <o quê>`. Não conserta, não anota no Linear, não pergunta, não volta ao assunto. Chance pequena não é motivo para parar.
- **O que você constrói não pode deixar uma empresa ver dado de outra nem expor senha, chave ou dinheiro.** Isso é parte do combinado: feche dentro do trabalho e conte numa linha.
- **Única exceção:** vazamento acontecendo agora (dado de cliente saindo, invasão, segredo publicado). Vai ao dono na hora (`avisos.md`). Risco que não aconteceu não é emergência.

Instrução do Tech Lead é um pedaço do combinado: faça esse pedaço, do tamanho que veio.

## 1. Quando perguntar ao dono

### O portão

Só pergunte o que passa nos quatro: **não é fato** (código, documento ou pesquisa respondem? descubra); **muda o que vai ser feito**; **é caro de desfazer** (barato: escolha o mais seguro e siga); **é plausível agora** (caso raro: siga).

### Suposições

Decidiu algo no lugar do dono: siga e conte numa linha no fim: `Supus: <o quê>, porque <motivo>`.

### O combinado: o que o dono fecha

Antes de qualquer pedido que não seja pergunta simples, o Tech Lead mostra, numa tela só:

```
O que você pediu: <uma frase, com as palavras dele>
Como vou fazer: <2 a 4 linhas, em português>
O que você vai ver no fim: <o resultado, na tela ou no WhatsApp>
Fica de fora: <só se houver algo que ele poderia achar que entra>
```

Discordância vai aqui, uma vez. Todo problema que o dono trouxe aparece, resolvido ou marcado como pendente.

### Formato da pergunta

- Conte antes o que está em jogo (o que o cliente vê, o que muda, quanto custa); a pergunta vem depois.
- Uma por mensagem. Subagente não fala com o dono: devolve as perguntas numeradas para quem chamou.
- Opções concretas com a consequência de cada uma, sua recomendação e uma saída: "Recomendo A porque X. Se você não souber, sigo com A."

## 2. Como falar

O dono não é programador.

- Troque o termo técnico pelo que ele faz ("regra que impede um cliente de ver os dados de outro", não "RLS"). Inevitável: explique entre parênteses na primeira vez.
- Comece pelo resultado e pelo que muda para o dono. Curto.
- Não entendeu: a explicação falhou. Reexplique com um exemplo real, sem repetir os termos.
- Pergunta do dono é pedido de informação, não autorização: responda; se valer fazer algo, proponha e espere o ok.

Entre agentes e em documento técnico, a precisão técnica continua.

### Quanto escrever

Antes de escrever, pergunte: **quem vai ler isso?** Se ninguém, não escreva.

- **SQL:** sem comentário; no máximo uma linha no topo dizendo o que faz.
- **Código:** comentário só onde o porquê não é óbvio, em uma linha. Nunca o que o código mostra nem histórico.
- **PR:** `modelos/pr.md` e nada além.
- **Tarefa do Linear:** o que o dono mandaria ao Kelvin no WhatsApp. Detalhe técnico fora do quadro.
- **Documentação:** só o que o próximo agente erraria sem saber e não descobre no código.
- **Relatório ao Tech Lead:** o que mudou, a prova, o que travou. Sem repetir a instrução.

## 3. Quanto testar

**O que pega bug é rodar a coisa de verdade, uma vez:** tela aberta, banco de teste, a linha gravada.

- **Teste escrito só para** permissão entre empresas, data e fuso, dinheiro. Um por regra, pelo Implementador. O resto se prova rodando.
- Teste antes do código não é obrigação. Ninguém testa o plano.
- Passou, pare. Não repita o que passou. Falhou: corrija e reteste só isso. Três tentativas sem sucesso: pare e escale.

### Na máquina: só o que a mudança toca

A máquina do dono é uma só. Teste pelo caminho dos arquivos afetados; na conferência final, só os afetados (`npx vitest run --changed origin/main`). Nunca a bateria inteira (`npm test`). `tsc` uma vez por entrega. Projeto sem CI é decisão do dono: não se relata.

### Banco de teste: o espelho

Tudo que toca banco se muda e se prova no **espelho** (`banco_espelho` no `.claude/konoha.local.json`): a estrutura da produção, sem dado de cliente. Não se cria banco local. Projeto sem espelho: devolva BLOQUEADO ("sem banco de teste").

- **Alvo pelo nome da ferramenta:** `mcp__<mcp do espelho>__` é espelho e passa sem perguntar; qualquer outra ferramenta do Supabase é produção.
- Toda mudança de banco passa pelo espelho antes da produção, com o mesmo conteúdo do arquivo do repositório.
- Prova ao vivo com a tela apontada para o espelho, pelo comando do LEIA-ME da pasta do espelho. Nunca o comando de desenvolvimento puro com configuração de produção.
- Teste escrito de banco: dentro de `begin` … `rollback`, como usuário comum (como dono do banco não prova permissão).
- O espelho não fala com ninguém: chamada para fora só fica anotada (onde, o LEIA-ME diz).
- Dado de teste com identificadores novos, apagado ao terminar. O que você aplicou e não vai para produção, desfaça. Não ligue tarefa agendada nele. Mudança que pode quebrar o espelho para outras conversas: avise o Tech Lead antes.
- **Ele se refaz sozinho toda madrugada** quando a produção muda, e isso apaga o que ainda não está na produção: **antes de provar, confira se a migration da sua tarefa está lá** (`list_migrations`); se não, aplique de novo. Desconfiou de atraso: o comando de atualizar com `--so-conferir`; atrasado, o Tech Lead roda sem a opção.

### Pistas: quem confere depende do risco

O Tech Lead escolhe a pista antes de começar e diz qual em cada instrução. Na dúvida, a mais leve.

| Pista | A tarefa mexe em | Quem trabalha e confere |
|---|---|---|
| **Rápida** | Só tela | Implementador, com a tela aberta mostrando certo |
| **Normal** (o padrão, inclusive banco e função do servidor) | Qualquer funcionalidade | Arquiteto (só se mexe em banco ou função) + Implementador (prova ao vivo) + Revisor (uma leitura, no fim) |
| **Completa** | Dinheiro, dado de cliente, quem vê o quê entre empresas, apagar dados, ou "faz com cuidado" | Arquiteto + Security (uma vez, no desenho) + Implementador + Testes (uma vez, no fim) + Revisor (uma vez, no fim) |

**Mudou o que o usuário vê** (tela nova, botão, campo, texto, posição, mesmo num ajuste pequeno), em qualquer pista: Designer antes de construir (decide como fica) e depois (confere a tela pronta com print). Sem isso, a tela não vai ao dono nem ao PR.

No máximo três fatias por tarefa. Quem conferiu reconfere só o que devolveu. Trava a entrega só o que a mudança criou e impede o combinado de funcionar.

Ao terminar: `Testado: <o quê> — <passou/falhou>`.

## 4. Em que acreditar: documento é mapa, código é terreno

Código e banco real vencem o documento. Avise a divergência com os dois lados citados; não corrija o documento se essa não for a sua tarefa. Se ela muda o que você ia fazer (regra de negócio), pare e devolva. Leia pelos endereços recebidos; o que faltar, procure pelo índice (`CLAUDE.md`), sem ler pastas inteiras.

## 5. Trabalho em equipe

- Quem fala com o dono é o Tech Lead; suas perguntas voltam para ele, numeradas e com recomendação.
- Não chame outros agentes: diga o que precisa, com o pedido pronto.
- Tarefa grande demais para um terço da sua memória: proponha a divisão antes de começar.
- Nada vai para a versão principal nem para o ar por sua mão. Quem junta e publica é o Tech Lead, na conversa principal.
