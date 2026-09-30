"""Testes da regra do vigia-banco.py (sem Docker). Rodar depois de qualquer mudança nele."""

import importlib.util
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("vigia", os.path.join(AQUI, "vigia-banco.py"))
V = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)

H = 3600
falhas = 0


def caso(nome, obtido, esperado):
    global falhas
    ok = obtido == esperado
    falhas += not ok
    print(f"{'ok  ' if ok else 'FALHA'} {nome}" + ("" if ok else f": veio {obtido}, esperado {esperado}"))


# 1. Banco novo para o vigia: começa a contar, não desliga
d, e = V.decidir({"crm": {"uso": 10, "ligado_em": 0}}, {}, 10 * H)
caso("banco novo não desliga", d, [])
caso("banco novo começa a contar agora", e["crm"], {"uso": 10, "desde": 10 * H})

# 2. Uso igual há 2 h e ligado há mais de 2 h: desliga
d, _ = V.decidir({"crm": {"uso": 10, "ligado_em": 0}}, {"crm": {"uso": 10, "desde": 8 * H}}, 10 * H)
caso("parado há 2 h desliga", d, ["crm"])

# 3. Uso igual há 1 h 59: não desliga
d, _ = V.decidir({"crm": {"uso": 10, "ligado_em": 0}}, {"crm": {"uso": 10, "desde": 8 * H + 60}}, 10 * H)
caso("parado há menos de 2 h não desliga", d, [])

# 4. Uso mudou: não desliga e o relógio recomeça
d, e = V.decidir({"crm": {"uso": 11, "ligado_em": 0}}, {"crm": {"uso": 10, "desde": 0}}, 10 * H)
caso("uso mudou não desliga", d, [])
caso("uso mudou recomeça o relógio", e["crm"], {"uso": 11, "desde": 10 * H})

# 5. Banco religado depois da última leitura (mesmo uso por coincidência): recomeça
d, e = V.decidir({"crm": {"uso": 10, "ligado_em": 9 * H}}, {"crm": {"uso": 10, "desde": 0}}, 10 * H)
caso("religado recomeça", d, [])
caso("religado conta desde agora", e["crm"]["desde"], 10 * H)

# 6. Banco que saiu da lista (desligado por alguém) sai do estado
_, e = V.decidir({}, {"velho": {"uso": 1, "desde": 0}}, 10 * H)
caso("banco desligado sai do estado", "velho" in e, False)

# 7. Dois bancos: só o parado desliga
d, _ = V.decidir({"a": {"uso": 5, "ligado_em": 0}, "b": {"uso": 7, "ligado_em": 0}},
                 {"a": {"uso": 5, "desde": 0}, "b": {"uso": 6, "desde": 0}}, 10 * H)
caso("dois bancos: só o parado", d, ["a"])

print("\n" + ("Todos passaram." if not falhas else f"{falhas} falha(s)."))
raise SystemExit(1 if falhas else 0)
