import json,re,subprocess,os
from PIL import Image
sp=json.load(open('specs-carrusel-video.json'))[0]
def palabras(s):
    t=" ".join(str(v) for k,v in s.items() if k not in("tipo","num","ref") for v in (v if isinstance(v,list) else [v]))
    t=re.sub(r"[\*\[\]',]"," ",t); return len(t.split())
os.makedirs('vid',exist_ok=True); lst=[]; durs=[]
for i,s in enumerate(sp['slides'],1):
    f=f'outv/PUB-0306-x.png' if i==1 else f'outv/PUB-0306-{i:02d}.png'
    im=Image.open(f).convert('RGB'); bg=im.getpixel((5,5)) if i>1 else im.getpixel((5,5))
    C=Image.new('RGB',(1080,1920),bg); C.paste(im,(0,285)); C.save(f'vid/{i:02d}.png')
    d=round(0.6+palabras(s)/4.3,2); durs.append(d); lst.append((f'vid/{i:02d}.png',d))
tot=sum(durs); print(durs,tot)
subprocess.run(['python3','sintonia.py','vid/m.wav',str(tot),'viva',str(durs[-1])],check=True)
with open('vid/l.txt','w') as F:
    for f,d in lst: F.write(f"file '{os.path.abspath(f)}'\nduration {d}\n")
    F.write(f"file '{os.path.abspath(lst[-1][0])}'\n")
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i','vid/l.txt','-i','vid/m.wav','-vf','fps=30,format=yuv420p','-c:v','libx264','-crf','20','-c:a','aac','-b:a','128k','-t',str(tot),'-movflags','+faststart','out/PUB-0306-video.mp4'],check=True)
print('ok')
