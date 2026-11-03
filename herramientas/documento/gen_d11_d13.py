#!/usr/bin/env python3
"""Specs de los vídeos de sentencias D11-D15 («El documento, subrayado» v3), 3/11/2026 (segunda tanda de sentencias de Sergio).
Los nombres de los clientes NO van aquí (repositorio público): van en Magnific/sentencias/sentencia-Dn.ocultar.txt, solo en el Mac.
Uso: python3 gen_d11_d13.py -> specs/D11-v3.json … specs/D13-v3.json."""
import json
V = "../../../recursos/voces/documento-v3/"
MUS = "../../../recursos/musica/musica-lofi-100bpm.mp3"
CIERRE = {"titulo": "¿Te ha pasado?", "texto": "Te ayudamos a reclamar a la aerolínea.", "subtitulos": ["Llama al 944 027 596"],
          "locucion": "Llama al nueve cuatro cuatro, cero dos siete, cinco nueve seis.", "voz": "../../../recursos/voces/comics-v2/voz-cierre.mp3"}
def t(tipo, n, subs, **kw):
    d = dict(tipo=tipo, subtitulos=subs, **kw); d.setdefault("locucion", " ".join(subs)); d["voz"] = V + n + ".mp3"; return d

S = {}
# D11 · TAP, Lisboa-Bilbao con 5 h de retraso: el bebé sin asiento también cobra (JPI n.º 12 de Bilbao, 15/5/2023). Firme.
S["D11"] = dict(id="D11-tap-bebe", categoria="UN CASO REAL", juzgado="Juzgado de Primera Instancia n.º 12 de Bilbao", fecha="15 de mayo de 2023", pdf="sentencia-D11.pdf",
 titulo=["Lisboa–Bilbao: TAP no quería compensar al bebé que viajaba en brazos", "El juez dice que *el bebé también tiene derecho*"], titulo_tam=76,
 portada_dato=["250 €", "también para el bebé: 1.026,56 € para la familia"],
 tramos=[
  t("gancho", "D11-1", ["TAP no quería compensar a un bebé que viajaba en brazos.", "El juez dijo que también tenía derecho."]),
  t("doc", "D11-2", ["El vuelo de Lisboa a Bilbao llegó cinco horas tarde.", "TAP aceptó pagar a los otros tres pasajeros, pero no al bebé:", "decía que, con menos de dos años, no pagó billete ni ocupaba asiento."],
    pagina_num=2, subrayar=["por tener una edad inferior a dos años no pagó billete ni ocupaba un asiento"], margen=[150, 60], doc_entra=2.5,
    cita="«… *por tener una edad inferior a dos años no pagó billete ni ocupaba un asiento* en el vuelo…»"),
  t("doc", "D11-3", ["Pero el bebé figuraba con su nombre en la reserva y tenía tarjeta de embarque.", "Para el juez, eso basta: el Reglamento también se aplica al bebé."],
    pagina_num=5, subrayar=["consta el nombre del menor", "se ha de aplicar el Reglamento al bebé"], margen=[110, 60], doc_entra=0.2,
    cita="«… en la reserva emitida al adquirir los billetes *consta el nombre del menor* (…) *se ha de aplicar el Reglamento al bebé*.»"),
  t("lista", "D11-4", [], locucion="Esto es lo que TAP tendrá que pagarles: doscientos cincuenta euros a cada uno de los cuatro, también al bebé, el parking que pagaron de más, los intereses y las costas.",
    cabecera="Lo que TAP tendrá que pagarles", total=["En total, para la familia:", "1.026,56 € + intereses"], extra=1.2,
    items=[dict(t="250 € a cada uno", d="los cuatro, también el bebé", palabra="doscientos"), dict(t="El parking", d="lo que pagaron de más por el retraso", palabra="el parking"),
           dict(t="Intereses y costas", d="TAP paga también el juicio", palabra="los intereses")]),
  t("consejo", "D11-5", ["¿Viajas con un bebé en brazos?", "Si figura con su nombre en la reserva y tiene tarjeta de embarque,", "también puede tener derecho a compensación."],
    grande="¿Tu bebé *viaja en brazos*?", pequeno="Si figura en la reserva con su nombre, también puede reclamar. Tienes 5 años.", norma="Reglamento (CE) 261/2004, arts. 3 y 7"),
 ],
 cierre=dict(CIERRE, legal="Reglamento (CE) 261/2004, arts. 3, 7 y 12. Imágenes de archivo. Cada caso se estudia de forma individual."), musica=MUS)

