# Oye los clips ya montados (modelo Parakeet, o Whisper con «w») y compara con el guion: palabras que faltan o sobran, sobre todo en los cortes.
# python3 chkout.py [w] PUB-0228 PUB-0229 ...
import sys, json, subprocess, difflib, re, unicodedata, glob, sherpa_onnx, soundfile as sf
S = "/tmp/claude-0/-home-claude/e7eefa61-a30f-57c7-bc2e-7996fd2458cc/scratchpad"
args = sys.argv[1:]; W = args and args[0] == "w"; ids = args[1:] if W else args
if W:
    d = S + "/video/sherpa-onnx-whisper-turbo/"
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=d+'turbo-encoder.int8.onnx', decoder=d+'turbo-decoder.int8.onnx', tokens=d+'turbo-tokens.txt', language='es', task='transcribe', num_threads=2)
else:
    d = glob.glob("/tmp/claude-0/-home-claude-erreklamatu-rrss/e7eefa61-a30f-57c7-bc2e-7996fd2458cc/scratchpad/pk/sherpa-onnx-nemo-parakeet*/")[0]
    rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=d+'encoder.int8.onnx', decoder=d+'decoder.int8.onnx', joiner=d+'joiner.int8.onnx', tokens=d+'tokens.txt', model_type='nemo_transducer', num_threads=2)
def norm(p):
    p = unicodedata.normalize("NFD", p.lower()); return re.sub(r"[^a-z0-9ñ]", "", "".join(c for c in p if unicodedata.category(c) != "Mn" or c == "̃"))
import defs
for v, pid, k, tit, tramos, op in defs.C:
    if ids and pid not in ids: continue
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"out/{pid}.mp4", "-ac", "1", "-ar", "16000", f"chk/{pid}.wav"], check=True)
    a, sr = sf.read(f"chk/{pid}.wav", dtype="float32"); fin = len(a) / sr - 2.6; txt = []; p = 0.0
    x = a[:int(fin * sr)]; cfg = sherpa_onnx.VadModelConfig(); cfg.silero_vad.model = S + "/video/silero_vad.onnx"; cfg.silero_vad.min_silence_duration = 0.3
    cfg.silero_vad.min_speech_duration = 0.2; cfg.silero_vad.threshold = 0.4; cfg.silero_vad.max_speech_duration = 12; cfg.sample_rate = sr
    vad = sherpa_onnx.VoiceActivityDetector(cfg, buffer_size_in_seconds=120); ws = cfg.silero_vad.window_size; segs = []; i = 0
    def vaciar():
        while not vad.empty():
            g = vad.front; segs.append((g.start, g.start + len(g.samples))); vad.pop()
    while i + ws <= len(x): vad.accept_waveform(x[i:i+ws]); i += ws; vaciar()
    vad.flush(); vaciar()
    for g0, g1 in segs:
        g0 = max(0, g0 - int(0.15 * sr)); g1 = min(len(x), g1 + int(0.15 * sr))
        st = rec.create_stream(); st.accept_waveform(sr, x[g0:g1]); rec.decode_stream(st); txt.append(st.result.text.strip())
    oi = " ".join(txt).split(); ref = " ".join(t[3] for t in tramos).split()
    on = [norm(w) for w in oi]; rn = [norm(w) for w in ref]; keep_o = [i for i, w in enumerate(on) if w]; keep_r = [i for i, w in enumerate(rn) if w]
    sm = difflib.SequenceMatcher(None, [rn[i] for i in keep_r], [on[i] for i in keep_o], autojunk=False)
    print(f"## {pid} {fin:.1f} s  parecido {sm.ratio():.2f}", flush=True)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal": continue
        R = " ".join(ref[keep_r[i]] for i in range(i1, i2)); O = " ".join(oi[keep_o[j]] for j in range(j1, j2))
        ctx = " ".join(ref[keep_r[i]] for i in range(max(0, i1 - 3), i1))
        print(f"   …{ctx} [guion: {R or '—'}] [oído: {O or '—'}]")
    # arranque y final
    st = rec.create_stream(); st.accept_waveform(sr, a[0:int(3.5*sr)]); rec.decode_stream(st); ini = st.result.text.strip()
    st = rec.create_stream(); st.accept_waveform(sr, a[int(max(0, fin - 3.5)*sr):int((fin + 0.4)*sr)]); rec.decode_stream(st)
    print(f"   arranque: «{ini}» | final: «{st.result.text.strip()}»", flush=True)
