#!/usr/bin/env python3
"""Specs de los vídeos de sentencias D7-D10 («El documento, subrayado» v3), 3/11/2026.
Sentencias nuevas que Sergio dejó en Magnific/sentencias el 3/11 (copias como sentencia-D7.pdf … sentencia-D10.pdf, nunca en el repo).
Los nombres de los clientes NO van aquí (repositorio público): van en Magnific/sentencias/sentencia-Dn.ocultar.txt, solo en el Mac.
Uso: python3 gen_d7_d10.py  -> escribe specs/D7-v3.json … specs/D10-v3.json. Las imágenes de archivo van en STOCK (abajo)."""
import json
V = "../../../recursos/voces/documento-v3/"
MUS = "../../../recursos/musica/musica-lofi-100bpm.mp3"
CIERRE = {"titulo": "¿Te ha pasado?", "texto": "Te ayudamos a reclamar a la aerolínea.", "subtitulos": ["Llama al 944 027 596"],
          "locucion": "Llama al nueve cuatro cuatro, cero dos siete, cinco nueve seis.", "voz": "../../../recursos/voces/comics-v2/voz-cierre.mp3"}
def t(tipo, n, subs, **kw):
    d = dict(tipo=tipo, subtitulos=subs, **kw); d.setdefault("locucion", " ".join(subs)); d["voz"] = V + n + ".mp3"; return d

S = {}
# D7 · Iberia, tres días en Barajas sin hotel y sin maleta (Mercantil n.º 3 de Bilbao, 25/10/2021). Rebeldía de Iberia.
# Ojo: el fundamento primero dice «1.990,82 euros», pero las partidas del fallo suman 1.890,82 € (224,59 + 1.480 + 186,23). Se usa el fallo.
S["D7"] = dict(id="D7-iberia-barajas", categoria="UN CASO REAL", juzgado="Juzgado de lo Mercantil n.º 3 de Bilbao", fecha="25 de octubre de 2021", pdf="sentencia-D7.pdf",
 titulo=["Bilbao–Dublín: tres días en Barajas sin hotel y sin maleta", "El juez obliga a Iberia a pagarle *1.890 €*"], titulo_tam=78,
 portada_dato=["1.890,82 €", "por tres días en Barajas sin atención, el billete y la maleta"],
 tramos=[
  t("gancho", "D7-1", ["Tres días atrapada en Barajas, sin hotel y sin maleta.", "El juez obliga a Iberia a pagarle casi 1.900 euros."],
    locucion="Tres días atrapada en Barajas, sin hotel y sin maleta. El juez obliga a Iberia a pagarle casi mil novecientos euros."),
  t("doc", "D7-2", ["Volaba de Bilbao a Dublín, con escala en Madrid.", "Iberia tardó dos días en confirmarle que el vuelo estaba cancelado.", "Y en todo ese tiempo, no le ofreció ni un sitio donde dormir."],
    pagina_num=2, subrayar=["la demandada no le ofreció la posibilidad de pernoctar en algún alojamiento"], margen=[150, 60], doc_entra=2.5,
    cita="«… *la demandada no le ofreció la posibilidad de pernoctar en algún alojamiento*.»"),
  t("doc", "D7-3", ["Iberia ni siquiera se presentó al juicio.", "Y el juez dio por probado todo lo que contó la pasajera."],
    pagina_num=2, subrayar=["se declaró en rebeldía a la demandada"], margen=[150, 60], doc_entra=0.2, extra=0.8,
    cita="«… *se declaró en rebeldía a la demandada*…»"),
  t("lista", "D7-4", [], locucion="Esto es lo que Iberia tendrá que pagarle: mil cuatrocientos ochenta euros por los días en Barajas sin atención, la cancelación, la maleta, los intereses y las costas.",
    cabecera="Lo que Iberia tendrá que pagarle", total=["En total:", "1.890,82 € + intereses"], extra=1.2,
    items=[dict(t="1.480 €", d="por tres días en Barajas sin ninguna atención", palabra="mil"), dict(t="224,59 €", d="por la cancelación: el billete que pagó ella y los daños", palabra="la cancelación"),
           dict(t="186,23 €", d="por la maleta perdida", palabra="la maleta"), dict(t="Intereses y costas", d="Iberia paga también el juicio", palabra="los intereses")]),
  t("consejo", "D7-5", ["¿Te cancelan el vuelo y te dejan tirado en el aeropuerto?", "La aerolínea tiene que darte comida y, si hace falta, hotel.", "Guarda los tickets: tienes cinco años para reclamar."],
    grande="¿Te dejaron *tirado en el aeropuerto*?", pequeno="Comida y, si hace falta, hotel: corren a cargo de la aerolínea. Tienes 5 años para reclamar.", norma="Reglamento (CE) 261/2004, arts. 5 y 9"),
 ],
 cierre=dict(CIERRE, legal="Reglamento (CE) 261/2004, arts. 5, 8 y 9. Imágenes de archivo. Cada caso se estudia de forma individual."), musica=MUS)

