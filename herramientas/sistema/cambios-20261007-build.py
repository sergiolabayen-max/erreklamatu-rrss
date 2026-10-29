# Cambios pedidos del 7 de octubre de 2026: rehace las especificaciones de los clips corregidos a partir de las publicadas.
import json, copy, os
S = "/tmp/claude-0/-home-claude-erreklamatu-rrss/e7eefa61-a30f-57c7-bc2e-7996fd2458cc/scratchpad"
OLD = "/tmp/claude-0/-home-claude/e7eefa61-a30f-57c7-bc2e-7996fd2458cc/scratchpad"
CC = "/home/claude/cc/sistema"; M = S + "/m10"
FU = {"av": (CC + "/specs-20261006-av.json", CC + "/specs-20261006-av.tiempos.json"),
      "ej": (CC + "/specs-20261006-ej.json", CC + "/specs-20261006-ej.tiempos.json"),
      "ps": (CC + "/specs-20261006-ps.json", CC + "/specs-20261006-ps.tiempos.json"),
      "pe": (CC + "/specs-20261006-pe.json", S + "/art/sistema/specs-20261006-pe.tiempos.json"),
      "vi": (S + "/af/sistema/specs-20261006b-v10.json", S + "/art/sistema/specs-20261006b-v10.tiempos.json"),
      "qa": (S + "/af/sistema/specs-20261006b-v1.json", S + "/art/sistema/specs-20261006b-v1.tiempos.json")}
QUIERO = {"av": ["PUB-0165", "PUB-0166", "PUB-0167", "PUB-0168", "PUB-0169", "PUB-0170", "PUB-0176", "PUB-0178"],
          "ej": ["PUB-0155", "PUB-0156", "PUB-0157", "PUB-0159", "PUB-0160", "PUB-0161", "PUB-0163"],
          "ps": ["PUB-0135", "PUB-0144"], "pe": ["PUB-0145"], "vi": ["PUB-0185"], "qa": ["PUB-0196"]}
TIT = {"PUB-0155": ["Gastos de hipoteca:", "¿hay garantía de éxito?"],
       "PUB-0156": ["Gastos de hipoteca:", "el acuerdo, más rápido"],
       "PUB-0157": ["Gastos de hipoteca:", "¿cuánto tarda reclamar?"],
       "PUB-0163": ["Gastos de hipoteca:", "garantías y plazos"],
       "PUB-0160": ["¿Quieres reclamar tu vuelo?", "Por dónde empezar"],
       "PUB-0161": ["Reclamar tu vuelo:", "nos ocupamos de todo"],
       "PUB-0145": ["Lapurtutako dirua:", "noren ardura da?"],
       "PUB-0185": ["Mal tiempo: te ponen un bus.", "¿Puedes pedir el dinero?"]}
def ruta(v, clave, val):
    if not isinstance(val, str) or not val.startswith("/tmp/"): return val
    b = os.path.basename(val)
    if clave == "modelo": return OLD + "/video/sherpa-onnx-whisper-turbo"
    if clave == "vad": return OLD + "/video/silero_vad.onnx"
    if clave == "audio": return f"{M}/{v}.wav"
    if clave == "video": return f"{M}/src/{v}.pad.mp4" if (v in ("ps", "av") and "pad" in b) else f"{M}/src/{v}.mp4"
    return val
for v, (fs, ft) in FU.items():
    sp = json.load(open(fs, encoding="utf8")); ti = json.load(open(ft, encoding="utf8")); out_t = {}
    for k in list(sp):
        if k in ("video", "audio", "modelo", "vad"): sp[k] = ruta(v, k, sp[k])
    sp.pop("capas", None); sp.pop("desfase", None)
    if v == "av":
        sp["credito"] = "Imágenes: EITB"; sp["rotulos"]["espectador"] = sp["rotulos"]["espectador"].replace("  ·  EITB (2017)", "  ·  EITB")                     # Sergio, 7/10: «quita 2017»
    clips = []
    for c in sp["clips"]:
        if c["id"] not in QUIERO[v]: continue
        c = copy.deepcopy(c); w = copy.deepcopy(ti[c["id"]])
        for t in c["tramos"]:
            for k in ("video", "audio"):
                if k in t: t[k] = ruta(v, k, t[k])
        if c["id"] in TIT: c["titular"] = TIT[c["id"]]
        if c["id"] == "PUB-0135":                                     # fuera el tramo del ertzaina
            c["tramos"] = c["tramos"][:3]; w = [x for x in w if x["tramo"] < 3]; c["recortes"] = [r for r in c["recortes"] if r[0] < 138.7]
        if c["id"] == "PUB-0144":                                     # la presentadora termina «ciberestafas»
            c["tramos"][0]["fin"] = 8.25
            for x in w:
                if x["tramo"] == 0 and x["p"].startswith("ciberestafas"): x["fin"] = 7.97
        if c["id"] == "PUB-0159":                                     # empieza en «¿Qué sectores…»
            t0 = c["tramos"][0]; i = t0["texto"].index("¿qué sectores"); t0["texto"] = "¿Qué" + t0["texto"][i + 4:]; t0["inicio"] = 170.44
            k = next(n for n, x in enumerate(w) if x["tramo"] == 0 and x["p"] == "¿qué"); w = w[k:]; w[0]["p"] = "¿Qué"; w[0]["ini"] = 170.5
            c["recortes"] = [[170.44] + c["recortes"][0][1:]] + c["recortes"][1:]
        if c["id"] == "PUB-0196":                                     # el primer plano era el final del anterior: se congela el del pasajero hasta que entra
            t0 = c["tramos"][0]; D = 404.62; t0["video"] = M + "/src/qa196.mp4"; t0["recortes"] = [[0.0, 162, 0, 700]]
            fin = t0["fin"] - D; t0["inicio"] = 0.0; t0["fin"] = round(fin, 2); t0.pop("enc", None)
            for x in w:
                if x["tramo"] == 0: x["ini"] = round(max(0.05, x["ini"] - D), 2); x["fin"] = round(max(0.1, x["fin"] - D), 2)
            c["recortes"] = [r for r in c["recortes"] if r[0] > 410]
        if c["id"] == "PUB-0185":                                     # la respuesta no quedaba a medias: dos reconocedores oyen «…que te permitirían por ley»
            t1 = c["tramos"][1]; assert t1["texto"].endswith("posibilidades que…"); t1["texto"] = t1["texto"][:-1] + " te permitirían por ley."
            k = max(n for n, x in enumerate(w) if x["tramo"] == 1); w[k]["p"] = "que"; w[k]["ini"] = 81.64; w[k]["fin"] = 81.72
            w[k + 1:k + 1] = [{"p": "te", "ini": 81.72, "fin": 81.88, "tramo": 1}, {"p": "permitirían", "ini": 81.88, "fin": 82.44, "tramo": 1},
                              {"p": "por", "ini": 82.44, "fin": 82.6, "tramo": 1}, {"p": "ley.", "ini": 82.6, "fin": 82.84, "tramo": 1}]
            w[k - 1]["fin"] = 81.64
        clips.append(c); out_t[c["id"]] = w
    sp["clips"] = clips
    json.dump(sp, open(f"{M}/spec-{v}.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
    json.dump(out_t, open(f"{M}/spec-{v}.tiempos.json", "w", encoding="utf8"), ensure_ascii=False, indent=0)
    print(v, [c["id"] for c in clips], sp["video"], os.path.exists(sp["video"]), sp.get("credito"))
