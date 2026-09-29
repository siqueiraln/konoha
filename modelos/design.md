# Modelo: manual de estilo do produto (`DESIGN.md`)

Arquivo do projeto: `DESIGN.md` na raiz. Todo agente que mexe em tela lê antes de começar. Quando a tela discorda do manual, a tela está errada.

Duas camadas:
- **Do produto:** cores, fontes, espaçamentos, tom. Cada produto tem a sua identidade.
- **Da empresa:** comportamentos (estados, verbos, erros, confirmações). Iguais em todo produto, copiados de `~/.claude/empresa-agentes/modelos/design.md` e só alterados com decisão do dono.

```markdown
# Manual de estilo: <produto>

## Visão geral
<Em 3 a 5 linhas: para quem é, que sensação a tela passa, o que ela nunca parece.
Anti-referências: produtos com que não queremos parecer.>

## Tokens
Fonte da verdade: `design/tokens.tokens.json` (formato Design Tokens 2025.10,
com tema claro e escuro). Aqui só o resumo e o uso.

| Token | Valor | Uso |
|-------|-------|-----|
| `color.primary` | #... | ação principal — no máximo uma por área da tela |
| ... | | |

## Cores
<Regras com nome. Todo par de texto e fundo passa WCAG 2.2 AA (4,5:1; 3:1 para texto grande e ícones).>

## Tipografia
<Níveis fixos (título da página, título de seção, título de card, corpo, legenda).
Corpo com no mínimo 16px; números que se comparam em coluna usam algarismos de largura igual.>

## Elevação
<Uma receita de superfície elevada (cartão, menu, modal). Sem sombras inventadas.>

## Componentes
Mapa do que já existe. Antes de criar, procure aqui.

| Componente | Onde está | Quando usar | Não usar para |
|------------|-----------|-------------|---------------|
| Tabela de dados | `src/components/...` | listas com mais de 5 colunas | ... |

Regra das 3 vezes: algo que aparece 3 vezes com o mesmo propósito vira componente
compartilhado e entra nesta tabela.

## Faça e não faça
<Regras com nome, no formato abaixo. Uma a três por assunto.>

---

## Regras da empresa (iguais em todo produto)

**A Regra do Erro no Lugar.** O erro aparece junto do campo ou do controle que falhou, dizendo o quê, por quê e como corrigir. Nunca só num aviso que some.

**A Regra da Tela Honesta.** A tela nunca afirma o que o servidor não confirmou. Botão desabilitado diz por quê. Toda gravação se mostra na tela ("Salvo às 14:32").

**A Regra dos Verbos.** Botão é verbo + objeto ("Criar lead", "Salvar proposta"), nunca "OK", "Sim" ou "Enviar" solto. Mesmos verbos em todo o produto: "Novo X" para abrir, "Criar" para gravar algo novo, "Salvar" para gravar mudança, "Excluir" para apagar.

**A Regra do Desfazer.** Ação reversível acontece na hora e oferece "Desfazer". Confirmação só para o que não volta, dizendo exatamente o que vai ser perdido.

**A Regra do Um Destaque.** No máximo uma ação principal por área da tela. Se tudo tem o mesmo peso, nada tem.

**A Regra do Termo Único.** Um conceito tem um nome só, o do `CONTEXT.md`. "Lead" não vira "contato" três telas depois.

**A Regra do Mesmo Jeito.** Ações parecidas funcionam igual em todo o produto: se editar um lead abre um painel lateral, editar uma empresa também abre.

**A Regra do Nada Escondido.** O que o computador mostra, o celular também mostra, de outro jeito. Nada de informação só ao passar o mouse.

**A Regra do Carregando.** Carregamento mostra o esqueleto da tela, não tela em branco nem só uma rodinha.

**A Regra do Primeiro Uso.** Nunca um painel em branco na primeira vez: exemplo ou uma ação clara para começar.

**A Regra Anti-IA.** Proibido: texto em degradê, borda colorida só de um lado, efeito de vidro, grade de cards todos iguais, número grande com métricas embaixo como enfeite, rótulo pequeno em maiúsculas acima de toda seção, numeração 01/02/03 decorativa, fundo creme ou areia, cinza claro sem contraste. Teste: alguém acostumado com Linear, Notion ou Stripe confiaria nesta tela?

**Tamanhos de tela verificados:** 360×740, 375×667, 768×1024, 1024×768, 1280×800, 1440×900, e zoom de 200%. Nenhum causa rolagem para os lados na página.
```
