# Silencios (pausas) de un wav en una ventana.  python3 sil.py tv 14 20 [minimo]
import soundfile as sf, numpy as np, sys
v=sys.argv[1]; a,sr=sf.read('/tmp/claude-0/-home-user-erreklamatu-rrss/35d0557c-8694-51f8-b5cc-84a0f9e75554/scratchpad/radio2/src/'+v+'.wav',dtype='float32')
def huecos(t0,t1,minimo=0.14):
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
args=sys.argv[2:]; m=0.14
if len(args)%2: m=float(args[-1]); args=args[:-1]
for k in range(0,len(args),2):
    t0,t1=float(args[k]),float(args[k+1]); print(f"{v} {t0}-{t1}:", " ".join(f"[{p:.2f}-{q:.2f}]" for p,q in huecos(t0,t1,m)))
