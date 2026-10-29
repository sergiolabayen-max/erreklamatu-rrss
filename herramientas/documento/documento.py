#!/usr/bin/env python3
"""«El documento, subrayado» (29/10/2026): vídeo vertical con un fragmento real de una sentencia del despacho,
anonimizado, con la frase clave subrayada en verde, la explicación y el cierre de marca.

Uso:
  python3 documento.py ocr pagina.png                   -> pagina.tsv (tesseract, castellano)
  python3 documento.py recorte spec.json carpeta        -> fragmento anonimizado + vista previa con el subrayado
  python3 documento.py todo spec.json carpeta           -> voz + recorte + vídeo 1080 × 1920

Spec (JSON):
{
 "id": "D1-athletic", "categoria": "UN CASO NUESTRO", "juzgado": "Juzgado de Primera Instancia n.º 9 de Bilbao",
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

# ---------- vídeo ----------
DW = 960   # ancho del documento en el vídeo
def fondo_doc(spec, frag_png, marcas, sub, size):
    """Página del documento en el vídeo: tarjeta de papel con la franja verde dibujada en CSS (animación de izquierda a derecha)."""
    k = DW / size[0]; h = round(size[1] * k)
    barras = "".join(f'<div class="bar" style="left:{(b[0]-6)*k}px;top:{(b[1]-2)*k}px;height:{(b[3]-b[1]+8)*k}px;width:{(b[2]-b[0]+12)*k}px;animation-delay:{0.35+0.45*i}s"></div>' for i, b in enumerate(marcas)) if sub else ""
    return f"""<!doctype html><meta charset="utf-8"><style>{css().replace('{W}', str(VW)).replace('{H}', str(VH))}
