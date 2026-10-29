#!/usr/bin/env python3
"""Cómics de Erreklamatu, versión 2 (28/10/2026). Rehecho porque los scripts de octubre se perdieron (vivían en un scratchpad).

Uso:
  python3 comic.py recortar entrada.png salida.png      quita el marco blanco que mete Magnific y deja la viñeta a 1856 × 2304
  python3 comic.py laminas spec.json carpeta            láminas 1080 × 1350 (carrusel de Instagram), con y sin texto
  python3 comic.py voz spec.json carpeta                 procesa las locuciones (quita pausas largas, acelera ×1,08)
  python3 comic.py video spec.json carpeta              vídeo 1080 × 1920 a 30 fps (5 redes) y portada 9:16
  python3 comic.py todo spec.json carpeta               voz + laminas + video

Spec (JSON; coordenadas en píxeles de la lámina de 1080 × 1350):
{
  "id": "PUB-XXXX", "categoria": "TEMPORAL", "abogado": "Jon Ortiz",
  "gancho": ["Te cancelan por el temporal:", "el hotel lo paga la aerolínea"],   # primer segundo del vídeo y portada del carrusel
  "laminas": [
    {"img": "viñetas/01.png",
     "bocadillos": [{"texto": "¿Y ahora dónde *duermo*?", "x": 60, "y": 60, "w": 520, "cola": [420, 520]}],   # *así* = azul
     "rotulo": {"texto": "Consulta gratuita · Jon Ortiz, abogado de ERREKLAMATU", "x": 640, "y": 40, "w": 400},
     "voz": "voz/01.mp3", "subtitulos": ["Te cancelan el vuelo por el temporal.", "Y nadie te dice dónde dormir."]}
  ],
  "cierre": {"titulo": "¿TE HA PASADO?", "texto": "Te ayudamos a reclamar a la aerolínea.", "voz": "voz/cierre.mp3",
             "subtitulos": ["Llama al 944 027 596"], "legal": "Reglamento (CE) 261/2004, arts. 5, 8 y 9. Cada caso se estudia de forma individual."},
  "musica": "tranquila"            # sintonía de sistema/sintonia.py bajo la voz; null = sin música
}
Rutas relativas: respecto a la carpeta del spec. Lo que Claude no puede hacer: oír la locución. Hay que revisarla al oído.
"""
import json, os, re, subprocess, sys, html, shutil, tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SISTEMA = AQUI.parent / "sistema"
FUENTES = AQUI / "fuentes"
LOGO = SISTEMA / "logo-alta.png"
NAVY, VERDE, AZUL_TXT = "#0b2a6b", "#3ee98c", "#1f4fa8"
W, H = 1080, 1350               # lámina
VW, VH = 1080, 1920             # vídeo
PX, PY, PW = 66, 270, 948       # panel dentro del vídeo
PH = round(PW * H / W)          # 1185
PRE, POST, FUNDIDO, ZOOM, PORTADA = 0.12, 0.28, 0.2, 0.06, 0.8

def run(*a, **k): return subprocess.run([str(x) for x in a], check=True, **k)
def dur(f): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)]).decode())

# ---------- recortar ----------
def recortar(ent, sal, umbral=245):
    from PIL import Image, ImageChops
    im = Image.open(ent).convert("RGB")
    fondo = Image.new("RGB", im.size, (255, 255, 255))
    diff = ImageChops.difference(im, fondo).convert("L").point(lambda p: 255 if p > 255 - umbral else 0)
    caja = diff.getbbox() or (0, 0, *im.size)
    im = im.crop(caja)
    # ajusta a 4:5 recortando lo que sobre (sin deformar) y escala a 1856 × 2304
    w, h = im.size; obj = 1856 / 2304
    if w / h > obj: nw = round(h * obj); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else: nh = round(w / obj); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im.resize((1856, 2304), Image.LANCZOS).save(sal)
    print(ent, "->", sal, "recorte", caja)

