# Las rutas de SPECS y N apuntan a la carpeta de trabajo de la tanda del 5 de octubre de 2026: hay que cambiarlas al usarlo con otros vídeos.
"""Encuadre por zonas: coloca la cara de cada plano en la zona de cara (por encima de los subtítulos).
Uso: python3 encuadre.py medir   -> planos2.json (cajas de cara, muestreo denso)
     python3 encuadre.py calcular -> recortes nuevos por plano (planos3.json)"""
import sys, json, os, subprocess
N = "/tmp/claude-0/-home-claude-erreklamatu-rrss/049ce1e0-2613-5255-8bf4-bbf49454531a/scratchpad/video/n"
sys.path.insert(0, N + "/cv4")
import cv2, numpy as np
CAS = cv2.CascadeClassifier(N + "/haar.xml")
SPECS = [("/home/claude/cc/sistema/specs-clips-eitb-siml.json", N + "/..", ["PUB-0007", "PUB-0008", "PUB-0010", "PUB-0012", "PUB-0014"]),
         (N + "/spec-v1.json", N, None), (N + "/spec-v2.json", N, None), (N + "/spec-v3.json", N, None), (N + "/spec-v4.json", N, None)]
# zonas del diseño (px del vídeo vertical de 1080 x 1920)
TY = 480; CARA_FIN = 560; CARA_MAX = 580; AIRE_MIN, AIRE_MAX = 15, 110
def tam(src):
    o = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", src]).decode().strip().split(",")
    return int(o[0]), int(o[1])
def cuadros(src, a, b, W, H, fps=2):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a + 0.08:.3f}", "-t", f"{max(0.3, b - a - 0.16):.3f}", "-i", src, "-vf", f"fps={fps},format=bgr24", "-f", "rawvideo", "-"], capture_output=True).stdout
    n = len(raw) // (W * H * 3); return np.frombuffer(raw[:n * W * H * 3], np.uint8).reshape(n, H, W, 3)
def planos(spec, clip):
    crop0, cy0 = spec.get("crop", 174), spec.get("cy", 44)
    rec = sorted([r[0], r[1], r[2] if len(r) > 2 else cy0, r[3] if len(r) > 3 else crop0] for r in clip["recortes"]); out = []
    for n, tr in enumerate(clip["tramos"]):
        cortes = [tr["inicio"]] + [r[0] for r in rec if tr["inicio"] < r[0] < tr["fin"]] + [tr["fin"]]
        for a, b in zip(cortes, cortes[1:]):
            r = [r for r in rec if r[0] <= a + 1e-6][-1] if any(r[0] <= a + 1e-6 for r in rec) else rec[0]
            out.append(dict(tramo=n, quien=tr["quien"], a=a, b=b, x=r[1], y=r[2], lado=r[3]))
    return out
def cara(im, p):
    Hs, Ws = im.shape[:2]; x0 = max(0, int(p["x"] - 0.05 * p["lado"])); x1 = min(Ws, int(p["x"] + 1.05 * p["lado"]))
    y0 = max(0, int(p["y"] - 0.1 * p["lado"])); y1 = min(Hs, int(p["y"] + 1.2 * p["lado"]))
    z = im[y0:y1, x0:x1]; k = 480 / z.shape[0]; z = cv2.resize(z, None, fx=k, fy=k, interpolation=cv2.INTER_CUBIC); g = cv2.cvtColor(z, cv2.COLOR_BGR2GRAY)
    fs = list(CAS.detectMultiScale(g, 1.05, 6, minSize=(int(0.22 * p["lado"] * k),) * 2))
    if not len(fs): return None
    fx, fy, fw, fh = max(fs, key=lambda f: f[2])
    return [x0 + fx / k, y0 + fy / k, fw / k, fh / k]
def medir():
    res = []
    for ruta, carpeta, solo in SPECS:
        spec = json.load(open(ruta)); src = os.path.join(carpeta, spec["video"]); W, H = tam(src)
        for clip in spec["clips"]:
            if solo and clip["id"] not in solo: continue
            for i, p in enumerate(planos(spec, clip)):
                fr = cuadros(src, p["a"], p["b"], W, H); det = [cara(f, p) for f in fr]; ok = [d for d in det if d]
                p.update(spec=ruta, src=src, W=W, H=H, id=clip["id"], plano=i, muestras=len(fr), con_cara=len(ok), det=[[round(v, 1) for v in d] if d else None for d in det])
                res.append(p); print(clip["id"], i, p["quien"], f'{len(ok)}/{len(fr)}', flush=True)
    json.dump(res, open("planos2.json", "w"))
def calcular(manual):
    P = json.load(open("planos2.json")); out = []
    for p in P:
        k = f'{p["id"]}#{p["plano"]}'; m = manual.get(k, {}); ok = [d for d in p["det"] if d]
        q = dict(p); q.pop("det"); q["viejo"] = [p["x"], p["y"], p["lado"]]
        if "recorte" in m: q["nuevo"] = m["recorte"]; q["modo"] = "manual"
        elif len(ok) >= max(2, 0.4 * p["muestras"]) and not m.get("sin_cara"):
            top = float(np.percentile([d[1] for d in ok], 20)); bot = float(np.percentile([d[1] + d[3] for d in ok], 85)); cx = float(np.median([d[0] + d[2] / 2 for d in ok]))
            lado = m.get("lado", p["lado"]); x = p["x"] if lado == p["lado"] and "x" not in m else m.get("x", cx - 0.47 * lado)
            h = (bot - top) / lado * 1080; aire = min(AIRE_MAX, max(AIRE_MIN, CARA_FIN - h))
            y = top - aire * lado / 1080 + m.get("dy", 0); y = max(y, m.get("techo", min(p["y"], y)))
            x = max(0, min(x, p["W"] - lado)); y = max(0, min(y, p["H"] - lado))
            q["nuevo"] = [int(round(x)), int(round(y)), int(lado)]; q["modo"] = "cara"
            q["cara_rel"] = [round((top - y) / lado * 1080), round((bot - y) / lado * 1080), round((cx - x) / lado * 1080)]
        else: q["nuevo"] = q["viejo"]; q["modo"] = "sin cara"
        out.append(q)
        print(k, q["quien"], q["modo"], q["viejo"], "->", q["nuevo"], q.get("cara_rel"), "" if q["modo"] != "cara" or q["cara_rel"][1] <= CARA_MAX else "  <<< cara baja")
    json.dump(out, open("planos3.json", "w"), indent=1)
if __name__ == "__main__":
    if sys.argv[1] == "medir": medir()
    else: calcular(json.load(open("manual.json")) if os.path.exists("manual.json") else {})
