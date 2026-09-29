"""Quadro do Linear entregue à conversa, sem depender da memória do agente.

Gancho do Claude Code para dois momentos:
- SessionStart (abrir, retomar, depois de resumir a memória): entrega a marca
  desta conversa e a foto do quadro do time (o que está andando, com quem, há
  quanto tempo a conversa dona da trava não se mexe, e o que mudou em 24 h).
- UserPromptSubmit (cada mensagem do dono): olha as tarefas travadas por esta
  conversa e avisa o que mudou lá fora desde a última olhada: comentário de
  outra conversa, trava tirada. Sem mudança, não diz nada.

A trava na descrição da tarefa carrega a marca `c-<8 letras>`, tirada do id
interno da conversa. Com a marca o gancho acha as tarefas da conversa e a
última atividade dela (a data do arquivo da conversa em ~/.claude/projects).

Só roda em projetos com `linear_time` no `.claude/konoha.json` (projeto.py). Qualquer erro vira silêncio (nunca trava
a conversa); na abertura, vira uma linha dizendo que o quadro não veio.
A chave vem de LINEAR_API_KEY (ambiente ou registro do Windows) e só vai para
api.linear.app.

Depois de qualquer mudança, rode `python testar-quadro.py` nesta pasta.
"""

import glob
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import projeto  # noqa: E402

API = "https://api.linear.app/graphql"
BRASILIA = timezone(timedelta(hours=-3))
PARADA_HORAS = 12
ESTADO = os.path.join(os.path.expanduser("~"), ".claude", "empresa-agentes-estado")
PROJETOS = os.path.join(os.path.expanduser("~"), ".claude", "projects")

# ---------------------------------------------------------------- comum


def marca(session_id: str) -> str:
    return "c-" + (session_id or "")[:8]


def time_da_pasta(cwd: str):
    """O time do Linear do projeto, de `.claude/konoha.json` (campo linear_time)."""
    return projeto.config(cwd).get("linear_time") or None


def chave():
    valor = os.environ.get("LINEAR_API_KEY")
    if valor:
        return valor.strip()
    try:  # guardada depois que o app abriu: só está no registro
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as reg:
            return str(winreg.QueryValueEx(reg, "LINEAR_API_KEY")[0]).strip()
    except Exception:
        return None


def consultar(key: str, query: str, variaveis: dict) -> dict:
    corpo = json.dumps({"query": query, "variables": variaveis}).encode()
    pedido = urllib.request.Request(
        API, data=corpo, headers={"Content-Type": "application/json", "Authorization": key}
    )
    with urllib.request.urlopen(pedido, timeout=6) as resposta:
        dados = json.load(resposta)
    if dados.get("errors"):
        raise RuntimeError(dados["errors"][0].get("message", "erro do Linear"))
    return dados["data"]


def data(iso: str) -> datetime:
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))


def hora(dt: datetime) -> str:
    return dt.astimezone(BRASILIA).strftime("%d/%m %H:%M")


def trava(descricao: str):
    """Primeira linha da descrição, se for uma trava; senão None."""
    primeira = (descricao or "").strip().splitlines()[0:1]
    if primeira and primeira[0].lstrip().startswith("🔒"):
        return primeira[0].strip()
    return None


def marca_na(texto: str):
    import re

    achado = re.search(r"\bc-[0-9a-f]{8}\b", texto or "")
    return achado.group(0) if achado else None


def ultima_atividade(marca_conversa: str):
    """Data do arquivo da conversa dona da marca, ou None se não achar."""
    curto = marca_conversa[2:]
    arquivos = glob.glob(os.path.join(PROJETOS, "*", curto + "*.jsonl"))
    if not arquivos:
        return None
    return datetime.fromtimestamp(max(os.path.getmtime(a) for a in arquivos), tz=timezone.utc)


