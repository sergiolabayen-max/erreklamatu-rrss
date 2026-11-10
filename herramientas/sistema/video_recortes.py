"""Propone los recortes de cada tramo localizando la cara de quien habla. Uso: se importa (recortes_clip) o se ejecuta para ver una tira de comprobación."""
import sys; sys.path.insert(0, "./cv4")
import cv2, subprocess, numpy as np, json, os, tempfile
CAS = cv2.CascadeClassifier("haar.xml")
def frame(src, t):
    f = tempfile.mktemp(suffix=".png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", f], check=True)
    im = cv2.imread(f); os.remove(f); return im
def caras(im, zona_y=(0.0, 0.8)):
    H, W = im.shape[:2]; g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    out = []
    for (x, y, w, h) in CAS.detectMultiScale(g, 1.08, 6, minSize=(int(H * 0.13),) * 2):
        if zona_y[0] * H <= y + h / 2 <= zona_y[1] * H: out.append((int(x), int(y), int(w), int(h)))
    return out
def elegir(fs, W, H, lado):
    """lado: 'der', 'izq', 'centro' o 'mayor'. Devuelve la cara que encaja o None."""
    def cx(f): return (f[0] + f[2] / 2) / W
    if not fs: return None
    if lado == "mayor": return max(fs, key=lambda f: f[2])
    grandes = [f for f in fs if f[3] > 0.24 * H and 0.3 < cx(f) < 0.7]          # plano completo
    if grandes and len(fs) == 1: return grandes[0]
    if lado == "der": c = [f for f in fs if cx(f) > 0.58]
    elif lado == "izq": c = [f for f in fs if cx(f) < 0.42]
    else: c = [f for f in fs if 0.3 < cx(f) < 0.7]
    if c: return max(c, key=lambda f: f[2])
    return grandes[0] if grandes else None
def recorte(f, W, H, techo, suelo, k=2.5):
    x, y, w, h = f; lado = int(min(k * h, suelo - techo, W)); lado -= lado % 2
    cx = x + w / 2; top = y - 0.5 * h
    top = max(techo, min(top, suelo - lado)); left = max(0, min(cx - lado / 2, W - lado))
    return [int(left) - int(left) % 2, int(top) - int(top) % 2, lado]
def recortes_tramo(src, t0, t1, lado, techo, suelo, paso=0.4, defecto=None):
    """Devuelve [[t, x, y, lado], ...] para el tramo. Un recorte nuevo cada vez que la cara cambia de sitio (cambio de plano)."""
    ts = list(np.arange(t0 + 0.05, t1 - 0.02, paso)); det = []
    im0 = frame(src, ts[0]); H, W = im0.shape[:2]
    for t in ts:
        im = im0 if t == ts[0] else frame(src, t)
        det.append(elegir(caras(im, (techo / H, suelo / H)), W, H, lado))
    # agrupar en planos: salto de posición o de tamaño
    grupos = []; act = None
    for t, f in zip(ts, det):
        if f is None:
            if act: act["n0"] += 1
            continue
        if act and abs((f[0] + f[2] / 2) - act["cx"]) < 0.12 * W and 0.7 < f[3] / act["h"] < 1.45:
            act["fs"].append(f); act["cx"] = np.median([g[0] + g[2] / 2 for g in act["fs"]]); act["h"] = np.median([g[3] for g in act["fs"]])
        else:
            act = {"t": t, "fs": [f], "cx": f[0] + f[2] / 2, "h": f[3], "n0": 0}; grupos.append(act)
    grupos = [g for g in grupos if len(g["fs"]) >= 2 or len(grupos) == 1] or grupos[:1]
    out = []
    for i, g in enumerate(grupos):
        med = [int(np.median([f[j] for f in g["fs"]])) for j in range(4)]
        x, y, l = recorte(med, W, H, techo, suelo)
        out.append([round(float(t0 if i == 0 else g["t"] - paso / 2), 2), x, y, l])
    if not out and defecto: out = [[t0] + list(defecto)]
    sin = sum(1 for f in det if f is None)
    return out, {"muestras": len(ts), "sin_cara": sin}
if __name__ == "__main__":
    src, t0, t1, lado, techo, suelo = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], int(sys.argv[5]), int(sys.argv[6])
    print(recortes_tramo(src, t0, t1, lado, techo, suelo))
