# python3 omni_tr.py r12 r6 ... -> aud/<k>.txt (texto por trozos) y aud/<k>.palabras.json ([palabra, ini, fin]) con Omnilingual ASR 1B (CTC)
import sys, glob, json, sherpa_onnx, soundfile as sf
R="/tmp/claude-0/-home-user-erreklamatu-rrss/35d0557c-8694-51f8-b5cc-84a0f9e75554/scratchpad/radio2"
d=glob.glob(R+"/video/sherpa-onnx-omnilingual*/")[0]
rec=sherpa_onnx.OfflineRecognizer.from_omnilingual_asr_ctc(model=d+"model.int8.onnx",tokens=d+"tokens.txt",num_threads=int(sys.argv[1]))
for k in sys.argv[2:]:
    a,sr=sf.read(f"{R}/src/{k}.wav",dtype="float32")
    cfg=sherpa_onnx.VadModelConfig(); cfg.silero_vad.model=R+"/video/silero_vad.onnx"; cfg.silero_vad.min_silence_duration=0.3
    cfg.silero_vad.min_speech_duration=0.25; cfg.silero_vad.threshold=0.45; cfg.silero_vad.max_speech_duration=20; cfg.sample_rate=sr
    vad=sherpa_onnx.VoiceActivityDetector(cfg,buffer_size_in_seconds=2000); ws=cfg.silero_vad.window_size; segs=[]; i=0
    def vaciar():
        while not vad.empty():
            g=vad.front; segs.append((g.start,g.start+len(g.samples))); vad.pop()
    while i+ws<=len(a): vad.accept_waveform(a[i:i+ws]); i+=ws; vaciar()
    vad.flush(); vaciar()
    jun=[]
    for g0,g1 in segs:
        if jun and g1-jun[-1][0] <= 20*sr and g0-jun[-1][1] < 1.0*sr: jun[-1]=(jun[-1][0],g1)
        else: jun.append((g0,g1))
    out=open(f"{R}/aud/{k}.txt","w"); pal=[]
    for g0,g1 in jun:
        p0=max(0,g0-int(0.1*sr)); p1=min(len(a),g1+int(0.1*sr))
        st=rec.create_stream(); st.accept_waveform(sr,a[p0:p1]); rec.decode_stream(st); r=st.result
        out.write(f"[{g0/sr:7.2f}-{g1/sr:7.2f}] {r.text.strip()}\n"); out.flush()
        toks=list(r.tokens); tss=list(r.timestamps); cur=None
        for tk,t in zip(toks,tss):
            t=p0/sr+t
            if tk.strip()=="" or tk=="▁":
                if cur and cur[0]: pal.append(cur)
                cur=None; continue
            if tk.startswith("▁") and cur:
                if cur[0]: pal.append(cur)
                cur=None
            if cur is None: cur=[tk.replace("▁",""),t,t+0.08]
            else: cur[0]+=tk; cur[2]=t+0.08
        if cur and cur[0]: pal.append(cur)
    json.dump([[w,round(s,2),round(e,2)] for w,s,e in pal],open(f"{R}/aud/{k}.palabras.json","w"),ensure_ascii=False)
    out.close(); print("hecho",k,flush=True)
