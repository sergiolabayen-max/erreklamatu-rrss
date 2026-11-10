# Programar Facebook e Instagram en Meta Business Suite (método probado)

Desde el 11/10/2026 Facebook e Instagram se programan **solo aquí**, desde el chat del proyecto, con el Chrome de Sergio. Buffer queda para X, TikTok y YouTube.

## ENLACES DE FACEBOOK: SIEMPRE EN EL PRIMER COMENTARIO (decisión de Sergio, 14/10/2026, 13:22)

**Por qué.** Meta solo deja publicar **2 publicaciones con enlace al mes** en la página de Facebook de Erreklamatu (sin Meta One; descubierto el 14/10/2026). En octubre de 2026 ya están gastadas; el cupo se renueva el día 1 de cada mes.

**Lo que se hizo el 14/10/2026.** En las 200 piezas no publicadas que llevaban enlace en el texto de Facebook (aprobadas, pendientes, con cambios pedidos y en reserva) se quitó el enlace, con su línea de entrada («Toda la información 👇», «Más información 👇», «Informazio gehiago 👇»…), y se pasó al campo `comentario_facebook`. El texto anterior queda en `facebook_antes_enlace_a_comentario`. PUB-0308 deja los perfiles como @erreklamatucom y @erreklamatu en el texto, con los enlaces en el comentario; PUB-0342 lleva en el comentario los enlaces de las tres noticias. Las piezas nuevas se escriben ya así: el texto de Facebook sin enlaces y el enlace en `comentario_facebook`.

**Al programar Facebook.**
- Se usa `textos.facebook` tal cual (no lleva enlaces).
- Si aun así Meta muestra la tarjeta de un enlace, o el botón «Programar» sale gris con el aviso «Publica más enlaces con Meta One · Elimina tu enlace para terminar de publicar», pulsar **«Eliminar enlace»** (quita la tarjeta sin tocar el texto; el correo info@erreklamatu.com se queda).
- **Nunca pulsar «Obtener Meta One»** (es de pago).
- Si una pieza tuviera todavía una URL en `textos.facebook`, no se programa su Facebook: queda en `pendiente_redes` y se avisa a Sergio.

**Después de publicar.**
- Comprobado que la publicación de Facebook ha salido (Contenido > Publicadas), se pone `comentario_facebook` como **primer comentario**, comentando **como la página de Erreklamatu**, no como el perfil personal de Sergio. Si no se puede confirmar que se actúa como la página, no se comenta y se avisa.
- Se teclea el texto, se comprueba que el enlace y los saltos de línea quedan igual que en la ficha, se publica y se recarga para ver que el comentario está.
- En la pieza se guarda `comentario_facebook_hecho` = {fecha, url de la publicación}.
- En Instagram no se ponen comentarios con enlace.

**Sin comprobar.** Que un enlace en un comentario no gaste el cupo de Meta (el cupo afecta a las publicaciones, según el aviso de Meta). Si Meta bloquea el comentario, se anota y se avisa a Sergio.

**Piezas ya programadas en Meta con el enlace en el texto (antes de la decisión):** PUB-0031 (14/10, 21:26), PUB-0122 (20/10, 09:24) y PUB-0023 (25/10, 21:01). Editadas en Meta el 14/10/2026 con el visto bueno de Sergio: enlace fuera del texto, fechas y horas intactas, verificado en Programadas. El enlace está en comentario_facebook, para el primer comentario tras publicar.

Historial:

- **9/10/2026:** pruebas de imagen (PUB-0383) y reel (PUB-0166). Las dos salieron a su hora (sábado 10/10 10:33 y domingo 11/10 09:12).
- **11/10/2026, 16:40–17:13:** cambio de herramientas. Programadas 8 piezas (7 reels y 1 carrusel): PUB-0056, 0064, 0031, 0007, 0133, 0122, 0009 y 0023. PUB-0060 no entró (vídeo de 12,3 MB) y Sergio la retiró.
- **14/10/2026, 08:08:** PUB-0473 (publicación para fijar) programada a las 8:27 en Facebook (sin enlace, por el límite) e Instagram; X por Buffer.
- **14/10/2026, 13:40:** enlaces de Facebook al primer comentario en 200 piezas (ver arriba).

