# Pesquisa: seasonedcc/seasoned-skills → empresa de agentes

Fonte: https://github.com/seasonedcc/seasoned-skills (lido via `gh api` em 2026-09-26, sem clonar nem executar nada).
Caminhos entre parênteses são relativos à raiz do repositório. "orq." abrevia `content/skills/orchestration/SKILL.md`.

## Como o seasoned funciona, em 8 linhas

- Uma sessão "orquestradora" (modelo mais forte) decide, delega, lê diffs e roda os gates longos; subagentes ("lanes") leem, constroem e testam, cada um num worktree isolado com banco, portas e env próprios (`content/doctrine/orchestration.md`, `content/skills/worktrees/SKILL.md`).
- O trabalho entra por um documento de *shaping* (Shape Up adaptado), e o documento termina num texto de `/goal` que dispara o build (`content/skills/shaping/SKILL.md`, `docs/the-way-of-working.md`, já lidos).
- Uma Definition of Done composta (gates, testes, cobertura de rotas, seed de demo, responsivo, browser, sem comentários, review loop, self-improvement) vale para toda tarefa (`content/doctrine/dod/*.md`).
- Todo PR abre como draft assim que os gates rápidos passam; a revisão adversarial roda contra o draft; merge na branch padrão é sempre ato do usuário (`content/doctrine/orchestration.md`, orq.).
- Nenhuma afirmação de subagente é aceita sem verificação ("verify, never trust"); o julgamento nunca desce de nível (orq.).
- Um *ledger* no scratchpad guarda estado durável; compactação é ritual comandado pelo usuário (`/prepare-for-compaction` → `/compact` → `/reground`) (`docs/running-a-session.md`).
- Toda tarefa termina com *self-improvement*: lições viram PR em draft que só o usuário marca como pronto/mergeia (`content/skills/self-improvement/SKILL.md`).
- Quase toda regra vem com o incidente que a motivou; o valor está nos detalhes operacionais, não em princípios genéricos.

---

## 1. Conteúdo por agente

### 1.1 tech-lead (orquestrador)

**Papel e limites**
- Orquestra toda tarefa, não só as grandes. Delega leitura/build/teste; "agents type; you decide, triage, and read diffs". Edição pessoal só quando escrever o charter custaria mais que a edição (escala de uma linha) (`content/doctrine/orchestration.md`).
- Regra para subagentes, que deve ir no prompt de todos os outros agentes: se você foi spawnado com tarefa específica, execute direto e nunca spawne subagentes, abra PR ou faça merge, a menos que o charter mande (`content/doctrine/orchestration.md`).
- Merge na branch padrão é do usuário: abrir o PR e parar. CI verde ou review aprovado nunca implica autorização (`content/doctrine/orchestration.md`). Em modo `/goal`, pode mergear PRs intermediários numa feature branch do goal (nunca na default), com um PR draft da feature branch para a default cujo corpo é reescrito a cada merge para descrever o estado atual (`content/doctrine/goals-merges-off.md`; variante que permite merge na base: `content/doctrine/goals-merges-on.md`).
- Gates longos são do orquestrador: o charter de um builder termina em commit (ou commit + push) e para; o builder roda só checagens rápidas (lint, typecheck dos arquivos tocados). O orquestrador roda a suíte completa em background e é dono de push/PR/merge (`content/doctrine/orchestration.md`, orq. "Charters").

**Rodada de arquitetura antes de delegar** (orq. "Judgment stays at the top")
- Toda demanda passa por uma rodada de arquitetura: mapear o mecanismo por trás do pedido, onde mais ele vive, e as repercussões das correções candidatas; corrigir no nível da causa raiz (um defeito que aparece numa rota mas nasce num primitivo compartilhado → corrige o primitivo). Lotes de demandas são agrupados por mecanismo, não por tela.
- Nunca trocar o caso principal por um caso raro: uma correção cujo custo cai sobre a maioria para fechar um canto raro é o formato errado. Aceite o resíduo e registre, ou escopo a mitigação ao próprio canto.
- Design e adjudicação são do nível do orquestrador. Se a evidência sob um design muda, refaça o design no topo; nunca repasse o design velho com "re-verifique suas citações".
- Invariantes que atravessam várias lanes (um saldo que todas precisam conservar) são desenhadas pelo orquestrador, commitadas como fixture, e as lanes recebem só regras de consumo.
- Quando lanes re-expressam comportamento existente (regras de autorização, validação), primeiro encomende um mapa auditado capacidade → comportamento de verdade com `file:line`, e todo charter de correção cita o mapa.
- No design, inventarie toda "costura" que o build não consegue exercitar sem algo que só o usuário fornece (chave de API de vendor, conta paga, dispositivo) e entregue a lista ao usuário enquanto o design ainda está aberto.
- Se manter uma abordagem verde exige correções caso a caso que geram novos casos, ou uma lane mói horas num defeito, isso é cheiro de design: pause e reabra a forma com o usuário.
- Qualquer escolha de ferramenta, lib, modelo ou serviço externo começa com pesquisa web ao vivo, nunca só com conhecimento de treino.
- Recomendações: uma opção que dissolve o trade-off vence todas que só o precificam; status quo só é recomendado se nenhuma opção dissolve.
- Antes de perguntar ao usuário sobre algo ou planejar mudança, checar trabalho em voo (`gh pr list` + branches remotas). Premissas sobre o sistema em produção são sondadas ao vivo (browser, curl, DNS), não inferidas do código.
- Termos do stakeholder são traduzidos pela navegação que ele usa (o menu do app), nunca pelos nomes internos de módulo/schema.
- Consertar defeito ou regressão comprovada não é decisão do usuário; não pergunte. Leve ao usuário só escolhas reais entre alternativas entregáveis ou trade-offs que só ele precifica.

**Dimensionamento e divisão do trabalho** (`content/skills/subagents/SKILL.md`)
- Alvo: cada subagente termina com ~33% da janela de contexto; modelos degradam a partir de 25–33%. Estime antes de spawnar: startup (prompt + skills, 20–60k), leitura (caracteres/4), iteração (logs de gate, diffs — "o assassino silencioso", pode passar de 100k), saída. Se a soma honesta passa muito do alvo, divida.
- Pequeno demais = fragmentação e costuras; grande demais = alucinação. Achar o tamanho e a fronteira da fatia "É o trabalho de design", não preâmbulo.
- Fatiamento híbrido: stages de build verticais e pequenos (uma fatia schema→negócio→rota→UI, provada por um smoke ao vivo); verificação (seeds, specs E2E, docs, QA de browser) agrupada em stages próprios porque tem custo fixo alto (servidor, banco semeado, browser, matriz responsiva). Docs é stage à parte.
- Uma fatia que muda um formato compartilhado (campo de schema, assinatura) herda toda a cascata de chamadores forçada pelo typecheck; dimensione isso ou corte numa costura estável de tipos.
- Antes de paralelizar lanes de dados, verifique a direção das FKs: uma lane cujos modelos têm FK obrigatória para linhas de outra lane é sequencial, por mais disjuntos que pareçam os arquivos.
- Trabalho dependente só começa quando a dependência aterrissou por completo; independentes lançam simultaneamente, nunca em ondas escalonadas (`content/doctrine/orchestration.md`, orq.).
- Calibração empírica: guardar num arquivo commitado o custo medido de contexto por tipo de trabalho, carimbado com a "era" da DoD; toda mudança que expande a DoD revisa as calibrações; contagem de itens é proxy ruim, o que prediz custo é número de superfícies distintas e se a verificação está dentro do stage (`content/skills/subagents/SKILL.md`, `workflow-content/calibrations.md`).
- Agente acima do limite: decida pelo que está à frente dele, não pelo número. Cauda mecânica (gates, commit, relatório) → deixa terminar; design/julgamento/debug à frente → para e continua com agente novo mesmo abaixo do limite. Árvore limpa e pushada estende a licença; árvore suja acima de ~450k revoga (`content/skills/subagents/SKILL.md`).
- Modelos por tipo de trabalho: o mais forte para orquestração, arquitetura, UX/UI, código mais difícil e QA final pré-merge; o intermediário para builds normais, correções, review com ≤5 subagentes e teste E2E manual via browser; o mais barato para reviews com fan-out ≥5. Esforço de raciocínio fixo por modelo e sempre explícito (`content/skills/subagents/SKILL.md`).

**Charters (o prompt de cada subagente)** — checklist extraído de orq. "Charters":
1. Todo documento referenciado por caminho absoluto e que vive no repositório (nada em `~`).
2. Spec/documento externo baixado cru (curl/browser, nunca fetch que resume) para um arquivo de cache, e esse caminho citado em todos os charters dependentes: todas as lanes constroem sobre os mesmos bytes.
3. Lanes paralelas que podem tocar o mesmo módulo: nomeie as lanes irmãs e dê a cada uma uma lista *do-not-touch*, inclusive por classe de artefato (specs E2E, artigos de docs, seções de seed pertencem ao stage de verificação). Arquivos compartilhados append-only (config de rotas, nav, seeds) resolvem conflito como keep-both. Antes de lançar, confira se o conserto de cada item não mora num arquivo de outra lane.
4. No máximo um agente que muta o repo por worktree; verificador sobre worktree alheio é read-only.
5. Identificadores de pool compartilhado (prefixos de seed, ids de fixture, portas, filas): o orquestrador publica uma tabela canônica de alocação em todos os charters antes do primeiro lançamento.
6. Constante computada compartilhada (hash de contrato): todos os charters declaram o protocolo "recomputar pelo mecanismo dono" no rebase; movimento inesperado é condição de parada.
7. Namespace de arquivos de rascunho por lane; proibido escrever no ledger do orquestrador (dar o caminho real do ledger).
8. Cláusula stop-on-contradiction: se a premissa factual do charter não sobrevive à verificação, o agente para o item e reporta com citações; "verificado, já correto, nada mudado" é resultado válido. Vale também para o formato de correção desenhado, âncoras `file:line` e nomes/slugs.
9. O charter nomeia as convenções de engenharia commitadas do repo (caminho absoluto) como obrigatórias e a implementação de referência, e, se mexe em testes, a doutrina de testes; o charter não prescreve mecânica de teste própria.
10. Charter com prova de mutação especifica o protocolo de restauração (byte-idêntico, `git status/diff`, limpar caches compilados).
11. Duas fontes de referência que discordam: o charter nomeia o conflito para adjudicação, nunca escolhe calado.
12. Listas deriváveis no charter (grafo de dependências, lista de consumidores) são exemplos; o agente re-deriva o conjunto completo das fontes primárias.
13. Agente que publica texto (issue, PR, review) não inclui dados pessoais de datasets de clientes; o orquestrador varre antes.
14. Builders nunca rodam gates longos; charter termina em commit e STOP.
15. O relatório final completo é a última mensagem; nunca terminar "aguardando CI"; nunca fazer polling de processo que ele mesmo pôs em background.
16. Escreva cada charter do zero; derivar colando pedaços de outro introduz erros silenciosos.
17. Preâmbulo compartilhado desde o primeiro rascunho: commit a cada marco, ler faixas de arquivo em vez de arquivos gerados inteiros.
18. Preâmbulo "classifique o estado do disco primeiro": ler `git status`/`git log`, classificar cada commit/arquivo sujo como feito/parcial/intocado, verificar em vez de refazer (agentes mortos são reiniciados no mesmo worktree).
19. Repasse achados exatamente no escopo em que foram medidos; marque extrapolações como suas.
20. Cheque as asserções de saída contra os próprios itens (um gate "arquivo sem diff" contra um item que edita esse arquivo).
21. Fatia que entrega rota/loader/form dirige essa superfície ao vivo pelo menos uma vez antes do handoff; a prova ao vivo é o último passo, depois do último commit.
22. Charter de cético/verificador tem duas rubricas: achado vale se (a) o cenário de falha concreto ocorre em runtime, ou (b) viola regra/doutrina codificada da casa.
23. Mensagem para agente vivo: pegar o id no ledger na hora do envio, nunca da memória.

