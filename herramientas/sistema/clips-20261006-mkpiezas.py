#!/usr/bin/env python3
"""Compone los documentos de las piezas (pdb/PUB-XXXX.json) a partir de piezas.py, defs.py, los vídeos montados (out/) y assets.json."""
import json, os, sys, subprocess, importlib
import defs, ejfix, piezas
from piezas import P, CIERRES, ORIGEN
AHORA = sys.argv[1] if len(sys.argv) > 1 else subprocess.check_output(["date", "-Iseconds"]).decode().strip()
HOY = AHORA[:10]
ENLACES = ["A · enlace en el cuerpo", "B · enlace fuera del cuerpo", "C · sin enlace"]
NOM = {"jon": "JON ORTIZ", "locucion": "LOCUCIÓN", "ainhoa": "AINHOA EGILUZ", "txaro": "TXARO ORTIZ DE ZARATE", "ertzaina": None, "presentadora": "PRESENTADORA", "presentador": "PRESENTADOR",
       "reportera": "REPORTERA", "aurkezlea": "AURKEZLEA", "espectador": "ESPECTADOR"}
ERTZ = {"ps": "ISKANDER SEGUROLA", "pe": "DAVID VILLA"}
assets = json.load(open("assets.json")) if os.path.exists("assets.json") else {}
def dur(pid):
    f = f"out/{pid}.mp4"
    if not os.path.exists(f): return None
    return round(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode()))
docs = {}; avisos = []
for n, (v, pid, kicker, tit, tramos, op) in enumerate(defs.C):
    p = P[pid]; eu = p.get("idioma") == "Euskera"; ci = CIERRES[p["ci"]]; url = p["url"]
    enl = "" if eu else ENLACES[n % 3]; L = enl[:1]
    x = p["x"]; rx = None
    if L == "A": x = x + " 👇\n" + url
    if L == "B": rx = p.get("rx", "Toda la información") + " 👇\n" + url
    fb = p["fb"] + "\n\n" + ci[0] + (("\n\nToda la información 👇\n" + url) if L == "A" else "")
    ig = p["ig"] + "\n\n" + ci[1] + ("\n\nEnlace en la bio." if L in ("A", "B") else "") + "\n\n" + p["tags"]
    tk = p["tk"] + " " + " ".join(t for t in p["tags"].split() if t != "#Bilbao" and t != "#Bilbo")
    yt = p["yt"][0] + "\n\n" + p["yt"][1] + "\n\n" + ci[2] + "\n\n📞 944 027 596\n" + url
    if len(x) > 280: avisos.append(f"{pid} X {len(x)}")
    if len(p["yt"][0]) > 100: avisos.append(f"{pid} título YouTube {len(p['yt'][0])}")
    if len(tk) > 300: avisos.append(f"{pid} TikTok {len(tk)}")
    guion = "\n".join(f'{(NOM[t[2]] or ERTZ[v])}: {t[3]}' for t in tramos)
    d = dur(pid); a = assets.get(pid, {})
    doc = dict(id=pid, estado="Pendiente de revisión", formato="Vídeo", idioma=p.get("idioma", "Castellano"), enfoque=p["enf"], pilar=p["pilar"], area=p["area"], prioridad="Media",
               tema=p["tema"], titular=p["tit"], mensajes=p["msgs"], base_legal=p["base"], busqueda=p.get("busq", ""), notas=p["notas"], origen=ORIGEN[v][0], video_origen=ORIGEN[v][1],
               guion=guion, duracion_s=d, cta="Kontsulta doan · 944 027 596" if eu else "Consulta gratuita · 944 027 596", prueba_enlace=enl, respuesta_x=rx,
               textos=dict(x=x, facebook=fb, instagram=ig, tiktok=tk, youtube=yt), url_web=url, urls=dict(x="", facebook="", instagram="", tiktok="", youtube=""),
               creado_el=AHORA, actualizado_el=AHORA, verificado_el=HOY, caduca_el="2027-01-04", aprobado_el="", programado_el="", publicado_el="", fecha_objetivo="", motivo_rechazo="", cambios_pedidos=None,
               creatividades=[dict(tipo="video", url=a.get("url", ""), publica=a.get("publica", ""), uso=["x", "facebook", "instagram", "tiktok", "youtube"],
                                   etiqueta=f"Clip vertical 1080 × 1920 · esquema por zonas · cortinilla de cierre · {d} s" + (" · BORRADOR" if eu else ""))])
    docs[pid] = doc
os.makedirs("pdb", exist_ok=True)
for pid, d in docs.items(): json.dump(d, open(f"pdb/{pid}.json", "w"), ensure_ascii=False, indent=1)
print(len(docs), "piezas"); print("\n".join(avisos) or "sin avisos")
