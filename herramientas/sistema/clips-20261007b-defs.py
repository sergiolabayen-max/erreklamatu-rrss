# Segunda pasada sobre audios y vídeos ya trabajados (7 de octubre de 2026, tarde): los fragmentos aprovechables que quedaron sin montar.
# Cada tramo: (inicio, fin, quien, texto corregido a partir de dos transcripciones automáticas, sin oír el audio[, opciones]).
# Los segundos son los del archivo de la carpeta «Bideoak» de Sergio (los mismos que en las tandas del 6 y del 7 de octubre).
S = "/tmp/claude-0/-home-claude/e7eefa61-a30f-57c7-bc2e-7996fd2458cc/scratchpad"                      # modelo de voz
M = "/tmp/claude-0/-home-claude-erreklamatu-rrss/e7eefa61-a30f-57c7-bc2e-7996fd2458cc/scratchpad/m9"   # carpeta de trabajo
JON = r"{\b1}Jon Ortiz{\b0}  ·  Abogado de Erreklamatu"
OSC = r"{\b1}Óscar Sánchez{\b0}  ·  Abogado de Erreklamatu"
JONR = JON + "  ·  en la radio"; OSCR = OSC + "  ·  en la radio"
CUAD = [0, 0, 1080]

V = {
 # ---- audios de radio: retrato fijo del abogado (fijo/<audio>.mp4) y cartel de la emisora (fijo/<audio>r.mp4)
 "a14": dict(video=M + "/fijo/a14.mp4", audio=M + "/a14.wav", credito="Audio: COPE · Mediodía COPE (8 de junio de 2023)", prefijo="",
             rotulos={"jon": JONR, "locucion": r"{\b1}Mediodía COPE{\b0}  ·  8 de junio de 2023"}, preguntan=["locucion"],
             enc={"jon": CUAD, "locucion": CUAD}, marco={"sin_cara": CUAD}),
 "a3": dict(video=M + "/fijo/a3.mp4", audio=M + "/a3.wav", credito="Audio: Radio Popular · EgunOn Magazine (1 de septiembre de 2023)",
            rotulos={"jon": JONR, "pregunta": "Pregunta del programa", "programa": r"{\b1}EgunOn Magazine{\b0}  ·  Radio Popular  ·  1 de septiembre de 2023"}, preguntan=["pregunta", "programa"],
            enc={"jon": CUAD, "pregunta": CUAD, "programa": CUAD}, marco={"sin_cara": CUAD}),
 "a11": dict(video=M + "/fijo/a11.mp4", audio=M + "/a11.wav", credito="Audio: Radio Euskadi · Boulevard (4 de agosto de 2023)",
             rotulos={"oscar": OSCR, "pregunta": "Pregunta del programa"},
             enc={"oscar": CUAD, "pregunta": CUAD}, marco={"sin_cara": CUAD}),
 # ---- vídeos (mismas configuraciones de encuadre que el 6 de octubre)
 "v2": dict(video=M + "/src/v2.mp4", audio=M + "/v2.wav", credito="Imágenes: EITB · En Jake (7 de julio de 2022)",
            rotulos={"oscar": OSC}, enc={"oscar": ["izq"], "presentador": ["izq"]},
            marco={"lado_izq": 200, "lado_der": 150, "lado_pleno": 244, "sin_cara": [10, 28, 200]}),
 "v3": dict(video=M + "/src/v3.mp4", audio=M + "/v3.wav", credito="Imágenes: EITB · Qué me estás contando (25 de noviembre de 2019)",
            rotulos={"oscar": OSC}, enc={"oscar": ["der"], "presentador": ["izq", "centro"]},
            marco={"lado_der": 250, "lado_izq": 250, "lado_pleno": 300, "techo": 28, "sin_cara": [400, 40, 230]}),
 "v4": dict(video=M + "/src/v4.mp4", audio=M + "/v4.wav", credito="Imágenes: EITB · Está pasando (1 de julio de 2019)",
            rotulos={"oscar": OSC + "  ·  por teléfono"}, enc={"presentador": ["izq", "mayor"]},
            marco={"lado_izq": 190, "lado_pleno": 244, "sin_cara": [0, 30, 190]}),
 "inf": dict(video=M + "/src/inf25.mp4", audio=M + "/inf.wav", credito="Imágenes: EITB · informativos (enero de 2021)", prefijo="",
             rotulos={"jon": JON, "locucion": r"{\b1}Informativos de EITB{\b0}  ·  enero de 2021", "testimonio": r"{\b1}Testimonio de un cliente{\b0}  ·  Informativos de EITB"}, preguntan=["locucion"],
             enc={"locucion": [420, 0, 1080], "testimonio": [535, 0, 1080]}, marco={"sin_cara": [420, 0, 1080]}),
 "qa": dict(video=M + "/src/qa.mp4", audio=M + "/qa.wav", credito="Imágenes: EITB · Quédate con Ane (8 de enero de 2024)", prefijo="",
            rotulos={"presentadora": r"{\b1}En EITB{\b0}  ·  sobre Erreklamatu"}, preguntan=[],
            enc={"presentadora": [74, 180, 518]}, marco={"sin_cara": [74, 180, 518]}),
 "vi": dict(video=M + "/src/vfin.mp4", audio=M + "/vfin.wav", credito="Imágenes: EITB · En Jake (octubre de 2024)", prefijo="",
            rotulos={"presentador": r"{\b1}En Jake (ETB2){\b0}  ·  en la oficina de Erreklamatu", "reportero": r"{\b1}En Jake (ETB2){\b0}  ·  en la oficina de Erreklamatu"}, preguntan=[],
            enc={"presentador": [242, 0, 330], "reportero": [100, 8, 330]}, marco={"sin_cara": [100, 8, 330]}),
}
RAD14 = {"video": M + "/fijo/a14r.mp4"}; RAD3 = {"video": M + "/fijo/a3r.mp4"}; RAD11 = {"video": M + "/fijo/a11r.mp4"}
FIJO4 = {"video": M + "/fijo/v4f.mp4", "audio": M + "/v4.wav", "enc": CUAD}
FIJOI = {"video": M + "/fijo/inff.mp4", "enc": CUAD}
INI = {"video": M + "/src/vini.mp4", "audio": M + "/vini.wav"}     # principio del vídeo del viento (el final es el archivo principal: sus segundos son los del original menos 236)