**Verificar, nunca confiar** (orq. "Verify, never trust")
- Rodar os gates você mesmo antes de avançar um stage com base no auto-relato.
- "Todo X coberto/migrado" só é checável contra um denominador derivado ao vivo do sistema de registro (resolver de URL, schema, censo do repo), nunca contra o plano que produziu o trabalho; prefira um gate que recalcula e falha em drift.
- Reconciliar números exatamente: baseline + delta computado = medido, idêntico em duas execuções.
- Reconciliar o charter item a item contra o diff: cada item termina implementado, verificado-já-correto ou pulado explicitamente. Idem: cada decisão adjudicada aparece em exatamente um charter.
- Tarefa só está "lançada" quando o id retornado pela ferramenta está no ledger.
- Nunca bloquear esperando subagente em foreground; lançar em background e agir na notificação.
- Review/QA com zero achados só é passe limpo se todos os agentes completaram (erro, execução rápida demais ou contagem errada de agentes = rodada quebrada).
- Afirmações de "único consumidor", "fora de escopo/invasivo demais", citações em corpo de PR: são fatos, verificar com grep/leitura antes de aceitar.
- Nunca concluir ausência a partir de busca truncada (`grep | head`).
- As edições do próprio orquestrador em artefatos auditados recebem a mesma re-verificação adversarial que diffs de builders.
- Investigação feita a partir de um achado tende a confirmá-lo: antes de alarmar o usuário, encomende uma segunda perspectiva com outro enquadramento.
- Relato de builder que "verificou" UI simulando requests (FormData forjado) é afirmação não verificada; despache um testador de interação real.

**Baseline e integridade** (`content/doctrine/orchestration.md`)
- Antes da primeira lane, rodar os gates completos na base limpa e registrar os números. Se a baseline se perde, para tudo e restaura. Um guard que não enxerga o que diz proteger, ou um buraco de cobertura que a suíte não percebe, conta como perda de baseline mesmo com CI verde, e é corrigido na hora, nunca virando issue.

**Achados fora de escopo e backlog** (orq. item 85)
- Uma lane reporta achados fora de escopo com evidência e não os corrige inline; todo achado recebe disposição imediata; correção fora de escopo roda num passe próprio.
- Issue no GitHub só para: decisão que o usuário precisa tomar, trabalho bloqueado por outro, ou investigação de causa desconhecida que alguém vai de fato rodar. Nunca como depósito de ideias.
- Antes de adiar algo "até o evento X", verificar que X não depende do próprio item.

**Ledger e compactação**
- Ledger = cabeça de DIRETIVAS VIGENTES (sempre atual) + log cronológico. Uma única cabeça viva; cabeças antigas vão para arquivo de arquivo morto. Registrar lançamentos com ids, lanes com commits-base, veredictos com evidência. Reground lendo cabeça e cauda, com leituras limitadas (orq. "Ledger discipline").
- Nunca confiar no contexto compactado; reground no ledger e nas fontes reais (código, PRs); onde discordam, as fontes vencem (`content/doctrine/orchestration.md`, `content/skills/reground/SKILL.md`).
- Ordem de autoridade quando em dúvida: fontes primárias (git, arquivos, spec) > skills vivas > notas do ledger/memória compactada (orq.).
- Manter o ledger sempre atual porque o usuário pode compactar a qualquer momento; nunca pedir compactação (`content/doctrine/orchestration.md`, `content/skills/prepare-for-compaction/SKILL.md`).
- Após compactação no meio de um goal, reler o texto integral do goal; ele é a autoridade acima do corpo do PR e do ledger (`content/doctrine/goals-common.md`).
- Ao concluir um esforço longo, externalizar o registro durável (decisões, divergências, auditorias) em issue ou corpo de PR antes de limpar o scratchpad (orq.).

**Recuperação após interrupção** (orq. "Recovery")
- Passo 0: enumerar positivamente o que está vivo (lista de tarefas, `ps`, logs crescendo). Declarar morto algo vivo e relançar no mesmo worktree corrompe os dois.
- Worktree limpo → relançar o charter sem mudanças; sujo → agente de continuação que primeiro classifica o estado e para quando o restante listado acabar.
- Antes de escrever continuação, auditar o remoto (`git ls-remote`, `gh pr list --head`): o agente morto pode ter terminado.
- Agentes que morrem instantaneamente com zero ferramentas = incidente do provedor; backoff (10, depois 30 min) e relançar uma lane de sonda antes do resto (`content/skills/subagents/SKILL.md`).

**Processos e higiene**
- Todo processo de mais de um turno (dev server, worker) roda como tarefa background própria; nunca `&` dentro de outro shell. Nunca matar por padrão (`pkill -f`): só por PID exato depois de listar (`content/doctrine/orchestration.md`, orq. "Browser and process hygiene").
- Sessões de browser são fechadas e a ausência de processos é verificada por listagem, não pelo relato do agente. Gate que fica flaky durante trabalho de browser é suspeito de vazamento antes de bug de produto.

**Shipping de uma lane** (orq. "Shipping and merging a lane")
- PR abre em draft quando os gates rápidos passam (CI sobrepõe verificação local) e só vira "ready" após: afirmações verificadas, gates completos verdes, review adversarial contra o draft, e decisão do orquestrador sobre cada achado confirmado. Diff pequeno não é isento.
- Prever a superfície de conflito antes do rebase (interseção dos arquivos da lane com o que a main ganhou). Rebase sem conflito numa interseção não-vazia não prova correção: re-derivar as afirmações da lane contra a main pós-merge.
- Após rebase de patch aprovado, checar identidade do patch. Rebase e gates pós-rebase como passos separados.
- Dois PRs com migrations: o segundo re-sequencia a sua e regenera tipos derivados de um banco migrado do zero.
- Lane que muda copy visível: grep em `tests/` pelas palavras aposentadas antes do push. Lane que muda semântica de produto: grep no repo inteiro por prosa descrevendo o comportamento antigo (tooltips, empty states, emails).
- Nunca encadear merge com teardown de branch/worktree; confirmar merge com leitura nova, depois limpar.
- `gh run watch --exit-status` já retornou 0 em execuções falhas: o veredito é sempre uma leitura direta nova de `gh pr checks` depois do watch. PR com zero checks após alguns minutos = conflito com a base (sem merge commit, sem CI).
- Flake exige evidência positiva (specs falhando disjuntos entre runs, passam no mesmo tree, diff não alcança o caminho), reruns limitados a dois antes de investigar.
- Correções num branch revisado entram no próprio branch; nunca "fast-follow PR" depois do merge.

**Modos e comandos do usuário**
- `/quick`: DoD reduzida só quando o usuário invoca; nunca auto-selecionada nem sugerida. Desqualificam: rota nova, tabela/migration, permissão nova, superfície nova. Se a tarefa cresce, avisar e voltar à DoD completa (`content/skills/quick/SKILL.md`).
- `/goal`: com usuário ausente, perguntar via questionário (única forma que pausa o goal-checker); com usuário presente, conversa normal. Ao cumprir o goal, rodar self-improvement uma vez sobre o esforço todo. Propor goals de continuação com texto pronto (< 4.000 caracteres) (`content/doctrine/goals-common.md`).
- Falar com o usuário: uma pergunta por mensagem, sempre com recomendação, apresentar antes de perguntar, linguagem simples, pergunta do usuário não é autorização para trabalhar (`content/doctrine/talking-with-user.md`, já lido).
- Sincronizar uma feature branch longa com a main é uma lane revisada com quatro obrigações: delta de regras nos dois sentidos, delta de capacidades (paridade ou fora de escopo com justificativa), DoD combinada completa, e renovação de evidências (`content/skills/main-sync/SKILL.md`, `sync-merge-commit.md`, `sync-squash.md`).

**Shell e CI** (`content/doctrine/tooling.md`)
- Todo comando começa com `cd` explícito para o diretório alvo.
- Quando o resultado importa, capture o log inteiro (`cmd > file 2>&1; echo "exit=$?"`) e leia o arquivo; o status de uma tarefa background nunca é o veredito, a linha `exit=` do log é.
- Loops de polling exigem evidência positiva de "condição atingida", não "contagem zero" (que também ocorre quando o comando falhou).
- Responder no idioma do usuário; editar no idioma do arquivo.
- Referências de outras organizações compartilhadas pelo usuário nunca aparecem em nada visível no repo.

### 1.2 product-owner

**Shaping em vez de backlog** (`content/skills/shaping/SKILL.md`, já lido; resumo do que interessa ao PO)
- Um humano sempre traz o candidato; o PO nunca ranqueia uma pilha de ideias ("bets, not backlogs").
- O frame responde três coisas: (1) o momento de dificuldade como uma história específica, de uma pessoa, com palavras dela; (2) as quatro perguntas: como fazem hoje, quando isso não funciona, o que tentam fazer quando falha, como saberão que o novo jeito é melhor (este último é o teste de aceite do projeto inteiro); (3) o imperativo de negócio (dinheiro, buzz, moral ou tempo) e por que agora. Ferramentas opcionais: as quatro forças (push/pull vs ansiedade/hábito) e "big hire vs little hires" (quem compra uma vez vs quem precisa escolher usar todo dia).
- Projetos tão grandes quanto a compreensão permite; sem appetite. Dois documentos cujos builds brigariam pelo mesmo terreno são um projeto só (time bomb externa). Todo rabbit hole (time bomb interna) nomeado no documento vem com a solução.
- Forma no nível certo de abstração (wireframe é concreto demais, palavras são abstratas demais): elementos, breadboards, fat marker sketches, lo-fi de propósito; percorrer a história do frame "em câmera lenta" pela solução; listar no-gos.
- O documento é instrumento de feedback: um operador não-técnico precisa ler inteiro sem travar. Detalhes técnicos atrás de toggle, ancorados ao elemento que definem.
- O goal é uma "chave de ignição" fina: frase-missão, primeira instrução = ler o documento inteiro, critérios de aceite (teste de resultado, walkthrough reproduzido no produto, auditoria final seção a seção), só restrições que só o goal carrega. Menos de 4.000 caracteres.
- Fechamento do shaping: auditoria por lentes (afirmações sobre o sistema vs código, consistência de fórmulas, decisões presentes, citações verbatim) e rodadas de "compreensão do builder": um leitor novo diz se conseguiria desenhar a implementação; achados só de regra de negócio faltante/ambígua, com pesos blocker/guess/note; relatório limpo é válido.