# D12 · TAP, Miami-Lisboa-Bilbao: cancelan el Lisboa-Bilbao, llegan 13 h tarde por Múnich; 600 € + 400 € de daño moral a cada uno de seis (JPI n.º 12 de Bilbao, 18/7/2023). Firme.
# El bebé no cobra: no tenía billete ni tarjeta a su nombre (se dice en los textos, no en el vídeo).
S["D12"] = dict(id="D12-tap-miami", categoria="UN CASO REAL", juzgado="Juzgado de Primera Instancia n.º 12 de Bilbao", fecha="18 de julio de 2023", pdf="sentencia-D12.pdf",
 titulo=["Miami–Bilbao: les cancelaron el último vuelo y llegaron trece horas tarde", "El juez obliga a TAP a pagarles *6.000 €*"], titulo_tam=74,
 portada_dato=["6.000 €", "compensación y daño moral para seis pasajeros"],
 tramos=[
  t("gancho", "D12-1", ["Volvían de Miami a Bilbao con niños pequeños y TAP les canceló el último vuelo.", "Llegaron trece horas tarde.", "El juez obliga a TAP a pagarles 6.000 euros."],
    locucion="Volvían de Miami a Bilbao con niños pequeños y TAP les canceló el último vuelo. Llegaron trece horas tarde. El juez obliga a TAP a pagarles seis mil euros."),
  t("doc", "D12-2", ["Les mandaron por Múnich, con dos vuelos más largos que el que tenían.", "Y con niños pequeños, el juez vio una angustia mayor que la de una cancelación normal."],
    pagina_num=7, subrayar=["zozobra y angustia superior a la que genera una cancelación", "menores de corta"], margen=[150, 60], doc_entra=1.5,
    cita="«… la existencia de una *zozobra y angustia superior a la que genera una cancelación* se revelan como evidentes teniendo en cuenta que entre los pasajeros se encontraban *menores de corta* edad.»"),
  t("doc", "D12-3", ["Además, TAP no pudo demostrar que les diera comida ni información."],
    pagina_num=8, subrayar=["TAP no ha aportado ninguna prueba sobre la asistencia", "considero probada la falta de asistencia e información"], margen=[110, 60], doc_entra=0.2, extra=1.0,
    cita="«… *TAP no ha aportado ninguna prueba sobre la asistencia* que prestó (…) *considero probada la falta de asistencia e información*.»"),
  t("lista", "D12-4", [], locucion="Esto es lo que TAP tendrá que pagarles: seiscientos euros de compensación a cada uno, cuatrocientos más a cada uno por daño moral, y los intereses.",
    cabecera="Lo que TAP tendrá que pagarles", total=["En total, para seis pasajeros:", "6.000 € + intereses"], extra=1.4,
    items=[dict(t="600 € a cada uno", d="de compensación por la cancelación", palabra="seiscientos"), dict(t="400 € más a cada uno", d="por daño moral", palabra="cuatrocientos"),
           dict(t="Intereses", d="desde que se presentó la demanda", palabra="los intereses")]),
  t("consejo", "D12-5", ["¿Te cancelan el vuelo y nadie te explica nada ni te da de comer?", "Además de la compensación, puedes reclamar el daño moral.", "Tienes cinco años."],
    grande="¿Te dejaron *sin información ni comida*?", pequeno="Además de la compensación, puedes reclamar el daño moral. Tienes 5 años.", norma="Reglamento (CE) 261/2004, arts. 7, 9 y 12"),
 ],
 cierre=dict(CIERRE, legal="Reglamento (CE) 261/2004, arts. 5, 7, 9 y 12. Imágenes de archivo. Cada caso se estudia de forma individual."), musica=MUS)

