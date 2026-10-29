# Clips de los cinco vídeos recibidos el 6 de octubre de 2026. Cada tramo: (inicio, fin, quien, texto corregido a partir de UNA transcripción automática), o con un quinto dato: opciones del tramo (por ejemplo {"enc": [...]}).
S = "/tmp/claude-0/-home-claude-erreklamatu-rrss/049ce1e0-2613-5255-8bf4-bbf49454531a/scratchpad"
N5 = S + "/n5"
JON = r"{\b1}Jon Ortiz{\b0}  ·  Abogado de Erreklamatu"
AIN = r"{\b1}Ainhoa Egiluz{\b0}  ·  Equipo jurídico de Erreklamatu"

V = {
 "tv": dict(video=N5 + "/src/tv.mp4", audio=N5 + "/tv.wav", credito="Imágenes: TVE", preguntan=["locucion"], prefijo="",
            rotulos={"jon": JON, "locucion": r"{\b1}Informativo de TVE{\b0}  ·  con Jon Ortiz, de Erreklamatu"},
            enc={"jon": ["mayor"], "locucion": [316, 30, 648]},
            marco={"lado_pleno": 720, "lado_ventana": 720, "sin_cara": [316, 30, 648], "planos": "cortes", "cara_min": 0.2}),
 "ej": dict(video=N5 + "/ej.n.mp4", audio=N5 + "/ej.wav", credito="Imágenes: EITB · programa En Jake", cierre_lineas=["Consulta gratuita", "Primero analizamos tu caso"],
            rotulos={"jon": JON, "reportera": "Pregunta del programa", "presentador": "Presentador del programa"},
            enc={"jon": ["izq"], "reportera": ["izq"], "presentador": ["der"]},
            marco={"lado_izq": 560, "lado_der": 520, "lado_pleno": 700, "techo": 80, "sin_cara": [0, 103, 556]}),
}

# ---------------------------------------------------------------- TVE · huelga del personal de tierra (enero de 2024)
T_LOC1 = (38.37, 42.00, "locucion", "Este paisaje de maletas solitarias tiene muchas historias detrás.")
T_JON2 = (42.10, 64.29, "jon", "Muchas veces tengo que comprar cosas que llevaba en la maleta; me voy tres días, tres semanas, lo que sea, el tiempo que sea de vacaciones. No cuento con los abrigos que llevaba, por ejemplo; ahora, en época invernal, tengo que comprarme algún abrigo. La ley establece un máximo, en principio, que serían alrededor de 1.500 euros, pero luego hay casos especiales, por ejemplo cuando haces una declaración de especial valor de lo que llevas en la maleta.")
T_LOC3 = (64.49, 69.78, "locucion", "¿Y si en esa maleta iba una herramienta de trabajo? ¿Y si he perdido dinero por ese retraso en su entrega?")
T_JON3A = (70.05, 77.83, "jon", "Todo lo que se pueda acreditar y tenga cierta lógica: los gastos que has tenido, el dinero que has perdido y luego la molestia que te ha supuesto.", {"video": N5 + "/tv.pad.mp4", "enc": [[70.05, 316, 30, 648], [76.44, 46, 0, 900]]})
T_JON3B = (78.30, 83.77, "jon", "En la mayoría de los casos, en el noventa y pico por ciento de los casos, se obtiene una indemnización.", {"video": N5 + "/tv.pad.mp4", "enc": [[78.30, 46, 0, 900], [81.32, 316, 30, 648]]})
T_JON4 = (87.47, 98.51, "jon", "Perfectamente puede darse que te la entreguen con un mes de retraso o que no te la entreguen. La ley establece que a partir de los 21 días en que no has recibido la maleta se puede considerar por perdida.", {"video": N5 + "/tv.pad.mp4", "enc": [[87.47, 316, 30, 648], [91.76, 0, 40, 600], [94.56, 96, 0, 900], [96.88, 316, 30, 648]]})

