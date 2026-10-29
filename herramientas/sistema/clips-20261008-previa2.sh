# Copias ligeras (720 × 1280) de los clips indicados; salta las que ya existen y son más nuevas que el clip.  bash previa2.sh PUB-0246 ...
for p in "$@"; do f=out/$p.mp4; d=previa/$p-previa.mp4
  [ -f "$f" ] || { echo "falta $f" >> previa.log; continue; }
  [ -f "$d" ] && [ "$d" -nt "$f" ] && continue
  nice -n 10 ffmpeg -v error -y -i $f -vf scale=720:1280 -c:v libx264 -preset medium -crf 28 -pix_fmt yuv420p -c:a aac -b:a 64k -movflags +faststart previa/$p-previa.tmp.mp4 && mv previa/$p-previa.tmp.mp4 $d && echo "ok $p $(date +%H:%M:%S)" >> previa.log
done; echo "PREVIA_FIN $(date +%H:%M:%S)" >> previa.log