# ---------------------------------------------------------------- COPE, Mediodía COPE, 8 de junio de 2023: indemnización para un bebé (audio)
X_C1 = (23.28, 46.75, "locucion", "Pues escucha lo que le ha pasado a un matrimonio que viajaba con un bebé en un vuelo entre Lisboa y Bilbao que sufrió un retraso de más de cinco horas. Cuando aterrizaron, pusieron una reclamación y la aerolínea solo pagó una parte, sin contar con el bebé, que, te recuerdo, no pagaba billete. Bueno, pues un juzgado de Bilbao ha dicho lo contrario: que el bebé también tiene derecho a una indemnización por el retraso de ese vuelo.", RAD14)
X_C2 = (46.90, 60.60, "locucion", "Jon Ortiz, abogado de Erreklamatu y encargado del caso, nos ha contado que, en el momento que la aerolínea obliga a identificar al bebé y emitir una tarjeta de embarque, se le generan automáticamente una serie de derechos.", RAD14)
X_C3 = (60.62, 83.20, "jon", "Sí había una tarjeta de embarque con su nombre, sí había una reserva con su nombre y sí se habían pagado… perdón, una serie de importes con su nombre. Por tanto, eso le da derecho a que, si luego acontece una incidencia, como ha sido el caso, también se genere un derecho de indemnización, porque existía una reserva a su nombre y existía una tarjeta de embarque a su nombre.")
X_D1 = (111.84, 128.45, "locucion", "No es la primera vez que pasa esto. El problema es que, al no haber una sentencia firme del Tribunal Europeo de Justicia, las aerolíneas intentan evitar este tipo de pagos y dejan en las propias familias la voluntad de abrir un proceso judicial, a veces lento, pero que en todos los casos acaba dándoles la razón.", RAD14)
X_D2 = (128.50, 151.50, "jon", "Entonces, una sentencia de un tribunal superior sí que… supondría una obligación. Pero bueno, ya existe también una regulación que habla de retrasos, de cancelaciones, de denegaciones de embarque, superconsolidada, y que sin embargo las compañías, cuando ocurren ese tipo de incidencias, muchas veces también se oponen al pago de las indemnizaciones.")

