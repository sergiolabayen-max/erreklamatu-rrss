#!/usr/bin/env python3
"""Genera una nota de prensa de ERREKLAMATU con el formato exacto de la plantilla de Sergio (12/10/2026).
Uso: python3 nota_desde_plantilla.py plantilla.docx nota.json salida.docx
Plantillas: Erreklamatu-reforma-derechos-pasajeros-reglamento-UE.docx (castellano, lang es-ES)
            Erreklamatu-bidaiarien-eskubideak-EB-erregelamendua.docx (euskera, lang eu-ES)
nota.json: {"lang":"es-ES", "cabecera":"NOTA DE PRENSA", "fecha":"Bilbao, 13 de octubre de 2026", "titular":"...", "entradilla":"...",
            "bloques":[{"h":"Subtítulo"} | {"p":"Párrafo"} | {"b":"Arranque en negrita.", "p":" resto del párrafo"}]}
Se conservan de la plantilla el logo, el estilo de cada tipo de párrafo, el cierre «ERREKLAMATU es un despacho…», la raya y los contactos.
Las comillas de las citas van como en la plantilla: “…”."""
import json, re, sys, zipfile, html
pl, nj, out = sys.argv[1:4]
N = json.load(open(nj, encoding="utf-8")); L = N.get("lang", "es-ES")
z = zipfile.ZipFile(pl); x = z.read("word/document.xml").decode("utf8")
ps = re.findall(r'<w:p[ >].*?</w:p>', x, re.S)
e = lambda s: html.escape(s, quote=False)
SP = '<w:spacing w:lineRule="auto" w:line="264" w:before="0" w:after="140"/>'
def par(runs, prpr=f'<w:lang w:val="{L}"/>'):
    return f'<w:p><w:pPr><w:pStyle w:val="Normal"/>{SP}<w:rPr>{prpr}</w:rPr></w:pPr>' + "".join(
        f'<w:r><w:rPr>{rp}</w:rPr><w:t xml:space="preserve">{e(t)}</w:t></w:r>' for rp, t in runs) + '</w:p>'
lg = f'<w:lang w:val="{L}"/>'
nuevo = [
  f'<w:p><w:pPr><w:pStyle w:val="Normal"/><w:rPr>{lg}</w:rPr></w:pPr><w:r><w:rPr>' + re.search(r'<w:r><w:rPr>(.*?)</w:rPr><w:t', ps[2], re.S).group(1) + f'</w:rPr><w:t>{e(N["cabecera"])}</w:t></w:r></w:p>',
  par([(f'<w:i/><w:sz w:val="20"/>{lg}', N["fecha"])]),
  par([(f'<w:b/><w:bCs/><w:sz w:val="40"/>{lg}', N["titular"])], f'<w:b/><w:bCs/><w:sz w:val="40"/>{lg}'),
  par([(f'<w:b/><w:bCs/>{lg}', N["entradilla"])], f'<w:b/><w:bCs/>{lg}'),
]
for b in N["bloques"]:
    if "h" in b: nuevo.append(par([(f'<w:b/><w:bCs/><w:color w:val="003378"/><w:sz w:val="28"/>{lg}', b["h"])], f'<w:b/><w:bCs/><w:color w:val="003378"/><w:sz w:val="28"/>{lg}'))
    elif "b" in b: nuevo.append(par([(f'<w:b/><w:bCs/><w:sz w:val="21"/>{lg}', b["b"]), (f'<w:sz w:val="21"/>{lg}', b.get("p", ""))]))
    else: nuevo.append(par([(f'<w:sz w:val="21"/>{lg}', b["p"])]))
# plantilla: 0 logo, 1 vacío, 2 cabecera, 3 fecha … y los tres últimos (cierre, raya, contactos) se conservan tal cual
cuerpo = "".join(ps[:2]) + "".join(nuevo) + "".join(ps[-3:])
ini = x.index(ps[0]); fin = x.index(ps[-1]) + len(ps[-1])
x2 = x[:ini] + cuerpo + x[fin:]
zo = zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED)
for it in z.infolist(): zo.writestr(it, x2.encode("utf8") if it.filename == "word/document.xml" else z.read(it.filename))
zo.close(); print("ok", out, len(nuevo), "párrafos nuevos")
