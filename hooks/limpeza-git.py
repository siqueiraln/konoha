"""Limpeza do que já foi juntado: pastas de trabalho, branches locais e do GitHub.

Pedido do dono: PR juntado não deixa lixo para trás. Só apaga o que tem certeza
de estar na versão principal e sem trabalho pendente:

- **Branch de PR juntado seu** (gh pr list --state merged --author @me), cuja
  ponta é exatamente a que foi juntada: apaga a pasta de trabalho dela (se
  estiver limpa), a branch local e a branch no GitHub.
- **Branch local antiga já contida na principal** (sem PR, ponta mais velha que
  7 dias): apaga só a local. Branch recém-criada da principal fica.
- **Pasta de trabalho sem branch** (detached) limpa, contida na principal e
  parada há mais de 1 dia: apaga a pasta.
- Nunca: a pasta principal, a pasta onde a conversa está, pasta com qualquer
  arquivo alterado ou novo, branch de outra pessoa no GitHub.

Modos:
    python limpeza-git.py [--simular]   na pasta do projeto: limpa agora e conta o que fez
    (gancho SessionStart)               lança a limpeza em segundo plano e volta na hora;
                                        só em projetos com `.claude/konoha.json`
Registro em ~/.claude/empresa-agentes-estado/limpeza-git.log.
Depois de qualquer mudança, rode `python testar-limpeza.py`.
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import projeto  # noqa: E402

ESTADO = os.environ.get("KONOHA_ESTADO") or os.path.join(os.path.expanduser("~"), ".claude", "empresa-agentes-estado")
DIAS_BRANCH_ANTIGA = 7
# Windows: sem isto, cada git/gh chamado em segundo plano abre uma janela de terminal por um instante.
SEM_JANELA = 0x08000000 if os.name == "nt" else 0  # CREATE_NO_WINDOW
HORAS_PASTA_PARADA = 24


def git(pasta, *args, timeout=30):
    r = subprocess.run(["git", "-C", pasta, *args], capture_output=True, text=True, encoding="utf-8",
                       errors="ignore", timeout=timeout, stdin=subprocess.DEVNULL, creationflags=SEM_JANELA)
    return r.returncode, r.stdout.strip()


def registrar(texto):
    try:
        os.makedirs(ESTADO, exist_ok=True)
        with open(os.path.join(ESTADO, "limpeza-git.log"), "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat(timespec='seconds')} {texto}\n")
    except Exception:
        pass


def prs_juntados(pasta):
    """{branch: ponta juntada} dos seus PRs juntados; {} se o gh não responder."""
    try:
        r = subprocess.run(["gh", "pr", "list", "--state", "merged", "--author", "@me", "--limit", "200",
                            "--json", "headRefName,headRefOid"], cwd=pasta, capture_output=True, text=True,
                           encoding="utf-8", timeout=30, stdin=subprocess.DEVNULL, creationflags=SEM_JANELA)
        return {p["headRefName"]: p["headRefOid"] for p in json.loads(r.stdout or "[]")}
    except Exception:
        return {}


def pastas_de_trabalho(pasta):
    _, saida = git(pasta, "worktree", "list", "--porcelain")
    itens, atual = [], {}
    for linha in saida.splitlines() + [""]:
        if not linha.strip():
            if atual:
                itens.append(atual)
            atual = {}
        elif linha.startswith("worktree "):
            atual["caminho"] = linha[9:]
        elif linha.startswith("HEAD "):
            atual["ponta"] = linha[5:]
        elif linha.startswith("branch refs/heads/"):
            atual["branch"] = linha[18:]
    return itens


def contida_na_principal(pasta, ponta):
    return git(pasta, "merge-base", "--is-ancestor", ponta, "origin/main")[0] == 0


def limpa(caminho):
    cod, saida = git(caminho, "status", "--porcelain")
    return cod == 0 and saida == ""


def mesma_pasta(a, b):
    return os.path.normcase(os.path.abspath(a)).rstrip("\\/") == os.path.normcase(os.path.abspath(b)).rstrip("\\/")


def dentro(filho, pai):
    f, p = os.path.normcase(os.path.abspath(filho)), os.path.normcase(os.path.abspath(pai))
    return f == p or f.startswith(p.rstrip("\\/") + os.sep)


def planejar(pasta, cwd, juntados):
    """Lista de ações [(tipo, alvo, motivo)] sem executar nada."""
    acoes = []
    pastas = pastas_de_trabalho(pasta)
    if not pastas:
        return acoes
    principal = pastas[0]["caminho"]
    em_uso = {}
    for p in pastas:
        if p.get("branch"):
            em_uso[p["branch"]] = p
    agora = time.time()

    for p in pastas[1:]:
        caminho, branch, ponta = p["caminho"], p.get("branch"), p.get("ponta", "")
        if mesma_pasta(caminho, principal) or dentro(cwd, caminho) or not os.path.isdir(caminho):
            continue
        if not limpa(caminho):
            continue
        if branch and juntados.get(branch) == ponta:
            acoes.append(("pasta", caminho, f"PR juntado ({branch})"))
        elif not branch and contida_na_principal(pasta, ponta):
            try:
                parada = (agora - os.path.getmtime(caminho)) / 3600 > HORAS_PASTA_PARADA
            except OSError:
                parada = False
            if parada:
                acoes.append(("pasta", caminho, "sem branch, já contida na principal"))

    removidas = {a[1] for a in acoes if a[0] == "pasta"}
    _, saida = git(pasta, "for-each-ref", "--format=%(refname:short) %(objectname) %(committerdate:unix)", "refs/heads")
    for linha in saida.splitlines():
        nome, ponta, data = (linha.split(" ") + ["", "", "0"])[:3]
        if nome in ("main", "master"):
            continue
        uso = em_uso.get(nome)
        if uso and uso["caminho"] not in removidas:
            continue  # aberta numa pasta que fica
        if juntados.get(nome) == ponta:
            acoes.append(("branch", nome, "PR juntado"))
        elif contida_na_principal(pasta, ponta) and agora - int(data or 0) > DIAS_BRANCH_ANTIGA * 86400:
            acoes.append(("branch", nome, "antiga e já contida na principal"))

    _, saida = git(pasta, "for-each-ref", "--format=%(refname:short) %(objectname)", "refs/remotes/origin")
    for linha in saida.splitlines():
        nome, ponta = (linha.split(" ") + [""])[:2]
        curto = nome[len("origin/"):] if nome.startswith("origin/") else nome
        if curto in ("HEAD", "main", "master", "origin"):
            continue
        if juntados.get(curto) == ponta:
            acoes.append(("github", curto, "PR juntado"))
    return acoes


def executar(pasta, acoes):
    feitas = []
    for tipo, alvo, motivo in acoes:
        if tipo == "pasta":
            cod, _ = git(pasta, "worktree", "remove", alvo)
        elif tipo == "branch":
            cod, _ = git(pasta, "branch", "-D" if motivo == "PR juntado" else "-d", alvo)
        else:
            cod, _ = git(pasta, "push", "origin", "--delete", alvo, timeout=60)
        registrar(f"{'ok ' if cod == 0 else 'ERRO'} {tipo} {alvo} ({motivo})")
        if cod == 0:
            feitas.append((tipo, alvo, motivo))
    git(pasta, "worktree", "prune")
    return feitas


def limpar(cwd, simular=False):
    cod, pasta = git(cwd, "rev-parse", "--show-toplevel")
    if cod != 0:
        return []
    _, comum = git(cwd, "rev-parse", "--path-format=absolute", "--git-common-dir")
    principal = os.path.dirname(comum) if comum else pasta
    git(principal, "fetch", "--prune", "origin", timeout=60)
    acoes = planejar(principal, cwd, prs_juntados(principal))
    return acoes if simular else executar(principal, acoes)


def resumo(acoes):
    conta = {t: sum(1 for a in acoes if a[0] == t) for t in ("pasta", "branch", "github")}
    return f"{conta['pasta']} pastas de trabalho, {conta['branch']} branches locais, {conta['github']} branches no GitHub"


def main():
    if "--segundo-plano" in sys.argv:
        cwd = sys.argv[sys.argv.index("--segundo-plano") + 1]
        try:
            feitas = limpar(cwd)
            registrar(f"fim ({cwd}): {resumo(feitas)}")
        except Exception as erro:
            registrar(f"ERRO geral: {type(erro).__name__}: {erro}")
        return
    if sys.stdin.isatty() or "--simular" in sys.argv or "--agora" in sys.argv:
        simular = "--simular" in sys.argv
        acoes = limpar(os.getcwd(), simular=simular)
        for tipo, alvo, motivo in acoes:
            print(f"{'apagaria' if simular else 'apagado'}: {tipo} {alvo} ({motivo})")
        print(("Simulação: " if simular else "Limpo: ") + resumo(acoes))
        return
    try:  # gancho SessionStart: lança em segundo plano e volta na hora
        entrada = json.load(sys.stdin)
        cwd = entrada.get("cwd", "")
        if not isinstance(entrada, dict) or not projeto.config(cwd):
            return
        flags = SEM_JANELA | 0x00000200 if os.name == "nt" else 0  # CREATE_NO_WINDOW | NEW_PROCESS_GROUP
        subprocess.Popen([sys.executable, os.path.abspath(__file__), "--segundo-plano", cwd],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         creationflags=flags, close_fds=True)
    except Exception:
        return


if __name__ == "__main__":
    main()
