# Recalcula los tiempos de palabra solo de algunos clips y los mezcla en spec-<v>.tiempos.json.  python3 retie.py v10 PUB-0185 PUB-0186
import json, sys, subprocess, os
v, ids = sys.argv[1], sys.argv[2:]
sp = json.load(open(f"spec-{v}.json")); tmp = dict(sp, clips=[c for c in sp["clips"] if c["id"] in ids])
json.dump(tmp, open(f"spec-{v}-re.json", "w"), ensure_ascii=False)
out = subprocess.run(["python3", "/home/claude/cc/sistema/video_clips.py", "tiempos", f"spec-{v}-re.json"], capture_output=True, text=True)
print(out.stdout.strip()); print(out.stderr.strip()[-300:])
ti = json.load(open(f"spec-{v}.tiempos.json")); ti.update(json.load(open(f"spec-{v}-re.tiempos.json"))); json.dump(ti, open(f"spec-{v}.tiempos.json", "w"), ensure_ascii=False)
with open(f"tie-{v}.log", "a") as f: f.write(out.stdout)
os.remove(f"spec-{v}-re.json"); os.remove(f"spec-{v}-re.tiempos.json")
