#!/usr/bin/env python3
"""Cambios pedidos por Sergio el 8/10/2026 (7:30-7:45): nuevos textos de las 12 piezas. Escribe ed3/<id>.json con {textos, url_web?, titular?} y lo hecho."""
import json, os, re
D = "/tmp/claude-0/-home-claude-erreklamatu-rrss/e7eefa61-a30f-57c7-bc2e-7996fd2458cc/scratchpad/ed2/publicaciones"
OUT = os.path.dirname(os.path.abspath(__file__))
def L(p): return json.load(open(f"{D}/{p}.json"))
def xlen(s): return sum(2 if ord(c) > 0x2000 else 1 for c in re.sub(r"https?://\S+", "x" * 23, s))
R = {}
CIE_FB = "Primero analizamos tu caso. La consulta es gratuita. Y si reclamamos por ti, solo cobramos si ganamos.\n\n📞 944 027 596\n✉️ info@erreklamatu.com"
SUS = "\n\n🔔 Suscríbete al canal para ver los próximos vídeos."
EQ = "https://erreklamatu.com/es/vuelos/reclamar-equipaje/"
# frases de la reforma, todas del banco de mensajes (MSG-042, MSG-046, MSG-050) o de la nota y el carrusel ya aprobados
REF_MALETA_FB = ("📌 Lo que cambia: el nuevo reglamento europeo de derechos del pasajero, que se aplicará desde el 23 de octubre de 2027, solo garantiza gratis "
                 "un accesorio personal de hasta 40 × 30 × 15 cm o que quepa bajo el asiento de delante. Las aerolíneas podrán vender tarifas sin maleta de cabina, "
                 "aunque tendrán que mostrar por defecto las que la incluyen. Hasta esa fecha se aplican las reglas actuales.")
REF_MALETA_IG = "📌 Desde el 23 de octubre de 2027, con el nuevo reglamento europeo, solo será siempre gratis un accesorio personal de 40 × 30 × 15 cm: la maleta de cabina dejará de estar garantizada sin coste."
REF_MALETA_CORTA = "Desde el 23/10/2027, el nuevo reglamento europeo solo garantiza gratis un accesorio personal de 40 × 30 × 15 cm."

# PUB-0125: textos literales de Sergio
R["PUB-0125"] = dict(textos=dict(L("PUB-0125")["textos"],
  x="📍 Bilboko abokatu-bulegoa gara: Barroeta Aldamar kalea 4, 6. solairua.\n\n🕘 Astelehenetik ostiralera: 9:00–14:00 eta 16:00–18:00.\n📞 944 027 596\n\nHegaldi- eta banku-erreklamazioetan laguntzen dizugu. Deitu edo idatzi. #Erreklamatu 👇\nhttps://erreklamatu.com/",
  facebook="📍 Bilboko abokatu-bulegoa gara: Barroeta Aldamar kalea 4, 6. solairua.\n\nProfesionalen talde bat duzu zure zerbitzura. Hegaldi- eta banku-erreklamazioetan laguntzen dizugu.\n\nAstelehenetik ostiralera artatzen zaitugu, 9:00etatik 14:00etara eta 16:00etatik 18:00etara. Deitu edo idatzi eta kontatu zure kasua. Telefonoz edo posta elektronikoz egin dezakezu kontsulta, eta agiriak etxetik bidali.\n\nEuskara da gure lan-hizkuntza. Batez ere Euskal Herrian egiten dugu lan, baina Estatu osoko erreklamazioak ere kudeatzen ditugu.\n\nInformazioa eta kontsulta doakoak dira.\n\n📞 944 027 596\n✉️ info@erreklamatu.com\n\nInformazio guztia 👇\nhttps://erreklamatu.com/",
  instagram="📍 Bilboko abokatu-bulegoa gara: Barroeta Aldamar kalea 4, 6. solairua.\n\n🕘 Astelehenetik ostiralera: 9:00–14:00 eta 16:00–18:00.\n\nProfesionalen talde bat duzu zure zerbitzura. Hegaldi- eta banku-erreklamazioetan laguntzen dizugu. Deitu edo idatzi eta kontatu zure kasua. Euskara da gure lan-hizkuntza.\n\nInformazioa eta kontsulta doakoak dira.\n\n📞 944 027 596\n\nEsteka bioan.\n\n#erreklamatu #Bilbo #Bizkaia #abokatuak #erreklamazioak"),
  titular="Gertu gaituzu, dei bakar batera",
  hecho="Imagen rehecha con la misma foto, encuadre y diseño: antetítulo «BILBOKO ABOKATU-BULEGOA», titular «Gertu gaituzu, / dei bakar batera.» y debajo las tres frases que pediste. Textos de X, Facebook e Instagram puestos tal cual los escribiste.")

