# Lista de casos extremos da empresa

Vale para toda tela e todo teste. Ninguém precisa prever: a lista lembra.

**Como a lista cresce:** todo bug que escapou para o produto e não estava coberto aqui vira uma linha nova, com o caso que o revelou. Quem achou o bug escreve a linha (ou pede ao Tech Lead). Linha nunca sai da lista sem decisão do dono.

Formato de linha nova:
```
- [caso concreto] — o que a tela deve fazer — origem: [projeto, data, o que aconteceu]
```

---

## Dados

- **Lista vazia** (0 itens) — mostra o estado vazio certo (ver tipos abaixo), nunca uma tabela vazia sem explicação.
- **Um item só** — plural certo ("1 lead", não "1 leads"); layout não quebra.
- **Muitos itens** (1.000+) — a tela continua rápida; paginação ou carregamento aos poucos; nada trava.
- **Texto longo** (nome com 100+ caracteres, e-mail enorme, palavra sem espaço) — quebra ou corta com "…" e mostra o texto inteiro de outro jeito; não empurra a tela para os lados.
- **Emoji e acentos** (😀, "ção", "Ñ") — aparecem certos em todo lugar, inclusive em busca e ordenação.
- **Campo opcional em branco** — a tela não mostra "null", "undefined", "NaN" nem traço solto sem sentido.
- **Número zero, negativo e muito grande** (R$ 0,00, -5, R$ 1.000.000.000) — formatado certo, cabe no espaço.
- **Datas nas bordas** (virada de mês, de ano, fuso horário, 29/02) — mostra o dia certo para quem está vendo.

## Ações

- **Clique duplo ou repetido** (10 cliques no botão de salvar) — grava uma vez só; o botão mostra que está trabalhando.
- **Sair no meio** (fechar a aba, voltar, atualizar a página durante o preenchimento) — o que foi digitado não se perde sem aviso.
- **Duas abas abertas na mesma tela** — uma não apaga o trabalho da outra em silêncio.
- **Ação desfeita** — quando a ação é reversível, oferece "desfazer"; quando não é, pede confirmação dizendo o que vai ser perdido.

## Conexão e sistema

- **Internet cai no meio da ação** — avisa, não finge que salvou, e deixa tentar de novo sem redigitar.
- **Internet lenta** — mostra que está carregando (esqueleto da tela, não tela em branco).
- **Erro do servidor** — explica em linguagem simples e diz o que fazer; o resto da tela continua funcionando.
- **Sessão expirada** — leva ao login e volta para onde a pessoa estava, sem perder o que digitou.

## Pessoas

- **Sem permissão** — explica que não tem acesso e a quem pedir; não mostra botão que vai falhar.
- **Primeiro uso** (conta nova, nada cadastrado) — nunca painel em branco: exemplo ou uma ação clara para começar.
- **Só teclado** — dá para fazer tudo com Tab, Enter e Esc; o foco aparece.
- **Celular com teclado aberto** — o formulário continua usável; o botão de enviar não some.
- **Zoom 200%** — nada some nem se sobrepõe.

## Tipos de estado vazio

1. **Primeiro uso** — explica o que vai aparecer ali e oferece a primeira ação.
2. **Limpo pelo usuário** (concluiu tudo) — reconhece ("Nenhuma pendência") sem parecer erro.
3. **Busca ou filtro sem resultado** — diz qual filtro está ativo e oferece limpar.
4. **Sem permissão** — diz que existe conteúdo, mas não para esta pessoa.
5. **Erro ao carregar** — diz que falhou, não que está vazio, e oferece tentar de novo.

---

## Casos acrescentados por bugs reais

Aqui entra só o que vale para qualquer produto. O caso concreto (commit, tela, empresa) fica no projeto onde aconteceu, na pasta `docs` do `.claude/konoha.json` dele, junto com os casos que só existem lá. Quem aplica a lista lê as duas.

- **Usuário com acesso a várias empresas** (root, conta compartilhada, consultor) — cada tela mostra só a empresa escolhida, nunca mistura. — origem: bug real (root via mensagens agendadas de outra empresa; 11 testes simulados na área não pegaram)
- **Registro sem o vínculo que "sempre existe"** (conversa sem cliente, negócio sem etapa, contato sem empresa) — a tela funciona e mostra o vazio de forma clara. — origem: bug real (58% das conversas reais sem cliente; nenhum dado de teste tinha o caso)
- **Data perto da meia-noite no fuso do Brasil** (ex.: 23h30 de São Paulo, que já é o dia seguinte em UTC) — mostra o dia certo. Todo teste de data roda com o fuso fixo. — origem: bug real (data um dia antes; 33 testes na área, nenhum com fuso fixo)
- **Resposta real do serviço externo com os valores padrão dele** (campos que a API grava sozinha, como desligado por padrão) — o simulado usado no teste é conferido contra uma resposta real gravada. — origem: bug real (o simulado da API de WhatsApp não tinha o campo `enabled=false`)
- **Duas ações ao mesmo tempo sobre o mesmo registro** (dois atendentes, ou tela e automação) — nenhuma se perde, nada duplica. — origem: bug real
- **Volume real** (a empresa com mais dados, não a de teste) — a consulta termina dentro do tempo limite. — origem: bug real