# D8 · TAP, dos compensaciones: cancelación + retraso del vuelo de repuesto (JPI n.º 11 de Bilbao, 1/2/2023). STJUE 12/3/2020.
S["D8"] = dict(id="D8-tap-doble", categoria="UN CASO REAL", juzgado="Juzgado de Primera Instancia n.º 11 de Bilbao", fecha="1 de febrero de 2023", pdf="sentencia-D8.pdf",
 titulo=["Lisboa–Bilbao: le cancelaron el vuelo y el de repuesto también llegó tarde", "El juez obliga a TAP a pagarle *dos compensaciones*"], titulo_tam=72,
 portada_dato=["530,88 €", "dos compensaciones y los taxis"],
 tramos=[
  t("gancho", "D8-1", ["TAP le canceló el vuelo de Lisboa a Bilbao.", "El de repuesto también llegó tarde.", "Y el juez le dio dos compensaciones."]),
  t("doc", "D8-2", ["TAP solo quería pagar una.", "Decía que el retraso del vuelo de repuesto no se podía sumar."],
    pagina_num=2, subrayar=["sólo procede una compensación por la cancelación"], margen=[150, 60], doc_entra=0.2, extra=0.6,
    cita="«… *sólo procede una compensación por la cancelación*, a la que no se puede adicionar la compensación por el retraso del vuelo alternativo…»"),
  t("doc", "D8-3", ["Pero el juez, apoyándose en el Tribunal de Justicia de la Unión Europea,", "le reconoció una compensación por cada problema."],
    pagina_num=3, subrayar=["un derecho a compensación por cada uno de esos sucesivos inconvenientes", "procede la estimación de las dos compensaciones"], margen=[110, 60], doc_entra=0.2,
    cita="«… *un derecho a compensación por cada uno de esos sucesivos inconvenientes* (…) *procede la estimación de las dos compensaciones*…»"),
  t("doc", "D8-4", ["TAP decía que los taxis fueron un gasto voluntario.", "Para el juez, esa asistencia le tocaba a la aerolínea."],
    pagina_num=4, subrayar=["Tal asistencia debía ser prestada por la aerolínea"], margen=[150, 60], doc_entra=1.0,
    cita="«… *Tal asistencia debía ser prestada por la aerolínea* con independencia del derecho de compensación…»"),
  t("lista", "D8-5", [], locucion="Esto es lo que TAP tendrá que pagarle: doscientos cincuenta euros por la cancelación, otros doscientos cincuenta por el retraso del vuelo de repuesto, los taxis, los intereses y las costas.",
    cabecera="Lo que TAP tendrá que pagarle", total=["En total:", "530,88 € + intereses"], extra=1.2,
    items=[dict(t="250 €", d="por la cancelación", palabra="doscientos"), dict(t="Otros 250 €", d="por el retraso del vuelo de repuesto", palabra="otros"),
           dict(t="Los taxis en Lisboa", d="30,88 €, al alojamiento y de vuelta al aeropuerto", palabra="los taxis"), dict(t="Intereses y costas", d="TAP paga también el juicio", palabra="los intereses")]),
  t("consejo", "D8-6", ["¿Te cancelaron el vuelo y el de repuesto también llegó tarde?", "Si es la misma aerolínea y llega con tres horas o más de retraso,", "puedes reclamar por los dos. Tienes cinco años."],
    grande="¿El vuelo de repuesto *también llegó tarde*?", pequeno="Si es la misma aerolínea, puedes reclamar por los dos. Tienes 5 años.", norma="Reglamento (CE) 261/2004, art. 7 · TJUE, 12 de marzo de 2020"),
 ],
 cierre=dict(CIERRE, legal="Reglamento (CE) 261/2004, arts. 5, 7 y 9; STJUE de 12 de marzo de 2020. Imágenes de archivo. Cada caso se estudia de forma individual."), musica=MUS)

