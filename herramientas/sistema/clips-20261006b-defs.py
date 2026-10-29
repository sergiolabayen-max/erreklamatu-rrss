# Clips de las intervenciones en medios recuperadas el 6 de octubre de 2026 (tarde). Cada tramo: (inicio, fin, quien, texto corregido a partir de UNA transcripción automática[, opciones]).
S = "/tmp/claude-0/-home-claude-erreklamatu-rrss/049ce1e0-2613-5255-8bf4-bbf49454531a/scratchpad"
M7 = S + "/m7"
JON = r"{\b1}Jon Ortiz{\b0}  ·  Abogado de Erreklamatu"
OSC = r"{\b1}Óscar Sánchez{\b0}  ·  Abogado de Erreklamatu"

V = {
 "v9": dict(video=M7 + "/src/v9b.mp4", audio=M7 + "/v9b.wav", desfase=-0.04, credito="Imágenes: EITB · En Jake (junio de 2025)", prefijo="",
            rotulos={"jon": r"{\b1}Jon Ortiz{\b0}  ·  Erreklamatu  ·  junio de 2025", "reportera": r"{\b1}En Jake (ETB2){\b0}  ·  junio de 2025"},
            enc={"jon": [0, 64, 404], "reportera": [0, 64, 404]},
            marco={"lado_pleno": 404, "lado_ventana": 404, "sin_cara": [0, 64, 404]}),
 "v10": dict(video=M7 + "/src/v10b.mp4", audio=M7 + "/v10b.wav", desfase=-0.04, credito="Imágenes: EITB · En Jake (octubre de 2024)",
            rotulos={"oscar": OSC, "reportero": "Pregunta del programa"}, preguntan=["reportero"], capas=M7 + "/v10capas.json",
            marco={"sin_cara": [0, 58, 300]}),
 "v1": dict(video=M7 + "/src/v1pad2.mp4", audio=M7 + "/v1yt.wav", credito="Imágenes: EITB · Quédate con Ane (8 de enero de 2024)",
            rotulos={"jon": JON, "pasajero": "Pregunta de un pasajero"}, preguntan=["pasajero"],
            enc={"jon": ["izqarriba"], "pasajero": ["mayor"]},
            marco={"lado_izq": 518, "lim_izq": [0, 518], "lado_pleno": 700, "sin_cara": [0, 190, 518]}),   # vídeo con 112 px añadidos a la izquierda (se estira la primera columna: pared blanca), para centrar a Jon sin que asome el panel de al lado
 "v2": dict(video=M7 + "/src/v2.mp4", audio=M7 + "/v2.wav", credito="Imágenes: EITB · En Jake (7 de julio de 2022)",
            rotulos={"oscar": OSC},
            enc={"oscar": ["izq"], "presentador": ["izq"]},
            marco={"lado_izq": 200, "lado_der": 150, "lado_pleno": 244, "sin_cara": [10, 28, 200]}),
 "v3": dict(video=M7 + "/src/v3yt.mp4", audio=M7 + "/v3yt.wav", credito="Imágenes: EITB · Qué me estás contando (25 de noviembre de 2019)",
            rotulos={"oscar": OSC},
            enc={"oscar": ["der"], "presentador": ["izq", "centro"]},
            marco={"lado_der": 250, "lado_izq": 250, "lado_pleno": 300, "techo": 28, "sin_cara": [400, 40, 230]}),
 "v4": dict(video=M7 + "/src/v4.mp4", audio=M7 + "/v4.wav", credito="Imágenes: EITB · Está pasando (1 de julio de 2019)",
            rotulos={"oscar": r"{\b1}Óscar Sánchez{\b0}  ·  Abogado de Erreklamatu  ·  por teléfono"},
            enc={"presentador": ["izq", "mayor"]},
            marco={"lado_izq": 190, "lado_pleno": 244, "sin_cara": [0, 30, 190]}),
 "a14": dict(video=M7 + "/fijo/a14.mp4", audio=M7 + "/a14.wav", credito="Audio: COPE · Mediodía COPE (8 de junio de 2023)", prefijo="",
            rotulos={"jon": r"{\b1}Jon Ortiz{\b0}  ·  Abogado de Erreklamatu  ·  en la radio", "locucion": r"{\b1}Mediodía COPE{\b0}  ·  8 de junio de 2023"}, preguntan=["locucion"],
            enc={"jon": [0, 0, 1080], "locucion": [0, 0, 1080]}, marco={"sin_cara": [0, 0, 1080]}),
 "a3": dict(video=M7 + "/fijo/a3.mp4", audio=M7 + "/a3.wav", credito="Audio: Radio Popular · EgunOn Magazine (1 de septiembre de 2023)",
            rotulos={"jon": r"{\b1}Jon Ortiz{\b0}  ·  Abogado de Erreklamatu  ·  en la radio", "pregunta": "Pregunta del programa"},
            enc={"jon": [0, 0, 1080], "pregunta": [0, 0, 1080]}, marco={"sin_cara": [0, 0, 1080]}),
 "a11": dict(video=M7 + "/fijo/a11.mp4", audio=M7 + "/a11.wav", credito="Audio: Radio Euskadi · Boulevard (4 de agosto de 2023)",
            rotulos={"oscar": r"{\b1}Óscar Sánchez{\b0}  ·  Abogado de Erreklamatu  ·  en la radio", "pregunta": "Pregunta del programa"},
            enc={"oscar": [0, 0, 1080], "pregunta": [0, 0, 1080]}, marco={"sin_cara": [0, 0, 1080]}),
 "v11": dict(video=M7 + "/src/v11n.mp4", audio=M7 + "/v11n.wav", desfase=-0.04, credito="Imágenes: EITB · informativos (enero de 2021)", prefijo="",
            rotulos={"jon": JON, "locucion": r"{\b1}Informativos de EITB{\b0}  ·  enero de 2021"}, preguntan=["locucion"],
            enc={"locucion": ["mayor"]},
            marco={"lado_pleno": 1080, "lado_ventana": 1080, "lado_min": 640, "sin_cara": [420, 0, 1080], "planos": "cortes", "cara_min": 0.09}),
}
RAD14 = {"video": M7 + "/fijo/a14r.mp4"}; RAD3 = {"video": M7 + "/fijo/a3r.mp4"}; RAD11 = {"video": M7 + "/fijo/a11r.mp4"}
FIJO11 = {"video": M7 + "/fijo/v11.mp4", "enc": [0, 0, 1080]}
FIJO4 = {"video": M7 + "/fijo/v4.mp4", "audio": M7 + "/v4.wav", "enc": [0, 0, 1080]}

