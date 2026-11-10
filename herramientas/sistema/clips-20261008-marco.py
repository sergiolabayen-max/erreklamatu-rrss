#!/usr/bin/env python3
"""Encuadre automático por zonas para clips nuevos.
Uso:  python3 marco.py encuadrar spec.json            -> rellena "recortes" de cada clip (y escribe spec.planos.json)
      python3 marco.py previa spec.json hoja.png [ids] -> hoja de comprobación con el diseño por zonas

En la especificación, cada tramo lleva "enc": a quién hay que buscar en la imagen.
  "der" | "izq" | "centro" | "mayor" | "izqarriba" | "derarriba" (de dos ventanas apiladas en ese lado, la de arriba)  o una lista de preferencias ["izq", "der"]  o un recorte fijo [x, y, lado]
  o una lista de recortes fijos con su momento [[t, x, y, lado], ...].
La especificación lleva "marco": {"lado_ventana": 186, "lado_pleno": 244, "techo": 0, "sin_cara": [x, y, lado], "k": 2.4}.
"""
import sys, json, os, subprocess, re, tempfile
N = "/tmp/claude-0/-home-claude/e7eefa61-a30f-57c7-bc2e-7996fd2458cc/scratchpad/video/n"
sys.path.insert(0, N + "/cv4"); sys.path.insert(0, "/home/claude/cc/sistema")
import cv2, numpy as np
CAS = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
RUTA_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "caras.cache.json"); CACHE = json.load(open(RUTA_CACHE)) if os.path.exists(RUTA_CACHE) else {}
CARA_FIN, AIRE_MIN, AIRE_MAX, OBJ = 560, 15, 110, 450       # zonas: la cara acaba como mucho a 560 px del borde superior del vídeo

def tam(src):
    o = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", src]).decode().strip().split(",")
    return int(o[0]), int(o[1])
def cuadros(src, a, b, W, H, fps=4):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-t", f"{max(0.3, b - a):.3f}", "-i", src, "-vf", f"fps={fps},format=bgr24", "-f", "rawvideo", "-"], capture_output=True).stdout
    n = len(raw) // (W * H * 3); return np.frombuffer(raw[:n * W * H * 3], np.uint8).reshape(n, H, W, 3)
def caras(im, techo):
    H, W = im.shape[:2]; k = max(1.0, 720 / H) if H < 720 else 720 / H
    z = cv2.resize(im, None, fx=k, fy=k, interpolation=cv2.INTER_CUBIC if k > 1 else cv2.INTER_AREA); g = cv2.cvtColor(z, cv2.COLOR_BGR2GRAY)
    out = []
    for (x, y, w, h) in CAS.detectMultiScale(g, 1.06, 6, minSize=(int(0.11 * H * k),) * 2):
        x, y, w, h = x / k, y / k, w / k, h / k
        if y >= techo - 2 and y + h / 2 < 0.78 * H: out.append((x, y, w, h))
    return out
def elegir(fs, W, H, pref):
    def cx(f): return (f[0] + f[2] / 2) / W
    if not fs: return None, None
    for p in pref:
        if p == "mayor": return max(fs, key=lambda f: f[2]), "pleno"
        if p in ("izqarriba", "derarriba"):                       # dos ventanas apiladas en un lado: la de arriba
            c = [f for f in fs if (cx(f) < 0.5 if p == "izqarriba" else cx(f) > 0.5)]
            if c: return min(c, key=lambda f: f[1]), p[:3]
            continue
        grandes = [f for f in fs if f[3] > 0.25 * H and 0.25 < cx(f) < 0.75]
        if grandes and len(fs) == 1: return grandes[0], "pleno"
        c = [f for f in fs if (cx(f) > 0.56 if p == "der" else cx(f) < 0.44 if p == "izq" else 0.3 < cx(f) < 0.7)]
        if c: return max(c, key=lambda f: f[2]), ("pleno" if p == "centro" else p)
    return None, None