# ---------------------------------------------------------------- Radio Popular, EgunOn Magazine, 1 de septiembre de 2023: pasajeros desembarcados por exceso de carga (audio)
Y_I = (10.08, 27.70, "programa", "Bueno, pues con esto de los aviones y de las cosas que provocan a los viajeros, o que les fastidian las vacaciones, ha habido una que nos ha dejado un poco muertos. O sea, en un vuelo de Lufthansa han denegado el embarque a varios pasajeros; les han hecho descender del avión porque había un exceso de carga en el avión.", RAD3)
Y_C = (78.82, 118.40, "jon", "Quiero decir, no es más que otra incidencia más, u otra política de estas compañías, que al final el último afectado es el pasajero o la pasajera, ¿no? Sí, en este caso fue, bueno, unos pasajeros que iban a tomar un vuelo, en este caso con la compañía Lufthansa, y bueno, al percatarse… Ya habían embarcado, incluso, y al percatarse la compañía, bueno, pues que, como tú bien dices, el vuelo tenía un exceso de carga y no podía realizar el trayecto en esas condiciones, pues bueno, la solución fue dejar… dejar sin embarcar, dejar en la calle, digamos, a 35 pasajeros para solucionar ese problema.")
Y_Q2 = (118.60, 127.30, "pregunta", "¿Y cómo es que los aviones no detectan que haya un exceso de carga? Quizás porque hay demasiado equipaje… ¿Esto no lo pueden medir antes?", RAD3)
Y_G1 = (127.95, 132.45, "jon", "Sí, efectivamente, al final no se trata más que de otra mala gestión de la compañía, ¿no?")
Y_G2 = (158.00, 206.70, "jon", "Bueno, tenemos que recordar que los overbookings se dan también porque las compañías venden más billetes de los que tienen. Entonces, no sé yo… cada uno opinará, pero no sé qué práctica es peor, ¿no? Entiendo que en este caso hubo una mala gestión de la compañía en cuanto al cálculo del peso, ya sea equipaje, o también puede ser no solo equipaje de los pasajeros, sino material que la propia compañía tiene que trasladar, ya sea de sus trabajadores, ya sea de sus aviones… bueno, material de la propia compañía que quieren trasladar de un aeropuerto a otro, y que eso hace que hubiese un… un exceso de peso, y por tanto los afectados son los pasajeros. Pero lo que comento, ¿no?: otras veces el overbooking simplemente será por haber vendido más billetes de lo que corresponde, que también, desde luego, no es una práctica muy ética, ¿no?")
Y_Q3 = (273.88, 283.38, "pregunta", "Y ya para terminar, tenemos un minuto: ¿ha habido… hay problemas de seguridad en eso de que los aviones tengan exceso de carga? Quiero decir que da un poco de miedo, a ver si se va a caer.", RAD3)
Y_S = (283.60, 323.85, "jon", "Sí, desde luego. Es cierto que ya eso no es la materia que nos corresponde a nosotros, pero desde luego da un poco de… da un poco de miedo encontrarnos, como tú bien dices, ¿no?, que nos comunican que el avión tiene demasiado peso y que en esas condiciones no puede viajar. Porque claro, es un poco lo que he comentado: sabiendo un poco las chapuzas, digamos, por decirlo de una manera, que estas compañías muchas veces hacen y que al final los pasajeros se ven afectados, nos da un poco de miedo pensar cuántas veces hemos viajado ya, cada uno como usuario o usuaria de estos aviones, con excesos de este tipo o con algún problema similar. Sí que… sí que asusta un poco.")

