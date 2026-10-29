# Clips de los dos vídeos de la pandemia (En Jake, ETB2): Óscar Sánchez, 20/05/2020 (v8), y Jon Ortiz, 03/12/2021 (v5). Tanda del 7 de octubre de 2026.
# Cada tramo: (inicio, fin, quien, texto corregido a partir de dos transcripciones automáticas, sin oír el audio).
# El vídeo de cada uno es la versión «en panel» (panel.py): 1080 x 1080, con el abogado siempre en el mismo sitio; por eso el recorte es fijo.
S = "/tmp/claude-0/-home-claude/e7eefa61-a30f-57c7-bc2e-7996fd2458cc/scratchpad"; M = S + "/m8"
JON = r"{\b1}Jon Ortiz{\b0}  ·  Abogado de Erreklamatu"
OSC = r"{\b1}Óscar Sánchez{\b0}  ·  Abogado de Erreklamatu"
OSC20 = r"{\b1}Óscar Sánchez{\b0}  ·  Erreklamatu  ·  mayo de 2020"
V = {
 "v5": dict(video=M + "/src/v5p.mp4", audio=M + "/v5.wav", credito="Imágenes: EITB · En Jake", rotulos={"jon": JON}),
 "v8": dict(video=M + "/src/v8p.mp4", audio=M + "/v8.wav", credito="Imágenes: EITB · En Jake", rotulos={"oscar": OSC}),
}
# ---------------------------------------------------------------- En Jake (ETB2), 3 de diciembre de 2021: Jon Ortiz
J_Q1 = (3.60, 12.45, "presentador", "Jon, hola, ¿qué tal? Bienvenido a En Jake. A ver, esto es muy importante cuando vas a viajar: tener en cuenta dónde vas, porque, claro, la situación es muy dispar según el destino, ¿no?")
J_A1 = (13.62, 32.95, "jon", "Kaixo, egun on. Pues sí, así es, ¿no? Ya habéis hecho un breve resumen vosotros, y ya veis que cada… que cada país, bueno, pues aplica las… el reglamento, la normativa que considera correspondiente, y bueno, pues hay que estar muy bien informados, al detalle, para, bueno, para que el viaje salga lo mejor posible.")
J_A2B = (59.36, 69.75, "jon", "Los requisitos hoy son unos y mañana tranquilamente pueden cambiar. Entonces, bueno, ante eso no queda otra que informarse, informarse y… llevarlo lo mejor posible.")
J_Q3 = (95.55, 112.15, "presentador", "Jon, algo que están haciendo mucho las compañías: cambiar el vuelo. O sea, te llega un mensaje, tú tienes un vuelo cogido y, cada dos por tres, te llega… tal compañía te comunica que tu vuelo saldrá dos horas más tarde o al día siguiente. Ahí, ¿qué puedes hacer y qué no puedes hacer?")
T_A3A = "Efectivamente, es una práctica muy habitual y cada vez más, y bueno, con la pandemia creo que han aumentado estos casos. Bueno, lo primero de todo, estar muy atento a las notificaciones, al canal de notificación que hayas elegido para comunicarte con… con las compañías, ya sea el mail o el móvil o cualquier tipo de comunicación."
T_A3B = "Y bueno, antes, informarte, ¿no? Cuando sucede un cambio de horario, un cambio de programación, con un plazo menor a 14 días, pues bueno, siempre… siempre existe el derecho o bien a… a rehusar ese cambio, porque no te cuadra o no es posible, tu planificación no cuadra con el cambio que te están proponiendo, o… o siempre a optar a la alternativa que te ofrezcan. Por tanto, en caso de que no te interesase dicho cambio, bueno, siempre tendrías la opción del reembolso, ¿no? Entonces, optaríamos o bien por el reembolso o bien por el viaje alternativo que nos… que nos puedan ofrecer."
J_A3 = (113.45, 171.25, "jon", T_A3A + " " + T_A3B)
J_A3B = (134.15, 171.25, "jon", T_A3B)
J_Q4 = (171.98, 183.90, "presentador", "Vale, pero si yo tengo, por ejemplo… Lo normal, además, suele ser, dices: yo tengo el billete del avión, pero es que tengo también cogido el hotel, o el apartamento de destino, o cualquier otra actividad. ¿Qué pasa con eso?")
T_A4A = "Efectivamente, esa es muy buena pregunta, y es lo que nos encontramos día a día. Ahí tendríamos que reparar en cuál ha sido el motivo de dicha cancelación o de dicha desprogramación. En caso de que el problema, bueno, la incidencia, sea achacable a la compañía, pues bueno, se podría generar tanto el derecho al reembolso que he comentado o al viaje alternativo, pero además de eso se podría generar bien un derecho a indemnización y bien un derecho a recuperar todos los gastos que, como tú bien dices, puedes tener ya… puedes haber pagado ya en destino."
T_A4B = "También puede ser que, si la cancelación o la reprogramación de la que estamos hablando se debe a… a motivos no achacables a la compañía, como puede ser el tema del COVID o como puede ser una incidencia meteorológica, pues hay algunas veces en que, por desgracia, esos gastos que ya hemos asumido en destino no podemos recuperarlos o no podemos pedírselos a la compañía. Recuperables… pues bueno, habría que ya comprobar qué tipo de contratación hemos hecho con el hotel correspondiente o con lo que hayamos contratado en el destino, pero no sería achacable a la compañía."
J_A4A = (185.10, 218.20, "jon", T_A4A)
J_A4 = (185.10, 255.30, "jon", T_A4A + " " + T_A4B)
# ---------------------------------------------------------------- En Jake (ETB2), 20 de mayo de 2020: Óscar Sánchez
O_Q1 = (0.15, 14.60, "presentador", "Voy a saludar a Óscar Sánchez, abogado de Erreklamatu, una página especializada precisamente en estas cuestiones. Óscar, hola, bienvenido. Claro, vosotros ya trabajabais antes de lo de la pandemia en las reclamaciones de los vuelos, que es un clásico. Supongo que ahora estaréis con cantidad de trabajo.")
O_A1 = (16.50, 27.00, "oscar", "Sí, es una barbaridad las llamadas que estamos teniendo y… y las consultas que estamos teniendo, porque la gente no es muy conocedora de los derechos que tiene. Es una auténtica barbaridad las llamadas que tenemos.")
O_Q2 = (27.65, 37.40, "presentador", "¿Vosotros qué recomendáis, por ejemplo, a alguien que tenía previsto un vuelo, la compañía de momento no le ha dicho que lo anula, o ha dicho que lo anula, o le ofrece un bono? ¿Qué le estáis aconsejando?")
O_A2A = (38.22, 53.68, "oscar", "Es que las situaciones pueden ser diferentes. Si es un vuelo… sin ningún…, que no sea un viaje combinado, y la compañía te cancela el vuelo, la gente tiene que saber que tiene derecho al reembolso del billete, ¿vale? Es un derecho que tiene.")
O_Q3 = (70.90, 79.45, "presentador", "Posibilidades de acuerdos: en principio es más fácil intentar llegar a un acuerdo que pleitear, aunque vosotros estáis acostumbrados a negociar directamente con las compañías.")
O_A3 = (80.24, 109.95, "oscar", "Sí, sí, nosotros sí que es cierto que recomendamos a los clientes que lo intenten con las compañías; lo que pasa es que nos estamos dando cuenta de que hay muy pocas compañías que estén reembolsando el dinero, y hay mucha gente que quiere el reembolso, ¿no?, porque no está seguro de que vaya a poder viajar, o porque el viaje que iba a hacer era un viaje muy concreto y que no sabe igual si el año que viene lo va a poder realizar, o lo que fuere. Y ahí nos estamos encontrando un bloqueo total, en el que hay muchas compañías que se están negando a… a cumplir con los derechos de los pasajeros, claro.")
O_OUT = (110.72, 119.85, "presentador", "Pues Erreklamatu, una página especializada en reclamaciones, que ya digo que ahora hay cantidad, y ahí le van a poder dar algunas pistas. Óscar, un abrazo muy fuerte, gracias.")
F20 = dict(rotulos={"oscar": OSC20}, credito="Imágenes: EITB · En Jake (20 de mayo de 2020)")
# (vídeo, identificador, kicker, titular, tramos, opciones)
C = [
 ("v5", "PUB-0220", "", ["Te cambian la hora del vuelo:", "¿qué puedes hacer?"], [J_Q3, J_A3], {}),
 ("v5", "PUB-0221", "", ["Cambio de horario del vuelo:", "reembolso o alternativa"], [J_A3B], {}),
 ("v5", "PUB-0222", "", ["Te cancelan el vuelo: ¿y el", "hotel que ya has pagado?"], [J_Q4, J_A4], {}),
 ("v5", "PUB-0223", "", ["Cancelación por culpa de la", "aerolínea: reclama los gastos"], [J_Q4, J_A4A], {}),
 ("v5", "PUB-0224", "", ["Antes de volar, infórmate de", "las normas de tu destino"], [J_Q1, J_A1, J_A2B], {}),
 ("v8", "PUB-0225", "", ["Te cancelan el vuelo: tienes", "derecho al reembolso"], [O_Q2, O_A2A, O_OUT], {}),
 ("v8", "PUB-0226", "", ["2020: aerolíneas que se", "negaban a reembolsar"], [O_Q3, O_A3], F20),
 ("v8", "PUB-0227", "", ["2020: «una barbaridad» de", "consultas por vuelos"], [O_Q1, O_A1], F20),
]
