# Palabras con su segundo de un audio entero (Parakeet TDT v3, castellano): python3 pk_tr.py r9 r1 ... -> aud/<k>.pk.json y aud/<k>.pk.txt
import sys, glob, json, sherpa_onnx, soundfile as sf
R="/tmp/claude-0/-home-user-erreklamatu-rrss/35d0557c-8694-51f8-b5cc-84a0f9e75554/scratchpad/radio2"
d=glob.glob(R+"/video/sherpa-onnx-nemo-parakeet*/")[0]
rec=sherpa_onnx.OfflineRecognizer.from_transducer(encoder=d+'encoder.int8.onnx',decoder=d+'decoder.int8.onnx',joiner=d+'joiner.int8.onnx',tokens=d+'tokens.txt',model_type='nemo_transducer',num_threads=2)
for k in sys.argv[1:]:
    a,sr=sf.read(f"{R}/src/{k}.wav",dtype="float32")
    cfg=sherpa_onnx.VadModelConfig(); cfg.silero_vad.model=R+"/video/silero_vad.onnx"; cfg.silero_vad.min_silence_duration=0.3
    cfg.silero_vad.min_speech_duration=0.25; cfg.silero_vad.threshold=0.45; cfg.silero_vad.max_speech_duration=20; cfg.sample_rate=sr
    vad=sherpa_onnx.VoiceActivityDetector(cfg,buffer_size_in_seconds=2000); ws=cfg.silero_vad.window_size; segs=[]; i=0
    def vaciar():
        while not vad.empty():
            g=vad.front; segs.append((g.start,g.start+len(g.samples))); vad.pop()
    while i+ws<=len(a): vad.accept_waveform(a[i:i+ws]); i+=ws; vaciar()
    vad.flush(); vaciar(); pal=[]; out=open(f"{R}/aud/{k}.pk.txt","w")
    for g0,g1 in segs:
        p0=max(0,g0-int(0.1*sr)); p1=min(len(a),g1+int(0.1*sr))
        st=rec.create_stream(); st.accept_waveform(sr,a[p0:p1]); rec.decode_stream(st); r=st.result; ws_=[]
        for tok,t in zip(r.tokens,r.timestamps):
            if tok.startswith(" ") or not ws_: ws_.append([tok.strip(),p0/sr+t])
            else: ws_[-1][0]+=tok
        pal+=ws_; out.write(f"[{g0/sr:7.2f}-{g1/sr:7.2f}] "+" ".join(f"{w}@{t:.1f}" for w,t in ws_)+"\n")
    json.dump([[w,round(t,2)] for w,t in pal],open(f"{R}/aud/{k}.pk.json","w"),ensure_ascii=False); print("hecho",k,flush=True)
