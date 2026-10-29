#!/usr/bin/env python3
"""Monta clips verticales 1080 x 1920 a partir de una intervención en televisión: recorta el fragmento,
encuadra a quien habla a todo el ancho, pone el marco de Erreklamatu y graba los subtítulos sincronizados
sobre la parte baja del vídeo.

Uso:
  python3 video_clips.py tiempos specs.json          -> calcula cuándo se dice cada palabra (specs.tiempos.json)
  python3 video_clips.py montar  specs.json carpeta [id,id]  -> genera <id>.mp4 por cada clip (o solo los indicados)

specs.json:
  {"video": ruta, "audio": ruta a un wav mono de 16 kHz del mismo vídeo, "credito": "Imágenes: EITB · programa SIML",
   "modelo": carpeta del modelo sherpa-onnx whisper, "vad": ruta a silero_vad.onnx,
   "clips": [{"id": "PUB-0007", "kicker": "...", "titular": ["línea 1", "línea 2"],
              "tramos": [{"inicio": s, "fin": s, "quien": "pregunta" | "presentador" | "oscar", "texto": "lo que se dice, ya corregido",
                          "rotulo_desde": s (opcional: el nombre no sale hasta ese segundo, si antes no está en pantalla)}],
              "recortes": [[segundo_del_original, x], ...]}]}

- "tramos" son trozos del vídeo original, en orden; si no son contiguos, el clip salta de uno a otro.
- "texto" es la transcripción corregida de cada tramo. El programa NO decide el texto: solo calcula cuándo
  aparece cada palabra. Una persona debe revisar los subtítulos oyendo el audio antes de publicar.
- "recortes" dice qué cuadrado del original se muestra desde cada momento: [segundo, x] usa el tamaño y la altura
  por defecto ("crop" y "cy" de la especificación; 174 y 44 si no se dicen); [segundo, x, y, lado] fija los tres.
- Un tramo puede traer su propio "video" y "audio" (rutas): sirve para montar un clip con trozos de varios archivos, por ejemplo
  varias grabaciones de pantalla del mismo programa. En ese caso los recortes de cada archivo no deben coincidir en el segundo de inicio.
- Cada clip puede llevar sus propios "rotulos", "preguntan", "principal" (de quién es el nombre de la cabecera) y "prefijo" (texto delante del nombre;
  "" para quitar «Responde»). Las claves "enc" de los tramos y "marco" las usa video_marco.py para encuadrar y aquí se ignoran.
- "crf" (19 por defecto; más alto = archivo más pequeño) y "preset" de x264, en la especificación o en el clip.
- Opcionales en la especificación: "rotulos" ({"jon": "texto del rótulo"}, se suman a los de serie), "idioma"
  ("es" o "eu": idioma del reconocimiento y del texto del teléfono), "preguntan" (lista de "quien" cuyos
  subtítulos salen en verde; por defecto pregunta, presentador, presentadora y reportera).

Requiere ffmpeg con libass, Pillow, sherpa-onnx, soundfile, numpy y la fuente Poppins. logo.png, junto a este archivo.
"""
import difflib, json, os, re, subprocess, sys, tempfile, textwrap, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
FDIR = "/usr/share/fonts/truetype/google-fonts"
NAVY, AZUL, GREEN = (0, 51, 120), (10, 68, 150), (0, 232, 135)
W, H = 1080, 1920
TILE, TX = 1080, 0                      # el vídeo ocupa todo el ancho
CROP, CY = 174, 44                      # cuadrado que se toma del original (512 x 288)
# Diseños. "seguro" (por defecto desde el 04/10/2026) coloca titular, cara, subtítulos y teléfono en la franja que
# las aplicaciones no tapan: de 290 a 1250 px en vertical y de 65 a 940 px en horizontal (ver PROCEDIMIENTO).
# "clasico" es el anterior: se conserva para rehacer piezas ya publicadas con el mismo aspecto.
DISENOS = {
    "clasico": dict(ty=430, kicker_y=165, tit_y=215, tit_paso=88, tit_tam=70, tit_ancho=W - 140, sub_y=430 + 1080 - 185, sub_x=540, sub_tam=72,
                    sub_car=21, tag_x=44, tag_dy=58, credito="bajo", cta_y=1610, cta_x=540, grad_ini=430 + 1080 - 420, grad_lleno=430 + 1080, grad_max=225),
    "seguro":  dict(ty=480, kicker_y=246, tit_y=296, tit_paso=84, tit_tam=68, tit_ancho=870, sub_y=1166, sub_x=502, sub_tam=66,
                    sub_car=20, tag_x=70, tag_dy=58, credito="sobre", cta_y=1366, cta_x=502, grad_ini=480 + 450, grad_lleno=480 + 680, grad_max=205),
    # Esquema por zonas (5 de octubre de 2026). De arriba abajo: titular (290-470), cara (480-1060, sin nada encima), subtítulos (1085-1250)
    # y zona sacrificable (desde 1250: crédito, teléfono y pie). El nombre de quien habla va en la cabecera, no sobre la imagen.
    # El vídeo se funde a azul bajo la cara: así los subtítulos no pisan la imagen y los rótulos de la emisión quedan ocultos.
    "zonas":   dict(ty=480, kicker_y=280, tit_y=313, tit_paso=73, tit_tam=62, tit_ancho=870, sub_y=1166, sub_x=502, sub_tam=66,
                    sub_car=20, tag_x=70, tag_dy=58, rotulo="cabecera", credito="franja", cred_y=1296, cta_y=1372, cta_x=502,
                    grad_ini=1030, grad_lleno=1200, grad_max=255),
}
CTA = "Consulta gratuita  ·  944 027 596"
CTAS = {"es": CTA, "eu": "Kontsulta doan  ·  944 027 596"}
PREGUNTAN = ["pregunta", "presentador", "presentadora", "reportera"]
RESPONDE = {"es": "Responde ", "eu": "Erantzuna: "}
ROTULOS = {"oscar": r"{\b1}Óscar Sánchez{\b0}  ·  Abogado de Erreklamatu", "pregunta": "Pregunta del programa", "presentador": "Presentador del programa",
           "presentadora": "Presentadora del programa", "reportera": "Reportera del programa"}

