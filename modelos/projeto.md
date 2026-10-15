# Modelo: documento de projeto

Arquivo: `docs/projetos/<nome-do-projeto>/projeto.md`. Ordem das seções fixa. Partes 1 a 4 para o dono e o negócio, sem termo técnico; partes 5 e 6 para quem constrói. Só a verdade atual; o histórico fica no git.

```markdown
# <Nome do projeto>

> <Essência: uma frase que qualquer pessoa da empresa consegue repetir.>

**Status:** não construído | construído
**Tipo:** produto para vender | ferramenta de operação

---

## 1. O problema

### A história
<Uma pessoa, um momento, travando com o jeito atual. As palavras dela entre
aspas, com a fonte. Uma cena, não persona nem lista.>

### Como é feito hoje
<O jeito atual.>

### Onde o jeito de hoje falha
<Quando não funciona, e o que a pessoa tentava fazer nessa hora.>

### Como vamos saber que ficou melhor
<O teste de resultado, observável: comportamento, número ou tempo.>

### Por que agora
<A moeda (dinheiro, tempo, moral da equipe, visibilidade) e por que agora.>

## 2. A solução

<Linguagem simples, baixa fidelidade: as partes, como se ligam, o que entra e
o que fica de fora. Telas como lista de lugares e do que dá para fazer em cada um.>

## 3. A história recontada

<A mesma cena da parte 1, passo a passo, com a solução no lugar.>

1. <passo>
2. <passo>

**Final antigo:** <como a cena terminava>
**Final novo:** <como termina agora>

## 4. Armadilhas e fora de escopo

### Armadilhas
| Armadilha | Como está resolvida |
|-----------|---------------------|
| <onde o trabalho costuma afundar> | <a decisão que desarma> |

### Fora de escopo
- <o que este projeto deliberadamente não faz>

### Depois desta versão
- <o que foi cortado da primeira versão, com o motivo>

---

## 5. Parte técnica

### Termos
Conforme `CONTEXT.md`. <Só os termos que este projeto introduz ou muda.>

### Detalhes por parte da solução
Desenho técnico do Arquiteto em `docs/projetos/<nome>/tecnico.md`.
<Para cada parte da seção 2: regras exatas, dados, validações, integrações.
Ancorado na parte que define, nunca num bloco técnico solto.>

### Telas
Do designer em `docs/projetos/<nome>/telas.md` e, nas telas decisivas, esboços aprovados em `esbocos/`.

### Critérios de aceite
- **CA1**: Dado <estado com valores concretos>, quando <ação>, então <resultado observável>.
- **CA2**: ...

### Suposições deste projeto
Uma linha cada: `Supus: <o quê>, porque <motivo>`.

## 6. Objetivo (texto que inicia a construção)

> <Frase de missão = a essência.>
>
> 1. Leia `docs/projetos/<nome>/projeto.md` inteiro. Ele é a única fonte da verdade.
> 2. Aceite: o teste de resultado da parte 1 passa; a história recontada da parte 3
>    roda no produto pronto; todo critério CA provado (ao vivo; teste escrito só para
>    permissão entre empresas, data e fuso, dinheiro).
> 3. Ao terminar: audite a implementação contra o documento, parte por parte
>    (solução, armadilhas, fora de escopo, critérios). Corrija toda falta antes de
>    declarar pronto.
> 4. O fora de escopo é obrigatório.
> 5. Ao entregar, mude o Status do documento para "construído".
```
