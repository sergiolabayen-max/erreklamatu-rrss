#!/bin/bash
# Prepara los vídeos de archivo de D11-D15 (3/11/2026): ralentiza los clips cortos y monta planos combinados
# para que ningún tramo quede estático ni se repita en bucle (criterio de Sergio, PUB-0525).
# Uso: STOCK=<carpeta Magnific/stock> bash prep_stock_20261103b.sh
set -e; cd "$STOCK"
lento(){ ffmpeg -v error -y -i "$1" -vf "setpts=PTS/$3,minterpolate=fps=30:mi_mode=blend,scale=1280:720:flags=lanczos" -an -c:v libx264 -crf 17 -pix_fmt yuv420p "$2"; }
corte(){ ffmpeg -v error -y -ss "$2" -t "$3" -i "$1" -vf "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30,format=yuv420p" -an -c:v libx264 -crf 17 "$4"; }
mont(){ out=$1; shift; lst=$(mktemp); for f in "$@"; do echo "file '$PWD/$f'" >> $lst; done; ffmpeg -v error -y -f concat -safe 0 -i $lst -c copy "$out"; rm $lst; }
lento madre-bebe-avion_3030775.mp4 madre-bebe-avion-lenta_3030775.mp4 0.7
lento maleta-maletero-aeropuerto_2971254.mp4 maleta-maletero-aeropuerto-lenta_2971254.mp4 0.55
lento hombre-agobiado-movil-terminal_10225718.mp4 hombre-agobiado-movil-terminal-lenta_10225718.mp4 0.5
lento mostrador-facturacion-pasaporte_2744563.mp4 mostrador-facturacion-pasaporte-lenta_2744563.mp4 0.85
# D11 (bebé): gancho bebé 5 s + madre y bebé en el avión 5,5 s · sentencia 1: maleta 6 s + bebé 6 s · sentencia 2: madre y bebé 5 s + bebé 4,4 s
corte bebe-mochila-aeropuerto_3036639.mp4 0 5 _a.mp4; corte madre-bebe-avion-lenta_3030775.mp4 0 5.5 _b.mp4; mont D11-montaje-gancho.mp4 _a.mp4 _b.mp4
corte maleta-maletero-aeropuerto-lenta_2971254.mp4 0 6 _c.mp4; corte bebe-mochila-aeropuerto_3036639.mp4 6 6 _d.mp4; mont D11-montaje-sentencia.mp4 _c.mp4 _d.mp4
corte madre-bebe-avion-lenta_3030775.mp4 5.5 5.2 _e.mp4; corte bebe-mochila-aeropuerto_3036639.mp4 11.9 4.4 _f.mp4; mont D11-montaje-sentencia2.mp4 _e.mp4 _f.mp4
# D12 (Miami): Miami 6 s + madre e hija dormidas 6,5 s
corte miami-dron_5026772.mp4 0 6 _g.mp4; corte madre-nina-dormidas-terminal_56937.mp4 0 6.5 _h.mp4; mont D12-montaje-gancho.mp4 _g.mp4 _h.mp4
# D13 (Lufthansa): Múnich 5 s + hombre agobiado 6 s + hombre ante el ventanal 2,8 s
corte munich-dron_690454.mp4 0 5 _i.mp4; corte hombre-agobiado-movil-terminal_10225718.mp4 0 6 _j.mp4; corte hombre-movil-ventanal-aeropuerto_4960694.mp4 0 2.8 _k.mp4; mont D13-montaje-gancho.mp4 _i.mp4 _j.mp4 _k.mp4
# D14 (Air Canada) consejo: hombre en la sala de espera 6,5 s + Montreal 6,5 s
corte hombre-gafas-movil-sala-espera_4874054.mp4 20 6.5 _l.mp4; corte montreal-dron_5770753.mp4 32 6.5 _m.mp4; mont D14-montaje-consejo.mp4 _l.mp4 _m.mp4
# D15 (Bangkok): Bangkok 5 s + mujer ante la cinta 6 s
corte bangkok-dron_29199.mp4 0 5 _n.mp4; corte mujer-cinta-equipajes_5951.mp4 0 6 _o.mp4; mont D15-montaje-gancho.mp4 _n.mp4 _o.mp4
rm -f _?.mp4; for f in D1[1-5]-montaje*.mp4 *-lenta_{3030775,2971254,10225718,2744563}.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)"; done