# ---------- HTML ----------
def css():
    f = lambda n: (FUENTES / n).as_uri()
    return f"""
@font-face{{font-family:Bangers;src:url({f('Bangers-Regular.ttf')})}}
@font-face{{font-family:CN;src:url({f('ComicNeue-Bold.ttf')});font-weight:700}}
@font-face{{font-family:CN;src:url({f('ComicNeue-Regular.ttf')});font-weight:400}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:{{W}}px;height:{{H}}px;overflow:hidden;background:{NAVY}}}
.burb{{position:absolute;background:#fff;border:3px solid #111;border-radius:34px;padding:22px 28px;font:700 38px/1.25 CN,sans-serif;color:#111;text-align:center}}
.burb b{{color:{AZUL_TXT}}}
.rot{{position:absolute;background:{NAVY};color:#fff;font:700 30px/1.3 CN,sans-serif;padding:14px 20px;box-shadow:7px 7px 0 {VERDE};border:2px solid #fff}}
.rot b{{color:{VERDE}}}
svg.colas{{position:absolute;left:0;top:0}}
.tit{{font-family:Bangers;letter-spacing:1px;line-height:.98;text-shadow:5px 5px 0 rgba(0,0,0,.35)}}
"""

def marcado(t):
    t = html.escape(t)
    return re.sub(r"\*(.+?)\*", r"<b>\1</b>", t)

def cola_svg(b):
    """Cola del bocadillo: triángulo desde el borde inferior (o superior) de la caja hasta la punta."""
    if not b.get("cola"): return ""
    x, y, w = b["x"], b["y"], b["w"]; hx, hy = b["cola"]
    h = b.get("_h", 120); base_y = y + h - 3 if hy > y + h else y + 3
    cx = min(max(hx, x + 60), x + w - 60)
    return f'<polygon points="{cx-26},{base_y} {cx+26},{base_y} {hx},{hy}" fill="#fff" stroke="#111" stroke-width="3" stroke-linejoin="round"/>' \
           f'<line x1="{cx-23}" y1="{base_y}" x2="{cx+23}" y2="{base_y}" stroke="#fff" stroke-width="6"/>'

def lamina_html(img, lam, con_texto, contador=None, gancho=None):
    capas = [f'<img src="{Path(img).resolve().as_uri()}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px">']
    colas = []
    if con_texto:
        for i, b in enumerate(lam.get("bocadillos", [])):
            capas.append(f'<div class="burb" id="b{i}" style="left:{b["x"]}px;top:{b["y"]}px;width:{b["w"]}px">{marcado(b["texto"])}</div>')
            colas.append(b)
        r = lam.get("rotulo")
        if r: capas.append(f'<div class="rot" style="left:{r["x"]}px;top:{r["y"]}px;width:{r["w"]}px">{marcado(r["texto"])}</div>')
        if gancho:
            capas.append(f'<div style="position:absolute;left:0;top:0;width:{W}px;height:420px;background:linear-gradient({NAVY} 70%,rgba(11,42,107,0))"></div>')
            capas.append(f'<div class="tit" style="position:absolute;left:44px;top:40px;width:992px;font-size:96px;color:#fff">{html.escape(gancho[0])}<br><span style="color:{VERDE}">{html.escape(gancho[1])}</span></div>')
    if contador:
        capas.append(f'<div style="position:absolute;right:26px;bottom:22px;background:rgba(0,0,0,.55);color:#fff;font:700 24px CN;padding:6px 14px;border-radius:16px">{contador}</div>')
    capas.append(f'<div style="position:absolute;inset:0;border:6px solid #111"></div>')
    return capas, colas

