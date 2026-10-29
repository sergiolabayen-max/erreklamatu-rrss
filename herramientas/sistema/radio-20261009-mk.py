#!/usr/bin/env python3
"""Compone los documentos de las piezas (pdb/PUB-XXXX.json) a partir de defs.py, piezas.py, los vídeos montados (out/), ids.json (provisional -> PUB),
assets.json (copia ligera subida al centro de control) y publica.json (archivo completo en GitHub). Basado en clips-20261008-mkpiezas.py.
python3 mk.py [AHORA]"""
import json, os, sys, subprocess, re
import defs, piezas
from piezas import P, CI, ORIGEN
AHORA = sys.argv[1] if len(sys.argv) > 1 else subprocess.check_output(["date", "-Iseconds"], env=dict(os.environ, TZ="Europe/Madrid")).decode().strip()
HOY = AHORA[:10]
ENLACES = ["A · enlace en el cuerpo", "B · enlace fuera del cuerpo", "C · sin enlace"]
NOM = {"jon": "JON ORTIZ", "pregunta": "PREGUNTA", "programa": "PROGRAMA"}
ids = json.load(open("ids.json")); assets = json.load(open("assets.json")) if os.path.exists("assets.json") else {}
publica = json.load(open("publica.json")) if os.path.exists("publica.json") else {}
chk = json.load(open("chkout.json")) if os.path.exists("chkout.json") else {}
VENTANA = {"E6-03": ("11-01", "03-15", "Mal tiempo: temporada de temporales (norma de época del 8/10)"),
           "R1-04": ("11-01", "03-15", "El titular habla de mal tiempo (norma de época del 8/10)"),
           "E6-01": ("03-01", "05-15", "La pregunta habla de la Semana Santa («Aste Santukoetan»)"),
           "E6-09": ("03-15", "05-31", "La pregunta habla de «estos días de Semana Santa»"),
           "R1-10": ("06-15", "08-15", "La pregunta dice «ahora que comienza la temporada alta de vacaciones»"),
           "R2-04": ("06-01", "07-31", "Jon dice «ahora que llega el verano»"),
           "E13-01": ("08-15", "09-30", "Programa de la vuelta de vacaciones (agosto)")}
def xlen(t):
    t = re.sub(r"https?://\S+", "x" * 23, t); n = 0
    for ch in t:
        c = ord(ch); n += 1 if (c <= 4351 or 8192 <= c <= 8205 or 8208 <= c <= 8223 or 8242 <= c <= 8247) else 2
    return n
def dur(cid):
    f = f"out/{cid}.mp4"
    if not os.path.exists(f): return None
    try: return round(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], stderr=subprocess.DEVNULL).decode()))
    except Exception: return None
