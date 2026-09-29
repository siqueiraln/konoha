# Pesquisa: Product Owner

Material bruto para construir o agente. Nada aqui é o agente final.

## 1. Diagnóstico do original (`referencia/dev-squad-original/01_product-owner.md`)

**Manter:**
- Regras SDD de story: autocontida, critério verificável por máquina, escopo negativo, pré-condições com caminho, notas técnicas com referência exata.
- Exemplo ❌/✅ de critério de aceite (login OTP).
- Seção "Exemplos de Comportamento" (input concreto → output concreto, incluindo borda).

**Cortar:**
- Vocabulário de Scrum humano: cerimônias, capacidade em dias/pessoa, "escalar no mesmo dia", "manter stakeholders informados".
- Fórmula `(Valor + Urgência) / Esforço`: ignora o Risco que o próprio agente calcula e não considera dependência.

**Falta:**
- Linha de chegada antes do backlog (hoje ele gera backlog "completo" do PRD, sem corte).
- Glossário do domínio como artefato próprio.
- IDs nos critérios de aceite, para o Test Automator ligar teste a critério.
- Métrica de valor por épico (hoje só há critério técnico).
- O que fazer com lacunas do PRD (perguntar? assumir? registrar?).

## 2. Extraído das skills instaladas

### largada: o PM que subtrai
- **Linha de chegada:** a operação mínima que roda, o valor central entregue **uma vez, ponta a ponta**. É um resultado, não uma lista de features. Exemplo: "um afiliado recebe a oferta e o clique é rastreado".
- **Estado real:** medir, não supor. "Achado sem verificação não é estado; é palpite."
- **Lacuna = chegada − estado:** "o único backlog que importa".
- **Corte:** pergunta-mãe "necessário pra cruzar a linha, ou depois?". Na dúvida, é depois. O que foi cortado vai para a seção **"Depois do launch"** ("anti-inchaço com endereço").
- **Kill condition por item:** "pronto quando X; se travar em Y, para e reavalia". É o freio da superengenharia dentro da tarefa.
- **Portão:** nada é construído sem "pode ir".

### rumo: planejamento na névoa
- O destino pode ser uma **decisão a travar**, não só uma solução.
- **Fronteira:** só entra o que dá para decidir agora. Teste: "dá pra formular a pergunta com precisão agora?".
- **Quatro movimentos** para resolver incerteza: grilling (conversa), protótipo ("como parece/se comporta"), pesquisa (informação externa), tarefa (mundo real).
- **Checagem de não-quebrar:** dado gravado, regra com dono e fronteira externa não se decidem sozinhos; viram **decisão sinalizada** com o dono que falta decidir.
- **Índice, não depósito:** o documento linka e resume, não repete.

### grilling (mattpocock)
- Uma pergunta por vez, **cada uma com a resposta recomendada**.
- **Fato se busca, decisão se pergunta:** se dá para descobrir no ambiente, não pergunte.
- Percorre a árvore de decisões resolvendo dependências uma a uma.

### domain-modeling (mattpocock)
- `CONTEXT.md` = glossário e nada mais. Sem detalhe de implementação.
- Cada termo tem definição curta (1-2 frases, o que **é**, não o que faz) e `_Avoid_:` com os sinônimos proibidos.
- Termo resolvido é escrito **na hora**.
- Confrontar o usuário quando usa termo conflitante com o glossário ("conta" = Cliente ou Usuário?).
- ADR só quando as 3 condições valem: difícil de reverter, surpreendente sem contexto, fruto de trade-off real.

### brainstorming (superpowers)
- Avaliar escopo antes de detalhar: se o pedido tem subsistemas independentes, **decompor primeiro** em subprojetos, cada um com seu ciclo spec → plano → implementação.
- Propor 2-3 abordagens com trade-offs e recomendação.
- YAGNI implacável.
- **Autorrevisão da spec:** placeholders (TBD/TODO), contradição interna, escopo (cabe num plano só?), ambiguidade (dá pra ler de 2 jeitos? escolha um e explicite).