# ---------------------------------------------------------------- En Jake (ETB2), junio de 2025: el acuerdo de los Estados de la UE para recortar las compensaciones
N_J1 = (0.45, 37.75, "jon", "Bueno, pues nosotros pensamos que claramente perjudica, ¿no? Al final, la modificación… ha habido dos modificaciones, a grandes rasgos. Una es ampliar el tiempo que se pueden retrasar los vuelos. Por tanto, si antes a partir de un retraso de tres horas podías pedir una indemnización, ahora tiene que ser más de cuatro horas o más de seis, depende de la distancia de los vuelos. Y, por otra parte, se ha reducido el importe de las indemnizaciones: cuando antes era 400 euros, ahora va a ser 300, y cuando antes era 600, ahora va a ser 500. Por tanto, entendemos que en todos los aspectos perjudica claramente a los viajeros y a las viajeras.")
N_Q2 = (38.47, 45.36, "reportera", "¿A qué porcentaje de reclamaciones afectaría esta medida y qué conlleva eso en las aerolíneas?")
N_J2 = (45.86, 76.40, "jon", "Pues, a falta de calcularlo, sí que es verdad que la mayoría de los retrasos estarían en el margen de entre dos y cuatro horas. Y, como ya he explicado, si ya ese margen lo dejamos fuera de la aplicación, fuera de la indemnización, y ya tienes que irte a más de cuatro horas o, como decía, a más de seis horas en algunos casos, pues podríamos decir que el 70 % de las reclamaciones quedarían fuera, o el 70 % de los casos que antes se indemnizaban no habría que indemnizar. Y eso, obviamente, para las aerolíneas es una ventaja clara.")
N_Q3 = (77.16, 89.15, "reportera", "Uno de los objetivos, se dice, es reducir ese número de cancelaciones en beneficio del viajero, que puede llegar a su destino aunque sea unas horas más tarde. Pero ¿realmente beneficia más a las aerolíneas que al consumidor?")
N_J3A = (89.48, 98.39, "jon", "Sí, ese es el argumento que han utilizado, que repiten todo el rato. A nosotros nos cuesta ver o entender la explicación de dicho argumento.")
N_J3B = (99.14, 132.79, "jon", "Pero, como decía, al fin y al cabo, si estamos limitando los casos que se pueden reclamar o que se pueden indemnizar, estamos limitando las indemnizaciones en número, simplemente reduciendo los importes, pues está claro que al final, en nuestra opinión, esto obedece a la presión que hacen las aerolíneas a los Estados. Al final son poderosas, tienen mucho poder de influencia, y entendemos que es ceder a esa presión en contra de los derechos de las pasajeras y los pasajeros, que son al final los que van a salir afectados.")