def pagina(capas, colas, w=W, h=H):
    return f"""<!doctype html><meta charset="utf-8"><style>{css().replace('{W}', str(w)).replace('{H}', str(h))}</style>
<body>{capas[0]}<svg class="colas" width="{w}" height="{h}" id="svg"></svg>{''.join(capas[1:])}
<script>const C={json.dumps([{k: v for k, v in b.items() if k != 'texto'} for b in colas])};
let s='';C.forEach((b,i)=>{{const e=document.getElementById('b'+i);const h=e.offsetHeight;const x=b.x,y=b.y,w=b.w;const [hx,hy]=b.cola||[null,null];
if(hx===null)return;const below=hy>y+h;const by=below?y+h-3:y+3;const cx=Math.min(Math.max(hx,x+60),x+w-60);
s+=`<polygon points="${{cx-26}},${{by}} ${{cx+26}},${{by}} ${{hx}},${{hy}}" fill="#fff" stroke="#111" stroke-width="3" stroke-linejoin="round"/>`;}});
document.getElementById('svg').innerHTML=s;
// la cola va por debajo de la caja: se tapa su unión con la caja dibujando la caja encima (orden del DOM)
</script></body>"""

class Navegador:
    def __enter__(self):
        from playwright.sync_api import sync_playwright
        self.p = sync_playwright().start(); self.b = self.p.chromium.launch(); return self
    def png(self, doc, sal, w=W, h=H, transparente=False):
        pg = self.b.new_page(viewport={"width": w, "height": h})
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf8") as f: f.write(doc)
        pg.goto(Path(f.name).as_uri()); pg.wait_for_timeout(250)
        pg.screenshot(path=str(sal), omit_background=transparente); pg.close(); os.unlink(f.name)
    def __exit__(self, *a): self.b.close(); self.p.stop()

def ruta(spec_dir, r): return r if os.path.isabs(r) else str(Path(spec_dir) / r)

# ---------- láminas ----------
def laminas(spec, out, nav):
    d = spec["_dir"]; L = spec["laminas"]; n = len(L) + 1
    for i, lam in enumerate(L, 1):
        img = ruta(d, lam["img"])
        g = spec.get("gancho") if i == 1 else None
        for con, suf in ((True, ""), (False, "-limpia")):
            capas, colas = lamina_html(img, lam, con, contador=f"{i}/{n}" if con else None, gancho=g)
            nav.png(pagina(capas, colas), f"{out}/{spec['id']}-c{i:02d}{suf}.png")
        # versión para vídeo: con bocadillos, sin gancho ni contador (el gancho va en la portada del vídeo)
        capas, colas = lamina_html(img, lam, True)
        nav.png(pagina(capas, colas), f"{out}/v{i:02d}.png")
        capas, colas = lamina_html(img, lam, False)
        nav.png(pagina(capas, colas), f"{out}/v{i:02d}-limpia.png")
    nav.png(cierre_html(spec, W, H), f"{out}/{spec['id']}-c{n:02d}.png")
    print("láminas:", n)

def logo_caja(alto=64):
    return f'<div style="display:inline-block;background:#fff;border-radius:6px;padding:10px 16px"><img src="{LOGO.as_uri()}" style="height:{alto - 20}px;display:block"></div>'

def cierre_html(spec, w, h):
    c = spec["cierre"]; v = h == VH
    top = 300 if v else 160
    return f"""<!doctype html><meta charset="utf-8"><style>{css().replace('{W}', str(w)).replace('{H}', str(h))}</style><body>
<div style="position:absolute;left:0;top:{top}px;width:{w}px;text-align:center;color:#fff">
<div class="tit" style="font-size:{110 if v else 100}px;color:{VERDE}">{html.escape(c.get('titulo', '¿TE HA PASADO?'))}</div>
<div style="font:600 40px Poppins,sans-serif;margin-top:26px">{html.escape(c.get('texto', ''))}</div>
<div style="display:inline-block;margin-top:40px;background:{VERDE};color:{NAVY};font:700 32px Poppins;padding:14px 30px">Consulta gratuita · Solo cobramos si ganamos</div>
<div class="tit" style="font-size:{130 if v else 120}px;margin-top:50px">944 027 596</div>
<div style="font:500 34px Poppins;margin-top:14px">info@erreklamatu.com · erreklamatu.com</div>
<div style="margin-top:50px">{logo_caja(90)}</div></div>
<div style="position:absolute;left:60px;right:60px;bottom:{440 if v else 50}px;text-align:center;color:#9fb3dd;font:400 22px Poppins">{html.escape(c.get('legal', ''))}</div></body>"""

