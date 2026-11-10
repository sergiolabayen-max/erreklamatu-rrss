#!/usr/bin/env python3
"""PUB-0543 / PUB-0552 (C7, C7c), corrección de Sergio del 4/11/2026 (10:10): cada truco debe decir a qué incidencia se refiere
(reembolso → cancelación; compensación → cancelación o retraso; «consúltalo» → con un abogado; talón → maleta perdida o dañada).
Parte de specs/C7-v2.json y C7c-v2.json y escribe -v3. Voces en recursos/voces/consejos-v4."""
import json
V = "../../../recursos/voces/consejos-v4/"
def voz(t, n, loc, subs, grande=None):
    t.update(voz=V + n + ".mp3", locucion=loc, subtitulos=subs)
    if grande: t["grande"] = grande
s = json.load(open("specs/C7-v2.json")); T = s["tramos"]
voz(T[1], "C7-2", "Uno: si te cancelan el vuelo y pides el reembolso, la aerolínea tiene siete días para devolverte el dinero. En dinero, no en bonos, salvo que tú lo aceptes por escrito.",
    ["Uno: si te cancelan el vuelo y pides el reembolso,", "la aerolínea tiene siete días para devolverte el dinero.", "En dinero, no en bonos, salvo que tú lo aceptes por escrito."], "Vuelo cancelado: *reembolso en 7 días*")
voz(T[2], "C7-3", "Dos: si te cancelan o te retrasan el vuelo, no firmes nada en lo que renuncies a la compensación. Y si ya has firmado algo, consúltalo con un abogado: esas renuncias no siempre valen.",
    ["Dos: si te cancelan o te retrasan el vuelo,", "no firmes nada en lo que renuncies a la compensación.", "Y si ya has firmado algo, consúltalo con un abogado:", "esas renuncias no siempre valen."], "No firmes *renuncias a la compensación*")
voz(T[3], "C7-4", "Tres: si la incidencia afecta a todo el vuelo, habla con el resto de pasajeros. Apunta sus nombres y teléfonos: cuantos más reclaméis, más fuerza.",
    ["Tres: si la incidencia afecta a todo el vuelo,", "habla con el resto de pasajeros.", "Apunta sus nombres y teléfonos: cuantos más reclaméis, más fuerza."], "¿Afecta a todo el vuelo? *Habla con los demás*")
voz(T[4], "C7-5", "Cuatro: guarda el talón de la maleta facturada. Si se pierde o llega dañada, es tu prueba para reclamar. Y si te lo piden, hazle antes una foto.",
    ["Cuatro: guarda el talón de la maleta facturada.", "Si se pierde o llega dañada, es tu prueba para reclamar.", "Y si te lo piden, hazle antes una foto."], "Maleta perdida o dañada: *guarda el talón*")
s["id"] = s["id"].replace("-v2", "-v3"); json.dump(s, open("specs/C7-v3.json", "w"), ensure_ascii=False, indent=1)
s = json.load(open("specs/C7c-v2.json")); T = s["tramos"]
voz(T[1], "C7c-2", "Uno: si te cancelan el vuelo y pides el reembolso, tienen siete días para devolvértelo.", ["Uno: si te cancelan el vuelo y pides el reembolso,", "tienen siete días para devolvértelo."], "Vuelo cancelado: *reembolso en 7 días*")
voz(T[2], "C7c-3", "Dos: si te cancelan o te retrasan el vuelo, no firmes renuncias a la compensación.", ["Dos: si te cancelan o te retrasan el vuelo,", "no firmes renuncias a la compensación."], "No firmes *renuncias a la compensación*")
voz(T[3], "C7c-4", "Tres: si afecta a todo el vuelo, habla con los demás pasajeros. Juntos, más fuerza.", ["Tres: si afecta a todo el vuelo, habla con los demás pasajeros.", "Juntos, más fuerza."], "¿Afecta a todo el vuelo? *Habla con los demás*")
s["id"] = s["id"].replace("-v2", "-v3"); json.dump(s, open("specs/C7c-v3.json", "w"), ensure_ascii=False, indent=1)
print("ok")
