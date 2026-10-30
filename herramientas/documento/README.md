# «El documento, subrayado»

`documento.py` monta un vídeo vertical a partir de un caso real del despacho: un fragmento de la sentencia con los datos personales tapados, la frase clave subrayada y copiada en grande, el resultado, un consejo y el cierre de marca. Usa piezas de `../comics/comic.py` (voz, subtítulos, música, cierre).

- **Las sentencias NO se suben nunca a este repositorio, que es público.** Están en el Mac de Sergio, en `Documentos/LANA/Erreklamatu/Marketing/Magnific/sentencias/`, como `sentencia-D1.pdf`, `sentencia-D2.pdf`, etc. El nombre original está en esa misma carpeta. Para producir, se traen al contenedor (variable `SENTENCIAS`). El vídeo solo usa el fragmento ya anonimizado.
- **Anonimización:** solo se usa la columna del texto, porque el margen lleva las firmas y el CSV. Se tapan las palabras de `ocultar` y los patrones de `SENSIBLE` (fechas, números largos, DNI y NIE, CSV, NIG). Antes de dar una pieza por buena, revisa siempre `fragmento-previa.png` y la lista de palabras tapadas que imprime el script.
- **Actualidad sin fingir:** ni fechas ni «nueva sentencia». La actualidad la ponen el consejo (por ejemplo, el plazo de 5 años) y el gancho en presente.
- **OCR:** tesseract con el modelo de castellano `spa.traineddata` (tessdata_fast, en GitHub). Se descarga en `/tmp/tess` y se pasa como `TESSDATA`.
- **Cita:** el texto de `cita` se copia literalmente de la sentencia, incluidos sus errores (por ejemplo, «mas» sin tilde).

## Versión 2 (29/10/2026, validada por Sergio en PUB-0520)
- Cada tramo lleva un vídeo de archivo de fondo (carpeta `Magnific/stock` del Mac; procedencia en `recursos/stock/FUENTES.md`). Tipos de tramo: `gancho`, `doc`, `lista`, `consejo`; modo `lleno` o `marco` (apaisado en recuadro sobre copia desenfocada).
- Arranque: titular que se entiende solo (`titulo`), etiqueta «UN CASO REAL».
- La sentencia solo entra cuando se subraya (`doc_entra`), con el rótulo «Sentencia del <juzgado> · <fecha>». Nada de «datos personales ocultos» en pantalla ni en el pie.
- El recorte se ajusta solo a líneas completas.
- Estilo de marca: Poppins Bold, #003378 y #00E887, etiquetas en mayúsculas con espaciado .2em. Única excepción: la cita literal en Lora redonda (serif), solo para texto literal de sentencias.
- Comando: `python3 documento.py todo specs/Dn.json carpeta` (con `STOCK` y `SENTENCIAS` apuntando a las copias de la carpeta del Mac).

## Versión 3 (30/10/2026, correcciones de Sergio a PUB-0518, 0519 y 0521; valen para todos los vídeos de sentencias)
- **Arranque fuerte:** lo más noticioso del caso (lo que destaca la nota de prensa o, si no, la sentencia) va en los 2-3 primeros segundos, en la voz y en el titular. En cada caso se elige bien qué es lo noticioso (p. ej., el total y no solo una partida).
- **La sentencia, protagonista:** 2-3 pasajes de la sentencia (qué alegó la otra parte, cómo lo rebatió el juez, algún dato llamativo), cada uno con su locución. Nunca una frase seguida de un silencio. Cada tramo `doc` puede llevar su propio `pagina_num`, `subrayar`, `margen` y `cita` (fragmentos `fragmento-NN.png`).
- **Lo conseguido, partida a partida y presentado:** «Esto es lo que X tendrá que pagarles:», con intereses y costas. Nada de «además de la compensación…».
- **Miniatura:** titular descriptivo con sujeto y dato; foto a sangre ligada al caso (`portada_stock`, `portada_desde`, `portada_foto_y`); abajo, el dato clave (`portada_dato`), sin huecos vacíos.
- **Imágenes de recurso:** centradas en la zona visible, ligadas a lo que dice la locución en cada momento; personas de la edad del caso (si son menores, adolescentes) y con aspecto local; IA solo si no se nota.
- **Audio:** sin silencios largos ni ruidos sueltos; escuchar cada locución antes de montar.
- **Textos de los posts:** siempre con sujeto («dos aficionados del Athletic de la Margen Izquierda», «una clienta del Santander»).

## Limpieza de la voz (30/10/2026)
`voz()` pasa primero cada locución por `sin_ruiditos()`: quita tramos con sonido de menos de 0,14 s rodeados de silencio (respiraciones, chasquidos). Corrección de Sergio a PUB-0519: «un suspiro, un ruidito que se ha escapado». Imprime en qué segundo quitó algo. No sustituye a escuchar la pieza antes de aprobar.

## Imágenes de archivo recortadas (30/10/2026)
Un vídeo vertical cuyo motivo está arriba (p. ej. `adolescentes-aeropuerto-cenital_8190935`) se recorta con ffmpeg (`crop=720:430:0:0`) a un archivo `…-arriba_…mp4` en la carpeta STOCK y se usa en modo «marco», para que el titular no tape las caras.
