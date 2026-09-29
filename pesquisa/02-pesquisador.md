# Pesquisa: Pesquisador

Agente novo, sem equivalente na Dev Squad. Criado por decisão do dono para a rodada de overclock: depois da primeira versão rodando, traz os fatos que alimentam as propostas do PO.

## 1. Das skills instaladas

### research (mattpocock)
- Investigar contra **fontes primárias**: documentação oficial, código-fonte, especificações, APIs do próprio fornecedor. Resumo de terceiros não conta.
- **Seguir cada afirmação até a fonte dona dela.**
- Entregar **um arquivo Markdown**, com a fonte citada em cada afirmação.
- Rodar em segundo plano, para quem pediu continuar trabalhando.

### revenue-centric-design (Richard)
- **Mesmo motor, experiência diferente:** quando todos usam a mesma tecnologia, a diferença está na experiência (menos atrito na entrada, encaixe no fluxo de trabalho, uso contínuo e colaborativo). Pesquisa de mercado deve olhar **como** o concorrente entrega, não só **o que** ele tem.
- **Nicho que ninguém atende:** a ideia forte é a ferramenta que só faz sentido para um nicho específico (ex.: "CRM para clínicas de harmonização facial, com alerta de retoque em 110 dias"). Achado genérico vale menos que achado do nicho.
- **Fosso:** o que é difícil de copiar (marca, custo de trocar, efeito de rede interno).
- **Dor proporcional ao que se perde:** um lead perdido custa R$3.000 a uma clínica e R$60 a uma barbearia. Pesquisa de dor mede o prejuízo.

### shaping e doutrina (Seasoned)
- **Fato externo se pesquisa na web, não se pergunta ao dono.**
- **Toda escolha de ferramenta, biblioteca ou serviço começa com pesquisa ao vivo**, nunca só com o que o modelo lembra do treino.
- **Premissas sobre o sistema em produção se sondam ao vivo** (abrir, consultar, testar), não se deduzem do código.
- **Dados reais resolvem perguntas:** consultas no banco e dados de uso contam como pesquisa.
- **Citação exata é conferida contra a fonte**, palavra por palavra.
- **"Não achar nada" é resposta válida.** Pressionado a achar, o agente inventa.

## 2. Fontes externas (método)

| Fonte | Ideia útil |
|---|---|
| Hierarquia de fontes (primária, secundária, terciária) | Peso de uma afirmação depende de quão perto da origem ela está. |
| Mike Caulfield, **SIFT** / leitura lateral | Pare; investigue quem é a fonte; procure cobertura melhor; rastreie a afirmação até o contexto original. Checar a fonte **saindo dela** (o que outros dizem sobre ela) é mais eficaz que ler a própria fonte com cuidado. |
| **Triangulação** | Afirmação que decide algo precisa de pelo menos duas fontes independentes. |
| Sherman Kent, **palavras de probabilidade estimativa**; padrões de análise de inteligência (ICD 203) | Separar **fato** de **inferência**, e dizer o grau de confiança com palavras de significado fixo (quase certo, provável, possível, improvável). |
| **Mineração de avaliações** (Joanna Wiebe / Copyhackers) | As dores reais do mercado estão nas avaliações de 1 a 3 estrelas dos concorrentes (lojas de apps, G2, Capterra; no Brasil, Reclame Aqui). As palavras dos clientes valem mais que a página de vendas do concorrente. |
| **JTBD** (Christensen, Moesta) | Pesquisar o "trabalho" que o cliente contrata, e as alternativas que ele usa hoje, inclusive planilha e WhatsApp, não só os concorrentes diretos. |
| **Saturação** (pesquisa qualitativa) | Parar quando novas fontes param de trazer achados novos. Evita pesquisa infinita. |

## 3. Esqueleto proposto

Três frentes para o overclock, da mais barata e confiável para a mais incerta:
1. **O produto rodando:** dados de uso, o que já está pronto e pode ser reaproveitado, onde as pessoas travam.
2. **A tecnologia em uso:** o que a stack atual permite e não usamos (documentação oficial e novidades recentes).
3. **O mercado:** concorrentes diretos e alternativas (planilha, WhatsApp), o que oferecem, como entregam, e as reclamações dos clientes deles.

Regras transversais: fonte primária; fato separado de inferência; confiança com palavras fixas; triangulação no que decide; parar por saturação; "nada relevante" é resultado válido; não propõe nem prioriza (isso é do PO).
