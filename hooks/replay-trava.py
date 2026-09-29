"""Roda a trava nas chamadas reais das conversas e compara com outra versão.

    python replay-trava.py [dias=3] [trava_antiga.py] [--projeto trecho]

Lê os registros das conversas (~/.claude/projects/*<trecho>*; sem --projeto, todas),
passa cada chamada de ferramenta pela trava desta pasta e, se dada, pela versão
antiga, e mostra quantas perguntas e bloqueios cada uma daria e o que mudou.
Não roda nada: só decide. Use antes de instalar qualquer mudança na trava, para
não voltar a encher o dono de perguntas.
"""

import collections
import glob
import importlib.util
import json
import os
import sys
import time


def carregar(caminho, nome):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(os.path.abspath(caminho)))
    spec.loader.exec_module(mod)
    sys.path.pop(0)
    return mod


def chamadas(dias, trecho="*"):
    limite = time.time() - dias * 86400
    base = os.path.join(os.path.expanduser("~"), ".claude", "projects")
    for arquivo in glob.glob(os.path.join(base, f"*{trecho}*" if trecho != "*" else "*", "**", "*.jsonl"), recursive=True):
        if os.path.getmtime(arquivo) < limite:
            continue
        with open(arquivo, encoding="utf-8", errors="ignore") as f:
            for linha in f:
                try:
                    reg = json.loads(linha)
                except ValueError:
                    continue
                conteudo = (reg.get("message") or {}).get("content")
                if reg.get("type") != "assistant" or not isinstance(conteudo, list):
                    continue
                for bloco in conteudo:
                    if isinstance(bloco, dict) and bloco.get("type") == "tool_use":
                        yield {"tool_name": bloco.get("name", ""), "tool_input": bloco.get("input") or {}, "cwd": reg.get("cwd", "")}


def main():
    args = sys.argv[1:]
    trecho = "*"
    if "--projeto" in args:
        i = args.index("--projeto")
        trecho = args[i + 1]
        del args[i:i + 2]
    dias = float(args[0]) if args else 3
    aqui = os.path.dirname(os.path.abspath(__file__))
    nova = carregar(os.path.join(aqui, "proteger-banco.py"), "trava_nova")
    antiga = carregar(args[1], "trava_antiga") if len(args) > 1 else None
    total = collections.Counter()
    mudancas = collections.defaultdict(list)
    exemplos = collections.defaultdict(list)
    n = 0
    for c in chamadas(dias, trecho):
        n += 1
        d_nova = (nova.decidir(c) or ("livre", ""))
        total[("nova", d_nova[0])] += 1
        if antiga:
            d_antiga = (antiga.decidir(c) or ("livre", ""))
            total[("antiga", d_antiga[0])] += 1
            if d_antiga[0] != d_nova[0]:
                mudancas[(d_antiga[0], d_nova[0])].append(c)
        if d_nova[0] == "ask":
            exemplos[c["tool_name"].rsplit("__", 1)[-1]].append((c, d_nova[1]))
    print(f"{n} chamadas em {dias:g} dias")
    for versao in ("antiga", "nova") if antiga else ("nova",):
        print(f"  trava {versao}: " + ", ".join(f"{d} {total[(versao, d)]}" for d in ("ask", "deny", "livre")))
    for (de, para), lista in mudancas.items():
        print(f"\n{de} -> {para}: {len(lista)}")
        for c in lista[:8]:
            texto = json.dumps(c["tool_input"], ensure_ascii=False)[:220]
            print(f"  - {c['tool_name']}: {texto}")
    print("\nComo as perguntas chegam ao dono (1 exemplo por tipo):")
    for tipo, lista in exemplos.items():
        print(f"\n[{tipo}] x{len(lista)}\n{lista[-1][1]}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
