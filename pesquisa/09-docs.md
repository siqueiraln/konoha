# Pesquisa: Docs

Material bruto para construir o agente. Nada aqui é o agente final.

## 0. O que mudou desde o original

No original, a documentação era um acessório: README, API, changelog, depois que o código estabilizava. Na nossa empresa ela é **a memória**. Cada agente começa sem lembrar de nada; o que ele sabe do produto é o que está escrito. A dor do dono ("o agente não reaproveita o que ele mesmo fez em outra rota", "se perde com várias camadas") é, em boa parte, falta de memória escrita no lugar certo. Por isso o leitor principal do Docs é **o próximo agente**, e o segundo é **o dono**.

## 1. Diagnóstico do original (`08_docs-writer.md`)

**Manter:**
- "Documentação desatualizada é pior que ausente — prefira menos e correto."
- "Nunca documente comportamento que o código não implementa"; ler o código e os testes, não a intenção.
- Documento de retomada: um agente numa sessão nova continua sem perguntar.
- Referência cruzada com caminho exato (`docs/x.md#secao`), nunca "conforme a arquitetura".
- Comandos copiáveis ("rode `npm install`", não "instale as dependências").
- Glossário vivo, um termo por conceito.

**Cortar:** status de sprint (não temos sprint; o estado vive no documento de projeto e nos relatórios); guia de contribuição e código de conduta; comentários JSDoc em massa (a regra da casa é código sem comentário salvo o difícil).

**Falta:** o arquivo de instruções do projeto para agentes (`CLAUDE.md` / `AGENTS.md`) como roteador; poda do que ficou velho; verificação de cada afirmação contra o código; texto para o dono em linguagem simples; quando atualizar (no mesmo trabalho que muda o comportamento).

## 2. Da skill `writing-for-agents` (instalada)

- **Ponteiro de contexto:** a linha no `CLAUDE.md` que aponta para um documento decide **quando** o agente vai lê-lo. O texto do ponteiro importa mais que o documento: diga o que é e **em quais situações** ler. Ponteiro fraco para documento essencial é defeito.
- **Duas cargas:** tudo que fica sempre carregado (o `CLAUDE.md`) custa atenção em todo turno. O resto vai para documentos separados, alcançados por ponteiro.
- **Hierarquia:** passos no arquivo principal; referência consultada sob demanda; o que só alguns casos usam vai para arquivo separado. Arquivo grande demais dilui a atenção mesmo com tudo verdadeiro.
- **Uma fonte da verdade:** cada informação num lugar só. O ambiente também é fonte (`package.json`, configs, pastas): documento que repete o que o ambiente já diz é **cópia que envelhece**. Documente o que não dá para descobrir olhando: a convenção não escrita, o porquê de uma escolha, a armadilha.
- **Sedimento:** sem poda, as camadas velhas se acumulam porque acrescentar parece seguro e apagar parece arriscado. Toda linha precisa continuar valendo.
- **Frase que não muda comportamento** (o agente já faria aquilo de qualquer jeito) é peso morto: apague a frase inteira.
- **Diga o que fazer**, não só o que não fazer: proibição coloca a coisa proibida na cabeça do agente.

## 3. Seasoned

- **Prosa factual é verificada como código:** antes de publicar, tentar refutar cada afirmação contra a fonte. As mais perigosas são as de totalidade ("todas as rotas", "todo chamador"): escreva o mecanismo e exemplos conferidos; totalidade só quando o conjunto é pequeno e medido.
- **Escrever a partir do que se vê** (a tela, o número medido), nunca da intenção.
- **Mudou o comportamento, procure o texto antigo** no repositório inteiro: dicas de tela, e-mails, docs.
- **Instrução para agente:** cada frase descreve a regra atual, nunca "antes era X, agora é Y"; palavras simples; para conjuntos que crescem, descreva como listar, não a lista; cada lição mora num arquivo só, onde o próximo agente vai procurar.
- **Notas de versão** a partir do estudo de cada mudança (descrição e código), nunca só dos títulos; toda frase rastreável a uma mudança.
- **Voz para pessoas:** colega explicando para colega; problema antes da solução; específico ("menos de um minuto"), não vago; sem jargão de marketing; admitir o que ainda está cru.
- **Registro com checklist fechado:** todo documento responde as mesmas perguntas, inclusive com "nenhum", para o leitor distinguir "não tem" de "esqueceram".

## 4. Do CRM (caso real)

- **O que funciona:** `CLAUDE.md` de 134 linhas funcionando como **roteador** (quem decide o quê, fonte de dados, processo por tamanho de mudança, o portão das três perguntas), com ponteiros para `docs/crm/`: `visao-geral.md`, `banco.md` (com uma seção de "pegadinhas"), `padroes.md` (regra + exemplo + desvios contados), um arquivo por módulo, `saneamento.md` (problemas com evidência, dono e status, sem apagar o resolvido), ~70 ADRs curtos. Regra: mexeu no comportamento, atualiza o doc na mesma mudança.
- **O que preocupa:**
  - **`docs/` fica fora do controle de versão** ("arquivo local, fora do controle de versão", `CLAUDE.md`). A memória do projeto não viaja com o código: outra máquina, outro agente em outra pasta ou um disco perdido não têm os 621 documentos, e não há histórico de quando uma regra mudou.
  - Volume: 621 arquivos `.md` em `docs/`. Sem poda, vira sedimento.
  - ADRs com número duplicado (5 casos) por duas frentes escrevendo no mesmo dia.

## 5. Fontes externas (conferidas em 2026-09-26)

- **Diátaxis:** quatro tipos de documento para quatro necessidades: tutorial (aprender), guia de tarefa (fazer algo), referência (consultar), explicação (entender o porquê). Misturar os tipos num mesmo documento é o erro mais comum. [diataxis.fr](https://diataxis.fr/)
- **AGENTS.md:** formato aberto de instruções para agentes de código, mantido pela Agentic AI Foundation (Linux Foundation) desde dez/2025, lido por mais de 30 ferramentas. Desde 18/09/2026 o Claude Code lê o `AGENTS.md` quando não há `CLAUDE.md`. [agents.md](https://agents.md/), [Linux Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation), [The Register](https://www.theregister.com/ai-and-ml/2026/09/18/anthropic-decides-to-support-openais-markdown-instructions-spec/5297588)

## 6. Conflitos, resolvidos

1. **Um arquivo de instruções ou dois.** Decidido: **um só** por projeto. O que o projeto já usa continua (`CLAUDE.md` no CRM); projeto novo usa `CLAUDE.md` com a primeira linha apontando que vale também como `AGENTS.md`, ou o contrário, sem conteúdo duplicado.
2. **Documentar tudo x documentar o que não se descobre olhando.** Decidido: o segundo. O Docs não repete o que o código, as configs e o `package.json` já dizem.
3. **Docs dentro ou fora do git.** Pendente: pergunta ao dono (o CRM escolheu fora).

## 7. Esqueleto proposto

Três modos:
1. **Memória dos agentes** (depois de cada fatia ou projeto): atualiza o que a mudança tornou falso ou incompleto: `CLAUDE.md` (só ponteiros e regras que valem sempre), doc do módulo, `CONTEXT.md`, mapa de componentes do `DESIGN.md`, pegadinhas descobertas. Cada afirmação conferida contra o código.
2. **Para o dono** (quando algo vai para o ar): notas de versão em linguagem de negócio: o que mudou para quem usa, o que o dono precisa fazer ou avisar aos clientes.
3. **Poda** (periódica, ou quando um documento passa do tamanho): encontra o que ficou velho, repetido ou que não muda comportamento, e propõe remover.
