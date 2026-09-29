# Modelo: documento de projeto

Arquivo do projeto: `docs/projetos/<nome-do-projeto>/projeto.md`. Ordem das seções fixa.

O documento tem dois leitores. As partes 1 a 4 são para o **dono e as pessoas do negócio**: linguagem simples, sem termo técnico. Quem conhece a operação precisa conseguir ler do começo ao fim e dizer "não é assim que funciona aqui". As partes 5 e 6 são para **quem constrói**.

O documento diz só a verdade atual. O histórico fica no git.

```markdown
# <Nome do projeto>

> <Essência: uma frase que qualquer pessoa da empresa consegue repetir.>

**Status:** não construído | construído
**Tipo:** produto para vender | ferramenta de operação

---

## 1. O problema

### A história
<Uma pessoa, um momento, travando com o jeito atual. Com as palavras dela
quando existirem, entre aspas e com a fonte. Não é persona nem lista de
reclamações: é uma cena.>

### Como é feito hoje
<O jeito atual, sem a solução nova.>

### Onde o jeito de hoje falha
<Quando ele não funciona, e o que a pessoa estava tentando fazer nessa hora.>

### Como vamos saber que ficou melhor
<O teste de resultado. Algo observável: um comportamento, um número, um
tempo. Este é o teste de aprovação do projeto inteiro.>

### Por que agora
<O que o negócio ganha, em qual moeda: dinheiro, tempo, moral da equipe ou
visibilidade. E por que agora, não depois.>

## 2. A solução

<Em linguagem simples: as partes, como se ligam, o que entra e o que fica de
fora. Esboços em texto quando ajudarem (telas como lista de lugares e o
que dá para fazer em cada um). Baixa fidelidade de propósito: o leitor
precisa ver onde cabe a correção dele.>

## 3. A história recontada

<A mesma cena da parte 1, passo a passo, agora com a solução no lugar.>

1. <passo>
2. <passo>
...

**Final antigo:** <como a cena terminava>
**Final novo:** <como termina agora>

## 4. Armadilhas e fora de escopo

### Armadilhas
| Armadilha | Como está resolvida |
|-----------|---------------------|
| <parte onde o trabalho costuma afundar ou dar errado> | <a decisão que desarma> |

### Fora de escopo
- <o que este projeto deliberadamente não faz — ninguém faz escondido>

### Depois desta versão
- <o que foi cortado para a primeira versão, com o motivo; candidato ao overclock>

---

## 5. Parte técnica

### Termos
Conforme `CONTEXT.md`. <Só os termos que este projeto introduz ou muda.>

### Detalhes por parte da solução
Desenho técnico do Arquiteto em `docs/projetos/<nome>/tecnico.md`: costura (dados,
caminho único de escrita, matriz de permissões, efeitos, fatias) e o detalhe de cada parte.
<Para cada parte descrita na seção 2: regras de negócio exatas, dados que
guarda, validações, integrações, contratos já decididos. Ancorado na parte
que define, nunca num bloco técnico solto.>

### Telas
Detalhadas pelo designer em `docs/projetos/<nome>/telas.md` (fluxo, estados,
textos, casos extremos) e, nas telas decisivas, esboços aprovados em `esbocos/`.

### Critérios de aceite
Derivados da história recontada e do teste de resultado.
- **CA1** — Dado <estado com valores concretos>, quando <ação>, então <resultado observável>.
- **CA2** — ...

### Suposições deste projeto
Ver `docs/suposicoes.md`, entradas marcadas com este projeto.

## 6. Objetivo (texto que inicia a construção)

> <Frase de missão = a essência.>
>
> 1. Leia `docs/projetos/<nome>/projeto.md` inteiro. Ele é a única fonte da verdade.
> 2. Aceite: o teste de resultado da parte 1 passa; a história recontada da parte 3
>    roda no produto pronto; todos os critérios CA têm teste passando.
> 3. Ao terminar: audite a implementação contra o documento, parte por parte
>    (solução, armadilhas, fora de escopo, critérios). Corrija toda falta antes de
>    declarar pronto.
> 4. O fora de escopo é obrigatório.
> 5. Ao entregar, mude o Status do documento para "construído".
```