# ---------------------------------------------------------------- Radio Euskadi, Boulevard, 4 de agosto de 2023: cobro del equipaje de mano (audio)
Z_Q2 = (85.20, 99.00, "pregunta", "O sea, que si alguien se planta con una maleta en el aeropuerto y dice: «No, no, es que la ley dice que puedo llevarla, y además pesa solo cinco kilos», vamos a poner ese ejemplo, podría tener la razón, pero aun así se queda igual a las puertas hasta que pague.", RAD11)
Z_A2 = (99.10, 129.90, "oscar", "Efectivamente. Efectivamente, ese es el gran problema… pero esto, como cualquier conflicto social, ¿no? Es decir, si hay una parte que no te deja viajar y, en este caso, pues tiene el poder de poder decir si entras o no en un avión, pues al final estás bajo su mandato, ¿no?, bajo su mando. Por eso yo creo que es una muy buena noticia este expediente sancionador, porque en cierta manera, pues, el Estado entra en cierta manera a sancionar algo que yo creo que luego puede repercutir de forma beneficiosa para los consumidores.")
Z_Q3 = (129.95, 155.00, "pregunta", "Óscar, entonces, digamos que la trampa está en las medidas que ellos te dicen: «No, tú puedes llevar algo de 40 por 30 por 35, independientemente de los kilos, pero no más de esas medidas». Porque eso sí que lo dejan muy claro: que tú puedes subir al avión una bolsa, que sea mochila —si es maleta, ya no—, pero que tenga esas medidas concretas. Ahí es un poco la trampa que nos hacen.", RAD11)
Z_A3 = (155.60, 214.30, "oscar", "Sí, yo creo que hay alguna compañía que directamente no te deja subir ningún tipo de maleta; entonces ahí yo creo que hay menos debate, porque sí que la Ley de Navegación Aérea es clara en el sentido de lo que hemos comentado: poder llevar artículos que puedan ser necesarios para el viaje, equipaje, contigo. Pero sí que luego, si ya entramos en la cuestión de las medidas, etcétera, ahí hay más discusión, porque realmente cuánto es… cuánto tiene que pesar o cuánto tiene que medir esa maleta que llevas, y ahí… ahí sí que puede haber más debate. Sí que puede haber más debate. Desde nuestro punto de vista, hay una serie de normas, bueno, de recomendaciones internacionales, de una serie de medidas que son las que se suelen cumplir, las que conocemos todos: 55 por 25, creo que es, por 30, vamos, es decir, el típico maletín pequeño, y es lo que se suele cumplir y es lo que todo el mundo acepta como válido. Pero no hay una ley que diga que exactamente tiene que ser esa medida. Entonces ahí es donde entra, ¿no?, qué es lo que puedo llevar y qué es lo que no.")
Z_Q4 = (214.50, 226.00, "pregunta", "Entonces, al pasajero que tiene tiempo y ganas de pelear esto, ¿qué le recomendarías? ¿Que reclame? ¿Que espere? Porque puede estar al caer un cambio por parte de las compañías.", RAD11)
Z_A4 = (226.90, 285.75, "oscar", "El problema… el problema que tiene todo consumidor es que, si de forma previa la compañía… si la compañía no admite de forma voluntaria la devolución de esa cantidad, el problema es que te tienes que ir a un procedimiento, vamos a decir, judicial, es decir, a una reclamación judicial, para poder conseguir ese dinero. ¿Y qué pasa? Que son cantidades muy pequeñas. Bueno, que para cada uno serán importantes, pero sí que, para lo que supone un procedimiento judicial, son cantidades bajas. Por lo tanto, abocan al pasajero, al consumidor, a una situación un poco, pues, injusta, porque realmente, claro, tener que ir a un proceso judicial para que luego te den la razón… Y luego, cuidado, porque puede haber luego interpretaciones diferentes: algún juzgado… sí que es lo mínimo, mínimo; la jurisprudencia viene a decirlo, la ley, en la lógica de consumo, ¿no?, es decir, que no se puede cobrar. Pero incluso algún juzgado puede ser que no te dé la razón por una interpretación que haga propia, ¿no? Por lo tanto, claro, el consumidor se queda en una situación un poco desamparado.")
Z_Q5 = (285.80, 290.40, "pregunta", "¿A vosotros en Erreklamatu os llegan reclamaciones de este estilo? ¿Las aceptáis?", RAD11)
Z_A5 = (291.50, 336.60, "oscar", "Ese es el problema que tenemos. Nosotros sí que… sí que llevamos este tipo de reclamaciones cuando va con otra incidencia, ¿no? Es decir, también hay derecho a indemnizaciones por maletas con retraso, también hay derecho a indemnización por retraso en la llegada, por cancelaciones, overbooking… Cuando se suman a esa reclamación, nosotros sí que lo podemos reclamar, porque ya es una reclamación que ya se suma a otra cantidad. Por lo tanto, ya sí que es interesante para todas las partes el proceso. Pero nosotros, claro, el problema que tenemos es lo que te he comentado: que al final, por 40 euros, tienes que ir a hacer un proceso judicial, una demanda, etcétera, etcétera. Incluso ni nosotros podemos… podemos hacerlo, ya que nosotros solo cobramos en caso de ganar y un porcentaje. Por lo tanto, es una situación que también a nosotros nos genera bastante frustración por no poder llevarlas adelante.")

