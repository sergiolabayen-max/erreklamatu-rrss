#!/usr/bin/env python3
"""Specs de los vídeos de consejos (a partir de los artículos del blog que Sergio pasó el 3/11/2026).
Formato: gancho + un tramo «consejo» por punto (etiqueta numerada + titular; la explicación va en la voz y los subtítulos, sin texto pequeño para no duplicarla) + cierre. Atemporales: sin Navidad, verano ni años.
Criterios: 3-7 puntos (los más útiles), ritmo (frases cortas, un plano por punto), imágenes reales y sin logotipos de aerolíneas.
Uso: python3 gen_consejos.py -> specs/C1-v1.json …"""
import json
V = "../../../recursos/voces/consejos-v1/"
MUS = "../../../recursos/musica/musica-lofi-100bpm.mp3"
CIERRE = {"titulo": "¿Te ha pasado?", "texto": "Te ayudamos a reclamar a la aerolínea.", "subtitulos": ["Llama al 944 027 596"],
          "locucion": "Llama al nueve cuatro cuatro, cero dos siete, cinco nueve seis.", "voz": "../../../recursos/voces/comics-v2/voz-cierre.mp3"}
def t(tipo, n, subs, **kw):
    d = dict(tipo=tipo, subtitulos=subs, **kw); d.setdefault("locucion", " ".join(subs)); d["voz"] = V + n + ".mp3"; return d

S = {}
# C1 · «Los 10 errores que te pueden dejar sin indemnización» (artículo de Jon Ortiz). Se quedan los 5 más útiles + el cierre «no reclamar».
# Fuera: equipaje (PIR, va en su propio vídeo), overbooking y reembolso/vuelo alternativo (el artículo mezcla ahí la regla de las 3 horas,
# que en cancelaciones no es la que decide), y el aviso de 14 días (va en el vídeo de cancelaciones).
S["C1"] = dict(id="C1-errores-indemnizacion", categoria="CONSEJOS", portada_pie="Guía rápida · ERREKLAMATU",
 titulo=["5 errores que te pueden dejar sin indemnización", "si te retrasan o cancelan *un vuelo*"], titulo_tam=84,
 portada_dato=["5 errores", "y el peor de todos: no reclamar"],
 tramos=[
  t("gancho", "C1-1", ["¿Te han retrasado o cancelado un vuelo?", "Estos cinco errores te pueden dejar sin indemnización."]),
  t("consejo", "C1-2", ["Uno: tirar la tarjeta de embarque.", "Es la prueba de que ibas en ese vuelo. Guárdala."],
    num="ERROR 1 DE 5", grande="Tirar la *tarjeta de embarque*"),
  t("consejo", "C1-3", ["Dos: mirar la hora de salida.", "Lo que cuenta es la hora de llegada: con tres horas o más de retraso, puedes tener derecho a compensación."],
    num="ERROR 2 DE 5", grande="Mirar la hora *de salida*"),
  t("consejo", "C1-4", ["Tres: aceptar un vale sin leer la letra pequeña.", "Si lo aceptas como compensación, puedes estar renunciando al dinero."],
    num="ERROR 3 DE 5", grande="Aceptar un *vale* sin leer la letra pequeña", tam=84),
  t("consejo", "C1-5", ["Cuatro: creerte lo de las circunstancias extraordinarias.", "La aerolínea tiene que demostrarlas. Y no siempre puede."],
    num="ERROR 4 DE 5", grande="Creerte lo de las *circunstancias extraordinarias*", tam=80),
  t("consejo", "C1-6", ["Cinco: pagar los gastos de tu bolsillo.", "Comida, hotel o traslados por la incidencia también se reclaman. Guarda los tickets."],
    num="ERROR 5 DE 5", grande="Pagar los gastos *de tu bolsillo*"),
  t("consejo", "C1-7", ["Y el peor de todos: no reclamar.", "Que la aerolínea diga que no al principio no significa que no tengas razón."],
    grande="Y el peor: *no reclamar*"),
 ],
 cierre=dict(CIERRE, legal="Reglamento (CE) 261/2004. Imágenes de archivo. Cada caso se estudia de forma individual."), musica=MUS)

