# Guia: tela em React

Lido por seção: leia só a que a tarefa toca. Stack de referência: React + Vite, `@tanstack/react-query`, `react-router-dom`, `react-hook-form` + `zod`, `@supabase/supabase-js`. Em projeto existente, o que o projeto já usa vence este guia; divergência vira pergunta, não troca silenciosa. Visual e comportamento de tela são do `DESIGN.md` e do `telas.md`.

## 1. A tela não fala direto com o banco
- Componente e página nunca chamam `supabase.from`, `.rpc` ou `functions.invoke`. O acesso a dados mora em hooks por domínio (`src/hooks/<dominio>/`), um por operação, usado por todas as telas e pelo caminho único de escrita do desenho.
- Antes de criar um hook, procure um que já faça a operação (`src/hooks/`, pelo nome da tabela ou da função).
- Regra de negócio pura (cálculo, validação compartilhada) mora em `src/lib/<dominio>/`, sem React.

## 2. Leitura e escrita com react-query
- Leitura com `useQuery`, escrita com `useMutation`. Nunca `useState` + `useEffect` para buscar dado.
- Chaves numa fábrica por domínio (`leadKeys.all`, `leadKeys.detail(id)`), nunca escritas à mão.
- Toda escrita declara o que desatualiza: "grava X, invalida as chaves Y e Z", como está no desenho.
- Atualização otimista só em ação frequente e reversível (marcar, arrastar). Pagamento, envio e exclusão esperam a confirmação.
- Clique duplo: botão desabilitado com `isPending` **e** escrita à prova de repetição no banco. Os dois.

## 3. Formulários
- `react-hook-form` + `zod`, com mensagens em português ("Informe o telefone com DDD").
- Erro aparece no campo; erro do servidor que não é de campo aparece junto do botão. O que foi digitado não se perde.
- A validação da tela não substitui a do banco.

## 4. Permissão na tela
A tela esconde ou desabilita (dizendo por quê) o que a pessoa não pode, usando a mesma fonte do banco (papel vindo do banco), nunca uma regra própria. Botão que aparece e dá erro de permissão é defeito.

## 5. Dados, datas e listas
- Tipos gerados do banco (`Database`) e schemas `zod`. Sem `as` para calar erro de tipo.
- Datas formatadas por uma função única do projeto, no fuso que o desenho diz. Nunca `new Date()` solto para decidir "hoje".
- Paginação ou virtualização só quando a lista pode passar de algumas centenas de itens.
- Tempo real (Supabase Realtime) só quando o desenho pede: o hook abre e fecha a assinatura, e o que chega atualiza o cache do react-query.

## 6. Organização
- Páginas em `src/pages/`, componentes do domínio em `src/components/<dominio>/`, peças compartilhadas em `src/components/ui/`, hooks em `src/hooks/<dominio>/`, regra pura em `src/lib/<dominio>/`.
- Nomes pelo domínio (`useCriarLead`, `leadKeys`), com os termos do `CONTEXT.md`.
- `useState` só para o que é da tela; dado do servidor fica no react-query.
- Rota nova confere a autorização na própria rota, não só no menu.

## 7. Portão antes de declarar pronto
- Nenhum acesso a dados fora dos hooks.
- Toda escrita com invalidação declarada e botão protegido contra clique duplo.
- Nenhum componente novo que o mapa do `DESIGN.md` já tinha.
- Tipos gerados atualizados; sem erro de tipo, sem aviso no console.
