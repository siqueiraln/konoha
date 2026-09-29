"""Configuração do projeto onde a Konoha está trabalhando.

Cada projeto tem, no próprio repositório, o arquivo `.claude/konoha.json`:

    {
      "linear_time": "Nome do time no Linear",
      "n8n_hosts": ["dominio-do-n8n-sem-n8n-no-nome.com.br"],
      "docs": "docs/crm/konoha",
      "publicar_funcao": "npm run publicar:funcao -- {nome}"
    }

Todos os campos são opcionais. Sem o arquivo, o gancho do Linear não roda e a
trava do n8n reconhece só endereços com "n8n" no nome.
O que é de um projeto mora no projeto; a Konoha não tem nome de cliente.
"""

import json
import os

ARQUIVO = os.path.join(".claude", "konoha.json")


def config(cwd: str) -> dict:
    """Sobe de `cwd` até achar `.claude/konoha.json`. Devolve {} se não achar ou se estiver quebrado."""
    atual = os.path.abspath(cwd or ".")
    for _ in range(12):
        caminho = os.path.join(atual, ARQUIVO)
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
