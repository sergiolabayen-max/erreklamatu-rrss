#!/usr/bin/env python3
"""Escribe el documento de la tanda (Clips_tercera_pasada_8oct2026.md) a partir de defs.py, piezas.py y los vídeos montados."""
import subprocess, os, re, defs, piezas
P = piezas.P
NUEVAS = {"PUB-0247", "PUB-0250", "PUB-0251", "PUB-0253", "PUB-0254", "PUB-0255", "PUB-0264", "PUB-0266", "PUB-0267", "PUB-0268", "PUB-0270", "PUB-0271", "PUB-0272", "PUB-0273", "PUB-0274"}
FUENTE = {"a14": "COPE (audio)", "a3": "Radio Popular (audio)", "a11": "Radio Euskadi (audio)", "v4": "Está pasando, 2019", "v2": "En Jake, julio de 2022", "v3": "Qué me estás contando", "inf": "Informativos EITB, 2021",
          "qa": "Quédate con Ane, 2024", "av": "EITB, 2017 (low cost)", "avb": "EITB, 2017 (low cost)", "siml": "SIML (EITB)", "ep": "Está pasando (Jon)", "ana": "EITB, temporal Ana", "ej22": "En Jake, abril de 2022",
          "ed": "En Jake, estafas digitales", "tve": "TVE, huracán Kirk", "rtve": "TVE, huelga de tierra", "v5": "En Jake, diciembre de 2021", "v8": "En Jake, mayo de 2020"}
def dur(pid):
    try: return round(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"out/{pid}.mp4"]).decode()))
    except Exception: return 0
def mmss(s): return f"{s // 60}:{s % 60:02d}"
filas = []; tot = 0; nopub = []; sindesp = []
for v, pid, k, tit, tr, op in defs.C:
    p = P[pid]; n = p["notas"].replace(piezas.N3, "").replace(piezas.AU, "").replace(piezas.LLA, ""); d = dur(pid); tot += d
    m = re.search(r"(VERSIÓN LARGA DE [^:(.]*|VERSIÓN SEGUIDA DE [^(:.]*|ES PUB-0241 MÁS LA DESPEDIDA|SEGUNDA MITAD DE PUB-0222[^(:.]*|LA PIEZA ENTERA DEL INFORMATIVO)", n)
    que = "Nueva" if pid in NUEVAS else (m.group(1).strip().capitalize().replace("pub-", "PUB-").replace("Pub-", "PUB-") if m else "Versión larga")
    av = []
    if "no la publicaría" in n: av.append("yo no la publicaría"); nopub.append(pid)
    if "NO HABLA NADIE DEL DESPACHO" in n or "no hay voz de nadie del despacho" in n or "SOLO HABLA LA PRESENTADORA" in n or "No habla nadie del despacho" in n: av.append("no habla nadie del despacho"); sindesp.append(pid)
    for marca in ("RYANAIR", "VUELING", "IBERIA", "LUFTHANSA"):
        if "NOMBRA A " + marca in n: av.append("nombra a " + marca.capitalize())
    if "QUE LO VEA UN ABOGADO" in n: av.append("que lo vea un abogado")
    if "CONTENIDO DE LA PANDEMIA" in n: av.append("pandemia")
    filas.append(f"| {pid} | {p['tit']} | {FUENTE[v]} | {mmss(d)} | {que} | {'; '.join(av)} |")
open("doc-tabla.md", "w").write("| Pieza | Titular | Fuente | Dura | Qué es | Avisos |\n|---|---|---|---|---|---|\n" + "\n".join(filas) + "\n")
print(len(filas), "piezas", mmss(tot), "| nuevas", len(NUEVAS), "| no publicaría", nopub, "| sin despacho", sindesp)