def fuente(peso, tam):
    from PIL import ImageFont
    for nombre in (f"Poppins-{peso}.ttf", "Poppins-Bold.ttf"):
        ruta = os.path.join(FDIR, nombre)
        if os.path.exists(ruta): return ImageFont.truetype(ruta, tam)
    raise SystemExit("Falta la fuente Poppins en " + FDIR)

def norm(p):
    p = unicodedata.normalize("NFD", p.lower())
    return re.sub(r"[^a-z0-9ñ]", "", "".join(c for c in p if unicodedata.category(c) != "Mn" or c == "̃"))

# ---------------------------------------------------------------- tiempos de cada palabra
def trocear(a, sr, vad_ruta, t0, t1):
    """Divide el tramo en trozos de voz de 3 s como mucho. Devuelve [(inicio, fin)] en segundos del original."""
    import numpy as np, sherpa_onnx
    cfg = sherpa_onnx.VadModelConfig()
    cfg.silero_vad.model = vad_ruta; cfg.silero_vad.min_silence_duration = 0.1
    cfg.silero_vad.min_speech_duration = 0.15; cfg.silero_vad.threshold = 0.5; cfg.sample_rate = sr
    vad = sherpa_onnx.VoiceActivityDetector(cfg, buffer_size_in_seconds=120)
    x = a[int(t0 * sr):int(t1 * sr)]; ws = cfg.silero_vad.window_size; segs = []; i = 0
    def vaciar():
        while not vad.empty():
            s = vad.front; segs.append((s.start, s.start + len(s.samples))); vad.pop()
    while i + ws <= len(x):
        vad.accept_waveform(x[i:i + ws]); i += ws; vaciar()
    vad.flush(); vaciar()
    if sum(e - s for s, e in segs) < 0.7 * len(x): segs = [(0, len(x))]     # audio con ruido de fondo: el detector de voz se queda corto; se trocea todo el tramo
    fr = sr // 50
    def partir(s, e):
        if e - s <= 3.0 * sr: return [(s, e)]
        lo, hi = s + int(0.3 * (e - s)), s + int(0.7 * (e - s))
        if e - s > 6.0 * sr: lo, hi = s + int(1.5 * sr), s + int(3.0 * sr)
        en = np.array([np.abs(x[k:k + fr]).mean() for k in range(lo, hi, fr)])
        en = np.convolve(en, np.ones(3) / 3, mode="same")
        c = lo + int(np.argmin(en)) * fr + fr // 2
        return partir(s, c) + partir(c, e)
    out = []
    for s, e in segs: out += partir(s, e)
    return [(t0 + s / sr, t0 + e / sr) for s, e in out]

