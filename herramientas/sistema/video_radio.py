#!/usr/bin/env python3
"""Clips verticales (1080 x 1920) a partir de un AUDIO de radio, «lo más vídeo posible» sin inventar imagen (9 de octubre de 2026).

Uso:
  python3 video_radio.py tiempos spec.json             -> spec.tiempos.json (lo hace video_clips.py: mismo cálculo)
  python3 video_radio.py montar  spec.json carpeta [id,id]

Qué añade frente al «vídeo fijo» de las tandas anteriores (retrato quieto + cartel quieto):
- Planos con movimiento lento (Ken Burns) sobre fotos del archivo del centro de control (colección `fotos`), y cambio de plano
  cada 5-9 s mientras habla el abogado, siempre en el corte entre dos rótulos. Fundido corto (0,3 s) entre planos.
- Cartel «En la radio» (emisora y programa, sin año) cuando habla quien presenta, también con movimiento lento.
- Barras del sonido animadas (energía real del audio por bandas, 25 veces por segundo) en la parte baja de la imagen.
- Barra de progreso fina arriba de la imagen.
- Subtítulos grandes (72 px) con la palabra que suena resaltada (verde sobre blanco en las respuestas, blanco sobre verde en las preguntas).
  El momento de cada palabra sale del cálculo de tiempos (reconocimiento + reparto): es aproximado; se revisa oyendo.
El resto (cabecera con quién habla y titular, crédito, teléfono, pie, cortinilla de cierre) es el de video_clips.py, diseño «zonas».

spec.json (además de lo de video_clips.py: audio, modelo, vad, idioma, credito, rotulos, preguntan, prefijo, crf, preset, clips):
  "fuente": audio original con buena calidad (mp3) del que sale el sonido del clip
  "emisora", "programa": textos del cartel
  "planos": {"jon": [{"foto": ruta, "a": [x, y, lado], "b": [x, y, lado]}, ...], ...}  cuadrado inicial y final de cada plano (Ken Burns)
Requiere numpy, opencv (cv2), Pillow, soundfile, ffmpeg con libass y la fuente Poppins.
"""
import json, os, re, subprocess, sys, tempfile, textwrap
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import video_clips as vc
from PIL import Image, ImageDraw

T = 1080; FPS = 25
L = dict(vc.DISENOS["zonas"], sub_tam=72, sub_car=19)
VERDE_ASS, BLANCO_ASS = "&H0087E800&", "&H00FFFFFF&"
BARRAS_Y, BARRAS_H, BARRAS_N, BARRAS_W = 554, 42, 30, 560      # dentro del recuadro de 1080: de 554 a 596 (1034-1076 en pantalla), entre la barbilla y los subtítulos

def cartel_img(spec, ruta):
    """Cartel «En la radio · emisora · programa», 1080 x 1080, en azul de marca con un micrófono dibujado (sin logotipos de la emisora)."""
    eu = spec.get("idioma") == "eu"
    im = Image.new("RGB", (T, T), vc.NAVY); d = ImageDraw.Draw(im)
    for r in range(700, 0, -8):                                                 # halo suave
        c = tuple(int(a + (b - a) * (1 - r / 700) * 0.55) for a, b in zip(vc.NAVY, vc.AZUL)); d.ellipse([540 - r, 170 - r, 540 + r, 170 + r], fill=c)
    # micrófono (todo el cartel queda por encima de 520: debajo van las barras y los subtítulos)
    d.rounded_rectangle([495, 40, 585, 190], radius=45, fill="white")
    for y in range(70, 175, 22): d.line([(512, y), (568, y)], fill=(200, 214, 240), width=5)
    d.arc([460, 100, 620, 250], start=0, end=180, fill="white", width=11)
    d.line([(540, 250), (540, 285)], fill="white", width=11); d.line([(495, 288), (585, 288)], fill="white", width=11)
    for k, rr in enumerate((120, 160, 200)):                                    # ondas
        d.arc([540 - rr, 135 - rr, 540 + rr, 135 + rr], start=-35, end=35, fill=vc.GREEN, width=9 - 2 * k)
        d.arc([540 - rr, 135 - rr, 540 + rr, 135 + rr], start=145, end=215, fill=vc.GREEN, width=9 - 2 * k)
    t1 = "IRRATIAN" if eu else "EN LA RADIO"
    f = vc.fuente("SemiBold", 36); x = 540 - (sum(d.textlength(ch, font=f) + 8 for ch in t1) - 8) / 2
    for ch in t1: d.text((x, 318), ch, font=f, fill=vc.GREEN); x += d.textlength(ch, font=f) + 8
    for txt, peso, tam, y in ((spec.get("emisora", ""), "Bold", 70, 368), (spec.get("programa", ""), "Regular", 48, 452)):
        f = vc.fuente(peso, tam)
        while d.textlength(txt, font=f) > 900 and tam > 34: tam -= 2; f = vc.fuente(peso, tam)
        d.text((540 - d.textlength(txt, font=f) / 2, y), txt, font=f, fill="white")
    im.save(ruta)

