#!/usr/bin/env python3
"""Planos muy cerrados de los reportajes (la cara no cabe por encima de los subtítulos): se usa una copia del vídeo con una franja azul añadida por debajo,
para poder tomar un cuadrado más grande que el propio fotograma y que la cara quede más pequeña. Se ejecuta después de encuadrar; es idempotente."""
import json, sys
CFG = {"ps": dict(H=704, W=1264, lado=880, pad="ps.pad.mp4", sin=[280, 0, 704]), "pe": dict(H=720, W=1280, lado=900, pad="pe.pad.mp4", sin=[280, 0, 720])}
N5 = __import__("defs").N5
for v, c in CFG.items():
    sp = json.load(open(f"spec-{v}.json")); n = 0
    for clip in sp["clips"]:
        rec = clip.get("recortes") or []
        for r in rec:
            if r[3] >= 0.96 * c["H"] and r[3] <= c["H"] and r[1:] != c["sin"]:
                cx = r[1] + 0.47 * r[3]; r[1] = int(max(0, min(cx - 0.47 * c["lado"], c["W"] - c["lado"]))); r[2] = 0; r[3] = c["lado"]; n += 1
        for t in clip["tramos"]:
            dentro = [r for r in rec if t["inicio"] - 1e-6 <= r[0] < t["fin"]]
            antes = [r for r in rec if r[0] <= t["inicio"] + 1e-6]
            usados = dentro + (antes[-1:] if antes else [])
            if any(r[3] > c["H"] for r in usados): t["video"] = N5 + "/" + c["pad"]
            # si el tramo usa la copia con franja, todos sus recortes valen igual (la imagen está arriba, en las mismas coordenadas)
    json.dump(sp, open(f"spec-{v}.json", "w"), ensure_ascii=False, indent=1); print(v, n, "planos ampliados;", sum(1 for cl in sp["clips"] for t in cl["tramos"] if "video" in t), "tramos con la copia")
