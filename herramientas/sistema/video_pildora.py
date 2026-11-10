#!/usr/bin/env python3
"""Convierte un fragmento de vídeo horizontal en una píldora vertical 1080 x 1920 con marco de marca y subtítulos.

Uso:  python3 video_pildora.py spec.json salida.mp4
spec.json:
  {"video": ruta, "inicio": segundos, "fin": segundos, "kicker": texto, "titular": [línea1, línea2],
   "credito": "Imágenes: TVE", "recorte_x": 0,
   "subtitulos": [{"inicio": s, "fin": s, "texto": "..."}]}   (tiempos del vídeo original)

Los subtítulos NO se generan aquí: salen de una transcripción que una persona ha revisado oyendo el audio.
Requiere ffmpeg con libass, Pillow y la fuente Poppins. El logo va en logo.png, junto a este archivo.
"""
import json, os, subprocess, sys, tempfile, textwrap
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FDIR = "/usr/share/fonts/truetype/google-fonts"
NAVY, GREEN, W, H, VY = (0, 51, 120), (0, 232, 135), 1080, 1920, 470

def fuente(peso, tam):
    for nombre in (f"Poppins-{peso}.ttf", "Poppins-Bold.ttf"):
        ruta = os.path.join(FDIR, nombre)
        if os.path.exists(ruta): return ImageFont.truetype(ruta, tam)
    raise SystemExit("Falta la fuente Poppins en " + FDIR)

def ts(t):
    return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"

def main(spec, salida):
    tmp = tempfile.mkdtemp()
    bg = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(bg)
    x = 70
    for ch in spec["kicker"].upper():
        d.text((x, 150), ch, font=fuente("SemiBold", 30), fill=GREEN); x += d.textlength(ch, font=fuente("SemiBold", 30)) + 5
    for n, linea in enumerate(spec["titular"][:2]):
        d.text((70, 205 + 90 * n), linea, font=fuente("Bold", 74), fill="white")
    if spec.get("credito"):
        f = fuente("Regular", 24); d.text((W - 70 - d.textlength(spec["credito"], font=f), 420), spec["credito"], font=f, fill=(150, 170, 205))
    d.rectangle([0, 1740, W, H], fill="white")
    logo = Image.open(os.path.join(AQUI, "logo.png")).convert("RGB")
    logo = logo.resize((int(logo.width * 1.25), int(logo.height * 1.25)), Image.LANCZOS); bg.paste(logo, (70, 1740 + (180 - logo.height) // 2))
    f = fuente("Regular", 34); d.text((W - 70 - d.textlength("erreklamatu.com", font=f), 1806), "erreklamatu.com", font=f, fill=(84, 100, 140))
    fondo = os.path.join(tmp, "fondo.png"); bg.save(fondo)

    t0, t1 = float(spec["inicio"]), float(spec["fin"]); dur = t1 - t0
    ev = []
    for s in spec.get("subtitulos", []):
        lineas = textwrap.wrap(s["texto"], 25); bloques = [lineas[i:i + 2] for i in range(0, len(lineas), 2)]
        total = sum(len(" ".join(b)) for b in bloques); t = float(s["inicio"])
        for b in bloques:
            paso = (float(s["fin"]) - float(s["inicio"])) * len(" ".join(b)) / total
            ev.append(f"Dialogue: 0,{ts(max(t - t0, 0))},{ts(t + paso - t0)},S,,0,0,0,,{{\\pos(540,1645)}}" + "\\N".join(b)); t += paso
    ass = os.path.join(tmp, "subs.ass")
    open(ass, "w", encoding="utf8").write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: S,Poppins,68,&H00FFFFFF,&H00FFFFFF,&H00783300,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,5,40,40,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n")
    rx = int(spec.get("recorte_x", 0))
    fc = (f"[1:v]crop=ih:ih:{rx}:0,scale=1080:1080:flags=lanczos[v];[0:v][v]overlay=0:{VY}[c];"
          f"[c]ass={ass}:fontsdir={FDIR}[o];[1:a]afade=t=in:d=0.15,afade=t=out:st={dur-0.2:.2f}:d=0.2[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "25", "-i", fondo, "-ss", str(t0), "-t", str(dur), "-i", spec["video"],
                    "-filter_complex", fc, "-map", "[o]", "-map", "[a]", "-t", str(dur), "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", salida], check=True)
    print("ok", salida)

if __name__ == "__main__":
    main(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2])