## Historias de Facebook: prueba hasta el 23/10/2026

Decisión de Sergio (9/10/2026, 07:02):

- **Reels:** se deja activado «Compartir en una historia de Facebook». Viene así por defecto: no tocarlo.
- **Publicaciones con imagen (también carruseles):** se desactiva, hasta ver cómo queda una infografía vertical en formato historia.
- **Estadísticas de historias:** activadas en la cuenta el 9/10 a las 07:06 (Contenido > Historias). Las cifras anteriores no valen.
- **El 23/10** se comparan espectadores y reacciones de las historias y Sergio decide.
- La historia hay que dejarla bien a la primera: «Editar reel» en un reel ya programado no la ofrece.

## Requisitos

- Sesión con acceso al Chrome de Sergio. Las sesiones en la nube sin herramientas de navegador no pueden hacerlo.
- Navegador: el del perfil «Erreklamatu», deviceId `3623fed4-8c35-44e6-9149-8b48d04761f6`. Los nombres «Browser N» cambian: se elige por deviceId. La selección se pierde entre tandas: volver a llamar a `select_browser` antes de cada una.
- Meta Business Suite abre con sesión y con «Erreklamatu y erreklamatu» ya seleccionados en «Publicar en».

## Límite de tamaño de los archivos

- La subida al navegador (`file_upload`) admite **10 MiB por llamada** (10 485 760 bytes). Un vídeo de 10 341 111 bytes entró; uno de 12 300 028, no.
- Si un archivo se pasa, `browser_batch` rechaza **la tanda entera antes de ejecutar nada**: los pasos anteriores de esa tanda tampoco se hacen. No meter en la misma tanda una subida dudosa y un clic que importe.
- Un vídeo que se pase de 10 MiB no se puede programar por esta vía sin recomprimirlo o sin que lo suba Sergio. Decidirlo con él.

## Pasos comunes

1. **Datos de la pieza:** documento `publicaciones/PUB-XXXX` de la base de datos del centro de control (`textos.facebook`, `textos.instagram`, `creatividades[].publica`, `fecha_objetivo`, `fecha_objetivo_redes`).
2. **Archivo:** descargarlo de la URL pública de GitHub y copiarlo a `/mnt/user-data/uploads/rrss/` (desde otra carpeta la subida falla).
3. **Subir:** con `javascript_tool`, cambiar `HTMLInputElement.prototype.click` para que un input de tipo file se añada al documento en vez de abrir el selector del Mac. Pulsar el botón de añadir (vale el clic por script sobre el botón), luego `find` del input y `file_upload` con `paths`.
4. **Textos:** activar «Personaliza la publicación para Facebook e Instagram»; pestaña Facebook, escribir; pestaña Instagram, escribir.
   - **El editor se enfoca con un clic de ratón de verdad.** Enfocarlo por script y teclear corrompe el texto.
   - Antes de medir dónde está el editor, hacer una captura: con la pestaña en segundo plano la página no se pinta y las medidas salen a cero.
   - Tras teclear, comparar por script el texto del editor con el de la ficha (quitando saltos de línea repetidos) y parar si no coincide. La longitud en JavaScript cuenta cada emoji de fuera del plano básico (📞, 👇) como 2.
   - Tras los hashtags queda abierta una lista de sugerencias: se cierra con un clic en una zona vacía.
5. **Fecha y hora:** separadas para Facebook y para Instagram (sirve para AC-13). Fecha: clic, `cmd+a`, escribir `dd/mm/aaaa`, Intro. Hora: clic en el segmento de horas y teclear dos cifras; clic en el de minutos y teclear dos cifras. Comprobar con una captura ampliada: las horas no se leen por script.
6. **Verificar:** `https://business.facebook.com/latest/posts/scheduled_posts`. Una fila por red y pieza. Comprobar fecha, hora y **texto** de cada fila (longitud y final cotejados con la ficha). Las horas están en hora de Madrid, aunque el formulario diga «Europe/Vienna».
7. **Anotar en el centro de control:** campo `meta_business_suite` de la pieza (estado y fecha por red, historia, subtítulos, verificación), `pendiente_redes`, aviso al principio de `notas` y una línea en `registro`.