# PUB-0163: matiz de las hipotecas anteriores a junio de 2019 (MSG-011, web)
t = dict(L("PUB-0163")["textos"])
t["facebook"] = t["facebook"].replace("✅ ¿Hay garantía de éxito? «En esta materia que estamos comentando, concretamente, sí».",
  "✅ ¿Hay garantía de éxito? «En esta materia que estamos comentando, concretamente, sí». Hablamos de hipotecas firmadas antes de junio de 2019 en las que pagaste tú los gastos: notaría, registro, gestoría o tasación.")
t["instagram"] = t["instagram"].replace("✅ ¿Garantía de éxito? «En esta materia, sí».", "✅ ¿Garantía de éxito? «En esta materia, sí»: hipotecas firmadas antes de junio de 2019 en las que pagaste tú los gastos.")
t["x"] = t["x"].replace("✅ ¿Garantía de éxito? «En esta materia, sí».", "✅ ¿Garantía de éxito? «En esta materia, sí» (hipotecas anteriores a junio de 2019 con gastos pagados por ti).")
t["tiktok"] = "Reclamar los gastos de hipoteca: si la firmaste antes de junio de 2019 y pagaste tú los gastos, con acuerdo se resuelve en dos o tres meses. Con una pequeña documentación, nos ocupamos de todo. #gastoshipoteca #hipoteca #banca #erreklamatu"
t["youtube"] = t["youtube"].replace("si hay garantías de éxito, cuánto tardan y qué tiene que hacer el cliente.",
  "si hay garantías de éxito, cuánto tardan y qué tiene que hacer el cliente. Se refiere a hipotecas firmadas antes de junio de 2019 en las que el cliente pagó los gastos (notaría, registro, gestoría o tasación).")
R["PUB-0163"] = dict(textos=t, hecho="Añadido en los cinco textos que la garantía se refiere a hipotecas firmadas antes de junio de 2019 en las que el cliente pagó los gastos (notaría, registro, gestoría o tasación). Sale de la web (MSG-011). No toca el vídeo.")

# PUB-0165: texto nuevo con la reforma (lo pediste: «escribe tú el nuevo texto teniendo en cuenta el nuevo reglamento»)
t = dict(L("PUB-0165")["textos"])
t["facebook"] = ("🎒 ¿Pueden cobrarte un extra por llevar contigo la maleta de cabina?\n\n«La normativa dice que el equipaje es un elemento inherente al pasajero y que no se puede cobrar un extra por llevarlo con nosotros», "
  "explicaba Jon Ortiz, abogado de ERREKLAMATU, en EITB (vídeo de archivo, de 2017).\n\n" + REF_MALETA_FB +
  "\n\n¿Te han cobrado por el equipaje de mano? Cuéntanos tu caso.\n\n" + CIE_FB + "\n\nToda la información 👇\n" + EQ)
t["instagram"] = ("🎒 ¿Pueden cobrarte por la maleta de cabina?\n\n«El equipaje es un elemento inherente al pasajero y no se puede cobrar un extra por llevarlo con nosotros».\n\n"
  "Jon Ortiz, abogado de ERREKLAMATU, en EITB (vídeo de archivo, de 2017).\n\n" + REF_MALETA_IG +
  "\n\nConsulta gratuita. Solo cobramos si ganamos.\n\n📞 944 027 596\n\nEnlace en la bio.\n\n#equipajedemano #maletadecabina #derechosdelpasajero #vuelos #erreklamatu")