# ---------------------------------------------------------------- En Jake (ETB2), 17 de marzo de 2025
E_INTRO = (5.54, 11.14, "reportera", "Para saber todas esas cosas estamos con Jon Ortiz, de Erreklamatu, servicio vasco de reclamaciones.", {"enc": [[5.54, 541, 207, 378], [6.28, 767, 191, 470]]})
E_Q1 = (11.54, 26.87, "reportera", "Jon, por primera vez el sector bancario es el que más reclamaciones recibe y ha desbancado a la telefonía, las telecomunicaciones, que era el que estaba siempre en el primer puesto. Los vascos nos animamos a reclamar. ¿Vosotros también notáis ese volumen de reclamaciones en el sector bancario?")
E_A1 = (27.36, 42.15, "jon", "Nosotros llevamos ya varios años con este tipo de reclamaciones, pero es verdad que justamente de un año aquí hubo un boom importante en este tipo de reclamaciones, sobre todo a raíz de una sentencia del Tribunal Supremo, y sí, han subido mucho ese tipo de reclamaciones.")
E_Q2 = (42.40, 52.62, "reportera", "Me contabas antes que tenéis reclamaciones que se han puesto de hipotecas de 2018 y otras más recientes, y las recientes sí que se han solucionado; las de 2018, no. ¿Cómo se explica esto?")
E_A2A = (52.94, 62.11, "jon", "Al final influyen bastantes factores. Nosotros lo que hacemos, además estamos obligados por ley, es intentar una vía extrajudicial, un acuerdo previo, y no judicializar el tema.")
E_A2B = (62.61, 77.05, "jon", "Además, por el bien de los clientes y porque no se alargue. Pero es verdad que en ocasiones, cuando las entidades no aceptan las pretensiones o no aceptan lo que solicitamos, hay que judicializar el tema. Ahí entran varios factores y algunos procesos se pueden alargar.")
E_Q3 = (78.02, 88.78, "reportera", "¿Qué garantía de éxito hay si nosotros venimos primero a consultar y luego a interponer una reclamación? ¿Hay garantía de éxito, para que la gente se anime a venir a reclamar, o no?")
E_A3 = (89.42, 105.89, "jon", "Hombre, pues en esta materia que estamos comentando, concretamente, sí. Además, hay que tener en cuenta que nosotros lo que hacemos es un estudio previo del caso y ofrecemos a los clientes y a las clientas una serie de garantías, en las que en la mayoría de los casos los procesos se resuelven.")
E_Q4 = (106.40, 120.01, "reportera", "Decía Kontsumobide que el 46 % de las reclamaciones se solucionan a través de un acuerdo, con mediación o avenencia. ¿Vosotros diríais que también es la fórmula que más se utiliza para solucionar esas reclamaciones en vuestro caso?")
E_A4 = (120.47, 147.89, "jon", "Sí, al final todos deseamos que sea así. Al final el cliente o la clienta va a salir beneficiada, porque su reclamación se va a solucionar en un espacio más corto de tiempo. Para nosotros también es más fácil y, además, como comentaba, ahora mismo estamos obligados por ley a realizar ese intento antes que llevar el tema a los tribunales o a los juzgados, que, bueno, ahí ya se complica en cuanto a plazos. Por tanto, siempre es lo más aconsejable.")
E_Q5 = (148.24, 155.22, "reportera", "¿De qué plazos estaríamos hablando en el caso de llegar a un acuerdo? Supongo que si se judicializa la cosa se alarga un poco más. ¿De qué plazos hablamos?")
E_A5 = (156.02, 165.88, "jon", "Al final depende un poco también de la entidad a la que reclames, con la que contactes, pero bueno, en el plazo de dos o tres meses este tipo de solicitudes se suelen solucionar sin problema.")
E_Q6 = (166.33, 179.17, "reportera", "El sector bancario, decíamos, ha sido el primero en el ranking este año, pero ¿qué sectores dirías tú que son los que tienen más éxito a la hora de reclamar, de que el consumidor gane esa reclamación?")
E_A6 = (179.96, 197.49, "jon", "Bueno, desde nuestra experiencia, nosotros también somos especialistas en reclamaciones aéreas, y es verdad que es un ámbito en que los derechos de los consumidores y de las consumidoras están bastante protegidos, y eso hace que cuando inicies una reclamación, como he dicho antes, las posibilidades de éxito sean muy altas también.")
E_Q7 = (197.87, 207.20, "reportera", "La última pregunta es para animar a la gente si quiere reclamar o no. ¿Qué es lo que tendría que hacer? Supongo, primero consultar y después ya interponer esa reclamación. ¿Qué es lo que tienen que hacer?")
E_A7A = (207.23, 220.78, "jon", "Sí, lo primero de todo, nosotros siempre solemos decir que es informarse un poco de los derechos que tenemos como consumidores y, a partir de ahí, a través de nuestro servicio o cualquier otro, ponerte en contacto para saber, bueno, qué camino tienes que seguir.")
E_A7B = (221.16, 236.97, "jon", "Luego, a partir de ahí, nuestro primer objetivo es facilitar todo: simplemente con recabar una pequeña documentación, luego nos ocupamos de todo el proceso, y es un poco lo que se busca: que la gente pierda ese miedo a reclamar y que vea que no es un camino tan difícil ni tan complejo, y facilitar las cosas.")
E_FIN = (237.37, 251.24, "reportera", "Eskerrik asko, Jon Ortiz, por atendernos. Ya sabéis que hay que reclamar esos derechos que tenemos como consumidores y, aunque parezca un poco latoso, al final, como nos contaba Jon, en muchas ocasiones es garantía de éxito.", {"enc": [[237.37, 4, 114, 556], [238.9, 900, 240, 500], [240.5, 790, 205, 480], [241.3, 723, 200, 450]]})
E_A7C = (221.16, 236.97, "jon", "Luego, a partir de ahí, nuestro primer objetivo es facilitar todo: simplemente con recabar una pequeña documentación, luego nos ocupamos de todo el proceso, y es un poco lo que se busca: que la gente pierda ese miedo a reclamar y que vea que no es un camino tan difícil ni tan complejo, y facilitar las cosas.")
SOBRE = {"reportera": r"{\b1}En Jake (ETB2){\b0}  ·  con Jon Ortiz, de Erreklamatu"}

