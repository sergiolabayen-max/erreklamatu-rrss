#!/usr/bin/env python3
"""Montaje reanudable (como clips-20261008-resto.py): recorre las especificaciones, calcula los tiempos si faltan y monta clip a clip;
marca cada clip al terminar en ok/. Se puede relanzar las veces que haga falta.  python3 montar.py k [k ...]   (FORZAR=id,id para rehacer)"""
import json, os, subprocess, sys, time
S = os.path.dirname(os.path.abspath(__file__)) + "/../sis"; A = os.path.dirname(os.path.abspath(__file__)) + "/../aud"
os.makedirs("ok", exist_ok=True); os.makedirs("out", exist_ok=True)
forzar = set(os.environ.get("FORZAR", "").split(",")) - {""}
def log(t): open("lote.log", "a").write(f"{time.strftime('%H:%M:%S')} {t}\n")
def valido(cid):
    f = f"out/{cid}.mp4"
    if not os.path.exists(f): return False
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True)
    return r.returncode == 0 and r.stdout.strip() != ""
for k in sys.argv[1:]:
    ruta = f"spec-{k}.json"; sp = json.load(open(ruta))
    if not os.path.exists(f"spec-{k}.tiempos.json") or os.path.getmtime(f"spec-{k}.tiempos.json") < os.path.getmtime(ruta):
        pal = f"{A}/{k}.pk.json" if sp["idioma"] == "es" else f"{A}/{k}.palabras.json"
        subprocess.run(["python3", f"{S}/tiempos_omni.py", ruta, pal], stdout=open(f"tie-{k}.log", "w"), check=True); log(f"tiempos {k}")
    for c in sp["clips"]:
        cid = c["id"]
        if cid in forzar and os.path.exists(f"ok/{cid}"): os.remove(f"ok/{cid}")
        if os.path.exists(f"ok/{cid}") and valido(cid): continue
        log(f"montar {cid}")
        r = subprocess.run(["nice", "-n", "5", "python3", f"{S}/video_radio.py", "montar", ruta, "out", cid], stdout=open(f"mon-{k}.log", "a"), stderr=subprocess.STDOUT)
        if r.returncode == 0 and valido(cid): open(f"ok/{cid}", "w").close(); log(f"ok {cid}")
        else: log(f"FALLO {cid}")
log("FIN " + " ".join(sys.argv[1:]))
