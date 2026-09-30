"""Vigia do banco local: desliga o Supabase local parado há mais de 2 horas.

Pedido do dono (30/09/2026): os agentes ligavam bancos locais e deixavam ligados
horas depois de terminar, gastando a máquina. O vigia olha cada banco local ligado
(contêiner `supabase_db_<nome>`) e mede o uso pelas tabelas do schema `public`
(leituras e gravações somadas; os serviços internos do Supabase usam outros
schemas e não contam). Se o número não mexe há 2 horas, e o banco está ligado há
mais de 2 horas, desliga todos os contêineres daquele banco com `docker stop`.

Desligar não apaga nada: os dados ficam no volume, e `supabase start` liga de novo.

Modos:
    python vigia-banco.py [--simular]   olha agora e diz o que desligaria / desligou
    (gancho SessionStart ou Stop)       lança em segundo plano e volta na hora; roda
                                        no máximo a cada 10 minutos
Estado e registro em ~/.claude/empresa-agentes-estado/ (vigia-banco.json, vigia-banco.log).
Depois de qualquer mudança, rode `python testar-vigia.py`.
"""

import calendar
import json
import os
import subprocess
import sys
import time
from datetime import datetime

ESTADO = os.environ.get("KONOHA_ESTADO") or os.path.join(os.path.expanduser("~"), ".claude", "empresa-agentes-estado")
PARADO_SEGUNDOS = 2 * 3600
INTERVALO_SEGUNDOS = 10 * 60
PREFIXO = "supabase_db_"
# Windows: sem isto, cada docker chamado em segundo plano abre uma janela de terminal por um instante.
SEM_JANELA = 0x08000000 if os.name == "nt" else 0  # CREATE_NO_WINDOW
USO_SQL = ("select coalesce(sum(seq_scan + coalesce(idx_scan, 0) + n_tup_ins + n_tup_upd + n_tup_del), 0) "
           "from pg_stat_user_tables where schemaname = 'public'")


def docker(*args, timeout=30):
    r = subprocess.run(["docker", *args], capture_output=True, text=True, encoding="utf-8", errors="ignore",
                       timeout=timeout, stdin=subprocess.DEVNULL, creationflags=SEM_JANELA)
    return r.returncode, r.stdout.strip()


def registrar(texto):
    try:
        os.makedirs(ESTADO, exist_ok=True)
        with open(os.path.join(ESTADO, "vigia-banco.log"), "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat(timespec='seconds')} {texto}\n")
    except Exception:
        pass


def ler_estado():
    try:
        with open(os.path.join(ESTADO, "vigia-banco.json"), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def gravar_estado(estado):
    os.makedirs(ESTADO, exist_ok=True)
    with open(os.path.join(ESTADO, "vigia-banco.json"), "w", encoding="utf-8") as f:
        json.dump(estado, f)


def decidir(bancos, estado, agora):
    """Regra pura. bancos: {nome: {"uso": int, "ligado_em": epoch}}. estado: {nome: {"uso", "desde"}}.

    Devolve (desligar, estado_novo). O uso muda (ou o banco é novo para o vigia): o relógio
    recomeça. Desliga só se o uso está igual há PARADO_SEGUNDOS e o banco está ligado há pelo
    menos isso. Banco que não está mais ligado sai do estado.
    """
    desligar, novo = [], {}
    for nome, b in bancos.items():
        antes = estado.get(nome)
        if antes is None or antes.get("uso") != b["uso"] or antes.get("desde", 0) < b["ligado_em"]:
            novo[nome] = {"uso": b["uso"], "desde": agora}
            continue
        novo[nome] = antes
        if agora - antes["desde"] >= PARADO_SEGUNDOS and agora - b["ligado_em"] >= PARADO_SEGUNDOS:
            desligar.append(nome)
    return desligar, novo


def ligado_em(conteiner):
    """Hora (epoch) em que o contêiner foi ligado. O Docker dá em UTC, ex.: 2026-09-30T14:44:48.1Z."""
    _, saida = docker("inspect", "-f", "{{.State.StartedAt}}", conteiner)
    try:
        return calendar.timegm(time.strptime(saida[:19], "%Y-%m-%dT%H:%M:%S"))
    except Exception:
        return time.time()  # na dúvida, conta como recém-ligado: não desliga


def bancos_ligados():
    codigo, saida = docker("ps", "--filter", f"name={PREFIXO}", "--format", "{{.Names}}")
    if codigo != 0:
        return {}
    bancos = {}
    for conteiner in saida.splitlines():
        nome = conteiner[len(PREFIXO):]
        codigo, uso = docker("exec", conteiner, "psql", "-U", "postgres", "-tAc", USO_SQL, timeout=20)
        if codigo != 0 or not uso.strip().isdigit():
            continue  # não deu para medir: não mexe
        bancos[nome] = {"uso": int(uso.strip()), "ligado_em": ligado_em(conteiner)}
    return bancos


def desligar_banco(nome):
    _, saida = docker("ps", "--format", "{{.Names}}")
    conteineres = [c for c in saida.splitlines() if c.startswith("supabase_") and c.endswith("_" + nome)]
    if conteineres:
        docker("stop", *conteineres, timeout=120)
    return conteineres


def vigiar(simular=False):
    agora = time.time()
    desligar, novo = decidir(bancos_ligados(), ler_estado(), agora)
    feitos = []
    for nome in desligar:
        if simular:
            feitos.append(nome)
            continue
        conteineres = desligar_banco(nome)
        registrar(f"desligado {nome} ({len(conteineres)} contêineres), parado há mais de 2 h")
        novo.pop(nome, None)
        feitos.append(nome)
    if not simular:
        novo["_ultima_vez"] = agora
        gravar_estado({k: v for k, v in novo.items()})
    return feitos


def main():
    if "--segundo-plano" in sys.argv:
        try:
            vigiar()
        except Exception as erro:
            registrar(f"ERRO geral: {type(erro).__name__}: {erro}")
        return
    if sys.stdin.isatty() or "--simular" in sys.argv or "--agora" in sys.argv:
        simular = "--simular" in sys.argv
        feitos = vigiar(simular=simular)
        print(("Desligaria: " if simular else "Desligados: ") + (", ".join(feitos) or "nenhum"))
        return
    try:  # gancho: lança em segundo plano e volta na hora, no máximo a cada 10 minutos
        sys.stdin.read()
        if time.time() - ler_estado().get("_ultima_vez", 0) < INTERVALO_SEGUNDOS:
            return
        flags = SEM_JANELA | 0x00000200 if os.name == "nt" else 0  # CREATE_NO_WINDOW | NEW_PROCESS_GROUP
        subprocess.Popen([sys.executable, os.path.abspath(__file__), "--segundo-plano"],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         creationflags=flags, close_fds=True)
    except Exception:
        return


if __name__ == "__main__":
    main()