L261 = "Reglamento (CE) 261/2004. Imágenes de archivo. Cada caso se estudia de forma individual."
LMTL = "Convenio de Montreal, arts. 17, 19 y 31. Imágenes de archivo. Cada caso se estudia de forma individual."
def palabras(x):
    """La locución, con las cifras en letra (los subtítulos las dejan en número)."""
    for a, b in (("250", "doscientos cincuenta"), ("600", "seiscientos"), ("14 días", "catorce días")): x = x.replace(a, b)
    return x
def serie(k, idv, cat, titulo, dato, gancho, items, etiqueta, legal=L261, tam=84):
    """Vídeo de consejos: gancho (lista de frases) + un tramo por punto. items = [(frases de la voz, titular en pantalla, tam opcional)]."""
    n = len(items); tr = [t("gancho", f"{k}-1", gancho, locucion=palabras(" ".join(gancho)))]
    for i, it in enumerate(items, 1):
        frases, grande = it[0], it[1]; kw = dict(tam=it[2]) if len(it) > 2 else {}
        tr.append(t("consejo", f"{k}-{i+1}", frases, locucion=palabras(" ".join(frases)), num=f"{etiqueta} {i} DE {n}", grande=grande, **kw))
    S[k] = dict(id=idv, categoria=cat, portada_pie="Guía rápida · ERREKLAMATU", titulo=titulo, titulo_tam=tam, portada_dato=dato, tramos=tr,
                cierre=dict(CIERRE, legal=legal), musica=MUS)

# ── Versión corta de C1 (prueba de duración pedida por Sergio el 3/11: «haz otra versión más breve, de 25 segundos»): voces propias, más cortas.
serie("C1c", "C1c-errores-indemnizacion-corto", "CONSEJOS", ["3 errores que te pueden dejar sin indemnización", "si te retrasan o cancelan *un vuelo*"],
 ["3 errores", "que te pueden dejar sin indemnización"],
 ["Tres errores que te pueden dejar sin indemnización si te retrasan o cancelan un vuelo."],
 [(["Uno: tirar la tarjeta de embarque. Es tu prueba."], "Tirar la *tarjeta de embarque*"),
  (["Dos: mirar la hora de salida. Cuenta la de llegada."], "Mirar la hora *de salida*"),
  (["Tres: aceptar un vale. Puedes estar renunciando al dinero."], "Aceptar un *vale* sin leer la letra pequeña", 84)], "ERROR")

# C2 · «10 preguntas frecuentes sobre cancelaciones de vuelos» (Navidad fuera). Reglamento 261/2004, arts. 5, 7, 8 y 9.
serie("C2", "C2-cancelacion-derechos", "TUS DERECHOS", ["Te cancelan el vuelo: 5 cosas que la aerolínea te debe", "*conócelas* antes de aceptar nada"],
 ["250-600 €", "de compensación si la culpa es de la aerolínea"],
 ["¿Te han cancelado el vuelo?", "Esto es lo que la aerolínea te debe."],
 [(["Uno: tú eliges.", "Que te devuelvan el billete o que te lleven a tu destino en otro vuelo."], "Tú eliges: *reembolso u otro vuelo*"),
  (["Dos: mientras esperas, comida y bebida.", "Y si toca pasar la noche, hotel y traslado."], "Comida, bebida y *hotel* si hace falta"),
  (["Tres: una compensación de 250 a 600 euros, según la distancia.", "Salvo circunstancias extraordinarias."], "De *250 a 600 €* según la distancia"),
  (["Cuatro: si te avisan con menos de 14 días, por regla general, también hay compensación."], "Aviso con menos de *14 días*"),
  (["Cinco: si pierdes la conexión y todo iba en la misma reserva,", "te tienen que llevar hasta el destino final."], "Conexión perdida: *hasta el destino final*", 80)], "DERECHO")
serie("C2c", "C2c-cancelacion-derechos-corto", "TUS DERECHOS", ["Te cancelan el vuelo: 3 cosas que la aerolínea te debe", "*conócelas* antes de aceptar nada"],
 ["250-600 €", "de compensación si la culpa es de la aerolínea"],
 ["¿Te cancelan el vuelo? Tres cosas que te deben."],
 [(["Uno: reembolso u otro vuelo. Tú eliges."], "Tú eliges: *reembolso u otro vuelo*"),
  (["Dos: comida, bebida y hotel si hace falta."], "Comida, bebida y *hotel* si hace falta"),
  (["Tres: de 250 a 600 euros, si la culpa es suya."], "De *250 a 600 €* según la distancia")], "DERECHO")

