#!/usr/bin/env python3
"""«El documento, subrayado» (29/10/2026): vídeo vertical con un fragmento real de una sentencia del despacho,
anonimizado, con la frase clave subrayada en verde, la explicación y el cierre de marca.

Uso:
  python3 documento.py ocr pagina.png                   -> pagina.tsv (tesseract, castellano)
  python3 documento.py recorte spec.json carpeta        -> fragmento anonimizado + vista previa con el subrayado
  python3 documento.py todo spec.json carpeta           -> voz + recorte + vídeo 1080 × 1920
  python3 documento.py video spec.json carpeta          -> solo el montaje del vídeo

Spec (JSON):
{
 "id": "D1-athletic", "categoria": "UN CASO REAL", "juzgado": "Juzgado de Primera Instancia n.º 9 de Bilbao",
 "pagina": "/ruta/LOCAL/a/la/pagina.png",       # NUNCA en el repositorio: las sentencias tienen datos personales
 "subrayar": ["con mas claridad en el caso de los billetes perdidos", "procede estimar la plena compatibilidad ..."],
 "ocultar": [],   # palabras que se tapan siempre; los nombres de clientes van en sentencias/<pdf>.ocultar.txt (solo en el Mac) (además de fechas, DNI, CSV, NIG…)
 "margen": [260, 240],                          # píxeles por encima y por debajo de lo subrayado
 "gancho": ["Perdieron el partido del Athletic.", "El juez les devolvió las entradas."],
 "tramos": [ {"tipo": "doc", "subrayado": false, "voz": "...mp3", "subtitulos": [...]},
             {"tipo": "doc", "subrayado": true, ...},
             {"tipo": "texto", "grande": "250 € + entradas + taxi", "pequeno": "...", "voz": ..., "subtitulos": [...]} ],
 "cierre": {...como en comic.py...}, "musica": "../../../recursos/musica/musica-lofi-100bpm.mp3"
}
La imagen del documento sale ya anonimizada del paso «recorte»; el vídeo nunca usa la página original.
"""
import json, os, re, sys, subprocess, unicodedata, html
from pathlib import Path
from difflib import SequenceMatcher
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "comics"))
import comic
from comic import run, dur, css, logo_caja, cierre_html, subtitulo_html, Navegador, NAVY, VERDE, VW, VH

TESS = os.environ.get("TESSDATA", "/tmp/tess")
SENSIBLE = [r"^\d{1,2}/\d{1,2}/\d{2,4}$", r"\d{6,}", r"^[XYZ]?-?\d{7,8}-?[A-Z]$", r"CSV", r"NIG"]  # fechas, números largos, DNI/NIE, años

def norm(w): return re.sub(r"[^a-z0-9€]", "", unicodedata.normalize("NFKD", w.lower()).encode("ascii", "ignore").decode())