def barras_audio(a, sr, n_frames):
    """Altura (0-1) de BARRAS_N barras por fotograma: energía del audio en bandas logarítmicas de 90 a 5000 Hz, con subida rápida y caída lenta."""
    hop = sr // FPS; win = 2048; bandas = np.geomspace(90, 5000, BARRAS_N + 1); fr = np.fft.rfftfreq(win, 1 / sr)
    idx = [(np.searchsorted(fr, bandas[i]), max(np.searchsorted(fr, bandas[i + 1]), np.searchsorted(fr, bandas[i]) + 1)) for i in range(BARRAS_N)]
    out = np.zeros((n_frames, BARRAS_N)); h = np.hanning(win)
    for k in range(n_frames):
        c = k * hop + hop // 2; s = a[max(0, c - win // 2): c + win // 2]
        if len(s) < win: s = np.pad(s, (0, win - len(s)))
        m = np.abs(np.fft.rfft(s * h)); out[k] = [np.log10(1e-6 + m[i0:i1].mean()) for i0, i1 in idx]
    ref = np.percentile(out, 93, axis=0); lo = np.percentile(out, 15, axis=0)
    out = np.clip((out - lo) / np.maximum(ref - lo, 1e-3), 0, 1)
    sm = np.zeros_like(out); prev = np.zeros(BARRAS_N)
    for k in range(n_frames):
        prev = np.where(out[k] > prev, 0.55 * out[k] + 0.45 * prev, 0.82 * prev + 0.18 * out[k]); sm[k] = prev
    return sm

def plan_planos(clip, tiem, preguntan, base, dur):
    """Lista de planos [(ini, fin, tipo, quien, n)] en tiempo del clip. Mientras habla quien presenta: cartel. Mientras habla el abogado:
    planos de 5 a 9 s que cambian en el arranque de un rótulo (cue)."""
    cues = vc.rotulos(tiem, L["sub_car"]); arr = []
    for c in cues:
        n = c[0]["tramo"]; arr.append(base[n] + max(c[0]["ini"], clip["tramos"][n]["inicio"]) - clip["tramos"][n]["inicio"])
    out = []; cont = {}
    for n, tr in enumerate(clip["tramos"]):
        a, b = base[n], base[n] + tr["fin"] - tr["inicio"]
        if tr["quien"] in preguntan or tr["quien"] not in clip["_planos"]:
            if out and out[-1][2] == "cartel": out[-1] = (out[-1][0], b, "cartel", None, 0)
            else: out.append((a, b, "cartel", None, 0))
            continue
        q = tr["quien"]; ini = a
        cortes = [t for t in arr if a + 4.5 < t < b - 4.0]
        while True:
            cand = [t for t in cortes if ini + 5.0 <= t <= ini + 9.0]
            if b - ini <= 10.0 or not cand:
                if b - ini > 12.0:                                              # sin rótulo que encaje: se corta igual a 7 s
                    cand = [ini + 7.0]
                else:
                    k = cont.get(q, 0); out.append((ini, b, "foto", q, k)); cont[q] = k + 1; break
            t = min(cand, key=lambda x: abs(x - (ini + 7.0)))
            k = cont.get(q, 0); out.append((ini, t, "foto", q, k)); cont[q] = k + 1; ini = t
    out[-1] = (out[-1][0], dur, *out[-1][2:])
    return out

