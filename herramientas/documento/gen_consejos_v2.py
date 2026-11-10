#!/usr/bin/env python3
"""Correcciones de Sergio del 4/11/2026 a los vídeos de consejos (PUB-0537 a PUB-0554).
Parte de specs/Cn-v1.json y escribe specs/Cn-v2.json. Voces nuevas en recursos/voces/consejos-v3 (Magnific · ElevenLabs v3 · «Ana Beltrán»)."""
import json, copy
V3 = "../../../recursos/voces/consejos-v3/"
def cargar(k): return json.load(open(f"specs/{k}-v1.json"))
def voz(t, n, loc, subs): t.update(voz=V3 + n + ".mp3", locucion=loc, subtitulos=subs)
S = {}
# C1 / C1c · error 2: «Mirar la hora de salida» era impreciso (Sergio: «¿cuál es el error? ¿mirarse el reloj?»)
for k in ("C1", "C1c"):
    s = cargar(k); t = s["tramos"][2]; t["grande"] = "Contar el retraso *desde la salida*"
    if k == "C1": voz(t, "C1-3", "Dos: contar el retraso desde la hora de salida. Lo que cuenta es a qué hora llegas: con tres horas o más de retraso en destino, puedes tener derecho a compensación.",
                      ["Dos: contar el retraso desde la hora de salida.", "Lo que cuenta es a qué hora llegas:", "con tres horas o más de retraso en destino, puedes tener derecho a compensación."])
    else: voz(t, "C1c-3", "Dos: contar el retraso desde la salida. Lo que cuenta es a qué hora llegas.", ["Dos: contar el retraso desde la salida.", "Lo que cuenta es a qué hora llegas."])
    S[k] = s
# C2 / C2c · «tus derechos», no «lo que la aerolínea te debe»; rótulo del derecho 4
s = cargar("C2"); s["titulo"] = ["Te cancelan el vuelo: tus 5 derechos", "*conócelos* antes de aceptar nada"]
voz(s["tramos"][0], "C2-1", "¿Te han cancelado el vuelo? Estos son tus derechos, aunque la aerolínea no te los cuente.", ["¿Te han cancelado el vuelo?", "Estos son tus derechos, aunque la aerolínea no te los cuente."])
s["tramos"][4]["grande"] = "Si te avisan con menos de 14 días: *también compensación*"; S["C2"] = s
s = cargar("C2c"); s["titulo"] = ["Te cancelan el vuelo: tus 3 derechos", "*conócelos* antes de aceptar nada"]
voz(s["tramos"][0], "C2c-1", "¿Te cancelan el vuelo? Estos son tus tres derechos principales.", ["¿Te cancelan el vuelo?", "Estos son tus tres derechos principales."]); S["C2c"] = s
# C4 / C4c · plazos: sin «los plazos son cortos»; rótulo sin cifras sueltas
s = cargar("C4"); t = s["tramos"][4]; t["grande"] = "Reclama *por escrito y a tiempo*"
voz(t, "C4-5", "Cuatro: reclama siempre por escrito, y a tiempo. Tienes siete días si la maleta llega dañada, y veintiuno si llega con retraso. Guarda una copia.",
    ["Cuatro: reclama siempre por escrito, y a tiempo.", "Tienes siete días si la maleta llega dañada,", "y veintiuno si llega con retraso. Guarda una copia."]); S["C4"] = s
s = cargar("C4c"); t = s["tramos"][3]; t["grande"] = "Reclama *por escrito y a tiempo*"
voz(t, "C4c-4", "Tres: reclama por escrito, y a tiempo. Siete días si llega dañada, veintiuno si llega con retraso.",
    ["Tres: reclama por escrito, y a tiempo.", "Siete días si llega dañada, veintiuno si llega con retraso."]); S["C4c"] = s
