#!/usr/bin/env python3
"""Specs de los vídeos de consejos (a partir de los artículos del blog que Sergio pasó el 3/11/2026).
Formato: gancho + un tramo «consejo» por punto (con etiqueta numerada) + cierre. Atemporales: sin Navidad, verano ni años.
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
S["C1"] = dict(id="C1-errores-indemnizacion", categoria="EVITA ESTOS ERRORES",
 titulo=["5 errores que te pueden dejar sin indemnización", "si te retrasan o cancelan *un vuelo*"], titulo_tam=84,
 portada_dato=["5 errores", "que te pueden dejar sin indemnización"],
 tramos=[
  t("gancho", "C1-1", ["¿Te han retrasado o cancelado un vuelo?", "Estos cinco errores te pueden dejar sin indemnización."]),
  t("consejo", "C1-2", ["Uno: tirar la tarjeta de embarque.", "Es la prueba de que ibas en ese vuelo. Guárdala."],
    num="ERROR 1 DE 5", grande="Tirar la *tarjeta de embarque*", pequeno="Es la prueba de que ibas en ese vuelo. Guárdala, aunque sea en el móvil."),
  t("consejo", "C1-3", ["Dos: mirar la hora de salida.", "Lo que cuenta es la hora de llegada: con tres horas o más de retraso, puedes tener derecho a compensación."],
    num="ERROR 2 DE 5", grande="Mirar la hora *de salida*", pequeno="Cuenta la llegada: con 3 horas o más de retraso en destino, puede haber compensación.", norma="Reglamento (CE) 261/2004"),
  t("consejo", "C1-4", ["Tres: aceptar un vale sin leer la letra pequeña.", "Si lo aceptas como compensación, puedes estar renunciando al dinero."],
    num="ERROR 3 DE 5", grande="Aceptar un *vale* sin leer la letra pequeña", tam=84, pequeno="Si lo aceptas como compensación, puedes estar renunciando al dinero."),
  t("consejo", "C1-5", ["Cuatro: creerte lo de las circunstancias extraordinarias.", "La aerolínea tiene que demostrarlas. Y no siempre puede."],
    num="ERROR 4 DE 5", grande="Creerte lo de las *circunstancias extraordinarias*", tam=80, pequeno="Es la aerolínea la que tiene que demostrarlas. Y no siempre puede."),
  t("consejo", "C1-6", ["Cinco: pagar los gastos de tu bolsillo.", "Comida, hotel o traslados por la incidencia también se reclaman. Guarda los tickets."],
    num="ERROR 5 DE 5", grande="Pagar los gastos *de tu bolsillo*", pequeno="Comida, hotel o traslados por la incidencia también se reclaman. Guarda los tickets."),
  t("consejo", "C1-7", ["Y el peor de todos: no reclamar.", "Que la aerolínea diga que no al principio no significa que no tengas razón."],
    grande="Y el peor: *no reclamar*", pequeno="Un «no» de la aerolínea al principio no significa que no tengas razón."),
 ],
 cierre=dict(CIERRE, legal="Reglamento (CE) 261/2004. Imágenes de archivo. Cada caso se estudia de forma individual."), musica=MUS)

STOCK = {
 "C1": {"1": dict(stock="movil-vuelo-cancelado-tarjeta_8212162.mp4", modo="marco", marco_y=820), "2": dict(stock="tarjeta-embarque-pasaporte-lenta_9692863.mp4", modo="marco"),
        "3": dict(stock="panel-llegadas-arrived-lenta_3055336.mp4", modo="marco"), "4": dict(stock="mostrador-pasajera-documento_2289936.mp4", modo="marco", desde=1),
        "5": dict(stock="ventanilla-lluvia_551110.mp4", modo="marco"), "6": dict(stock="C1-montaje-gastos.mp4", modo="marco"),
        "7": dict(stock="mujer-portatil-casa_7159871.mp4", modo="marco"),
        "portada": dict(portada_stock="movil-vuelo-cancelado-tarjeta_8212162.mp4", portada_desde=3, portada_modo="marco", portada_marco_y=640)},
}

if __name__ == "__main__":
    for k, s in S.items():
        for i, tr in enumerate(s["tramos"], 1):
            tr.update(STOCK.get(k, {}).get(str(i), {}))
        s.update(STOCK.get(k, {}).get("portada", {}))
        json.dump(s, open(f"specs/{k}-v1.json", "w"), ensure_ascii=False, indent=1)
        print(k, len(s["tramos"]), "tramos")
    json.dump({k: [tr["locucion"] for tr in s["tramos"]] for k, s in S.items()}, open("/tmp/locuciones-consejos.json", "w"), ensure_ascii=False, indent=1)
