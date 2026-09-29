# Pesquisa: UX/UI Designer

Material bruto para construir o agente. Nada aqui é o agente final.
Extração detalhada das skills: `pesquisa/03-ux-ui-skills-bruto.md`. Seasoned: `pesquisa/seasoned-skills.md` §1.3 e §3.1.

## 1. Diagnóstico do original (`referencia/dev-squad-original/02_ux-ui-designer.md`)

**Manter:**
- "Specs vagas são bugs": se o construtor precisa adivinhar um valor, a spec falhou.
- Tokens citados por nome **e** valor de referência.
- Comportamento escrito como sequência de eventos (clicou → carrega → deu certo / deu erro).
- Diferenças por tamanho de tela listadas, não "responsivo".
- Acessibilidade como requisito.

**Cortar:**
- Spec de alta fidelidade de **todo** componente antes de construir. Custa caro, envelhece rápido e repete o que o design system já decide.
- Erro em toast (aviso que some): o Seasoned e a impeccable mandam o erro junto do campo.
- Figma como fonte: o dono não usa, e agentes não enxergam Figma.
- WCAG 2.1: a versão vigente é a 2.2.

**Falta:**
- Um **design system do produto** como arquivo único que todos leem (padrões fechados, não só cores).
- **Verificação da tela pronta**: o original só especifica, nunca olha o resultado.
- Estados de tela completos: vazio (5 tipos), erro por causa, dados extremos.
- Texto da tela (microcopy) como parte do design.
- Anti-padrões de "cara de IA".
- Encaixe com o documento de projeto do PO, que já traz as telas em baixa fidelidade.

## 2. Das skills instaladas (resumo; detalhe no arquivo bruto)

### impeccable
- **Brief antes de construir**, com parada para aprovação: ação principal única da tela, todos os estados, faixas reais de dados (0, típico, 500 itens), textos, o que a tela **não** deve ser.
- **Estados:** 8 por elemento interativo (o esquecido é o foco pelo teclado); carregando com esqueleto da tela, não rodinha; vazio em 5 tipos (primeiro uso, limpo pelo usuário, busca sem resultado, sem permissão, erro); erro explicado pela causa (sem login, sem permissão, limite, falha nossa).
- **Dados extremos:** nome com 100+ caracteres, emoji, 1000+ itens, botão clicado 10 vezes, internet caindo, conta zerada.
- **Verificação com placar:** 10 heurísticas de Nielsen (0 a 4, total 40); auditoria em 5 dimensões (acessibilidade, desempenho, uso de tokens, tamanhos de tela, anti-padrões); severidade P0 a P3 ("o usuário abriria chamado por isso? P1").
- **Screenshot obrigatório, mas não basta.** "Screenshot que você não leu não conta." Não inventar defeito para parecer que iterou; detector sem achado não prova que está pronto.
- **"Cara de IA" proibida:** borda colorida só de um lado, texto em degradê, efeito de vidro, número grande com métricas embaixo, grade de cards iguais, rótulo pequeno em maiúsculas acima de toda seção, fundo creme, cinza claro "elegante" sem contraste. Teste: alguém acostumado com Linear, Notion ou Stripe confiaria nesta tela?
- **DESIGN.md para agentes:** tokens no topo em bloco estruturado, 6 seções fixas, regras com nome ("A Regra do X") com tom de proibição. Só vira componente o que se repete 3+ vezes com a mesma intenção.

### revenue-centric-design
- **Nunca tela vazia no primeiro uso:** dados de exemplo, uma ação clara, progresso que começa em 20%.
- **Atrito certo:** cortar o que só coleta dado; manter o passo em que o usuário diz o que veio fazer.
- **Hierarquia de decisão:** a tela responde "o que eu faço agora?"; número vermelho vem com o botão que corrige.
- **Textos:** botão é verbo + objeto (nunca "OK"); o botão principal diz o que acontece e quanto custa; erro diz o quê, por quê e como corrigir.
- **Opção já marcada** decide 60–80% das escolhas: escolher o padrão é decisão de design.
- A prova final é **comportamento real** (ativação, tempo até o primeiro valor), não a tela bonita. Isso é trabalho do Pesquisador no overclock.

## 3. Seasoned

- **O design system é um conjunto de padrões, não uma biblioteca.** "Quando a tela discorda do design system, a tela está errada."
- **Vocabulário fechado:** status em exatamente 4 formas; verbos padronizados ("Novo", "Criar", "Salvar"); quando usar modal, gaveta lateral ou página própria; quando editar no lugar.
- **Todo estado é honesto:** botão desabilitado diz por quê; a tela nunca afirma o que o servidor não confirmou; toda gravação se mostra na tela.
- **Ação destrutiva:** apagar algo importante pede confirmação; remover algo que se recria fácil é instantâneo. (A impeccable prefere "desfazer" a confirmar; ver conflitos.)
- **Tamanhos de tela fixos:** 6 tamanhos + zoom 150%; nada escondido no celular que o computador mostra; formulário usável com o teclado aberto; campos com fonte 16px.
- **Planejamento em baixa fidelidade de propósito;** a fidelidade vem do design system aplicado na construção, e a verificação é por screenshots reais em todos os tamanhos.
- **Padrão novo de tela é invenção** e roda no modelo mais forte.