# ---------------------------------------------------------------- En Jake (ETB2), octubre de 2024: borrasca y vuelos cancelados en Bilbao
K_Q1 = (28.30, 34.02, "reportero", "Si por condiciones meteorológicas adversas perdemos un vuelo, lo primero, ¿qué es lo que tenemos que hacer?")
K_A1 = (34.10, 61.32, "oscar", "Sí, bueno, Mikel, y muchas gracias a vosotros. Lo primero que tenemos que hacer es guardar toda la documentación, eso siempre, y sobre todo saber qué derechos son los que tenemos. Al final, cuando hay una circunstancia extraordinaria como esta, algo ajeno a la compañía, lo que tenemos es derecho a un reembolso o a un vuelo alternativo. Tenemos derecho también a que nos pongan un hotel y los traslados entre el hotel y el aeropuerto para el vuelo alternativo, y también la manutención de los días en los que vayamos a estar tirados en Bilbao. Esos serían un poco los derechos que tendríamos.")
K_Q2 = (61.85, 75.55, "reportero", "Óscar, algún caso en concreto. Yo ayer estuve hablando con mucha gente. Por ejemplo, si yo voy a Barcelona o a Madrid y me cancelan el vuelo, pero me ponen un autobús, pero no me convence esa alternativa, ¿yo puedo seguir reclamando? Porque estamos hablando de un factor externo a la compañía.")
K_A2 = (75.60, 82.90, "oscar", "En ese caso, lo que hemos comentado: podrías ir en autobús o, si no te convence la alternativa, pedir el reembolso del vuelo. Esas serían las posibilidades que…")
K_Q2B = (83.35, 84.60, "reportero", "¿Puedo pedir el dinero?")
K_A2B = (84.65, 88.60, "oscar", "Efectivamente, el reembolso del vuelo, lo que has gastado, ya que no vas a usar ese vuelo.")
K_Q3 = (90.40, 106.25, "reportero", "Otro caso: una pareja que iba a Gran Canaria. No hay vuelos hoy; lo único que sale es mañana viernes. ¿Qué pasa en ese caso? Si me cancelan el de ayer y hasta dentro de dos días, mañana viernes, no puedo viajar, me tengo que quedar en un hotel en Bilbao. ¿Qué hago? ¿Me tengo que guardar esas facturas?")
K_A3 = (106.40, 138.95, "oscar", "Efectivamente. Ahí, como tienes que estar dos días, entra ya otro supuesto: si tú vas a coger ese vuelo alternativo, lo que sí que tiene que hacer la compañía es abonarte las cantidades que tú ya has desembolsado: desayunos, comidas, cenas, también el hotel en el que te vayas a tener que estar y luego, lo que hemos dicho, los traslados al aeropuerto desde ese hotel. Si tú tienes que abonar esas cantidades por anticipado, luego lo vas a poder reclamar. Puedes contactar con nosotros, con erreklamatu.com, nosotros podemos hacer la reclamación pertinente; también lo puedes reclamar por tu cuenta, no hay ningún problema, como prefiera el cliente.")
K_Q4 = (139.25, 151.10, "reportero", "Te pongo otro caso un poco más complicado: una chica joven que se marchaba a Canadá de vacaciones. Claro, tenía que ir desde Bilbao a Múnich y de Múnich a Canadá. Claro, perdió el enlace del vuelo de Alemania a Canadá. En ese caso…")
K_A4 = (151.20, 183.45, "oscar", "Mira, esa es una pregunta que la gente no suele saber, y es que el vuelo, si se compra con un mismo billete, es decir, si lo compras a través de una agencia y es conjunto, el vuelo es hasta el final. Es decir, desde el inicio hasta el final; el enlace nos olvidamos en cierta manera. Por lo tanto, el reembolso o la alternativa que hay que poner tiene que ser que te lleve al destino final. Cuestión diferente sería si hubieras comprado los vuelos independientes: en ese caso estaríamos hablando de que solo tienes derecho a reembolso de una parte del vuelo, vamos a decir, de la totalidad. Pero si has comprado conjuntamente, es la totalidad del vuelo lo que hay que tener en cuenta.")
K_Q5 = (185.50, 192.20, "reportero", "Quien viajaba a Valencia, por ejemplo: tenían una reunión importante de trabajo. ¿Eso se compensa de alguna forma, porque no llegaban?")
K_A5 = (194.10, 213.80, "oscar", "Sí. En este caso, si es circunstancia extraordinaria, ajena a la compañía, no entraría en esos derechos de indemnización. En casos diferentes, en los que ha sido un problema de la propia compañía, una avería técnica, por ejemplo, ahí sí que se pueden reclamar esos extras y, aparte, una indemnización. Pero en este caso nos tendríamos que limitar a los derechos de los que hemos estado hablando hace un momento.")
K_Q6 = (214.40, 217.60, "reportero", "¿Han sonado mucho los teléfonos esta mañana? Me imagino que estaréis a tope.")
K_A6 = (217.70, 239.35, "oscar", "Sin parar, sin parar. Todo el mundo nos está llamando, y es normal: al final, el caos que se genera… la gente no conoce mucho sus derechos. Y ahí sí que es verdad que también las compañías pecan un poco de no informar, y es otra obligación que tienen: tienen obligación de informar a los clientes y decirles qué derechos tienen y facilitar la posibilidad de reclamación. Vemos que ahí fallan un poquito las compañías, notamos, y es lo que nos trasladan los clientes.")
K_Q7 = (245.60, 251.80, "reportero", "Óscar, ¿quieres compartir con nosotros alguna llamada que te haya hecho algún pasajero, algún caso en concreto, para que aprendamos un poco más?")
K_A7 = (251.85, 288.30, "oscar", "Sí. Y es un caso concreto, pero que a la vez es típico, que es: «Joder, me quedo… si no me están poniendo hotel, no hay hoteles ahora mismo para poder… son las doce de la noche. ¿Qué hago?». Y ahí a veces es un poco frustrante no poder dar una solución, porque a veces la gente se tiene que quedar tirada en el aeropuerto sin un sitio donde dormir. Y eso es algo concreto, pero a la vez típico. Y la verdad es que son situaciones bastante difíciles: hay gente incluso con críos, gente en silla de ruedas… Esas llamadas tenemos siempre cuando pasan estas cuestiones. Y la verdad es que es una pena que estas situaciones pasen, cuando las compañías tienen obligación de dar esas soluciones.")