# D9 · TAP culpó al viento en Bilbao sin pruebas (JPI n.º 1 de Bilbao, 19/5/2023).
S["D9"] = dict(id="D9-tap-viento", categoria="UN CASO REAL", juzgado="Juzgado de Primera Instancia n.º 1 de Bilbao", fecha="19 de mayo de 2023", pdf="sentencia-D9.pdf",
 titulo=["Bilbao–Lisboa: TAP canceló el vuelo y le echó la culpa al viento", "El juez le pidió pruebas: *250 € a cada pasajero*"], titulo_tam=76,
 portada_dato=["750 €", "para tres pasajeros: 250 € cada uno"],
 tramos=[
  t("gancho", "D9-1", ["TAP canceló su vuelo de Bilbao a Lisboa y le echó la culpa al viento.", "Pero el juez le pidió pruebas."]),
  t("doc", "D9-2", ["TAP alegó fuertes rachas de viento en el aeropuerto de Bilbao.", "Y que por eso no tenía que pagar nada."],
    pagina_num=2, subrayar=["debido a las fuertes rachas de viento"], margen=[150, 60], doc_entra=0.2, extra=0.6,
    cita="«… *debido a las fuertes rachas de viento*, circunstancia extraordinaria que provocó la cancelación del vuelo…»"),
  t("doc", "D9-3", ["Pero solo presentó un certificado hecho por ella misma.", "Ningún documento oficial, como uno de ENAIRE, probaba que ese vuelo se viera afectado."],
    pagina_num=6, subrayar=["no se estima como prueba suficiente el certificado que se aporta", "unilateralmente confeccionado por la compañía"], margen=[110, 60], doc_entra=0.2,
    cita="«… *no se estima como prueba suficiente el certificado que se aporta, unilateralmente confeccionado por la compañía*…»"),
  t("lista", "D9-4", [], locucion="Esto es lo que TAP tendrá que pagarles: doscientos cincuenta euros a cada uno de los tres pasajeros, los intereses y las costas.",
    cabecera="Lo que TAP tendrá que pagarles", total=["En total, para los tres:", "750 € + intereses"], extra=1.4,
    items=[dict(t="250 € a cada uno", d="de compensación por la cancelación", palabra="doscientos"), dict(t="Intereses", d="desde que se presentó la demanda", palabra="los intereses"),
           dict(t="Las costas", d="TAP paga también el juicio", palabra="las costas")]),
  t("consejo", "D9-5", ["¿Te cancelan el vuelo y te dicen que es por el tiempo?", "No te conformes: la aerolínea tiene que probarlo.", "Tienes cinco años para reclamar."],
    grande="¿Te dijeron que *fue por el tiempo*?", pequeno="La aerolínea tiene que probarlo. Tienes 5 años para reclamar.", norma="Reglamento (CE) 261/2004, art. 5.3"),
 ],
 cierre=dict(CIERRE, legal="Reglamento (CE) 261/2004, arts. 5 y 7. Imágenes de archivo. Cada caso se estudia de forma individual."), musica=MUS)

# D10 · Iberia, Donostia–Madrid cancelado por avería; taxi para no perder el vuelo a Estambul (JPI n.º 4 de Donostia, 18/3/2025). Sentencia escaneada (OCR).
S["D10"] = dict(id="D10-iberia-taxi", categoria="UN CASO REAL", juzgado="Juzgado de Primera Instancia n.º 4 de Donostia", fecha="18 de marzo de 2025", pdf="sentencia-D10.pdf",
 titulo=["Donostia–Madrid: Iberia les canceló el vuelo y fueron en taxi para no perder su conexión", "El juez obliga a Iberia a pagar *también el taxi*"], titulo_tam=68,
 portada_dato=["1.275 €", "compensación y taxi para los dos"],
 tramos=[
  t("gancho", "D10-1", ["Iberia les canceló el vuelo de Donostia a Madrid y les ofreció otro al día siguiente.", "Para no perder su vuelo a Estambul, fueron en taxi.", "Y el juez obliga a Iberia a pagarlo."]),
  t("doc", "D10-2", ["Iberia reconoció que fue por una avería.", "Aceptaba pagar 250 euros a cada uno, pero no el taxi."],
    locucion="Iberia reconoció que fue por una avería. Aceptaba pagar doscientos cincuenta euros a cada uno, pero no el taxi.",
    pagina_num=2, subrayar=["fue por una avería técnica", "reconociendo en este punto su responsabilidad"], margen=[150, 60], doc_entra=0.2,
    cita="«… *fue por una avería técnica*, y *reconociendo en este punto su responsabilidad* y su obligación de indemnizar…»"),
  t("doc", "D10-3", ["Para el juez, el vuelo del día siguiente no les servía: con él perdían el enlace a Estambul.", "Así que el taxi corre a cargo de Iberia."],
    pagina_num=4, subrayar=["la pérdida por los demandantes de su enlace", "debe acogerse también el importe solicitado"], margen=[110, 60], doc_entra=0.2,
    cita="«… supondría, materialmente, *la pérdida por los demandantes de su enlace* (…) y *debe acogerse también el importe solicitado* por dicho transporte alternativo.»"),
  t("lista", "D10-4", [], locucion="Esto es lo que Iberia tendrá que pagarles: doscientos cincuenta euros a cada uno, el taxi de Donostia a Madrid, los intereses y las costas.",
    cabecera="Lo que Iberia tendrá que pagarles", total=["En total, para los dos:", "1.275 € + intereses"], extra=1.4,
    items=[dict(t="250 € a cada uno", d="de compensación por la cancelación", palabra="doscientos"), dict(t="El taxi a Madrid", d="775 €: 387,50 € por persona", palabra="el taxi"),
           dict(t="Intereses y costas", d="Iberia paga también el juicio", palabra="los intereses")]),
  t("consejo", "D10-5", ["¿El vuelo de repuesto te hace perder tu conexión?", "La aerolínea tiene que llevarte a tu destino lo antes posible.", "Si te buscas otra forma, guarda las facturas."],
    grande="¿El vuelo de repuesto *no te sirve*?", pequeno="Guarda las facturas: tienes 5 años para reclamar.", norma="Reglamento (CE) 261/2004, art. 8"),
 ],
 cierre=dict(CIERRE, legal="Reglamento (CE) 261/2004, arts. 5, 7 y 8. Imágenes de archivo. Cada caso se estudia de forma individual."), musica=MUS)