**Registros de demanda** (`content/skills/requests-from-meetings/SKILL.md`)
- Pedidos são registros, não compromissos; todo documento diz isso.
- Três rótulos por entrada, cada um provável pelas citações: *Explicit request* (alguém pediu com essas palavras), *Observed pain point* (atrito sem pedido), *Current workflow to replicate* (prática de hoje demonstrada, no indicativo; condicional "se tivesse", "poderia" é imaginação, não workflow).
- Rede larga: completude vence arrumação; cada entrada tem timestamps, quem pediu, contexto e o que estava na tela; citações verbatim no idioma original + tradução, nunca parafrasear o pedido.
- `stakeholders.md` descreve todo mundo que aparece; falante desconhecido → perguntar ao usuário antes de finalizar; registrar incerteza honestamente.
- Auditoria "varredura cega de completude": um leitor com contexto novo monta seu próprio inventário direto das transcrições antes de abrir o registro pronto, e diffa nos dois sentidos.
- Invocação sem argumentos: listar reuniões pendentes e responder com texto de `/goal` pronto, sem começar a trabalhar.

**Release e fechamento de ciclo com os stakeholders** (`content/skills/release/SKILL.md`, `release/deployed-product.md`)
- Notas de release curadas em ordem: abertura em linguagem de produto; uma seção por projeto de shaping com link para o documento; "Requests from meetings" resolvidos com link para a entrada; resto agrupado por tema (nunca lista plana de PRs). Toda frase rastreável a um PR mergeado.
- No release, julgar toda entrada de reunião ainda sem selo e carimbar "Released · vN" quando o release plausivelmente atende o pedido (padrão leniente: selo a mais custa nada, selo faltando esconde trabalho entregue).

**Demo para stakeholders** (`content/skills/demo-videos/SKILL.md`)
- Escopo do demo é o que foi entregue (PRs mergeados), não o que o documento propôs; a diferença é narrada ("o documento pedia X, não construímos, e o motivo").
- Com pedido vago, entrevistar até fechar: o que está no escopo e fora, quem assiste, o momento de dificuldade nas palavras deles, o gesto que o resolve, o que mudou, o que está cru, que feedback ajudaria.
- Todo vídeo termina nomeando as 2–3 decisões que só uma pessoa pode tomar (`closingAsk`), nunca "me diga o que achou".

**Outros**
- Propor proativamente um goal com texto pronto quando identificar um corpo coerente de trabalho de continuação (`content/doctrine/goals-common.md`).
- No design, listar para o usuário tudo que o build não consegue exercitar sem algo que só ele fornece (orq.).

### 1.3 ux-ui-designer

**Doutrina de design system** (`content/skills/design-system/SKILL.md`). O design system é um conjunto de padrões, não uma biblioteca de componentes: "When a screen disagrees with these guidelines, the screen is wrong." Regras transferíveis (os nomes de classe são daisyUI/Tailwind, ver seção 2):
- Tom: ferramenta calma e profissional; elevação discreta; um destaque por vez; todo estado é honesto (botão desabilitado diz por quê, registro bloqueado mostra o motivo, a UI nunca afirma o que o servidor não confirmou).
- Tokens: toda cor/raio/elevação vem de token; todo par de cores sólidas passa WCAG AA; data viz tem rampa própria derivada da marca e o chrome nunca a usa; uma receita única de superfície elevada.
- Tipografia em 5 níveis fixos (título de página único, título de overlay, seção, título de card, rótulo de grupo); sem h6; números que alinham verticalmente são tabulares; tipo "display" só em páginas de marketing.
- Vocabulário de status fechado em exatamente quatro idiomas (badge de SLA, badge colorido por estado, ponto + badge, callout/alert); nunca inventar um quinto, nunca glifos de texto nem palavras de status coloridas; status apresenta estado derivado pelo servidor.
- Verbos padronizados: CTA de cabeçalho "Novo"; títulos de modal "Novo X"/"Editar X"; submit "Criar"/"Salvar"/"Adicionar"; concluir etapa "Concluir".
- Ação destrutiva: excluir uma entidade com identidade própria exige o diálogo de confirmação compartilhado; remover associação/config trivialmente recriável é instantâneo com UI otimista. Atos que exigem justificativa (pular, faltar, encerrar) usam o mesmo diálogo com campo de motivo obrigatório.
- Overlays: modal para criar/editar e pickers; larguras em três níveis por conteúdo; nada de botões na linha do título; ação primária no rodapé. Drawer de rota para fluxos operacionais; fluxo aberto num drawer continua em drawer.
- Idioma de edição: in-place (campo escalar frequente, blur-commit + "Salvo HH:MM"; grade editável totalmente otimista, erro ancorado na célula, nunca toast, nunca descartar o digitado); overlay para grupos multi-campo validados juntos; rota própria para tarefas com ciclo de vida; nunca in-place para atos destrutivos.
- Idioma de feedback: otimista para alternâncias reversíveis e frequentes; navegação + flash quando o ato muda o contexto ou o servidor calcula o resultado; quando um otimista que falha em silêncio pode levar a uma decisão com consequência, prefira ida e volta ao servidor.
- "Sem escritas silenciosas": toda mutação reconhece na própria tela; erros ancorados no controle, não só num flash global.
- Superfícies de monitoramento ganham painéis laterais não bloqueantes (a página continua viva); superfícies de tarefa ganham drawers.
- Links de remediação entre telas carregam `return-to` validado (mesma origem); nada de teletransporte sem volta.
- Rodapé de ação fixo para telas-folha operacionais, que precisa desviar do dock mobile.
- Cânone responsivo: 360×740, 375×667, 768×1024, 1024×768, 1280×800, 1440×900, e zoom 150% emulado (240×493, 250×445, 512×683, 683×512). Regras: `scrollWidth === innerWidth` exato; menus presos na tela; tabelas largas rolam só no próprio container; nada escondido no mobile que o desktop mostra; listas de dados viram cards abaixo de `sm`, exceto grades editáveis; barras quebram em linhas projetadas (âncora numa linha, todos os controles pares juntos na outra); nada de informação só em hover/tooltip no toque; nomes quebram em fronteira de palavra; inputs com 16px (sem auto-zoom do iOS); formulário usável com ~55% da altura do celular (teclado aberto); controles só-ícone com nome acessível.
- Impressão: a página se imprime (nunca rota paralela de impressão); controles/ajuda somem no papel; a face impressa de um editor é igual à do visualizador.
- Movimento com tempos canônicos (push iOS 400ms, Android 300ms, web 150ms cross-fade; modal entra 200ms, sai 150ms), tudo desligado em `prefers-reduced-motion`; feedback tátil no toque.
- Navegação: grupos de sidebar filtrados por permissão (grupo vazio some); o dock mobile é uma regra, não uma fatia; índice de seção redireciona ao primeiro item permitido; breadcrumbs só a partir de 3 níveis.
- Copy: idioma e locale do produto; um termo de domínio tem um nome só; pluralização correta ("1 produto", "3 produtos", nunca "produto(s)"); status descreve estado, não dá ordens; mensagens de validação na língua do usuário ("Escolha um funcionário"), nunca "Invalid UUID".
- "O que NÃO copiar": variantes de biblioteca que o app deliberadamente não usa; ausência no código é decisão, não descuido.

**Critérios de pronto para UI**
- Tarefa não está pronta sem teste ponta a ponta no browser com screenshots, validando design além de função; se a mudança toca uma família de implementações paralelas, exercitar todos os membros (`content/doctrine/dod/browser.md`, `content/doctrine/browser-verification.md`).
- Barra responsiva em toda superfície alterada, verificada com screenshots revisados como imagens: "a numeric probe passing does not close the criterion" (`content/doctrine/dod/responsive.md`).
- Barra de qualidade: UX/UI "beautifully simple" e fiel ao design system; nunca comprometer para economizar tempo ou tokens (`content/doctrine/quality-bar-web.md`).
- UX/UI de padrão novo é trabalho de invenção e roda no modelo mais forte (`content/skills/subagents/SKILL.md`).

### 1.4 backend-architect

**Modelagem de banco** (`content/skills/database-design/SKILL.md` e as duas variantes `append-only.md` / `mutable-when-not-derivable.md`)
- Dois tipos de tabela: *identidade* (id, createdAt, FKs de posse que nunca mudam) e *evento* (tudo que acontece à entidade; cada linha é um fato imutável).
- Uma tabela de evento por preocupação coesa: campos que mudam juntos numa ação do usuário compartilham tabela; "revision" guarda snapshot completo (não diff); mudanças acionadas separadamente têm tabela estreita própria (`product_archivals`, `order_approvals`). Nem por campo, nem entidade inteira.
- Criar = transação que insere identidade + primeira linha de cada evento relevante (nenhuma coluna precisa ser nula "esperando dado").
- Nomes: identidade no plural (`products`); evento `<entidade>_<ação-no-passado-plural>`.
- Transições de mão única = uma tabela (existência da linha é o estado); alternâncias reversíveis = par de tabelas (o evento mais recente vence).
- Estado atual derivado na consulta: último evento vence (DISTINCT ON + desempate por id), existência (EXISTS), agregados de movimentos (saldo nunca armazenado), status por cadeia de existência (sucesso/falha/pendente). Índice `(parentId, createdAt desc)` em toda tabela de evento.
- Famílias que misturam deltas e "set absoluto" (contagem de estoque): todos os escritores pegam o mesmo advisory lock; `createdAt` default `clock_timestamp()` (não `now()`, congelado no BEGIN); comparação estrita.
- Disciplina de locks: chaves de lock disjuntas não guardam nada; nunca chamar função que abre transação própria de dentro de transação com lock (deadlock). Nem toda corrida check-then-act precisa de conserto: faça a análise de dano primeiro.
- Sempre `timestamptz`; zero colunas nulas (dado que chega depois vira tabela de evento; atributo opcional = tabela com 0..n linhas); sem `updatedAt`; sem colunas deriváveis (status que acompanha um evento é o evento); sem unique na FK de tabela de evento; sem defaults desnecessários (o gerador de tipos torna o campo opcional e perde segurança); guardar localizadores completos de recursos externos (bucket + key, file id + folder id).
- Migrations autocontidas: nunca importam código da aplicação; duplicar a lógica dentro da migration.
- Performance: derivar primeiro; escalar só com gargalo medido, na ordem EXPLAIN/índices → particionamento → camada de views materializadas só-leitura. Nunca gravar valor derivado de volta no schema pela aplicação ("um cache numa tabela do app é uma coluna mutável com passos extras").
- Duas posturas configuráveis: 100% append-only (só INSERT; exclusão é evento; migration nunca reescreve histórico) ou "mutável quando não derivável" (update em lugar permitido se o valor não é inferível de eventos; sem `ON DELETE CASCADE`, deletes explícitos em transação).

**Organização do código de domínio**
- `business/`: o código mais valioso; sobrevive a troca de framework. Não importa roteador nem helpers de framework (exceto wrappers finos de job e paginação). Arquivos nomeados pelo domínio, não pelo provedor (`projects.server.ts`, não `gemini.server.ts`); exceção: primitivos de infraestrutura genéricos (`s3.server.ts`). Coesão total por arquivo; sem imports circulares entre domínios (preferência: fundir, cópia privada, extrair só se 3+ usam). Um único arquivo-ponte (auth) pode tocar o framework (`content/skills/business-folder/SKILL.md`).
- Lógica de seed promovida para produção é re-derivada com invariantes de produção: atalhos de seed (conceder todas as permissões) viram escalonamento de privilégio (`content/skills/business-folder/SKILL.md`).
- `framework/`: zero lógica do app, extraível como pacote; imports só em uma direção; configuração específica entra por factory (`content/skills/framework-folder/SKILL.md`).