# ---------------------------------------------------------------- Quédate con Ane (ETB2), 8 de enero de 2024: huelga del personal de tierra de Iberia (tiempos de la copia de YouTube)
J_QD = (143.25, 152.00, "pasajero", "No sé muy bien si, cuando se quedan en el aeropuerto, nos las mandan a casa o me contactarán para que vaya a recogerlas a algún sitio.")
J_AD = (155.60, 183.75, "jon", "Pues lo habitual es que… lo habitual es, cuando llega con retraso la maleta y no la entregan al momento, que te la envíen luego al domicilio que tú has facilitado. Eso suele ser lo habitual. Ahora, como comentaba también al principio de la conexión, viendo el caos que existe, pues no sé yo qué medios van a tener para poder hacer eso. Lo más normal, ya digo, es que la manden al domicilio que se facilita, mediante cualquier empresa de entrega de paquetes.", {"enc": [[155.60, 157, 78, 340], [160.80, 0, 190, 518]]})
J_QA = (237.90, 246.30, "pasajero", "¿Me podría decir cuánto pagan por maleta perdida y por el contenido? No sé cuánto será el total, pero si me lo puede explicar, perfecto.")
J_AA1 = (252.85, 304.20, "jon", "Cuando ocurre cualquier incidencia con la maleta, ya sea una entrega tardía, una pérdida o una entrega con la maleta dañada, existe el derecho a una indemnización. Digamos que se puede dividir en dos partes la indemnización. Por una parte sería el daño material, que es un poco las compras o lo que has tenido que adquirir por la pérdida o por la entrega tardía de esa maleta. Porque, por ejemplo, el ejemplo que tú comentabas: te vas de vacaciones, ahora, por ejemplo, en invierno, a un destino en el que la temperatura suele ser baja en estas fechas; pues no cuentas con tus prendas de abrigo, obviamente no vas a pasarte cinco o seis días, ni siquiera tres, sin prenda de abrigo, sin ropa de abrigo. Entonces tienes que adquirir una serie de bienes; entonces esos gastos materiales nos los tendría que abonar la compañía.")
J_AA2 = (304.40, 335.35, "jon", "Y luego, por otra parte, estaría el otro 50 %, o la otra parte, que sería la indemnización moral, que es todos los percances, toda la molestia que te ha supuesto estar sin tu maleta, estar pendiente de que te la entreguen, etcétera. En principio, el máximo estipulado por la ley va variando, pero ahora mismo rondaría los 1.500 euros. Pero bueno, luego siempre puede haber excepciones: depende de lo grave que haya sido esa pérdida o de los daños morales que nos haya causado.")
J_AA3 = (319.45, 335.35, "jon", "En principio, el máximo estipulado por la ley va variando, pero ahora mismo rondaría los 1.500 euros. Pero bueno, luego siempre puede haber excepciones: depende de lo grave que haya sido esa pérdida o de los daños morales que nos haya causado.")
J_QB = (342.00, 347.10, "pasajero", "Sí, a ver: si me cancelan el vuelo, ¿tendría derecho a algún hotel o alguna cosa o algo así?")
J_AB = (351.30, 393.25, "jon", "Sí, siempre. Esa es la primera obligación que tiene la compañía: cuando sucede un retraso, una cancelación, tiene un deber de asistencia mínimo, ¿no? Ese deber de asistencia mínimo consiste en alojamiento, si tienes que pasar la noche fuera; en un vuelo alternativo hacia tu destino, porque se te ha cancelado o se ha retrasado; y también en los gastos de comida, en manutención. Por tanto, la compañía siempre está obligada a ofrecerte esa asistencia mínima. Si no te lo ofrece y lo tienes que adquirir por tus medios, es decir, te pagas tú el hotel, por ejemplo, en el caso de la pregunta que hacía este pasajero, luego la compañía estaría obligada a abonar ese hotel.")
J_QC = (404.90, 412.70, "pasajero", "Cuando me cancelan un vuelo, ¿tengo derecho a coger el siguiente, o me reembolsan, o me colocan en otro lado?", {"enc": [162, 0, 700]})
J_AC1 = (419.55, 440.80, "jon", "Sí, un poco lo que comentaba: es otra de las obligaciones básicas. Cuando pierdes un vuelo, bueno, pierdes… se retrasa, o pierdes una conexión, o se te cancela, tienen que, obviamente, trasladarte a tu destino en otro vuelo alternativo. Si no te lo ofrecen y lo adquieres por tus propios medios, tienen que abonártelo.")
J_AC2 = (449.95, 477.20, "jon", "Lo explico también: además de ese deber mínimo que hemos explicado, de manutención, alojamiento y vuelo alternativo, existe el derecho a la indemnización. Aparte de las maletas, que ya lo hemos explicado, cuando un vuelo se cancela o se retrasa se genera automáticamente un derecho a indemnización, que la cantidad además ya viene estipulada: depende de la distancia entre aeropuertos. Por tanto, un mínimo de asistencia, por una parte, y por otra parte, el derecho a ser indemnizados.")

