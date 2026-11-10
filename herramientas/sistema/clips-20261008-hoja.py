# Hoja de fotogramas de clips montados: python3 hoja.py salida.jpg id [id...]  (un fotograma cada n segundos, con el segundo anotado)
import sys, subprocess, os, json
from PIL import Image, ImageDraw
out=sys.argv[1]; ids=sys.argv[2:]; th=[]
for pid in ids:
    f=f"out/{pid}.mp4"; d=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]).decode())
    n=max(4,min(10,int(d/4))); ts=[0.6]+[d*(i+0.5)/n for i in range(1,n-1)]+[d-3.1, d-0.5]
    for t in ts:
        raw=subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.2f}","-i",f,"-frames:v","1","-vf","crop=1080:1200:0:250,scale=270:300","-f","image2pipe","-vcodec","png","-"],capture_output=True).stdout
        import io; im=Image.open(io.BytesIO(raw)).convert("RGB"); ImageDraw.Draw(im).rectangle([0,286,270,300],fill=(0,0,0)); ImageDraw.Draw(im).text((4,287),f"{pid[-4:]} {t:.1f}s de {d:.0f}",fill=(255,255,0)); th.append(im)
cols=10; rows=(len(th)+cols-1)//cols; sh=Image.new("RGB",(cols*272,rows*302),(30,30,30))
for i,im in enumerate(th): sh.paste(im,((i%cols)*272,(i//cols)*302))
sh.save(out,quality=88); print(sh.size,len(th))