# C3 · «10 preguntas frecuentes sobre retrasos de vuelos» (Semana Santa fuera). Arts. 3, 6, 7, 8 y 9; STJUE Sturgeon (C-402/07) y Germanwings (C-452/13).
# El artículo dice que se puede pedir el reembolso si el viaje «pierde su finalidad»; el vídeo usa la regla del reglamento: 5 horas o más (art. 6.1.iii).
serie("C3", "C3-retraso-claves", "TUS DERECHOS", ["Tu vuelo se retrasa: 5 cosas que debes saber", "para *no perder* lo que te corresponde"],
 ["3 horas", "de retraso en destino: puede haber compensación"],
 ["¿Tu vuelo va con retraso?", "Cinco cosas que tienes que saber."],
 [(["Uno: con un retraso largo, te tienen que dar de comer y de beber.", "Desde dos horas, según la distancia."], "Comida y bebida *desde 2 horas*"),
  (["Dos: el retraso se cuenta hasta que se abren las puertas del avión,", "no hasta que aterriza."], "Cuenta *cuando se abren las puertas*"),
  (["Tres: si llegas con tres horas o más de retraso,", "puede haber una compensación de 250 a 600 euros."], "*3 horas* o más: compensación"),
  (["Cuatro: con cinco horas o más de retraso,", "puedes no volar y pedir que te devuelvan el billete."], "*5 horas*: puedes no volar y pedir el dinero", 80),
  (["Cinco: si sales de un aeropuerto europeo, te protege la ley europea,", "aunque la aerolínea no sea europea."], "Sales de la UE: *te protege igual*")], "CLAVE")
serie("C3c", "C3c-retraso-claves-corto", "TUS DERECHOS", ["Tu vuelo se retrasa: 3 cosas que debes saber", "para *no perder* lo que te corresponde"],
 ["3 horas", "de retraso en destino: puede haber compensación"],
 ["¿Tu vuelo se retrasa? Tres cosas que debes saber."],
 [(["Uno: con un retraso largo, te tienen que dar de comer."], "Comida y bebida *desde 2 horas*"),
  (["Dos: cuenta cuando se abren las puertas, no cuando aterriza."], "Cuenta *cuando se abren las puertas*"),
  (["Tres: con tres horas o más en destino, puede haber compensación."], "*3 horas* o más: compensación")], "CLAVE")

# C4 · «10 preguntas frecuentes sobre reclamaciones por equipaje» (verano fuera). Convenio de Montreal, arts. 17.3, 19 y 31.
# No se da la cifra del tope: el artículo dice 1.288 DEG, pero desde el 28/12/2024 es 1.519 DEG (revisión de la OACI; BOE-A-2025-3872).
serie("C4", "C4-maleta-pasos", "CONSEJOS", ["Tu maleta no aparece: 5 pasos para reclamar", "el primero, *antes de salir* del aeropuerto"],
 ["5 pasos", "para reclamar si tu maleta no aparece"],
 ["¿Tu maleta no ha salido por la cinta?", "Cinco pasos para reclamar."],
 [(["Uno: antes de salir del aeropuerto,", "haz el parte de irregularidad de equipaje en el mostrador."], "El *parte (PIR)* antes de salir"),
  (["Dos: si tienes que comprar ropa o cosas de aseo, guarda los tickets.", "Solo lo razonable."], "Compras urgentes: *guarda los tickets*"),
  (["Tres: aunque te digan que fue culpa del servicio de equipajes,", "responde la aerolínea."], "Responde *la aerolínea*"),
  (["Cuatro: los plazos son cortos.", "Siete días si la maleta llega dañada, veintiuno si llega tarde."], "*7 días* si está dañada, *21* si llega tarde", 80),
  (["Cinco: si en veintiún días no aparece, se da por perdida.", "Haz una lista de lo que llevabas."], "21 días sin maleta: *perdida*")], "PASO", legal=LMTL)