# ---------------------------------------------------------------- En Jake (ETB2), 7 de julio de 2022: Óscar Sánchez
O_Q0 = (5.10, 24.90, "presentador", "Yo no sé si en Erreklamatu tienen constancia de que efectivamente hay un incremento en las reclamaciones. Le voy a preguntar a Óscar Sánchez, que es abogado de Erreklamatu. Óscar, ¿qué tal? Hola, bienvenido. No sé si estáis empezando ya a notar este efecto bola que estábamos comentando, de cómo está en general la situación de la aviación.")
O_A0 = (25.60, 43.90, "oscar", "Egun on. Una pasada. Sí que estamos notando un montón de llamadas, de emails… La verdad es que sí, sí, se está notando mucho. Este verano está pasando, pues, lo que habéis comentado antes en el reportaje, y nosotros estamos notando, sí, sí, un montón de consumidores que se están viendo afectados de diferentes formas, sí.")
O_QT = (125.92, 137.30, "presentador", "A ver, ponme el top de la compañía que se cierra en banda o que más reclamaciones tiene, porque igual no tiene por qué coincidir. La que más reclamaciones tiene, ¿cuál es?")
O_AT = (137.50, 162.34, "oscar", "No te… eso no te puedo decir; no es una cuestión de… de personalizar tampoco. Yo creo que es lo que he comentado: sí que dependerá mucho de las épocas, y tampoco es una cuestión de… de personalizar. No me gustaría hablar de una compañía en concreto. Yo sí que creo que hay momentos en concreto en los que están más saturados o menos saturados. Cuando están muy saturados, no pueden… no tienen capacidad igual para contestar, o no quieren, y entonces nos obligan a ir al proceso judicial.")

# ---------------------------------------------------------------- Qué me estás contando (ETB2), 25 de noviembre de 2019: Óscar Sánchez
P_QE = (178.40, 184.95, "presentador", "Interesantísimo, ¿no? Ahí podemos ver los conceptos por los que podemos reclamar. En erreklamatu.com, entiendo.")
P_AE = (185.30, 194.85, "oscar", "Sí, con nosotros, sin ningún problema. Nosotros solo cobramos en caso de conseguir una indemnización, y si no se consigue una indemnización no cobramos nada por nuestro trabajo, por efectuar reclamaciones de este tipo.")
P_QG = (267.30, 278.36, "presentador", "Óscar, muchísimas gracias, eskerrik asko, por habernos dado los consejos. Ya lo sabéis: en erreklamatu.com. Ahí podéis saber… e información, y podéis reclamar a través de ellos. Y recuerda lo que has dicho: que no cobráis si no recibís.")
P_AG = (279.90, 281.60, "oscar", "Efectivamente, efectivamente.")

# ---------------------------------------------------------------- Está pasando (ETB2), 1 de julio de 2019: huelga en el aeropuerto de Loiu (Óscar Sánchez, por teléfono)
H_P1 = (37.20, 59.90, "presentador", "¿Tiene derecho el usuario afectado, por ejemplo, por esta huelga a presentar una reclamación? Pues tenemos a los expertos en este tipo de reclamaciones. La compañía, o la empresa, se llama Erreklamatu —es un nombre… a recordar, desde luego, bastante fácil—, y Óscar Sánchez es abogado de esta plataforma. Óscar, arratsalde on.")
H_P2 = (62.70, 73.00, "presentador", "Si creo que una huelga como esta puede afectar a mi vuelo, ¿qué hago? ¿Confío en los servicios mínimos? ¿Pido a la compañía que me cambie el vuelo? En fin, Óscar, ¿qué hay que hacer?")
H_A2 = (73.20, 109.60, "oscar", "Nos encontramos con un problema, un problema serio, porque las compañías lo que quieren, lógicamente, es abaratar… bueno, que esta… que esta huelga no les salga… un problema mayor, y por lo tanto, hasta el último segundo, pues están constantemente haciendo encaje de bolillos para ver cómo organizar todos los vuelos, cómo reubicar a gente, etcétera. Entonces, por otro lado, los medios de atención al cliente, pues, están saturados, por lo normal, lo que nos cuentan los clientes, y se encuentra ya el cliente en una situación muy, muy complicada para gestionar si… si la compañía no se pone en contacto con ellos. Es decir, es muy complicado gestionarlo; esa es la realidad que nos encontramos.", FIJO4)
H_P3 = (141.50, 155.90, "presentador", "Hemos visto que hay dieciocho jornadas de huelga. ¿En previsión se puede hacer algo? ¿Tú recomendarías hacer algo a los clientes, a los usuarios que tengan vuelo para alguna de esas jornadas?")
H_A3 = (156.20, 175.30, "oscar", "Yo sí que les suelo recomendar que sean… y que sean insistentes, que estén detrás de la compañía y que no esperen. Pero sí que es verdad que a veces se convierte en algo muy complicado, porque no te cogen el teléfono, etcétera. Pero lo único es que sean insistentes, que continuamente se pongan en contacto con la compañía y que intenten buscar una solución. Pero hay poquito más que… que podamos recomendar.", FIJO4)