# ---------------------------------------------------------------- En Jake (ETB2), 7 de julio de 2022
O_QA = (43.95, 53.10, "presentador", "¿Cuál es el clásico? ¿Cuál es la reclamación clásica? ¿Los retrasos, la cancelación, la pérdida de equipaje? ¿Qué es lo que más os lleva a vosotros a reclamar?")
O_AA = (53.75, 75.42, "oscar", "Es que yo diría que todo. Es que es muy complicado decir. Retrasos es más fácil, porque al final un vuelo que llegue tarde… hay muchas dudas con ello, porque ya sabéis que para poder pedir una indemnización el retraso tiene que ser superior a tres horas en el destino. Hay mucha gente que tiene unas horas menos; entonces nos llama para preguntar, y entonces igual no puede reclamar.")
O_QB = (90.50, 93.45, "presentador", "¿Suelen responder bien las compañías a vuestras reclamaciones o no?")
O_AB = (94.62, 126.45, "oscar", "Pues tenemos de todo, y hay compañías de todo tipo, o sea, diferentes, pero también épocas. No sabemos por qué, hay épocas en las que igual al consumidor, con una reclamación, se le contesta favorablemente, y notamos eso más, pero hay otras que se cierran en banda. Y entonces, en ese caso, solo te queda poder llevarlo a una vía judicial o presentar una demanda, que es un poco, principalmente, el trabajo que nosotros realizamos; es decir, cuando el consumidor por sí mismo no puede conseguir sus derechos, pues entramos nosotros un poco en juego para conseguirlos, ¿no?")
O_QC = (163.05, 182.10, "presentador", "¿Ellos suelen explicar por qué les ha pasado? Porque la sensación que tenemos muchas veces los viajeros, cuando hay un retraso, cuando se cancela un vuelo, es que nos falta información y nunca nos llegamos a enterar de verdad por qué lo han retrasado. Dicen: «No, pues problemas operativos». ¿Exactamente qué es eso? ¿A vosotros os explican qué es lo que ha sucedido?")
O_AC = (183.20, 215.85, "oscar", "Sí, ese es uno de los problemas que nos encontramos. Una de las obligaciones que tienen las compañías es informar a su cliente, y eso es algo que muchas veces sí que vemos, una falta que es general. Y muchas veces vemos que hay una cierta picaresca de poner excusas como exoneratorias de responsabilidad para la compañía, cuestiones externas a la compañía; pero luego, realmente, cuando vas al proceso o presentas la demanda, te das cuenta de que no, de que muchas veces la compañía tiene que indemnizar y hace caso omiso. Eso sí que vemos, y eso es bastante generalizado.")
O_QD = (216.30, 222.30, "presentador", "A ver, unos consejos rápidos antes de acudir a Erreklamatu: ¿qué tenemos que llevar?")
O_AD = (231.30, 265.25, "oscar", "Sí, a ver, es muy sencillo. Si realmente guardas la documentación, es decir, reservas y tarjetas de embarque, con un retraso realmente ya puedes reclamar, y podemos reclamar enviándonos un e-mail, y nosotros podemos realizar esa reclamación. Pero luego hay veces que hay gastos extra, por ejemplo un hotel, comida, etcétera. Eso también podemos reclamarlo; ahí hay que guardar las facturas. Lo más importante es guardar toda la documentación: tarjetas de embarque, tiques de compra, reclamaciones, si se han hecho previas, también. Con esa documentación, si se nos envía, nosotros podemos llevar adelante sin ningún tipo de problema la reclamación.")
O_AD1 = (231.30, 243.70, "oscar", "Sí, a ver, es muy sencillo. Si realmente guardas la documentación, es decir, reservas y tarjetas de embarque, con un retraso realmente ya puedes reclamar, y podemos reclamar enviándonos un e-mail, y nosotros podemos realizar esa reclamación.")