# D13 · Lufthansa, Múnich-Bilbao cancelado sin alternativa: el billete que compró por su cuenta + 250 € (Mercantil n.º 2 de Bilbao, 8/3/2021). Sin recurso.
# Ojo: al final no usó el billete que compró (Lufthansa le reubicó y le convino más). El vídeo no dice que volara con él.
S["D13"] = dict(id="D13-lufthansa", categoria="UN CASO REAL", juzgado="Juzgado de lo Mercantil n.º 2 de Bilbao", fecha="8 de marzo de 2021", pdf="sentencia-D13.pdf",
 titulo=["Múnich–Bilbao: Lufthansa le canceló el vuelo sin ofrecerle alternativa", "El juez obliga a Lufthansa a pagarle *el billete que compró, aunque no lo usó*"], titulo_tam=74,
 portada_dato=["474,99 €", "compensación y el billete que compró por su cuenta"],
 tramos=[
  t("gancho", "D13-1", ["Lufthansa le canceló el vuelo de Múnich a Bilbao sin ofrecerle alternativa y se compró otro billete.", "El juez obliga a Lufthansa a pagárselo… aunque al final no lo usó."]),
  t("doc", "D13-2", ["La cancelación fue el mismo día del vuelo.", "Y Lufthansa reconoció que no le ofreció otro hasta el día siguiente."],
    pagina_num=2, subrayar=["la compañía aérea admite que no ofreció una alternativa"], margen=[150, 60], columna=[215, 1555], ocultar=["8", "7", "noviembre"], doc_entra=1.2,
    cita="«… *la compañía aérea admite que no ofreció una alternativa* al pasajero…»"),
  t("doc", "D13-3", ["Para el juez, sin información ni alternativa, era razonable que se comprara otro vuelo.", "Y además, los registros de Lufthansa le ofrecían poca confianza."],
    pagina_num=2, subrayar=["es razonable que el pasajero decidiera adquirir otro vuelo", "poca confianza ofrece el contenido de los registros"], margen=[110, 60], columna=[215, 1555], doc_entra=0.2,
    cita="«… *es razonable que el pasajero decidiera adquirir otro vuelo* (…) *poca confianza ofrece el contenido de los registros* de la compañía aérea…»"),
  t("lista", "D13-4", [], locucion="Esto es lo que Lufthansa tendrá que pagarle: doscientos cincuenta euros de compensación, el billete que compró por su cuenta, los intereses y las costas.",
    cabecera="Lo que Lufthansa tendrá que pagarle", total=["En total:", "474,99 € + intereses"], extra=1.4,
    items=[dict(t="250 €", d="de compensación por la cancelación", palabra="doscientos"), dict(t="224,99 €", d="el billete que compró por su cuenta", palabra="el billete"),
           dict(t="Intereses y costas", d="Lufthansa paga también el juicio", palabra="los intereses")]),
  t("consejo", "D13-5", ["¿Te cancelan el vuelo y no te ofrecen alternativa?", "Si te buscas otro, guarda el billete y los correos de la aerolínea.", "Tienes cinco años para reclamar."],
    grande="¿Te cancelan *y no te dan alternativa*?", pequeno="Guarda el billete y los correos: tienes 5 años para reclamar.", norma="Reglamento (CE) 261/2004, arts. 5, 8 y 12"),
 ],
 cierre=dict(CIERRE, legal="Reglamento (CE) 261/2004, arts. 5, 7, 8 y 12; Código Civil, art. 1101. Imágenes de archivo. Cada caso se estudia de forma individual."), musica=MUS)

