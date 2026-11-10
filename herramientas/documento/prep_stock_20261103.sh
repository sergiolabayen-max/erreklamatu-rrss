#!/bin/bash
# Prepara los vídeos de archivo del 3/11/2026 (D5 revisado, D7-D10): ralentiza los clips cortos para que no se repitan en bucle,
# voltea el del coche (volante a la derecha) y monta planos combinados para que un tramo largo no quede estático (criterio de Sergio, PUB-0525).
# Uso: STOCK=<carpeta Magnific/stock> bash prep_stock_20261103.sh
set -e; cd "$STOCK"
lento(){ ffmpeg -v error -y -i "$1" -vf "setpts=PTS/$3,${4:+$4,}minterpolate=fps=30:mi_mode=blend,scale=1280:720:flags=lanczos" -an -c:v libx264 -crf 17 -pix_fmt yuv420p "$2"; }
lento tranvia-lisboa_7396767.mp4 tranvia-lisboa-lenta_7396767.mp4 0.6
lento manga-viento-rachas_8889993.mp4 manga-viento-rachas-lenta_8889993.mp4 0.6
lento coche-asiento-trasero-autopista_9222585.mp4 coche-asiento-trasero-autopista-lenta-volteado_9222585.mp4 0.6 hflip
lento avion-despegando-atardecer_3036567.mp4 avion-despegando-atardecer-lenta_3036567.mp4 0.7
# corte(src, desde, duración, salida) a 1280x720 30 fps
corte(){ ffmpeg -v error -y -ss "$2" -t "$3" -i "$1" -vf "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30,format=yuv420p" -an -c:v libx264 -crf 17 "$4"; }
mont(){ out=$1; shift; lst=$(mktemp); for f in "$@"; do echo "file '$PWD/$f'" >> $lst; done; ffmpeg -v error -y -f concat -safe 0 -i $lst -c copy "$out"; rm $lst; }
# D5 (PUB-0525): grupo 4,5 s + ala sobre las nubes 7 s; luego despegue 6 s + grupo 5 s
corte grupo-jovenes-puerta-embarque-lenta-IA_3815513942.mp4 0 4.5 _a.mp4; corte ala-avion-nubes_8440916.mp4 3 7 _b.mp4; mont D5-montaje-gancho.mp4 _a.mp4 _b.mp4
corte avion-despegando-atardecer-lenta_3036567.mp4 0 6 _c.mp4; corte grupo-jovenes-puerta-embarque-lenta-IA_3815513942.mp4 4.5 5 _d.mp4; mont D5-montaje-sentencia.mp4 _c.mp4 _d.mp4
# D8 gancho: tranvía 4 s + aterrizaje 5 s · D9 gancho: manga 4 s + aviones en pista 5 s
corte tranvia-lisboa-lenta_7396767.mp4 0 4 _e.mp4; corte avion-aterrizando-ciudad_4215534.mp4 2 5 _f.mp4; mont D8-montaje-gancho.mp4 _e.mp4 _f.mp4
corte manga-viento-rachas-lenta_8889993.mp4 0 4 _g.mp4; corte aviones-rodando-pista_831579.mp4 10 5 _h.mp4  # 0-8 s: colas con logotipos; 32-38 s autopista; 40+ panel de Amtrak: no usar; mont D9-montaje-gancho.mp4 _g.mp4 _h.mp4
# D10 gancho: La Concha 5 s + coche 6 s
corte donostia-concha-dron_9592862.mp4 2 5 _i.mp4; corte coche-asiento-trasero-autopista-lenta-volteado_9222585.mp4 0 6 _j.mp4; mont D10-montaje-gancho.mp4 _i.mp4 _j.mp4
rm -f _?.mp4; ls -la *montaje* *lenta*_*.mp4