# ---------------------------------------------------------------- Informativos de EITB, enero de 2021 (versión en castellano de la pieza de PUB-0060 a PUB-0063)
W_A1 = (45.90, 48.36, "locucion", "Acudieron al equipo de abogados de Erreklamatu.")
W_A2 = (53.00, 56.10, "jon", "Estamos seguros que por ley les corresponde recuperar ese importe.", FIJOI)
W_A3 = (62.30, 66.50, "locucion", "Y solo entonces, en caso de recibir el dinero, es cuando el usuario pagaría por el servicio.", {"enc": [[62.30, 210, 0, 1080], [64.80, 0, 0, 1080]]})
W_A4 = (66.50, 71.80, "jon", "Si no conseguimos un importe, no conseguimos una indemnización para el cliente, pues el cliente no tiene que abonar absolutamente nada.", FIJOI)
W_T1 = (98.00, 102.45, "locucion", "Si la causa es ordinaria, culpa de la aerolínea, podemos incluso pedir una compensación.", {"enc": [[98.00, 420, 0, 1080], [98.16, 110, 0, 1080], [99.76, 420, 0, 1080], [101.80, 840, 0, 1080]]})
W_T2 = (102.45, 106.60, "locucion", "Le ocurrió a Imanol: viajaba a Omán y perdió la conexión debido a un retraso.", {"enc": [[102.45, 840, 0, 1080], [103.88, 420, 0, 1080]]})
W_T3 = (106.60, 121.65, "testimonio", "Y nos reubicó en el vuelo del día siguiente: el mismo vuelo, a la misma hora, 24 horas… Yo ya sabía, porque conocía la compañía de Erreklamatu, que se podía reclamar, porque además de estas cosas que te dan, tienes derecho a una compensación económica. Y bueno, parece que hemos ganado: hemos sacado como unos 600 euros cada uno.", {"enc": [[106.60, 535, 0, 1080], [117.04, 420, 0, 1080], [118.44, 535, 0, 1080]]})
W_T4 = (121.70, 124.35, "locucion", "Ideal para quienes quieren evitarse quebraderos de cabeza.", {"enc": [[121.70, 420, 0, 1080], [123.56, 840, 0, 1080]]})

# ---------------------------------------------------------------- Quédate con Ane (ETB2), 8 de enero de 2024: despedida de la presentadora a Jon Ortiz
J_FIN = (477.30, 507.50, "presentadora", "Jon Ortiz, ¿cuánto hubieran agradecido los miles de afectados por esta huelga del servicio de tierra de Iberia tenerte en un pantallón gigante en el propio aeropuerto, respondiendo a todas sus dudas? Porque generalmente los usuarios se quejan de la falta de información, y hasta que no te ves en una tesitura de estas, pues la verdad es que uno no se plantea todas estas cosas. Así que gracias por habernos aclarado todas estas cuestiones. Seguro que hay mucho más; tendréis tiempo en las próximas horas, porque me temo que mucho no vais a dormir. Pero ánimo, y gracias por ser tan didáctico y por explicarnos tan bien el asunto.")

