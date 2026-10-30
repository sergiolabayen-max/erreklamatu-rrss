#!/usr/bin/env python3
"""Specs v3 (30/10/2026) de los vídeos de sentencias D1-D4, con las correcciones de Sergio. Las imágenes («stock») se rellenan en STOCK_V3."""
import json, sys
V = "../../../recursos/voces/documento-v3/"
CIERRE_V = {"titulo": "¿Te ha pasado?", "texto": "Te ayudamos a reclamar a la aerolínea.", "subtitulos": ["Llama al 944 027 596"],
            "locucion": "Llama al nueve cuatro cuatro, cero dos siete, cinco nueve seis.", "voz": "../../../recursos/voces/comics-v2/voz-cierre.mp3"}
MUS = "../../../recursos/musica/musica-lofi-100bpm.mp3"
def loc(f): return f
S = {}
S["D1"] = dict(id="D1-athletic-roma", categoria="UN CASO REAL", juzgado="Juzgado de Primera Instancia n.º 9 de Bilbao", fecha="14 de marzo de 2025", pdf="sentencia-D1.pdf",
 titulo=["Bilbao–Roma: perdieron la conexión y el partido del Athletic", "El juez obliga a la aerolínea a pagar *también la entrada y el taxi*"], titulo_tam=74,
 portada_dato=["651,50 €", "compensación, entrada y taxi para los dos"],
 tramos=[
  dict(tipo="gancho", subtitulos=["Un retraso de Vueling les hizo perder el partido del Athletic en Roma.", "Y el juez obliga a la aerolínea a pagarles la entrada."], locucion="Un retraso de Vueling les hizo perder el partido del Athletic en Roma. Y el juez obliga a la aerolínea a pagarles la entrada.", voz=V+"D1-1.mp3"),
  dict(tipo="doc", pagina_num=1, subrayar=["allanándose únicamente a que se decrete una indemnización", "que no existe fundamento legal para tal reclamacion"], margen=[150, 60],
       cita="«… *allanándose únicamente a que se decrete una indemnización* (…) considerando *que no existe fundamento legal para tal reclamacion*…»",
       subtitulos=["Vueling solo aceptaba pagar la compensación de 250 euros.", "Para todo lo demás, decía que no había base legal."], locucion="Vueling solo aceptaba pagar la compensación de doscientos cincuenta euros. Para todo lo demás, decía que no había base legal.", voz=V+"D1-2.mp3", doc_entra=0.2),
  dict(tipo="doc", pagina_num=4, subrayar=["sean compensados por la totalidad", "con mas claridad en el caso de los billetes perdidos"], margen=[110, 60],
       cita="«… los pasajeros *sean compensados por la totalidad del perjuicio* (…) *con mas claridad en el caso de los billetes perdidos*…»",
       subtitulos=["Pero el juez le recordó que hay que compensar a los pasajeros por todo el perjuicio.", "Y que las entradas perdidas eran el caso más claro."], locucion="Pero el juez le recordó que hay que compensar a los pasajeros por todo el perjuicio. Y que las entradas perdidas eran el caso más claro.", voz=V+"D1-3.mp3", doc_entra=0.2),
  dict(tipo="doc", pagina_num=5, subrayar=["al no haberse siquiera abonado suma alguna pese", "al parcial allanamiento de la parte"], margen=[160, 60],
       cita="«… *al no haberse siquiera abonado suma alguna pese al parcial allanamiento de la parte*.»",
       subtitulos=["Y subrayó que Vueling ni siquiera les había pagado lo que reconocía deber."], locucion="Y subrayó que Vueling ni siquiera les había pagado lo que reconocía deber.", voz=V+"D1-4.mp3", doc_entra=0.1, extra=1.2),
  dict(tipo="lista", subtitulos=[], locucion="Esto es lo que Vueling tendrá que pagarles: doscientos cincuenta euros a cada uno, la entrada del partido, el taxi en Roma, los intereses y las costas.", voz=V+"D1-5.mp3",
       cabecera="Lo que Vueling tendrá que pagarles", total=["En total, para los dos:", "651,50 € + intereses"], extra=1.2,
       items=[dict(t="250 € a cada uno", d="de compensación por el retraso", palabra="doscientos"), dict(t="La entrada del partido", d="70 € que no pudieron disfrutar", palabra="la entrada"),
              dict(t="El taxi en Roma", d="81,50 € al llegar, ocho horas tarde", palabra="el taxi"), dict(t="Intereses y costas", d="Vueling paga también el juicio", palabra="los intereses")]),
  dict(tipo="consejo", subtitulos=["¿Un retraso te hizo perder algo que ya habías pagado?", "Guarda los justificantes. Tienes cinco años para reclamar."], locucion="¿Un retraso te hizo perder algo que ya habías pagado? Guarda los justificantes. Tienes cinco años para reclamar.", voz=V+"D1-6.mp3",
       grande="¿Perdiste algo *que ya habías pagado*?", pequeno="Guarda los justificantes: tienes 5 años para reclamar.", norma="Reglamento (CE) 261/2004, art. 12"),
 ],
 cierre=dict(CIERRE_V, legal="Reglamento (CE) 261/2004, arts. 7 y 12; Código Civil, art. 1101. Imágenes de archivo. Cada caso se estudia de forma individual."), musica=MUS)

