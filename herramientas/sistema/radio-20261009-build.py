# Genera spec-<k>.json para video_radio.py a partir de defs.py.  python3 build.py [k ...]
import json, sys, importlib, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import defs
solo = sys.argv[1:]; specs = {}
for k, cid, kicker, tit, tramos, op in defs.C:
    if solo and k not in solo: continue
    sp = specs.setdefault(k, dict(defs.V[k], clips=[]))
    trs = [dict(inicio=t[0], fin=t[1], quien=t[2], texto=t[3]) for t in tramos]
    for a, b in zip(trs, trs[1:]):
        if b["inicio"] < a["fin"] - 0.01 and b["inicio"] > a["inicio"]: print("AVISO solape", cid, a["fin"], b["inicio"])
    sp["clips"].append(dict(dict(id=cid, kicker=kicker, titular=tit, tramos=trs, principal="jon"), **op))
for k, sp in specs.items():
    json.dump(sp, open(f"spec-{k}.json", "w"), ensure_ascii=False, indent=1); print(f"spec-{k}.json", len(sp["clips"]), "clips", round(sum(t["fin"] - t["inicio"] for c in sp["clips"] for t in c["tramos"])), "s")