C = [
 # ---- TVE
 ("tv", "PUB-0126", "Huelgas", ["Huelga en tu aerolínea:", "qué puedes reclamar"], [
   (15.88, 38.12, "jon", "…que es un motivo propio de la compañía. Podemos reclamar todos los gastos que nos ha supuesto la pérdida del avión: el reembolso o el vuelo que he tenido que comprar para volver a mi destino, o el hotel que he tenido que pagar para alojarme porque me he quedado tirado en cierto sitio, la comida que he tenido que pagar durante esos días; es decir, todos los gastos de asistencia mínimos, que se llaman. Pero, por otra parte, se genera el derecho a la indemnización.")], {}),
 ("tv", "PUB-0127", "Equipaje", ["Sin maleta: lo que", "compras se reclama"], [T_LOC1, T_JON2], {"principal": "jon"}),
 ("tv", "PUB-0128", "Equipaje", ["¿Cuánto pagan por", "una maleta perdida?"], [
   (54.43, 64.29, "jon", "La ley establece un máximo, en principio, que serían alrededor de 1.500 euros, pero luego hay casos especiales, por ejemplo cuando haces una declaración de especial valor de lo que llevas en la maleta.")], {}),
 ("tv", "PUB-0129", "Equipaje", ["Maleta con retraso:", "qué puedes reclamar"], [T_LOC3, T_JON3A, T_JON3B], {"principal": "jon"}),
 ("tv", "PUB-0130", "Reclamar", ["Equipaje: más del 90 %", "logra indemnización"], [T_JON3B], {}),
 ("tv", "PUB-0131", "Equipaje", ["Maleta perdida:", "a partir de 21 días"], [T_JON4], {}),
 ("tv", "PUB-0132", "Equipaje", ["Maleta retrasada o", "perdida: tus derechos"], [T_LOC1, T_JON2, T_LOC3, T_JON3A, T_JON4], {"principal": "jon"}),
 # ---- En Jake 2025
 ("ej", "PUB-0152", "Bancos", ["Reclamaciones al banco:", "un boom en un año"], [E_INTRO, E_Q1, E_A1], {}),
 ("ej", "PUB-0153", "Hipotecas", ["Reclamar al banco:", "primero, un acuerdo"], [E_Q2, E_A2A, E_A2B], {"cierre_lineas": ["Consulta gratuita", "Solo cobramos si ganamos"]}),
 ("ej", "PUB-0154", "Bancos", ["Antes del juzgado,", "intentar un acuerdo"], [E_A2A], {}),
 ("ej", "PUB-0155", "Bancos", ["¿Hay garantía de éxito", "al reclamar al banco?"], [E_Q3, E_A3], {}),
 ("ej", "PUB-0156", "Bancos", ["Acuerdo con el banco:", "más rápido para ti"], [E_Q4, E_A4], {}),
 ("ej", "PUB-0157", "Bancos", ["¿Cuánto tarda una", "reclamación al banco?"], [E_Q5, E_A5], {}),
 ("ej", "PUB-0158", "Bancos", ["Acuerdo con el banco:", "dos o tres meses"], [E_A5], {}),
 ("ej", "PUB-0159", "Vuelos", ["Vuelos: tus derechos", "están muy protegidos"], [E_Q6, E_A6], {"cierre_lineas": ["Consulta gratuita", "Solo cobramos si ganamos"]}),
 ("ej", "PUB-0160", "Reclamar", ["¿Quieres reclamar?", "Por dónde empezar"], [E_Q7, E_A7A, E_A7B], {}),
 ("ej", "PUB-0161", "Erreklamatu", ["Nos ocupamos de", "todo el proceso"], [E_A7C], {}),
 ("ej", "PUB-0162", "Erreklamatu", ["«Reclamar es, muchas", "veces, garantía de éxito»"], [E_FIN], {"rotulos": SOBRE, "preguntan": []}),
 ("ej", "PUB-0163", "Bancos", ["Reclamar al banco:", "garantías y plazos"], [E_Q3, (89.42, 92.54, "jon", "Hombre, pues en esta materia que estamos comentando, concretamente, sí."), E_Q5, E_A5, E_A7C], {}),
]

# ---------------------------------------------------------------- Teleberri (ETB2): reportaje sobre ciberestafas (fecha sin confirmar; hacia septiembre de 2025)
TXARO = r"{\b1}Txaro Ortiz de Zarate{\b0}  ·  Víctima de ciberestafa"
ISK = r"{\b1}Iskander Segurola{\b0}  ·  Jefe de investigación de Ciberseguridad"
TB_AIN = r"{\b1}Teleberri (ETB2){\b0}  ·  con Ainhoa Egiluz, de Erreklamatu"
TB = r"{\b1}Teleberri (ETB2){\b0}  ·  reportaje sobre ciberestafas"
MARCO_REP = {"lado_pleno": 704, "lado_ventana": 704, "lado_min": 420, "sin_cara": [280, 0, 704], "planos": "cortes", "cara_min": 0.09}
V["ps"] = dict(video=N5 + "/ps.n.mp4", audio=N5 + "/ps.wav", credito="Imágenes: EITB · Teleberri", preguntan=["locucion", "presentadora"], prefijo="",
               cierre_lineas=["Consulta gratuita", "Solo cobramos si recuperamos tu dinero"],
               rotulos={"ainhoa": AIN, "txaro": TXARO, "ertzaina": ISK, "locucion": TB, "presentadora": TB},
               enc={"ainhoa": ["mayor"], "txaro": ["mayor"], "ertzaina": ["mayor"], "locucion": ["mayor"], "presentadora": ["mayor"]}, marco=MARCO_REP)