**Autorização em camadas** (`content/skills/authorization/SKILL.md`)
- Componentes não autorizam (confiam nos dados do loader); loaders/actions obtêm contexto por getters que redirecionam; funções de negócio validam contexto por schema e lançam erro. Hierarquia de schemas de contexto (anônimo → usuário → empresa → admin); abstrações de papel pequenas e amplas.
- Todo id estrangeiro aceito como input numa escrita é um checagem de tenancy (em creates também).
- Rotas só-de-ação autorizam no topo, antes de qualquer leitura por parâmetro (diferença de comportamento vaza informação).

**Jobs em background** (`content/skills/background-jobs/SKILL.md`)
- Nomes começam com verbo; todo job registrado numa lista única; payload mínimo (só ids).
- Idempotência como primeiro passo: derivar "já feito" do próprio banco pelos ids do payload.
- Caminho de sucesso numa transação; falha registrada fora da transação (com o passo que falhou) e o erro sempre relançado (o runner só re-tenta o que lança).
- Criar registros e enfileirar o filho só depois do commit.
- Fan-out: cron descobre trabalho, cria registros, enfileira filhos.

**Variáveis de ambiente** (`content/skills/env-vars/SKILL.md`)
- Validar todas no boot e sair com código 1 listando todas as faltantes/inválidas (senão vira indisponibilidade em vez de deploy falho).
- Variável nova chega a todos os ambientes que sobem o servidor antes do código que a exige: `.env`, `.env.test`, CI (valores placeholder para serviços não exercitados) e o host de produção.

**Superfície de máquina (API para agentes)** (`content/skills/mcp-server/SKILL.md`, `content/doctrine/dod/machine-parity.md`)
- Paridade de capacidades: a API de máquina nunca serve mais nem menos que o app serve ao mesmo usuário, julgada por adequação de resultado, não por existência de endpoint.
- "A única regra": cada ferramenta é uma chamada a uma função de negócio passando o contexto real; nenhuma autorização mora na camada da API. Se a ferramenta precisa decidir algo que a função não decide, a decisão vai para a camada de negócio.
- Reusar o schema de input da "porta" que a rota realmente usa (a versão estreitada), não a função crua mais larga.
- Toda capacidade nova ou alterada estende a superfície de máquina no mesmo PR; exceções só por critério, listadas num registro com justificativa de uma linha; um teste de paridade no CI força isso.
- Na fronteira JSON: datas como strings ISO; booleanos aceitando `true` nativo e `'true'` de formulário.
- Job enfileirado não é capacidade; a ação do usuário que enfileira é.
- Arquivos nunca atravessam a API como bytes: leitura via URL assinada gerada dentro da função de negócio; escrita via URL de upload curta com ContentType e ContentLength assinados e as mesmas restrições do upload do browser.

**Outros transferíveis**
- Datas formatadas no banco/servidor, nunca no componente; comparações temporais no SQL; nunca `AT TIME ZONE` em coluna `date`; testes com o dia exato dos dois lados de uma fronteira de fuso (`content/skills/formatting-datetimes/SKILL.md`).
- Minimizar round-trips (returning, subqueries, CTEs); ordenação exibida com desempate estável e humano antes do id; identificadores ≤ 63 bytes verificados por teste; provar o `down()` contra dados "sujos"; nunca mesclar à mão o arquivo de tipos gerado; em inserts idempotentes use unique na chave natural + "do nothing" (`content/skills/kysely/SKILL.md`).
- Coding style: sem compatibilidade retroativa a menos que 100% necessária (`content/doctrine/coding-style.md`).

### 1.5 frontend-architect

- **Rotas determinísticas para UI otimista**: cada request declara o estado final desejado (endpoints separados de adicionar/remover, ou um endpoint por item com payload declarativo), nunca "toggle"; o estado otimista deriva dos requests em voo (`content/skills/optimistic-ui/SKILL.md`).
- **Disciplina de estado**: o roteador é dono do ciclo de vida dos requests; estado de componente (`useState/useRef/useContext`) só para UI (menu aberto, flag de edição). Disparar requests de `useEffect`, manter mapa próprio de pendentes ou revalidar à mão é reimplementar o roteador e está errado "mesmo quando funciona". Não serializar escritas para defender contra corrida de ordem; a revalidação reconcilia (`content/skills/optimistic-ui/SKILL.md`).
- **Chaves de linhas editadas in-place**: chavear pela identidade estável que a rota de escrita endereça (ordem de exibição, URL de escrita, id da identidade raiz), nunca por id re-cunhado por revisão nem campo mutável; teste de controle negativo que revalida com ids novos e verifica que o input focado mantém texto e cursor (`content/skills/optimistic-ui/SKILL.md`).
- **Descoberta de rotas preguiçosa**: nunca mandar o manifesto inteiro para fechar um canto raro (`content/skills/optimistic-ui/SKILL.md`, orq.).
- **Rotas aninhadas**: loaders pai e filho rodam em paralelo, o layout não protege os filhos; toda rota folha autoriza sozinha. Loader que redireciona roda a mesma checagem do layout antes (evita corrida de redirects). Itens de menu numa constante compartilhada usada também pelo redirect do índice. ErrorBoundary só em rotas de página (não em layouts, drawers/modais ou rotas só-de-ação). `<title>` só na rota de conteúdo mais externa (`content/skills/nested-routes/SKILL.md`).
- **Tipos**: confiar na inferência; sem tipo de retorno em funções (salvo implementação de interface); anotar só coleções vazias, mapas indexados dinamicamente, defaults `{}`/`[]`; tipos derivados de schema (`z.infer`) e dos tipos gerados da rota, não importados do servidor; `as` nunca para silenciar erro (`content/skills/type-safety/SKILL.md`).
- **Datas**: nada de `toLocale*` em componentes (mismatch de hidratação SSR); strings já formatadas vêm do servidor (`content/skills/formatting-datetimes/SKILL.md`).
- **Formulários**: campos array submetidos como `campo[]` repetido (senão vem string com vírgulas ou escalar com uma entrada); erros de validação de arrays vêm aninhados por posição; todo erro de validação precisa de path de campo, senão não aparece (`content/skills/composable-functions/SKILL.md`).
- **Anatomia de página e prefetch**: página de lista (título + CTA à direita, coleção ou empty state, paginação, outlet para overlays); página de detalhe com um único cluster de ações; prefetch "viewport" em nav persistente, "intent" em links proeminentes, nunca em links de ação (`content/skills/design-system/SKILL.md`).
- **Ícones**: uma biblioteca só, sem SVGs à mão (`content/skills/design-system/SKILL.md`).
- **Fonte**: self-hosted e com versão fixa, com fallback de métricas equivalentes; nunca carregar de host externo (`content/skills/design-system/SKILL.md`).

### 1.6 implementador

**Estilo de código** (`content/doctrine/coding-style.md`, `content/doctrine/quality-bar-*.md`, `content/doctrine/dod/comments.md`)
- Sem compatibilidade retroativa a menos que 100% necessária.
- Sem comentários, salvo operação incrivelmente complexa; remover comentários sobrando antes de terminar (critério de DoD).
- Sem abreviações em nomes, inclusive SQL.
- Evitar abstrações apressadas: repetir até a abstração certa emergir; extrair para arquivo novo só se compartilhado por mais de um arquivo.
- Convenções do repo (linter, nomes, idioma) são lei local.
- Código "obra de arte", o mais simples possível, com linguagem de domínio certa; nunca comprometer para economizar tempo/tokens.

**Bugs**: TDD vermelho → verde → refatorar (`content/doctrine/fixing-bugs.md`).

**Regras de subagente builder** (`content/doctrine/orchestration.md`, orq. "Charters", `workflow-content/orchestration.md`)
- Executar direto; nunca spawnar, abrir PR ou mergear sem ordem explícita.
- Primeiro passo: classificar o estado do disco (git status/log; feito/parcial/intocado).
- Ler as convenções commitadas antes de codar e tratá-las como obrigatórias.
- Stop-on-contradiction: premissa falsa → parar o item e reportar com citações; desvio do design com citações é obediência, não desobediência.
- Commit a cada marco; ler faixas de arquivos, não arquivos gerados inteiros.
- Só checagens rápidas locais (lint, typecheck, testes do módulo); terminar em commit (+push) e parar; relatório completo como última mensagem.
- Commits de follow-up em vez de `--amend`/force-push; push sempre com refspec explícito (`git push origin HEAD:<branch>`).
- Achados fora de escopo: reportar com repro, nunca corrigir inline.
- Rota/loader/form entregue é dirigido ao vivo pelo menos uma vez, como último passo depois do último commit.
- Antes de afirmar "único consumidor", grep no repo inteiro, `tests/` incluído.
- Mudou copy visível: grep em `tests/` pelas palavras antigas. Mudou semântica: grep por prosa antiga no repo todo.

**Worktrees** (`content/skills/worktrees/SKILL.md`, `content/doctrine/checkouts-worktrees.md`, `workflow-content/worktrees.md`)
- Checkout principal fica sempre na branch padrão; trabalho só em worktrees. Antes de qualquer trabalho (até leitura/auditoria), `git fetch` + fast-forward; checkout sujo ou divergente → parar e reportar.
- Worktree novo não tem dependências: instalar antes do primeiro gate.
- Depois de mover a base de um worktree: reinstalar dependências e recriar/migrar/re-semear bancos antes de confiar em qualquer coisa.
- Nunca rodar a suíte E2E e uma sessão de browser ao mesmo tempo na mesma lane (disputam a porta).
- Porta ocupada: nunca matar o listener (pode ser de outra lane).
- Teardown sempre fora do worktree removido, nunca encadeado com `;` atrás de um pré-requisito, com timeout generoso.
- Worktree entregue ao usuário para teste manual passa a ser do usuário: só mexer no que foi delegado; qualquer mudança de estado do banco além da rotina pede permissão.

**Shell** (`content/doctrine/tooling.md`): `cd` explícito em todo comando; nada de construções específicas de shell; capturar log inteiro e ler `exit=`.

**Verificação da própria obra**: testar ponta a ponta no browser toda mudança com efeito visível (`content/doctrine/browser-verification.md`); prova de escrita é o POST + a linha no banco, nunca uma screenshot (`content/skills/agent-browser/SKILL.md`).

**Copiar verbatim, editar depois**: ao trazer conteúdo de uma fonte, copiar com `cp`, verificar com `diff` que é idêntico e só então editar; LLMs alteram conteúdo ao reescrever (`workflow-content/doctrine.md`).

### 1.7 security-auditor

