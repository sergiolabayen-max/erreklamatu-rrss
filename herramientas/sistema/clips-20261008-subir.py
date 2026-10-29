# Copia los vídeos montados a la carpeta pública (piezas/PUB-XXXX-clip-<md5 corto>.mp4) y escribe publica.json. No borra nada del repositorio.
import hashlib, glob, json, os, shutil
REPO = "/home/claude/erreklamatu-rrss/piezas"; pub = {}
for f in sorted(glob.glob("out/PUB-*.mp4")):
    pid = os.path.basename(f)[:-4]; h = hashlib.md5(open(f, "rb").read()).hexdigest()[:8]; dst = f"{REPO}/{pid}-clip-{h}.mp4"
    if not os.path.exists(dst): shutil.copy(f, dst)
    pub[pid] = f"https://raw.githubusercontent.com/sergiolabayen-max/erreklamatu-rrss/main/piezas/{pid}-clip-{h}.mp4"
json.dump(pub, open("publica.json", "w"), indent=1); print(json.dumps(pub, indent=1))