# C5c · «revisa lo asientos» (la voz se comía la s): nueva toma con el orden cambiado
s = cargar("C5c"); voz(s["tramos"][2], "C5c-3", "Dos: al hacer el check-in, revisa los asientos, para ir juntos.", ["Dos: al hacer el check-in, revisa los asientos, para ir juntos."]); S["C5c"] = s
# C6 / C6c · «que deberías conocer»; punto 1 (la compensación no es solo por overbooking); «5 años» sin cifra pegada; imágenes
for k in ("C6", "C6c"):
    s = cargar(k); n = "5" if k == "C6" else "3"
    s["titulo"] = [f"{n} derechos del pasajero que deberías conocer", "y que *te pueden valer dinero*"]
    T = s["tramos"]
    if k == "C6":
        voz(T[0], "C6-1", "Cinco derechos como pasajero de avión que deberías conocer. Y que te pueden valer dinero.", ["Cinco derechos como pasajero de avión que deberías conocer.", "Y que te pueden valer dinero."])
        voz(T[1], "C6-2", "Uno: la compensación de doscientos cincuenta a seiscientos euros no es solo por cancelación. También si llegas con tres horas o más de retraso, o si te dejan en tierra por overbooking.",
            ["Uno: la compensación de 250 a 600 euros", "no es solo por cancelación.", "También si llegas con tres horas o más de retraso,", "o si te dejan en tierra por overbooking."])
        T[3].update(stock="mujer-portatil-maleta_4390333.mp4"); T[3].pop("desde", None)
        T[5].update(stock="mujer-revisando-papeles-casa_1416434.mp4", grande="Tienes *cinco años* para reclamar"); T[5].pop("desde", None)
    else:
        voz(T[0], "C6c-1", "Tres derechos del pasajero que deberías conocer, y que te pueden valer dinero.", ["Tres derechos del pasajero que deberías conocer,", "y que te pueden valer dinero."])
        voz(T[1], "C6c-2", "Uno: no solo una cancelación da derecho a compensación. También un retraso de tres horas o más, o el overbooking.",
            ["Uno: no solo una cancelación da derecho a compensación.", "También un retraso de tres horas o más, o el overbooking."])
        T[3].update(stock="mujer-revisando-papeles-casa_1416434.mp4", grande="Tienes *cinco años* para reclamar"); T[3].pop("desde", None)
    T[0].update(stock="pasajeros-preocupados-panel_7578374.mp4", desde=7)
    T[1].update(stock="hombre-panel-vuelos-movil_10225897.mp4", grande="Compensación también por *retraso u overbooking*"); T[1].pop("desde", None)
    T[1]["num"] = T[1]["num"]
    s["portada_stock"] = "pasajeros-preocupados-panel_7578374.mp4"; s["portada_desde"] = 14; s["portada_modo"] = "marco"
    S[k] = s
# C7 / C7c · menos primeros planos de manos, sin toma repetida, personas de aspecto local
for k in ("C7", "C7c"):
    s = cargar(k); T = s["tramos"]
    T[0].update(stock="mujer-aeropuerto-movil-panel_4390693.mp4"); T[0].pop("desde", None)
    T[1].update(stock="mujer-sonriendo-movil-tarjeta_2402223.mp4"); T[1].pop("desde", None)
    T[2].update(stock="mano-papel-mesa-madera_5761375.mp4", desde=20)
    T[3].update(stock="pareja-charlando-terminal_8869300.mp4"); T[3].pop("desde", None)
    s["portada_stock"] = "mujer-aeropuerto-movil-panel_4390693.mp4"; s["portada_desde"] = 4; s["portada_modo"] = "marco"
    S[k] = s
# C9 / C9c · la práctica «por escrito» repetía la imagen de la anterior
s = cargar("C9"); s["tramos"][4].update(stock="empleada-mostrador-pasajero_1833528.mp4", desde=3); S["C9"] = s
s = cargar("C9c"); s["tramos"][3].update(stock="empleada-mostrador-pasajero_1833528.mp4", desde=3); S["C9c"] = s
if __name__ == "__main__":
    for k, s in S.items():
        s["id"] = s["id"] + "-v2"; json.dump(s, open(f"specs/{k}-v2.json", "w"), ensure_ascii=False, indent=1); print(k, "->", f"specs/{k}-v2.json")