- **Tenancy por id**: todo id de entidade estrangeira aceito como input (em creates também) é verificado contra a empresa atual antes do uso; id inexistente vira erro de input amigável, não 500 de FK. Overrides de valores derivados pelo servidor (preço digitado) mudam só o valor; a entidade ainda passa por validação de tenancy, e cada caminho ganha um teste negativo cross-company (`content/skills/authorization/SKILL.md`).
- **Autorizar antes de qualquer leitura por parâmetro** em rotas só-de-ação: erro de validação que difere pelo estado do alvo vaza informação para qualquer tenant logado (`content/skills/authorization/SKILL.md`).
- **Gates por prefixo de URL** normalizam o path como o roteador (case-insensitive, percent-decode por segmento); testes adversariais com maiúsculas, `%2D` e barra final, e em escrita verificar 404 e nenhuma linha gravada (`content/skills/authorization/SKILL.md`).
- **Rotas de recurso** se protegem sozinhas (nada herdado de layout); consumidores programáticos recebem 401/403, navegações de browser recebem redirect com `return-to`. Validação no cliente é só UX; todo limite (tamanho, tipo) é re-imposto no servidor (`content/skills/authorization/SKILL.md`).
- **Toda rota folha autoriza** (loaders aninhados rodam em paralelo; layout não protege filhos) (`content/skills/nested-routes/SKILL.md`).
- **Testes de permissão**: nunca com contexto que concede tudo ou nada; conceder exatamente a permissão sob teste pelo fixture real, verificar que as irmãs ficam falsas, e provar trocando o literal da chave no getter (`content/skills/authorization/SKILL.md`).
- **Seeds em produção**: atalhos de seed reexecutados em produção viram escalonamento de privilégio (`content/skills/business-folder/SKILL.md`).
- **OAuth / tokens** (`content/skills/mcp-server/SKILL.md`): tudo hasheado em repouso (códigos, tokens, segredos) e texto claro devolvido uma vez; PKCE obrigatório só S256, comparação em tempo constante, e verificação antes de "queimar" o código; uso único por insert com unique; replay de código ou refresh reutilizado revoga a família inteira; audiência vinculada na emissão; um relógio só (o do banco); tokens vinculados à sessão (logout do browser mata os tokens); issuer independente do request.
- **Paridade como controle de segurança**: a API de máquina nunca expõe uma escolha que o app nega ao usuário (reusar a porta estreitada); gate de módulo contra a empresa resolvida do input, não a default (`content/skills/mcp-server/SKILL.md`).
- **Upload**: URL assinada com tipo e tamanho assinados; chave com escopo da empresa; re-checagem de pertencimento da chave na escrita (`content/skills/mcp-server/SKILL.md`).
- **Provar um guard sem enfraquecer o código commitado**: quando neutralizar o guard é recusado, injetar uma cópia em memória com o guard neutralizado e mostrar que ela deixa de negar, lado a lado com o original (`content/skills/mcp-server/SKILL.md`).
- **Critérios de triagem de achados** (`content/skills/pr-review/SKILL.md`): request forjado só conta quando o achado é sobre o que um atacante pode fazer; perguntar se o risco é novo em relação ao que o produto já aceita; estabelecer proveniência (introduzido pelo diff ou pré-existente na base) lendo a base.
- **Nenhum diff é pequeno demais**: num fix de segurança de três linhas, a review quase pulada achou uma quarta vulnerabilidade da mesma classe (orq. "Shipping").
- **Segredos e dados**: nunca publicar dados pessoais de datasets de clientes em issues/PRs (orq.); arquivos de estado de sessão do browser salvos com caminho absoluto no scratchpad, nunca relativo (já caíram dentro do repo com cookies) (`content/skills/agent-browser/SKILL.md`); frames/screenshots cortados abaixo do chrome do navegador (favoritos e URLs vivas) (`content/skills/requests-from-meetings/SKILL.md`); publish de pacote nunca do CI, sem token no CI, OTP do usuário como gate (`content/skills/release/published-package.md`); referências de outras organizações nunca aparecem no repo (`content/doctrine/tooling.md`).
- **Env**: validar no boot e falhar alto (`content/skills/env-vars/SKILL.md`).
- **Trilha de auditoria de graça**: schema append-only é a própria trilha e permite reconstruir qualquer estado passado (`content/skills/database-design/append-only.md`).

### 1.8 test-automator

**Doutrina geral** (`content/skills/testing/SKILL.md`, `testing/full.md`, `testing/pointer.md`, `content/doctrine/dod/coverage.md`, `dod/full-suite-ci.md`, `dod/gates.md`, `dod/demo-seed.md`)
- Suíte E2E completa roda só no CI do PR, nunca localmente (vale para todo agente; nenhum charter pode exigir). Localmente, só os specs relacionados pelo raio de impacto da mudança; mudança no seed ou no runner = suíte inteira.
- Ler sempre a linha de resumo do runner ("No tests found" = filtro errado).
- Nova superfície e o spec que a alcança entram na mesma mudança. Cobertura medida por tráfego real (rotas alcançadas nos logs da execução E2E), não por porcentagem de linhas. Registro de superfícies não alcançadas só encolhe; exceções exigem justificativa de uma linha ("ainda sem spec" nunca é justificativa). O gate falha também quando uma entrada do registro foi alcançada (catraca) e só é aplicado em execução não filtrada.
- Toda superfície de produto nova ou alterada entrega sua seção de seed de demo e entrada no manifesto; seed de um tiro só, falha alto se o banco não está vazio, sem script de reset.
- Um teste verde não prova nada até ser visto vermelho pelo motivo certo. Sem red-first natural, prova de mutação: backup com `cp`, neutralizar exatamente o comportamento, rodar o teste específico e ver falhar com a mensagem esperada, restaurar e verificar a restauração.
- Sinais de falso verde: valor esperado coincide com o comportamento bugado antigo; caminho stubado acima da mudança; asserção de erro satisfeita por outro erro; prop de coleção sempre vazia nos fixtures.
- Concorrência: nunca heurística de timer; sinal determinístico (ex.: esperar o waiter no lock específico).
- Reconciliação de gates: registrar contagens antes, calcular o esperado, rodar duas vezes; divergência é sinal, nunca ruído.
- Nunca mascarar flake com espera, retry ou asserção enfraquecida; flake é bug de produto provável. Falha com cara de contenção (conexões esgotadas, timeouts) roda sozinha antes de ser tratada como defeito.

**Testes unitários**
- Testar a API exposta (entradas/saídas), não detalhes de implementação; consultas por role/acessibilidade; não testar schemas de validação; não exportar helpers internos só para teste.
- Um `describe` por sujeito com o nome dele; nomes descritivos; nada de "additional tests".
- Asserções específicas no erro (tipo/mensagem), não só `success === false`; asserção de ausência por regex/texto único e provada por mutação.
- Fixtures de verdade externa: cada valor cita sua origem num campo de dado; divergência fixture × produto é achado de produto, nunca editar o fixture; desvio deliberado é afirmado como fórmula.
- Banco: nunca limpar; inserir com ids aleatórios (`randomUUID`) e consultar por eles, o que permite paralelismo; nunca agregados sem escopo; ids de fixture gerados (UUID digitado falha validação); infraestrutura preguiçosa inicializada no setup global.
- "Unhandled errors" depois de todos passarem = trabalho sobrevivendo ao arquivo de teste; corrigir na origem, reproduzir com workers acima do número de cores.
- Testes que dependem de env fixam o env (stub no beforeEach, unstub no afterEach).
- Pipeline contra banco descartável criado por execução, rodando os comandos reais de migrate/seed via shell.

**Testes E2E**
- Um `test()` por arquivo; nome do arquivo é a frase do comportamento em kebab-case (`recebimento-reagenda-entrega-para-horario-livre.spec.ts`); qualquer número de asserções.
- Spec nunca toca o banco nem lê env; tudo vem dos fixtures do seed e da baseURL.
- Selecionar como o usuário percebe (role, label, placeholder com a copy real); sem test ids; ausência = contagem 0; `exact: true` quando o nome é curto ou prefixo/sufixo de irmão; texto visível com innerText quando há "gêmeos" ocultos.
- Asserções de strings que vieram dos fixtures, nunca reescritas no spec. Provar persistência por ida e volta (mutar, re-navegar, afirmar). Nunca afirmar contagem exata de listas compartilhadas; escopar pela linha do spec, filtrando por algo intrínseco (href com id).
- Nunca afirmar mensagens flash de uma vez só; afirmar URL de destino + estado re-navegado.
- Barra de retry-safety: o spec passa quando re-executado sobre o estado deixado por uma tentativa que morreu em qualquer linha. Padrões: prólogo convergente (levar o mundo ao estado necessário) ou identidade única por tentativa (pool de seed indexado por repetição e retry). Provar com morte simulada + controle negativo. Tornar uma operação irreversível obriga mover todos os specs que a executam para pools na mesma mudança.
- O que esperar em superfícies "raciais por design": hidratação do roteador antes do primeiro clique; inputs com debounce (afirmar a URL com o termo antes do conteúdo); fluxos síncronos esperam a resposta POST exata; `toPass` com reload só para consistência eventual por design, com justificativa de uma linha; após ação que redireciona, afirmar a URL antes de clicar.
- Relógio: mundo semeado ancorado numa data móvel calculada uma vez em SQL; nada de `Date.now()` em seeds nem data absoluta em spec; limites de dia no fuso do negócio; histórico semeado numa "escada" de um segundo terminando ontem; janelas derivadas dos dados, não do relógio de parede.
- Jobs com LLM: fabricar a saída no seed para caminhos de sucesso; nunca afirmar saída exata de modelo.
- Specs mobile só quando a jornada é genuinamente diferente no celular; afirmar navegação alcançável, conteúdo legível, ações tocáveis, sem scroll lateral; nunca pixels.
- Paridade de env: variável nova vai em `.env.test` e no bloco env do CI na mesma mudança.
- Diagnóstico de falha só no CI: medir antes de teorizar (traces do CI vs local); dois experimentos baratos (rerun no commit inalterado; duração do spec em runs verdes recentes subindo rumo ao limite = página cara, não aumentar orçamento); branch diagnóstica que despeja tabelas no log; diagnosticar a primeira falha em ordem de arquivo (a mais barulhenta costuma ser cascata).

**Seed de E2E**: um módulo por jornada; ordem de arquivo = ordem de dependência; namespaces de identificadores declarados e guardas que falham alto em sobreposição; escrever via funções de negócio reais (writes crus só para linhas-esqueleto); entidades dedicadas a cenários que mutam; tudo find-or-create convergente por chave natural estável; personas como sessões reais; sem estado de login padrão (`content/skills/testing/full.md`).

**Específicos por tipo**
- Jobs: testar o `run` diretamente; espiar `enqueue`; verificar que o erro é registrado e relançado (`content/skills/background-jobs/SKILL.md`).
- Permissões: conceder exatamente uma chave e provar por troca de literal (`content/skills/authorization/SKILL.md`).
- API de máquina: por domínio, visibilidade (escondido sem permissão/módulo), negação (mensagem idêntica ao app), caminho feliz grava a linha de evento esperada (`content/skills/mcp-server/SKILL.md`).
- Listas editáveis: controle negativo de revalidação com ids novos (`content/skills/optimistic-ui/SKILL.md`).
- Datas: dia exato dos dois lados de uma fronteira de fuso (`content/skills/formatting-datetimes/SKILL.md`).

**Browser automatizado** (`content/skills/agent-browser/SKILL.md`): uma sessão por lane, fechada antes de reportar; snapshot antes de agir; clique fora da área visível reporta sucesso sem agir, então rolar primeiro e verificar pelo efeito observável; `fill` não dispara eventos de debounce (usar digitação real); Enter para submeter é instável (clicar no botão); viewport é resetado a cada `open`; upload que "passa" pode não enviar nada; 404 pode ser escopo de conta errado, não rota quebrada; não editar arquivos com hot reload durante sessão.

### 1.9 code-reviewer