## Reel (`/latest/reels_composer`)

Tres pasos: Crear, Editar, Compartir.

- **Crear:** botón «Añadir vídeo». En Instagram el campo se llama «Reel con descripción». La vista previa y las miniaturas se quedan en negro o en gris con la pestaña en segundo plano: no es un fallo.
- **OJO, FALLO DEL 11/10: la pestaña de red se cambia SIEMPRE con clic de ratón.** Si se cambia de «Facebook» a «Instagram» con un clic por script, el editor muestra bien el texto de Facebook pero Meta no lo guarda y el reel de Facebook queda **sin texto** (en la lista de programadas sale como «Tu reel»). Pasó en PUB-0007, 0133, 0009 y 0023; en las tres primeras piezas, con clic de ratón, no pasó.
- **Editar:** no tocar nada. «Siguiente».
- **Compartir:**
  - Por defecto está elegido **«Compartir», que publica en el momento.** Antes de nada, pulsar **«Programar»** y comprobar que el botón azul de abajo dice «Programar».
  - Desmarcar «Subtítulos» (vienen con «Subtítulos automáticos activados»; nuestros vídeos ya los llevan).
  - Historia de Facebook («Share to»): dejarla activada durante la prueba.
  - Fecha y hora por red.
  - «Programar». Sale «Se ha programado el reel… en Facebook y… en Instagram»; «Cerrar».
- **Arreglar el texto de un reel de Facebook ya programado:** en «Programadas», clic en la fila, «…» arriba a la derecha del panel > «Editar reel». Se escribe la descripción, «Siguiente» y «Programar» (conserva la fecha). En ese panel hay un botón **«Publicar ahora»: no tocarlo.** El mismo menú tiene «Reprogramar publicación», «Mover a borradores» y «Eliminar publicación».

## Publicación con imagen o carrusel (`/latest/composer`)

- Botón «Añadir foto o vídeo». Todo está en una sola pantalla. El input admite varios archivos: para un carrusel se suben todos en una llamada, en su orden, y se comprueba el orden en la lista de miniaturas.
- En Instagram sale como carrusel. **En Facebook sale como publicación de varias fotos (mosaico)**: en la vista previa la portada vertical aparece recortada por los lados. No se ha comprobado cómo queda publicada.
- Aquí el cambio de pestaña por script sí conservó el texto de Facebook (comprobado volviendo a la pestaña antes de programar). Aun así, comprobarlo siempre.
- Activar «Definir fecha y hora»; fecha y hora por red.
- Historia de Facebook: desactivarla. Sale un cuadro con dos opciones: «No compartir esta publicación» (solo esa) y confirmar **por referencia** (`find` + `ref`); el cuadro tarda en pintarse.
- «Programar». Tarda unos 10 s. Sale «Se ha programado la publicación» con una oferta de promoción de pago: pulsar **«Quizá más tarde»**, nunca «Promocionar».
- Si el composer se queda colgado en «Programando tu publicación», no volver a pulsar nada (riesgo de duplicar): verificar en otra pestaña.
- Si «Programar» sale gris, pasar el ratón por encima: puede ser el límite de enlaces (ver arriba).

## Cosas que se ven en Meta y no son un problema

- **«Archivadas» en el planificador:** son historias de Facebook caducadas (duran 24 h), no vídeos archivados.
- **«Untitled Video»:** título interno de los reels de Facebook publicados por Buffer; el reel público llevaba el texto correcto.
- **«Tu reel» en la lista de programadas NO es normal:** significa que el reel de Facebook no tiene texto (ver el fallo del 11/10).

## Pendiente

- Comprobar la salida real de las 8 piezas programadas el 11/10 (la primera, PUB-0056, el 12/10 a las 16:25).
- No se sabe si los cuatro reels de Facebook corregidos con «Editar reel» conservan la historia de Facebook: mirarlo en Contenido > Historias cuando salgan (16, 18, 21 y 25/10).
- PUB-0060: retirada por Sergio el 11/10. Si se retoma, su vídeo hay que bajarlo de 10 MiB o subirlo a mano.
- El 23/10: comparar las estadísticas de las historias.