def tiempos(spec, ruta_spec):
    import soundfile as sf, sherpa_onnx
    audios = {}
    def cargar(ruta):                                    # cada tramo puede venir de un archivo distinto ("audio" en el tramo)
        if ruta not in audios:
            x, r = sf.read(ruta, dtype="float32"); audios[ruta] = (x.mean(axis=1) if x.ndim > 1 else x, r)
        return audios[ruta]
    d = spec["modelo"].rstrip("/") + "/"; pref = [f[:-len("-tokens.txt")] for f in os.listdir(d) if f.endswith("-tokens.txt")][0]
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=d + pref + "-encoder.int8.onnx", decoder=d + pref + "-decoder.int8.onnx",
                                                     tokens=d + pref + "-tokens.txt", language=spec.get("idioma", "es"), task="transcribe", num_threads=2)
    salida = {}
    # Lo que la máquina oye en cada tramo se guarda junto a la especificación: rehacer los tiempos tras corregir un texto no vuelve a reconocer el audio.
    RUTA_OIDAS = os.path.join(os.path.dirname(os.path.abspath(ruta_spec)), "oidas.cache.json"); OIDAS = json.load(open(RUTA_OIDAS, encoding="utf8")) if os.path.exists(RUTA_OIDAS) else {}
    for clip in spec["clips"]:
        palabras = []
        for n, tr in enumerate(clip["tramos"]):
            a, sr = cargar(tr.get("audio", spec["audio"]))
            oidas = []                                   # (palabra normalizada, tiempo central)
            clave = f'{tr.get("audio", spec["audio"])}|{spec.get("idioma", "es")}|{tr["inicio"]:.2f}|{tr["fin"]:.2f}'
            if clave in OIDAS: oidas = [tuple(o) for o in OIDAS[clave]]      # mismo tramo ya reconocido (versiones largas y cortas comparten tramos)
            else:
                for s, e in trocear(a, sr, spec["vad"], tr["inicio"], tr["fin"]):
                    st = rec.create_stream(); st.accept_waveform(sr, a[int(s * sr):int(e * sr)]); rec.decode_stream(st)
                    ws = [w for w in st.result.text.split() if norm(w)]
                    tot = sum(len(w) for w in ws) or 1; ac = 0
                    for w in ws:
                        oidas.append((norm(w), s + (e - s) * ac / tot, s + (e - s) * (ac + len(w)) / tot)); ac += len(w)
                OIDAS[clave] = oidas; json.dump(OIDAS, open(RUTA_OIDAS, "w", encoding="utf8"), ensure_ascii=False)
            ref = tr["texto"].split(); refn = [norm(w) for w in ref]
            sm = difflib.SequenceMatcher(None, refn, [o[0] for o in oidas], autojunk=False)
            ini = [None] * len(ref); fin = [None] * len(ref)
            for blq in sm.get_matching_blocks():
                for k in range(blq.size):
                    ini[blq.a + k], fin[blq.a + k] = oidas[blq.b + k][1], oidas[blq.b + k][2]
            # palabras sin emparejar: se reparten entre las vecinas según su longitud
            anclas = [(-1, tr["inicio"], tr["inicio"])] + [(i, ini[i], fin[i]) for i in range(len(ref)) if ini[i] is not None] + [(len(ref), tr["fin"], tr["fin"])]
            for (i0, _, f0), (i1, s1, _) in zip(anclas, anclas[1:]):
                hueco = list(range(i0 + 1, i1))
                if not hueco: continue
                tot = sum(len(ref[i]) for i in hueco); ac = 0
                for i in hueco:
                    ini[i] = f0 + (s1 - f0) * ac / tot; ac += len(ref[i]); fin[i] = f0 + (s1 - f0) * ac / tot
            emp = sum(b.size for b in sm.get_matching_blocks())
            print(f'{clip["id"]} tramo {n + 1}: {emp} de {len(ref)} palabras localizadas en el audio', flush=True)
            # los tiempos no pueden retroceder
            t = tr["inicio"]
            for i in range(len(ref)):
                ini[i] = max(ini[i], t); fin[i] = max(fin[i], ini[i] + 0.05); t = ini[i]
                palabras.append({"p": ref[i], "ini": round(ini[i], 2), "fin": round(min(fin[i], tr["fin"]), 2), "tramo": n})
        salida[clip["id"]] = palabras
    json.dump(salida, open(ruta_spec.replace(".json", ".tiempos.json"), "w", encoding="utf8"), ensure_ascii=False, indent=0)

