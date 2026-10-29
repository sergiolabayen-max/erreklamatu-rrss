# Herramientas de producción de RRSS de Erreklamatu

Las herramientas viven aquí, en el repositorio, con su historial. Así se pueden volver a reproducir las piezas desde cualquier sesión. Los scripts que se escriban en carpetas temporales hay que traerlos aquí y hacer *commit* antes de dar la pieza por terminada. El 28/10/2026 nos encontramos con que las herramientas de montaje de los cómics de octubre se habían perdido; esta norma es para que no vuelva a pasar.

## Norma de archivo (Sergio, 28/10/2026: «ordena bien y archiva tus recursos»)

1. **Cada herramienta nueva o modificada** va a `herramientas/<familia>/`, con una cabecera que diga qué hace y cómo se usa.
2. **Cada lote de piezas** guarda su especificación (JSON) en `herramientas/<familia>/specs/` con fecha. Con eso y la herramienta, la pieza se puede volver a generar.
3. **Recursos externos** (imágenes de Magnific, audios, vídeo de archivo): el original va a `recursos/<tipo>/`, con su procedencia (herramienta, fecha, *prompt* o enlace) en `recursos/<tipo>/FUENTES.md`. Excepción: los vídeos de archivo de más de 50 MB; de esos se apunta el enlace y la ruta.
4. **Documentos de método y guiones**, en `formatos/`, y copia en el proyecto Erreklamatu de claude.ai.
5. **Al terminar cada sesión de producción:** *commit* y *push*. Si el push falla, se avisa a Sergio y no se da nada por terminado.
6. **El centro de control** (`sistema/` del artefacto) conserva una copia de trabajo. La fuente de verdad es este repositorio.

## Qué hay

### `sistema/`: copia del centro de control (28/10/2026)
| Familia | Archivos | Para qué |
|---|---|---|
| Imágenes e infografías | `render.py`, `render-bloque.py` | PNG de marca a partir de un JSON |
| Carruseles | `carrusel.py`, `carrusel_talla.py`, `carrusel-a-video.py` | Láminas 1080 × 1350 y su versión en vídeo |
| Clips de TV | `video_clips.py`, `video_marco.py`, `video_encuadre.py`, `video_recortes.py`, `video_cortes.py`, `video_pildora.py`, `video_previa*.{py,sh}`, `tiempos_omni.py` | Montaje vertical, encuadre por zonas, subtítulos sincronizados |
| Audios de radio | `video_radio.py`, `audio_limpia.py`, `radio-20261009-*.py` | Clips verticales a partir de audio |
| Música | `sintonia.py` | Sintonía original generada por código («viva» o «tranquila») |
| Lotes concretos | `clips-2026100*-*.py`, `cambios-2026100*-*.py`, `calendario-*.py` | Definiciones y arreglos de cada tanda (de referencia) |
| Método | `PROCEDIMIENTO.md`, `METODO_META_BUSINESS_SUITE.md` | Procedimiento completo y programación en Meta |
| Marca | `logo.png`, `logo-alta.png`, `icono.svg`, `grabador-pestana.html` | |

Las especificaciones JSON de los lotes de octubre (`specs-*.json`) siguen en el centro de control. Se traen aquí cuando haga falta rehacer un lote.

**Las rutas de dentro de los scripts** apuntan a carpetas temporales de las sesiones que los escribieron. Antes de usarlos, se cambian por rutas de este repositorio.

### `comics/`: herramientas de montaje de los cómics (versión 2)
Se rehacen a partir de `claude/Comics_piloto.md`. Las de la versión 1 se perdieron.

## Investigaciones
`../investigacion/<fecha>-<tema>/`: datos y scripts de cada análisis (p. ej., el estudio de RRSS del 28/10/2026).

## Subir una pieza al centro de control (29/10/2026)

Cada creatividad lleva dos direcciones. En `publica` va la copia de GitHub (`raw.githubusercontent.com/...`), que es la que usan Buffer y Meta. En `url` va la copia del almacén del centro de control (`/_blob/...`, se sube con la herramienta Artifact, `asset: true`). El centro de control solo muestra lo que está en su almacén: si `url` apunta a GitHub, la portada y el vídeo no se ven.