serie("C4c", "C4c-maleta-pasos-corto", "CONSEJOS", ["Tu maleta no aparece: 3 pasos para reclamar", "el primero, *antes de salir* del aeropuerto"],
 ["3 pasos", "para reclamar si tu maleta no aparece"],
 ["¿Tu maleta no aparece? Tres pasos para reclamar."],
 [(["Uno: el parte, antes de salir del aeropuerto."], "El *parte (PIR)* antes de salir"),
  (["Dos: compras urgentes, con ticket."], "Compras urgentes: *guarda los tickets*"),
  (["Tres: plazos cortos. Siete días si está dañada, veintiuno si llega tarde."], "*7 días* si está dañada, *21* si llega tarde", 80)], "PASO", legal=LMTL)

# C5 · Nota de prensa «10 cosas que debes saber si vas a volar con niños» (verano fuera).
serie("C5", "C5-volar-con-ninos", "CONSEJOS", ["Volar con niños: 5 cosas que debes saber", "antes de llegar al *aeropuerto*"],
 ["5 consejos", "para volar con niños sin sustos"],
 ["¿Vas a volar con niños?", "Cinco cosas que te pueden ahorrar un disgusto."],
 [(["Uno: la leche, el agua y la comida del bebé pueden pasar el control,", "aunque superen el límite de líquidos. Avisa al pasar."], "La comida del bebé *sí pasa el control*", 80),
  (["Dos: pregunta si el carrito llega hasta la puerta del avión.", "Y si sale roto, haz el parte antes de salir."], "El carrito: *¿hasta la puerta del avión?*", 80),
  (["Tres: revisa los asientos al hacer el check-in,", "para no acabar separados de tus hijos."], "Revisa los asientos *en el check-in*"),
  (["Cuatro: lo imprescindible del bebé, en el equipaje de mano.", "Pañales, leche, medicación."], "Lo del bebé, *en el equipaje de mano*"),
  (["Cinco: si os toca pasar la noche por un retraso o una cancelación,", "la aerolínea tiene que daros hotel y traslado."], "¿Noche fuera? *Hotel y traslado*")], "CONSEJO")
serie("C5c", "C5c-volar-con-ninos-corto", "CONSEJOS", ["Volar con niños: 3 cosas que debes saber", "antes de llegar al *aeropuerto*"],
 ["3 consejos", "para volar con niños sin sustos"],
 ["¿Vas a volar con niños? Tres cosas que debes saber."],
 [(["Uno: la leche del bebé sí pasa el control."], "La comida del bebé *sí pasa el control*", 80),
  (["Dos: revisa los asientos en el check-in."], "Revisa los asientos *en el check-in*"),
  (["Tres: lo del bebé, en el equipaje de mano."], "Lo del bebé, *en el equipaje de mano*")], "CONSEJO")

# C6 · «Diez cosas que quizá no sabías sobre tus derechos como pasajero». Arts. 4, 7, 8 y 9; plazo de 5 años (art. 1964 CC, en el Estado español).
# El artículo describe mal el ámbito del reglamento (aerolíneas con sede en Europa «en cualquier parte del mundo»): no se usa.
serie("C6", "C6-derechos-desconocidos", "TUS DERECHOS", ["5 derechos del pasajero que quizá no conocías", "y que *te pueden valer dinero*"],
 ["5 años", "para reclamar tu vuelo"],
 ["Cinco derechos como pasajero de avión que casi nadie conoce."],
 [(["Uno: si te dejan en tierra por overbooking,", "además de otro vuelo, tienes derecho a una compensación."], "Overbooking: *también hay compensación*"),
  (["Dos: la compensación depende de la distancia, no de lo que pagaste.", "Aunque el billete fuera barato."], "Depende de *la distancia*, no del precio"),
  (["Tres: si no te ofrecen otro vuelo, cómpralo tú,", "guarda la factura y reclámalo."], "¿Sin otro vuelo? *Cómpralo y reclámalo*", 80),
  (["Cuatro: durante la espera, te tienen que dejar llamar o enviar un correo."], "Tienes derecho a *comunicarte*"),
  (["Cinco: en el Estado español, tienes cinco años para reclamar.", "Pero mejor no esperes."], "*5 años* para reclamar")], "DERECHO")
