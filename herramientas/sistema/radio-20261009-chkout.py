# Segunda lectura de los clips ya montados (como clips-20261008-chkout.py): oye el sonido del vídeo final y lo compara con el guion.
# Castellano: Parakeet TDT v3 (los tiempos de los subtítulos salieron de Parakeet sobre el audio original; aquí se vuelve a reconocer el clip montado,
# troceado de otra manera). Euskera: Omnilingual ASR 1B. Enseña palabras del guion que no se oyen y palabras oídas que no están, y el arranque y el final.
# python3 chkout.py [ids...]   (sin ids, todos los montados)
import sys, os, json, subprocess, difflib, re, unicodedata, glob, sherpa_onnx, soundfile as sf
R = "/tmp/claude-0/-home-user-erreklamatu-rrss/35d0557c-8694-51f8-b5cc-84a0f9e75554/scratchpad/radio2"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import defs
ids = sys.argv[1:]; os.makedirs("chk", exist_ok=True)
def norm(p):
    p = unicodedata.normalize("NFD", p.lower()); return re.sub(r"[^a-z0-9ñ]", "", "".join(c for c in p if unicodedata.category(c) != "Mn" or c == "̃"))
REC = {}
def rec(lang):
    if lang not in REC:
        if lang == "es":
            d = glob.glob(R + "/video/sherpa-onnx-nemo-parakeet*/")[0]
            REC[lang] = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=d+'encoder.int8.onnx', decoder=d+'decoder.int8.onnx', joiner=d+'joiner.int8.onnx', tokens=d+'tokens.txt', model_type='nemo_transducer', num_threads=2)
        else:
            d = glob.glob(R + "/video/sherpa-onnx-omnilingual*/")[0]
            REC[lang] = sherpa_onnx.OfflineRecognizer.from_omnilingual_asr_ctc(model=d + "model.int8.onnx", tokens=d + "tokens.txt", num_threads=2)
    return REC[lang]
res = {}
for k, cid, kicker, tit, tramos, op in defs.C:
    if ids and cid not in ids: continue
    if not os.path.exists(f"out/{cid}.mp4"): continue
    lang = defs.V[k]["idioma"]; r = rec(lang)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"out/{cid}.mp4", "-ac", "1", "-ar", "16000", f"chk/{cid}.wav"], check=True)
    a, sr = sf.read(f"chk/{cid}.wav", dtype="float32"); fin = len(a) / sr - 2.6
    cfg = sherpa_onnx.VadModelConfig(); cfg.silero_vad.model = R + "/video/silero_vad.onnx"; cfg.silero_vad.min_silence_duration = 0.3
    cfg.silero_vad.min_speech_duration = 0.2; cfg.silero_vad.threshold = 0.4; cfg.silero_vad.max_speech_duration = 15; cfg.sample_rate = sr
    vad = sherpa_onnx.VoiceActivityDetector(cfg, buffer_size_in_seconds=600); ws = cfg.silero_vad.window_size; segs = []; i = 0; x = a[:int(fin * sr)]
    def vaciar():
        while not vad.empty():
            g = vad.front; segs.append((g.start, g.start + len(g.samples))); vad.pop()
    while i + ws <= len(x): vad.accept_waveform(x[i:i+ws]); i += ws; vaciar()
    vad.flush(); vaciar(); txt = []
    for g0, g1 in segs:
        g0 = max(0, g0 - int(0.15 * sr)); g1 = min(len(x), g1 + int(0.15 * sr))
        st = r.create_stream(); st.accept_waveform(sr, x[g0:g1]); r.decode_stream(st); txt.append(st.result.text.strip())
    oi = " ".join(txt).split(); ref = " ".join(t[3] for t in tramos).split()
    on = [norm(w) for w in oi]; rn = [norm(w) for w in ref]; ko = [i for i, w in enumerate(on) if w]; kr = [i for i, w in enumerate(rn) if w]
    sm = difflib.SequenceMatcher(None, [rn[i] for i in kr], [on[i] for i in ko], autojunk=False)
    out = [f"## {cid} {fin:.1f} s  parecido {sm.ratio():.2f}"]
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal": continue
        Rr = " ".join(ref[kr[i]] for i in range(i1, i2)); O = " ".join(oi[ko[j]] for j in range(j1, j2))
        ctx = " ".join(ref[kr[i]] for i in range(max(0, i1 - 3), i1))
        out.append(f"   …{ctx} [guion: {Rr or '—'}] [oído: {O or '—'}]")
    st = r.create_stream(); st.accept_waveform(sr, a[0:int(3.5 * sr)]); r.decode_stream(st); ini = st.result.text.strip()
    st = r.create_stream(); st.accept_waveform(sr, a[int(max(0, fin - 3.5) * sr):int((fin + 0.4) * sr)]); r.decode_stream(st)
    out.append(f"   arranque: «{ini}» | final: «{st.result.text.strip()}»")
    print("\n".join(out), flush=True); res[cid] = dict(parecido=round(sm.ratio(), 2), texto="\n".join(out))
    os.remove(f"chk/{cid}.wav")
prev = json.load(open("chkout.json")) if os.path.exists("chkout.json") else {}
prev.update(res); json.dump(prev, open("chkout.json", "w"), ensure_ascii=False, indent=1)
