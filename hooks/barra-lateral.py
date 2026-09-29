"""Conferente da barra lateral: a conversa não termina a resposta com a barra desatualizada.

Gancho Stop do Claude Code. Roda quando a conversa vai terminar uma resposta e
lê o registro dela (transcript). Só vale em projetos com `linear_time` no
`.claude/konoha.json` (projeto.py) e só em conversas com trabalho: as que
travaram uma tarefa no Linear com a própria marca (`c-<8 letras>`, a mesma do
quadro-linear.py). Conversa só de pergunta não é mexida.

Confere três coisas (referência do Tech Lead §6.2):
1. A conversa foi renomeada (`set_session_title` em "self") ao menos uma vez.
2. Está num dos grupos de andamento (`move_sessions` com "self").
3. Se a última mensagem tem um "Sua vez:" que não é "nada agora", o grupo é
   `Sua vez`; se não tem, o grupo não é `Sua vez`.

Faltou algo: responde "block" com o que fazer, e a conversa arruma antes de
parar. Bloqueia uma vez só por resposta (stop_hook_active); qualquer erro vira
silêncio. Depois de qualquer mudança, rode `python testar-barra.py`.
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import projeto  # noqa: E402

GRUPOS = ["Análise", "Executando", "Sua vez", "Stand-by", "Finalizada"]
ESTADO = os.environ.get("KONOHA_ESTADO") or os.path.join(os.path.expanduser("~"), ".claude", "empresa-agentes-estado")
CACHE_GRUPOS = os.path.join(ESTADO, "grupos.json")


def _texto(conteudo) -> str:
    if isinstance(conteudo, str):
        return conteudo
    if isinstance(conteudo, list):
        return "".join(b.get("text", "") for b in conteudo if isinstance(b, dict))
    return ""


def ler_transcript(caminho: str):
    """Devolve (chamadas, resultados, ultima_fala): chamadas [(id, nome, entrada)], resultados {id: texto},
    ultima_fala = texto da última mensagem da conversa ao dono nesta resposta."""
    chamadas, resultados, ultima_fala = [], {}, ""
    with open(caminho, encoding="utf-8", errors="ignore") as f:
        for linha in f:
            try:
                reg = json.loads(linha)
            except ValueError:
                continue
            msg = reg.get("message") or {}
            conteudo = msg.get("content")
            if reg.get("type") == "user" and isinstance(conteudo, str) and not reg.get("isMeta"):
                ultima_fala = ""  # nova mensagem do dono: a resposta começa de novo
            if not isinstance(conteudo, list):
                continue
            for b in conteudo:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "tool_use":
                    chamadas.append((b.get("id"), b.get("name", ""), b.get("input") or {}))
                elif b.get("type") == "tool_result":
                    resultados[b.get("tool_use_id")] = _texto(b.get("content"))
                elif b.get("type") == "text" and reg.get("type") == "assistant" and b.get("text", "").strip():
                    ultima_fala = b["text"]
    return chamadas, resultados, ultima_fala


def mapa_grupos(chamadas, resultados) -> dict:
    """{id: nome} dos grupos, do que a conversa viu (list_groups, create_group) e do cache."""
    mapa = {}
    try:
        with open(CACHE_GRUPOS, encoding="utf-8") as f:
            mapa.update(json.load(f))
    except Exception:
        pass
    for ident, nome, _ in chamadas:
        if not nome.endswith(("__list_groups", "__create_group")):
            continue
        try:
            dados = json.loads(resultados.get(ident, ""))
        except ValueError:
            continue
        for g in dados if isinstance(dados, list) else [dados]:
            if isinstance(g, dict) and g.get("id") and g.get("name"):
                mapa[g["id"]] = g["name"]
    try:
        os.makedirs(ESTADO, exist_ok=True)
        with open(CACHE_GRUPOS, "w", encoding="utf-8") as f:
            json.dump(mapa, f, ensure_ascii=False)
    except Exception:
        pass
    return mapa


def situacao(chamadas, resultados, marca: str):
    """(tem_tarefa, renomeada, grupo_atual) a partir das chamadas desta conversa."""
    tem_tarefa = renomeada = False
    grupo_id = None
    for _, nome, entrada in chamadas:
        if nome.endswith("__save_issue") and marca in json.dumps(entrada, ensure_ascii=False):
            tem_tarefa = True
        elif nome.endswith("__set_session_title") and entrada.get("session_id") in ("self", None):
            renomeada = True
        elif nome.endswith("__move_sessions") and "self" in (entrada.get("session_ids") or []):
            grupo_id = entrada.get("group_id")
    grupo = mapa_grupos(chamadas, resultados).get(grupo_id) if grupo_id else None
    return tem_tarefa, renomeada, grupo


def pede_o_dono(fala: str) -> bool:
    m = re.search(r"sua vez\W{0,4}:?\**\s*(.+)", fala, re.I)
    if not m:
        return False
    return not re.search(r"nada agora|pode cuidar de outra coisa", m.group(1), re.I)


def problemas(tem_tarefa, renomeada, grupo, fala) -> list:
    if not tem_tarefa:
        return []
    faltas = []
    if not renomeada:
        faltas.append("renomeie esta conversa (`set_session_title`, \"self\") para `<Projeto> - <assunto da tarefa>`")
    esperado_sua_vez = pede_o_dono(fala)
    if grupo not in GRUPOS:
        alvo = "`Sua vez`" if esperado_sua_vez else "o grupo do andamento (`Análise`, `Executando`, `Stand-by` ou `Finalizada`)"
        faltas.append(f"mova esta conversa (`move_sessions`, \"self\") para {alvo}")
    elif esperado_sua_vez and grupo != "Sua vez":
        faltas.append(f"a mensagem pede algo ao dono, mas a conversa está em `{grupo}`: mova para `Sua vez`")
    elif not esperado_sua_vez and grupo == "Sua vez":
        faltas.append("a conversa está em `Sua vez`, mas a mensagem não pede nada ao dono: mova para o grupo do andamento de agora")
    return faltas


def main():
    try:
        entrada = json.load(sys.stdin)
    except Exception:
        return
    if not isinstance(entrada, dict) or entrada.get("stop_hook_active"):
        return
    if not projeto.config(entrada.get("cwd", "")).get("linear_time"):
        return
    try:
        chamadas, resultados, fala = ler_transcript(entrada["transcript_path"])
        marca = "c-" + (entrada.get("session_id") or "")[:8]
        faltas = problemas(*situacao(chamadas, resultados, marca), fala)
    except Exception:
        return
    if faltas:
        motivo = (
            "Barra lateral desatualizada (referência do Tech Lead §6.2). Antes de terminar: "
            + "; ".join(faltas)
            + ". Carregue as ferramentas pelo ToolSearch se precisar (mcp__ccd_sidebar__list_groups, "
            "move_sessions, mcp__ccd_session_mgmt__set_session_title). Não mande mensagem nova ao dono por causa disso."
        )
        print(json.dumps({"decision": "block", "reason": motivo}, ensure_ascii=False))


if __name__ == "__main__":
    main()
