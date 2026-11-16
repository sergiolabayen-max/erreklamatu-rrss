#!/usr/bin/env python3
"""Hoja de revisión visual de una pieza (filtro de corrección, pedido por Sergio el 16/11/2026).

Sergio: «que haya un filtro de corrección antes de enviarme piezas con estos errores» (PUB-0617: cara de la chica
cortada en el gancho; PUB-0619: de Jon solo se veía la frente). El fallo vino de revisar solo uno o dos fotogramas.

Uso:
  python3 hoja_revision.py VIDEO_O_IMAGENES... --salida carpeta
Para un vídeo saca UN FOTOGRAMA POR SEGUNDO, de principio a fin, con el segundo escrito encima, en hojas de 4 × 3
(se ven grandes). Para imágenes (infografías, láminas de carrusel) hace hojas de 3 × 2. Imprime las rutas de las hojas.

Las hojas las revisa SIEMPRE un revisor que no ha hecho la pieza (subagente nuevo), con la lista de
sistema/REVISION_VISUAL.md, ANTES de poner la pieza en «Pendiente de revisión».
"""
import argparse, os, subprocess, sys, glob
from PIL import Image, ImageDraw, ImageFont

FUENTE = next((f for f in glob.glob("/usr/share/fonts/**/*Poppins*Bold*.ttf", recursive=True)), None)

def rotulo(im, texto):
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FUENTE, 28) if FUENTE else ImageFont.load_default()
    d.rectangle([0, 0, 150, 40], fill=(0, 0, 0))
    d.text((8, 4), texto, fill=(0, 232, 135), font=f)
    return im

def hojas(imgs, cols, filas, ancho, salida, base):
    rutas = []
    por = cols * filas
    for h in range(0, len(imgs), por):
        lote = imgs[h:h + por]
        w = ancho; hh = int(w * lote[0][1].height / lote[0][1].width)
        hoja = Image.new("RGB", (cols * w + (cols + 1) * 8, filas * hh + (filas + 1) * 8), (40, 40, 40))
        for i, (txt, im) in enumerate(lote):
            im = rotulo(im.convert("RGB").resize((w, hh)), txt)
            hoja.paste(im, (8 + (i % cols) * (w + 8), 8 + (i // cols) * (hh + 8)))
        r = os.path.join(salida, f"{base}-hoja-{h // por + 1:02d}.jpg"); hoja.save(r, quality=88); rutas.append(r)
    return rutas

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("ficheros", nargs="+"); ap.add_argument("--salida", default="revision")
    a = ap.parse_args(); os.makedirs(a.salida, exist_ok=True)
    for f in a.ficheros:
        base = os.path.splitext(os.path.basename(f))[0]
        if f.lower().endswith((".mp4", ".mov", ".webm")):
            tmp = os.path.join(a.salida, base + "-fot"); os.makedirs(tmp, exist_ok=True)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f, "-vf", "fps=1,scale=540:-1", os.path.join(tmp, "%04d.png")], check=True)
            fr = sorted(glob.glob(os.path.join(tmp, "*.png")))
            imgs = [(f"{i}s", Image.open(p)) for i, p in enumerate(fr)]
            for r in hojas(imgs, 4, 3, 360, a.salida, base): print(r)
        else:
            imgs = [(os.path.basename(f)[:8], Image.open(f))]
            for r in hojas(imgs, 1, 1, 720, a.salida, base): print(r)

if __name__ == "__main__":
    main()