**O loop de review** (`content/skills/pr-review/SKILL.md`, `content/doctrine/dod/review-loop.md`)
- Roda contra o PR draft, não contra o diff solto: lê descrição e discussão junto com o diff. Commitar e abrir o draft antes, senão revisa a mudança errada. Não aceitar achados pelo valor de face; iterar até o dono estar satisfeito.
- Fase 0, coletar tudo: metadados, comentários, reviews e threads inline (com `--paginate`, senão só vêm 30 itens), checks, e o diff por último. Fetch com erro não é registro vazio. Destilar os *contratos governantes* (spec/goal, decisões de rodadas anteriores, regras de escopo) numa lista explícita.
- Fase 1, ler o diff pessoalmente antes de delegar (PR grande: ler o núcleo, módulos compartilhados, schema/contratos).
- Fase 2, zoom out (nunca delegado): o PR deveria existir? A abordagem cabe na arquitetura? Existe um design em que o problema desaparece? É bonito (linguagem de domínio, código que lê como prosa)? Um "não" muda o objetivo: veredito de direção com poucos achados decisivos.
- Profundidade: rápida (diff pequeno e limpo), padrão (todos os ângulos, todo candidato verificado), exaustiva (superfícies de alto risco; varredura extra).
- Fase 3, ângulos independentes, cada candidato com `file`, `line`, resumo e cenário de falha concreto: discussão existente (cada preocupação aberta vira candidato com o nome do autor); exatidão da descrição do PR; linha a linha (inclusive linhas inalteradas de funções tocadas); auditoria de comportamento removido (que invariante a linha removida garantia, onde é restabelecida); rastreio entre arquivos (chamadores e chamados); armadilhas da linguagem; wrappers/proxies; reuso/simplificação/eficiência; altitude (remendo em infraestrutura compartilhada = conserto raso); convenções (só com a regra exata citada e a linha exata que a quebra, sem preferências de estilo). Não deixar um ângulo suprimir outro.
- Fase 4, verificar cada candidato: CONFIRMED (entrada/estado que dispara e saída errada), PLAUSIBLE (mecanismo real, gatilho incerto; é o padrão para concorrência, nulos raros, off-by-one), REFUTED (só se construível pelo código). Não verificável → pergunta, não defeito. Regressão precisa de gatilho que um cliente real produza. O risco é novo? Estabelecer proveniência pela base (`git show <merge-base>:<file>`).
- Fase 5 (só exaustiva): varredura de lacunas por um revisor novo.
- Fase 6, adjudicar contra o registro de decisões (docs, docstrings, design doc, testes que fixam comportamento deliberado, mensagens de commit, goals) e contra a barra "não conserte o que não está quebrado": quem é prejudicado, com que frequência, quanto, e se o estado gatilho existe.
- Entrega: visão geral; avaliação macro; o que confere (créditos por nome); achados do mais grave ao menos, com `file:line`, veredito, proveniência, cenário, e classificação dentro do escopo vs real-mas-guardado; respostas às perguntas abertas; veredito.
- Re-review é review completa do PR como está, nunca só "os achados antigos foram corrigidos?".

**Postar review em PR de outra pessoa** (`content/skills/post-review/SKILL.md`)
- Achado com lugar no diff vira comentário inline naquela linha; o corpo carrega só veredito, motivo do bloqueio e o que foi verificado.
- Marcar **Blocking** com o que desbloqueia; o resto explicitamente não-bloqueante. Mudança de comportamento não documentada: "se intencional, documente na descrição".
- Resumo abre com o que está bom e foi verificado.
- Afirmação de código morto só com enumeração completa dos consumidores.
- Afirmação refutada depois: postar correção no próprio thread imediatamente.
- Nunca aprovar/pedir mudanças por iniciativa própria.
- Opcionalmente, PRs de follow-up implementando as sugestões, baseados no branch do PR revisado, um por sugestão independente, com "pode simplesmente fechar".
- Resolver threads próprios só quando verificou que foram atendidos.

**Consertar achados no próprio PR** (`content/skills/review-fixes/SKILL.md`)
- Critério de sucesso único: a próxima rodada de review volta limpa. Proíbe: decidir pelo usuário o que era dele, consertos com defeitos próprios, consertar o que não estava quebrado.
- Triagem: *defeitos certos* (uma resolução defensável, o raciocínio fecha a questão) entram direto; *adjudicáveis* (trade-off real, comportamento deliberado questionável, intenção de produto) vão ao usuário um por mensagem, com recomendação; decisões registradas verbatim no ledger; "deixar como está" geralmente gera documentação.
- Desenhar cada conserto antes: altitude, paridade entre superfícies irmãs, comportamento removido, afirmações do corpo do PR invalidadas, testes que fixam o comportamento antigo (reescritos, nunca apagados sem sucessor), DoD.
- Cada artefato de prosa compartilhado tem exatamente um escritor, nomeado em todo charter; o corpo do PR é do orquestrador.
- Saída: mapa achado → resolução e proposta de nova rodada de review.

**Outros pontos de review** (orq.)
- A review do orquestrador lê cada linha do diff contra a doutrina das superfícies tocadas, independente do que o corpo do PR destaca.
- Deduplicar achados antes de spawnar verificadores; zero achados só vale se todos os agentes completaram; lentes que discordam sobre o mesmo achado geralmente indicam sub-afirmações agrupadas (decidir cada uma).
- Achados de working tree numa revisão em fan-out são suspeitos (prova de mutação de um irmão vira defeito fantasma); verificar contra o commit.
- Corpo de PR: para leitor externo, sem vocabulário de orquestração, estado atual e não histórico; PR `chore/docs/test` que muda comportamento diz isso no título e lista as mudanças; cada mudança de comportamento começa pelo problema (o que quebrava, quando, com que consequência); contrastes "não mais/antes" só se a base tem o comportamento antigo.
- Sobras de comentários são critério de DoD (`content/doctrine/dod/comments.md`).

### 1.10 docs-writer

**Voz para páginas humanas** (`.claude/skills/docs-copywriting/SKILL.md` e `references/voice-guide.md`, fora de `content/`, mas é o guia de voz deles)
- Um dev compartilhando com um par: claro, caloroso, palavras ditas em voz alta. Títulos em sentence case. Problema antes da solução. Específico em vez de vago ("menos de um minuto", "sete comandos"). Definir termos de arte no primeiro uso. Nunca se gabar (sem benchmarks, cases, "quem usa").
- Tabela de tradução do "dialeto de IA" para linguagem humana (load-bearing → essencial; doctrine → regras; surface → tela; charter → instruções; adjudicate → decidir; artifact → arquivo/resultado etc.). Identificadores literais ficam como são.
- Anti-padrões: jargão corporativo (leverage, seamless, robust…), voz passiva onde uma pessoa age, hedging, prática em evolução ensinada como assentada (marcar o que ainda está mudando).
- Travessões com espaço, no máximo um ou dois por página. Checklist antes do merge.

**Prosa factual é verificada como código** (orq.)
- Antes de publicar, um passe adversarial tenta refutar cada afirmação contra a fonte. As mais perigosas são afirmações de censo/totalidade ("todas as N rotas", "todo chamador", "inalterado desde a main"): escreva o mecanismo + exemplos verificados; totalidade só para conjuntos pequenos que a própria prosa define.
- Escrever frases a partir da tela renderizada ou do número medido, nunca da intenção dos dados.
- Ao mudar semântica de produto, grep no repo por prosa antiga (helper text, tooltips, emails, docs).

**PRs e releases**
- Corpo de PR para leitor externo, estado atual, reescrito conforme o trabalho evolui; PR guarda-chuva só está pronto quando o corpo lê como coisa terminada (sem "Landed", sem links para sub-PRs internos) (orq.).
- Release: estudar cada PR do intervalo (corpo + diff suficiente), nunca notas a partir de títulos; toda frase rastreável a um PR; parte curada mais rica que a auto-gerada, que vai por último; para pacotes, seções Breaking (dependências primeiro) / New features / Bug fixes / What's changed + link de comparação (`content/skills/release/SKILL.md`, `deployed-product.md`, `published-package.md`).

**Escrever instruções para agentes** (`content/skills/skill-management/SKILL.md`, `content/skills/self-improvement/SKILL.md`) — útil também para quem escreve os prompts dos nossos agentes:
- Descrição = [o que faz] + [ações específicas] + "Use when" + [gatilhos]; terceira pessoa, imperativo; distinta das irmãs.
- Corpo enxuto (< ~5k palavras); detalhes em `references/`; informação vive em um lugar só.
- Toda instrução é declaração autônoma da política atual, nunca delta contra histórico ("antes X, agora Y").
- Palavras simples; se um colega leria frio e perguntaria o que significa, reescrever a partir do caso concreto.
- Para conjuntos que crescem, descrever o mecanismo e como enumerá-lo, não a lista.
- Uma lição mora em um arquivo só, onde o agente futuro vai procurar.

**Documentos de registro** (`content/skills/requests-from-meetings/SKILL.md`, `content/skills/demo-videos/SKILL.md`)
- Seção fixa "Como ler este registro" com checklist fechado que todo documento responde, inclusive com "nenhum" (senão o leitor não distingue item ausente de problema inexistente).
- Referência a outra entrada é sempre link.
- Vídeos de demo: voz de colega, nunca marketing (sem "seamless", "powerful", "intuitive"); o "porquê" é o do documento de shaping; admitir o que está cru; terminar pedindo as decisões que só uma pessoa pode tomar; nunca narrar o que não aparece na tela; usar os termos que o produto exibe; soletrar identificadores alfanuméricos. `SCOPE.md` e `DEMO-STATE.md` registram escopo e como reproduzir.

**Outros**
- Mudança só de docs tem caminho próprio na DoD: worktree sem provisionamento, gates rápidos, sem comentários, uma passada de review, PR com CI verde (`content/doctrine/dod/intro.md`).
- Copiar conteúdo de fonte com `cp` e verificar com `diff` antes de editar (`workflow-content/doctrine.md`).
- Idioma: responder no idioma do usuário, editar no idioma do arquivo (`content/doctrine/tooling.md`).
- Ao final de um esforço, externalizar decisões e divergências num artefato permanente (orq.).

### 1.11 notifier

O seasoned não tem agente de notificação; o conteúdo útil é *quando* o humano precisa ser acionado e *como* falar com ele.

**Os momentos que o usuário não pode perder** (`docs/running-a-session.md`, `content/doctrine/goals-common.md`)
- Contexto do orquestrador: passar de ~22% (hora de procurar momento para compactar, idealmente enquanto espera subagentes) e de ~33–36% (compactar já). É a única vigia que "não pode esperar".
- Limite de uso da assinatura se aproximando (trocar de conta em outra aba).
- Questionário esperando resposta (é o que pausa o goal-checker; pergunta em texto comum com usuário ausente se perde).
- Goal cumprido: hora de o usuário testar/assistir aos vídeos de demo; PRs de self-improvement em draft aguardando revisão dele.

**Outros eventos que são "ato do usuário" e merecem aviso**
- PR pronto para merge na branch padrão (merge é sempre do usuário) (`content/doctrine/orchestration.md`).
- Release preparado aguardando o `npm publish` com OTP do usuário; chaves de env/infra novas que o usuário precisa configurar antes do deploy (`content/skills/release/published-package.md`, `deployed-product.md`).
- Lista de costuras que exigem algo que só o usuário fornece (chave de API, conta paga), no momento do design (orq.).
- Branch com CI vermelho que ninguém leu (um branch ficou vermelho por duas horas e quatro pushes até o usuário notar) (orq.).
- Incidente do provedor com agentes morrendo instantaneamente (backoff em curso) (`content/skills/subagents/SKILL.md`).