def corte(src, t, margen=0.45):
    a = max(0, t - margen)
    out = subprocess.run(["ffmpeg", "-v", "info", "-ss", f"{a:.3f}", "-t", f"{2 * margen:.3f}", "-i", src, "-vf", "select='gte(scene,0)',metadata=print", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    pts = [float(x) for x in re.findall(r"pts_time:([0-9.]+)", out)]; sc = [float(x) for x in re.findall(r"lavfi.scene_score=([0-9.]+)", out)]
    if not sc: return t, 0
    i = max(range(len(sc)), key=lambda k: sc[k]); return round(a + pts[i], 2), sc[i]
CORTES = {}
def cortes_secos(src, a, b, umbral):
    if src not in CORTES:
        out = subprocess.run(["ffmpeg", "-v", "info", "-i", src, "-vf", "scale=320:-2,select='gt(scene,0.12)',metadata=print", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
        CORTES[src] = list(zip([float(x) for x in re.findall(r"pts_time:([0-9.]+)", out)], [float(x) for x in re.findall(r"lavfi.scene_score=([0-9.]+)", out)]))
    return [t for t, sc in CORTES[src] if a <= t <= b and sc >= umbral]
def dif(src, t1, t2, reg):
    """Cuánto cambia la zona del recorte entre dos momentos (0-255). Si apenas cambia, es el mismo plano."""
    x, y, l = reg; ims = []
    for t in (t1, t2):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", "-vf", f"crop={l}:{l}:{x}:{y},scale=48:48,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
        ims.append(np.frombuffer(raw[:2304], np.uint8).astype(float))
    return float(np.abs(ims[0] - ims[1]).mean()) if len(ims[0]) == len(ims[1]) == 2304 else 99.0
def recorte_cara(g, W, H, M, modo):
    fs = g["fs"]; top = float(np.percentile([f[1] for f in fs], 20)); bot = float(np.percentile([f[1] + f[3] for f in fs], 85)); cx = float(np.median([f[0] + f[2] / 2 for f in fs]))
    h = bot - top; lmax = M.get("lado_" + modo, M.get("lado_pleno", H) if modo == "pleno" else M.get("lado_ventana", H))
    lado = int(min(max(M.get("k", 2.4) * h, M.get("lado_min", 0)), lmax, H, W)); lado -= lado % 2
    hpx = h / lado * 1080; aire = min(AIRE_MAX, max(AIRE_MIN, CARA_FIN - hpx))
    y = top - aire * lado / 1080; x = cx - 0.47 * lado
    lim = M.get("lim_" + modo)                                    # límites horizontales de la ventana: [x0, x1]
    x0, x1 = lim if lim else (0, W)
    x = max(x0, min(x, x1 - lado)); y = max(M.get("techo", 0), min(y, H - lado))
    return [int(round(x)), int(round(y)), lado], [round((top - y) / lado * 1080), round((bot - y) / lado * 1080), round((cx - x) / lado * 1080)]

def encuadrar(ruta, ids=()):
    spec = json.load(open(ruta)); src = spec["video"] if os.path.isabs(spec["video"]) else os.path.join(os.path.dirname(os.path.abspath(ruta)), spec["video"]); W, H = tam(src); M = spec.get("marco", {})
    sin = M.get("sin_cara") or [int((W - 0.9 * H) / 2), int(0.04 * H), int(0.9 * H) - int(0.9 * H) % 2]; planos = []
    for clip in spec["clips"]:
        if clip.get("recortes") and clip["id"] not in ids: continue        # ya encuadrado: solo se rehace si se pide por su identificador
        rec = []
        for n, tr in enumerate(clip["tramos"]):
            enc = tr.get("enc", spec.get("enc", {}).get(tr["quien"], "mayor")); a, b = tr["inicio"], tr["fin"]
            if isinstance(enc, list) and enc and isinstance(enc[0], (int, float)): rec.append([a] + list(enc)); planos.append(dict(id=clip["id"], tramo=n, a=a, modo="fijo", nuevo=enc)); continue
            if isinstance(enc, list) and enc and isinstance(enc[0], list):
                for r in enc: rec.append([max(a, r[0])] + list(r[1:])); planos.append(dict(id=clip["id"], tramo=n, a=max(a, r[0]), modo="fijo", nuevo=r[1:]))
                continue
            pref = enc if isinstance(enc, list) else [enc]; fps = 4; clave_c = f'{src}|{a}|{b}|{M.get("techo", 0)}'
            fr = cuadros(src, a, b, W, H, fps) if clave_c not in CACHE else [None] * len(CACHE[clave_c]); ts = [a + i / fps for i in range(len(fr))]
            clave_c = f'{src}|{a}|{b}|{M.get("techo", 0)}'
            if clave_c not in CACHE: CACHE[clave_c] = [[list(map(float, c)) for c in caras(f, M.get("techo", 0))] for f in fr]; json.dump(CACHE, open(RUTA_CACHE, "w"))
            det = [elegir([tuple(c) for c in cs], W, H, pref) for cs in CACHE[clave_c]]
            if clip.get("planos", M.get("planos")) == "cortes":
                # vídeo montado con cortes secos: un recorte por plano, con todas las caras vistas en él
                cs = [a] + [t for t in cortes_secos(src, a, b, M.get("corte", 0.3)) if a + 0.4 < t < b - 0.4] + [b]
                cs = [cs[0]] + [t for i, t in enumerate(cs[1:-1], 1) if t - cs[i - 1] >= 0.5] + [cs[-1]]
                for i, (p0, p1) in enumerate(zip(cs, cs[1:])):
                    dd = [(f, m) for t, (f, m) in zip(ts, det) if p0 + 0.1 <= t < p1 - 0.1 and f is not None and f[3] >= M.get("cara_min", 0.0) * H]
                    nm = sum(1 for t in ts if p0 + 0.1 <= t < p1 - 0.1)
                    if len(dd) >= max(2, 0.3 * nm):
                        modo = max(set(m for f, m in dd), key=[m for f, m in dd].count); g = dict(fs=[f for f, m in dd if m == modo]); r, rel = recorte_cara(g, W, H, M, modo)
                    else: r, rel, modo = list(tr.get("sin_cara", sin)), None, "sin cara"
                    if rec and i and all(abs(u - v) <= 0.09 * r[2] for u, v in zip(rec[-1][1:], r)): continue      # mismo encuadre que el plano anterior: no se salta
                    rec.append([round(p0, 2)] + r); planos.append(dict(id=clip["id"], tramo=n, a=round(p0, 2), modo=modo, nuevo=r, rel=rel))
                    print(clip["id"], n, tr["quien"], f"{p0:.2f}", modo, r, rel, f"{len(dd)}/{nm}", flush=True)
                continue
            grupos = []; act = None
            for t, (f, modo) in zip(ts, det):
                if f is None: clave = None
                else: clave = modo
                if act and act["modo"] == clave and (f is None or (abs((f[0] + f[2] / 2) - act["cx"]) < 0.1 * W and 0.72 < f[3] / act["h"] < 1.4 and abs(f[1] - act["y"]) < 0.12 * H)):
                    act["n"] += 1
                    if f is not None: act["fs"].append(f); act["cx"] = float(np.median([q[0] + q[2] / 2 for q in act["fs"]])); act["h"] = float(np.median([q[3] for q in act["fs"]])); act["y"] = float(np.median([q[1] for q in act["fs"]]))
                else:
                    act = dict(t=t, modo=clave, n=1, fs=[f] if f is not None else [], cx=(f[0] + f[2] / 2) if f is not None else 0, h=f[3] if f is not None else 0, y=f[1] if f is not None else 0); grupos.append(act)
            # grupos de menos de 0,75 s se pegan al anterior (o al siguiente, si son el primero)
            lim = []
            for g in grupos:
                if g["n"] < 3 and lim: lim[-1]["n"] += g["n"]; continue
                lim.append(g)
            if len(lim) > 1 and lim[0]["n"] < 3: lim[1]["t"] = lim[0]["t"]; lim[1]["n"] += lim[0]["n"]; lim = lim[1:]
            # grupos iguales seguidos (misma posición) se funden
            fin = []
            for g in lim:
                p = fin[-1] if fin else None
                if p and p["modo"] == g["modo"] and (g["modo"] is None or (abs(g["cx"] - p["cx"]) < 0.06 * W and 0.8 < g["h"] / p["h"] < 1.25 and abs(g["y"] - p["y"]) < 0.07 * H)): p["n"] += g["n"]; p["fs"] += g["fs"]; continue
                fin.append(g)
            # una frontera sin cambio de plano real (la imagen no salta) no es un plano nuevo: se queda el grupo con cara, o el más largo
            k = 1
            while k < len(fin):
                t0, sc = corte(src, fin[k]["t"] - 0.4, 0.8)
                if sc < 0.06: t0 = fin[k]["t"] - 0.4                                  # transición animada: no hay un fotograma de corte claro
                fin[k]["t0"] = t0
                p, g = fin[k - 1], fin[k]; ref = p if p["modo"] is not None else g
                reg = recorte_cara(ref, W, H, M, ref["modo"])[0] if ref["modo"] is not None else [0, 0, min(W, H)]
                d = dif(src, max(a, p["t"], fin[k]["t"] - 1.0), min(b - 0.05, fin[k]["t"] + 0.5), reg)
                print("   frontera", clip["id"], n, f'{fin[k]["t"]:.2f}', p["modo"], "->", g["modo"], "escena", round(sc, 3), "dif", round(d, 1), flush=True)
                if d < M.get("umbral", 13):
                    p, g = fin[k - 1], fin[k]
                    gana = p if (g["modo"] is None or (p["modo"] is not None and p["n"] >= g["n"])) else g
                    gana = dict(gana, t=p["t"], n=p["n"] + g["n"]);
                    if "t0" in p: gana["t0"] = p["t0"]
                    else: gana.pop("t0", None)
                    fin[k - 1:k + 1] = [gana]
                else: k += 1
            for i, g in enumerate(fin):
                t0 = a
                if i: t0 = min(max(g["t0"], a + 0.2), b - 0.2)
                if g["modo"] is None: r, rel, modo = list(tr.get("sin_cara", sin)), None, "sin cara"
                else: (r, rel), modo = recorte_cara(g, W, H, M, g["modo"]), g["modo"]
                rec.append([round(t0, 2)] + r); planos.append(dict(id=clip["id"], tramo=n, a=round(t0, 2), modo=modo, nuevo=r, rel=rel, muestras=g["n"]))
                print(clip["id"], n, tr["quien"], f"{t0:.2f}", modo, r, rel, g["n"], "" if not rel or rel[1] <= 585 else " <<< cara baja", flush=True)
        clip["recortes"] = rec
    json.dump(spec, open(ruta, "w"), ensure_ascii=False, indent=1)

def previa(ruta, salida, ids):
    import video_clips as V
    from PIL import Image, ImageDraw
    spec = json.load(open(ruta)); src = spec["video"] if os.path.isabs(spec["video"]) else os.path.join(os.path.dirname(os.path.abspath(ruta)), spec["video"]); L = V.DISENOS["zonas"]
    tmp = tempfile.mkdtemp(); thumbs = []
    for clip in spec["clips"]:
        if ids and clip["id"] not in ids: continue
        rot, pre, pr, prefijo = V.cabecera(spec, clip); fnd = os.path.join(tmp, "fondo.png")
        V.fondo(clip, clip.get("credito", spec.get("credito", "")), fnd, L, clip.get("cta", spec.get("cta", V.CTAS[spec.get("idioma", "es")])), rot.get(pr, ""), prefijo)
        bg = Image.open(fnd).convert("RGB"); mk = Image.open(fnd.replace("fondo", "mascara"))
        rec = sorted(clip["recortes"]); np_ = 0
        for n, tr in enumerate(clip["tramos"]):
            cortes = [tr["inicio"]] + [r[0] for r in rec if tr["inicio"] < r[0] < tr["fin"]] + [tr["fin"]]
            for a, b in zip(cortes, cortes[1:]):
                r = [r for r in rec if r[0] <= a + 1e-6][-1] if any(r[0] <= a + 1e-6 for r in rec) else rec[0]; x, y, lado = r[1:4]
                k = 3 if b - a > 6 else 2 if b - a > 1.5 else 1
                for j in range(k):
                    t = a + (b - a) * (j + 0.5) / k if k > 1 else a + (b - a) / 2
                    if j == 0 and k > 1: t = a + 0.12
                    if j == k - 1 and k > 1: t = b - 0.15
                    f = os.path.join(tmp, "f.png")
                    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", src, "-frames:v", "1", "-vf", f"crop={lado}:{lado}:{x}:{y},scale=1080:1080:flags=lanczos", f], check=True)
                    im = bg.copy(); im.paste(Image.open(f).convert("RGB"), (0, L["ty"])); im.paste(mk, (0, 0), mk); d = ImageDraw.Draw(im)
                    fu = V.fuente("Bold", L["sub_tam"]); col = (0, 232, 135) if tr["quien"] in pre else "white"
                    for q, tx in enumerate(("subtítulo de prueba", "en dos líneas")):
                        d.text((L["sub_x"] - d.textlength(tx, font=fu) / 2, L["sub_y"] - 84 + q * 84), tx, font=fu, fill=col, stroke_width=3, stroke_fill=(0, 26, 66))
                    th = im.crop((0, 240, 1080, 1440)).resize((270, 300), Image.LANCZOS); dd = ImageDraw.Draw(th); dd.rectangle([0, 286, 270, 300], fill=(0, 0, 0))
                    dd.text((4, 287), f'{clip["id"][-4:]} t{n} p{np_} {t:.1f}s {tr["quien"][:6]}', fill=(255, 255, 0)); thumbs.append(th)
                np_ += 1
    cols = 10; rows = (len(thumbs) + cols - 1) // cols
    sh = Image.new("RGB", (cols * 274 + 4, rows * 304 + 4), (30, 30, 30))
    for i, th in enumerate(thumbs): sh.paste(th, (4 + (i % cols) * 274, 4 + (i // cols) * 304))
    sh.save(salida); print(sh.size, len(thumbs))

if __name__ == "__main__":
    if sys.argv[1] == "encuadrar": encuadrar(sys.argv[2], sys.argv[3:])
    else: previa(sys.argv[2], sys.argv[3], sys.argv[4:])
