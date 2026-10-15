# Lista de casos extremos da empresa

Vale para toda tela e todo teste. A lista não cresce: ninguém propõe linha nova. Linha só sai com decisão do dono. O projeto pode ter a sua (`casos-extremos.md` na pasta `docs` do `.claude/konoha.local.json`); quem aplica lê as duas.

## Dados

- **Lista vazia:** mostra o estado vazio certo (tipos abaixo).
- **Um item só:** plural certo ("1 lead"), layout não quebra.
- **Muitos itens (1.000+):** continua rápida, pagina ou carrega aos poucos.
- **Texto longo** (100+ caracteres, palavra sem espaço): quebra ou corta com "…", não empurra a tela.
- **Emoji e acentos:** certos em todo lugar, inclusive busca e ordenação.
- **Campo opcional em branco:** nunca "null", "undefined", "NaN".
- **Zero, negativo, muito grande:** formatado certo e cabe.
- **Datas nas bordas** (virada de mês e ano, 29/02): o dia certo para quem vê.
- **Meia-noite no fuso do Brasil** (23h30 em São Paulo já é amanhã em UTC): dia certo; teste de data com fuso fixo.
- **Registro sem o vínculo que "sempre existe"** (conversa sem cliente): a tela funciona e mostra o vazio.
- **Volume real** (a maior empresa): a consulta termina no tempo limite.

## Ações

- **Clique duplo ou repetido:** grava uma vez; o botão mostra que está trabalhando.
- **Sair no meio** (fechar, voltar, atualizar): o digitado não se perde sem aviso.
- **Duas abas na mesma tela:** uma não apaga a outra em silêncio.
- **Duas ações ao mesmo tempo no mesmo registro** (dois atendentes, ou tela e automação): nada se perde nem duplica.
- **Ação desfeita:** reversível oferece "desfazer"; irreversível pede confirmação dizendo o que se perde.

## Conexão e sistema

- **Internet cai no meio:** avisa, não finge que salvou, deixa tentar sem redigitar.
- **Internet lenta:** esqueleto da tela, não tela em branco.
- **Erro do servidor:** explica em linguagem simples; o resto da tela funciona.
- **Sessão expirada:** login e volta para onde estava, sem perder o digitado.
- **Serviço externo com os valores padrão dele:** o simulado do teste é conferido contra uma resposta real gravada.

## Pessoas

- **Sem permissão:** explica e diz a quem pedir; não mostra botão que vai falhar.
- **Acesso a várias empresas:** cada tela mostra só a empresa escolhida.
- **Primeiro uso:** nunca painel em branco; exemplo ou primeira ação clara.
- **Só teclado:** tudo com Tab, Enter e Esc; foco visível.
- **Celular com teclado aberto:** o botão de enviar não some.
- **Zoom 200%:** nada some nem se sobrepõe.

## Tipos de estado vazio

1. **Primeiro uso:** explica o que vai aparecer e oferece a primeira ação.
2. **Limpo pelo usuário:** reconhece ("Nenhuma pendência") sem parecer erro.
3. **Busca ou filtro sem resultado:** diz o filtro ativo e oferece limpar.
4. **Sem permissão:** diz que existe conteúdo, mas não para esta pessoa.
5. **Erro ao carregar:** diz que falhou, não que está vazio, e oferece tentar de novo.
