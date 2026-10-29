# «El documento, subrayado»

`documento.py` monta un vídeo vertical a partir de un caso real del despacho: un fragmento de la sentencia con los datos personales tapados, la frase clave subrayada y copiada en grande, el resultado, un consejo y el cierre de marca. Usa piezas de `../comics/comic.py` (voz, subtítulos, música, cierre).

- **Las sentencias NO se suben nunca a este repositorio, que es público.** Están en el Mac de Sergio, en `Documentos/LANA/Erreklamatu/Marketing/Magnific/sentencias/`, como `sentencia-D1.pdf`, `sentencia-D2.pdf`, etc. El nombre original está en esa misma carpeta. Para producir, se traen al contenedor (variable `SENTENCIAS`). El vídeo solo usa el fragmento ya anonimizado.
- **Anonimización:** solo se usa la columna del texto, porque el margen lleva las firmas y el CSV. Se tapan las palabras de `ocultar` y los patrones de `SENSIBLE` (fechas, números largos, DNI y NIE, CSV, NIG). Antes de dar una pieza por buena, revisa siempre `fragmento-previa.png` y la lista de palabras tapadas que imprime el script.
- **Actualidad sin fingir:** ni fechas ni «nueva sentencia». La actualidad la ponen el consejo (por ejemplo, el plazo de 5 años) y el gancho en presente.
- **OCR:** tesseract con el modelo de castellano `spa.traineddata` (tessdata_fast, en GitHub). Se descarga en `/tmp/tess` y se pasa como `TESSDATA`.
- **Cita:** el texto de `cita` se copia literalmente de la sentencia, incluidos sus errores (por ejemplo, «mas» sin tilde).
