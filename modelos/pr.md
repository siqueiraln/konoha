# Modelo: pedido de junção (PR)

Um PR por tarefa do Linear (referência do Tech Lead, §4). Quem lê é quem junta e o dono, no celular. O detalhe já está no documento do projeto, no ADR, no andamento e nas provas.

**Título:** o mesmo da tarefa do Linear (a frase de WhatsApp), com o código no fim: `<Área>: <o que muda para quem usa> (STR-nn)`.

**Corpo:** nesta ordem, 100 a 150 palavras no total. Nada além destas cinco partes.

```markdown
<O que muda para quem usa, em 2 a 4 linhas, linguagem de negócio. Sem nome de arquivo, tabela ou função.>

**Antes de juntar:** <nada | o que precisa estar no ar antes, em uma linha>
**Depois de juntar:** <nada | o que o dono faz ou avisa, em uma linha>
**Voltar atrás:** <reverter o PR basta | caminho do roteiro de volta, em uma linha>
**Detalhe:** <documento do projeto ou do módulo> · <ADR, se houver>
```

O PR só abre quando a mudança em produção de que ele depende já foi aplicada (referência §4).

**Proibido no corpo** (vai para o andamento ou para a pasta de provas, nunca para o PR): lista de testes e contagens, tabela de arquivos ou funções tocadas, comandos SQL, códigos de conferência, portão de pertencimento e varredura de consumidores, histórico do que já foi aplicado e quando, trechos de relatório de agente.

**Exemplo** (o PR 427 do CRM, que saiu com 400 palavras, neste modelo):

```markdown
Os lembretes da agenda e o bloco "Enviar WhatsApp" das automações passam a poder mandar botões, link do Meet, localização e cartão de contato. Vale para qualquer empresa; o Instituto Mix é o primeiro a usar. Mensagens e automações que já existem continuam iguais.

**Antes de juntar:** nada. Banco, n8n e função do servidor já estão no ar desde 10/10.
**Depois de juntar:** nada.
**Voltar atrás:** roteiro em `supabase/provas/mensagem-botoes/` (cinco passos, na ordem de lá).
**Detalhe:** `docs/crm/modulos/mensagem-com-botoes.md` · ADR 0133
```
