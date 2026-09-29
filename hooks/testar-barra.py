"""Testes do barra-lateral.py. Rodar depois de qualquer mudança nele.

Monta registros de conversa de mentira e confere quando o conferente bloqueia.
"""

import json
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
SESSAO = "abcd1234-0000-0000-0000-000000000000"
MARCA = "c-abcd1234"

PROJETO = tempfile.mkdtemp(prefix="konoha-barra-")
os.makedirs(os.path.join(PROJETO, ".claude"))
with open(os.path.join(PROJETO, ".claude", "konoha.json"), "w", encoding="utf-8") as f:
    f.write('{"linear_time": "Vila"}')
SEM_CONFIG = tempfile.mkdtemp(prefix="konoha-barra-sem-")
ESTADO_TESTE = tempfile.mkdtemp(prefix="konoha-barra-estado-")

GRUPOS = [{"id": "g-analise", "name": "Análise"}, {"id": "g-exec", "name": "Executando"},
          {"id": "g-suavez", "name": "Sua vez"}, {"id": "g-standby", "name": "Stand-by"},
          {"id": "g-fim", "name": "Finalizada"}]


def usuario(texto):
    return {"type": "user", "message": {"role": "user", "content": texto}}


def ferramenta(ident, nome, entrada, resultado=""):
    return [
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": ident, "name": nome, "input": entrada}]}},
        {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": ident, "content": [{"type": "text", "text": resultado}]}]}},
    ]


def fala(texto):
    return {"type": "assistant", "message": {"content": [{"type": "text", "text": texto}]}}


def trava():
    return ferramenta("t1", "mcp__linear__save_issue", {"id": "STR-9", "description": f"🔒 Com a conversa [X](l) · {MARCA} · desde hoje"})


def titulo():
    return ferramenta("t2", "mcp__ccd_session_mgmt__set_session_title", {"session_id": "self", "title": "Agenda - Reagendar"})


def grupos():
    return ferramenta("t3", "mcp__ccd_sidebar__list_groups", {}, json.dumps(GRUPOS))


def mover(gid, ident="t4"):
    return ferramenta(ident, "mcp__ccd_sidebar__move_sessions", {"session_ids": ["self"], "group_id": gid})


def rodar(registros, cwd=PROJETO, ativo=False):
    arq = tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8")
    for r in registros:
        arq.write(json.dumps(r, ensure_ascii=False) + "\n")
    arq.close()
    entrada = {"hook_event_name": "Stop", "session_id": SESSAO, "transcript_path": arq.name, "cwd": cwd, "stop_hook_active": ativo}
    env = dict(os.environ, KONOHA_ESTADO=ESTADO_TESTE)
    r = subprocess.run([sys.executable, os.path.join(AQUI, "barra-lateral.py")], input=json.dumps(entrada),
                       capture_output=True, text=True, encoding="utf-8", timeout=20, env=env)
    os.unlink(arq.name)
    return json.loads(r.stdout)["reason"] if r.stdout.strip() else ""


falhas = []


def caso(nome, cond):
    print(("ok   " if cond else "FALHA") + " " + nome)
    if not cond:
        falhas.append(nome)


def flat(*partes):
    saida = []
    for p in partes:
        saida.extend(p if isinstance(p, list) else [p])
    return saida


SUA_VEZ = "O que mudou: PR aberto.\n\nSua vez: juntar o PR #12."
NADA = "O que mudou: seguindo.\n\nSua vez: nada agora, pode cuidar de outra coisa."

caso("pergunta sem tarefa: não bloqueia", rodar(flat(usuario("como funciona?"), fala("Funciona assim."))) == "")
caso("projeto sem konoha.json: não bloqueia", rodar(flat(usuario("x"), trava(), fala(SUA_VEZ)), cwd=SEM_CONFIG) == "")
r = rodar(flat(usuario("faz"), trava(), fala(NADA)))
caso("tarefa sem título nem grupo: bloqueia pedindo os dois", "renomeie" in r and "mova" in r)
caso("tudo certo em Executando: não bloqueia", rodar(flat(usuario("faz"), trava(), titulo(), grupos(), mover("g-exec"), fala(NADA))) == "")
r = rodar(flat(usuario("faz"), trava(), titulo(), grupos(), mover("g-exec"), fala(SUA_VEZ)))
caso("pede algo ao dono mas está em Executando: bloqueia pedindo Sua vez", "mova para `Sua vez`" in r)
caso("pede algo ao dono e está em Sua vez: não bloqueia", rodar(flat(usuario("faz"), trava(), titulo(), grupos(), mover("g-suavez"), fala(SUA_VEZ))) == "")
r = rodar(flat(usuario("juntei"), trava(), titulo(), grupos(), mover("g-suavez"), fala(NADA)))
caso("ficou em Sua vez sem pedir nada: bloqueia", "não pede nada ao dono" in r)
caso("mudou de Sua vez para Executando nesta resposta: não bloqueia",
     rodar(flat(usuario("juntei"), trava(), titulo(), grupos(), mover("g-suavez"), mover("g-exec", "t5"), fala(NADA))) == "")
caso("segunda parada seguida (stop_hook_active): não bloqueia de novo", rodar(flat(usuario("faz"), trava(), fala(NADA)), ativo=True) == "")
caso("Sua vez em negrito também conta",
     "mova para `Sua vez`" in rodar(flat(usuario("faz"), trava(), titulo(), grupos(), mover("g-exec"), fala("**Sua vez:** testar na Idealize."))))
caso("trava de outra conversa não conta como tarefa desta",
     rodar(flat(usuario("faz"), ferramenta("t9", "mcp__linear__save_issue", {"description": "🔒 · c-99999999"}), fala(NADA))) == "")
caso("registro quebrado: não bloqueia", rodar([{"type": "lixo"}, "não é objeto"]) == "")

print(f"\n{'TODOS PASSARAM' if not falhas else str(len(falhas)) + ' FALHARAM'}")
sys.exit(1 if falhas else 0)
