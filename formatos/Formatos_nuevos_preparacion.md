# Formatos nuevos de RRSS: preparación y guiones (28/10/2026)

Origen: informe «Redes sociales de Erreklamatu: qué funciona y nuevos contenidos» (https://claude.ai/artifact/DQSKeDzMaQEXF2fxTPqYCX). Aprobado por Sergio el 28/10/2026: todos los formatos salvo «¿Cuánto te deben desde Loiu?». Créditos de Magnific: «gasta los que necesites». Jon Ortiz y Óscar Sánchez autorizan su voz real con su versión ilustrada (no van a grabar nada nuevo de momento). Jon en vuelos, Óscar Sánchez en banca. Sin tope de vídeos al día: si dan buenos resultados, se publican los que haga falta.

## Criterios comunes (de los datos de octubre)
- 20 a 30 segundos. Los clips que funcionaron duraban de 16 a 34 s.
- **Primer segundo:** el dinero, la prueba o el desenlace en grande. Nada de presentaciones.
- Se entiende sin sonido: texto en pantalla y subtítulos.
- **Contenido propio** (Instagram, Facebook y TikTok premian lo original; a 28/10, Instagram sin límites de alcance).
- Contacto: teléfono y email, salvo el email en Instagram. Cierre con «Comenta …» en Instagram, TikTok y Facebook.
- Cada afirmación jurídica sale del banco de mensajes (MSG); lo que no está, se verifica antes.
- Sin logotipos reales de aerolíneas ni bancos en imágenes generadas o de archivo.

## Lo que ya existe (no hay que rehacerlo)
- Fichas de personaje en Magnific (Historial): Jon, Óscar, Laura, Mikel, la familia, Ane y Koldo (cómic europeo de línea clara, colores de marca).
- Voz: ElevenLabs v3 en Magnific, «Ana Beltrán» (castellano peninsular).
- Sintonía «viva» y música lo-fi de los cómics; cortinilla de cierre; logo en alta.
- Esquema de vídeo por zonas seguras; scripts de clips y radio en `sistema/` del centro de control.

## Lo que falta preparar
1. ~~Herramientas de montaje de los cómics~~ **Hecho (29/10):** rehechas en `herramientas/comics/comic.py` del repositorio GitHub `erreklamatu-rrss`, probadas de principio a fin. Todo el archivo de herramientas está ahora en el repositorio (normas en `herramientas/README.md`).
2. **Plantilla de gancho** (primer segundo) común a todos los formatos, y plantillas de «Mito o verdad», «El documento, subrayado», «Esta semana en los aeropuertos», «Reseñas en vídeo» y «Alerta en vídeo».
3. **Banco de vídeo de archivo** de Magnific (unos 50 clips verticales, sin logotipos): aviones, terminal, paneles, mostrador, cinta de maletas, móvil con SMS, cajero, documentos.
4. **Personajes:** hoja de expresiones de Koldo (vuelos) y de Laura (banca); retrato frontal ilustrado de Jon apto para *Speak*.
5. **Voz en euskera:** probar 3 o 4 voces y elegir una.
6. **Datos semanales de aeropuertos:** la pasada de aeropuertos solo guarda el último resumen. Para el resumen de los lunes hay que guardar los recuentos de cada pasada.
7. **Alerta en vídeo:** que la tarea de «pieza pedida» genere también la versión en vídeo.
8. **Medición:** marcar cada pieza piloto con su formato en el centro de control y comparar a las dos semanas.

## Guiones: cómic versión 2 (cuatro nuevos)
Situaciones de la lista aprobada el 15/10 que aún no se han producido. Personaje fijo: Koldo en vuelos, Laura en banca. Duración: 25 a 30 s.

**C1 · «Cancelado por el temporal. ¿Y el hotel?»** (Jon · MSG-003, 004, 022, 009)
- 0-2 s · Koldo, con la maleta en la terminal de noche, panel de «CANCELADO» detrás. Rótulo grande: «Te cancelan por el temporal: el hotel lo paga la aerolínea».
- 2-8 s · Koldo, al teléfono: «¿Y ahora dónde duermo?» Bocadillo del mostrador: «Es el tiempo. No podemos hacer nada.»
- 8-20 s · Jon en la consulta gratuita: «Con un temporal puede no haber compensación. Pero te tienen que dar otro vuelo o tu dinero, la comida y, si hay que pasar la noche, el hotel.»
- 20-25 s · «¿No te lo dieron? Guarda las facturas y deja tu caso en nuestras manos.»
- 25-28 s · Cierre: consulta gratuita · solo cobramos si ganamos · 944 027 596 · info@erreklamatu.com.

**C2 · «Perdiste la conexión en Madrid»** (Jon · MSG-001, 002)
- 0-2 s · Koldo corriendo por un pasillo, el avión de la conexión despegando tras el cristal. Rótulo: «Llegas 4 horas tarde: hasta 600 €».
- 2-8 s · «El primer vuelo salió con retraso. El segundo ya no me esperó.»
- 8-20 s · Jon: «Lo que cuenta es la hora a la que llegas a tu destino final. Si son 3 horas o más, puedes tener derecho a 250, 400 o 600 € según la distancia.»
- 20-28 s · «Guarda las tarjetas de embarque de los dos vuelos y déjanoslo a nosotros.» Cierre.

**C3 · «Pagó 6.500 € por 3.000 €»** (Óscar · MSG-053, 054, 029, 031)
- 0-2 s · Laura mirando el extracto, cifras en rojo. Rótulo: «Gastó 3.000 €. Pagó 6.500 €».
- 2-8 s · «Pago cada mes y la deuda no baja.»
- 8-20 s · Óscar: «Es una tarjeta revolving: casi toda la cuota se va en intereses. Si el interés es usurario, te devuelven todo lo que pagaste de más.»
- 20-28 s · «Busca los extractos y déjanos tu caso.» Cierre. Ejemplo tomado de la web del despacho (MSG-053).

**C4 · «Todavía le debo dinero al banco»** (Óscar · MSG-060, 062, 055)
- 0-2 s · Laura dudando ante el móvil. Rótulo: «¿Debes dinero de la tarjeta? Puedes reclamar igual».
- 2-8 s · «Pensaba que, mientras debiera algo, no podía reclamar. Y casi dejo de pagar.»
- 8-20 s · Óscar: «Se puede reclamar con deuda pendiente, y esa deuda puede quedar cancelada. Lo que no hay que hacer es dejar de pagar: la deuda crece y pueden meterte en un fichero de morosos.»
- 20-28 s · «Primero se reclama. Nosotros nos encargamos.» Cierre.

## Guiones: Mito o verdad (cuatro)
Formato: 3 afirmaciones de 4-5 s cada una, «¿Mito o verdad?» en grande; la respuesta aparece con un sello. Cierre: «¿Cuántas acertaste? Cuéntanoslo en comentarios.» 20-25 s.

**MV1 · Vuelos**
1. «Con una low cost no tienes los mismos derechos.» → MITO. El reglamento vale para cualquier compañía. (MSG-014)
2. «Si el retraso es por mal tiempo, no te deben nada.» → MITO. Sin compensación, pero sí comida, hotel y otro vuelo o tu dinero. (MSG-003, 022)
3. «Con 5 horas de retraso puedes renunciar al viaje y recuperar el billete.» → VERDAD. (MSG-005)

**MV2 · Maletas**
1. «Si tu maleta llega rota, tienes un mes para reclamar.» → MITO. Son 7 días desde que la recibes. (MSG-013)
2. «Si a los 21 días no ha aparecido, cuenta como perdida.» → VERDAD. (MSG-028)
3. «Si la maleta llega tarde, no puedes reclamar nada.» → MITO. La aerolínea responde del daño por el retraso. (MSG-028, 013)

**MV3 · Phishing**
1. «Si diste el código, el banco no te devuelve nada.» → MITO. Debe devolver lo no autorizado salvo que pruebe negligencia grave. (MSG-024)
2. «La prueba le toca al banco, no a ti.» → VERDAD. (MSG-024)
3. «Lo primero es avisar al banco, pedir el bloqueo y denunciar.» → VERDAD. (MSG-025)

**MV4 · Revolving**
1. «Si dejo de pagar la tarjeta, se acaba el problema.» → MITO. La deuda crece y pueden demandarte. (MSG-055)
2. «Si todavía debes dinero, no puedes reclamar.» → MITO. Se puede, y la deuda puede quedar cancelada. (MSG-060)
3. «Más de 6 puntos sobre la media puede ser usura.» → VERDAD, según el Supremo. (MSG-029)

## Guiones: El documento, subrayado — con casos reales del despacho (28/10, idea de Sergio)
Formato: 20-25 s. Primer segundo: la frase del fallo subrayada sobre la sentencia real (anonimizada) y el resultado en grande. Después, el artículo que lo sostiene (Reglamento 261 o RDL 19/2018), una línea de qué te supone a ti y cierre. Fuente de cada caso: la nota de prensa publicada en la web (leída el 28/10/2026). Sergio consigue la sentencia.

**Cómo se mantiene el interés sin fingir que es reciente**
- Ni fecha ni palabras de novedad: fuera «nueva», «acaba de», «hoy», «reciente», «precedente». Se cuenta en pasado neutro: «Un juzgado de Bilbao les dio la razón».
- La actualidad la pone quien lo ve, no el caso. Gancho en presente («¿Te cancelan el vuelo de Navidad?») y el caso como prueba de que se puede.
- El plazo de 5 años (MSG-006) es un gancho verdadero: «¿Te pasó en los últimos 5 años? Aún estás a tiempo».
- Si hay noticia (huelga, temporal, Volotea), el caso que mejor encaje se publica ese día.
- Es un juzgado de primera instancia, no jurisprudencia: se dice «un juez», nunca «la justicia establece».
- En la imagen de la sentencia se tapan nombres, número de procedimiento y fecha. Taparlo no es mentir; si alguien pregunta, se le contesta.
- Antes de producir cada pieza se comprueba que el criterio sigue vigente. El Reglamento 2026/2202 se aplica desde el 23/10/2027: entonces se revisan todas.
- Ni nombres de pasajeros ni de empresas organizadoras, aunque salgan en la nota.

**Los cuatro elegidos**
- **S1 · Daño moral: 500 € más por pasajero.** Enter Air, vuelo cancelado desde Irlanda, 117 menores, Juzgado de Primera Instancia n.º 9 de Pamplona: 250 € + 500 € de daño moral por pasajero. Después, 35 más cobraron lo mismo sin juicio. Subrayado: la frase del juez sobre «zozobra, angustia, incertidumbre». Artículo: 261, art. 5 y 7 (MSG-001/002). Gancho: «El juez les dio 500 € más a cada uno. No por el vuelo: por la noche que pasaron». Nota: /es/erreklamatu-logra-mas-de-90-000-euros-para-120-pasajeros/
- **S2 · Perdieron el partido y les devolvieron las entradas.** Vueling, conexión perdida en Barcelona camino de Roma (Athletic), Juzgado de Primera Instancia n.º 9 de Bilbao: 250 € por pasajero, las entradas (70 €) y el taxi. Vueling solo aceptaba los 250 €. Subrayado: el reembolso de las entradas. Artículo: 261, art. 7 + Código Civil. Gancho: «El retraso les hizo perder el partido del Athletic. El juez les devolvió hasta las entradas». Nota: /es/vueling-condenada-a-indemnizar-a-dos-pasajeros-y-a-devolverles-las-entradas-del-partido-del-athletic-en-roma/
- **S3 · Cuatro cosas en una sentencia.** Vueling, Bilbao–Gran Canaria cancelado el mismo día, 12 pasajeros que iban a un congreso, Juzgado de Primera Instancia n.º 12 de Bilbao: 400 € por pasajero, los billetes, los hoteles no disfrutados y 200 € de daño moral (más de 13.500 € en total). Subrayado: el fallo con las cuatro partidas. Artículo: 261, art. 5, 7 y 8. Gancho: «Les cancelaron el vuelo. El juez les dio cuatro cosas». Nota: /es/vueling-condenada-a-pagar-mas-de-13-500-euros-a-12-pasajeros-por-cancelar-un-vuelo/
- **S4 · «Usó su clave» no basta (banca).** Banco Santander, cargo de criptomonedas no autorizado, Juzgado de Primera Instancia n.º 12 de Bilbao: devolver 1.923,67 € más intereses y costas. El banco alegó 3D Secure sin pericial. Subrayado: que la autenticación reforzada no prueba que la clienta autorizara. Norma: RDL 19/2018 (no es del 261). Gancho: «El banco dijo: "Usó su clave". El juez: eso no demuestra nada». Nota: /es/un-juzgado-de-bilbao-da-la-razon-a-una-victima-de-phishing/
- **Reserva · S5 Hop / grupo de danzas de Donostia:** cancelación a la ida y denegación de embarque a la vuelta, Juzgado de lo Mercantil n.º 1 de Bilbao: 600 € por cada vuelo y persona. Es el caso más antiguo (nota de 2020).

**Descartados:** Lufthansa por exceso de carga (la nota no habla de sentencia) e ikastola de Gernika (Vueling pagó tras la demanda; tampoco hay sentencia). Errata en la web: el título de esa nota dice 7.015 € y el texto 7.105 €.

**Sentencias públicas que puedo buscar yo en CENDOJ:** la STS 571/2025, de 9 de abril (phishing), que cita la nota de S4, como refuerzo; y, para revolving, la STS 258/2023 (MSG-029), porque en el blog no hay ningún caso propio de banca salvo el de phishing.

## Guiones: «Jon habla» (pilotos de *Speak*)
El Jon ilustrado del cómic, en primer plano, habla con su propia voz sacada de la radio. 20-25 s, gancho en pantalla en el primer segundo.
- **H1:** fragmento de PUB-0213 (Radio Popular, exceso de carga): «Serían tres conceptos: una asistencia mínima, la indemnización según la distancia y los gastos generados.» Rótulo: «Te bajan del avión: 3 cosas que te deben».
- **H2:** fragmento de PUB-0426 (Radio Popular): «El porcentaje de éxito es bastante alto. Para librarse de pagar, tiene que ser algo extraordinario… y aun así tienen que darte asistencia.» Rótulo: «¿Quién gana, tú o la aerolínea?»
- **Óscar (28/10):** autoriza, como Jon, pero de momento no graba. De Óscar hay decenas de fragmentos de vuelos en TV (SIML, En Jake, TVE…), que sirven para «Óscar habla» de vuelos tal cual. Para banca, con su voz: clonarla a partir de esos audios si Magnific lo permite (lo compruebo). Si no, voz sintética neutra («si no puede ser con su voz, ponemos otra»).

## Plantillas que faltan por definir al producir
- **F · Esta semana en los aeropuertos vascos:** carrusel y vídeo de 15 s. Vuelos cancelados y con más de 3 h de retraso por aeropuerto (Loiu, Hondarribia, Foronda, Noain, Biarritz), qué se puede reclamar y cierre. Sale cuando haya una semana de datos guardados.
- **G · Clip de TV con capa propia:** 3 s de gancho propio, el fragmento intacto con un texto de contexto encima y un cierre propio. Primeros 5: clips de menos de 35 s aún no publicados.
- **H · Reseñas en vídeo:** una reseña real por vídeo (capturas de la colección `resenas`), 10-15 s.
- **A · Alerta en vídeo:** 15-20 s con el titular de la alerta («¿Ibas en el … de las …?»), vídeo de archivo y la sintonía.
