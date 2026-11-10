# Copias de los clips montados con su identificador definitivo (ids.json): ligera (720 × 1280, crf 28, 64 kb/s) para el centro de control
# y completa en la carpeta pública del repositorio (piezas/PUB-XXXX-clip-<md5 corto>.mp4). Escribe publica.json. No borra nada del repositorio.
import json, os, subprocess, hashlib, shutil
REPO = "/home/user/erreklamatu-rrss/piezas"; ids = json.load(open("ids.json")); pub = json.load(open("publica.json")) if os.path.exists("publica.json") else {}
SALTA = [x for x in os.environ.get("SALTA", "").split(",") if x]
os.makedirs("lig", exist_ok=True)
for cid, pid in ids.items():
    if any(cid.startswith(x) for x in SALTA): continue
    src = f"out/{cid}.mp4"; lig = f"lig/{pid}-previa.mp4"
    if not os.path.exists(lig) or os.path.getmtime(lig) < os.path.getmtime(src):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", "scale=720:1280", "-c:v", "libx264", "-preset", "medium", "-crf", "28", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", lig], check=True)
    h = hashlib.md5(open(src, "rb").read()).hexdigest()[:8]; dst = f"{REPO}/{pid}-clip-{h}.mp4"
    if not os.path.exists(dst): shutil.copy(src, dst)
    pub[cid] = f"https://raw.githubusercontent.com/sergiolabayen-max/erreklamatu-rrss/main/piezas/{pid}-clip-{h}.mp4"
json.dump(pub, open("publica.json", "w"), indent=1); print(len(pub), "copias")