P_PRE_C = (0.48, 7.78, "presentadora", "Ojo con los timos, porque uno de cada cuatro delitos ya ocurre en internet y nueve de cada diez tienen que ver con ciberestafas.")
P_PRE = (0.48, 25.37, "presentadora", "Ojo con los timos, porque uno de cada cuatro delitos ya ocurre en internet y nueve de cada diez tienen que ver con ciberestafas. Las trampas digitales son cada vez más creíbles y además son más sofisticadas, lo que aumenta el riesgo de que cualquiera de nosotros pueda caer en ellas. Un simple clic, una llamada inesperada, responder al teléfono con un sí o un mensaje convincente puede bastar para poner en juego nuestros ahorros y nuestra seguridad.")
P_TX1 = (26.11, 35.23, "txaro", "Pues yo voy a llamar por teléfono a las 9 de la mañana y resulta que no puedo llamar por teléfono. Me dice: «Te falta la tarjeta SIM».")
P_LO2 = (35.54, 43.14, "locucion", "Y así comenzó la pesadilla de Txaro. Los ciberdelincuentes obtuvieron un duplicado de su tarjeta SIM, suplantando su identidad.")
P_TX2 = (43.24, 51.60, "txaro", "«Vives en Barcelona, tienes 47 años». No tenían más que mi nombre y el número de carné de identidad.")
P_LO3 = (51.97, 56.23, "locucion", "Y tras dejarle sin servicio telefónico, tomaron el control de su banca digital.")
P_TX3 = (56.51, 66.05, "txaro", "Han emitido tres tarjetas magnéticas a mi nombre, que hay unos gastos importantes en un comercio, y luego lo más importante lo hizo en Alemania.")
P_LO4 = (66.38, 72.62, "locucion", "En ocho horas le robaron una gran cantidad de dinero. En su caso ha conseguido recuperarlo todo.")
P_TX4 = (72.70, 75.40, "txaro", "Así es. Un poco duro.")
P_ER1 = (81.25, 91.22, "ertzaina", "La inteligencia artificial ha supuesto un avance exponencial en cuanto a la sofisticación. Hacen estafas más dirigidas, a personas con nombre y apellido.")
P_LO5 = (91.52, 95.98, "locucion", "Las ciberestafas suponen ya el 90 % de los delitos informáticos en Euskadi.")
P_ER2 = (96.03, 107.50, "ertzaina", "Se hacen pasar por entidades legítimas, como puede ser un banco, una agencia de paquetería, la propia administración pública; generan una urgencia o una alarma para que actúes con rapidez y no te dé tiempo a pensar.")
P_LO6 = (107.60, 115.64, "locucion", "Este tipo de estafas han provocado una avalancha de demandas. Una reciente sentencia del Supremo ha unificado criterios sobre los casos de phishing.")
P_AIN = (115.68, 131.90, "ainhoa", "…que el banco debe implementar sistemas de seguridad efectivos para que esto no pase y, en el caso de que suceda, tiene que demostrar que no ha habido ningún fallo de seguridad y que ha sido culpa de la propia clienta por actuar de manera negligentemente grave.")
P_LO7 = (132.05, 138.62, "locucion", "Si caemos en la trampa, hay que notificarlo al banco y documentar lo ocurrido de la mejor manera para interponer una denuncia.")
P_ER3 = (138.82, 154.20, "ertzaina", "La principal recomendación: usar contraseñas robustas, cambiarlas a menudo y, sobre todo, muchísimo cuidado con los SMS que recibimos y aquellos que contengan enlaces. Ninguna entidad nos va a mandar un SMS en el que tengamos que ingresar nuestros datos personales o bancarios.")
P_ER3C = (149.40, 154.20, "ertzaina", "Ninguna entidad nos va a mandar un SMS en el que tengamos que ingresar nuestros datos personales o bancarios.")
P_LO8 = (154.32, 159.76, "locucion", "Y es que a nivel mundial se detectan 900 millones de intentos de phishing al año.")
RA = {"locucion": TB_AIN, "presentadora": TB_AIN}
C += [
 ("ps", "PUB-0133", "Phishing", ["Phishing: es el banco", "quien debe demostrarlo"], [P_LO6, P_AIN], {"principal": "ainhoa"}),
 ("ps", "PUB-0134", "Phishing", ["Phishing: el banco debe", "probar tu negligencia grave"], [P_AIN], {}),
 ("ps", "PUB-0135", "Phishing", ["Phishing: quién responde", "y qué hacer si caes"], [P_LO6, P_AIN, P_LO7, P_ER3], {"principal": "locucion", "rotulos": RA}),
 ("ps", "PUB-0136", "Ciberestafas", ["Le duplicaron la SIM", "y le vaciaron la cuenta"], [P_TX1, P_LO2, P_TX2, P_LO3, P_TX3, P_LO4, P_TX4], {"principal": "txaro"}),
 ("ps", "PUB-0137", "Ciberestafas", ["«Te falta la tarjeta SIM»:", "así empezó la estafa"], [P_TX1, P_LO2, P_LO4, P_TX4], {"principal": "txaro"}),
 ("ps", "PUB-0138", "Ciberestafas", ["Así te engañan: prisa", "y un nombre conocido"], [P_ER1, P_LO5, P_ER2], {"principal": "ertzaina"}),
 ("ps", "PUB-0139", "Ciberestafas", ["Se hacen pasar por tu", "banco y te meten prisa"], [P_ER2], {}),
 ("ps", "PUB-0140", "Ciberestafas", ["Si caes en la trampa:", "banco, pruebas, denuncia"], [P_LO7, P_ER3, P_LO8], {"principal": "ertzaina"}),
 ("ps", "PUB-0141", "Ciberestafas", ["Ningún banco te pide", "tus datos por SMS"], [P_ER3C], {}),
 ("ps", "PUB-0142", "Ciberestafas", ["Uno de cada cuatro", "delitos, en internet"], [P_PRE], {"preguntan": []}),
 ("ps", "PUB-0143", "Ciberestafas", ["Uno de cada cuatro", "delitos, en internet"], [P_PRE_C], {"preguntan": []}),
 ("ps", "PUB-0144", "Phishing", ["Phishing: del SMS a", "la sentencia"], [P_PRE_C, P_TX1, P_LO2, P_LO4, P_LO6, P_AIN, P_LO7], {"principal": "locucion", "rotulos": RA}),
]

