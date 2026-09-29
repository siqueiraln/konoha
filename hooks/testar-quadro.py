"""Testes do quadro-linear.py. Rodar depois de qualquer mudança nele.

Sem argumento: só casos com dados inventados (não precisa de chave).
Com `--vivo <pasta de um projeto com linear_time no .claude/konoha.json>`:
também lê o quadro de verdade (precisa de LINEAR_API_KEY) e
mostra a foto como a conversa receberia. Não escreve nada no Linear.
"""

import importlib.util
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("quadro", os.path.join(AQUI, "quadro-linear.py"))
q = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q)

AGORA = datetime(2026, 9, 29, 18, 0, tzinfo=timezone.utc)
MINHA = "c-aaaaaaaa"
OUTRA = "c-bbbbbbbb"


def tarefa(ident, descricao, status="In Progress", comentarios=()):
    return {
        "id": "uuid-" + ident,
        "identifier": ident,
        "title": "Título " + ident,
        "description": descricao,
        "updatedAt": "2026-09-29T15:00:00.000Z",
        "state": {"name": status, "type": "started"},
        "project": {"name": "Mensageria"},
        "comments": {"nodes": [{"body": b, "createdAt": "2026-09-29T16:00:00.000Z"} for b in comentarios]},
    }


falhas = []


def caso(nome, cond):
    print(("ok   " if cond else "FALHA") + " " + nome)
    if not cond:
        falhas.append(nome)


# marca e pasta
caso("marca usa os 8 primeiros do id", q.marca("3fcca94c-8882-460f") == "c-3fcca94c")
import tempfile

PROJETO = tempfile.mkdtemp(prefix="konoha-teste-")
os.makedirs(os.path.join(PROJETO, ".claude"))
with open(os.path.join(PROJETO, ".claude", "konoha.json"), "w", encoding="utf-8") as f:
    f.write('{"linear_time": "Vila"}')
os.makedirs(os.path.join(PROJETO, "src", "fundo"))
SEM_CONFIG = tempfile.mkdtemp(prefix="konoha-sem-config-")
caso("projeto com konoha.json dá o time", q.time_da_pasta(PROJETO) == "Vila")
caso("subpasta do projeto também", q.time_da_pasta(os.path.join(PROJETO, "src", "fundo")) == "Vila")
caso("pasta sem konoha.json não roda", q.time_da_pasta(SEM_CONFIG) is None)

# trava
com_trava = f"🔒 Com a conversa [Lembretes](claude://x) · {OUTRA} · desde 29/09 10:00\nTexto\nSessão: Lembretes"
caso("lê a trava na 1ª linha", q.marca_na(q.trava(com_trava)) == OUTRA)
caso("trava fora da 1ª linha não conta", q.trava(f"Texto\n🔒 {OUTRA}") is None)
caso("descrição vazia não quebra", q.trava(None) is None and q.trava("") is None)

# foto
sit = lambda m, agora: "ATIVA, teste"
andando = [
    tarefa("STR-1", f"🔒 Com a conversa [Minha](l) · {MINHA} · desde x"),
    tarefa("STR-2", com_trava),
    tarefa("STR-3", "Sem trava\nSessão: FollowUP - IA"),
]
mudou = [andando[0], tarefa("STR-9", "x", status="Done")]
foto = q.texto_foto(MINHA, "Vila", andando, mudou, AGORA, sit=sit)
caso("foto dá a marca desta conversa", f"Marca desta conversa: {MINHA}" in foto)
caso("foto reconhece a própria trava", "STR-1 Título STR-1 [Mensageria]: trava DESTA conversa" in foto)
caso("foto mostra quem travou e se vive", f"STR-2 Título STR-2 [Mensageria]: travada por Com a conversa [Lembretes](claude://x) ({OUTRA}, ATIVA, teste)" in foto)
caso("foto usa a linha Sessão quando não há trava", "sem trava; Sessão: FollowUP - IA" in foto)
caso("mudou em 24h não repete o que está andando", foto.count("- STR-1 ") == 1 and "STR-9 Título STR-9: Done" in foto)
caso("foto com quadro vazio", "- nada" in q.texto_foto(MINHA, "Vila", [], [], AGORA, sit=sit))

# situação da conversa dona da trava (arquivo da conversa)
caso("conversa inexistente", q.situacao("c-00000000", AGORA) == "conversa não achada neste computador")

