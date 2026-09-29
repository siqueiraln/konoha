# Guia: tela em React

Lido por seção. O Arquiteto e o Implementador leem só a seção que a tarefa toca.
Stack de referência: React + Vite, `@tanstack/react-query`, `react-router-dom`, `react-hook-form` + `zod`, `@supabase/supabase-js`. Em projeto existente, o que o projeto já usa vence este guia; divergência vira pergunta, não troca silenciosa.

O visual e o comportamento de tela (estados, textos, erros) são do `DESIGN.md` do projeto e do `telas.md` do designer. Este guia trata de como o código da tela é organizado.

---

## 1. A tela não fala direto com o banco

- **Componente e página nunca chamam `supabase.from`, `.rpc` ou `functions.invoke`.** O acesso a dados mora em hooks por domínio (`src/hooks/<dominio>/`), um por operação. Num projeto real, ~45 componentes falando direto com o banco foram a origem de boa parte da lógica duplicada.
- **Um hook por operação, usado por todas as telas.** Se duas telas gravam a mesma entidade, as duas usam o mesmo hook, que usa o caminho único de escrita do desenho.
- **Antes de criar um hook, procure** um que já faça a operação (`src/hooks/`, busca pelo nome da tabela ou da função). Hook que só repassa `supabase.from()` sem regra nenhuma não se paga; o que se paga é o hook que concentra a regra.
- **Regra de negócio pura** (cálculo, formatação de domínio, validação compartilhada) mora em `src/lib/<dominio>/`, sem React, testável sozinha.

## 2. Leitura e escrita com react-query

- **Leitura:** `useQuery`. Nunca `useState` + `useEffect` + busca manual; isso reimplementa o react-query, pior.
- **Escrita:** `useMutation`.
- **Chaves de consulta numa fábrica por domínio** (`leadKeys.all`, `leadKeys.detail(id)`), nunca escritas à mão em cada tela.
- **Toda escrita declara o que ela desatualiza.** No desenho, cada ação diz: "grava X, invalida as chaves Y e Z". Tela que mostra dado velho depois de salvar é esquecimento de invalidação.
- **Atualização otimista** (a tela muda antes do servidor confirmar) só em ação frequente e reversível (marcar, arrastar, alternar). Se o servidor recusar, a tela volta e mostra o erro no lugar. Ação com consequência (pagamento, envio, exclusão) espera a confirmação.
- **Clique duplo:** o botão fica desabilitado e mostra que está trabalhando enquanto a escrita roda (`isPending`); a escrita também é à prova de repetição no banco. Os dois, não um só.

## 3. Formulários

- `react-hook-form` + `zod`. O schema `zod` é a regra de validação da tela, e as mensagens estão na língua do usuário ("Informe o telefone com DDD"), nunca "Invalid input".
- Erro de validação e erro do servidor aparecem **no campo**, não só num aviso que some. Erro do servidor que não é de um campo aparece junto do botão que falhou.
- O que foi digitado nunca se perde por erro.
- A validação da tela **não substitui** a do banco. O banco valida de novo (restrições, regras de acesso, função).

## 4. Permissão na tela

- A tela **reflete** a permissão do banco: esconde ou desabilita (dizendo por quê) o que a pessoa não pode fazer. A decisão é do banco; a tela usa a mesma fonte (papel do usuário vindo do banco), nunca uma regra própria diferente.
- Botão que aparece e dá erro de permissão ao clicar é defeito.

## 5. Dados, datas e listas

- **Tipos** vêm dos tipos gerados do banco (`Database`), e dos schemas `zod` para formulário. Sem `as` para calar erro de tipo.
- **Datas:** o banco guarda com fuso; a tela formata sempre por uma função única do projeto, no fuso da empresa ou do usuário (o desenho diz qual). Nunca `new Date()` solto para decidir "hoje".
- **Listas longas:** paginação ou virtualização (`@tanstack/react-virtual`) quando a lista pode passar de algumas centenas de itens. Não antes.
- **Tempo real** (Supabase Realtime) só quando o desenho pede; a assinatura é aberta e fechada pelo hook, e o que chega atualiza o cache do react-query, não um estado paralelo.

## 6. Organização

- Página em `src/pages/`, componentes do domínio em `src/components/<dominio>/`, peças visuais compartilhadas em `src/components/ui/`, hooks em `src/hooks/<dominio>/`, regra pura em `src/lib/<dominio>/`.
- **Nomes pelo domínio** (`useCriarLead`, `leadKeys`), com os termos do `CONTEXT.md`.
- **Estado de tela** (`useState`) só para o que é da tela: painel aberto, aba escolhida, texto sendo digitado. Dado do servidor fica no react-query.
- Rota nova: a autorização da página é conferida na própria rota, não só no menu.

## 7. Portão antes de declarar pronto

- Nenhum acesso a dados fora dos hooks.
- Toda escrita com invalidação declarada e botão protegido contra clique duplo.
- Nenhum componente novo que o mapa do `DESIGN.md` já tinha.
- Tipos gerados atualizados; sem erro de tipo, sem aviso no console.
