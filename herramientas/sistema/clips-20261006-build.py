#!/usr/bin/env python3
"""Genera spec-<video>.json a partir de defs.py. Conserva los recortes ya calculados.  python3 build.py [videos]"""
import json, os, sys, importlib
import defs; importlib.reload(defs)
from defs import V, C, S
import ejfix
solo = sys.argv[1:]
specs = {}
for v, pid, kicker, tit, tramos, op in C:
    if solo and v not in solo: continue
    cfg = V[v]
    sp = specs.setdefault(v, dict({k: cfg[k] for k in cfg}, modelo=S + "/video/sherpa-onnx-whisper-turbo", vad=S + "/video/silero_vad.onnx", diseno="zonas", crf=24, preset="faster", clips=[]))
    trs = []
    for t in tramos:
        d = {"inicio": t[0], "fin": t[1], "quien": t[2], "texto": t[3]}
        if len(t) > 4: d.update(t[4])
        trs.append(d)
    sp["clips"].append(dict({"id": pid, "kicker": kicker, "titular": tit, "tramos": trs}, **op))
for v, sp in specs.items():
    ruta = f"spec-{v}.json"
    if os.path.exists(ruta):                                   # conserva los recortes de los clips cuyos tramos no han cambiado
        ant = {c["id"]: c for c in json.load(open(ruta))["clips"]}
        for c in sp["clips"]:
            a = ant.get(c["id"])
            if a and a.get("recortes") and [(t["inicio"], t["fin"], t.get("enc")) for t in a["tramos"]] == [(t["inicio"], t["fin"], t.get("enc")) for t in c["tramos"]]: c["recortes"] = a["recortes"]
    json.dump(sp, open(ruta, "w"), ensure_ascii=False, indent=1)
    print(ruta, len(sp["clips"]), "clips", round(sum(t["fin"] - t["inicio"] for c in sp["clips"] for t in c["tramos"])), "s")