# ---------------------------------------------------------------- montaje
def ts(t):
    t = max(t, 0); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"

def rotulos(palabras, max_car=21):
    """Agrupa las palabras en rótulos de dos líneas como mucho. Corta en los signos de puntuación; una frase que
    no cabe se reparte en trozos de longitud parecida."""
    def lineas(ws): return len(textwrap.wrap(" ".join(w["p"] for w in ws), max_car))
    def largo(ws): return len(" ".join(w["p"] for w in ws))
    # 1) frases: se corta tras . ? ! : … y al cambiar de tramo
    frases, act = [], []
    for w in palabras:
        if act and w["tramo"] != act[-1]["tramo"]: frases.append(act); act = []
        act.append(w)
        if re.search(r"[.?!:…]$", w["p"]): frases.append(act); act = []
    if act: frases.append(act)
    # 2) cada frase, en trozos que quepan, prefiriendo cortar tras una coma
    def partir(ws):
        if lineas(ws) <= 2: return [ws]
        n = -(-lineas(ws) // 2); objetivo = largo(ws) / n
        mejor, coste = None, 1e9
        for k in range(1, len(ws)):
            c = abs(largo(ws[:k]) - objetivo) - (8 if re.search(r"[,;]$", ws[k - 1]["p"]) else 0)
            if ws[k]["p"].lower() in ("que", "y", "o", "pero", "porque", "para", "en", "de", "con", "aunque", "e"): c -= 3
            if lineas(ws[:k]) <= 2 and c < coste: mejor, coste = k, c
        return [ws[:mejor]] + partir(ws[mejor:])
    cues = []
    for f in frases:
        for trozo in partir(f):
            # una frase muy corta se une a la anterior si es del mismo tramo y cabe
            if cues and cues[-1][0]["tramo"] == trozo[0]["tramo"] and largo(trozo) < 12 and lineas(cues[-1] + trozo) <= 2 and trozo is f:
                cues[-1] = cues[-1] + trozo
            else: cues.append(trozo)
    return cues

def fondo(clip, credito, ruta, L, CTA=CTA, nombre="", prefijo=""):
    from PIL import Image, ImageDraw
    TY = L["ty"]
    bg = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(bg)
    d.ellipse([W - 430, 120, W + 470, 1020], fill=AZUL)                     # disco de marca, detrás del vídeo
    x = 70
    if L.get("rotulo") == "cabecera" and nombre:                              # quién habla, en la cabecera: nada tapa la cara
        m = re.match(r"\{\\b1\}(.*?)\{\\b0\}(.*)", nombre); negr, resto = (m.group(1), re.sub(r"\s+", " ", m.group(2))) if m else (nombre, "")
        t = 29
        while t > 22 and d.textlength(prefijo + resto, font=fuente("Regular", t)) + d.textlength(negr, font=fuente("Bold", t)) > L["tit_ancho"]: t -= 1
        d.text((x, L["kicker_y"]), prefijo, font=fuente("Regular", t), fill=(200, 214, 240)); x += d.textlength(prefijo, font=fuente("Regular", t))
        d.text((x, L["kicker_y"]), negr, font=fuente("Bold", t), fill=GREEN); x += d.textlength(negr, font=fuente("Bold", t))
        d.text((x, L["kicker_y"]), resto, font=fuente("Regular", t), fill=(200, 214, 240))
    else:
        for ch in clip["kicker"].upper():
            f = fuente("SemiBold", 30); d.text((x, L["kicker_y"]), ch, font=f, fill=GREEN); x += d.textlength(ch, font=f) + 5
    tam = L["tit_tam"]                                                       # el titular se encoge hasta caber en su ancho
    while tam > 50 and max(d.textlength(l, font=fuente("Bold", tam)) for l in clip["titular"][:2]) > L["tit_ancho"]: tam -= 2
    for n, linea in enumerate(clip["titular"][:2]):
        f = fuente("Bold", tam)
        if d.textlength(linea, font=f) > L["tit_ancho"]: raise SystemExit(f'{clip["id"]}: la línea del titular no cabe: {linea}')
        d.text((70, L["tit_y"] + L["tit_paso"] * n), linea, font=f, fill="white")
    if credito and L["credito"] == "bajo":
        f = fuente("Regular", 22); d.text((W - 40 - d.textlength(credito, font=f), TY + TILE + 18), credito, font=f, fill=(150, 170, 205))
    if L["cta_y"] >= TY + TILE:                                               # teléfono bajo el vídeo (diseño clásico)
        f = fuente("SemiBold", 44); d.text((L["cta_x"] - d.textlength(CTA, font=f) / 2, L["cta_y"]), CTA, font=f, fill="white")
    d.rectangle([0, 1740, W, H], fill="white")
    alta = os.path.join(AQUI, "logo-alta.png")                                # logo original en alta resolución (Sergio, 05/10/2026), ya recortado
    if os.path.exists(alta):
        logo = Image.open(alta).convert("RGBA"); logo = logo.resize((428, round(428 * logo.height / logo.width)), Image.LANCZOS)
        bg.paste(logo, (76, 1740 + (180 - logo.height) // 2), logo)
    else:
        logo = Image.open(os.path.join(AQUI, "logo.png")).convert("RGB")
        logo = logo.resize((int(logo.width * 1.25), int(logo.height * 1.25)), Image.LANCZOS); bg.paste(logo, (70, 1740 + (180 - logo.height) // 2))
    f = fuente("Regular", 34); d.text((W - 70 - d.textlength("erreklamatu.com", font=f), 1806), "erreklamatu.com", font=f, fill=(84, 100, 140))
    bg.save(ruta)
    # degradado oscuro sobre el vídeo, para que los subtítulos (y el teléfono, en el diseño seguro) se lean
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    for y in range(L["grad_ini"], TY + TILE):
        k = min(1.0, (y - L["grad_ini"]) / max(1, L["grad_lleno"] - L["grad_ini"]))
        col = (0, 26, 66)
        if L["grad_max"] == 255 and y > L["grad_lleno"]:                      # fundido completo: el azul oscuro enlaza con el azul del fondo
            j = (y - L["grad_lleno"]) / max(1, TY + TILE - L["grad_lleno"]); col = tuple(int(c0 + (c1 - c0) * j) for c0, c1 in zip((0, 26, 66), NAVY))
        gd.line([(0, y), (W, y)], fill=col + (int(L["grad_max"] * k ** 1.3),))
    if L["cta_y"] < TY + TILE:                                                # teléfono sobre el vídeo, dentro de la franja visible
        f = fuente("SemiBold", 44); gd.text((L["cta_x"] - gd.textlength(CTA, font=f) / 2, L["cta_y"]), CTA, font=f, fill="white", stroke_width=2, stroke_fill=(0, 26, 66))
    if credito and L["credito"] == "franja":                                  # crédito de las imágenes, bajo los subtítulos
        f = fuente("Regular", 24); gd.text((L["cta_x"] - gd.textlength(credito, font=f) / 2, L["cred_y"]), credito, font=f, fill=(150, 170, 205))
    if credito and L["credito"] == "sobre":                                   # crédito de las imágenes, bajo el rótulo del nombre
        f = fuente("Regular", 22); gd.text((L["tag_x"], TY + L["tag_dy"] + 44), credito, font=f, fill=(235, 240, 250), stroke_width=2, stroke_fill=(0, 26, 66))
    g.save(ruta.replace("fondo", "mascara"))

CIERRE_S = 2.6                                                               # segundos de la cortinilla de cierre
CIERRE_LINEAS = {"es": ["Consulta gratuita", "Solo cobramos si ganamos"], "eu": ["Kontsulta doan", "Irabazten badugu bakarrik kobratzen dugu"]}
TELEFONO, WEB = "944 027 596", "erreklamatu.com"

def cierre(ruta, lineas):
    """Cortinilla de cierre: logo, las dos promesas, teléfono y web. Centrada en la pantalla (x = 540) y dentro de lo que ninguna aplicación tapa:
    de 290 a 1250 px en vertical; por debajo de 790 px, donde empiezan los botones de TikTok y YouTube, nada pasa de x = 885."""
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(im); cx = W // 2
    d.ellipse([W - 430, 120, W + 470, 1020], fill=AZUL)
    d.rounded_rectangle([cx - 380, 372, cx + 380, 584], radius=30, fill="white")       # el logo va sobre blanco, como en el pie
    logo = Image.open(os.path.join(AQUI, "logo-alta.png")).convert("RGBA"); logo = logo.resize((640, round(640 * logo.height / logo.width)), Image.LANCZOS)
    im.paste(logo, (cx - 320, 478 - logo.height // 2), logo)
    y = 676; LIM = 690; t = 48                                                           # ancho máximo: nada pasa de x = 885
    while t > 42 and max(d.textlength(l, font=fuente("SemiBold", t)) for l in lineas) + 70 > LIM: t -= 1
    if max(d.textlength(l, font=fuente("SemiBold", t)) for l in lineas) + 70 > LIM: t = 46   # si ni así cabe en un renglón, se parte a tamaño normal
    f = fuente("SemiBold", t)
    for l in lineas:                                                                     # cada promesa centrada, con su marca; si no cabe, en dos renglones
        filas = [l]
        if d.textlength(l, font=f) + 70 > LIM:
            p = l.split(" "); k = min(range(1, len(p)), key=lambda k: abs(d.textlength(" ".join(p[:k]), font=f) - d.textlength(" ".join(p[k:]), font=f)))
            filas = [" ".join(p[:k]), " ".join(p[k:])]
        for n, fila in enumerate(filas):
            ancho = d.textlength(fila, font=f) + (70 if n == 0 else 0); x0 = cx - ancho / 2
            if n == 0:
                r = 24; c = (x0 + r, y + round(0.72 * t))
                d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=GREEN)
                d.line([(c[0] - 11, c[1] + 1), (c[0] - 3, c[1] + 9), (c[0] + 12, c[1] - 8)], fill=NAVY, width=6, joint="curve")
            d.text((x0 + (70 if n == 0 else 0), y), fila, font=f, fill="white"); y += 60 if n + 1 < len(filas) else 86
    y += 6
    f = fuente("Bold", 112); d.text((cx - d.textlength(TELEFONO, font=f) / 2, y), TELEFONO, font=f, fill="white")
    f = fuente("SemiBold", 54); d.text((cx - d.textlength(WEB, font=f) / 2, y + 186), WEB, font=f, fill=GREEN)
    im.save(ruta)

def cabecera(spec, clip):
    """Quién sale en la cabecera. Cada clip puede traer sus propios "rotulos", "preguntan", "principal" y "prefijo"; si no, valen los de la especificación.
    Por defecto el nombre es el de la primera persona que no pregunta, y lleva «Responde» delante si en el clip hay una pregunta."""
    rot = dict(ROTULOS, **spec.get("rotulos", {})); rot.update(clip.get("rotulos", {})); preguntan = clip.get("preguntan", spec.get("preguntan", PREGUNTAN))
    principal = clip.get("principal") or next((t["quien"] for t in clip["tramos"] if t["quien"] not in preguntan), clip["tramos"][0]["quien"])
    prefijo = clip.get("prefijo", spec.get("prefijo", RESPONDE[spec.get("idioma", "es")] if any(t["quien"] in preguntan for t in clip["tramos"]) else ""))
    return rot, preguntan, principal, prefijo

def montar(spec, ruta_spec, carpeta, solo=()):
    tiem = json.load(open(ruta_spec.replace(".json", ".tiempos.json"), encoding="utf8"))
    os.makedirs(carpeta, exist_ok=True)
    for clip in spec["clips"]:
        if solo and clip["id"] not in solo: continue
        L = DISENOS[clip.get("diseno", spec.get("diseno", "zonas"))]; TY, SUB_Y, TAG_Y = L["ty"], L["sub_y"], L["ty"] + L["tag_dy"]
        rot, preguntan, principal, prefijo = cabecera(spec, clip); crop0, cy0 = spec.get("crop", CROP), spec.get("cy", CY)
        tmp = tempfile.mkdtemp(); fnd = os.path.join(tmp, "fondo.png")
        fondo(clip, clip.get("credito", spec.get("credito", "")), fnd, L, clip.get("cta", spec.get("cta", CTAS[spec.get("idioma", "es")])), rot.get(principal, ""), prefijo)
        # tiempo del original -> tiempo del clip
        base, ac = [], 0.0
        for tr in clip["tramos"]: base.append(ac); ac += tr["fin"] - tr["inicio"]
        dur = ac
        def sal(t, n): return base[n] + min(max(t, clip["tramos"][n]["inicio"]), clip["tramos"][n]["fin"]) - clip["tramos"][n]["inicio"]
        # piezas de vídeo: cada tramo, partido donde cambia el recorte
        orden = lambda lista: sorted([r[0], r[1], r[2] if len(r) > 2 else cy0, r[3] if len(r) > 3 else crop0] for r in lista)
        rec0 = orden(clip.get("recortes", [])); piezas = []
        for tr in clip["tramos"]:
            rec = orden(tr["recortes"]) if "recortes" in tr else rec0                              # un tramo de otro archivo trae sus propios recortes
            cortes = [tr["inicio"]] + [r[0] for r in rec if tr["inicio"] < r[0] < tr["fin"]] + [tr["fin"]]
            for a, b in zip(cortes, cortes[1:]):
                r = [r for r in rec if r[0] <= a + 1e-6][-1] if any(r[0] <= a + 1e-6 for r in rec) else rec[0]
                piezas.append((a, b, r[1], r[2], r[3], tr.get("video", spec["video"])))
        # Cada trozo de vídeo y cada tramo de audio entra como una entrada propia, ya situada en su segundo (-ss antes de -i).
        # Así no se descodifica el original desde el principio ni se guardan en memoria los planos que esperan turno
        # (con un original de 1920 x 1080 y nueve planos, el montaje anterior agotaba la memoria).
        fc = []; ent = []; NP, NT = len(piezas), len(clip["tramos"])
        for i, (a, b, x, y, lado, vid) in enumerate(piezas):
            ent += ["-ss", f"{a:.3f}", "-t", f"{b - a + 0.2:.3f}", "-i", vid]
            fc.append(f"[{1 + i}:v]fps=25,setpts=PTS-STARTPTS,trim=duration={b - a:.3f},setpts=PTS-STARTPTS,crop={lado}:{lado}:{x}:{y},scale={TILE}:{TILE}:flags=lanczos,unsharp=5:5:0.6:5:5:0.0,setsar=1[v{i}]")
        fc.append("".join(f"[v{i}]" for i in range(len(piezas))) + f"concat=n={len(piezas)}:v=1:a=0[vc]")
        for i, tr in enumerate(clip["tramos"]):
            ent += ["-ss", f"{tr['inicio']:.3f}", "-t", f"{tr['fin'] - tr['inicio'] + 0.2:.3f}", "-i", tr.get("video", spec["video"])]
            fc.append(f"[{1 + NP + i}:a]asetpts=PTS-STARTPTS,atrim=duration={tr['fin'] - tr['inicio']:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st={tr['fin'] - tr['inicio'] - 0.05:.3f}:d=0.05[a{i}]")
        IM, IC = 1 + NP + NT, 2 + NP + NT                                                         # entradas de la máscara y de la cortinilla
        fc.append("".join(f"[a{i}]" for i in range(len(clip["tramos"]))) + f"concat=n={len(clip['tramos'])}:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100[a]")
        # subtítulos y rótulo de quién habla
        ev = []
        cues = rotulos(tiem[clip["id"]], L["sub_car"])
        # Cuándo entra cada rótulo. Ninguno entra menos de 0,7 s después del anterior: si el reconocimiento no localizó las palabras
        # (pasa con ruido de calle y en euskera), varios rótulos caían en el mismo instante y se pisaban o duraban un parpadeo.
        entra = []
        for k, c in enumerate(cues):
            a = sal(c[0]["ini"], c[0]["tramo"])
            if entra: a = max(a, min(entra[-1] + 0.7, dur - 0.5))
            entra.append(a)
        for k, c in enumerate(cues):
            n = c[0]["tramo"]; a = entra[k]; b = max(sal(c[-1]["fin"], n) + 0.25, a + 0.6)
            b = min(b, entra[k + 1]) if k + 1 < len(cues) and entra[k + 1] > a + 0.2 else min(b, dur)   # un rótulo nunca pisa al siguiente
            est = "Q" if clip["tramos"][n]["quien"] in preguntan else "S"
            ev.append(f"Dialogue: 1,{ts(a)},{ts(b)},{est},,0,0,0,,{{\\pos({L['sub_x']},{SUB_Y})}}" + "\\N".join(textwrap.wrap(" ".join(w['p'] for w in c), L["sub_car"])))
        for n, tr in enumerate(clip["tramos"]):
            if L.get("rotulo") == "cabecera": break                                               # el nombre ya está en la cabecera
            desde = base[n] + max(0.0, tr.get("rotulo_desde", tr["inicio"]) - tr["inicio"])     # el rótulo solo sale cuando esa persona está en pantalla
            if desde >= base[n] + tr["fin"] - tr["inicio"] - 0.2: continue                        # quien habla no llega a salir en este tramo: sin rótulo
            ev.append(f"Dialogue: 0,{ts(desde)},{ts(base[n] + tr['fin'] - tr['inicio'])},T,,0,0,0,,{{\\pos({L['tag_x']},{TAG_Y})}}" + rot[tr["quien"]])
        ass = os.path.join(tmp, "subs.ass")
        open(ass, "w", encoding="utf8").write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: S,Poppins,{L["sub_tam"]},&H00FFFFFF,&H00FFFFFF,&H00421A00,&H00000000,-1,0,0,0,100,100,0,0,1,3,0,5,40,40,40,1
Style: Q,Poppins,{L["sub_tam"]},&H0087E800,&H0087E800,&H00421A00,&H00000000,-1,0,0,0,100,100,0,0,1,3,0,5,40,40,40,1
Style: T,Poppins,34,&H00FFFFFF,&H00FFFFFF,&H00783300,&H00783300,0,0,0,0,100,100,0,0,3,14,0,4,40,40,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n")
        fc.append(f"[0:v][vc]overlay={TX}:{TY}:shortest=1[c0];[c0][{IM}:v]overlay=0:0[c];[c]ass={ass}:fontsdir={FDIR}[o0]")
        con_cierre = clip.get("cierre", spec.get("cierre", True)); extra = []; total = dur
        if con_cierre:                                                                            # cortinilla de cierre, con fundido desde el azul
            cie = os.path.join(tmp, "cierre.png"); cierre(cie, clip.get("cierre_lineas", spec.get("cierre_lineas", CIERRE_LINEAS[spec.get("idioma", "es")])))
            extra = ["-loop", "1", "-framerate", "25", "-t", f"{CIERRE_S + 1:.1f}", "-i", cie]; total = dur + CIERRE_S
            fc.append(f"[o0]trim=duration={dur:.3f},setpts=PTS-STARTPTS,format=yuv420p,setsar=1[m]")
            fc.append(f"[{IC}:v]fps=25,trim=duration={CIERRE_S},setpts=PTS-STARTPTS,fade=t=in:st=0:d=0.3:color=0x003378,format=yuv420p,setsar=1[e]")
            fc.append("[m][e]concat=n=2:v=1:a=0[o]"); fc.append(f"[a]apad=pad_dur={CIERRE_S}[af]")
        else:
            fc.append("[o0]null[o]"); fc.append("[a]anull[af]")
        salida = os.path.join(carpeta, clip["id"] + ".mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "25", "-i", fnd] + ent + [
                        "-loop", "1", "-framerate", "25", "-i", fnd.replace("fondo", "mascara")] + extra + [
                        "-filter_complex", ";".join(fc), "-map", "[o]", "-map", "[af]", "-t", f"{total:.3f}", "-r", "25",
                        "-c:v", "libx264", "-preset", spec.get("preset", "medium"), "-crf", str(clip.get("crf", spec.get("crf", 19))), "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", salida], check=True)
        json.dump([{"ini": round(entra[k], 2), "texto": " ".join(w["p"] for w in c)} for k, c in enumerate(cues)],
                  open(os.path.join(carpeta, clip["id"] + ".subtitulos.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        print("ok", salida, f"{total:.1f} s", flush=True)

if __name__ == "__main__":
    spec = json.load(open(sys.argv[2], encoding="utf-8"))
    if sys.argv[1] == "tiempos": tiempos(spec, sys.argv[2])
    else: montar(spec, sys.argv[2], sys.argv[3], sys.argv[4].split(",") if len(sys.argv) > 4 else ())      # cuarto dato opcional: identificadores a montar, separados por comas