# D14 · Air Canada, denegación de embarque en Montreal (trayecto Montreal-Londres-Lisboa-Bilbao) (Mercantil n.º 2 de Bilbao, 17/9/2020). Sin recurso.
# Ojo: el fundamento tercero suma 1.385,46 € (350 + 96,66 + 938,80) y así lo cuenta la nota de la web; el fallo solo dice 938,80 €. Se usa la cifra de la nota (avisado a Sergio).
# No se aplica el Reglamento 261 (vuelo desde fuera de la UE con aerolínea no comunitaria): el plazo es el del Convenio de Montreal (2 años), no 5.
S["D14"] = dict(id="D14-air-canada", categoria="UN CASO REAL", juzgado="Juzgado de lo Mercantil n.º 2 de Bilbao", fecha="17 de septiembre de 2020", pdf="sentencia-D14.pdf",
 titulo=["Montreal–Bilbao: Air Canada no le dejó embarcar, a miles de kilómetros de casa", "El juez le reconoce *daño moral, los billetes y las llamadas*"], titulo_tam=74,
 portada_dato=["1.385,46 €", "daño moral, billetes nuevos y llamadas"],
 tramos=[
  t("gancho", "D14-1", ["Air Canada no le dejó subir al avión en Montreal, a miles de kilómetros de casa.", "El juez le da la razón: más de 1.300 euros."],
    locucion="Air Canada no le dejó subir al avión en Montreal, a miles de kilómetros de casa. El juez le da la razón: más de mil trescientos euros."),
  t("doc", "D14-2", ["Le habían cambiado el itinerario y él lo había aceptado.", "Air Canada decía que solo para una parte del viaje.", "Para el juez, eso no tenía sentido: la denegación de embarque fue injustificada."],
    pagina_num=2, subrayar=["no tiene sentido que el demandante aceptara la modificación sólo para parte del trayecto", "embarque debe considerarse injustificada"], margen=[150, 60], doc_entra=2.0,
    cita="«… *no tiene sentido que el demandante aceptara la modificación sólo para parte del trayecto*. En consecuencia, la denegación del *embarque debe considerarse injustificada*.»"),
  t("doc", "D14-3", ["Aquí no se aplica el reglamento europeo.", "Aun así, el juez le reconoció 350 euros de daño moral por verse tirado tan lejos de casa."],
    pagina_num=3, subrayar=["justifican una afectación psíquica"], margen=[150, 60], doc_entra=0.2,
    cita="«Las circunstancias que el actor describe *justifican una afectación psíquica*…»"),
  t("lista", "D14-4", [], locucion="Esto es lo que Air Canada tendrá que pagarle: trescientos cincuenta euros de daño moral, los billetes que tuvo que comprar para volver, las llamadas y los intereses.",
    cabecera="Lo que Air Canada tendrá que pagarle", total=["En total:", "1.385,46 € + intereses"], extra=1.4,
    items=[dict(t="350 €", d="de daño moral", palabra="trescientos"), dict(t="938,80 €", d="los billetes que compró para volver a casa", palabra="los billetes"),
           dict(t="96,66 €", d="las llamadas que tuvo que hacer", palabra="las llamadas"), dict(t="Intereses", d="desde la demanda", palabra="los intereses")]),
  t("consejo", "D14-5", ["¿Te dejan en tierra con una aerolínea de fuera de Europa?", "Aunque no se aplique el reglamento europeo, puedes reclamar los gastos y el daño moral.", "No esperes: el plazo puede ser de solo dos años."],
    grande="¿Te dejan en tierra *fuera de Europa*?", pequeno="Puedes reclamar gastos y daño moral. No esperes: el plazo puede ser de 2 años.", norma="Convenio de Montreal, art. 35"),
 ],
 cierre=dict(CIERRE, legal="Convenio de Montreal; Código Civil, arts. 1101 y 1108. Imágenes de archivo. Cada caso se estudia de forma individual."), musica=MUS)