## 4. Fontes externas (conferidas em 2026-09-26)

| Fonte | Ideia útil |
|---|---|
| **WCAG 2.2** (W3C) | Padrão vigente de acessibilidade. A 3.0 é rascunho (último em 10/09/2026), sem recomendação final antes de 2028. Quem cumpre 2.2 AA deve cumprir a maior parte do mínimo da 3.0. [w3.org/WAI/news/2026-09-10/wcag3](https://www.w3.org/WAI/news/2026-09-10/wcag3/) |
| **Design Tokens Format 2025.10** (W3C Community Group) | Primeira versão estável do formato de tokens (28/10/2025): um arquivo `.tokens.json` com temas (claro/escuro) que as ferramentas leem. [anúncio](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/) |
| Nielsen, **10 heurísticas** | Base do placar de verificação (já usada pela impeccable). |
| Steve Krug, *Não me faça pensar* | Teste do "porta-malas": em qualquer tela, o usuário sabe onde está, o que dá para fazer e como voltar. |
| Brad Frost, **Atomic Design** | Montar telas a partir de peças menores reaproveitadas; base da regra "3 repetições viram componente". |
| Adam Wathan e Steve Schoger, *Refactoring UI* | Hierarquia por peso e cor antes de tamanho; menos bordas, mais espaço. |

## 5. Convergências

1. **Estados são o design:** vazio, carregando, erro e dados extremos aparecem em todas as fontes; o original só listava estados visuais de botão.
2. **Padrões fechados e poucos:** Seasoned (vocabulário fechado), impeccable (DESIGN.md, 3 repetições), Atomic Design.
3. **Olhar o resultado:** Seasoned e impeccable exigem screenshot real lido; o original não verificava nada.
4. **Texto faz parte da tela:** verbos padronizados, erro com o que fazer, um termo por conceito (bate com o `CONTEXT.md` do PO).
5. **Erro junto do campo, não em aviso que some.**

## 6. Conflitos a decidir

1. **Fidelidade antes de construir.** Seasoned: baixa fidelidade sempre. Impeccable: pergunta a cada tarefa, e em telas importantes gera imagem do esboço, que vira contrato depois de aprovada. Revenue-centric: fluxo que decide conversão (primeiro uso, página de venda) precisa ser pensado em detalhe antes.
2. **Apagar: confirmar ou desfazer?** Seasoned confirma o que é importante; impeccable prefere desfazer. Proposta: desfazer quando a ação é reversível; confirmação só quando não é.
3. **Bonito x converte:** a impeccable proíbe o bloco de números grandes que a revenue-centric elogia em página de venda. Proposta: a regra de "cara de IA" vale para o produto; página de venda segue o que a pesquisa de conversão mostra.
4. **Design system igual para todo produto x identidade própria:** padrões de comportamento (estados, verbos, erros) são da empresa; cores, fontes e tom são de cada produto.

## 7. Esqueleto proposto

Três modos:
1. **Design system do produto:** cria ou atualiza o `DESIGN.md` (tokens no formato estável + regras com nome + padrões de comportamento da empresa). Uma vez por produto, depois só mudanças.
2. **Telas de um projeto:** a partir do documento do PO, detalha fluxo, estados, textos e dados extremos de cada tela, usando os padrões do DESIGN.md. Padrão novo é detalhado e marcado como invenção.
3. **Verificação da tela pronta:** screenshots em todos os tamanhos, lidos; placar de heurísticas e auditoria; achados com severidade. Não conserta, devolve para quem construiu.

### Dores do dono (2026-09-26) que o agente precisa resolver
- **Casos extremos que ninguém prevê**, mesmo com muitos testes: quem escreve o teste é a mesma cabeça que escreveu o código, com o mesmo ponto cego. Resposta: uma **lista de extremos da empresa**, aplicada mecanicamente a toda tela (não depende de prever), que **cresce a cada bug encontrado** em produção; e a verificação feita por outro agente, não por quem construiu.
- **O mesmo componente feito de jeitos diferentes em rotas diferentes:** cada agente começa sem memória e só lê o que está perto da tarefa. Resposta: antes de desenhar, **procurar o que já existe** (mapa de componentes no `DESIGN.md`, ou pesquisa "sistema atual" do Pesquisador); a verificação compara a tela com as **telas vizinhas** e aponta desvio como defeito ("componente próprio quando já existia um compartilhado"); regra das 3 repetições vira componente compartilhado.
- **Produto que já existe sem padrão** (ex.: o CRM): um modo de **extrair o padrão do que já existe**: mapear as variações do mesmo componente, escolher uma, escrever no `DESIGN.md`. As telas antigas se alinham aos poucos, sempre que forem mexidas.
