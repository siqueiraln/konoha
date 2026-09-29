# Pesquisa: Testes

Material bruto para construir o agente. Nada aqui é o agente final.
Fontes detalhadas: o caso real e as ferramentas levantadas (no repositório do projeto de origem), `pesquisa/05-implementador-skills-bruto.md` (TDD, mutação, verificação), `pesquisa/seasoned-skills.md` §1.8.

Papel decidido (2026-09-26): o **olhar de fora**, depois do Implementador. O Implementador escreve os testes que guiam a construção; este agente aplica a lista de casos extremos, testa permissão com outra empresa, testa ponta a ponta no navegador e confere se os testes do Implementador testam de verdade.

## 1. A resposta à dor do dono, com dados do CRM

"O agente faz uma caralhada de testes mas as bobagens continuam." Os números confirmam, e mostram por quê:

- **~5 mil casos de teste em 499 arquivos**, e **em 7 de 10 bugs recentes que chegaram à produção já havia teste na área.** O problema não é quantidade; é o tipo de teste.
- **Nenhum teste do front usa o banco de verdade:** 103 arquivos simulam o Supabase, por regra da casa. Exemplo: o usuário root via mensagens agendadas de outra empresa, e o hook tinha 11 testes, todos com Supabase simulado.
- **Os dados de teste são limpos demais.** 58% das conversas reais não tinham cliente vinculado; nenhum dado de teste tinha esse caso.
- **Ninguém fixa o fuso.** A data aparecia um dia antes (UTC-3); havia 33 testes na área.
- **O simulado da API externa mentia.** O dublê da API de WhatsApp não tinha um campo que a API real grava por padrão.
- **Permissão entre empresas quase sem teste:** só 8 dos 33 testes de banco rodam como usuário comum; o resto roda como dono do banco, que ignora as regras. Uma migration admite: os testes "só passaram porque rodaram como o dono da função".
- **Os testes de banco rodam contra produção**, dependem de dados reais, e um deles "pulava em silêncio".
- **Não há teste ponta a ponta, prova de mutação, medida de cobertura nem execução automática a cada mudança.** A versão principal ficou 8 dias com 11 testes vermelhos sem ninguém notar; há 157 erros de tipo antigos.
- **Os logs da raiz** mostram o processo de teste morrendo antes de rodar qualquer teste, repetido 4 vezes: tentativa sem diagnóstico.

Classes de bug que escaparam, em ordem: permissão entre empresas; dado real diferente do dado de teste (vazio, sem vínculo, conta compartilhada); fuso e datas; corrida (dois ao mesmo tempo); simulado diferente da API real; volume e tempo limite.

## 2. Diagnóstico do original (`06_test-automator.md`)

**Manter:** testar comportamento, não detalhe interno; teste instável é bug; determinístico (sem depender de ordem ou relógio); simular só o que é externo.

**Cortar:** meta de 80% de cobertura de linhas (mede linha executada, não comportamento conferido: o CRM tem 5 mil testes e os bugs passam); "mocks para DB" (é exatamente o que deixou passar os furos de permissão); "um assert por teste".

**Falta:** banco de verdade; permissão com outra empresa; dados sujos como os reais; fuso fixo; prova de mutação; ponta a ponta no navegador; execução automática a cada mudança; o que fazer com teste instável.

## 3. Seasoned (o mais detalhado sobre testes)