serie("C6c", "C6c-derechos-desconocidos-corto", "TUS DERECHOS", ["3 derechos del pasajero que quizá no conocías", "y que *te pueden valer dinero*"],
 ["5 años", "para reclamar tu vuelo"],
 ["Tres derechos del pasajero que casi nadie conoce."],
 [(["Uno: el overbooking también da compensación."], "Overbooking: *también hay compensación*"),
  (["Dos: depende de la distancia, no del precio."], "Depende de *la distancia*, no del precio"),
  (["Tres: tienes cinco años para reclamar."], "*5 años* para reclamar")], "DERECHO")

# C7 · «10 consejos prácticos para reclamar un vuelo» (agosto fuera). Arts. 8.1.a (7 días) y 15 (sin renuncias). Fuera: el «solo el 5 % cobra
# por su cuenta», que el artículo no respalda con ninguna fuente.
serie("C7", "C7-trucos-reclamar", "CONSEJOS", ["5 trucos para reclamar tu vuelo", "y *no dejar dinero* por el camino"],
 ["5 trucos", "para reclamar tu vuelo"],
 ["¿Vas a reclamar un vuelo?", "Cinco trucos para no dejar dinero por el camino."],
 [(["Uno: si pides el reembolso, tienen siete días para devolverte el dinero."], "Reembolso en *7 días*"),
  (["Dos: no firmes nada en lo que renuncies a la compensación."], "No firmes *renuncias*"),
  (["Tres: habla con el resto de pasajeros.", "Cuantos más reclaméis, más fuerza."], "Habla con *los demás pasajeros*"),
  (["Cuatro: no entregues el talón de la maleta.", "Y si te lo piden, hazle una foto."], "El talón de la maleta: *hazle una foto*", 80),
  (["Cinco: ponte en manos de especialistas.", "La consulta es gratis y solo cobramos si ganamos."], "Consulta *gratis*")], "TRUCO")
serie("C7c", "C7c-trucos-reclamar-corto", "CONSEJOS", ["3 trucos para reclamar tu vuelo", "y *no dejar dinero* por el camino"],
 ["3 trucos", "para reclamar tu vuelo"],
 ["Tres trucos para reclamar tu vuelo."],
 [(["Uno: el reembolso, en siete días."], "Reembolso en *7 días*"),
  (["Dos: no firmes renuncias."], "No firmes *renuncias*"),
  (["Tres: habla con los demás pasajeros."], "Habla con *los demás pasajeros*")], "TRUCO")

# C8 · «20 consejos para evitar problemas con tu vuelo» (verano fuera). Prevención; fuera lo que el artículo no respalda
# (que el check-in online «te libra» del overbooking) y las marcas de aplicaciones.
serie("C8", "C8-evitar-problemas", "CONSEJOS", ["5 consejos para que tu vuelo no te dé problemas", "*antes* de salir de casa"],
 ["5 consejos", "antes de volar"],
 ["Cinco consejos para que tu vuelo no te dé problemas."],
 [(["Uno: si hay escalas, que vayan en la misma reserva", "y con margen entre vuelos."], "Escalas: *misma reserva y con margen*", 80),
  (["Dos: activa las alertas de tu vuelo y mira el correo.", "Los cambios llegan por ahí."], "Activa *las alertas*"),
  (["Tres: comprueba que tu pasaporte está vigente.", "Algunos países piden seis meses de validez."], "Pasaporte: *¿te quedan 6 meses?*"),
  (["Cuatro: etiqueta la maleta por fuera y por dentro, con tu teléfono."], "Etiqueta *por fuera y por dentro*"),
  (["Cinco: en el equipaje de mano, una batería y lo básico para unas horas."], "Batería y lo básico *en la mano*")], "CONSEJO")
serie("C8c", "C8c-evitar-problemas-corto", "CONSEJOS", ["3 consejos para que tu vuelo no te dé problemas", "*antes* de salir de casa"],
 ["3 consejos", "antes de volar"],
 ["Tres consejos para que tu vuelo no te dé problemas."],
 [(["Uno: escalas en la misma reserva."], "Escalas: *misma reserva y con margen*", 80),
  (["Dos: activa las alertas del vuelo."], "Activa *las alertas*"),
  (["Tres: etiqueta la maleta por fuera y por dentro."], "Etiqueta *por fuera y por dentro*")], "CONSEJO")