# D15 · Equipaje retrasado Biarritz-Bangkok (escala en Zúrich) y a la vuelta (Mercantil n.º 1 de Donostia, 19/8/2020). Firme.
# La sentencia nombra a dos aerolíneas distintas (una en el encabezado y otra en el texto) y el artículo del blog no dice cuál: el vídeo dice «la aerolínea» y tapa sus nombres (sentencia-D15.ocultar.txt, solo en el Mac).
S["D15"] = dict(id="D15-maletas-bangkok", categoria="UN CASO REAL", juzgado="Juzgado de lo Mercantil n.º 1 de Donostia", fecha="19 de agosto de 2020", pdf="sentencia-D15.pdf",
 titulo=["Biarritz–Bangkok: llegaron y sus maletas tardaron siete días en aparecer", "El juez obliga a la aerolínea a pagarles *790 € por el mal rato*"], titulo_tam=74,
 portada_dato=["790 €", "de daño moral, además de los gastos"],
 tramos=[
  t("gancho", "D15-1", ["Llegaron a Bangkok y sus maletas tardaron siete días en aparecer.", "El juez obliga a la aerolínea a pagarles 790 euros por el mal rato."],
    locucion="Llegaron a Bangkok y sus maletas tardaron siete días en aparecer. El juez obliga a la aerolínea a pagarles setecientos noventa euros por el mal rato."),
  t("doc", "D15-2", ["La aerolínea ya les había pagado lo que gastaron en ropa y en lo básico.", "Y decía que con eso ya estaban indemnizados."],
    pagina_num=2, subrayar=["considera que han sido ya indemnizados los pasajeros"], margen=[150, 60], doc_entra=1.2,
    cita="«… *considera que han sido ya indemnizados los pasajeros*…»"),
  t("doc", "D15-3", ["Pero el juez dijo que llegar a otro país y que no aparezca la maleta ya es un trastorno importante.", "Y fijó cincuenta euros por persona y día de retraso."],
    pagina_num=4, subrayar=["no aparecer la maleta ya es un trastorno importante", "lo fijamos en 50 euros por día"], margen=[110, 60], doc_entra=0.2,
    cita="«… *no aparecer la maleta ya es un trastorno importante* (…) *lo fijamos en 50 euros por día*…»"),
  t("lista", "D15-4", [], locucion="Esto es lo que la aerolínea tendrá que pagarles, además de los gastos: setecientos euros por los siete días sin maletas a la ida, noventa por la maleta que tardó tres días a la vuelta, y los intereses.",
    cabecera="Lo que la aerolínea tendrá que pagarles", total=["Además de los gastos que ya cobraron:", "790 € + intereses"], extra=1.4,
    items=[dict(t="700 €", d="por siete días sin maletas a la ida", palabra="setecientos"), dict(t="90 €", d="por la maleta que tardó tres días a la vuelta", palabra="noventa"),
           dict(t="Intereses", d="desde la demanda", palabra="los intereses")]),
  t("consejo", "D15-5", ["¿Tu maleta no llega?", "Haz el parte en el aeropuerto y reclama por escrito antes de 21 días.", "Además de los gastos, puedes pedir el daño moral."],
    grande="¿Tu maleta *no llega*?", pequeno="Parte en el aeropuerto y reclamación por escrito antes de 21 días.", norma="Convenio de Montreal, arts. 19, 22 y 31"),
 ],
 cierre=dict(CIERRE, legal="Convenio de Montreal, arts. 19, 22 y 31. Imágenes de archivo. Cada caso se estudia de forma individual."), musica=MUS)