# Imágenes de archivo por tramo (1-based) y portada; se rellena al elegir los clips.
STOCK = {
 "D7": {"1": dict(stock="sillas-vacias-aeropuerto-noche_3637085.mp4", modo="marco"), "2": dict(stock="panel-cancelado-IA_7462012.mp4", modo="marco"),
        "3": dict(stock="sillas-vacias-aeropuerto-noche_3637085.mp4", modo="marco", desde=5), "4": dict(stock="cinta-equipajes-vacia-vertical_8426064.mp4", modo="lleno"),
        "5": dict(stock="panel-cancelado-IA_7462012.mp4", modo="marco", desde=1),
        "portada": dict(portada_stock="sillas-vacias-aeropuerto-noche_3637085.mp4", portada_desde=2, portada_modo="marco", portada_marco_y=640)},
 "D8": {"1": dict(stock="D8-montaje-gancho.mp4", modo="marco"), "2": dict(stock="avion-aterrizando-ciudad_4215534.mp4", modo="marco", desde=6),
        "3": dict(stock="tranvia-lisboa-lenta_7396767.mp4", modo="marco", desde=3), "4": dict(stock="coche-ciudad-noche_6826313.mp4", modo="marco"),
        "5": dict(stock="coche-ciudad-noche_6826313.mp4", modo="lleno", desde=10), "6": dict(stock="avion-aterrizando-ciudad_4215534.mp4", modo="marco", desde=1),
        "portada": dict(portada_stock="tranvia-lisboa-lenta_7396767.mp4", portada_desde=2, portada_modo="marco", portada_marco_y=640)},
 "D9": {"1": dict(stock="D9-montaje-gancho.mp4", modo="marco"), "2": dict(stock="manga-viento-rachas-lenta_8889993.mp4", modo="marco"),
        "3": dict(stock="aviones-rodando-pista_831579.mp4", modo="marco", desde=16), "4": dict(stock="aviones-rodando-pista_831579.mp4", modo="lleno", desde=20),
        "5": dict(stock="manga-viento-rachas-lenta_8889993.mp4", modo="marco", desde=2),
        "portada": dict(portada_stock="manga-viento-rachas-lenta_8889993.mp4", portada_desde=1, portada_modo="marco", portada_marco_y=640)},
 "D10": {"1": dict(stock="D10-montaje-gancho.mp4", modo="marco"), "2": dict(stock="coche-asiento-trasero-autopista-lenta-volteado_9222585.mp4", modo="marco", desde=2),
         "3": dict(stock="avion-silueta-cielo-dorado_3035784.mp4", modo="marco"), "4": dict(stock="donostia-concha-dron_9592862.mp4", modo="lleno", desde=10),
         "5": dict(stock="avion-silueta-cielo-dorado_3035784.mp4", modo="marco", desde=5),
         "portada": dict(portada_stock="donostia-concha-dron_9592862.mp4", portada_desde=4, portada_modo="marco", portada_marco_y=640)},
}

if __name__ == "__main__":
    for k, s in S.items():
        for i, tr in enumerate(s["tramos"], 1):
            tr.update(STOCK.get(k, {}).get(str(i), {}))
        s.update(STOCK.get(k, {}).get("portada", {}))
        json.dump(s, open(f"specs/{k}-v3.json", "w"), ensure_ascii=False, indent=1)
        print(k, len(s["tramos"]), "tramos")
    json.dump({k: [tr["locucion"] for tr in s["tramos"]] for k, s in S.items()}, open("/tmp/locuciones-d7-d10.json", "w"), ensure_ascii=False, indent=1)
