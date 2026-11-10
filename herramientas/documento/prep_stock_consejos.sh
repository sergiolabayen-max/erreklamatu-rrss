#!/bin/bash
# Prepara los vídeos de archivo de los vídeos de consejos (C1…). Uso: STOCK=<carpeta Magnific/stock> bash prep_stock_consejos.sh
set -e; cd "$STOCK"
lento(){ ffmpeg -v error -y ${4:+-ss $4 -t $5} -i "$1" -vf "setpts=PTS/$3,minterpolate=fps=30:mi_mode=blend,scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720" -an -c:v libx264 -crf 17 -pix_fmt yuv420p "$2"; }
corte(){ ffmpeg -v error -y -ss "$2" -t "$3" -i "$1" -vf "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30,format=yuv420p" -an -c:v libx264 -crf 17 "$4"; }
mont(){ out=$1; shift; lst=$(mktemp); for f in "$@"; do echo "file '$PWD/$f'" >> $lst; done; ffmpeg -v error -y -f concat -safe 0 -i $lst -c copy "$out"; rm $lst; }
# C1 · tarjeta de embarque (6 s, a 0,8×); panel de llegadas: solo 6-11 s, el tramo con «Arrived» (antes y después sale en coreano y chino), a 0,5×
lento tarjeta-embarque-pasaporte_9692863.mp4 tarjeta-embarque-pasaporte-lenta_9692863.mp4 0.8
lento panel-llegadas_3055336.mp4 panel-llegadas-arrived-lenta_3055336.mp4 0.5 6 5
# C1 · gastos: solo las manos pagando (4-7,3 s; antes y después se ve la cara de la clienta) + ticket saliendo de la impresora
corte mujer-pagando-tarjeta-cafe_2484186.mp4 4 3.3 _a.mp4; corte ticket-impresora_7668855.mp4 0 7.6 _b.mp4; mont C1-montaje-gastos.mp4 _a.mp4 _b.mp4
rm -f _?.mp4; for f in C1-montaje*.mp4 *-lenta_{9692863,3055336}.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)"; done
# C3 · pasarela: solo 0-5,8 s (al final entra la cola de un avión con librea reconocible), a 0,55×; persona con maleta a 0,8×
lento pasajeros-saliendo-pasarela_3548036.mp4 pasajeros-saliendo-pasarela-lenta_3548036.mp4 0.55 0 5.8
lento persona-andando-maleta_6112878.mp4 persona-andando-maleta-lenta_6112878.mp4 0.8
# C4 · zona de equipajes (6 s) a 0,7×; mano escribiendo (5 s) a 0,75×
lento zona-equipajes-mostradores_7387456.mp4 zona-equipajes-mostradores-lenta_7387456.mp4 0.7
lento mano-escribiendo-cuaderno_2425280.mp4 mano-escribiendo-cuaderno-lenta_2425280.mp4 0.75
for f in *-lenta_{3548036,6112878,7387456,2425280}.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)"; done
# Segunda pasada (voces más largas): café a 0,9×; persona con maleta a 0,65×; mano escribiendo a 0,6×; agente de viajes a 0,8× (C9 usa dos segmentos)
lento cafe-bolleria-mesa_5993996.mp4 cafe-bolleria-mesa-lenta_5993996.mp4 0.9
lento persona-andando-maleta_6112878.mp4 persona-andando-maleta-lenta_6112878.mp4 0.65
lento mano-escribiendo-cuaderno_2425280.mp4 mano-escribiendo-cuaderno-lenta_2425280.mp4 0.6
lento agente-viajes-pasaporte_8425923.mp4 agente-viajes-pasaporte-lenta_8425923.mp4 0.8
