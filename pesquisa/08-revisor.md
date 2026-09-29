# Pesquisa: Revisor

Material bruto para construir o agente. Nada aqui é o agente final.

Papel (combinado com o dono em 2026-09-26): **lê o código, não roda o produto**. Pergunta "está feito do jeito certo e vai continuar funcionando quando alguém mexer depois?". Pega o que funciona hoje e passa em qualquer teste, mas está errado. É também o **último portão** antes do dono.

## 1. Diagnóstico do original (`07_code-reviewer.md`)

**Manter:** critica o código, não o autor; toda crítica com sugestão; reconhecer o que foi bem feito; bloqueio só com justificativa técnica, nunca preferência; convenções do projeto.

**Cortar:** SOLID/DRY como lista de princípios soltos (vira gosto pessoal); "sugestões" e "nits" em volume (ruído); avaliar só o `git diff` sem a spec.

**Falta:** conferir contra o desenho (`tecnico.md`, `telas.md`, documento de projeto); a pergunta "essa mudança devia existir?"; cenário concreto em cada achado; verificar achado antes de reportar; distinguir o que a mudança introduziu do que já existia; conferir os relatórios do Implementador, Security e Testes; o que fazer na segunda rodada.

## 2. Seasoned (o processo mais completo)

- **Coletar tudo antes:** descrição, discussão, relatórios, e as **regras que governam** a mudança (spec, decisões anteriores, escopo), numa lista explícita. O diff por último.
- **Ler o diff pessoalmente** antes de qualquer delegação.
- **Zoom out, nunca delegado:** a mudança devia existir? Cabe na arquitetura? Existe um desenho em que o problema desaparece? O código lê como prosa, na língua do domínio? Um "não" aqui muda o veredito inteiro: poucos achados decisivos de direção, não uma lista de detalhes.
- **Ângulos independentes:** linha a linha (inclusive linhas não alteradas das funções tocadas); **comportamento removido** (que garantia a linha apagada dava, e onde ela foi restabelecida); rastreio de quem chama e quem é chamado; reuso e simplificação; **altitude** (remendo em peça compartilhada é conserto raso); convenções só com a regra exata citada e a linha exata que a quebra.
- **Todo achado tem cenário concreto de falha** (entrada ou estado que dispara, e a saída errada). Verificação: CONFIRMADO (dá para construir o gatilho), PLAUSÍVEL (mecanismo real, gatilho incerto: concorrência, nulo raro), REFUTADO (descartado). Não verificável vira pergunta, não defeito.
- **Proveniência:** introduzido pela mudança ou já existia (ler a versão anterior).
- **"Não conserte o que não está quebrado":** quem é prejudicado, com que frequência, quanto, e se o estado que dispara existe. Comportamento deliberado registrado (decisão, teste que fixa, spec) não é defeito.
- **Segunda rodada é revisão completa** do estado atual, nunca só "os achados antigos foram corrigidos?".
- **Código morto** só com a lista completa de quem usava.
- **Consertos:** defeito certo (uma resolução defensável) entra direto; o que é escolha (troca real, intenção de produto) vai ao dono, um por vez, com recomendação.

## 3. Das skills instaladas

- **Dois eixos separados** (mattpocock `code-review`): **Padrões** (segue as regras do projeto?) e **Spec** (faz o que foi pedido?). Um código pode passar num e falhar no outro; reportar separado impede um de esconder o outro. O eixo Spec procura: pedido que falta ou está pela metade; **o que entrou sem ter sido pedido**; o que parece feito mas está errado. Cada achado cita a linha da spec.
- **Cheiros de código** (Fowler, *Refactoring* cap. 3), sempre como julgamento, nunca violação, e **as regras do projeto vencem**: nome misterioso, código duplicado, cirurgia espalhada (uma mudança lógica obriga editar muitos arquivos), generalidade especulativa (abstração para necessidade que a spec não tem), intermediário que só repassa, obsessão por tipos primitivos, o mesmo `switch` repetido.
- **Calibração** (superpowers `requesting-code-review`): nem tudo é crítico; elogio exato ajuda o autor a confiar no resto; desvio do plano é apontado para confirmar se foi de propósito; se o problema está no plano e não no código, dizer.

## 4. Fonte externa: Google Engineering Practices (conferido em 2026-09-26)

- **Padrão de aprovação:** aprovar quando a mudança "definitivamente melhora a saúde geral do código", mesmo sem ser perfeita. Não existe código perfeito, só melhor. [standard.html](https://google.github.io/eng-practices/review/reviewer/standard.html)
- **O que olhar:** desenho, funcionalidade, complexidade (entendido rápido?), **superengenharia** (resolver o problema de agora, não o especulado), testes, nomes, comentários (o porquê, não o quê), consistência, documentação atualizada, **cada linha**, o contexto em volta, e o que foi bem feito. [looking-for.html](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- **"Detalhe:"** como prefixo do que é opcional e não segura a aprovação.

## 5. Do caso do CRM (o que um revisor teria pego)

Coisas que funcionavam e passavam nos testes: estado da conversa gravado em 23 lugares da tela; contato criado por 5 caminhos; componentes falando direto com o banco (~45); função do banco com parâmetro novo deixando a antiga viva; conserto de segurança num lugar com a "irmã" aberta; guarda que nega por acidente; numeração de migration e de decisão duplicada.

## 6. Conflitos, resolvidos

1. **Lista de sugestões e detalhes (original) x só o que tem cenário (Seasoned).** Decidido: achado **bloqueante** precisa de cenário concreto ou de regra escrita violada (guias, `DESIGN.md`, convenções do projeto, `tecnico.md`). Detalhes opcionais no máximo 3, marcados como opcionais; o resto não se escreve.
2. **Aprovar só perfeito x aprovar se melhora.** Decidido: padrão do Google. Aprova quando melhora e não tem bloqueante; o opcional não segura.
3. **Revisor conserta?** Decidido: não. Devolve ao Implementador. Escolha que é do dono vai ao dono pelo Tech Lead.

## 7. Esqueleto proposto

Entrada: a fatia (ou o projeto inteiro) pronta, com os relatórios do Implementador, do Security e do Testes.

1. **Juntar as regras que governam:** documento de projeto, `tecnico.md`, `telas.md`, `DESIGN.md`, guias, convenções, ADRs.
2. **Zoom out:** devia existir? Cabe no desenho? Tem jeito mais simples?
3. **Eixo Spec:** item a item contra o desenho e as telas; o que falta; o que entrou sem pedir.
4. **Eixo Padrões:** caminho único de escrita, tela sem acesso direto ao banco, peça reinventada, convenções, cheiros, comportamento removido, altitude, cada linha.
5. **Os relatórios batem?** O relatório do Implementador bate com o diff; achados do Security e do Testes resolvidos ou recusados com motivo; todo critério de aceite com teste que já foi visto vermelho.
6. **Verificar cada achado** (confirmado / plausível / refutado; introduzido ou já existia).
7. **Veredito:** aprovado, aprovado com detalhes opcionais, ou devolvido.
