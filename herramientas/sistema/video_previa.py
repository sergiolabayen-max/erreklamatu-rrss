"""Hoja de comprobación: compone fotogramas de cada plano con el diseño por zonas y dibuja las zonas. Uso: previa.py salida.png [ids...]"""
import sys, json, os, subprocess, tempfile
sys.path.insert(0, "/home/claude/cc/sistema")
import video_clips as V
from PIL import Image, ImageDraw
P = json.load(open("planos3.json")); ids = sys.argv[2:] or sorted({p["id"] for p in P})
L = V.DISENOS["zonas"]; specs = {}
def clipde(p):
    if p["spec"] not in specs: specs[p["spec"]] = json.load(open(p["spec"]))
    sp = specs[p["spec"]]; return sp, next(c for c in sp["clips"] if c["id"] == p["id"])
tmp = tempfile.mkdtemp(); thumbs = []
for cid in ids:
    ps = [p for p in P if p["id"] == cid]; sp, clip = clipde(ps[0])
    rot = dict(V.ROTULOS, **sp.get("rotulos", {})); pre = sp.get("preguntan", V.PREGUNTAN)
    principal = next((t["quien"] for t in clip["tramos"] if t["quien"] not in pre), clip["tramos"][0]["quien"])
    fnd = os.path.join(tmp, "fondo.png"); V.fondo(clip, clip.get("credito", sp.get("credito", "")), fnd, L, clip.get("cta", sp.get("cta", V.CTA)), rot.get(principal, ""), "Responde " if any(t["quien"] in pre for t in clip["tramos"]) else "")
    bg = Image.open(fnd).convert("RGB"); mk = Image.open(fnd.replace("fondo", "mascara"))
    for p in ps:
        x, y, lado = p["nuevo"]; n = 3 if p["b"] - p["a"] > 3 else 2
        for j in range(n):
            t = p["a"] + (p["b"] - p["a"]) * (j + 0.5) / n
            f = os.path.join(tmp, "f.png")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", p["src"], "-frames:v", "1", "-vf", f"crop={lado}:{lado}:{x}:{y},scale=1080:1080:flags=lanczos", f], check=True)
            im = bg.copy(); im.paste(Image.open(f).convert("RGB"), (0, L["ty"])); im.paste(mk, (0, 0), mk); d = ImageDraw.Draw(im)
            fu = V.fuente("Bold", L["sub_tam"]); col = (0, 232, 135) if p["quien"] in pre else "white"
            for k, tx in enumerate(("subtítulo de prueba", "en dos líneas")):
                d.text((L["sub_x"] - d.textlength(tx, font=fu) / 2, L["sub_y"] - 84 + k * 84), tx, font=fu, fill=col, stroke_width=3, stroke_fill=(0, 26, 66))
            for yy, c in ((290, (255, 255, 0)), (1250, (255, 255, 0)), (1085, (255, 80, 80))): d.line([(0, yy), (1080, yy)], fill=c, width=3)
            th = im.resize((270, 480), Image.LANCZOS); ImageDraw.Draw(th).text((6, 462), f'{cid[-4:]}#{p["plano"]} {p["modo"]} {t:.0f}s', fill=(255, 255, 0))
            thumbs.append(th)
cols = 9; rows = (len(thumbs) + cols - 1) // cols
sh = Image.new("RGB", (cols * 274 + 4, rows * 484 + 4), (30, 30, 30))
for i, th in enumerate(thumbs): sh.paste(th, (4 + (i % cols) * 274, 4 + (i // cols) * 484))
sh.save(sys.argv[1]); print(sh.size, len(thumbs))