t["x"] = ("🎒 «El equipaje es un elemento inherente al pasajero», decía Jon Ortiz, de #Erreklamatu, en EITB (2017).\n\n" + REF_MALETA_CORTA + " 👇\n" + EQ)
t["tiktok"] = "¿Pueden cobrarte por la maleta de cabina? «El equipaje es un elemento inherente al pasajero», decía Jon Ortiz en 2017. Desde el 23/10/2027, el nuevo reglamento europeo solo garantiza gratis un accesorio personal. #equipajedemano #maletadecabina #vuelos #erreklamatu"
t["youtube"] = ("¿Pueden cobrarte por la maleta de cabina?\n\nJon Ortiz, abogado de ERREKLAMATU, en EITB (vídeo de archivo, de 2017), sobre el cobro de suplementos por el equipaje de mano.\n\n"
  "Lo que cambia: el nuevo reglamento europeo de derechos del pasajero, que se aplicará desde el 23 de octubre de 2027, solo garantiza gratis un accesorio personal de hasta 40 × 30 × 15 cm; las aerolíneas podrán vender tarifas sin maleta de cabina. Hasta esa fecha se aplican las reglas actuales.\n\n"
  "Consulta gratuita, y solo cobramos si ganamos." + SUS + "\n\n📞 944 027 596\n" + EQ)
R["PUB-0165"] = dict(textos=t, hecho="Textos reescritos: lo que dijo Jon en 2017, atribuido y fechado, y lo que cambia con el nuevo reglamento desde el 23/10/2027 (solo el accesorio personal de 40 × 30 × 15 cm garantizado gratis; tarifas sin maleta de cabina, mostrando por defecto las que la incluyen; hasta esa fecha, las reglas actuales). Todo sale de MSG-042 y MSG-046 y del carrusel PUB-0217 ya aprobado. Se mantiene «(2017)» en los textos: el vídeo dice algo que el reglamento cambiará y la fecha lo explica. El vídeo no cambia (el crédito ya no lleva el año). QUE LO VEA UN ABOGADO antes de aprobar.")

# PUB-0176: en positivo
t = dict(L("PUB-0176")["textos"])
for k in t:
    t[k] = t[k].replace("Lo de comercial se le da regular. Lo suyo es reclamar a las aerolíneas.", "Como comercial no se le da nada mal. Pero donde de verdad es un crack es reclamando a las aerolíneas.")
    t[k] = t[k].replace("Lo de comercial se le da regular: lo suyo es reclamar a las aerolíneas.", "Como comercial no se le da nada mal, pero donde de verdad es un crack es reclamando a las aerolíneas.")
R["PUB-0176"] = dict(textos=t, hecho="Cambiado en Facebook, Instagram, X y TikTok «Lo de comercial se le da regular. Lo suyo es reclamar a las aerolíneas» por «Como comercial no se le da nada mal. Pero donde de verdad es un crack es reclamando a las aerolíneas». El vídeo no lleva esa frase.")

# PUB-0203 y PUB-0205: previsión del reglamento (no piden quitar el año)
for pid in ("PUB-0203", "PUB-0205"):
    t = dict(L(pid)["textos"])
    t["facebook"] = t["facebook"].replace("\n\nPrimero analizamos tu caso.", "\n\n" + REF_MALETA_FB + "\n\nPrimero analizamos tu caso.")
    t["instagram"] = t["instagram"].replace("\n\nConsulta gratuita.", "\n\n" + REF_MALETA_IG + "\n\nConsulta gratuita.")
    t["youtube"] = t["youtube"].replace("\n\nConsulta gratuita, y solo cobramos si ganamos.",
        "\n\nLo que cambia: el nuevo reglamento europeo de derechos del pasajero, que se aplicará desde el 23 de octubre de 2027, solo garantiza gratis un accesorio personal de hasta 40 × 30 × 15 cm; las aerolíneas podrán vender tarifas sin maleta de cabina. Hasta esa fecha se aplican las reglas actuales.\n\nConsulta gratuita, y solo cobramos si ganamos.")
    t["tiktok"] = t["tiktok"].replace(" #equipajedemano", " Desde el 23/10/2027, el nuevo reglamento europeo solo garantiza gratis un accesorio personal. #equipajedemano")
    R[pid] = dict(textos=t)
