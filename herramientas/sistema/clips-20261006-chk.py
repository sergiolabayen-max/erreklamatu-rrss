# Revisa los tiempos: últimas palabras apretadas contra el final del tramo, primeras palabras tardías y proporción de palabras localizadas.
import json, sys, re
for v in sys.argv[1:]:
    sp = json.load(open(f"spec-{v}.json")); ti = json.load(open(f"spec-{v}.tiempos.json"))
    loc = {}
    for l in open(f"tie-{v}.log"):
        m = re.match(r"(PUB-\d+) tramo (\d+): (\d+) de (\d+)", l)
        if m: loc[(m.group(1), int(m.group(2)) - 1)] = (int(m.group(3)), int(m.group(4)))
    for c in sp["clips"]:
        ws = ti[c["id"]]
        for n, t in enumerate(c["tramos"]):
            w = [x for x in ws if x["tramo"] == n]; a, b = t["inicio"], t["fin"]; msg = []
            if len(w) >= 4 and w[-1]["ini"] - w[-3]["ini"] < 0.25: msg.append(f"FINAL APRETADO {[(x['p'], x['ini']) for x in w[-3:]]} fin={b}")
            if b - w[-1]["ini"] > 1.6: msg.append(f"sobra final {b - w[-1]['ini']:.1f}s tras «{w[-1]['p']}»@{w[-1]['ini']}")
            if w[1]["ini"] - a > 1.5 if len(w) > 1 else False: msg.append(f"arranque tardío: «{w[1]['p']}»@{w[1]['ini']} (tramo desde {a})")
            k = loc.get((c["id"], n))
            if k and k[0] < 0.75 * k[1]: msg.append(f"solo {k[0]}/{k[1]} localizadas")
            if msg: print(c["id"], n, t["quien"], " | ".join(msg))
