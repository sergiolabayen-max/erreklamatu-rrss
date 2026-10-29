#!/bin/bash
# Copia ligera para el centro de control: 720 x 1280, crf 28. El archivo que se publica (1080 x 1920) sigue en GitHub.
cd "$(dirname "$0")"
for f in out/PUB-*.mp4; do p=$(basename $f .mp4); [ -s previa/$p-previa.mp4 ] && continue
  ffmpeg -v error -y -i $f -vf scale=720:1280 -c:v libx264 -preset medium -crf 28 -pix_fmt yuv420p -c:a aac -b:a 64k -movflags +faststart previa/$p-previa.tmp.mp4 && mv previa/$p-previa.tmp.mp4 previa/$p-previa.mp4
done; echo PREVIA_OK > previa.log