def recuadro(src, a, b, u):
    """Fotograma 1080 x 1080 tomado del cuadrado [x, y, lado] interpolado entre a y b (u de 0 a 1, con arranque y final suaves)."""
    import cv2
    u = u * u * (3 - 2 * u); x, y, s = [p + (q - p) * u for p, q in zip(a, b)]; k = T / s
    M = np.float32([[k, 0, -x * k], [0, k, -y * k]])
    return cv2.warpAffine(src, M, (T, T), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

def recuadro_video(spec, clip, planos, dur, alturas, ruta, tmp):
    import cv2
    cartel = os.path.join(tmp, "cartel.png"); cartel_img(spec, cartel)
    fotos = {}
    def foto(r):
        if r not in fotos: fotos[r] = cv2.cvtColor(np.array(Image.open(r).convert("RGB")), cv2.COLOR_RGB2BGR)
        return fotos[r]
    car = cv2.imread(cartel)
    nfr = int(round(dur * FPS))
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{T}x{T}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "ultrafast", "-crf", "12", "-pix_fmt", "yuv420p", ruta], stdin=subprocess.PIPE)
    def cuadro(p, t):
        a0, a1, tipo, q, n = p; u = (t - a0) / max(0.01, a1 - a0); u = min(max(u, 0), 1)
        if tipo == "cartel": return recuadro(car, [0, 0, T], [27, 20, T - 54], u)
        lista = clip["_planos"][q]; pl = lista[n % len(lista)]
        return recuadro(foto(pl["foto"]), pl["a"], pl["b"], u)
    xs = [540 - BARRAS_W // 2 + i * BARRAS_W / BARRAS_N for i in range(BARRAS_N)]; bw = BARRAS_W / BARRAS_N * 0.62
    for k in range(nfr):
        t = k / FPS
        i = max(j for j, p in enumerate(planos) if p[0] <= t + 1e-6)
        im = cuadro(planos[i], t)
        if i > 0 and t - planos[i][0] < 0.3:                                    # fundido corto desde el plano anterior
            w = (t - planos[i][0]) / 0.3; im = cv2.addWeighted(cuadro(planos[i - 1], t), 1 - w, im, w, 0)
        h = alturas[min(k, len(alturas) - 1)]
        y0, y1, x0, x1 = BARRAS_Y - 8, BARRAS_Y + BARRAS_H + 8, 540 - BARRAS_W // 2 - 14, 540 + BARRAS_W // 2 + 8   # fondo oscuro translúcido solo en la franja de las barras
        im[y0:y1, x0:x1] = (im[y0:y1, x0:x1] * 0.55 + np.array([66, 26, 0]) * 0.45).astype(np.uint8)
        cy = BARRAS_Y + BARRAS_H / 2
        for j in range(BARRAS_N):
            hh = 4 + (BARRAS_H - 4) * h[j]
            cv2.rectangle(im, (int(xs[j]), int(cy - hh / 2)), (int(xs[j] + bw), int(cy + hh / 2)), (135, 232, 0), -1, cv2.LINE_AA)
        cv2.rectangle(im, (0, 0), (int(T * t / dur), 7), (135, 232, 0), -1)          # barra de progreso
        ff.stdin.write(im.tobytes())
    ff.stdin.close(); ff.wait()
    if ff.returncode: raise SystemExit("fallo al codificar el recuadro")

def ass_resaltado(cues, entra, clip, preguntan, sal, dur):
    """Rótulos de dos líneas como mucho; dentro de cada rótulo, la palabra que suena va resaltada."""
    ev = []
    for k, c in enumerate(cues):
        n = c[0]["tramo"]; a = entra[k]; b = max(sal(c[-1]["fin"], n) + 0.25, a + 0.6)
        b = min(b, entra[k + 1]) if k + 1 < len(cues) and entra[k + 1] > a + 0.2 else min(b, dur)
        q = clip["tramos"][n]["quien"] in preguntan; est = "Q" if q else "S"; hi = BLANCO_ASS if q else VERDE_ASS
        palabras = [w["p"] for w in c]; lineas = textwrap.wrap(" ".join(palabras), L["sub_car"])
        cortes = []; acc = 0                                                     # índice de palabra donde empieza cada línea
        for ln in lineas: cortes.append(acc); acc += len(ln.split())
        def texto(j):
            out = []
            for i, p in enumerate(palabras):
                if i in cortes and i > 0: out.append("\\N")
                elif i > 0: out.append(" ")
                out.append(("{\\c" + hi + "}" + p + "{\\r}") if i == j else p)
            return "".join(out)
        marcas = [max(a, min(b, sal(w["ini"], n))) for w in c] + [b]
        pos = f"{{\\pos({L['sub_x']},{L['sub_y']})}}"
        if marcas[0] > a + 0.05: ev.append(f"Dialogue: 1,{vc.ts(a)},{vc.ts(marcas[0])},{est},,0,0,0,,{pos}{texto(-1)}")
        for j in range(len(c)):
            t0, t1 = marcas[j], max(marcas[j + 1], marcas[j])
            if t1 - t0 < 0.02: continue
            ev.append(f"Dialogue: 1,{vc.ts(t0)},{vc.ts(t1)},{est},,0,0,0,,{pos}{texto(j)}")
    return ev

def montar(spec, ruta_spec, carpeta, solo=()):
    import soundfile as sf
    tiem_all = json.load(open(ruta_spec.replace(".json", ".tiempos.json"), encoding="utf8")); os.makedirs(carpeta, exist_ok=True)
    a16, sr16 = sf.read(spec["audio"], dtype="float32")
    if a16.ndim > 1: a16 = a16.mean(axis=1)
    for clip in spec["clips"]:
        if solo and clip["id"] not in solo: continue
        clip["_planos"] = spec["planos"]
        rot, preguntan, principal, prefijo = vc.cabecera(spec, clip); tiem = tiem_all[clip["id"]]
        tmp = tempfile.mkdtemp(); fnd = os.path.join(tmp, "fondo.png")
        vc.fondo(clip, clip.get("credito", spec.get("credito", "")), fnd, L, clip.get("cta", spec.get("cta", vc.CTAS[spec.get("idioma", "es")])), rot.get(principal, ""), prefijo)
        base, ac = [], 0.0
        for tr in clip["tramos"]: base.append(ac); ac += tr["fin"] - tr["inicio"]
        dur = ac
        def sal(t, n): return base[n] + min(max(t, clip["tramos"][n]["inicio"]), clip["tramos"][n]["fin"]) - clip["tramos"][n]["inicio"]
        # barras: del audio de 16 kHz de los mismos tramos
        trozo = np.concatenate([a16[int(tr["inicio"] * sr16):int(tr["fin"] * sr16)] for tr in clip["tramos"]])
        nfr = int(round(dur * FPS)); alturas = barras_audio(trozo, sr16, nfr)
        planos = plan_planos(clip, tiem, preguntan, base, dur)
        rv = os.path.join(tmp, "recuadro.mp4"); recuadro_video(spec, clip, planos, dur, alturas, rv, tmp)
        cues = vc.rotulos(tiem, L["sub_car"]); entra = []
        for k, c in enumerate(cues):
            a = sal(c[0]["ini"], c[0]["tramo"])
            if entra: a = max(a, min(entra[-1] + 0.7, dur - 0.5))
            entra.append(a)
        ev = ass_resaltado(cues, entra, clip, preguntan, sal, dur)
        ass = os.path.join(tmp, "subs.ass")
        open(ass, "w", encoding="utf8").write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: {vc.W}
PlayResY: {vc.H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: S,Poppins,{L["sub_tam"]},&H00FFFFFF,&H00FFFFFF,&H00421A00,&H00000000,-1,0,0,0,100,100,0,0,1,4,0,5,40,40,40,1
Style: Q,Poppins,{L["sub_tam"]},&H0087E800,&H0087E800,&H00421A00,&H00000000,-1,0,0,0,100,100,0,0,1,4,0,5,40,40,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n")
        fc = []; ent = []; NT = len(clip["tramos"])
        ent += ["-i", rv]
        for i, tr in enumerate(clip["tramos"]):
            ent += ["-ss", f"{tr['inicio']:.3f}", "-t", f"{tr['fin'] - tr['inicio'] + 0.2:.3f}", "-i", spec["fuente"]]
            fc.append(f"[{2 + i}:a]aformat=channel_layouts=mono,asetpts=PTS-STARTPTS,atrim=duration={tr['fin'] - tr['inicio']:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st={tr['fin'] - tr['inicio'] - 0.05:.3f}:d=0.05[a{i}]")
        IM, IC = 2 + NT, 3 + NT
        fc.append("".join(f"[a{i}]" for i in range(NT)) + f"concat=n={NT}:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100[a]")
        fc.append(f"[0:v][1:v]overlay=0:{L['ty']}:shortest=1[c0];[c0][{IM}:v]overlay=0:0[c];[c]ass={ass}:fontsdir={vc.FDIR}[o0]")
        cie = os.path.join(tmp, "cierre.png"); vc.cierre(cie, clip.get("cierre_lineas", spec.get("cierre_lineas", vc.CIERRE_LINEAS[spec.get("idioma", "es")])))
        extra = ["-loop", "1", "-framerate", "25", "-t", f"{vc.CIERRE_S + 1:.1f}", "-i", cie]; total = dur + vc.CIERRE_S
        fc.append(f"[o0]trim=duration={dur:.3f},setpts=PTS-STARTPTS,format=yuv420p,setsar=1[m]")
        fc.append(f"[{IC}:v]fps=25,trim=duration={vc.CIERRE_S},setpts=PTS-STARTPTS,fade=t=in:st=0:d=0.3:color=0x003378,format=yuv420p,setsar=1[e]")
        fc.append("[m][e]concat=n=2:v=1:a=0[o]"); fc.append(f"[a]apad=pad_dur={vc.CIERRE_S}[af]")
        salida = os.path.join(carpeta, clip["id"] + ".mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "25", "-i", fnd] + ent + [
                        "-loop", "1", "-framerate", "25", "-i", fnd.replace("fondo", "mascara")] + extra + [
                        "-filter_complex", ";".join(fc), "-map", "[o]", "-map", "[af]", "-t", f"{total:.3f}", "-r", "25",
                        "-c:v", "libx264", "-preset", spec.get("preset", "faster"), "-crf", str(clip.get("crf", spec.get("crf", 24))), "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", salida], check=True)
        json.dump({"subtitulos": [{"ini": round(entra[k], 2), "texto": " ".join(w["p"] for w in c)} for k, c in enumerate(cues)],
                   "planos": [[round(p[0], 2), round(p[1], 2), p[2], p[3], p[4]] for p in planos]},
                  open(os.path.join(carpeta, clip["id"] + ".subtitulos.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        subprocess.run(["rm", "-rf", tmp])
        print("ok", salida, f"{total:.1f} s", flush=True)

if __name__ == "__main__":
    spec = json.load(open(sys.argv[2], encoding="utf-8"))
    if sys.argv[1] == "tiempos": vc.tiempos(spec, sys.argv[2])
    else: montar(spec, sys.argv[2], sys.argv[3], sys.argv[4].split(",") if len(sys.argv) > 4 else ())
