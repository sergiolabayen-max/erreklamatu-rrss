#!/usr/bin/env python3
"""Tiempos de palabra para clips en euskera (9 de octubre de 2026): el reconocimiento de Whisper en euskera no sirve (repite frases
y se inventa palabras), así que la transcripción entera se hace con Omnilingual ASR 1B de Meta (sherpa-onnx, CTC), que da cada
carácter con su segundo. Aquí se alinea, carácter a carácter, el texto corregido de cada tramo con lo que oyó la máquina en esos
segundos, y cada palabra toma el segundo de su primera letra emparejada. Las palabras sin pareja se reparten entre las vecinas.
Salida: spec.tiempos.json con el mismo formato que video_clips.py tiempos.
En castellano se usa igual con las palabras de Parakeet TDT v3 (aud/<k>.pk.json), que trae el segundo de cada palabra: así los tiempos
no dependen de volver a reconocer el audio con Whisper, y Whisper queda para la segunda lectura del clip montado (chkout).

  python3 tiempos_omni.py spec.json palabras.json     (palabras.json: [[palabra, inicio, fin], ...] de todo el audio)
"""
import difflib, json, sys, re, unicodedata

def norm(p):
    p = unicodedata.normalize("NFD", p.lower())
    return re.sub(r"[^a-z0-9ñ]", "", "".join(c for c in p if unicodedata.category(c) != "Mn" or c == "̃"))

def alinear(ref_words, oid, t_ini, t_fin):
    """ref_words: palabras del texto; oid: [[palabra, ini, fin]] reconocidas en el tramo. Devuelve (ini, fin) por palabra y cuántas se emparejaron."""
    hs, ht = [], []                                                    # cadena oída y segundo de cada carácter
    for w, a, b in oid:
        n = norm(w)
        for i, ch in enumerate(n): hs.append(ch); ht.append(a + (b - a) * i / max(1, len(n)))
        hs.append(" "); ht.append(b)
    rs, rw = [], []                                                    # cadena de referencia y palabra de cada carácter
    for k, w in enumerate(ref_words):
        for ch in norm(w): rs.append(ch); rw.append(k)
        rs.append(" "); rw.append(-1)
    sm = difflib.SequenceMatcher(None, "".join(rs), "".join(hs), autojunk=False)
    ini = [None] * len(ref_words); fin = [None] * len(ref_words); cnt = [0] * len(ref_words); tot = [0] * len(ref_words)
    for k in rw:
        if k >= 0: tot[k] += 1
    for bl in sm.get_matching_blocks():
        if bl.size < 2: continue
        for j in range(bl.size):
            k = rw[bl.a + j]
            if k < 0: continue
            t = ht[bl.b + j]; cnt[k] += 1
            ini[k] = t if ini[k] is None else min(ini[k], t); fin[k] = t if fin[k] is None else max(fin[k], t)
    ok = [cnt[k] >= max(2, 0.5 * tot[k]) or (tot[k] <= 2 and cnt[k] == tot[k] and tot[k] > 0) for k in range(len(ref_words))]
    for k in range(len(ref_words)):
        if not ok[k]: ini[k] = fin[k] = None
    anclas = [(-1, t_ini, t_ini)] + [(k, ini[k], fin[k] + 0.08) for k in range(len(ref_words)) if ini[k] is not None] + [(len(ref_words), t_fin, t_fin)]
    for (i0, _, f0), (i1, s1, _) in zip(anclas, anclas[1:]):
        hueco = list(range(i0 + 1, i1))
        if not hueco: continue
        s1 = max(s1, f0); L = sum(len(ref_words[i]) for i in hueco) or 1; ac = 0
        for i in hueco:
            ini[i] = f0 + (s1 - f0) * ac / L; ac += len(ref_words[i]); fin[i] = f0 + (s1 - f0) * ac / L
    t = t_ini; out = []
    for i in range(len(ref_words)):
        a = max(ini[i], t); b = max(fin[i] if fin[i] is not None else a, a + 0.05); t = a
        out.append((round(a, 2), round(min(b, t_fin), 2)))
    return out, sum(ok)

if __name__ == "__main__":
    ruta = sys.argv[1]; spec = json.load(open(ruta, encoding="utf8")); pal = json.load(open(sys.argv[2], encoding="utf8")); salida = {}
    if pal and len(pal[0]) == 2:                                       # formato de Parakeet ([palabra, inicio]): el final es el inicio de la siguiente (como mucho +0,6 s)
        pal = [[w, t, min(pal[i + 1][1] if i + 1 < len(pal) else t + 0.4, t + 0.6)] for i, (w, t) in enumerate(pal)]
    for clip in spec["clips"]:
        ws = []
        for n, tr in enumerate(clip["tramos"]):
            ref = tr["texto"].split(); oid = [p for p in pal if p[2] > tr["inicio"] and p[1] < tr["fin"]]
            tt, ok = alinear(ref, oid, tr["inicio"], tr["fin"])
            print(f'{clip["id"]} tramo {n + 1}: {ok} de {len(ref)} palabras localizadas en el audio', flush=True)
            ws += [{"p": w, "ini": a, "fin": b, "tramo": n} for w, (a, b) in zip(ref, tt)]
        salida[clip["id"]] = ws
    json.dump(salida, open(ruta.replace(".json", ".tiempos.json"), "w", encoding="utf8"), ensure_ascii=False, indent=0)