S["D2"] = dict(id="D2-menores-irlanda", categoria="UN CASO REAL", juzgado="Juzgado de Primera Instancia n.º 9 de Pamplona", fecha="4 de diciembre de 2025", pdf="sentencia-D2.pdf",
 titulo=["Menores tirados en Irlanda, sin sus padres", "Más de *90.000 € de indemnización* para 120 pasajeros"], titulo_tam=80,
 portada_dato=["+90.000 €", "para 120 pasajeros, casi todos menores"],
 tramos=[
  dict(tipo="gancho", subtitulos=["120 pasajeros, casi todos menores, tirados en Irlanda sin sus padres.", "Más de 90.000 euros de indemnización."], locucion="Ciento veinte pasajeros, casi todos menores, tirados en Irlanda sin sus padres. Más de noventa mil euros de indemnización.", voz=V+"D2-1.mp3"),
  dict(tipo="doc", pagina_num=9, subrayar=["en el extranjero y tratándose de menores de edad todos ellos sin la compañía de sus padres", "es incuestionable que sí es susceptible de causar por sí mismo el impacto o sufrimiento psíquico"], margen=[60, 40],
       cita="«… *teniendo lugar en el extranjero y tratándose de menores de edad todos ellos sin la compañía de sus padres* (…) *es incuestionable que sí es susceptible de causar por sí mismo el impacto o sufrimiento psíquico*…»",
       subtitulos=["Su vuelo a Pamplona se canceló sin aviso, y llegaron un día tarde.", "Para el juez, siendo menores, en el extranjero y sin sus padres,", "el sufrimiento era incuestionable."], locucion="Su vuelo a Pamplona se canceló sin aviso, y llegaron un día tarde. Para el juez, siendo menores, en el extranjero y sin sus padres, el sufrimiento era incuestionable.", voz=V+"D2-2.mp3", doc_entra=2.0),
  dict(tipo="doc", pagina_num=9, subrayar=["la cantidad interesada por el daño moral más simbólica que", "reparadora del daño efectivamente ocasionado"], margen=[80, 60],
       cita="«… *Siendo la cantidad interesada por el daño moral más simbólica que reparadora del daño efectivamente ocasionado*…»",
       subtitulos=["Y llegó a decir que los 500 euros pedidos por daño moral", "eran una cantidad más simbólica que reparadora."], locucion="Y llegó a decir que los quinientos euros pedidos por daño moral eran una cantidad más simbólica que reparadora.", voz=V+"D2-3.mp3", doc_entra=0.1, extra=0.8),
  dict(tipo="lista", subtitulos=[], locucion="Esto es lo que la aerolínea tendrá que pagar a cada pasajero del juicio: doscientos cincuenta euros de compensación, quinientos por daño moral, sus gastos, los intereses y las costas.", voz=V+"D2-4.mp3",
       cabecera="Lo que la aerolínea paga a cada pasajero del juicio", total=["A cada uno:", "750 € + gastos"], extra=1.0,
       items=[dict(t="250 € de compensación", d="por la cancelación", palabra="doscientos"), dict(t="500 € por daño moral", d="42.500 € entre los 85", palabra="quinientos"),
              dict(t="Sus gastos", d="lo que tuvieron que comprar", palabra="sus gastos"), dict(t="Intereses y costas", d="la aerolínea paga también el juicio", palabra="los intereses")]),
  dict(tipo="consejo", subtitulos=["Con ese mismo criterio, la aerolínea pagó sin juicio a otros 35.", "En total, más de 90.000 euros."], locucion="Con ese mismo criterio, la aerolínea pagó sin juicio a otros treinta y cinco. En total, más de noventa mil euros.", voz=V+"D2-5.mp3",
       grande="Más de *90.000 €*", pequeno="85 pasajeros por sentencia y 35 más sin juicio, con el mismo criterio."),
  dict(tipo="consejo", subtitulos=["El daño moral no es automático: hay que probar lo que se vivió.", "De eso nos encargamos nosotros."], locucion="El daño moral no es automático: hay que probar lo que se vivió. De eso nos encargamos nosotros.", voz=V+"D2-6.mp3",
       grande="El daño moral *no es automático*", pequeno="Hay que probar lo que se vivió. De eso nos encargamos nosotros."),
 ],
 cierre=dict(CIERRE_V, legal="Reglamento (CE) 261/2004, arts. 7 y 12; Convenio de Montreal, art. 19. Imágenes de archivo. Cada caso se estudia de forma individual."), musica=MUS)