t = R["PUB-0203"]["textos"]
t["x"] = "🎒 Te cobran por el equipaje de mano. ¿Reclamas?\n\n«Hay que reclamar y se puede ganar», decía Óscar Sánchez, de #Erreklamatu (vídeo de 2019).\n\n" + REF_MALETA_CORTA
t = R["PUB-0205"]["textos"]
t["x"] = "🎒 ¿Derecho a llevar equipaje de mano sin facturarlo? «Sí», decía Óscar Sánchez, de #Erreklamatu (vídeo de 2019).\n\n" + REF_MALETA_CORTA
for pid in ("PUB-0203", "PUB-0205"):
    R[pid]["hecho"] = ("Añadida la previsión del nuevo reglamento en los cinco textos: desde el 23/10/2027 solo el accesorio personal de 40 × 30 × 15 cm queda garantizado gratis; "
                       "podrá haber tarifas sin maleta de cabina, mostrando por defecto las que la incluyen; hasta esa fecha, las reglas actuales (MSG-042 y MSG-046). "
                       "En X, para que quepa, la cita se acorta. No se pidió quitar el año y se mantiene. El vídeo no cambia. QUE LO VEA UN ABOGADO antes de aprobar.")

# PUB-0206: sin año + previsión del reglamento (ya estaba en Facebook)
t = dict(L("PUB-0206")["textos"])
for k in t:
    t[k] = t[k].replace(" (vídeo de archivo, de 2019)", "").replace(" (vídeo de 2019)", "").replace(" (Vídeo de 2019).", "")
TE = "Desde el 23 de octubre de 2027, el nuevo reglamento europeo lo deja por escrito: no podrán cobrarte por la tarjeta impresa si ya has facturado."
t["facebook"] = t["facebook"].replace("La reforma europea de los derechos del pasajero lo deja por escrito a partir del 23 de octubre de 2027: no podrán cobrarte por la tarjeta impresa si ya has facturado.",
  "📌 Y lo que viene: el nuevo reglamento europeo de derechos del pasajero, que se aplicará desde el 23 de octubre de 2027, lo deja por escrito: no podrán cobrarte por la tarjeta impresa si ya has facturado.")
t["instagram"] = t["instagram"].replace("\n\nConsulta gratuita.", "\n\n📌 " + TE + "\n\nConsulta gratuita.")
t["x"] = t["x"] + "\n\n" + "Desde el 23/10/2027, el nuevo reglamento europeo lo deja por escrito si ya has facturado."
t["tiktok"] = t["tiktok"].replace(" #tarjetadeembarque", " " + TE + " #tarjetadeembarque")
t["youtube"] = t["youtube"].replace("\n\nConsulta gratuita, y solo cobramos si ganamos.", "\n\n" + TE + "\n\nConsulta gratuita, y solo cobramos si ganamos.")
R["PUB-0206"] = dict(textos=t, hecho="Quitado el año de los textos y del crédito del vídeo (vídeo rehecho). Previsión del reglamento en los cinco textos: desde el 23/10/2027 no podrán cobrar por la tarjeta impresa si ya has facturado (art. 11 ter nuevo, leído el 6/10; hoy no he podido volver a abrir el texto completo). QUE LO VEA UN ABOGADO.")