### revenue-centric-design (Richard @richardrx)
- **Filtro Canivete Suíço (2 camadas):**
  - Camada 1, merece existir? Precisa passar nos 4: carga cognitiva, especificidade para o ICP, custo operacional (manter/suportar/documentar), reforça a proposta central.
  - Camada 2, construir agora? Fácil de rejeitar × fácil de implementar (custo da versão que valida, não da versão sonhada).
  - "Toda feature que entra, fica. E cobra aluguel para sempre."
- **Priorização:** `(Novos Usuários + Nova Receita + Impacto) / Esforço`.
- **Swiss Knife Index:** features usadas por >40% dos ativos em 30 dias ÷ total de features. Abaixo de 0,3 = canivete desajeitado.
- **Ativação > cadastro:** cadastro → taxa de ativação; tempo de sessão → tempo até a primeira ação útil; tour completo → retenção D7. Medir **TTV** (time-to-value).
- **Aha moment empírico:** o que todo cliente que pagou fez na semana 1 e quem saiu não fez.
- Churn abaixo de 30 dias é problema de onboarding, não falta de feature.
- A/B test sem amostra suficiente não prova nada; sem volume, 5 boas entrevistas valem mais.

## 3. Fontes externas (clássicos de produto)

| Fonte | Ideia útil para o agente |
|---|---|
| Marty Cagan, *Inspired* | **4 riscos:** valor (vão querer?), usabilidade (vão conseguir usar?), viabilidade técnica (dá pra construir?), viabilidade de negócio (funciona para o negócio?). Discovery reduz risco antes da delivery. |
| Jeff Patton, *User Story Mapping* | Mapa da jornada do usuário (backbone) com fatias horizontais de release. A primeira fatia é o **walking skeleton**: o fluxo inteiro, raso, ponta a ponta. É a linha de chegada do largada em forma de mapa. |
| Bill Wake, **INVEST** | Story boa é Independente, Negociável, Valiosa, Estimável, Pequena (Small) e Testável. |
| Mike Cohn / Richard Lawrence, **SPIDR** | Padrões para quebrar story grande: Spike, Paths (caminhos alternativos), Interface, Data (subconjuntos de dados), Rules (regras de negócio). |
| Gojko Adzic, *Specification by Example* | Critério de aceite como **exemplos concretos** que viram teste executável. Base do Gherkin (Dan North, BDD). |
| Ryan Singer, *Shape Up* (Basecamp) | **Appetite** (quanto tempo vale gastar, não quanto vai levar), **rabbit holes** (riscos conhecidos, já neutralizados na spec), **no-gos** (fora de escopo explícito). |
| Teresa Torres, *Continuous Discovery Habits* | **Opportunity Solution Tree:** resultado desejado → oportunidades (dores) → soluções → experimentos. Evita pular direto para a solução. |
| Clayton Christensen / Bob Moesta, **JTBD** | Story ancorada no "trabalho" que o usuário contrata o produto para fazer, não na persona demográfica. |
| Intercom, **RICE** | Reach × Impact × Confidence / Effort. O fator **Confidence** penaliza o que é palpite. |

## 4. Convergências (onde várias fontes dizem a mesma coisa)

1. **Menor fatia ponta a ponta primeiro:** linha de chegada (largada) = walking skeleton (Patton) = appetite (Shape Up).
2. **Cortar é o trabalho:** corte (largada), Canivete Suíço (Richard), YAGNI (brainstorming), no-gos (Shape Up).
3. **Critério = exemplo concreto testável:** SDD original, Specification by Example, Gherkin.
4. **Incerteza se trata antes de construir:** 4 riscos (Cagan), névoa/fronteira (rumo), Confidence (RICE), rabbit holes (Shape Up).
5. **Valor se mede por comportamento, não por entrega:** ativação/TTV (Richard), resultado desejado (Torres).
6. **Uma linguagem só:** CONTEXT.md (domain-modeling), glossário vivo (docs-writer original).
