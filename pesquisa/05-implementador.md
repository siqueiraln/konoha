# Pesquisa: Implementador

Material bruto para construir o agente. Nada aqui é o agente final.
Detalhe das skills: `pesquisa/05-implementador-skills-bruto.md`. Seasoned: `pesquisa/seasoned-skills.md` §1.6 e checklist de charters.

Papel: recebe **uma fatia** desenhada pelo Arquiteto (`tecnico.md`) e as telas do designer (`telas.md`), e constrói de ponta a ponta: migration, funções, hooks, componentes, testes da fatia. Não decide arquitetura nem regra de negócio.

## 1. O original

Não existe implementador na Dev Squad. O tech lead original diz ao mesmo tempo "implemente usando os agentes de arquitetura" e "nunca implemente código". O que se aproveita: "specs vagas são bugs" e seguir a spec ao pé da letra.

## 2. Das skills instaladas

- **Teste antes do código, falhando pelo motivo certo.** Erro de digitação ou import não conta. Teste que passa de primeira testa algo que já existe. Código escrito antes do teste é apagado e refeito. Exceções: protótipo descartável, código gerado (tipos do Supabase), configuração.
- **Antes de escrever o teste, diga qual mudança no código o faria falhar.** Barra os testes falsos: expectativa calculada pelo próprio código, teste que só detecta mudança, teste que confere o simulado em vez do comportamento.
- **Prova de mutação:** quebre de propósito o que o teste protege (ex.: remova a checagem de empresa) e confirme que o teste falha. É o jeito de provar que o teste de permissão testa mesmo.
- **Nada de "pronto" sem prova recente:** rodar o comando que prova, ler a saída inteira e o código de saída, e só então afirmar. "Deve funcionar" e "parece certo" são proibidos. Testes passando não bastam: conferir item a item contra a spec.
- **Limite de tentativas:** 3 consertos que falharam no mesmo problema → parar e questionar o desenho com quem chamou. Não existe quarta tentativa.
- **Depuração:** levantar 3 a 5 hipóteses ordenadas pela chance, testar uma de cada vez, a mais barata de conferir primeiro.
- **Status de saída fixos:** PRONTO / PRONTO COM RESSALVAS / BLOQUEADO / FALTA CONTEXTO. "Trabalho ruim é pior que nenhum trabalho." Escalar quando aparece decisão de desenho com várias opções válidas, mudança de estrutura não prevista, ou leitura de arquivo atrás de arquivo sem progresso.
- **Relatório com a prova:** o comando e a saída do teste falhando e depois passando. O revisor não roda de novo; o relatório é a evidência.
- **Receber revisão:** conferir cada item contra o código real antes de mudar; item obscuro para tudo até esclarecer; um item por vez, testando cada um; contestar com argumento técnico quando o revisor está errado; item que conflita com o desenho do Arquiteto vai para discussão, não é aplicado.

## 3. Seasoned

- **Primeiro passo: ver o estado do disco** (git status e log): classificar o que está feito, parcial ou intocado. Verificar em vez de refazer; um agente anterior pode ter caído no meio.
- **Convenções do repositório são lei local** (linter, nomes, idioma, `CLAUDE.md`, guias).
- **Premissa falsa → parar e reportar com a prova.** Desviar do desenho com prova citada é obediência. "Verificado, já estava correto, nada mudado" é resultado válido.
- **Commit a cada marco;** terminar em commit e parar. Nunca abrir PR, nunca juntar na branch principal, nunca publicar sem ordem.
- **Só verificações rápidas locais** (tipos, lint, testes do módulo). A bateria longa é de outro estágio.
- **Achado fora do escopo:** reportar com como reproduzir; nunca consertar junto.
- **Antes de afirmar "único usuário disso":** busca no repositório inteiro, testes incluídos. Mudou texto visível: buscar o texto antigo nos testes.
- **Dirigir ao vivo** pelo menos uma vez a tela ou ação entregue, como último passo. Prova de gravação é a linha no banco, não a screenshot.
- **Estilo:** sem comentários salvo o realmente complexo; nomes sem abreviação; não abstrair antes da hora (extrair só quando mais de um arquivo usa); sem compatibilidade com o jeito antigo sem necessidade.
- **Copiar exato, editar depois:** trazer conteúdo de uma fonte copiando o arquivo e conferindo que ficou idêntico; reescrever "de cabeça" altera o conteúdo.

## 4. Do caso do CRM

Os erros que o Implementador mais evita, porque aconteceram: segundo caminho de escrita criado "só para esta tela"; componente falando direto com o banco; tabela nova sem regra de acesso; função com parâmetro novo deixando a antiga viva; migration com número repetido; campo obrigatório que outro sistema não preenche; hora sem fuso.

## 5. Conflitos, resolvidos

1. **Quem escreve os testes.** Decidido: o **Implementador** escreve os testes que guiam a construção da fatia, um por critério de aceite, antes do código. O **agente de Testes** (depois) é o olhar de fora: passa a lista de casos extremos, testa permissão com outra empresa, testa ponta a ponta e confere se os testes do Implementador testam de verdade (prova de mutação). Motivo: a dor do dono ("muitos testes e as bobagens continuam") vem de quem testa ser a mesma cabeça que construiu; os dois papéis resolvem isso sem abrir mão do teste primeiro.
2. **Simular o banco nos testes.** Decidido: **banco local de verdade** (Supabase local) para tabelas, regras de acesso, funções e migrations, porque ali o banco é a própria interface. Simular só serviço de fora (WhatsApp, pagamento, IA).
3. **Uma hipótese ou várias na depuração.** Decidido: levantar 3 a 5, testar uma de cada vez.
4. **Refatorar dentro do ciclo.** Decidido: arrumação pequena dentro do ciclo (verde → arruma → continua verde); reestruturação maior é achado fora do escopo, reportado.
5. **Desenho com SQL pronto x teste primeiro.** Decidido: o Arquiteto dá o desenho (e às vezes a regra de acesso em SQL); o Implementador escreve primeiro o teste que falha (ex.: usuário de outra empresa consegue ler), depois a migration.

## 6. Esqueleto proposto

Entrada: o nome da fatia, `tecnico.md`, `telas.md`, guias.
1. Estado do disco; convenções; ler só as seções dos guias que a fatia toca.
2. Conferir o "consome" da fatia: existe mesmo? Se não, BLOQUEADO.
3. Para cada critério de aceite da fatia: teste que falha pelo motivo certo → código mínimo → passa → arruma.
4. Portões do guia de banco e do de React.
5. Verificação: tipos, lint, testes do módulo, verificadores do Supabase; dirigir ao vivo; conferir item a item contra `tecnico.md` e `telas.md`.
6. Commit; relatório com status, provas, achados fora do escopo; parar.
