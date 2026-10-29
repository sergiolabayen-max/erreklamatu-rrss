# Consulta en el diccionario de Euskaltzaindia (Euskaltzaindiaren Hiztegia): python3 hiztegia.py hitza [hitza ...]
import sys, re, html, subprocess, urllib.parse
for q in sys.argv[1:]:
    u = "https://www.euskaltzaindia.eus/index.php?option=com_hiztegianbilatu&task=bilaketa&Itemid=1693&lang=eu&non=sarreraBuruaStrict&query=" + urllib.parse.quote(q)
    t = subprocess.run(["curl", "-sSL", u], capture_output=True, text=True).stdout
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S); t = html.unescape(re.sub(r"<[^>]+>", " ", t)); t = re.sub(r"\s+", " ", t)
    i = t.find("emaitza"); j = t.find("Loturak", i)
    print(f"## {q}: " + (t[i - 3:(j if j > 0 else i + 500)][:600] if i > 0 else "SIN RESULTADO"))