# C9 · «Diez malas prácticas de las compañías aéreas» (Navidad fuera). El artículo dice «más de 15 días»: el reglamento dice 2 semanas (art. 5.1.c).
# Arts. 5, 8, 14 y 15. Se quedan 4 (las otras ya salen en C1, C2 y C6).
serie("C9", "C9-malas-practicas", "CUIDADO", ["4 malas prácticas de las aerolíneas", "y qué hacer si *te pasan*"],
 ["4 malas prácticas", "de las aerolíneas, y qué hacer"],
 ["Cuatro malas prácticas de las aerolíneas,", "y qué hacer si te pasan."],
 [(["Una: te cambian el vuelo semanas antes.", "Si te avisan con catorce días o más, no hay compensación, pero puedes pedir que te devuelvan el dinero."], "Te cambian el vuelo: *puedes pedir el dinero*", 80),
  (["Dos: te dicen que el billete no es reembolsable y te ofrecen un bono.", "Si cancelan ellos, no tienes que aceptarlo."], "¿Un bono? *No estás obligado*"),
  (["Tres: «lo compraste en una agencia».", "Da igual: tus derechos son los mismos."], "«Fue en una agencia»: *da igual*"),
  (["Cuatro: no te informan de tus derechos.", "Y tienen que dártelos por escrito."], "Te deben informar *por escrito*")], "PRÁCTICA")
serie("C9c", "C9c-malas-practicas-corto", "CUIDADO", ["3 malas prácticas de las aerolíneas", "y qué hacer si *te pasan*"],
 ["3 malas prácticas", "de las aerolíneas, y qué hacer"],
 ["Tres malas prácticas de las aerolíneas."],
 [(["Una: te ofrecen un bono. No tienes que aceptarlo."], "¿Un bono? *No estás obligado*"),
  (["Dos: «fue en una agencia». Da igual."], "«Fue en una agencia»: *da igual*"),
  (["Tres: no te informan. Deben hacerlo por escrito."], "Te deben informar *por escrito*")], "PRÁCTICA")

STOCK = {
 "C1": {"1": dict(stock="movil-vuelo-cancelado-tarjeta_8212162.mp4", modo="marco", marco_y=820), "2": dict(stock="tarjeta-embarque-pasaporte-lenta_9692863.mp4", modo="marco"),
        "3": dict(stock="panel-llegadas-arrived-lenta_3055336.mp4", modo="marco"), "4": dict(stock="mostrador-pasajera-documento_2289936.mp4", modo="marco", desde=1),
        "5": dict(stock="ventanilla-lluvia_551110.mp4", modo="marco"), "6": dict(stock="C1-montaje-gastos.mp4", modo="marco"),
        "7": dict(stock="mujer-portatil-casa_7159871.mp4", modo="marco"),
        "portada": dict(portada_stock="movil-vuelo-cancelado-tarjeta_8212162.mp4", portada_desde=3, portada_modo="marco", portada_marco_y=640)},
}