S["D3"] = dict(id="D3-gran-canaria", categoria="UN CASO REAL", juzgado="Juzgado de Primera Instancia n.º 12 de Bilbao", fecha="29 de marzo de 2025", pdf="sentencia-D3.pdf",
 titulo=["12 profesionales vascos se quedaron sin su congreso en Gran Canaria", "El juez condena a Vueling a pagarles *más de 13.500 €*"], titulo_tam=72,
 portada_dato=["13.509 €", "para los 12 pasajeros, daño moral incluido"],
 tramos=[
  dict(tipo="gancho", subtitulos=["Doce profesionales vascos se quedaron sin su congreso en Gran Canaria.", "Vueling les canceló el vuelo sin aviso,", "y ahora tendrá que pagarles más de 13.500 euros."], locucion="Doce profesionales vascos se quedaron sin su congreso en Gran Canaria. Vueling les canceló el vuelo sin aviso, y ahora tendrá que pagarles más de trece mil quinientos euros.", voz=V+"D3-1.mp3"),
  dict(tipo="doc", pagina_num=3, subrayar=["La parte demandada no contestó a la demanda en el plazo concedido", "siendo declarada en situación de rebeldía procesal"], margen=[90, 60],
       cita="«*La parte demandada no contestó a la demanda en el plazo concedido* a tal efecto *siendo declarada en situación de rebeldía procesal*…»",
       subtitulos=["Vueling ni siquiera contestó a la demanda."], locucion="Vueling ni siquiera contestó a la demanda.", voz=V+"D3-2.mp3", doc_entra=0.0, extra=2.4),
  dict(tipo="doc", pagina_num=5, subrayar=["se reclama el importe de las reservas", "del hotel abonado y no disfrutado", "costes que tiene que asumir la compañía en caso de cancelación"], margen=[95, 30],
       cita="«… se reclama *el importe de las reservas* (…), *del hotel abonado y no disfrutado* (…), *costes que tiene que asumir la compañía en caso de cancelación*.»",
       subtitulos=["Y el juez fue claro: los billetes y el hotel que no pudieron usar", "son costes que tiene que asumir la compañía."], locucion="Y el juez fue claro: los billetes y el hotel que no pudieron usar son costes que tiene que asumir la compañía.", voz=V+"D3-3.mp3", doc_entra=0.1, extra=0.8),
  dict(tipo="lista", subtitulos=[], locucion="Esto es lo que Vueling tendrá que pagarles: cuatrocientos euros a cada uno, los billetes, el hotel y otros gastos, doscientos euros por daño moral a cada uno, los intereses y las costas.", voz=V+"D3-4.mp3",
       cabecera="Lo que Vueling tendrá que pagarles", total=["En total, para los 12:", "13.509,42 €"], extra=1.0,
       items=[dict(t="400 € a cada uno", d="de compensación: 4.800 €", palabra="cuatrocientos"), dict(t="Los billetes", d="3.348,77 €", palabra="los billetes"),
              dict(t="El hotel y otros gastos", d="2.960,65 €", palabra="el hotel"), dict(t="200 € de daño moral a cada uno", d="2.400 €, algo poco habitual", palabra="doscientos"),
              dict(t="Intereses y costas", d="Vueling paga también el juicio", palabra="los intereses")]),
  dict(tipo="consejo", subtitulos=["Si no te avisan con dos semanas de antelación,", "puedes tener derecho a compensación."], locucion="Si no te avisan con dos semanas de antelación, puedes tener derecho a compensación.", voz=V+"D3-5.mp3",
       grande="¿No te avisaron con *2 semanas*?", pequeno="Puedes tener derecho a compensación.", norma="Reglamento (CE) 261/2004, art. 5"),
 ],
 cierre=dict(CIERRE_V, legal="Reglamento (CE) 261/2004, arts. 5 y 7. Imágenes de archivo. Cada caso se estudia de forma individual."), musica=MUS)