# ---------------------------------------------------------------- En Jake (ETB2), octubre de 2024: cancelaciones por viento en Bilbao (principio y final de la conexión con la oficina)
K_I1 = (0.72, 7.50, "presentador", "Tú estuviste exactamente ahí, en el aeropuerto, hablando con ellos, y hoy hemos ido a la oficina de Erreklamatu para saber a qué hay derecho y a qué no.", dict(INI, enc=[[0.72, 316, 0, 330], [2.10, 45, 0, 400]]))
K_I2 = (8.50, 14.60, "reportero", "Sí, nos acompaña, Xabier, este mediodía Óscar Sánchez, abogado de erreklamatu.com. Óscar, lo primero, gracias por estar con nosotros.", dict(INI, enc=[[8.50, 45, 0, 400], [11.04, 100, 8, 330]]))
K_F1 = (52.50, 64.95, "reportero", "Óscar Sánchez, abogado de erreklamatu.com, eskerrik asko por haber estado con nosotros esta mañana. Y lo dicho, Xabi: hoy os van a sonar los teléfonos un montón, porque hablamos de, lo decías tú, 8.000 pasajeros afectados ayer por las cancelaciones y los desvíos.", {"enc": [[52.50, 0, 58, 300], [53.92, 100, 8, 330], [60.30, 45, 0, 400]]})
K_F2 = (65.00, 88.30, "presentador", "Eskerrik asko, Mikel. Bueno, pues esperemos que les haya servido un poco también de pistas sobre lo que se puede reclamar o no: el billete sí, o la alternativa que te den; los gastos que generen esos retrasos; no una indemnización, porque son causas ajenas a la compañía y están justificadas, concretamente ayer, por esa alerta naranja sobre vientos. Yo creo que ha quedado bastante claro.", {"enc": [[65.00, 45, 0, 400], [67.70, 242, 0, 330], [81.60, 606, 80, 268]]})

P = {"principal": "oscar"}; PJ = {"principal": "jon"}
# (vídeo, identificador, kicker, titular, tramos, opciones)
C = [
 ("a14", "PUB-0228", "Bebés", ["El caso del bebé que ganó", "a la aerolínea en el juzgado"], [X_C1, X_C2, X_C3], PJ),
 ("a14", "PUB-0229", "Bebés", ["Indemnización para bebés:", "las aerolíneas se resisten"], [X_D1, X_D2], PJ),
 ("a3", "PUB-0230", "Overbooking", ["35 pasajeros fuera del", "avión por exceso de carga"], [Y_I, Y_C], PJ),
 ("a3", "PUB-0231", "Overbooking", ["Exceso de carga: «una mala", "gestión de la compañía»"], [Y_Q2, Y_G1, Y_G2], PJ),
 ("a3", "PUB-0232", "Overbooking", ["Avión con exceso de", "carga: «asusta un poco»"], [Y_Q3, Y_S], PJ),
 ("a11", "PUB-0233", "Equipaje de mano", ["Tienes razón con tu maleta,", "pero no subes si no pagas"], [Z_Q2, Z_A2], P),
 ("a11", "PUB-0234", "Equipaje de mano", ["Equipaje de mano: ¿qué", "medidas puedes llevar?"], [Z_Q3, Z_A3], P),
 ("a11", "PUB-0235", "Equipaje de mano", ["Equipaje de mano: ¿merece", "la pena reclamarlo?"], [Z_Q4, Z_A4], P),
 ("a11", "PUB-0236", "Equipaje de mano", ["Equipaje de mano: cuándo", "lo reclamamos por ti"], [Z_Q5, Z_A5], P),
 ("v2", "PUB-0237", "Reclamar", ["Verano: se disparan las", "reclamaciones de vuelos"], [O_Q0, O_A0], P),
 ("v2", "PUB-0238", "Reclamar", ["¿Qué aerolínea recibe", "más reclamaciones?"], [O_QT, O_AT], P),
 ("v3", "PUB-0239", "Reclamar", ["Reclamar tu vuelo: solo", "cobramos si ganamos"], [P_QE, P_AE, P_QG, P_AG], P),
 ("v4", "PUB-0240", "Huelgas", ["Huelga en el aeropuerto:", "¿qué hago con mi vuelo?"], [H_P1, H_P2, H_A2], P),
 ("v4", "PUB-0241", "Huelgas", ["Huelga anunciada: insiste", "a la aerolínea y no esperes"], [H_P3, H_A3], P),
 ("inf", "PUB-0242", "Reclamar", ["Si no recuperas tu dinero,", "no pagas nada"], [W_A1, W_A2, W_A3, W_A4], PJ),
 ("inf", "PUB-0243", "Clientes", ["«Hemos sacado unos 600", "euros cada uno»"], [W_T2, W_T3, W_T4], {"principal": "testimonio"}),
 ("vi", "PUB-0244", "Temporales", ["Cancelación por viento: qué", "se puede reclamar y qué no"], [K_I1, K_I2, K_F1, K_F2], {}),
 ("qa", "PUB-0245", "Erreklamatu", ["«Gracias por ser", "tan didáctico»"], [J_FIN], {}),
]
