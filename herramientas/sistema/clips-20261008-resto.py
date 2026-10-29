#!/usr/bin/env python3
"""Continúa el montaje después de un reinicio: se puede lanzar las veces que haga falta; salta lo ya hecho.  python3 resto.py"""
import json, os, subprocess, time
VC = "/home/claude/cc/sistema/video_clips.py"
def log(t):
    open("lote.log", "a").write(f"{t} {time.strftime('%H:%M:%S')}\n")
def valido(pid):
    f = f"out/{pid}.mp4"
    if not os.path.exists(f): return False
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True)
    return r.returncode == 0 and r.stdout.strip() != ""
def run(args, salida):
    r = subprocess.run(args, stdout=open(salida, "a"), stderr=subprocess.STDOUT)
    return r.returncode == 0
os.makedirs("ok2", exist_ok=True)
# (especificación, forzar aunque exista el vídeo, identificadores o None = todos)
PLAN = [("siml", False, None), ("ep", False, None), ("ana", False, None), ("ej22", False, None), ("ed", False, None), ("tve", False, None), ("rtve", False, None), ("v5", False, None), ("v8", False, None),
        ("a11", True, ["PUB-0253", "PUB-0254", "PUB-0255"]), ("v4", True, ["PUB-0258"]), ("v2", True, ["PUB-0259"]), ("inf", True, None), ("qa", True, None), ("avb", True, None)]
for v, forzar, ids in PLAN:
    ruta = f"spec-{v}.json"; spec = json.load(open(ruta)); todos = [c["id"] for c in spec["clips"]]; ids = ids or todos
    pend = [p for p in ids if not os.path.exists(f"ok2/{p}") and (forzar or not valido(p))]
    if not pend:
        for p in ids: open(f"ok2/{p}", "a").close()
        continue
    if not os.path.exists(f"spec-{v}.tiempos.json"):
        log(f"== {v} tiempos")
        if not run(["python3", VC, "tiempos", ruta], f"tie-{v}.log"): log(f"FALLO tiempos {v}"); continue
    if any(not c.get("recortes") for c in json.load(open(ruta))["clips"]):
        log(f"== {v} encuadre")
        if not run(["python3", "marco.py", "encuadrar", ruta], f"enc-{v}.log"): log(f"FALLO encuadre {v}"); continue
    for p in pend:
        log(f"== {v} montar {p}")
        if run(["python3", VC, "montar", ruta, "out", p], f"mon-{v}.log") and valido(p): open(f"ok2/{p}", "a").close()
        else: log(f"FALLO montar {p}")
log("FIN_RESTO")
