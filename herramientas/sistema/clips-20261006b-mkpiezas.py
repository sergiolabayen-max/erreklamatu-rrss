#!/usr/bin/env python3
"""Compone los documentos de las piezas (pdb/PUB-XXXX.json) a partir de piezas.py, defs.py, los vídeos montados (out/) y assets.json."""
import json, os, sys, subprocess, re
import defs, piezas
from piezas import P, CIERRES, ORIGEN
AHORA = sys.argv[1] if len(sys.argv) > 1 else subprocess.check_output(["date", "-Iseconds"]).decode().strip()
HOY = AHORA[:10]
ENLACES = ["A · enlace en el cuerpo", "B · enlace fuera del cuerpo", "C · sin enlace"]
NOM = {"jon": "JON ORTIZ", "oscar": "ÓSCAR SÁNCHEZ", "locucion": "LOCUCIÓN", "presentador": "PRESENTADOR", "reportera": "REPORTERA", "reportero": "REPORTERO", "pasajero": "PASAJERO", "pregunta": "PREGUNTA"}
assets = json.load(open("assets.json")) if os.path.exists("assets.json") else {}
def xlen(t):
    t = re.sub(r"https?://\S+", "x" * 23, t); n = 0
    for ch in t:
        c = ord(ch); n += 1 if (c <= 4351 or 8192 <= c <= 8205 or 8208 <= c <= 8223 or 8242 <= c <= 8247) else 2
    return n
def dur(pid):
    f = f"out/{pid}.mp4"
    if not os.path.exists(f): return None
    return round(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode()))
docs = {}; avisos = []
for n, (v, pid, kicker, tit, tramos, op) in enumerate(defs.C):
    p = P[pid]; ci = CIERRES[p["ci"]]; url = p["url"]
    enl = ENLACES[n % 3]; L = enl[:1]
    x = p["x"]; rx = None
    if L == "A": x = x + " 👇\n" + url
    if L == "B": rx = p.get("rx", "Toda la información") + " 👇\n" + url
    fb = p["fb"] + "\n\n" + ci[0] + (("\n\nToda la información 👇\n" + url) if L == "A" else "")
    ig = p["ig"] + "\n\n" + ci[1] + ("\n\nEnlace en la bio." if L in ("A", "B") else "") + "\n\n" + p["tags"]
    tk = p["tk"] + " " + " ".join(t for t in p["tags"].split() if t != "#Bilbao")
    yt = p["yt"][0] + "\n\n" + p["yt"][1] + "\n\n" + ci[2] + "\n\n🔔 Suscríbete al canal para ver los próximos vídeos.\n\n📞 944 027 596\n" + url  # AC-12 (08/10/2026): pedir la suscripción
    if xlen(x) > 280: avisos.append(f"{pid} X {xlen(x)}")
    if xlen(p["x"] + " 👇\n" + url) > 280: avisos.append(f"{pid} X con enlace {xlen(p['x'] + ' 👇' + chr(10) + url)} (aviso: no cabría si cambia el turno de la prueba)")
    if len(p["yt"][0]) > 100: avisos.append(f"{pid} título YouTube {len(p['yt'][0])}")
    if len(tk) > 300: avisos.append(f"{pid} TikTok {len(tk)}")
    guion = "\n".join(f'{NOM[t[2]]}: {t[3]}' for t in tramos)
    d = dur(pid); a = assets.get(pid, {})
    audio = p.get("fmt") == "audio"
    doc = dict(id=pid, estado="Pendiente de revisión", formato="Vídeo", idioma="Castellano", enfoque=p["enf"], pilar=p["pilar"], area=p["area"], prioridad="Media",
               tema=p["tema"], titular=p["tit"], mensajes=p["msgs"], base_legal=p["base"], busqueda="", notas=p["notas"], origen=ORIGEN[v][0], video_origen=ORIGEN[v][1],
               guion=guion, duracion_s=d, cta="Consulta gratuita · 944 027 596", prueba_enlace=enl, respuesta_x=rx,
               textos=dict(x=x, facebook=fb, instagram=ig, tiktok=tk, youtube=yt), url_web=url, urls=dict(x="", facebook="", instagram="", tiktok="", youtube=""),
               creado_el=AHORA, actualizado_el=AHORA, verificado_el=HOY, caduca_el="2027-01-05", aprobado_el="", programado_el="", publicado_el="", fecha_objetivo="", motivo_rechazo="", cambios_pedidos=None,
               creatividades=[dict(tipo="video", url=a.get("url", ""), publica=a.get("publica", ""), ligera=True, uso=["x", "facebook", "instagram", "tiktok", "youtube"],
                                   etiqueta=f"Clip vertical 1080 × 1920 · esquema por zonas · cortinilla de cierre · {d} s" + (" · audio de radio con foto fija" if audio else "") + " · aquí se ve una copia ligera (720 × 1280); a las redes va el archivo de 1080 × 1920")])
    if v in ("a14", "a3", "v11"): doc["fotos"] = ["FOTO-15"]          # retrato de Jon Ortiz
    if v in ("a11", "v4"): doc["fotos"] = ["FOTO-09"]                 # retrato de Óscar Sánchez (americana, brazos cruzados)
    docs[pid] = doc
os.makedirs("pdb", exist_ok=True)
for pid, d in docs.items(): json.dump(d, open(f"pdb/{pid}.json", "w"), ensure_ascii=False, indent=1)
print(len(docs), "piezas"); print("\n".join(avisos) or "sin avisos")