# PUB-0207: sin año y enlace a la página general de reclamar vuelo
RV = "https://erreklamatu.com/es/reclamar-vuelo/"
t = dict(L("PUB-0207")["textos"])
for k in t:
    t[k] = t[k].replace(" (vídeo de archivo, de 2019)", "").replace(" (vídeo de 2019)", "").replace("https://erreklamatu.com/es/vuelos/reclamar-vuelo-retrasado/", RV)
R["PUB-0207"] = dict(textos=t, url_web=RV, hecho="Quitado el año de los textos y del crédito del vídeo (vídeo rehecho). Enlace cambiado a la página general https://erreklamatu.com/es/reclamar-vuelo/ (la del menú «Reclamar vuelo»; /es/vuelos/reclamar-vuelo/ da error 404).")

# PUB-0208: sin año
t = dict(L("PUB-0208")["textos"])
for k in t:
    t[k] = t[k].replace(" (vídeo de archivo, de 2019)", "").replace(" (vídeo de 2019)", "")
R["PUB-0208"] = dict(textos=t, hecho="Quitado el año de los textos y del crédito del vídeo (vídeo rehecho). Se mantiene «vídeo de archivo» en Facebook, Instagram y YouTube.")

# PUB-0209: sin año + reforma en todas las redes (ya estaba en Facebook)
t = dict(L("PUB-0209")["textos"])
for k in t:
    t[k] = t[k].replace(" (vídeo de archivo, de 2019)", "").replace(" (vídeo de 2019)", "")
NI = "Desde el 23 de octubre de 2027, con el nuevo reglamento europeo, no podrán cobrarte por sentarte junto a un niño menor de 14 años que viaje contigo."
t["facebook"] = t["facebook"].replace("La reforma europea lo cambia para quien viaja con niños: desde el 23 de octubre de 2027, la aerolínea tendrá que ofrecer gratis un asiento contiguo a quien acompañe a un menor de 14 años.",
  "📌 Y lo que viene: el nuevo reglamento europeo de derechos del pasajero lo cambia para quien viaja con niños. Desde el 23 de octubre de 2027, la aerolínea no podrá cobrarte por sentarte junto a un niño menor de 14 años que viaje contigo.")
t["instagram"] = t["instagram"].replace("\n\nConsulta gratuita.", "\n\n📌 " + NI + "\n\nConsulta gratuita.")
t["x"] = "💺 Viajas con tus hijos y, si no pagas, os separan. Hoy, cobrar por elegir asiento es legal; separar casi de forma automática a quienes compran juntos «roza la abusividad», decía Óscar Sánchez, de #Erreklamatu.\n\nDesde el 23/10/2027 no podrán cobrar por sentarte junto a un menor de 14 años."
t["tiktok"] = t["tiktok"].replace(" #asientos", " " + NI + " #asientos")
t["youtube"] = t["youtube"].replace("\n\nConsulta gratuita, y solo cobramos si ganamos.", "\n\n" + NI + "\n\nConsulta gratuita, y solo cobramos si ganamos.")
R["PUB-0209"] = dict(textos=t, hecho="Quitado el año de los textos y del crédito del vídeo (vídeo rehecho). Previsión del reglamento en los cinco textos: desde el 23/10/2027 no podrán cobrar por sentarte junto a un niño menor de 14 años que viaje contigo (MSG-050). En Facebook se cambió «tendrá que ofrecer gratis un asiento contiguo» por esa frase, que es la del banco de mensajes: si no hay asientos contiguos, el reglamento solo dice que la aerolínea «procurará ayudar».")

# PUB-0213: el caso del exceso de peso
t = dict(L("PUB-0213")["textos"])
t["facebook"] = t["facebook"].replace("🛑 Ya has embarcado y la aerolínea te baja del avión. ¿A qué tienes derecho?\n\nJon Ortiz, abogado de ERREKLAMATU, en Radio Popular (septiembre de 2023), lo resumía en tres conceptos:",
  "🛑 Ya has embarcado y la aerolínea te baja del avión porque va con exceso de peso. ¿A qué tienes derecho?\n\nJon Ortiz, abogado de ERREKLAMATU, lo explicaba en Radio Popular (septiembre de 2023), a raíz de un vuelo del que bajaron a varios pasajeros por exceso de peso. Lo resumía en tres conceptos:")