- **Teste verde não prova nada até ser visto vermelho pelo motivo certo.** Sem isso, prova de mutação: neutralizar exatamente o comportamento, ver falhar com a mensagem esperada, restaurar e conferir.
- **Sinais de falso verde:** o valor esperado coincide com o comportamento errado antigo; o caminho foi simulado acima da mudança; o teste de erro passou por outro erro; a lista dos dados de teste está sempre vazia.
- **Teste instável nunca é mascarado** com espera, nova tentativa ou asserção enfraquecida: provavelmente é bug de produto. Concorrência se testa com sinal determinístico, nunca com cronômetro.
- **Ponta a ponta:** um comportamento por arquivo, nome do arquivo é a frase do comportamento; selecionar como o usuário vê (papel, rótulo, texto); provar gravação indo e voltando (grava, recarrega, confere); nunca conferir a mensagem que some; relógio ancorado numa data calculada; fuso do negócio.
- **O teste passa se rodado de novo** sobre o estado deixado por uma tentativa que morreu no meio.
- **Cobertura medida por telas e ações alcançadas**, não por linha; lista do que não é alcançado só diminui.
- **Dados de teste:** identificadores aleatórios por teste (permite rodar em paralelo); nunca limpar o banco inteiro.
- **Permissão:** conceder exatamente a permissão testada e conferir que as vizinhas continuam negadas.
- **Bateria completa roda na execução automática** (CI), não na máquina; localmente só o que a mudança afeta.

## 4. Ferramentas atuais (conferidas em 2026-09-26; links no arquivo detalhado)

- **Banco:** `supabase test db` com pgTAP, em **banco local**, cada arquivo desfeito no final; permissão testada assumindo o papel de usuário comum com um usuário específico. A documentação também mostra teste com o cliente JS e dois usuários.
- **Prova de mutação:** StrykerJS com Vitest, rodando só nos arquivos da mudança (lista vinda do `git diff`) e reaproveitando resultados anteriores. **Atenção:** com o Vitest 5 (lançado em 25/09/2026) o Stryker roda zero testes e marca tudo como sobrevivente (problema aberto). Ficar no Vitest 4 até corrigirem. O CRM está no 4.
- **Navegador:** Playwright 1.63, seletores por papel e texto, um contexto limpo por teste, sessão salva por papel (serve para "empresa A x empresa B"), gravação do passo a passo na nova tentativa, `--repeat-each` e `--fail-on-flaky-tests` para caçar instabilidade, fuso fixo (`America/Sao_Paulo`).
- **Vitest 4.1:** rodar só o afetado pela mudança (`--changed`), `expect.poll` para esperar sem cronômetro.

## 5. Conflitos, resolvidos

1. **Simular o Supabase (regra atual do CRM) x banco local.** Decidido: permissão, restrição, função e gatilho se testam **no banco local**; simulado só para serviço externo, e o simulado é conferido contra uma resposta real gravada da API (senão ele mente, como o da API de WhatsApp).
2. **Meta de cobertura por linha x por comportamento.** Decidido: sem meta de linha. Cobertura = cada critério de aceite, cada linha da matriz de permissões e cada caso extremo que se aplica têm teste que já foi visto vermelho.
3. **Bateria completa local x automática.** Decidido: localmente, só o que a mudança afeta; a bateria completa roda automaticamente a cada mudança enviada (CI). Produto sem execução automática ganha uma; é trabalho deste agente propor e do Implementador montar.

## 6. Esqueleto proposto

Entrada: a fatia pronta (relatório do Implementador, o `git diff`), `tecnico.md`, `telas.md`, a lista de casos extremos.

1. **Os testes do Implementador testam?** Prova de mutação nos pontos sérios (checagem de empresa, restrição, proteção contra repetição, regra de negócio central): quebra, tem que ficar vermelho. Sinais de falso verde.
2. **Permissão de fora:** cada linha da matriz que a fatia toca, com usuário de outra empresa e com papel sem permissão, no banco local, pela API como a tela chama.
3. **Casos extremos:** a lista inteira nas telas e ações da fatia, com **dados sujos como os reais** (campo vazio, sem vínculo, texto enorme, emoji) e **fuso fixo**.
4. **Ponta a ponta:** a história recontada do projeto e os fluxos do `telas.md`, no navegador, provando gravação por ida e volta.
5. **Instabilidade:** repetir os testes novos várias vezes; instável é bug, investigado, nunca mascarado.
6. Achados voltam ao Implementador com o teste que falha. Bug que escapou da lista de casos extremos vira linha nova na lista.
