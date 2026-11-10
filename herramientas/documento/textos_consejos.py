#!/usr/bin/env python3
"""Textos de redes de los vídeos de consejos C2–C9 y de las versiones cortas C1c–C9c, a partir de las specs (los puntos ya revisados).
Uso: python3 textos_consejos.py -> specs/textos-consejos-20261103.json (añade a lo que haya)."""
import json, re
F = "specs/textos-consejos-20261103.json"
T = json.load(open(F))
EMO = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
META = {  # url, hashtags, frase de cierre útil, base legal
 "C1": ("reclamar-vuelo-retrasado/", "#vueloretrasado #vuelocancelado #derechosdelpasajero #consejosdeviaje #erreklamatu", "Guárdalo para tu próximo viaje 📌", None),
 "C2": ("reclamar-vuelo-cancelado/", "#vuelocancelado #derechosdelpasajero #consejosdeviaje #erreklamatu", "Guárdalo por si te cancelan un vuelo 📌",
        "Reglamento (CE) 261/2004: arts. 5 (aviso con menos de 14 días), 7 (250, 400 o 600 € según la distancia), 8 (reembolso o transporte alternativo hasta el destino final) y 9 (asistencia). Plazo de 5 años en el Estado español."),
 "C3": ("reclamar-vuelo-retrasado/", "#vueloretrasado #derechosdelpasajero #consejosdeviaje #erreklamatu", "Guárdalo para tu próximo viaje 📌",
        "Reglamento (CE) 261/2004: arts. 3.1 (vuelos que salen de la UE, sea cual sea la aerolínea), 6 (asistencia desde 2, 3 o 4 horas según la distancia; reembolso con 5 horas o más), 7 y 9. STJUE Sturgeon (C-402/07 y C-432/07): compensación con 3 horas o más de retraso en la llegada; STJUE Germanwings (C-452/13): la llegada es cuando se abre al menos una puerta."),
 "C4": ("reclamar-equipaje/", "#equipajeperdido #maletaperdida #derechosdelpasajero #consejosdeviaje #erreklamatu", "Guárdalo para tu próximo viaje 📌",
        "Convenio de Montreal: art. 17.3 (el equipaje se da por perdido a los 21 días), art. 19 (retraso) y art. 31 (reclamación por escrito: 7 días si está dañado, 21 días si llega con retraso). La aerolínea responde aunque el servicio de equipajes lo haga otra empresa. Plazo para demandar: 2 años (art. 35)."),
 "C5": ("reclamar-vuelo-retrasado/", "#viajarconniños #viajarconbebes #consejosdeviaje #derechosdelpasajero #erreklamatu", "Guárdalo si vas a viajar con niños 📌",
        "Nota de prensa de Erreklamatu «10 cosas que debes saber si vas a volar con niños». Líquidos del bebé: excepción a las restricciones de líquidos en el control de seguridad. Alojamiento y traslado: Reglamento (CE) 261/2004, art. 9."),
 "C6": ("reclamar-vuelo-cancelado/", "#derechosdelpasajero #overbooking #vuelocancelado #consejosdeviaje #erreklamatu", "Guárdalo para tu próximo viaje 📌",
        "Reglamento (CE) 261/2004: art. 4 (denegación de embarque), art. 7 (la compensación va por distancia, no por precio), art. 8 (transporte alternativo) y art. 9.2 (dos llamadas o correos). Plazo de 5 años en el Estado español (art. 1964 del Código Civil, según el Tribunal Supremo)."),
 "C7": ("reclamar-vuelo-cancelado/", "#reclamarvuelo #derechosdelpasajero #consejosdeviaje #erreklamatu", "Guárdalo por si tienes que reclamar 📌",
        "Reglamento (CE) 261/2004: art. 8.1.a (reembolso en 7 días) y art. 15 (las obligaciones con el pasajero no pueden limitarse ni excluirse)."),
 "C8": ("reclamar-vuelo-retrasado/", "#consejosdeviaje #viajar #derechosdelpasajero #erreklamatu", "Guárdalo para tu próximo viaje 📌",
        "Artículo de Erreklamatu «20 consejos para evitar problemas con tu vuelo». Consejos de prevención; no hay norma que citar salvo la de cada país sobre la validez del pasaporte."),
 "C9": ("reclamar-vuelo-cancelado/", "#vuelocancelado #derechosdelpasajero #aerolineas #consejosdeviaje #erreklamatu", "Guárdalo por si te pasa 📌",
        "Reglamento (CE) 261/2004: art. 5.1.c (sin compensación si avisan con 2 semanas o más), art. 7.3 (reembolso en bonos solo con acuerdo firmado del pasajero), art. 8 (reembolso), art. 14 (información por escrito) y art. 15. Comprar en agencia no cambia los derechos frente a la aerolínea."),
}
def limpio(x): return x.replace("*", "")
def may(x): return ("«" + may(x[1:])) if x.startswith("«") else x[0].upper() + x[1:]
def textos(k, s, base):
    m = META[base]; pts = [tr for tr in s["tramos"] if tr["tipo"] == "consejo"]
    tit = limpio(s["titulo"][0]); gan = " ".join(s["tramos"][0]["subtitulos"])
    def expl(tr):  # la explicación de la voz, sin el «Uno:» del principio
        x = " ".join(tr["subtitulos"]); return re.sub(r"^(Uno|Una|Dos|Tres|Cuatro|Cinco|Y el peor de todos):\s*", "", x)
    lista = "\n".join(f"{EMO[i]} {may(expl(tr))}" for i, tr in enumerate(pts))
    corta = "\n".join(f"{EMO[i]} {limpio(tr['grande'])}" for i, tr in enumerate(pts))
    x = "\n".join(f"{i+1}. {limpio(tr['grande'])}" for i, tr in enumerate(pts))
    cta = "Solo cobramos si ganamos.\n📞 944 027 596\n✉️ info@erreklamatu.com"
    return {
     "facebook": f"✈️ {gan}\n\n{lista}\n\n{m[2]}\n\n{cta}",
     "instagram": f"✈️ {tit}\n\n{corta}\n\n{m[2]}\n\nSolo cobramos si ganamos.\n📞 944 027 596\n\nComenta VUELO y te decimos si puedes reclamar.\n\n{m[1]}",
     "tiktok": f"{tit}. {m[2].replace(' 📌', '.')} Consulta gratuita: 944 027 596 · info@erreklamatu.com {' '.join(m[1].split()[:3])} #erreklamatu",
     "x": f"✈️ {tit}:\n\n{x}\n\n📞 944 027 596 · ✉️ info@erreklamatu.com",
     "youtube": f"{tit}\n\n{gan}\n\n{lista}\n\n{cta}\n🌐 erreklamatu.com"}
if __name__ == "__main__":
    import gen_consejos as g
    for k, s in g.S.items():
        if k == "C1": continue
        base = k.rstrip("c"); m = META[base]
        tx = textos(k, s, base)
        if len(tx["x"]) > 280: tx["x"] = tx["x"].replace(" · ✉️ info@erreklamatu.com", "")
        T[k] = {"tema": f"Consejos (vídeo atemporal{', versión corta de prueba' if k.endswith('c') else ''}): {limpio(s['titulo'][0])}",
                "titular": limpio(s["titulo"][0]) + " " + limpio(s["titulo"][1]),
                "url_web": "https://erreklamatu.com/es/vuelos/" + m[0], "base_legal": m[3] or T["C1"]["base_legal"], "textos": tx}
        print(k, len(tx["x"]))
    json.dump(T, open(F, "w"), ensure_ascii=False, indent=1)