docs = {}; avisos = []; n = 0
for k, cid, kicker, tit, tramos, op in defs.C:
    if cid not in ids: continue
    pid = ids[cid]; p = P[cid]; eu = defs.V[k]["idioma"] == "eu"; ci = CI[p["ci"]]; url = p["url"]
    enl = ENLACES[n % 3]; L = enl[:1]; n += 1
    mas = "Informazio gehiago 👇" if eu else "Toda la información 👇"
    x = p["x"]; rx = None
    if L == "A": x = x + " 👇\n" + url
    if L == "B": rx = mas + "\n" + url
    ult = p["fb"].split("\n\n")[-1]
    ya = any(w in ult for w in ("Gorde bideo", "Guarda este", "Guárdalo", "Síguenos", "Jarraitu gaitzazu", "Cuéntanos", "Konta iezaguzu", "Mándaselo", "partekatu", "compártelo", "guárdalo"))
    comercial = p["ci"] in ("consulta", "ocupamos", "sabes", "e_kontsulta", "e_aukera")
    fb = p["fb"] + ("" if (ya and not comercial) else "\n\n" + ci[0]) + (("\n\n" + mas + "\n" + url) if L == "A" else "")
    ig = p["ig"] + "\n\n" + ci[1] + (("\n\nEsteka bioan." if eu else "\n\nEnlace en la bio.") if L in ("A", "B") else "") + "\n\n" + p["tags"]
    tk = p["tk"] + " " + " ".join(t for t in p["tags"].split() if t not in ("#Bilbao", "#Bilbo"))
    sus = "🔔 Harpidetu kanalera hurrengo bideoak ikusteko." if eu else "🔔 Suscríbete al canal para ver los próximos vídeos."
    yt = p["yt"][0] + "\n\n" + p["yt"][1] + "\n\n" + ci[2] + "\n\n" + sus + "\n\n📞 944 027 596\n" + url
    if xlen(x) > 280: avisos.append(f"{cid} X {xlen(x)}")
    if xlen(p["x"] + " 👇\n" + url) > 280: avisos.append(f"{cid} X con enlace {xlen(p['x'] + ' 👇' + chr(10) + url)}")
    if len(p["yt"][0]) > 100: avisos.append(f"{cid} título YouTube {len(p['yt'][0])}")
    if len(tk) > 300: avisos.append(f"{cid} TikTok {len(tk)}")
    if ig.count("#") > 5: avisos.append(f"{cid} Instagram con más de cinco etiquetas")
    if "info@" in ig: avisos.append(f"{cid} correo en Instagram")
    if "Kontsulta doan" in "".join(ci) and eu and "Kontsulta doan da" not in ci[0]: avisos.append(f"{cid} cierre en euskera sin «Kontsulta doan da»")
    guion = "\n".join(f'{NOM[t[2]]}: {t[3]}' for t in tramos)
    d = dur(cid); a = assets.get(cid, {}); pub = publica.get(cid, "")
    if not a or not pub: avisos.append(f"{cid} sin asset o sin archivo público")
    comp = ("Comprobación de la instrucción permanente: gancho en el titular del vídeo y en la primera línea (situación o pregunta del lector); escrito desde lo que le pasa al pasajero"
            + (" o al cliente del banco" if p["area"] == "Banca" else "") + "; dice qué puede hacer y cómo ayuda ERREKLAMATU; llamada a la acción «" + p["ci"] + "» (varía entre piezas); sin promesas de resultado"
            + ("; euskera escrito por Claude, sin revisar por una persona" if eu else "") + ". ")
    seg = ""
    if cid in chk: seg = f" Segunda lectura automática del clip montado: parecido {chk[cid]['parecido']:.2f} con el guion (las diferencias son sobre todo muletillas quitadas)."
    notas = (piezas.N0 + p["notas"] + " " + comp + f"Dura {d} s con la cortinilla." + (piezas.SUB_EU if eu else piezas.SUB_ES) + seg).replace("  ", " ")
    doc = dict(id=pid, estado="Pendiente de revisión", formato="Vídeo", idioma="Euskera" if eu else "Castellano", enfoque=p["enf"], pilar=p["pilar"], area=p["area"], prioridad="Media",
               tema=p["tema"], titular=" ".join(tit), mensajes=p["msgs"], base_legal=p["base"], busqueda="", notas=notas, origen=ORIGEN[k][0], video_origen=ORIGEN[k][1],
               guion=guion, duracion_s=d, cta=("Kontsulta doan · 944 027 596" if eu else "Consulta gratuita · 944 027 596"), prueba_enlace=enl, respuesta_x=rx,
               textos=dict(x=x, facebook=fb, instagram=ig, tiktok=tk, youtube=yt), url_web=url, urls=dict(x="", facebook="", instagram="", tiktok="", youtube=""),
               creado_el=AHORA, actualizado_el=AHORA, verificado_el=HOY, caduca_el="2027-01-07", aprobado_el="", programado_el="", publicado_el="", fecha_objetivo="", motivo_rechazo="", cambios_pedidos=None,
               fotos=["FOTO-15", "FOTO-13"], tanda="Audios de radio 9/10/2026", clip_provisional=cid,
               creatividades=[dict(tipo="video", url=a.get("url", ""), publica=pub, ligera=True, uso=["x", "facebook", "instagram", "tiktok", "youtube"],
                                   etiqueta=f"Clip vertical 1080 × 1920 · audio de radio «lo más vídeo posible» (retrato con zoom lento, cartel de la emisora, barras del sonido, subtítulos palabra a palabra) · cortinilla de cierre · {d} s · aquí se ve una copia ligera (720 × 1280); a las redes va el archivo de 1080 × 1920")])
    if cid in VENTANA:
        v = VENTANA[cid]; doc["ventana"] = dict(desde=v[0], hasta=v[1], motivo=v[2])
    docs[pid] = doc
os.makedirs("pdb", exist_ok=True)
for pid, d in docs.items(): json.dump(d, open(f"pdb/{pid}.json", "w"), ensure_ascii=False, indent=1)
print(len(docs), "piezas"); print("\n".join(avisos) or "sin avisos")