def fondo_video(spec):
    return f"""<!doctype html><meta charset="utf-8"><style>{css().replace('{W}', str(VW)).replace('{H}', str(VH))}</style><body>
<div style="position:absolute;left:{PX}px;top:176px">{logo_caja(84)}</div>
<div class="tit" style="position:absolute;right:{VW - PX - PW}px;top:184px;font-size:62px;color:{VERDE}">{html.escape(spec.get('categoria', ''))}</div></body>"""

def portada_video(spec, img):
    """Primer segundo del vídeo: el gancho en grande, la viñeta debajo y quién lo explica. Maquetado en columna para que nada se pise."""
    g = spec["gancho"]
    return f"""<!doctype html><meta charset="utf-8"><style>{css().replace('{W}', str(VW)).replace('{H}', str(VH))}
.col{{position:absolute;left:{PX}px;top:110px;width:{PW}px;height:{VH - 110 - 120}px;display:flex;flex-direction:column;gap:30px}}
.cab{{display:flex;justify-content:space-between;align-items:center}}
.ima{{flex:1;min-height:0;display:flex;justify-content:center}} .ima img{{height:100%;max-width:100%;object-fit:contain;border:6px solid {VERDE}}}</style><body>
<div class="col"><div class="cab">{logo_caja(84)}<div class="tit" style="font-size:62px;color:{VERDE}">{html.escape(spec.get('categoria', ''))}</div></div>
<div class="tit" style="font-size:112px;color:#fff">{html.escape(g[0])}<br><span style="color:{VERDE}">{html.escape(g[1])}</span></div>
<div class="ima"><img src="{Path(img).resolve().as_uri()}"></div>
<div style="background:{VERDE};color:{NAVY};font:700 40px Poppins;padding:22px 28px;box-shadow:8px 8px 0 #000">El abogado {html.escape(spec.get('abogado', ''))} te explica qué hacer</div></div></body>"""

def subtitulo_html(t):
    return f"""<!doctype html><meta charset="utf-8"><style>body{{width:{VW}px;height:300px;background:transparent;margin:0}}</style><body>
<div style="position:absolute;left:90px;right:90px;top:20px;text-align:center;color:#fff;font:700 52px/1.3 Poppins,sans-serif;text-shadow:0 3px 8px rgba(0,0,0,.4)">{html.escape(t)}</div></body>"""

# ---------- voz ----------
def voz(spec, out):
    d = spec["_dir"]; os.makedirs(f"{out}/voz", exist_ok=True)
    items = [(f"{i:02d}", l.get("voz")) for i, l in enumerate(spec["laminas"], 1)] + [("cierre", spec["cierre"].get("voz"))]
    for k, f in items:
        if not f: continue
        sal = f"{out}/voz/{k}.wav"
        # quita silencio inicial y final, acorta pausas internas a 0,22 s y acelera ×1,08 (método del 15/10)
        run("ffmpeg", "-v", "error", "-y", "-i", ruta(d, f), "-af",
            "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,"
            "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,"
            "silenceremove=stop_periods=-1:stop_duration=0.22:stop_threshold=-42dB:stop_silence=0.22,"
            "atempo=1.08,aresample=48000", "-ac", "1", sal)
        print(k, f"{dur(ruta(d, f)):.2f}s ->", f"{dur(sal):.2f}s")