def situacao(marca_conversa: str, agora: datetime) -> str:
    ultima = ultima_atividade(marca_conversa)
    if ultima is None:
        return "conversa não achada neste computador"
    horas = (agora - ultima).total_seconds() / 3600
    quando = f"última atividade {hora(ultima)}"
    return f"PARADA, {quando}" if horas > PARADA_HORAS else f"ATIVA, {quando}"


def ler_estado(session_id: str) -> dict:
    try:
        with open(os.path.join(ESTADO, session_id + ".json"), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def gravar_estado(session_id: str, estado: dict):
    os.makedirs(ESTADO, exist_ok=True)
    with open(os.path.join(ESTADO, session_id + ".json"), "w", encoding="utf-8") as f:
        json.dump(estado, f)


def responder(evento: str, texto: str):
    if texto:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": evento, "additionalContext": texto}}, ensure_ascii=False))


# ---------------------------------------------------------------- consultas

CAMPOS = "id identifier title description updatedAt state { name type } project { name }"

Q_FOTO = """
query($time: String!, $desde: DateTimeOrDuration!) {
  andando: issues(first: 50, filter: { team: { name: { eq: $time } }, state: { type: { eq: "started" } } }) {
    nodes { %s }
  }
  mudou: issues(first: 30, orderBy: updatedAt, filter: { team: { name: { eq: $time } }, updatedAt: { gt: $desde } }) {
    nodes { %s }
  }
}
""" % (CAMPOS, CAMPOS)

Q_MINHAS = """
query($time: String!, $marca: String!, $ids: [ID!], $desde: DateTimeOrDuration!) {
  minhas: issues(first: 10, filter: { team: { name: { eq: $time } }, description: { contains: $marca } }) {
    nodes { %s comments(filter: { createdAt: { gt: $desde } }) { nodes { body createdAt } } }
  }
  antigas: issues(first: 10, filter: { id: { in: $ids } }) {
    nodes { %s }
  }
}
""" % (CAMPOS, CAMPOS)


# ---------------------------------------------------------------- textos (puros, testáveis)


def texto_foto(minha_marca: str, time_: str, andando: list, mudou: list, agora: datetime, sit=situacao) -> str:
    linhas = [
        f"[Quadro do Linear, time {time_}, entregue automaticamente em {hora(agora)}]",
        f"Marca desta conversa: {minha_marca}. Use na trava (🔒 ... · {minha_marca} · desde ...) e na assinatura dos comentários.",
        "",
        "Andando agora (In Progress):",
    ]
    if not andando:
        linhas.append("- nada")
    for t in andando:
        tv = trava(t["description"])
        dono = marca_na(tv) if tv else None
        if dono == minha_marca:
            quem = "trava DESTA conversa"
        elif dono:
            quem = f"travada por {tv.lstrip('🔒 ').split(' · ')[0]} ({dono}, {sit(dono, agora)})"
        else:
            origem = next((l for l in (t["description"] or "").splitlines() if l.startswith("Sessão")), "sem trava")
            quem = f"sem trava; {origem.strip()}"
        linhas.append(f"- {t['identifier']} {t['title']} [{(t.get('project') or {}).get('name', '-')}]: {quem}")
    ids_andando = {t["identifier"] for t in andando}
    outras = [t for t in mudou if t["identifier"] not in ids_andando]
    linhas += ["", "Mudou nas últimas 24 h (fora as de cima):"]
    if not outras:
        linhas.append("- nada")
    for t in outras:
        linhas.append(f"- {t['identifier']} {t['title']}: {t['state']['name']} ({hora(data(t['updatedAt']))})")
    linhas += [
        "",
        "Regras: referência do Tech Lead §6.1 (Foto do quadro, A trava da tarefa). Ao dono, só o que toca o pedido dele.",
    ]
    return "\n".join(linhas)


def texto_mudancas(minha_marca: str, minhas: list, antigas: list) -> str:
    """antigas: tarefas que eram desta conversa na última olhada. Devolve '' se nada mudou lá fora."""
    avisos = []
    ids_minhas = {t["identifier"] for t in minhas}
    for t in antigas:
        if t["identifier"] not in ids_minhas:
            tv = trava(t["description"])
            quem = f"agora está com {tv.lstrip('🔒 ').split(' · ')[0]}" if tv else "sem trava"
            avisos.append(f"- {t['identifier']} {t['title']}: a trava NÃO é mais desta conversa ({quem}). Pare de mexer nela e diga ao dono.")
    for t in minhas:
        de_fora = [c for c in t.get("comments", {}).get("nodes", []) if minha_marca not in (c["body"] or "")]
        for c in de_fora:
            corpo = " ".join((c["body"] or "").split())
            avisos.append(f"- {t['identifier']}: comentário de fora ({hora(data(c['createdAt']))}): {corpo[:300]}")
    if not avisos:
        return ""
    return "\n".join(["[Mudou lá fora, nas tarefas travadas por esta conversa]"] + avisos + ["Confira na fonte antes de afirmar (referência do Tech Lead §6.1, Mudou lá fora?)."])


# ---------------------------------------------------------------- momentos


def abertura(entrada: dict, key: str, time_: str):
    agora = datetime.now(timezone.utc)
    minha = marca(entrada["session_id"])
    dados = consultar(key, Q_FOTO, {"time": time_, "desde": "-P1D"})
    texto = texto_foto(minha, time_, dados["andando"]["nodes"], dados["mudou"]["nodes"], agora)
    estado = ler_estado(entrada["session_id"])
    estado["olhada"] = agora.isoformat()
    gravar_estado(entrada["session_id"], estado)
    responder("SessionStart", texto)


def mensagem(entrada: dict, key: str, time_: str):
    agora = datetime.now(timezone.utc)
    minha = marca(entrada["session_id"])
    estado = ler_estado(entrada["session_id"])
    desde = estado.get("olhada") or (agora - timedelta(hours=1)).isoformat()
    antes = estado.get("minhas", {})
    ids = [v["id"] for v in antes.values() if v.get("id")]
    dados = consultar(key, Q_MINHAS, {"time": time_, "marca": minha, "ids": ids, "desde": desde})
    minhas = [t for t in dados["minhas"]["nodes"] if marca_na(trava(t["description"]) or "") == minha]
    texto = texto_mudancas(minha, minhas, dados["antigas"]["nodes"])
    novas_minhas = {t["identifier"]: {"id": t["id"]} for t in minhas}
    estado.update({"olhada": agora.isoformat(), "minhas": novas_minhas})
    gravar_estado(entrada["session_id"], estado)
    responder("UserPromptSubmit", texto)


def main():
    try:
        entrada = json.load(sys.stdin)
    except Exception:
        return
    if not isinstance(entrada, dict):
        return
    evento = entrada.get("hook_event_name")
    time_ = time_da_pasta(entrada.get("cwd", ""))
    if not time_ or not entrada.get("session_id"):
        return
    key = chave()
    if not key:
        if evento == "SessionStart":
            responder(evento, "[Quadro do Linear] Chave LINEAR_API_KEY não configurada: tire a foto do quadro você mesmo (referência §6.1).")
        return
    try:
        if evento == "SessionStart":
            abertura(entrada, key, time_)
        elif evento == "UserPromptSubmit":
            mensagem(entrada, key, time_)
    except Exception as erro:
        try:  # o aviso de cada mensagem falha calado; o registro é o único rastro
            os.makedirs(ESTADO, exist_ok=True)
            with open(os.path.join(ESTADO, "erros.log"), "a", encoding="utf-8") as f:
                f.write(f"{datetime.now(BRASILIA).isoformat()} {evento} {type(erro).__name__}: {erro}\n")
        except Exception:
            pass
        if evento == "SessionStart":
            responder(evento, f"[Quadro do Linear] Não consegui ler o quadro ({type(erro).__name__}): tire a foto você mesmo (referência §6.1). Marca desta conversa: {marca(entrada['session_id'])}.")


if __name__ == "__main__":
    main()