# ---------------------------------------------------------------- Gaur Egun (ETB1): el mismo reportaje en euskera. BORRADORES: el reconocimiento en euskera no es fiable.
TXARO_EU = r"{\b1}Txaro Ortiz de Zarate{\b0}  ·  Ziberiruzurraren biktima"
VILLA = r"{\b1}David Villa{\b0}  ·  Ertzaintzaren bozeramailea"
AIN_EU = r"{\b1}Ainhoa Egiluz{\b0}  ·  erreklamatu.com"
GE = r"{\b1}Gaur Egun (ETB1){\b0}  ·  ziberiruzurrei buruzko erreportajea"
GE_AIN = r"{\b1}Gaur Egun (ETB1){\b0}  ·  Ainhoa Egiluz, Erreklamatu"
V["pe"] = dict(video=N5 + "/pe.n.mp4", audio=N5 + "/pe.wav", credito="Irudiak: EITB · Gaur Egun", idioma="eu", preguntan=["locucion", "aurkezlea"], prefijo="",
               cierre_lineas=["Kontsulta doan", "Dirua berreskuratzen badugu bakarrik kobratzen dugu"],
               rotulos={"ainhoa": AIN_EU, "txaro": TXARO_EU, "ertzaina": VILLA, "locucion": GE, "aurkezlea": GE},
               enc={"ainhoa": ["mayor"], "txaro": ["mayor"], "ertzaina": ["mayor"], "locucion": ["mayor"], "aurkezlea": ["mayor"]},
               marco={"lado_pleno": 720, "lado_ventana": 720, "lado_min": 430, "sin_cara": [280, 0, 720], "planos": "cortes", "cara_min": 0.09})
