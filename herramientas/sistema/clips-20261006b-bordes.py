# Primeras y últimas palabras de cada tramo con su segundo, para ver si los cortes caen bien.  python3 bordes.py v10 [v2 ...]
import json, sys
for v in sys.argv[1:]:
    sp = json.load(open(f"spec-{v}.json")); ti = json.load(open(f"spec-{v}.tiempos.json"))
    for c in sp["clips"]:
        ws = ti[c["id"]]
        for n, t in enumerate(c["tramos"]):
            w = [x for x in ws if x["tramo"] == n]
            if not w: print(c["id"], n, "SIN PALABRAS"); continue
            k = list(w[0].keys())
            ini = " ".join(f"{x['p']}@{x['ini']:.2f}" for x in w[:3]); fin = " ".join(f"{x['p']}@{x['ini']:.2f}" for x in w[-3:])
            print(f"{c['id']} {n} {t['quien'][:5]:5} [{t['inicio']:.2f}-{t['fin']:.2f}] {ini}  …  {fin}")