def ocr(png):
    tsv = Path(png).with_suffix(".tsv")
    if not tsv.exists():
        run("tesseract", png, str(tsv)[:-4], "-l", "spa", "--tessdata-dir", TESS, "-c", "tessedit_create_tsv=1", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    words = []
    for ln in open(tsv, encoding="utf8").read().splitlines()[1:]:
        c = ln.split("\t")
        if len(c) < 12 or not c[11].strip(): continue
        words.append(dict(t=c[11], n=norm(c[11]), x=int(c[6]), y=int(c[7]), w=int(c[8]), h=int(c[9]), line=(c[2], c[3], c[4])))
    return words

def buscar(words, frase):
    """Secuencia de palabras que mejor casa con la frase (tolera errores del OCR). Devuelve sus índices."""
    obj = [norm(w) for w in frase.split() if norm(w)]
    best = (0, None)
    for i in range(len(words) - len(obj) + 1):
        cand = [words[i + k]["n"] for k in range(len(obj))]
        s = SequenceMatcher(None, " ".join(obj), " ".join(cand)).ratio()
        if s > best[0]: best = (s, list(range(i, i + len(obj))))
    if best[0] < 0.8: raise SystemExit(f"No encuentro «{frase}» (mejor parecido {best[0]:.2f})")
    return best[1]

def cajas_por_linea(words, idx):
    lines = {}
    for i in idx:
        w = words[i]; k = w["line"]
        a = lines.setdefault(k, [w["x"], w["y"], w["x"] + w["w"], w["y"] + w["h"]])
        a[0] = min(a[0], w["x"]); a[1] = min(a[1], w["y"]); a[2] = max(a[2], w["x"] + w["w"]); a[3] = max(a[3], w["y"] + w["h"])
    return sorted(lines.values(), key=lambda b: b[1])

def recorte(spec, out):
    from PIL import Image, ImageDraw
    pg = spec.get("pagina")
    if not pg or not os.path.exists(pg):          # se rasteriza desde el PDF de la carpeta «sentencias» del Mac (nunca se sube al repositorio)
        pdf = os.path.join(os.environ.get("SENTENCIAS", "/mnt/user-data/uploads/Magnific/sentencias"), spec["pdf"])
        pg = f"{out}/pagina"; run("pdftoppm", "-r", 200, "-png", "-f", spec["pagina_num"], "-l", spec["pagina_num"], "-singlefile", pdf, pg); pg += ".png"
    words = ocr(pg); im = Image.open(pg).convert("RGB")
    marcas = []
    for f in spec["subrayar"]: marcas += cajas_por_linea(words, buscar(words, f))
    top = min(b[1] for b in marcas) - spec.get("margen", [260, 240])[0]; bot = max(b[3] for b in marcas) + spec.get("margen", [260, 240])[1]
    X0, X1 = spec.get("columna", [245, 1565])                     # fuera queda el margen con firmas, CSV y sellos
    top = max(0, top); bot = min(im.height, bot)
    d = ImageDraw.Draw(im); tapadas = []
    ocultar = [norm(x) for x in spec.get("ocultar", [])]
    loc = os.path.join(os.environ.get("SENTENCIAS", "/mnt/user-data/uploads/Magnific/sentencias"), spec.get("pdf", "x").replace(".pdf", ".ocultar.txt"))
    if os.path.exists(loc): ocultar += [norm(x) for x in open(loc, encoding="utf8").read().split()]   # nombres de clientes: solo en el Mac, nunca en el repositorio
    for w in words:
        if not (top <= w["y"] <= bot): continue
        if w["n"] in ocultar or any(re.search(p, w["t"]) for p in SENSIBLE):
            d.rectangle([w["x"] - 4, w["y"] - 4, w["x"] + w["w"] + 4, w["y"] + w["h"] + 4], fill=(20, 20, 20)); tapadas.append(w["t"])
    frag = im.crop((X0, top, X1, bot))
    frag.save(f"{out}/fragmento.png")
    rel = [[b[0] - X0, b[1] - top, b[2] - X0, b[3] - top] for b in marcas]
    json.dump(dict(size=frag.size, marcas=rel, tapadas=tapadas), open(f"{out}/fragmento.json", "w"), ensure_ascii=False)
    prev = frag.copy(); dp = ImageDraw.Draw(prev, "RGBA")
    for b in rel: dp.rectangle([b[0] - 6, b[1] - 2, b[2] + 6, b[3] + 6], fill=(62, 233, 140, 110))
    prev.save(f"{out}/fragmento-previa.png")
    print("fragmento", frag.size, "líneas subrayadas", len(rel), "tapadas", tapadas)

# ---------- vídeo (versión 2, 29/10/2026, tras las correcciones de Sergio a PUB-0520) ----------
# Cada tramo = fondo de vídeo de archivo (aeropuerto, avión…) + una capa HTML transparente animada encima.
#  - «gancho»: vídeo a pantalla completa con el titular descriptivo (se entiende solo, sin la voz).
#  - «doc»: primero el vídeo; la sentencia entra justo cuando se subraya («doc_entra», segundos desde que empieza la voz).
#  - «lista»: lo que concedió el juez, partida a partida, al ritmo de la voz («en»), y el total.
#  - «consejo»: vídeo enmarcado arriba y el consejo en grande debajo.
# El rótulo de la sentencia es «Sentencia del <juzgado> · <fecha>». Los vídeos de archivo están en la carpeta
# Magnific/stock del Mac (licencia de Magnific: no se suben al repositorio público); procedencia en recursos/stock/FUENTES.md.
DW = 1000   # ancho de la sentencia en el vídeo
STOCK = os.environ.get("STOCK", "/mnt/user-data/uploads/Magnific/stock")

def _cat(spec): return html.escape(spec.get("categoria", "UN CASO REAL"))

def _doc(cuerpo, extra_css=""):
    return f"""<!doctype html><meta charset="utf-8"><style>{css().replace('{W}', str(VW)).replace('{H}', str(VH))}
body{{background:transparent}}
.an{{opacity:0;animation:ap .45s ease-out forwards}} @keyframes ap{{from{{opacity:0;transform:translateY(40px)}}to{{opacity:1;transform:none}}}}
.fi{{opacity:0;animation:fi .5s ease-out forwards}} @keyframes fi{{to{{opacity:1}}}}
.pie{{position:absolute;left:0;right:0;bottom:0;height:560px;background:linear-gradient(rgba(6,22,60,0),rgba(6,22,60,.88) 45%)}}
.top{{position:absolute;left:60px;right:60px;top:120px;display:flex;justify-content:space-between;align-items:center}}
.pill{{font-family:Bangers;font-size:54px;letter-spacing:1px;color:{NAVY};background:{VERDE};padding:6px 22px 2px;box-shadow:6px 6px 0 rgba(0,0,0,.35)}}
{extra_css}</style><body>{cuerpo}</body>"""

def capa_gancho(spec, fondo_img=None):
    t = spec["titulo"]
    bg = f'<img src="{Path(fondo_img).resolve().as_uri()}" style="position:absolute;inset:0;width:{VW}px;height:{VH}px;object-fit:cover">' if fondo_img else ""
    return _doc(f"""{bg}<div class="pie"></div>
<div style="position:absolute;left:0;right:0;top:0;padding:120px 60px 170px;background:linear-gradient(rgba(6,22,60,.95) 72%,rgba(6,22,60,0));display:flex;flex-direction:column;gap:34px">
<div style="display:flex;justify-content:space-between;align-items:center">{logo_caja(84)}<div class="pill">{_cat(spec)}</div></div>
<div class="tit" style="font-size:104px;color:#fff;margin-top:20px">{html.escape(t[0])}</div>
<div style="font:700 48px/1.25 Poppins,sans-serif;color:{VERDE}">{comic.marcado(t[1]).replace('<b>', '<b style="color:#fff">')}</div></div>""")

def capa_doc(spec, frag_png, marcas, size, t0):
    """La sentencia entra en t0 (s); el subrayado empieza 0,5 s después y la cita literal, tras el subrayado."""
    k = DW / size[0]; h = round(size[1] * k); top = 440
    barras = "".join(f'<div class="bar" style="left:{(b[0]-6)*k}px;top:{(b[1]-2)*k}px;height:{(b[3]-b[1]+8)*k}px;width:{(b[2]-b[0]+12)*k}px;animation-delay:{t0+0.4+0.25*i:.2f}s"></div>' for i, b in enumerate(marcas))
    tc = t0 + 0.4 + 0.25 * len(marcas) + 0.2
    rot = f"Sentencia del {spec.get('juzgado','')} · {spec.get('fecha','')}"
    cita = spec.get("cita", "")
    return _doc(f"""<div class="fi" style="position:absolute;inset:0;background:rgba(6,22,60,.86);animation-delay:{t0-0.15:.2f}s"></div>
<div class="pie"></div>
<div class="top">{logo_caja(84)}<div class="pill">{_cat(spec)}</div></div>
<div class="an" style="position:absolute;left:60px;right:60px;top:300px;color:#fff;font:700 38px/1.3 Poppins;animation-delay:{t0:.2f}s">{html.escape(rot)}</div>
<div class="an card" style="top:{top}px;height:{h}px;animation-delay:{t0:.2f}s"><img src="{Path(frag_png).resolve().as_uri()}">{barras}</div>
<div class="an" style="position:absolute;left:50px;right:50px;top:{top + h + 50}px;background:#fff;border-left:16px solid {VERDE};padding:26px 32px;box-shadow:0 14px 34px rgba(0,0,0,.45);animation-delay:{tc:.2f}s">
<div style="font:600 44px/1.3 Poppins,sans-serif;color:{NAVY}">{comic.marcado(cita).replace('<b>','<b style="background:rgba(62,233,140,.55);color:#0b2a6b">')}</div>
<div style="margin-top:12px;font:500 26px Poppins;color:#5a6b8c">Texto literal de la sentencia</div></div>""",
f""".card{{position:absolute;left:{(VW-DW)//2}px;width:{DW}px;background:#fff;box-shadow:0 18px 40px rgba(0,0,0,.5)}} .card img{{width:100%;height:100%;display:block}}
.bar{{position:absolute;background:rgba(62,233,140,.5);transform-origin:left;transform:scaleX(0);animation:s .45s ease-out forwards;mix-blend-mode:multiply}}
@keyframes s{{to{{transform:scaleX(1)}}}}""")

def capa_lista(spec, t, pre):
    filas = "".join(f"""<div class="an fila" style="animation-delay:{pre + it.get('en', 0):.2f}s"><div class="ico">✓</div>
<div><div class="tit" style="font-size:92px;color:#fff">{html.escape(it['t'])}</div><div style="font:600 38px/1.25 Poppins;color:#dfe8ff;margin-top:6px">{html.escape(it['d'])}</div></div></div>""" for it in t["items"])
    ult = pre + max(it.get("en", 0) for it in t["items"]) + 0.6
    return _doc(f"""<div style="position:absolute;inset:0;background:rgba(6,22,60,.72)"></div><div class="pie"></div>
<div style="position:absolute;left:60px;right:60px;top:130px;display:flex;flex-direction:column;gap:40px">
<div style="display:flex;justify-content:space-between;align-items:center">{logo_caja(84)}<div class="pill">{_cat(spec)}</div></div>
<div class="tit" style="font-size:84px;color:{VERDE};margin:14px 0 4px">{html.escape(t['cabecera'])}</div>
{filas}
<div class="an" style="margin-top:8px;background:{VERDE};color:{NAVY};padding:22px 30px;box-shadow:8px 8px 0 rgba(0,0,0,.4);animation-delay:{ult:.2f}s">
<div style="font:700 36px Poppins">{html.escape(t['total'][0])}</div><div class="tit" style="font-size:104px;text-shadow:none">{html.escape(t['total'][1])}</div></div></div>""",
f""".fila{{display:flex;gap:30px;align-items:center;background:rgba(255,255,255,.10);border-left:10px solid {VERDE};padding:34px 30px}}
.ico{{flex:none;width:90px;height:90px;border-radius:50%;background:{VERDE};color:{NAVY};font:700 60px/90px Poppins;text-align:center}}""")

def capa_consejo(spec, t):
    y = MARCO_Y + MARCO_H + 70
    return _doc(f"""<div class="pie"></div>
<div class="top">{logo_caja(84)}<div class="pill">{_cat(spec)}</div></div>
<div style="position:absolute;left:60px;right:60px;top:{y}px;text-align:center">
<div class="tit" style="font-size:{t.get('tam', 120)}px;color:#fff">{comic.marcado(t['grande']).replace('<b>', f'<b style="color:{VERDE}">')}</div>
<div style="margin-top:26px;color:#fff;font:700 46px/1.3 Poppins">{html.escape(t.get('pequeno',''))}</div>
<div style="display:inline-block;margin-top:30px;border:3px solid {VERDE};color:{VERDE};font:600 32px Poppins;padding:10px 24px">{html.escape(t.get('norma',''))}</div></div>""")

MARCO_Y, MARCO_H = 300, 608
def fondo(t, D, sal):
    """Fondo de vídeo de archivo de D segundos. modo «lleno»: a pantalla completa; «marco»: el vídeo apaisado en un recuadro
    sobre una copia desenfocada y oscurecida (así no se pierde nitidez al pasarlo a vertical)."""
    src = t["stock"] if os.path.isabs(t["stock"]) else os.path.join(STOCK, t["stock"])
    ss = t.get("desde", 0); z = t.get("zoom", 0.06)
    cover = f"scale={VW}:{VH}:force_original_aspect_ratio=increase,crop={VW}:{VH}"
    if t.get("modo", "lleno") == "lleno":
        fl = f"[0:v]fps=30,{cover},scale=w='{VW}*(1+{z}*t/{D})':h=-1:eval=frame,crop={VW}:{VH},format=yuv420p[v]"
    else:
        fl = (f"[0:v]fps=30,split[a][b];[a]{cover},boxblur=30:2,eq=brightness=-0.25[bg];"
              f"[b]scale={VW}:-2,scale=w='{VW}*(1+{z}*t/{D})':h=-1:eval=frame,crop={VW}:{MARCO_H}[fg];[bg][fg]overlay=0:{MARCO_Y},format=yuv420p[v]")
    run("ffmpeg", "-v", "error", "-y", "-stream_loop", -1, "-ss", ss, "-i", src, "-t", D, "-filter_complex", fl, "-map", "[v]", "-an", "-r", 30, "-c:v", "libx264", "-crf", 18, sal)

def fotogramas(nav, doc, D, carpeta):
    """Graba la capa HTML (transparente) fotograma a fotograma, a 30 fps, controlando el reloj de las animaciones."""
    import tempfile
    pg = nav.b.new_page(viewport={"width": VW, "height": VH})
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf8") as f: f.write(doc)
    pg.goto(Path(f.name).as_uri()); pg.wait_for_timeout(400)
    pg.evaluate("document.getAnimations().forEach(a=>a.pause())")
    carpeta.mkdir(exist_ok=True)
    for p in carpeta.iterdir(): p.unlink()
    for i in range(int(round(D * 30))):
        pg.evaluate(f"document.getAnimations().forEach(a=>a.currentTime={i*1000/30})")
        pg.screenshot(path=str(carpeta / f"{i:04d}.png"), omit_background=True)
    pg.close(); os.unlink(f.name)

def video(spec, out, nav):
    tmp = Path(out) / "vtmp"; tmp.mkdir(exist_ok=True)
    meta = json.load(open(f"{out}/fragmento.json")); frag = f"{out}/fragmento.png"
    segs = []; PRE = comic.PRE
    tramos = spec["tramos"] + [dict(tipo="cierre", **spec["cierre"])]
    for n, t in enumerate(tramos, 1):
        a = f"{out}/voz/{n:02d}.wav"; va = dur(a) if os.path.exists(a) else 0
        D = round(PRE + va + comic.POST + float(t.get("extra", 0)), 3) if va else float(t.get("dur", 2.5))
        sal = tmp / f"f{n:02d}.mp4"
        frases = t.get("subtitulos") or []; tot = sum(len(f) for f in frases) or 1
        subs = []; t0 = PRE
        for j, f in enumerate(frases):
            dd = (va or D) * len(f) / tot; sp = tmp / f"sub-{n}-{j}.png"; nav.png(subtitulo_html(f), sp, VW, 300, transparente=True)
            subs.append((sp, t0, t0 + dd)); t0 += dd
        if t["tipo"] == "cierre":
            p = tmp / "cierre.png"; nav.png(cierre_html(spec, VW, VH), p, VW, VH)
            ins = ["-loop", 1, "-t", D, "-i", p]; fl = ["[0:v]fps=30,format=rgba[c0]"]; cur = "[c0]"
        else:
            bg = tmp / f"bg{n:02d}.mp4"; fondo(t, D, bg)
            if t["tipo"] == "gancho": doc = capa_gancho(spec)
            elif t["tipo"] == "doc": doc = capa_doc(spec, frag, meta["marcas"], meta["size"], PRE + float(t.get("doc_entra", 0)))
            elif t["tipo"] == "lista": doc = capa_lista(spec, t, PRE)
            else: doc = capa_consejo(spec, t)
            fr = tmp / f"fr{n:02d}"; fotogramas(nav, doc, D, fr)
            ins = ["-i", bg, "-framerate", 30, "-i", fr / "%04d.png"]; fl = ["[0:v][1:v]overlay=0:0:format=auto[c0]"]; cur = "[c0]"
            if t["tipo"] == "gancho":     # portada del vídeo (miniatura): un fotograma del fondo con el titular
                fimg = tmp / "fondo-portada.jpg"; run("ffmpeg", "-v", "error", "-y", "-ss", min(2.0, D / 2), "-i", bg, "-frames:v", 1, "-q:v", 2, fimg)
                nav.png(capa_gancho(spec, fimg), tmp / "portada.png", VW, VH)
        k0 = 1 if t["tipo"] == "cierre" else 2
        for j, (sp, a0, a1) in enumerate(subs):
            ins += ["-loop", 1, "-t", D, "-i", sp]
            y = 1590 if t["tipo"] == "cierre" else 1500
            fl.append(f"{cur}[{k0+j}:v]overlay=0:{y}:enable='between(t,{a0:.3f},{a1:.3f})'[o{j}]"); cur = f"[o{j}]"
        fl.append(f"{cur}{'fade=t=in:st=0:d=0.2,' if n == 1 else ''}format=yuv420p[v]")
        run("ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fl), "-map", "[v]", "-t", D, "-r", 30, "-c:v", "libx264", "-crf", 18, sal)
        segs.append((sal, a if va else None, D))
        print("tramo", n, t["tipo"], f"{D:.2f}s")
    comic.mezclar_y_cerrar(spec, out, tmp, segs)

def voz(spec, out):
    d = spec["_dir"]; os.makedirs(f"{out}/voz", exist_ok=True)
    tramos = spec["tramos"] + [spec["cierre"]]
    for n, t in enumerate(tramos, 1):
        if not t.get("voz"): continue
        run("ffmpeg", "-v", "error", "-y", "-i", comic.ruta(d, t["voz"]), "-af",
            "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,"
            "silenceremove=stop_periods=-1:stop_duration=0.22:stop_threshold=-42dB:stop_silence=0.22,atempo=1.08,aresample=48000", "-ac", "1", f"{out}/voz/{n:02d}.wav")

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "ocr": print(len(ocr(sys.argv[2])), "palabras"); sys.exit()
    spec = comic.cargar(sys.argv[2]); out = sys.argv[3]; os.makedirs(out, exist_ok=True)
    if cmd in ("recorte", "todo"): recorte(spec, out)
    if cmd == "todo": voz(spec, out)
    if cmd in ("todo", "video"):          # «video»: solo vuelve a montar (usa el recorte y las voces ya preparados)
        with Navegador() as nav: video(spec, out, nav)