STOCK = {
 "D11": {"1": dict(stock="D11-montaje-gancho.mp4", modo="marco", marco_y=820), "2": dict(stock="D11-montaje-sentencia.mp4", modo="marco"),
         "3": dict(stock="D11-montaje-sentencia2.mp4", modo="marco"), "4": dict(stock="maleta-maletero-aeropuerto-lenta_2971254.mp4", modo="lleno"),
         "5": dict(stock="bebe-mochila-aeropuerto_3036639.mp4", modo="marco", desde=1),
         "portada": dict(portada_stock="bebe-mochila-aeropuerto_3036639.mp4", portada_desde=3, portada_modo="marco", portada_marco_y=640)},
 "D12": {"1": dict(stock="D12-montaje-gancho.mp4", modo="marco", marco_y=820), "2": dict(stock="ciudad-noche-ventanilla_7285533.mp4", modo="marco"),
         "3": dict(stock="madre-nina-dormidas-terminal_56937.mp4", modo="marco", desde=6.5), "4": dict(stock="miami-dron_5026772.mp4", modo="lleno", desde=14),
         "5": dict(stock="ciudad-noche-ventanilla_7285533.mp4", modo="marco", desde=11),
         "portada": dict(portada_stock="miami-dron_5026772.mp4", portada_desde=8, portada_modo="marco", portada_marco_y=640)},
 "D13": {"1": dict(stock="D13-montaje-gancho.mp4", modo="marco", marco_y=820), "2": dict(stock="hombre-movil-ventanal-aeropuerto_4960694.mp4", modo="marco", desde=3),
         "3": dict(stock="munich-dron_690454.mp4", modo="marco", desde=5), "4": dict(stock="hombre-agobiado-movil-terminal-lenta_10225718.mp4", modo="lleno"),
         "5": dict(stock="hombre-movil-ventanal-aeropuerto_4960694.mp4", modo="marco", desde=8),
         "portada": dict(portada_stock="hombre-agobiado-movil-terminal_10225718.mp4", portada_desde=3, portada_modo="marco", portada_marco_y=640)},
 "D14": {"1": dict(stock="montreal-dron_5770753.mp4", modo="marco", marco_y=820), "2": dict(stock="mostrador-facturacion-pasaporte-lenta_2744563.mp4", modo="marco"),
         "3": dict(stock="hombre-gafas-movil-sala-espera_4874054.mp4", modo="marco"), "4": dict(stock="montreal-dron_5770753.mp4", modo="lleno", desde=15),
         "5": dict(stock="D14-montaje-consejo.mp4", modo="marco"),
         "portada": dict(portada_stock="montreal-dron_5770753.mp4", portada_desde=3, portada_modo="marco", portada_marco_y=640)},
 "D15": {"1": dict(stock="D15-montaje-gancho.mp4", modo="marco", marco_y=820), "2": dict(stock="mujer-cinta-equipajes_5951.mp4", modo="marco", desde=6),
         "3": dict(stock="bangkok-dron_29199.mp4", modo="marco", desde=8), "4": dict(stock="maletas-cinta-vertical_3626062.mp4", modo="lleno"),
         "5": dict(stock="mujer-cinta-equipajes_5951.mp4", modo="marco", desde=18),
         "portada": dict(portada_stock="mujer-cinta-equipajes_5951.mp4", portada_desde=4, portada_modo="marco", portada_marco_y=640)},
}

if __name__ == "__main__":
    for k, s in S.items():
        for i, tr in enumerate(s["tramos"], 1):
            tr.update(STOCK.get(k, {}).get(str(i), {}))
        s.update(STOCK.get(k, {}).get("portada", {}))
        json.dump(s, open(f"specs/{k}-v3.json", "w"), ensure_ascii=False, indent=1)
        print(k, len(s["tramos"]), "tramos")
    json.dump({k: [tr["locucion"] for tr in s["tramos"]] for k, s in S.items()}, open("/tmp/locuciones-d11-d13.json", "w"), ensure_ascii=False, indent=1)