# ---------- vídeo ----------
def video(spec, out, nav):
    d = spec["_dir"]; tmp = Path(out) / "vtmp"; tmp.mkdir(exist_ok=True)
    nav.png(fondo_video(spec), tmp / "fondo.png", VW, VH)
    nav.png(portada_video(spec, f"{out}/v01-limpia.png"), tmp / "portada.png", VW, VH)
    nav.png(cierre_html(spec, VW, VH), tmp / "cierre.png", VW, VH)
    segs = []     # (archivo de vídeo, archivo de audio o None, duración)
    # portada (gancho): 0,8 s, sin voz
    run("ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", PORTADA, "-i", tmp / "portada.png", "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", 18, tmp / "s00.mp4")
    segs.append((tmp / "s00.mp4", None, PORTADA))
    todas = [(f"{i:02d}", l) for i, l in enumerate(spec["laminas"], 1)] + [("cierre", spec["cierre"])]
    subs_total = []
    for k, l in todas:
        a = f"{out}/voz/{k}.wav"; va = dur(a) if os.path.exists(a) else 0
        extra = 0.35 if 0 < va < 1.6 else 0
        D = round(PRE + va + POST + extra, 3) if va else float(l.get("dur", 2.0))
        frases = l.get("subtitulos") or []
        # reparto de tiempos por número de caracteres
        tot = sum(len(f) for f in frases) or 1; t = PRE; tiempos = []
        for f in frases:
            dd = va * len(f) / tot if va else D / max(len(frases), 1); tiempos.append((t, t + dd)); t += dd
        ins = []; filt = []
        if k == "cierre":
            ins += ["-loop", "1", "-t", D, "-i", tmp / "cierre.png"]; base = "[0:v]"; nxt = 1
            filt.append(f"{base}fps=30,format=rgba[bg]"); cur = "[bg]"
        else:
            ins += ["-loop", "1", "-t", D, "-i", tmp / "fondo.png", "-loop", "1", "-t", D, "-i", f"{out}/v{k}-limpia.png", "-loop", "1", "-t", D, "-i", f"{out}/v{k}.png"]; nxt = 3
            z = f"scale=w='{PW}*(1+{ZOOM}*t/{D})':h=-1:eval=frame,crop={PW}:{PH}"
            filt += [f"[1:v]fps=30,{z}[lim]", f"[2:v]fps=30,{z},format=rgba,fade=t=in:st={PRE + 0.05}:d=0.25:alpha=1[tex]",
                     f"[0:v]fps=30[bg0]", f"[bg0][lim]overlay={PX}:{PY}[bg1]", f"[bg1][tex]overlay={PX}:{PY}[bg]"]
            cur = "[bg]"
        for j, (f, (t0, t1)) in enumerate(zip(frases, tiempos)):
            p = tmp / f"sub-{k}-{j}.png"; nav.png(subtitulo_html(f), p, VW, 300, transparente=True)
            ins += ["-loop", "1", "-t", D, "-i", p]
            y = 1500 if k != "cierre" else 1590
            filt.append(f"{cur}[{nxt}:v]overlay=0:{y}:enable='between(t,{t0:.3f},{t1:.3f})'[o{j}]"); cur = f"[o{j}]"; nxt += 1
            subs_total.append(f)
        filt.append(f"{cur}fade=t=in:st=0:d={FUNDIDO},format=yuv420p[v]")
        sal = tmp / f"s{k}.mp4"
        run("ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(filt), "-map", "[v]", "-t", D, "-r", 30, "-c:v", "libx264", "-crf", 18, sal)
        segs.append((sal, a if va else None, D))
    mezclar_y_cerrar(spec, out, tmp, segs)

def mezclar_y_cerrar(spec, out, tmp, segs):
    """Voz en su sitio, música con ducking, concatenación, barra de progreso, portada y copia ligera. Lo usan también otros formatos."""
    d = spec["_dir"]; tmp = Path(tmp)
    total = sum(s[2] for s in segs)
    # audio: silencio + voz de cada tramo en su sitio
    partes = []; t = 0.0
    for v_, a_, D in segs:
        if a_: partes.append((a_, t + PRE))
        t += D
    ins = []; fl = []
    for i, (a_, t0) in enumerate(partes):
        ins += ["-i", a_]; fl.append(f"[{i}:a]adelay={int(t0 * 1000)}:all=1,apad[a{i}]")
    fl.append("".join(f"[a{i}]" for i in range(len(partes))) + f"amix=inputs={len(partes)}:normalize=0:duration=longest,atrim=0:{total:.3f}[voz]")
    vozf = tmp / "voz.wav"
    run("ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fl), "-map", "[voz]", "-ar", 48000, "-ac", 2, vozf)
    audio = vozf
    if spec.get("musica"):
        mus = tmp / "musica.wav"; cierre_d = segs[-1][2]; m = spec["musica"]
        if m in ("viva", "tranquila"):        # sintonía generada por código
            run(sys.executable, SISTEMA / "sintonia.py", mus, f"{total:.2f}", m, f"{cierre_d:.2f}"); vol = 0.16
        else:                                  # pista de archivo (p. ej. la lo-fi de 100 BPM que eligió Sergio el 16/10): en bucle, recortada y con fundidos
            run("ffmpeg", "-v", "error", "-y", "-stream_loop", -1, "-i", ruta(d, m), "-t", f"{total:.3f}", "-af",
                f"afade=t=in:d=0.4,afade=t=out:st={max(total - 1.2, 0):.3f}:d=1.2", "-ar", 48000, "-ac", 2, mus); vol = 0.22
        audio = tmp / "mezcla.wav"
        run("ffmpeg", "-v", "error", "-y", "-i", vozf, "-i", mus, "-filter_complex",
            f"[1:a]volume={vol}[m];[m][0:a]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=300[md];[0:a][md]amix=inputs=2:normalize=0,alimiter=limit=0.95[a]",
            "-map", "[a]", "-ar", 48000, audio)
    with open(tmp / "lista.txt", "w") as F:
        for v_, _, _ in segs: F.write(f"file '{Path(v_).resolve()}'\n")
    run("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", 0, "-i", tmp / "lista.txt", "-c", "copy", tmp / "solo_video.mp4")
    # barra de progreso verde abajo
    final = f"{out}/{spec['id']}-video.mp4"
    run("ffmpeg", "-v", "error", "-y", "-i", tmp / "solo_video.mp4", "-i", audio, "-f", "lavfi", "-i", f"color=c=0x3ee98c:s={VW}x12:r=30:d={total:.3f}",
        "-filter_complex", f"[0:v][2:v]overlay=x='-W+W*t/{total:.3f}':y={VH - 12}:shortest=1,format=yuv420p[v]",
        "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", 21, "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", final)
    shutil.copy(tmp / "portada.png", f"{out}/{spec['id']}-portada.png")
    # copia ligera para Meta (< 10 MiB)
    if os.path.getsize(final) > 9.5 * 2**20:
        run("ffmpeg", "-v", "error", "-y", "-i", final, "-c:v", "libx264", "-preset", "veryfast", "-crf", 27, "-c:a", "copy", "-movflags", "+faststart", f"{out}/{spec['id']}-video-meta.mp4")
    print("vídeo:", final, f"{total:.1f}s", f"{os.path.getsize(final) / 2**20:.1f} MiB")

def cargar(f):
    s = json.load(open(f, encoding="utf8")); s["_dir"] = str(Path(f).resolve().parent); return s

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "recortar": recortar(sys.argv[2], sys.argv[3]); sys.exit()
    spec = cargar(sys.argv[2]); out = sys.argv[3]; os.makedirs(out, exist_ok=True)
    if cmd in ("voz", "todo"): voz(spec, out)
    if cmd in ("laminas", "video", "todo"):
        with Navegador() as nav:
            if cmd in ("laminas", "todo"): laminas(spec, out, nav)
            if cmd in ("video", "todo"): video(spec, out, nav)