# ---------------------------------------------------------------- Qué me estás contando (ETB2), 25 de noviembre de 2019: equipaje de mano (tiempos de la copia de YouTube)
P_QA = (12.25, 18.85, "presentador", "¿En qué ocasiones tenemos que reclamar? ¿Cuándo nos estamos enfrentando a comportamientos abusivos por parte de estas compañías?")
P_AA = (19.95, 51.85, "oscar", "Arratsalde on. Pues en este caso concreto se ve muy claro, ¿no? Esta sentencia no es nueva, porque el Tribunal de Justicia de la Unión Europea ya se había posicionado en este tema y ya decía que hay obligación de la compañía de tener que llevar, de permitirte llevar un equipaje de mano para poder realizar un viaje en condiciones dignas. Entonces, esto es algo que nos encontramos: nos encontramos muchas situaciones en las que las compañías abusan de sus clientes, vamos a decir, y efectivamente lo que nosotros recomendamos es que hay que reclamar y que se puede ganar.")
P_AB = (65.90, 85.30, "oscar", "Efectivamente, esa es una cultura que poco a poco está entrando y que nosotros cada vez vemos más: cada vez tenemos más clientes que están ya hartos de estas situaciones y que lo que quieren es, aunque sea, que esto no vuelva a pasar. Y esta señora, bueno, son 20 euros, pero el revuelo que en cierta manera se ha montado seguro que sirve para que la gente tenga una conciencia mayor sobre sus derechos.")
P_QC = (85.40, 90.45, "presentador", "¿A qué tenemos derecho, por cierto? ¿Tenemos derecho a llevar un equipaje de mano con nosotros sin que sea facturado o no?")
P_AC = (91.40, 117.90, "oscar", "Sí, sí, sí, tenemos derecho. El problema es que la ley siempre tiene conceptos indeterminados, y este tipo de compañías lo que hacen es estirarlo contra el cliente, contra el pasajero. Pero lo que dice la ley es que tenemos derecho a llevar con nosotros, con nosotras, un equipaje para poder viajar y para poder llevar una ropa básica, etcétera. Lo que está haciendo Ryanair es que puedas llevar un ordenador, pero para nada ropa con la que puedas viajar e ir a un destino.")
P_QD = (124.95, 137.10, "presentador", "¿A qué más tenemos derecho? Por cierto, porque también antes nos obligaban a imprimir la tarjeta de embarque; si no lo hacías, te cobraban. ¿Cuáles son esos comportamientos abusivos que tenemos que tener muy en cuenta?")
P_AD1 = (138.00, 150.38, "oscar", "Derechos hay bastantes, ¿no? Eso que estás comentando con la tarjeta de embarque ya también está resuelto: es un abuso también, no te pueden cobrar, y menos las cantidades que cobran.")
P_AD2 = (150.45, 177.80, "oscar", "Pero luego hay también otros derechos que luego no se ejercitan: cuando hay unos retrasos superiores a tres horas, tienes derecho a indemnización; cuando hay un overbooking, cuando hay cancelaciones, cuando te retrasan la maleta… Es decir, tienes derecho muchas veces a indemnizaciones, a atención, a que te pongan en un hotel, a que te den comida, etcétera. La gente, al no conocerlos, pues muchas veces se queda sin poder ejercitarlos, ¿no? Nosotros lo que hacemos es un poco promocionarlos, en cierta manera, para que la gente los conozca y los pueda reclamar.")
P_AE = (185.50, 194.95, "oscar", "Sí, con nosotros, sin ningún problema. Nosotros solo cobramos en caso de conseguir una indemnización, y si no se consigue una indemnización no cobramos nada por nuestro trabajo, por efectuar reclamaciones de este tipo.")
P_QF = (223.50, 228.85, "presentador", "Vas con tus hijos, te quieres sentar con ellos, no puedes… Por elegir el asiento, ¿también tienen el derecho a cobrarte o no?")
P_AF = (230.00, 254.60, "oscar", "Es legal. Sí que es verdad que es una práctica legal. Lo que es discutible es que se utilice esta práctica para, de una forma casi automática, separar a las personas que compran un billete conjunto. Ahí entiendo yo que todavía hay algo que explorar, porque sí que nos hemos dado cuenta de que muchas compañías lo que están haciendo es eso: es decir, te separan para casi obligarte a pagar un asiento. Y entendemos que eso roza la abusividad con el pasajero.")

# ---------------------------------------------------------------- Está pasando (ETB2), 1 de julio de 2019: huelga en el aeropuerto de Loiu (Óscar Sánchez, por teléfono)
H_Q = (116.45, 122.95, "presentador", "Yo me presento en el aeropuerto un día como hoy y me dicen que no tengo vuelo. ¿Puedo pedir un transporte alternativo a la compañía?")
H_A = (123.28, 141.45, "oscar", "La compañía está obligada a devolverte el billete, si te cancelan un vuelo, o darte un transporte alternativo. Es una obligación de la compañía. En el caso de que no se te ofrezca un vuelo alternativo y tú cojas por tu cuenta un vuelo alternativo, también tendrías derecho a solicitar el dinero que te ha costado. Es una obligación que tienen.", FIJO4)

# ---------------------------------------------------------------- COPE, Mediodía COPE, 8 de junio de 2023: indemnización para un bebé (audio)
X_L1 = (0.35, 13.45, "locucion", "Y ahora que llegan las vacaciones y muchas familias van a coger un avión, es importante saber que los bebés menores de dos años no pagan billete de avión. Pero ¿sabías que también tienen derecho a una indemnización si se retrasa el vuelo?", RAD14)
X_J2 = (96.25, 111.25, "jon", "Si hay una obligación por parte de las aerolíneas a identificar a tu bebé, a que hagas una reserva, a que metas sus datos y a que emitan una tarjeta de reserva, se generan unos derechos; en este caso, uno de esos derechos es también a cobrar la indemnización.")
X_J3 = (134.30, 151.50, "jon", "Pero bueno, ya existe también una regulación que habla de retrasos, de cancelaciones, de denegaciones de embarque, superconsolidada, y que sin embargo las compañías, cuando ocurren ese tipo de incidencias, muchas veces también se oponen al pago de las indemnizaciones.")

