# Rutas pensadas para la carpeta de trabajo del vídeo: modelo y detector de voz en la carpeta superior, wav junto al script.
import sherpa_onnx, soundfile as sf, numpy as np, sys, json
d='../sherpa-onnx-whisper-turbo/'
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=d+'turbo-encoder.int8.onnx',decoder=d+'turbo-decoder.int8.onnx',tokens=d+'turbo-tokens.txt',language='es',task='transcribe',num_threads=2)
def huecos(a,sr,t0,t1,minimo=0.09):
    x=a[int(t0*sr):int(t1*sr)]; fr=int(0.01*sr); e=np.array([np.sqrt((x[i:i+fr]**2).mean()) for i in range(0,len(x)-fr,fr)])
    thr=max(np.percentile(e,15)*1.6, e.max()*0.035); bajo=e<thr; out=[]; i=0
    while i<len(bajo):
        if bajo[i]:
            j=i
            while j<len(bajo) and bajo[j]: j+=1
            if (j-i)*0.01>=minimo: out.append((round(t0+i*0.01,2),round(t0+j*0.01,2)))
            i=j
        else: i+=1
    return out
def asr(a,sr,t0,t1):
    st=rec.create_stream(); st.accept_waveform(sr,a[int(t0*sr):int(t1*sr)]); rec.decode_stream(st); return st.result.text.strip()
Q=json.loads(sys.argv[1])
for v,wins in Q.items():
    a,sr=sf.read(v+'.wav',dtype='float32')
    for (t0,t1) in wins:
        hs=huecos(a,sr,t0,t1); cortes=[t0]+[round((h[0]+h[1])/2,2) for h in hs]+[t1]
        print(f"## {v} {t0}-{t1}  huecos:",hs,flush=True)
        for p,q in zip(cortes,cortes[1:]):
            if q-p>0.25: print(f"   {p:7.2f}-{q:7.2f}  {asr(a,sr,p,q)}",flush=True)