t["instagram"] = t["instagram"].replace("🛑 Te bajan del avión. ¿Qué puedes reclamar?", "🛑 Te bajan del avión por exceso de peso. ¿Qué puedes reclamar?")
t["x"] = t["x"].replace("🛑 La aerolínea te baja del avión. ¿Qué reclamas?", "🛑 Te bajan del avión por exceso de peso. ¿Qué reclamas?")
t["tiktok"] = t["tiktok"].replace("Te bajan del avión:", "Te bajan del avión por exceso de peso:")
t["youtube"] = t["youtube"].replace("explica qué puede reclamar un pasajero al que deniegan el embarque: asistencia, indemnización y gastos.",
  "explica qué puede reclamar un pasajero al que bajan del avión, a raíz de un vuelo del que bajaron a varios pasajeros por exceso de peso: asistencia, indemnización y gastos.")
R["PUB-0213"] = dict(textos=t, hecho="Dicho en los cinco textos que a los pasajeros los bajaron del avión por exceso de peso. Las notas de la pieza decían «exceso de carga» (de la página de la emisora); uso «exceso de peso», como lo dices tú. No se nombra a la aerolínea. El vídeo no cambia.")

# PUB-0215: sin año + reforma
t = dict(L("PUB-0215")["textos"])
for k in t:
    t[k] = t[k].replace(" (agosto de 2023)", "").replace(" (2023)", "")
t["facebook"] = t["facebook"].replace("\n\nPrimero analizamos tu caso.", "\n\n" + REF_MALETA_FB + "\n\nPrimero analizamos tu caso.")
t["instagram"] = t["instagram"].replace("\n\nConsulta gratuita.", "\n\n" + REF_MALETA_IG + "\n\nConsulta gratuita.")
t["x"] = "🎒 ¿Te pueden cobrar el equipaje de mano?\n\nLa Ley de Navegación Aérea dice que es parte del precio del billete, pero no dice cuántos kilos, explicaba Óscar Sánchez, de #Erreklamatu.\n\n" + REF_MALETA_CORTA
t["tiktok"] = t["tiktok"].replace(" #equipajedemano", " Desde el 23/10/2027, el nuevo reglamento europeo solo garantiza gratis un accesorio personal. #equipajedemano")
t["youtube"] = t["youtube"].replace("\n\nConsulta gratuita, y solo cobramos si ganamos.",
  "\n\nLo que cambia: el nuevo reglamento europeo de derechos del pasajero, que se aplicará desde el 23 de octubre de 2027, solo garantiza gratis un accesorio personal de hasta 40 × 30 × 15 cm; las aerolíneas podrán vender tarifas sin maleta de cabina. Hasta esa fecha se aplican las reglas actuales.\n\nConsulta gratuita, y solo cobramos si ganamos.")
R["PUB-0215"] = dict(textos=t, hecho="Quitado el año de los textos, del crédito y del cartel de la radio (vídeo rehecho). Previsión del reglamento en los cinco textos (MSG-042 y MSG-046). Cómo encaja la Ley de Navegación Aérea con el reglamento no lo sé: QUE LO VEA UN ABOGADO.")

for pid, r in R.items():
    for k, v in r["textos"].items():
        if k == "x" and v and xlen(v) > 280: print("X LARGO", pid, xlen(v))
        if k == "instagram" and v and len(re.findall(r"#\w", v)) > 5: print("TAGS", pid)
        if k == "tiktok" and v and len(v) > 300: print("TK LARGO", pid, len(v))
        if "2019" in v and pid in ("PUB-0206", "PUB-0207", "PUB-0208", "PUB-0209"): print("AÑO", pid, k)
        if "2023" in v and pid == "PUB-0215": print("AÑO", pid, k)
    json.dump(r, open(f"{OUT}/{pid}.json", "w"), ensure_ascii=False, indent=1)
print(len(R))