# ---------------------------------------------------------------- Radio Popular, EgunOn Magazine, 1 de septiembre de 2023: pasajeros desembarcados por exceso de carga (audio)
Y_Q = (213.90, 217.80, "pregunta", "¿A qué tienen derecho estos trabajadores que tuvieron que ser expulsados del avión?", RAD3)
Y_A = (219.45, 269.80, "jon", "Pues bueno, lo primero es lo que corresponde, una asistencia básica, digamos, que fue así: fue el traslado en un vuelo alternativo, más la manutención que necesiten en ese momento. Y luego, como en los casos que mencionaba también, que se dé un overbooking, y también con los casos que se dan cancelaciones, etcétera, se tiene derecho a una indemnización, una indemnización que siempre se establece dependiendo de la distancia entre aeropuertos. Por tanto, así como los gastos generados, serían tres conceptos: una asistencia mínima, que es el traslado a su destino más la comida que necesiten en ese tiempo en el que se ven afectados; la indemnización por ese percance, y luego los gastos extras soportados por no llegar a su destino a tiempo, los costes que les ha podido acarrear.")
Y_B1 = (128.00, 148.10, "jon", "Sí, efectivamente, al final no se trata más que de otra mala gestión de la compañía. En este caso estamos hablando de un exceso de carga, pero bueno, esto derivó en… la palabra técnica que todos conocemos es un overbooking, que es, al final, que no te dejen embarcar pese a cumplir con todas las condiciones.")
Y_B2 = (157.20, 163.15, "jon", "Tenemos que recordar que los overbookings se dan también porque las compañías venden más billetes de los que tienen.")

# ---------------------------------------------------------------- Radio Euskadi, Boulevard, 4 de agosto de 2023: cobro del equipaje de mano (audio)
Z_Q = (40.20, 49.15, "pregunta", "Creo que la Ley de Navegación Aérea ya contempla que el precio del billete de avión incluye el equipaje de mano, de hasta 10 kilos de peso, pero pese a todo se ha seguido cobrando.", RAD11)
Z_A = (50.45, 84.85, "oscar", "Eh, sí. Se establece en la Ley de Navegación Aérea que el equipaje de mano es una parte del precio del billete, pero no dice efectivamente que sean 10 kilos lo que se pueda llevar. Y ahí, en esa indefinición, es donde las compañías tratan de jugar con la picaresca. Porque se establece que el equipaje de mano, que es lo que necesitas para un viaje, debe ir contigo sin un coste adicional; pero claro, ¿cuánto es ese equipaje de mano? ¿Son 10 kilos? ¿Son 5? Yo creo que ahí entra un poco la picaresca de las compañías.")

# ---------------------------------------------------------------- Informativos de EITB, enero de 2021: reclamaciones en la pandemia (versión en castellano de la pieza de PUB-0063)
W_L1 = (71.85, 74.95, "locucion", "También el último temporal ha cancelado y recolocado infinidad de vuelos.", {"enc": [420, 0, 1080]})
W_J = (74.95, 92.59, "jon", "Un alojamiento, si es necesario, para pasar la noche, y luego un vuelo alternativo para regresar a tu hogar. Si es el propio cliente el que tiene que buscar un vuelo alternativo para volver a su destino, pues todos esos gastos los tendría que afrontar la compañía. Y, además de eso, el importe que ha supuesto ese viaje que finalmente no has utilizado.", FIJO11)
W_L2 = (92.64, 102.45, "locucion", "En circunstancias extraordinarias, como en temporales y la covid, nos corresponde recuperar lo gastado. Si la causa es ordinaria, culpa de la aerolínea, podemos incluso pedir una compensación.", {"enc": [[92.60, 420, 0, 1080], [101.80, 0, 0, 1080]]})