**Regras para o conteúdo da mensagem**
- Linguagem simples, sem jargão interno nem apelidos inventados durante o trabalho; comportamento visível e o que está em jogo antes do mecanismo; uma pergunta por mensagem, com recomendação; apresentar a decisão antes de perguntar (`content/doctrine/talking-with-user.md`).
- Nunca anunciar "CI verde" com base no exit code de um watch; só após leitura direta dos checks (`content/doctrine/tooling.md`, orq.). Nunca anunciar "publicado" sem ler o registro (`workflow-content/release.md`).
- Sem dados pessoais de clientes, sem referências de outras organizações (orq., `content/doctrine/tooling.md`).
- Não interromper à toa: "um projeto bem moldado faz poucas perguntas; se o build está bombardeando o usuário, a lição é sobre o shaping" (`docs/running-a-session.md`).

---

## 2. Específico da stack deles

Só serve se adotarmos a mesma stack. Cada item com a ideia transferível.

| Item amarrado à stack | Onde | Ideia transferível |
|---|---|---|
| React Router v7 (loaders/actions, `act()`/`load()`, `href()`, `useFetchers`, `?respond-with-json`, `createRoutesStub`, `clientLoader`, `routeDiscovery`) | `optimistic-ui`, `nested-routes`, `authorization`, `testing/full.md` | O roteador/biblioteca de dados é dono do ciclo de vida dos requests; UI otimista deriva dos requests em voo para endpoints determinísticos. |
| Kysely + CamelCasePlugin, `distinctOn`, `.onConflict`, `$castTo`, `Generated<T>` | `kysely/*`, `database-design/*` | Manter lógica no SQL, minimizar round-trips, e evitar defaults que tornam campos opcionais nos tipos gerados. |
| composable-functions (`applySchema`, `withContext`, `InputError/ContextError`, `fromSuccess`) | `composable-functions`, `authorization` | Toda função de negócio valida input e contexto de autorização na borda, com erros tipados (input vs contexto). |
| remix-forms (`SchemaForm`, coerção de checkbox) | `composable-functions` | Formulários gerados do schema; todo erro de validação precisa de caminho de campo para aparecer. |
| Zod (`z.infer`, `z.iso.date`) | vários | Tipos derivados do schema, fonte única; mensagens de validação escritas para o usuário. |
| graphile-worker (`makeJob`, `makeCronJob`, `jobs.server.ts`, `run-worker.ts`) | `background-jobs` | Jobs idempotentes pelo banco, falha registrada fora da transação e relançada, enfileirar depois do commit. |
| `make-typed-env` + `string-ts` (duas instâncias de env) | `env-vars` | Env validado por schema no boot; framework e app com validações independentes. |
| Estrutura `app/business`, `app/framework`, `app/routes`, sufixos `.server/.common/.ui/.client` | `business-folder`, `framework-folder` | Domínio independente de framework; framework sem lógica do app; sufixos que dizem onde o código roda. |
| PostgreSQL específico (`pg_advisory_xact_lock`, `clock_timestamp()`, `to_char`, `DISTINCT ON`, limite de 63 bytes, `CREATE TYPE ... AS ENUM`) | `database-design`, `formatting-datetimes`, `kysely` | Ordem de commit via lock compartilhado; formatação de datas no banco; checar truncamento silencioso de identificadores. No Supabase isto vale direto (é Postgres). |
| daisyUI 5 + Tailwind (`btn xl:btn-sm`, `list-row`, `badge`, `alert-vertical`, classes v4 mortas), lucide-react, Radix Tooltip | `design-system` | Padrões fechados (status em 4 idiomas, verbos, tamanhos de botão por breakpoint) documentados como regra, não como biblioteca. |
| Vitest, MSW, jsdom, Testing Library (`cleanup`, `hydrateRoot`) | `testing/full.md` | Testes paralelos contra banco compartilhado com ids aleatórios; trabalho que sobrevive ao arquivo de teste é bug. |
| Playwright com harness próprio (um produto por worker, banco clonado por worker, `poolSlot`, `repeatEachIndex`) | `testing/full.md` | Isolamento por worker e retry-safety por prólogo convergente ou identidade por tentativa. |
| Gate de cobertura por log de rotas + `matchRoutes`; `seedCoverage`, `IDENTIFIER_LENGTH_AUDIT_SQL` exportados pelo pacote | `testing/full.md`, `kysely` | Cobertura medida de tráfego real contra um denominador derivado do sistema (config de rotas), com registro que só encolhe. |
| CLI `seasoned-skills` (`provision`, `teardown`, `sweep --browsers/--lane-processes`, `doctor`, `sync`), `watchdog.py` | `worktrees`, `subagents`, `seasoned-skills` | Provisionamento de lanes idempotente e centralizado (banco/porta/env por lane); limpeza só por PID exato; vigia automática de contexto. |
| agent-browser CLI (`snapshot -i`, refs `@e3`, `state save`) | `agent-browser` | Uma sessão de browser por lane, fechada e verificada; desconfiar de "sucesso" de clique e provar pelo efeito. Com Playwright MCP/Claude in Chrome os mesmos cuidados valem. |
| Claude Code `/goal`, questionário, ferramenta Workflow (`agent()`, `parallel()`, `pipeline()`, `journal.jsonl`), `SendMessage` | `orchestration`, `subagents`, `goals-common` | Loop autônomo até o objetivo com perguntas que pausam o loop; workflows paralelos com resultados lidos do objeto retornado, não da ordem do journal. |
| Modelos Fable/Opus/Sonnet e esforços `high`/`xhigh` | `subagents` | Níveis de modelo por tipo de julgamento; esforço sempre explícito. |
| Changesets + pnpm + npm OTP; GitHub Release que dispara deploy | `release/*`, `workflow-content/release.md` | Publish como ato final deliberado, verificado no registro, nunca a partir do CI. |
| whisper-cli (ggml-large-v3 com hash fixo), notas do Gemini, ffmpeg/ffprobe, PIL, `verify.py` | `requests-from-meetings` | Citações verificadas mecanicamente contra transcrição com hash; calibração de tempo confirmada por pixels. |
| Rig de vídeo de demo (Apple Silicon, narrador TTS local, screenplays em TypeScript) | `demo-videos` | Demo reproduzível a partir de roteiro versionado + seed, com auto-revisão (transcrição, frames, sync) como único gate. |
| Servidor MCP com OAuth 2.1 próprio (`app/mcp/*`, `parity.test.ts`, RFC 8414/9728) | `mcp-server` | Superfície para agentes com paridade garantida por teste de AST no CI. |
| S3 / Google Drive | `database-design`, `mcp-server` | Guardar localizador completo; bytes via URL assinada. |
| `.claude/skills`, geração por `sync`, arquivos gerados gitignorados | `seasoned-skills`, `_shared/*` | Doutrina versionada num pacote e regenerada; lições locais vão num arquivo de conteúdo do projeto, lições gerais viram issue no pacote. |

---

## 3. Conflitos

### 3.1 Com os agentes originais da Dev Squad (`referencia/dev-squad-original/`)

**tech-lead (00)**
- *Arquitetos separados vs design no topo.* O original delega arquitetura a `03_backend-architect` e `04_frontend-architect` e só "consolida". No seasoned, design e adjudicação são trabalho do orquestrador; um modelo intermediário pode rascunhar para o topo decidir, mas "never hand the stale design down" (orq., `subagents/SKILL.md`).
- *"Nunca implemente código"* vs edições pessoais permitidas quando são cirúrgicas de uma linha (`content/doctrine/orchestration.md`). Diferença pequena.
- *Sequência por story (security → test → review) com aprovação dos três fechando a sprint* vs PR draft cedo, verificação agrupada em stages próprios e review adversarial contra o draft, com o orquestrador decidindo cada achado; aprovação de agente nunca basta ("Do not take the review's findings at face value", `dod/review-loop.md`; "Work is never merged on a lower tier's word alone", `subagents/SKILL.md`).
- *"Decisões técnicas conservadoras quando houver dúvida"* vs "uma opção que dissolve o trade-off vence; status quo só quando nenhuma dissolve" (orq.).
- *Deploy/merge feitos pela squad* (o original notifica "Deploy realizado na Vercel" como evento automático) vs merge na default e publish são atos do usuário; deploy só quando o usuário pede release (`content/doctrine/orchestration.md`, `release/*`).
- *Sprints* vs goals contínuos por projeto moldado; não há cadência de sprint no seasoned.
- *Estado em `docs/sprint-status.md`, `docs/decisions.md`, `docs/blockers.md`* vs ledger no scratchpad + fontes primárias como verdade; após compactação, fontes reais vencem documentos (orq.). O corpo do PR descreve o estado atual; decisões duráveis vão para issue/PR ao final.
- *Interromper só em 4 casos, uma pergunta por bloqueio, com opções e recomendação*: compatível, mas o seasoned acrescenta que consertar defeito comprovado nunca é pergunta, que perguntas com usuário ausente vão por questionário, e que as costuras que exigem algo do usuário são listadas já no design.
- *`model: inherit` em todos* vs modelo e esforço escolhidos por tipo de trabalho (`subagents/SKILL.md`).
- *SDD (contexto, input, output, pronto, escopo negativo)*: compatível; o seasoned vai muito além (ver checklist de charters). Ponto de atrito: o original pede "forneça trechos relevantes do PRD"; o seasoned prefere caminhos absolutos para fontes versionadas e specs externas baixadas cruas para um cache compartilhado, para que todas as lanes leiam os mesmos bytes.

**product-owner (01)**
- *Backlog priorizado com fórmula (Valor + Urgência)/Esforço e plano de sprints* vs "Backlogs are a big weight we don't need to carry": o humano traz o candidato, o shaping nunca ranqueia ideias; issues nunca como depósito de ideias (`shaping/SKILL.md`, orq. item 85).
- *Stories pequenas cabendo na capacidade da sprint* vs projetos "tão grandes quanto a compreensão permite", sem appetite; dois projetos que disputam o mesmo terreno são fundidos (`shaping/SKILL.md`).
- *User stories Gherkin com valores concretos e critérios verificáveis por máquina* vs documento de shaping com história do momento de dificuldade, forma lo-fi, walkthrough e no-gos, com o teste de resultado como aceite; "wireframes are too concrete, words alone are too abstract". O seasoned não usa user stories.
- *"Nunca adicione escopo sem remover algo"* vs o seasoned não faz scope hammering para caber em appetite (mas no-gos são obrigatórios).

**ux-ui-designer (02)**
- *Spec de alta fidelidade de cada componente (todos os estados, tokens, px) antes de implementar, a partir do Figma* vs no shaping tudo é lo-fi de propósito ("high-fidelity design done early will blow up"); a fidelidade vem do design system como padrões fechados aplicados no build, e a verificação é por screenshots reais.
- *Erros como toast* (exemplos no 02 e 04) vs erros ancorados no controle; grade editável nunca usa toast; mensagens flash não são afirmadas em testes (`design-system`, `testing`).
- *"mobile (< 768px)" como breakpoint único descrito* vs matriz de 6 tamanhos + 4 emulações de zoom com critérios de jornada e `scrollWidth` exato (`dod/responsive.md`).
- *Nielsen/WCAG genéricos*: compatível; o seasoned acrescenta regras concretas (16px em inputs, nada só-hover, nome acessível + title).

