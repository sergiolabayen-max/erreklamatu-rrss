# Propone cortes limpios para un tramo y enseña lo que se oye: python3 tramo.py k a b [k a b ...]
#   a = segundo aproximado de la primera palabra; b = segundo aproximado de la ÚLTIMA palabra (su arranque).
# inicio = final de la pausa anterior a la primera palabra (−0,08 s); fin = arranque de la pausa que sigue a la última palabra (+0,12 s).
# Enseña las palabras de Parakeet (castellano) u Omnilingual (euskera) con su segundo y el texto de Whisper que solapa.
import sys, json, re, os, numpy as np, soundfile as sf
R = "/tmp/claude-0/-home-user-erreklamatu-rrss/35d0557c-8694-51f8-b5cc-84a0f9e75554/scratchpad/radio2"
def energia(a, sr, t0, t1):
    t0 = max(0, t0); x = a[int(t0 * sr):int(t1 * sr)]; fr = int(0.01 * sr)
    return np.array([np.sqrt((x[i:i + fr] ** 2).mean()) for i in range(0, max(0, len(x) - fr), fr)]), t0
def pausas(a, sr, t0, t1, minimo=0.12):
    e, t0 = energia(a, sr, t0, t1)
    if not len(e): return []
    thr = max(np.percentile(e, 15) * 1.6, e.max() * 0.035); bajo = e < thr; out = []; i = 0
    while i < len(bajo):
        if bajo[i]:
            j = i
            while j < len(bajo) and bajo[j]: j += 1
            if (j - i) * 0.01 >= minimo: out.append((round(t0 + i * 0.01, 2), round(t0 + j * 0.01, 2)))
            i = j
        else: i += 1
    return out
A = sys.argv[1:]; cache = {}
for n in range(0, len(A), 3):
    k, a, b = A[n], float(A[n + 1]), float(A[n + 2])
    if k not in cache: cache[k] = sf.read(f"{R}/src/{k}.wav", dtype="float32")
    x, sr = cache[k]
    pa = pausas(x, sr, a - 2.0, a + 0.4); antes = [p for p in pa if p[1] <= a + 0.25]
    ini = round(antes[-1][1] - 0.08, 2) if antes else round(a - 0.15, 2)
    pb = pausas(x, sr, b + 0.1, b + 4.0); desp = [p for p in pb if p[0] >= b + 0.15]
    fin = round(desp[0][0] + 0.12, 2) if desp else round(b + 0.8, 2)
    if os.path.exists(f"{R}/aud/{k}.pk.json"): pal = [(w, t) for w, t in json.load(open(f"{R}/aud/{k}.pk.json"))]
    else: pal = [(w, s) for w, s, e in json.load(open(f"{R}/aud/{k}.palabras.json"))]
    ws = [w for w, t in pal if ini - 0.05 <= t <= fin]
    print(f"### {k} propuesta inicio {ini}  fin {fin}  ({fin - ini:.1f} s)")
    print("    PRIMERAS:", " ".join(f"{w}@{t:.2f}" for w, t in pal if ini - 1.5 <= t <= ini + 1.2))
    print("    ÚLTIMAS :", " ".join(f"{w}@{t:.2f}" for w, t in pal if fin - 1.5 <= t <= fin + 1.5))
    print("    TEXTO   :", " ".join(ws))
    for l in (open(f"{R}/aud/{k}.txt") if os.path.exists(f"{R}/aud/{k}.txt") else []):
        m = re.match(r"\[\s*([\d.]+)-\s*([\d.]+)\] (.*)", l)
        if m and float(m.group(2)) > ini and float(m.group(1)) < fin: print(f"    WHISPER [{m.group(1)}-{m.group(2)}] {m.group(3)}")
