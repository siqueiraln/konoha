"""Testes do limpeza-git.py com repositórios de mentira. Rodar depois de qualquer mudança nele."""

import importlib.util
import os
import subprocess
import sys
import tempfile
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("limpeza", os.path.join(AQUI, "limpeza-git.py"))
L = importlib.util.module_from_spec(spec)
spec.loader.exec_module(L)


def g(pasta, *args):
    r = subprocess.run(["git", "-C", pasta, *args], capture_output=True, text=True)
    assert r.returncode == 0, (args, r.stderr)
    return r.stdout.strip()


def commit(pasta, arquivo, texto="x"):
    with open(os.path.join(pasta, arquivo), "w") as f:
        f.write(texto)
    g(pasta, "add", arquivo)
    g(pasta, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", arquivo)
    return g(pasta, "rev-parse", "HEAD")


base = tempfile.mkdtemp(prefix="konoha-limpeza-")
origem = os.path.join(base, "origem.git")
subprocess.run(["git", "init", "-q", "--bare", "-b", "main", origem], check=True)
repo = os.path.join(base, "repo")
subprocess.run(["git", "clone", "-q", origem, repo], check=True, capture_output=True)
g(repo, "checkout", "-q", "-b", "main")
commit(repo, "a.txt")
g(repo, "push", "-q", "origin", "main")

# 1. PR juntado (merge): branch com pasta de trabalho limpa, também no GitHub
wt1 = os.path.join(base, "wt-juntado")
g(repo, "worktree", "add", "-q", "-b", "feat/juntada", wt1)
ponta1 = commit(wt1, "b.txt")
g(wt1, "push", "-q", "origin", "feat/juntada")
g(repo, "merge", "-q", "--no-ff", "-m", "merge", "feat/juntada")
g(repo, "push", "-q", "origin", "main")

# 2. PR juntado mas a pasta tem arquivo novo não salvo: nada da branch sai
wt2 = os.path.join(base, "wt-suja")
g(repo, "worktree", "add", "-q", "-b", "feat/suja", wt2)
ponta2 = commit(wt2, "c.txt")
g(wt2, "push", "-q", "origin", "feat/suja")
g(repo, "merge", "-q", "--no-ff", "-m", "merge2", "feat/suja")
g(repo, "push", "-q", "origin", "main")
with open(os.path.join(wt2, "rascunho.txt"), "w") as f:
    f.write("trabalho não salvo")

# 3. PR juntado e depois ganhou commit novo: fica
wt3 = os.path.join(base, "wt-continuou")
g(repo, "worktree", "add", "-q", "-b", "feat/continuou", wt3)
ponta3_juntada = commit(wt3, "d.txt")
commit(wt3, "e.txt")

# 4. Branch nova, recém-criada da principal, sem commit: fica
g(repo, "branch", "feat/nova")

# 5. Trabalho em andamento sem PR: fica
wt5 = os.path.join(base, "wt-andando")
g(repo, "worktree", "add", "-q", "-b", "feat/andando", wt5)
commit(wt5, "f.txt")

# 6. Branch no GitHub de outra pessoa, juntada, sem PR seu: fica
g(repo, "push", "-q", "origin", "main:outra/pessoa")

# 7. PR juntado mas é a pasta onde a conversa está: a pasta fica
wt7 = os.path.join(base, "wt-da-conversa")
g(repo, "worktree", "add", "-q", "-b", "feat/conversa", wt7)
ponta7 = commit(wt7, "g.txt")

g(repo, "fetch", "-q", "--prune", "origin")
juntados = {"feat/juntada": ponta1, "feat/suja": ponta2, "feat/continuou": ponta3_juntada, "feat/conversa": ponta7}
acoes = L.planejar(repo, wt7, juntados)
alvos = {(t, os.path.normcase(a) if t == "pasta" else a) for t, a, _ in acoes}

falhas = []


def caso(nome, cond):
    print(("ok   " if cond else "FALHA") + " " + nome)
    if not cond:
        falhas.append(nome)


nc = os.path.normcase
caso("PR juntado: apaga a pasta", ("pasta", nc(wt1)) in alvos)
caso("PR juntado: apaga a branch local", ("branch", "feat/juntada") in alvos)
caso("PR juntado: apaga a branch no GitHub", ("github", "feat/juntada") in alvos)
caso("pasta com arquivo não salvo: fica, e a branch dela também", ("pasta", nc(wt2)) not in alvos and ("branch", "feat/suja") not in alvos)
caso("branch no GitHub da pasta suja pode sair (o conteúdo já está na principal)", ("github", "feat/suja") in alvos)
caso("PR juntado que ganhou commit novo: fica", not any(a == "feat/continuou" or a == nc(wt3) for _, a in alvos))
caso("branch recém-criada da principal: fica", ("branch", "feat/nova") not in alvos)
caso("trabalho sem PR: fica", not any(a in ("feat/andando", nc(wt5)) for _, a in alvos))
caso("branch de outra pessoa no GitHub: fica", ("github", "outra/pessoa") not in alvos)
caso("pasta onde a conversa está: fica", ("pasta", nc(wt7)) not in alvos and ("branch", "feat/conversa") not in alvos)
caso("pasta principal nunca", ("pasta", nc(repo)) not in alvos)

feitas = L.executar(repo, acoes)
caso("executa tudo o que planejou", len(feitas) == len(acoes))
caso("pasta apagada de verdade", not os.path.exists(wt1))
caso("trabalho não salvo continua lá", os.path.exists(os.path.join(wt2, "rascunho.txt")))

print(f"\n{'TODOS PASSARAM' if not falhas else str(len(falhas)) + ' FALHARAM'}")
sys.exit(1 if falhas else 0)