def _m(st, **kw): return dict(stock=st, modo="marco", **kw)
STOCK.update({
 "C2": {"1": _m("hombre-llamada-maleta-hotel_9724030.mp4", desde=2, marco_y=820), "2": _m("mujer-mirando-panel-vuelos_5916077.mp4"),
        "3": _m("abrir-habitacion-hotel-tarjeta_6737621.mp4"), "4": _m("mujer-banca-movil_3089726.mp4"),
        "5": _m("manos-movil-navegando_2872495.mp4"), "6": _m("multitud-terminal-atardecer_10089789.mp4", desde=4)},
 "C3": {"1": _m("pasajeros-durmiendo-terminal_7640560.mp4", marco_y=820), "2": _m("cafe-bolleria-mesa_5993996.mp4"),
        "3": _m("pasajeros-saliendo-pasarela-lenta_3548036.mp4"), "4": _m("mano-reloj-macro_2362760.mp4"),
        "5": _m("persona-andando-maleta-lenta_6112878.mp4"), "6": _m("avion-despegando-torre-control_3425543.mp4")},
 "C4": {"1": _m("cinta-equipajes-vacia_7283089.mp4", marco_y=820), "2": _m("zona-equipajes-mostradores-lenta_7387456.mp4"),
        "3": _m("manos-contando-billetes-euro_7244231.mp4"), "4": _m("equipaje-cargando-bodega_3547467.mp4"),
        "5": _m("pasajeros-recogiendo-maletas-cinta_5321253.mp4", desde=3), "6": _m("mano-escribiendo-cuaderno-lenta_2425280.mp4")},
 "C5": {"1": _m("familia-bebe-aeropuerto-avion_4391364.mp4", marco_y=820), "2": _m("bebe-biberon-manos_6077255.mp4"),
        "3": _m("padre-carrito-bebe-aeropuerto_3013810.mp4"), "4": _m("familia-bebe-hijo-volando_3031751.mp4"),
        "5": _m("panales-juguetes-bebe_3729437.mp4"), "6": _m("pareja-piernas-pasillo-hotel_1455768.mp4", desde=8)},
 "C6": {"1": _m("pasajeros-varados-malas-noticias_7578287.mp4", marco_y=820), "2": _m("pasajeros-varados-malas-noticias_7578287.mp4", desde=17),
        "3": _m("ruta-avion-atlantico-mapa_7641082.mp4", desde=8), "4": _m("hombre-reservando-portatil-movil_5329673.mp4"),
        "5": _m("hombre-telefono-sala-espera_5474350.mp4"), "6": _m("calendario-pasando-meses_3297288.mp4")},
 "C7": {"1": _m("mano-papel-mesa-madera_5761375.mp4", marco_y=820), "2": _m("manos-tecleando-portatil_7457582.mp4"),
        "3": _m("mano-papel-mesa-madera_5761375.mp4", desde=20), "4": _m("grupo-pasajeros-hablando-aeropuerto_7781173.mp4"),
        "5": _m("maleta-roja-etiqueta-vacia_8805988.mp4"), "6": _m("boli-apreton-manos-mesa_4362732.mp4")},
 "C8": {"1": _m("manos-haciendo-maleta_8358758.mp4", marco_y=820), "2": _m("pasillo-rodante-aeropuerto_400600.mp4", desde=2),
        "3": _m("persona-usando-movil_3800092.mp4"), "4": _m("manos-pasaporte-puerta-embarque_3297994.mp4"),
        "5": _m("manos-etiqueta-maleta_7897725.mp4"), "6": _m("movil-cargando-bateria-externa_3667989.mp4")},
 "C9": {"1": _m("hombre-serio-portatil-cocina_5042236.mp4", marco_y=820), "2": _m("azafata-tierra-mostrador-pasaporte_2744579.mp4"),
        "3": _m("ejecutivo-entregando-documentos_2552355.mp4"), "4": _m("agente-viajes-pasaporte_8425923.mp4"),
        "5": _m("agente-viajes-pasaporte_8425923.mp4", desde=8.5)},
})
# Versiones de 25 s: reutilizan los planos de su versión larga (gancho + tres puntos).
for _k, _idx in {"C1": [2, 3, 4], "C2": [2, 3, 4], "C3": [2, 3, 4], "C4": [2, 3, 5], "C5": [2, 4, 5], "C6": [2, 3, 6],
                 "C7": [2, 3, 4], "C8": [2, 3, 5], "C9": [3, 4, 5]}.items():
    _L = STOCK[_k]
    STOCK[_k + "c"] = {"1": _L["1"], **{str(j): _L[str(i)] for j, i in enumerate(_idx, 2)}, "portada": _L.get("portada", {})}

if __name__ == "__main__":
    for k, s in S.items():
        for i, tr in enumerate(s["tramos"], 1):
            tr.update(STOCK.get(k, {}).get(str(i), {}))
        s.update(STOCK.get(k, {}).get("portada", {}))
        json.dump(s, open(f"specs/{k}-v1.json", "w"), ensure_ascii=False, indent=1)
        print(k, len(s["tramos"]), "tramos")
    json.dump({k: [tr["locucion"] for tr in s["tramos"]] for k, s in S.items()}, open("/tmp/locuciones-consejos.json", "w"), ensure_ascii=False, indent=1)
