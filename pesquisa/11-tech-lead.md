# Pesquisa: Tech Lead

Material bruto. Nada aqui é o agente final.
Fontes: `referencia/dev-squad-original/00_tech-lead.md`, `pesquisa/seasoned-skills.md` §1.1 (o maior capítulo do Seasoned), documentação oficial do Claude Code (conferida em 2026-09-26), e as decisões do dono ao longo da construção dos outros agentes.

## 1. Fatos do Claude Code que decidem o formato (conferidos na fonte)

Fonte: https://code.claude.com/docs/en/sub-agents.md
- **Subagente pode chamar subagente**, até três camadas abaixo da conversa principal. Por isso cada agente da empresa precisa da regra "não chame outros agentes; peça ao Tech Lead".
- **Subagente não pode perguntar ao dono** (`AskUserQuestion` é removido dos subagentes). Toda pergunta sobe para a conversa principal. Confirma a regra do protocolo.
- **A conversa principal pode ser o Tech Lead:** `claude --agent tech-lead`, ou `"agent": "tech-lead"` no `.claude/settings.json` do projeto. Funcionamento no app desktop: não confirmado na documentação; testar na instalação.
- **Modelo por agente:** `sonnet`, `opus`, `haiku`, `fable`, id completo, ou `inherit`.
- Outros campos úteis: `isolation: worktree` (cópia isolada do repositório por agente), `memory`, `skills`, `maxTurns`, `disallowedTools`.
- Existe o gancho `SubagentStop` (quando um subagente termina).

Nota de método: o agente auxiliar que pesquisou isso errou dois pontos (disse que subagente pode perguntar ao dono e que `SubagentStop` não existe). A conferência na fonte corrigiu. É a regra "verificar, nunca confiar" na prática.

## 2. Diagnóstico do original (`00_tech-lead.md`)

**Manter:** não implementa, decide e delega; toda delegação com contexto, entrada, saída, critério de pronto e o que não fazer; interromper o dono só no que é dele, uma pergunta por vez, com opções e recomendação; decide conflitos entre agentes e registra.

**Cortar:** sprints, backlog, "sprint status"; arquitetos em paralelo e "consolidar decisões" (agora é um Arquiteto); "decisões conservadoras na dúvida" (o Seasoned: a opção que dissolve o dilema vence); Notifier a cada marco; "deploy realizado na Vercel" como evento automático; "forneça trechos do PRD" (melhor: o caminho e a seção exata).

**Falta:** conferir o trabalho dos agentes (hoje aceita o relatório); tamanho de cada tarefa; registro de andamento que sobrevive à memória cheia; o que fazer quando um agente morre no meio; tipos de pedido diferentes (pergunta, conserto, projeto, auditoria); o fluxo novo da empresa.

## 3. Seasoned: o que mais importa (resumo; detalhe no arquivo do Seasoned)

- **Os agentes digitam; o chefe decide, confere e lê as mudanças.** Edição própria só quando escrever as instruções custaria mais que a edição.
- **Rodada de arquitetura antes de delegar:** qual o mecanismo por trás do pedido, onde mais ele vive, consertar na causa. Demandas agrupadas por mecanismo, não por tela.
- **Consertar defeito comprovado não é pergunta.** Ao dono só vão escolhas reais.
- **Tamanho:** cada agente termina em ~1/3 da memória. Estimar antes; dividir se passar.
- **As instruções de cada tarefa (charter):** caminhos exatos; o que não tocar quando há agentes em paralelo; parar se a premissa for falsa ("verificado, já estava certo" é resultado válido); terminar em commit e parar; convenções do projeto como lei; classificar o estado do disco primeiro.
- **Verificar, nunca confiar:** conferir o relatório contra a mudança item a item; rodar as verificações você mesmo; "todos cobertos" só contra uma contagem feita no sistema real; zero achados só vale se o agente terminou de verdade.
- **Registro de andamento (ledger):** cabeça com as diretivas vigentes + diário cronológico. Atualizado sempre, porque a memória pode ser compactada a qualquer momento. Depois de compactar: reler o registro e as fontes; onde discordam, as fontes vencem.
- **Recuperação:** antes de relançar, confirmar o que ainda está vivo; o agente "morto" pode ter terminado.
- **Linha de base:** antes da primeira mudança, rodar tudo na versão limpa e anotar os números.
- **Juntar na versão principal é do usuário.** Testes verdes ou revisão aprovada não autorizam.
- **Paralelismo:** o que é independente sai junto; o que depende espera a dependência terminar. Um agente que escreve por cópia do repositório.

## 4. As decisões do dono que o Tech Lead carrega

- **Porta única:** o dono fala só com o Tech Lead.
- **Fluxo:** PO (documento) → Designer (telas; esboço visual só nas telas decisivas) → Arquiteto (costura, depois partes) → Implementador (fatias de ponta a ponta) → Security + Testes → Revisor → Docs.
- **Uma pergunta por chamada** para a Pesquisadora; trabalho dividido para caber na memória de cada agente ("se perde com várias camadas").
- **Avisos:** só os do `protocolos/avisos.md`; o resto o dono pergunta ao Tech Lead.
- **Documento é mapa, código é terreno** (protocolo §4); os agentes recebem **endereços com seção**, não "leia a documentação".
- Lista de casos extremos cresce a cada bug; o Tech Lead acrescenta as linhas propostas pelos agentes.

## 5. Ponto aberto para o dono

**Quem junta o trabalho na versão principal.** Na Vercel, juntar na versão principal normalmente **coloca no ar** sozinho (a integração com o Git publica a principal). Então "juntar" é, na prática, "publicar para os clientes".

## 6. Esqueleto proposto

Arquivo do agente curto, com os passos; a referência longa (checklist de instruções, fluxos por tipo de pedido) em `protocolos/tech-lead-referencia.md`, lida por seção.
1. Classificar o pedido: pergunta, conserto, projeto, auditoria, overclock.
2. Rodada de arquitetura (o mecanismo, onde mais vive).
3. Montar o fluxo do tipo; dividir por tamanho; lançar em paralelo o independente.
4. Instruções de cada tarefa pelo checklist.
5. Conferir cada entrega; decidir cada achado; registrar no andamento.
6. Falar com o dono pelo protocolo; avisar pelo protocolo de avisos.
7. No fim: Docs, lições para a lista e os guias, e a entrega na mão do dono.
