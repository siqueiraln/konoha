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


def _ler(pasta: str):
    """A configuração desta pasta (a local antes da versionada), {} se quebrada, None se não houver."""
    for arquivo in ARQUIVOS:
        caminho = os.path.join(pasta, arquivo)
        if os.path.isfile(caminho):
            try:
                with open(caminho, encoding="utf-8") as f:
                    dados = json.load(f)
                return dados if isinstance(dados, dict) else {}
            except (OSError, ValueError):
                return {}
    return None


def _pasta_principal(worktree: str):
    """Pasta de trabalho separada (git worktree) aponta, no arquivo `.git`, para o repositório principal."""
    try:
        with open(os.path.join(worktree, ".git"), encoding="utf-8") as f:
            linha = f.readline().strip()
    except OSError:
        return None
    if not linha.startswith("gitdir:"):
        return None
    gitdir = os.path.normpath(linha[len("gitdir:"):].strip())
    partes = gitdir.split(os.sep)
    if ".git" in partes and "worktrees" in partes:
        return os.sep.join(partes[: partes.index(".git")]) or None
    return None


def config(cwd: str) -> dict:
    """Sobe de `cwd` até achar a configuração. Numa pasta de trabalho separada (git worktree, que não leva
    o arquivo local, fora do git), usa a da pasta principal do repositório. {} se não achar."""
    atual = os.path.abspath(cwd or ".")
    for _ in range(12):
        dados = _ler(atual)
        if dados is not None:
            return dados
        if os.path.isfile(os.path.join(atual, ".git")):
            principal = _pasta_principal(atual)
            dados = _ler(principal) if principal else None
            if dados is not None:
                return dados
        pai = os.path.dirname(atual)
        if pai == atual:
            break
        atual = pai
    return {}
