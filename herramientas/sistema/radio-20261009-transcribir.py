# python3 transcribir.py idioma r1 r2 ...  -> aud/<k>.txt con líneas [ini- fin] texto (whisper turbo, VAD silero)
import sys, os, sherpa_onnx, soundfile as sf
R="/tmp/claude-0/-home-user-erreklamatu-rrss/35d0557c-8694-51f8-b5cc-84a0f9e75554/scratchpad/radio2"
lang=sys.argv[1]; d=R+"/video/sherpa-onnx-whisper-turbo/"
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=d+'turbo-encoder.int8.onnx',decoder=d+'turbo-decoder.int8.onnx',tokens=d+'turbo-tokens.txt',language=lang,task='transcribe',num_threads=4)
os.makedirs(R+"/aud",exist_ok=True)
for k in sys.argv[2:]:
    a,sr=sf.read(f"{R}/src/{k}.wav",dtype="float32")
    cfg=sherpa_onnx.VadModelConfig(); cfg.silero_vad.model=R+"/video/silero_vad.onnx"; cfg.silero_vad.min_silence_duration=0.35
    cfg.silero_vad.min_speech_duration=0.25; cfg.silero_vad.threshold=0.45; cfg.silero_vad.max_speech_duration=18; cfg.sample_rate=sr
    vad=sherpa_onnx.VoiceActivityDetector(cfg,buffer_size_in_seconds=2000); ws=cfg.silero_vad.window_size; segs=[]; i=0
    def vaciar():
        while not vad.empty():
            g=vad.front; segs.append((g.start,g.start+len(g.samples))); vad.pop()
    while i+ws<=len(a): vad.accept_waveform(a[i:i+ws]); i+=ws; vaciar()
    vad.flush(); vaciar()
    # whisper procesa siempre ventanas de 30 s: se juntan segmentos seguidos hasta 26 s para no pagar 30 s por cada frase corta
    jun=[]
    for g0,g1 in segs:
        if jun and g1-jun[-1][0] <= 26*sr: jun[-1]=(jun[-1][0],g1)
        else: jun.append((g0,g1))
    out=open(f"{R}/aud/{k}.txt","w")
    for g0,g1 in jun:
        p0=max(0,g0-int(0.1*sr)); p1=min(len(a),g1+int(0.1*sr))
        st=rec.create_stream(); st.accept_waveform(sr,a[p0:p1]); rec.decode_stream(st)
        out.write(f"[{g0/sr:7.2f}-{g1/sr:7.2f}] {st.result.text.strip()}\n"); out.flush()
    out.close(); print("hecho",k,flush=True)
