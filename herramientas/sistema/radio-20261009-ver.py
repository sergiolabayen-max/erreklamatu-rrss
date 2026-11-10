# Palabras con su segundo (Omnilingual u otro .palabras.json / .pk.json), en líneas de ~20 palabras: python3 ver.py k [desde hasta]
import json, sys, os
R = "/tmp/claude-0/-home-user-erreklamatu-rrss/35d0557c-8694-51f8-b5cc-84a0f9e75554/scratchpad/radio2/aud/"
k = sys.argv[1]; a = float(sys.argv[2]) if len(sys.argv) > 2 else 0; b = float(sys.argv[3]) if len(sys.argv) > 3 else 1e9
f = R + k + (".palabras.json" if os.path.exists(R + k + ".palabras.json") else ".pk.json")
p = [x for x in json.load(open(f)) if a <= x[1] <= b]; line = []; prev = None
for x in p:
    if prev is not None and (x[1] - prev > 0.7 or len(line) >= 18): print(" ".join(line)); line = []
    line.append(f"{x[0]}@{x[1]:.1f}"); prev = x[1]
if line: print(" ".join(line))