S["D4"] = dict(id="D4-cripto-santander", categoria="UN CASO REAL", juzgado="Juzgado de Primera Instancia n.º 12 de Bilbao", fecha="20 de mayo de 2025", pdf="sentencia-D4.pdf",
 titulo=["Le cargaron 1.923 € en criptomonedas con su tarjeta, sin su permiso", "El juez obliga al Santander a *devolvérselo todo, con intereses*"], titulo_tam=72,
 portada_dato=["1.923 €", "devueltos con intereses: sentencia firme"],
 tramos=[
  dict(tipo="gancho", subtitulos=["Le cargaron casi 2.000 euros en criptomonedas con su tarjeta, sin su permiso.", "Y el juez obliga al Santander a devolvérselo todo."], locucion="Le cargaron casi dos mil euros en criptomonedas con su tarjeta, sin su permiso. Y el juez obliga al Santander a devolvérselo todo.", voz=V+"D4-1.mp3"),
  dict(tipo="doc", pagina_num=6, subrayar=["dicha operación se", "efectuó mediante el empleo de un sistema de autenticación reforzado"], margen=[110, 40],
       cita="«… *dicha operación se efectuó mediante el empleo de un sistema de autenticación reforzado*…»",
       subtitulos=["El banco alegó que la compra había pasado su sistema de seguridad reforzado."], locucion="El banco alegó que la compra había pasado su sistema de seguridad reforzado.", voz=V+"D4-2.mp3", doc_entra=0.1, extra=1.2),
  dict(tipo="doc", pagina_num=10, subrayar=["sin que se haya aportado dictamen pericial específico por la parte demandada"], margen=[90, 40],
       cita="«… *sin que se haya aportado dictamen pericial específico por la parte demandada*…»",
       subtitulos=["Pero no aportó ningún informe pericial.", "Y ella había avisado al banco y denunciado enseguida."], locucion="Pero no aportó ningún informe pericial. Y ella había avisado al banco y denunciado enseguida.", voz=V+"D4-3.mp3", doc_entra=0.1),
  dict(tipo="doc", pagina_num=12, subrayar=["La prueba exigible a la entidad financiera va mucho más allá de la mera", "afirmación de cumplimiento de los protocolos de seguridad"], margen=[60, 60],
       cita="«*La prueba exigible a la entidad financiera va mucho más allá de la mera afirmación de cumplimiento de los protocolos de seguridad*…»",
       subtitulos=["Para el juez, al banco no le basta con decir", "que cumplió sus protocolos de seguridad."], locucion="Para el juez, al banco no le basta con decir que cumplió sus protocolos de seguridad.", voz=V+"D4-4.mp3", doc_entra=0.1, extra=1.2),
  dict(tipo="lista", subtitulos=[], locucion="Esto es lo que el Santander tendrá que devolverle: los mil novecientos veintitrés euros, los intereses desde el día del cargo y las costas. Y la sentencia es firme.", voz=V+"D4-5.mp3",
       cabecera="Lo que el Santander tendrá que devolverle", total=["Sentencia firme:", "lo recupera todo"], extra=0.8,
       items=[dict(t="1.923,67 €", d="el cargo que ella nunca autorizó", palabra="los mil"), dict(t="Los intereses", d="desde el día del cargo", palabra="los intereses"),
              dict(t="Las costas", d="el banco paga también el juicio", palabra="las costas")]),
  dict(tipo="consejo", subtitulos=["Si te pasa, avisa al banco enseguida,", "pide el bloqueo y denuncia."], locucion="Si te pasa, avisa al banco enseguida, pide el bloqueo y denuncia.", voz=V+"D4-6.mp3",
       grande="Avisa al banco *enseguida*", pequeno="Pide el bloqueo y denuncia. La prueba le toca al banco.", norma="Real Decreto-ley 19/2018, art. 44"),
 ],
 cierre=dict(CIERRE_V, texto="Te ayudamos a reclamar al banco.", legal="Real Decreto-ley 19/2018, arts. 44 y 46. Imágenes de archivo. Cada caso se estudia de forma individual."), musica=MUS)

if __name__ == "__main__":
    stock = json.load(open("specs/stock_v3.json")) if len(sys.argv) > 1 and sys.argv[1] == "stock" else {}
    for k, sp in S.items():
        for i, t in enumerate(sp["tramos"]):
            st = stock.get(k, {}).get(str(i + 1)) or {"stock": "TBD"}
            t.update(st)
        if k in stock and "portada" in stock[k]: sp.update(stock[k]["portada"])
        json.dump(sp, open(f"specs/{k}-v3.json", "w"), ensure_ascii=False, indent=1)
    print("ok")