P = {"principal": "oscar"}; PJ = {"principal": "jon"}
C = [
 ("v9", "PUB-0180", "Reforma 261", ["2025: «Es ceder a la", "presión de las aerolíneas»"], [N_J3B], {}),
 ("v9", "PUB-0181", "Reforma 261", ["2025: con 4 horas, el 70 %", "se quedaba sin cobrar"], [N_Q2, N_J2], PJ),
 ("v9", "PUB-0182", "Reforma 261", ["2025: el recorte que la UE", "quiso aplicar al pasajero"], [N_J1], {}),
 ("v9", "PUB-0183", "Reforma 261", ["2025: ¿a quién beneficiaba", "el recorte de la UE?"], [N_Q3, N_J3A, N_J3B], PJ),
 ("v10", "PUB-0184", "Temporales", ["Vuelo cancelado por", "temporal: tus derechos"], [K_Q1, K_A1], P),
 ("v10", "PUB-0185", "Temporales", ["Te ponen un autobús:", "¿puedes pedir el dinero?"], [K_Q2, K_A2, K_Q2B, K_A2B], P),
 ("v10", "PUB-0186", "Temporales", ["Dos días sin vuelo:", "guarda las facturas"], [K_Q3, K_A3], P),
 ("v10", "PUB-0187", "Conexiones", ["Pierdes el enlace: cuenta", "el destino final"], [K_Q4, K_A4], P),
 ("v10", "PUB-0188", "Temporales", ["Temporal o avería: cuándo", "hay indemnización"], [K_Q5, K_A5], P),
 ("v10", "PUB-0189", "Derechos", ["La aerolínea está", "obligada a informarte"], [K_Q6, K_A6], P),
 ("v10", "PUB-0190", "Temporales", ["Medianoche, sin hotel", "y en el aeropuerto"], [K_Q7, K_A7], P),
 ("v1", "PUB-0191", "Equipaje", ["Maleta con retraso:", "¿te la llevan a casa?"], [J_QD, J_AD], PJ),
 ("v1", "PUB-0192", "Equipaje", ["Maleta perdida: qué", "indemnización te toca"], [J_QA, J_AA1, J_AA2], PJ),
 ("v1", "PUB-0193", "Equipaje", ["Tu maleta no llega: los", "gastos van a la aerolínea"], [J_AA1], {}),
 ("v1", "PUB-0194", "Equipaje", ["Maleta perdida: el máximo", "ronda los 1.500 euros"], [J_QA, J_AA3], PJ),
 ("v1", "PUB-0195", "Cancelaciones", ["Vuelo cancelado: ¿me", "tienen que pagar el hotel?"], [J_QB, J_AB], PJ),
 ("v1", "PUB-0196", "Cancelaciones", ["Vuelo cancelado: ¿otro", "vuelo o el dinero?"], [J_QC, J_AC1], PJ),
 ("v1", "PUB-0197", "Derechos", ["Asistencia e indemnización:", "dos derechos distintos"], [J_AC2], {}),
 ("v2", "PUB-0198", "Retrasos", ["Retraso: más de 3 horas", "en destino para reclamar"], [O_QA, O_AA], P),
 ("v2", "PUB-0199", "Reclamar", ["Cuando la aerolínea", "se cierra en banda"], [O_QB, O_AB], P),
 ("v2", "PUB-0200", "Derechos", ["¿Te explican por qué", "se retrasó tu vuelo?"], [O_QC, O_AC], P),
 ("v2", "PUB-0201", "Reclamar", ["Qué guardar para", "reclamar tu vuelo"], [O_QD, O_AD], P),
 ("v2", "PUB-0202", "Reclamar", ["Reserva y tarjeta de embarque:", "con eso ya puedes reclamar"], [O_AD1], {}),
 ("v3", "PUB-0203", "Equipaje de mano", ["Equipaje de mano: hay que", "reclamar y se puede ganar"], [P_QA, P_AA], P),
 ("v3", "PUB-0204", "Reclamar", ["Reclamar aunque", "sean 20 euros"], [P_AB], {}),
 ("v3", "PUB-0205", "Equipaje de mano", ["¿Tienes derecho a llevar", "equipaje de mano?"], [P_QC, P_AC], P),
 ("v3", "PUB-0206", "Abusos", ["Cobrar por la tarjeta de", "embarque es un abuso"], [P_QD, P_AD1], P),
 ("v3", "PUB-0207", "Derechos", ["Los derechos del pasajero", "que no se reclaman"], [P_AD2], {}),
 ("v3", "PUB-0208", "Reclamar", ["Solo cobramos si", "consigues indemnización"], [P_AE], {}),
 ("v3", "PUB-0209", "Asientos", ["Pagar por sentarte con", "tus hijos: ¿es legal?"], [P_QF, P_AF], P),
 ("v4", "PUB-0210", "Huelgas", ["Huelga y vuelo cancelado:", "¿me dan otro transporte?"], [H_Q, H_A], P),
 ("a14", "PUB-0211", "Bebés", ["Un juzgado: el bebé también", "cobra si el vuelo se retrasa"], [X_L1, X_J2], PJ),
 ("a14", "PUB-0212", "Reclamar", ["La norma es clara y aun", "así se resisten a pagar"], [X_J3], {}),
 ("a3", "PUB-0213", "Overbooking", ["Te bajan del avión: los", "tres conceptos a reclamar"], [Y_Q, Y_A], PJ),
 ("a3", "PUB-0214", "Overbooking", ["Overbooking: no embarcas", "aunque cumplas todo"], [Y_B1, Y_B2], {}),
 ("a11", "PUB-0215", "Equipaje de mano", ["El equipaje de mano va", "en el precio del billete"], [Z_Q, Z_A], P),
 ("v11", "PUB-0216", "Temporales", ["Vuelo cancelado por temporal:", "lo que debe darte la aerolínea"], [W_L1, W_J, W_L2], PJ),
]