.card{{position:absolute;left:{(VW-DW)//2}px;top:410px;width:{DW}px;height:{h}px;background:#fff;box-shadow:0 18px 40px rgba(0,0,0,.45)}}
.card img{{width:100%;height:100%;display:block}}
.bar{{position:absolute;background:rgba(62,233,140,.45);transform-origin:left;transform:scaleX(0);animation:s .5s ease-out forwards;mix-blend-mode:multiply}}
@keyframes s{{to{{transform:scaleX(1)}}}}</style><body>
<div style="position:absolute;left:60px;top:150px">{logo_caja(84)}</div>
<div class="tit" style="position:absolute;right:60px;top:158px;font-size:58px;color:{VERDE}">{html.escape(spec.get('categoria','UN CASO NUESTRO'))}</div>
<div style="position:absolute;left:60px;right:60px;top:280px;color:#cfe0ff;font:600 28px/1.3 Poppins">{html.escape(spec.get('juzgado',''))} · datos personales ocultos</div>
<div class="card"><img src="{Path(frag_png).resolve().as_uri()}">{barras}</div>{cita_html(spec) if sub else ''}</body>"""

def cita_html(spec):
    """La frase subrayada, copiada literalmente de la sentencia y en grande: en el móvil el escaneo no se lee."""
    c = spec.get("cita")
    if not c: return ""
    return f"""<div style="position:absolute;left:50px;right:50px;top:{spec.get('cita_top', 900)}px;background:#fff;border-left:16px solid {VERDE};padding:30px 36px;box-shadow:0 14px 34px rgba(0,0,0,.45);opacity:0;animation:f .4s ease-out 1.1s forwards">
<div style="font:600 44px/1.32 Poppins,sans-serif;color:{NAVY}">{comic.marcado(c).replace('<b>','<b style="background:rgba(62,233,140,.55);color:#0b2a6b">')}</div>
<div style="margin-top:14px;font:500 26px Poppins;color:#5a6b8c">Texto literal de la sentencia</div></div><style>@keyframes f{{to{{opacity:1}}}}</style>"""

def portada(spec, frag_png):
    g = spec["gancho"]
    return f"""<!doctype html><meta charset="utf-8"><style>{css().replace('{W}', str(VW)).replace('{H}', str(VH))}</style><body>
<img src="{Path(frag_png).resolve().as_uri()}" style="position:absolute;left:-60px;top:520px;width:1200px;filter:blur(3px);opacity:.35">
<div style="position:absolute;inset:0;background:linear-gradient({NAVY} 35%,rgba(11,42,107,.55) 65%,{NAVY})"></div>
<div style="position:absolute;left:60px;top:150px">{logo_caja(84)}</div>
<div class="tit" style="position:absolute;right:60px;top:158px;font-size:58px;color:{VERDE}">{html.escape(spec.get('categoria','UN CASO NUESTRO'))}</div>
<div class="tit" style="position:absolute;left:60px;right:60px;top:420px;font-size:120px;color:#fff">{html.escape(g[0])}<br><span style="color:{VERDE}">{html.escape(g[1])}</span></div>
<div style="position:absolute;left:60px;right:60px;bottom:260px;color:#fff;font:600 38px Poppins">Lo que dijo el juez, subrayado 👇</div></body>"""

def tarjeta(spec, t):
    return f"""<!doctype html><meta charset="utf-8"><style>{css().replace('{W}', str(VW)).replace('{H}', str(VH))}</style><body>
<div style="position:absolute;left:60px;top:150px">{logo_caja(84)}</div>
<div class="tit" style="position:absolute;right:60px;top:158px;font-size:58px;color:{VERDE}">{html.escape(spec.get('categoria','UN CASO NUESTRO'))}</div>
<div style="position:absolute;left:70px;right:70px;top:520px;text-align:center">
<div class="tit" style="font-size:{t.get('tam',104)}px;color:#fff">{comic.marcado(t['grande']).replace('<b>', f'<b style="color:{VERDE}">')}</div>
<div style="margin-top:40px;color:#dfe8ff;font:600 40px/1.35 Poppins">{html.escape(t.get('pequeno',''))}</div></div></body>"""

def video(spec, out, nav):
    tmp = Path(out) / "vtmp"; tmp.mkdir(exist_ok=True)
    meta = json.load(open(f"{out}/fragmento.json")); frag = f"{out}/fragmento.png"
    nav.png(portada(spec, frag), tmp / "portada.png", VW, VH)
    segs = []
    run("ffmpeg", "-v", "error", "-y", "-loop", 1, "-t", 1.2, "-i", tmp / "portada.png", "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", 18, tmp / "s00.mp4")
    segs.append((tmp / "s00.mp4", None, 1.2))
    tramos = spec["tramos"] + [dict(tipo="cierre", **spec["cierre"])]
    for n, t in enumerate(tramos, 1):
        a = f"{out}/voz/{n:02d}.wav"; va = dur(a) if os.path.exists(a) else 0
        D = round(comic.PRE + va + comic.POST + (0.6 if t.get("subrayado") else 0), 3) if va else float(t.get("dur", 2.5))
        if t["tipo"] == "doc":
            # la animación CSS se graba fotograma a fotograma con Playwright (vídeo de la página)
            seg = tmp / f"s{n:02d}.mp4"; grabar(nav, fondo_doc(spec, frag, meta["marcas"], t.get("subrayado"), meta["size"]), seg, D, zoom=t.get("subrayado"))
            base = seg
        else:
            p = tmp / f"t{n:02d}.png"; nav.png(cierre_html(spec, VW, VH) if t["tipo"] == "cierre" else tarjeta(spec, t), p, VW, VH)
            base = tmp / f"b{n:02d}.mp4"; run("ffmpeg", "-v", "error", "-y", "-loop", 1, "-t", D, "-i", p, "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", 18, base)
        frases = t.get("subtitulos") or []; tot = sum(len(f) for f in frases) or 1; t0 = comic.PRE; ins = ["-i", base]; fl = []; cur = "[0:v]"
        for j, f in enumerate(frases):
            dd = (va or D) * len(f) / tot; sp = tmp / f"sub-{n}-{j}.png"; nav.png(subtitulo_html(f), sp, VW, 300, transparente=True)
            ins += ["-loop", "1", "-t", D, "-i", sp]; y = 1520 if t["tipo"] != "cierre" else 1590
            fl.append(f"{cur}[{j+1}:v]overlay=0:{y}:enable='between(t,{t0:.3f},{t0+dd:.3f})'[o{j}]"); cur = f"[o{j}]"; t0 += dd
        fl.append(f"{cur}fade=t=in:st=0:d=0.2,format=yuv420p[v]")
        sal = tmp / f"f{n:02d}.mp4"
        run("ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fl), "-map", "[v]", "-t", D, "-r", 30, "-c:v", "libx264", "-crf", 18, sal)
        segs.append((sal, a if va else None, D))
    comic.mezclar_y_cerrar(spec, out, tmp, segs)

def grabar(nav, doc, sal, D, zoom=False):
    """Graba una página HTML animada: captura fotogramas con Playwright a 30 fps (la animación se controla con el reloj de la página)."""
    import tempfile
    pg = nav.b.new_page(viewport={"width": VW, "height": VH})
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf8") as f: f.write(doc)
    pg.goto(Path(f.name).as_uri()); pg.wait_for_timeout(300)
    pg.evaluate("document.getAnimations().forEach(a=>a.pause())")
    fr = Path(str(sal) + "_fr"); fr.mkdir(exist_ok=True); n = int(D * 30)
    for i in range(n):
        pg.evaluate(f"document.getAnimations().forEach(a=>a.currentTime={i*1000/30})")
        pg.screenshot(path=str(fr / f"{i:04d}.png"))
    pg.close(); os.unlink(f.name)
    z = f",scale=w='{VW}*(1+0.05*t/{D})':h=-1:eval=frame,crop={VW}:{VH}" if zoom else ""
    run("ffmpeg", "-v", "error", "-y", "-framerate", 30, "-i", fr / "%04d.png", "-vf", f"format=yuv420p{z}", "-c:v", "libx264", "-crf", 18, sal)
    for p in fr.iterdir(): p.unlink()
    fr.rmdir()

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
    if cmd == "todo":
        voz(spec, out)
        with Navegador() as nav: video(spec, out, nav)