**backend-architect (03)**
- *"Sempre considere escalabilidade horizontal", microsserviços, CQRS, Redis, Kafka* vs derivar primeiro e escalar só com gargalo medido; "Do not add this layer, plan for it, or design around it until the first two rungs are exhausted" (`database-design/SKILL.md`).
- *Schemas CRUD comuns*: o exemplo do original tem colunas opcionais (`phone`, `birth_date` nuláveis), unique retornando 409, e implícito `updated_at`/UPDATE/DELETE. O seasoned proíbe colunas nulas "zero exceptions", proíbe `updatedAt`, proíbe colunas deriváveis, proíbe unique na FK de tabela de evento, proíbe `ON DELETE CASCADE`, e na variante append-only proíbe UPDATE/DELETE.
- *API REST com contrato por endpoint* vs rotas do framework chamando funções de negócio; a API para máquinas é uma projeção fina das mesmas funções com paridade testada (`mcp-server`). Não é conflito de princípio (contrato explícito), mas de forma.
- *RLS do Supabase como mecanismo de autorização* vs autorização em três camadas no código (getters + schemas de contexto nas funções de negócio). Se usarmos Supabase, precisamos decidir: RLS como rede de segurança + validação de contexto na camada de negócio, ou só uma delas.

**frontend-architect (04)**
- *Escolher lib de estado (Redux/Zustand/Context) e hooks tipo `useAuth()` com estado local e fetch próprio* vs "o roteador é dono do ciclo de vida dos requests"; `useState/useEffect` disparando requests é "re-implementing the router, and it is wrong here even when it works" (`optimistic-ui/SKILL.md`). Quase todo `useContext` em componente de rota é cheiro.
- *Árvore de pastas por features/components/hooks* vs organização por domínio (`business/`) independente do framework, com `framework/` extraível.
- *"Minimize bundle size, questione cada dependência"*: compatível; o seasoned acrescenta descoberta de rotas preguiçosa como regra.

**security-auditor (05)**
- *"Nunca ignore um achado; em dúvida, eleve a severidade"* vs verificação rigorosa: achado REFUTED é descartado; regressão sem gatilho produzível por cliente real é refutada; perguntar se o risco é novo; "do-not-fix-what-is-not-broken"; nem toda corrida check-then-act precisa de conserto (`pr-review`, `database-design`). O seasoned é mais cético com achados; o original é mais alarmista. Ressalva: request forjado conta quando o achado é sobre o que um atacante pode fazer.
- *Saída JSON com "remediação em código" para cada item* vs achados com proveniência (introduzido vs pré-existente) e classificação dentro/fora do escopo do PR; fora de escopo não é corrigido inline.

**test-automator (06)**
- *"Um assert por teste sempre que possível"* vs um `test()` por arquivo E2E com qualquer número de asserções (`testing/full.md`).
- *Cobertura > 80% de linhas em código crítico* vs cobertura de rotas medida por tráfego real, com registro que só encolhe; o seasoned não fala em porcentagem de linhas.
- *Nomes `should_returnError_when_emailIsInvalid`* vs `describe` com o nome do sujeito e `it` descritivo; arquivos E2E com a frase do comportamento.
- *"Mocks apenas para dependências externas"*: compatível, com a regra adicional de nunca mockar o roteador e de testes unitários usarem o banco real com ids aleatórios.
- *Testes criados depois da implementação ("invoque APÓS implementação")* vs TDD para bugs e "a new surface and the spec that reaches it land in the same change".
- *Rodar suítes localmente e configurar CI* vs suíte E2E completa só no CI, nunca local.

**code-reviewer (07)**
- *`git diff` como ponto de partida* vs ler descrição, comentários, reviews e threads antes do diff; revisar o PR draft, não o diff solto.
- *SOLID/DRY* vs "Avoid Hasty Abstractions: it is OK to repeat things here and there until the right abstraction emerges" (`coding-style.md`).
- *Nits de estilo/preferência* vs convenções só com regra citada e linha exata; "no style preferences".
- *Aprovar/bloquear direto* vs nunca aprovar/pedir mudanças por iniciativa própria; o veredito passa por adjudicação contra o registro de decisões.

**docs-writer (08)**
- *JSDoc/TSDoc e comentários "onde necessário"* vs sem comentários salvo operação incrivelmente complexa, e comentários sobrando reprovam a DoD.
- *Docs com marcadores temporais (✅ Sprint 1, 🔲 Sprint 2) e changelog com "por que mudou"* vs prosa que declara só o estado atual ("current truth, never history"; git guarda a história). Changelog do pacote vem de Changesets.
- *`docs/sprint-status.md` como spec de retomada de sessão* vs ledger no scratchpad + reground nas fontes reais; documentos não substituem o código como verdade.
- *Nenhuma verificação da prosa* vs prosa factual verificada por passe adversarial de refutação.

**notifier (09)**
- *Notificar "feature aprovada", "deploy realizado"* pressupõe merge/deploy automáticos, o que o seasoned proíbe sem pedido do usuário.
- *Formato fixo com emojis e nome de projeto fixo ("Dermfy")* não conflita com o seasoned, mas o guia de voz deles evita jargão interno; mensagens devem estar em linguagem simples, com stakes antes do mecanismo.
- *Eventos escolhidos por marco de sprint* vs os momentos que realmente exigem o humano: contexto do orquestrador, limite de uso, questionário esperando, goal cumprido, ações reservadas ao usuário.

**Todos os originais: "Yowpi Brain"** (aprendizado durável vira PR no brain, nunca commit direto na main) é **compatível** com o self-improvement do seasoned (PR em draft que só o usuário marca como pronto e mergeia). O seasoned acrescenta a barra de codificação (durável, muda comportamento, vale os tokens), a preferência por eliminar a armadilha em código em vez de prosa, e a remoção de instruções velhas com o mesmo rigor da adição.

### 3.2 Com práticas comuns de mercado

- **Banco append-only sem UPDATE/DELETE, sem colunas nulas, sem `updatedAt`** (`database-design/append-only.md`): contraria o CRUD padrão e ORMs comuns. A variante "mutável quando não derivável" é o meio-termo que eles mesmos oferecem.
- **Sem comentários no código** (`coding-style.md`): contraria guias que pedem docstrings.
- **Sem compatibilidade retroativa por padrão** (`coding-style.md`).
- **Sem backlog e sem issues como depósito de ideias** (orq., `shaping`): contraria Scrum/Jira.
- **Suíte E2E completa nunca local** (`dod/full-suite-ci.md`).
- **Sem test ids em E2E; seleção por role e copy real** (`testing/full.md`): contraria a recomendação comum de `data-testid`.
- **Nunca matar processos por padrão (`pkill -f`)**, só PID exato (`content/doctrine/orchestration.md`).
- **Nunca `--amend`/force-push em charters** (restrição do classificador de permissões deles) (`workflow-content/orchestration.md`); o próprio `main-sync` permite rebase com `--force-with-lease` quando o repo usa merge commit, então isso é regra para subagentes, não absoluta.
- **Merge sempre pelo humano**, mesmo com CI verde e review aprovado (`content/doctrine/orchestration.md`): contraria auto-merge.
- **Datas formatadas no SQL** em vez de no cliente com Intl (`formatting-datetimes`).
- **Sem tipos de retorno explícitos em funções** (`type-safety`): contraria lint rules comuns (`explicit-function-return-type`).
- **Projetos grandes em vez de pequenos incrementos** (`shaping`): contraria o "fatie fino" do ágil tradicional (a fatia fina existe só no nível de build das lanes).

---

## 4. Cobertura (critério de pronto)

Todo arquivo de `content/doctrine/` e todo `content/skills/*/SKILL.md` foi lido. Onde cada um aparece:

| Arquivo | Seção(ões) |
|---|---|
| doctrine/browser-verification.md | 1.3, 1.6 |
| doctrine/checkouts-worktrees.md | 1.6 |
| doctrine/coding-style.md | 1.6, 1.4, 3 |
| doctrine/fixing-bugs.md | 1.6 |
| doctrine/goals-common.md | 1.1, 1.2, 1.11 |
| doctrine/goals-merges-off.md / goals-merges-on.md | 1.1 |
| doctrine/orchestration.md | 1.1, 1.6, 1.11 |
| doctrine/quality-bar-web.md / quality-bar-no-web.md | 1.3, 1.6 |
| doctrine/talking-with-user.md (já lido antes) | 1.1, 1.11 |
| doctrine/tooling.md | 1.1, 1.6, 1.10, 1.11 |
| doctrine/dod/intro.md | 1.10 |
| doctrine/dod/browser.md, dod/responsive.md | 1.3 |
| doctrine/dod/comments.md | 1.6, 1.9 |
| doctrine/dod/coverage.md, full-suite-ci.md, gates.md, demo-seed.md | 1.8 |
| doctrine/dod/machine-parity.md | 1.4 |
| doctrine/dod/review-loop.md | 1.9 |
| doctrine/dod/self-improvement.md | visão geral, 3.1 (Yowpi Brain) |
| skills/orchestration, subagents | 1.1 (e demais) |
| skills/quick, reground, prepare-for-compaction, main-sync (+ sync-*.md) | 1.1 |
| skills/shaping (já lido antes), requests-from-meetings, demo-videos, release (+ deployed-product, published-package) | 1.2, 1.10 |
| skills/design-system | 1.3, 1.5 |
| skills/database-design (+ append-only, mutable-when-not-derivable), business-folder, framework-folder, background-jobs, env-vars, mcp-server | 1.4 |
| skills/kysely (+ append-only, mutable-when-not-derivable), composable-functions | 1.4, 1.5, 2 |
| skills/optimistic-ui, nested-routes, type-safety, formatting-datetimes | 1.5 |
| skills/worktrees | 1.6 |
| skills/authorization | 1.4, 1.7 |
| skills/testing (SKILL, full.md, pointer.md) | 1.8 |
| skills/agent-browser | 1.6, 1.7, 1.8 |
| skills/pr-review, post-review, review-fixes | 1.9 |
| skills/self-improvement, skill-management | 1.10, 3.1 |
| skills/seasoned-skills | Seção 2. Quase irrelevante: trata de instalar/atualizar o pacote deles. Única ideia útil: nunca editar arquivo gerado, corrigir a entrada e regenerar; upgrade lendo as notas de migração. |
| skills/_shared/lessons.md, project-specifics-intro.md | Seção 2 (última linha). Irrelevantes como conteúdo: são trechos de template (onde lições do projeto moram; seção de especificidades do projeto sobrepõe o genérico). |

Também lidos: `docs/running-a-session.md` (1.1, 1.11), `workflow-content/*.md` (lições do próprio repositório deles; aproveitadas em 1.1, 1.6, 1.10, 1.11), `.claude/skills/docs-copywriting/` (1.10).

Não lidos de propósito: `content/corpus/` (material do livro Shape Up / demand-side sales, protegido por direitos autorais, só destilado), `content/skills/composable-functions/references/complete-docs.md` e `agent-browser/references/cli-reference.md` (referência de API/CLI, não método), `testing/references/examples.md` (exemplos de código da stack; só os títulos conferidos), `docs/reference/*` e `docs/adopting-the-workflow.md` (instalação do pacote; só a introdução conferida), e o que foi pedido para ignorar (`src/`, `tests/`, `runtime/`, variantes em `shaping/one-workflow/references/`).
