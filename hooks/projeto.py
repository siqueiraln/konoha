"""Configuração do projeto onde a Konoha está trabalhando.

Cada projeto tem o arquivo `.claude/konoha.local.json`, **fora do git** (o repositório
pode ser lido por outras pessoas e pelos agentes delas: o jeito da Konoha trabalhar não
vai para lá). Para o git ignorar só nesta máquina: a linha `.claude/konoha.local.json`
em `.git/info/exclude`. Projeto antigo pode ter `.claude/konoha.json` versionado; vale
se não houver o local.

    {
      "linear_time": "Nome do time no Linear",
      "n8n_hosts": ["dominio-do-n8n-sem-n8n-no-nome.com.br"],
      "docs": "<pasta, fora do repositório, com o que a Konoha aprendeu neste projeto>",
      "publicar_funcao": "npm run publicar:funcao -- {nome}",
      "banco_espelho": {"ref": "<código do projeto>", "mcp": "<servidor MCP ligado só nele>", "pasta": "<receita para refazer>"},
      "empresa_teste": {"nome": "<como aparece no sistema>", "id": "<company_id>"}
    }

Todos os campos são opcionais. Sem o arquivo, o gancho do Linear não roda e a
trava do n8n reconhece só endereços com "n8n" no nome.
O que é de um projeto mora no projeto; a Konoha não tem nome de cliente.
"""

import json
import os

ARQUIVOS = (os.path.join(".claude", "konoha.local.json"), os.path.join(".claude", "konoha.json"))


def config(cwd: str) -> dict:
    """Sobe de `cwd` até achar a configuração (a local antes da versionada). {} se não achar ou se estiver quebrada."""
    atual = os.path.abspath(cwd or ".")
    for _ in range(12):
        for arquivo in ARQUIVOS:
            caminho = os.path.join(atual, arquivo)
            if os.path.isfile(caminho):
                try:
                    with open(caminho, encoding="utf-8") as f:
                        dados = json.load(f)
                    return dados if isinstance(dados, dict) else {}
                except (OSError, ValueError):
                    return {}
        pai = os.path.dirname(atual)
        if pai == atual:
            break
        atual = pai
    return {}