# mudanças lá fora
minha = tarefa("STR-1", f"🔒 · {MINHA}", comentarios=[f"Entrega conferida\n— Minha · {MINHA}"])
caso("comentário assinado por mim não avisa", q.texto_mudancas(MINHA, [minha], [minha]) == "")
de_fora = tarefa("STR-1", f"🔒 · {MINHA}", comentarios=[f"Toques conferidos\n— Testes pendentes · {OUTRA}"])
aviso = q.texto_mudancas(MINHA, [de_fora], [de_fora])
caso("comentário de outra conversa avisa", "comentário de fora" in aviso and "Toques conferidos" in aviso)
sem_assinatura = tarefa("STR-1", f"🔒 · {MINHA}", comentarios=["Comentário do dono pelo Linear"])
caso("comentário do dono (sem marca) também avisa", "Comentário do dono" in q.texto_mudancas(MINHA, [sem_assinatura], [sem_assinatura]))
tomada = tarefa("STR-1", f"🔒 Com a conversa [Outra](l) · {OUTRA} · desde y")
aviso = q.texto_mudancas(MINHA, [], [tomada])
caso("trava tirada desta conversa avisa quem pegou", "NÃO é mais desta conversa" in aviso and "[Outra](l)" in aviso)
solta = tarefa("STR-1", "Última conversa: [Minha](l) · até z", status="Done")
caso("trava solta avisa sem trava", "sem trava" in q.texto_mudancas(MINHA, [], [solta]))
caso("nada mudou, nada diz", q.texto_mudancas(MINHA, [], []) == "")

# o gancho inteiro, pela entrada padrão
def rodar(entrada, env=None):
    r = subprocess.run([sys.executable, os.path.join(AQUI, "quadro-linear.py")], input=json.dumps(entrada),
                       capture_output=True, text=True, encoding="utf-8", env=env, timeout=20)
    return r.returncode, r.stdout.strip()

cod, saida = rodar({"hook_event_name": "UserPromptSubmit", "session_id": "x", "cwd": SEM_CONFIG})
caso("projeto sem konoha.json: sai calado", cod == 0 and saida == "")
cod, saida = rodar({"hook_event_name": "SessionStart"})
caso("entrada incompleta: sai calado", cod == 0 and saida == "")
cod, saida = rodar("não é json")
caso("entrada quebrada: sai calado", cod == 0 and saida == "")

if "--vivo" in sys.argv:
    i = sys.argv.index("--vivo")
    VIVO = sys.argv[i + 1] if len(sys.argv) > i + 1 else os.getcwd()
    TIME_VIVO = q.time_da_pasta(VIVO)
    caso(f"vivo: {VIVO} tem linear_time no konoha.json", bool(TIME_VIVO))
    cod, saida = rodar({"hook_event_name": "SessionStart", "session_id": "teste000-vivo", "cwd": VIVO})
    texto = json.loads(saida)["hookSpecificOutput"]["additionalContext"] if saida else ""
    print("\n--- foto real ---\n" + texto + "\n---")
    caso("vivo: foto veio do Linear", "Andando agora" in texto)
    cod, saida = rodar({"hook_event_name": "UserPromptSubmit", "session_id": "teste000-vivo", "cwd": VIVO})
    caso("vivo: mensagem sem tarefa travada sai calada", cod == 0 and saida == "")
    # o gancho engole erro; aqui a consulta de cada mensagem roda direto, para o erro aparecer
    try:
        key = q.chave()
        d = q.consultar(key, q.Q_MINHAS, {"time": TIME_VIVO, "marca": "Sessão", "ids": [], "desde": "-P2D"})
        ids = [t["id"] for t in d["minhas"]["nodes"]][:3]
        d2 = q.consultar(key, q.Q_MINHAS, {"time": TIME_VIVO, "marca": "c-nada0000", "ids": ids, "desde": "-P2D"})
        caso("vivo: consulta de cada mensagem aceita pelo Linear", bool(ids) and len(d2["antigas"]["nodes"]) == len(ids))
    except Exception as erro:
        caso(f"vivo: consulta de cada mensagem aceita pelo Linear ({erro})", False)
    try:
        os.remove(os.path.join(q.ESTADO, "teste000-vivo.json"))
    except OSError:
        pass

print(f"\n{'TODOS PASSARAM' if not falhas else str(len(falhas)) + ' FALHARAM'}")
sys.exit(1 if falhas else 0)