G_AUR = (0.10, 18.68, "aurkezlea", "Euskadin gertatzen diren lau delitutatik bat Interneten egiten da. Eta Interneten egiten diren horietatik ia denak iruzurrak izaten dira: hamarretik bederatzi inguru (?). Iruzurgileek gero eta sistema sinesgarriagoak eta hobeak erabiltzen dituzte, eta gero eta errazagoa da gaizkileen sarean (?) erortzea (?).")
G_LO1 = (20.10, 27.50, "locucion", "Sakelako telefonoarekin deirik egin ezin zuela ohartuta, bere telefono-konpainiara joan zen Txaro, azalpen eske.")
G_TX1 = (27.62, 36.89, "txaro", "«Ez, zuk eskatu duzu portabilidadea (?) … zerara, Vodafonera, eta zure SIMa daukate han (?)».")
G_LO2 = (37.11, 46.64, "locucion", "Ziberiruzurgileek bere mugikorraren eramangarritasuna lapurtu zuten. Bere nortasuna usurpatuz, bankuko kontuan sartu ziren gero.")
G_TX2 = (46.94, 59.47, "txaro", "Sortu zituzten (?) hemen (?) … eman zizkieten (?) … txartel bat (?), zerak, erosketak (?) … Hamabi kargu (?) … diru asko lapurtu zidaten (?), bai.")
G_LO3 = (59.82, 68.00, "locucion", "Zorionez, lapurtutako dirutza itzultzea lortu du Txarok. Phishinga da Euskadin gehien egiten den ziberiruzurra.")
G_ER1 = (71.80, 93.81, "ertzaina", "Iruzurgilea, ustezko komunikazio ofizial baten bitartez, konfiantzazko enpresa bezala aurkezten da. Mezu horretan klik egiten baldin badugu, iruzurgilearen sarean erori gara. Normalean haiek beldurra, presioa eta premia sortu nahi dute gure gain, guk pentsatu barik erreakzionatu dezagun.")
G_LO4 = (94.18, 97.33, "locucion", "Baina norena da lapurtutako diruaren erantzukizuna?")
G_AI1 = (97.45, 105.06, "ainhoa", "Azken aldian, egia esan, gero eta jurisprudentzia zabalagoa daukagu kasu hauetan, kontsumitzailearen eskubideen alde egiten duena.")
G_LO5 = (105.54, 117.00, "locucion", "Gorenak atera berri duen epai baten arabera, bankuari dagokio bezeroak zabarkeriaz jokatu duela erakustea. Eta hala, arrazoia eman diote berriki Bilbon bezero bati.")
G_AI2 = (117.14, 128.36, "ainhoa", "Kasu honetan (?) entitateak ez du frogatu emakume honek arduragabekeriaz jokatu duela, eta bankua dela inplementatu behar dituena (?) sistema egokiak, hau ez gertatzeko.")
G_LO6 = (128.68, 135.02, "locucion", "Ziberiruzur baten biktima bagara, lehenengo bankuari komunikatu eta gero salaketa jarri.")
G_ER2 = (135.35, 144.40, "ertzaina", "Gomendioen artean, pasahitz sendoak erabili eta sarri aldatu, baina batez ere, ez egin klik inolako kanpoko esteka susmagarrietan.")
G_LO7 = (144.47, 149.90, "locucion", "Mundu mailan bederatziehun milioi phishing saiakera detektatzen dira urtean.")
GA = {"locucion": GE_AIN}
C += [
 ("pe", "PUB-0145", "Phishing", ["Lapurtutako dirua:", "norena da ardura?"], [G_LO4, G_AI1, G_LO5, G_AI2], {"principal": "ainhoa"}),
 ("pe", "PUB-0146", "Phishing", ["Gero eta epai gehiago", "kontsumitzailearen alde"], [G_LO4, G_AI1], {"principal": "ainhoa"}),
 ("pe", "PUB-0147", "Phishing", ["Bankuak frogatu behar du,", "ez bezeroak"], [G_LO5, G_AI2], {"principal": "ainhoa"}),
 ("pe", "PUB-0148", "Ziberiruzurrak", ["Horrela engainatzen", "zaituzte: presa eta beldurra"], [G_ER1], {}),
 ("pe", "PUB-0149", "Ziberiruzurrak", ["Iruzurra jasan baduzu:", "bankua eta salaketa"], [G_LO6, G_ER2, G_LO7], {"principal": "ertzaina"}),
 ("pe", "PUB-0150", "Ziberiruzurrak", ["SIMa bikoiztu eta", "kontua hustu zioten"], [G_LO1, G_TX1, G_LO2, G_TX2, G_LO3], {"principal": "txaro"}),
 ("pe", "PUB-0151", "Ziberiruzurrak", ["Lau delitutatik bat,", "Interneten"], [G_AUR], {"preguntan": []}),
]

# ---------------------------------------------------------------- EITB, hacia el 7 de septiembre de 2017: «Vuelos low cost: ¿salen caros?»
ESP = r"{\b1}Consulta de un espectador{\b0}  ·  EITB (2017)"
V["av"] = dict(video=N5 + "/src/av.mp4", audio=N5 + "/av.wav", credito="Imágenes: EITB (2017)",
               rotulos={"jon": JON, "espectador": ESP},
               enc={"jon": ["der"], "presentador": ["izq", "mayor"], "espectador": ["izq", "mayor"]},
               marco={"lado_der": 232, "lado_izq": 240, "lado_pleno": 300, "techo": 56, "sin_cara": [412, 69, 228]})
A_INTRO = (1.54, 15.94, "presentador", "Jon Ortiz Larruzea, arratsalde on. Él es abogado de Erreklamatu. Ya el nombre de la empresa lo dice todo. Yo me acuerdo cuando la conocí: bueno, pues dice «reclama tú». Si tienes algo para reclamar, vete a donde ellos, que lo hacen, y cómo lo hacen.")
A_MANO = (53.70, 66.32, "jon", "Ahora mismo, ¿la normativa qué dice al respecto? La normativa dice que el equipaje es un elemento inherente al pasajero y que no se puede cobrar un extra, como en este caso, por llevarlo con nosotros.")
A_NORQ = (88.49, 109.84, "presentador", "Oye, Jon, ¿no hay una norma que regule todo? Te quiero decir, porque todos, bueno, casi todos, me imagino, habremos viajado en avión: según la línea que te toque o con la que hayas… es decir, según el billete que hayas comprado, según en qué línea, las normas cambian en cuanto al equipaje, la política de equipaje es diferente. ¿No hay una norma que obligue, que estandarice todo?")
A_NORA = (111.15, 131.75, "jon", "Sí, efectivamente, tienes razón. Bueno, entendemos que la normativa intenta regular la mayoría de los aspectos, pero bueno, como bien vemos, al final van surgiendo, con el paso del tiempo o cuando aparecen nuevas líneas de low cost, como habéis comentado, nuevas cláusulas; entonces, bueno, no sé cómo hacer frente a esas cláusulas o cómo se va a regular.")
A_HABQ = (177.41, 193.34, "presentador", "El tipo de reclamaciones, las reclamaciones más habituales. Sobre todo, y corrígeme, Jon, están los retrasos y cancelaciones, lo que tiene que ver con las maletas y el overbooking. La primera, la más habitual, es retrasos y cancelaciones en vuelos, por ejemplo.", {"video": N5 + "/av.pad.mp4", "enc": [[177.41, 107, 59, 232], [182.25, 0, 0, 640]]})
A_HABA = (193.55, 217.23, "jon", "Efectivamente, sí. Yo creo que las habéis recogido bien, e incluso el orden en el que las habéis recogido es el adecuado, en ese orden, sí. Los retrasos y las cancelaciones están al orden del día. También, por desgracia, el tema de maletas extraviadas o maletas dañadas, y quizá, por último, igual en menos cantidad, pero también los overbooking, efectivamente, sí.", {"video": N5 + "/av.pad.mp4", "enc": [[193.55, 0, 0, 640], [202.8, 430, 82, 210]]})
A_VER = (217.40, 224.96, "jon", "Y lo que tú decías, obviamente: ahora nosotros en verano tenemos un repunte interesante de casos que atender, porque obviamente es la época del año donde más gente viaja.")
A_3HQ = (242.73, 258.70, "presentador", "El tema de si se llega a destino con más de tres horas de retraso: tienes derecho a lo que se llama indemnización básica, y ahí aparece entre 250 y 600. ¿En base a qué, Jon, ese dinero, esa horquilla?")
A_3HA1 = (258.72, 268.02, "jon", "Eso es. El retraso, efectivamente, tiene que superar, y como bien has dicho tú, en la hora de llegada, no en la de salida, la hora que llega el avión a su destino tiene que superar las tres horas.")
A_3HA2 = (268.68, 280.75, "jon", "Y esa indemnización básica a la que haces referencia, efectivamente, varía dependiendo de la distancia entre el origen y el destino, donde has iniciado tu trayecto y donde lo finalizas. Dependiendo de esa distancia,")
A_3HA3 = (281.04, 295.37, "jon", "las indemnizaciones son de 250 euros para trayectos de menos de 1.500 kilómetros, de 400 euros para trayectos de entre 1.500 y 3.500 kilómetros y de 600 euros para trayectos que superen los 3.500 kilómetros.")
A_3HA3C = (281.04, 295.37, "jon", "Las indemnizaciones son de 250 euros para trayectos de menos de 1.500 kilómetros, de 400 euros para trayectos de entre 1.500 y 3.500 kilómetros y de 600 euros para trayectos que superen los 3.500 kilómetros.")
A_GA0 = (295.79, 302.56, "jon", "Eso es lo que, como tú cuentas, la indemnización básica. Luego, bueno, hay otra serie de gastos reclamables, gastos añadidos que hayas podido tener, u otro tipo de percances.")
A_GAQ = (302.83, 315.12, "presentador", "Bien, pues fíjate, sí que parece ser que la compañía está obligada, en el caso de que haya retrasos, a pagar siempre o indemnizar siempre los gastos de dietas, noches de hotel, desplazamientos al hotel y un vuelo alternativo.")
A_GA1 = (316.47, 330.18, "jon", "Efectivamente, sí. Bueno, esos son una serie de gastos extra que tú puedas tener. Es decir, las indemnizaciones que antes comentábamos son las que hacen frente a la molestia, al daño que has sufrido: las indemnizaciones.")
A_GA2 = (330.86, 345.38, "jon", "Y luego, aparte, se indemnizan los gastos materiales que hayas podido tener; es decir, una noche de hotel o dos que por llegar tarde a tu destino no has podido disfrutar, un coche de alquiler que tenías contratado, que no has podido disfrutar y lo tenías pagado, es decir, has perdido ese dinero, o un viaje en autobús.")
A_GA3 = (345.66, 356.23, "jon", "Si, por ejemplo, los que residimos aquí en Bilbao, imagínate que llegamos a Madrid, tenemos un bus contratado, no podemos cogerlo y tenemos que tomar otro: ese gasto extra, todo gasto extra que pueda suponer el retraso.")
A_ES1 = (411.36, 414.41, "espectador", "Bueno, yo tenía vuelo de Alicante a Turín el día 5.", {"enc": [195, 0, 250]})
A_ES2 = (422.79, 433.55, "espectador", "Lo cierto es que cuando llegué al aeropuerto nos comentaron que había un retraso nada más y nada menos de siete horas, con lo cual perdí la conexión a Turín vía Barcelona.", {"sin_cara": [195, 0, 250]})
A_ES3 = (450.75, 452.82, "espectador", "Pues me dieron el vuelo para el día siguiente.")
A_ES4 = (506.97, 516.50, "espectador", "En la reclamación me responden que no tengo derecho a ninguna compensación, puesto que en el vuelo que realmente he utilizado, que es el del día 6, no he tenido retraso.")
A_CA1 = (523.99, 536.64, "jon", "Bueno, sí, lo primero: lo que él menciona son dos incidencias diferentes. Primero ha sufrido un retraso, que luego le ha supuesto llegar a su destino un día más tarde, y luego está el tema de las maletas.")
A_CA2 = (537.36, 555.11, "jon", "Por una parte, el retraso: si las causas de ese retraso son efectivamente achacables a la compañía, como la mayoría de las veces es así, tiene derecho a una indemnización. En este caso, de Alicante a Turín, si no me equivoco, creo que son menos de 1.500 kilómetros; bueno, serían 250 por pasajero.")
A_MA1 = (569.44, 590.39, "jon", "Y luego, pues, el tema de las maletas: las cantidades con las que indemnizan a los pasajeros no están establecidas. Por tanto, luego se trataría de hacer una valoración del daño que ha supuesto no contar con la maleta, y bueno, se hace una similitud y se hace, por una parte, el daño, la molestia que te ha supuesto no contar con tus maletas, la preocupación, la angustia, etcétera.")
A_MA2 = (590.78, 613.20, "jon", "Y luego, por otra parte, si has tenido algún gasto material: muchas veces tenemos casos de personas que se van de vacaciones y se pasan, si van una semana de vacaciones, se pasan toda la semana o cinco días de esa semana sin su maleta y, por tanto, tienen que adquirir otras prendas para pasar esa semana, y esos gastos materiales, que se llaman así, pues esos también serían reclamables.")
A_INV = (633.40, 642.58, "jon", "Yo invito a José Antonio a… bueno, que si por sus propios cauces no consigue nada, bueno, que contacte con nosotros, que estaremos encantados de ayudarle.")
A_COM = (643.81, 645.74, "presentador", "Fíjate qué buen comercial es Jon.")
EN_EITB = {"presentador": r"{\b1}En EITB (2017){\b0}  ·  sobre Erreklamatu"}
C += [
 ("av", "PUB-0164", "Erreklamatu", ["«El nombre de la", "empresa lo dice todo»"], [A_INTRO], {"rotulos": EN_EITB, "preguntan": []}),
 ("av", "PUB-0165", "Equipaje de mano", ["¿Pueden cobrarte por", "la maleta de cabina?"], [A_MANO], {}),
 ("av", "PUB-0166", "Vuelos", ["Las tres reclamaciones", "aéreas más habituales"], [A_HABQ, A_HABA], {}),
 ("av", "PUB-0167", "Retrasos", ["Más de 3 horas tarde:", "de 250 a 600 euros"], [A_3HQ, A_3HA1, A_3HA2, A_3HA3], {}),
 ("av", "PUB-0168", "Retrasos", ["250, 400 o 600 euros:", "depende de la distancia"], [A_3HA3C], {}),
 ("av", "PUB-0169", "Retrasos", ["Las 3 horas cuentan", "a la llegada"], [A_3HA1], {}),
 ("av", "PUB-0170", "Retrasos", ["Además de la indemnización,", "los gastos"], [A_GA0, A_GAQ, A_GA1, A_GA2, A_GA3], {"principal": "jon"}),
 ("av", "PUB-0171", "Retrasos", ["Hotel, coche, autobús:", "lo que pierdes se reclama"], [A_GA2, A_GA3], {}),
 ("av", "PUB-0172", "Caso real", ["Siete horas de retraso…", "y le niegan la compensación"], [A_ES1, A_ES2, A_ES3, A_ES4, A_CA1, A_CA2], {"principal": "jon", "preguntan": ["espectador"]}),
 ("av", "PUB-0173", "Equipaje", ["Maleta que no llega:", "qué se indemniza"], [A_MA1, A_MA2], {}),
 ("av", "PUB-0174", "Equipaje", ["Sin maleta en vacaciones:", "lo que compras se reclama"], [A_MA2], {}),
 ("av", "PUB-0175", "Equipaje", ["Cada aerolínea, su", "política de equipaje"], [A_NORQ, A_NORA], {}),
 ("av", "PUB-0176", "Erreklamatu", ["«Qué buen comercial", "es Jon»"], [A_INV, A_COM], {"principal": "jon", "prefijo": ""}),
 ("av", "PUB-0177", "Retrasos", ["Vuelo con retraso:", "indemnización y gastos"], [A_3HA1, A_3HA3C, A_GA2], {}),
 ("av", "PUB-0178", "Vuelos", ["En verano, más viajes", "y más reclamaciones"], [A_VER], {}),
]
