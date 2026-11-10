#!/usr/bin/env python3
"""Genera las creatividades de Erreklamatu a partir de una especificación JSON.

Uso:  python3 render.py specs.json carpeta_salida
Cada pieza de specs.json produce dos PNG:
  <id>-tarjeta.png     1600 x 900   (X)
  <id>-infografia.png  1080 x 1350  (Facebook e Instagram)

Campos de cada pieza:
  id, kicker, titular, sub, marcas ("numeros" | "checks"),
  icono: motivo grande de la derecha, según el tema. Uno de: avion, reloj, maleta, calendario, documento,
         casa, euro, escudo, mazo, cancelado, candado, tarjeta, consulta, nube. Por defecto, avion.
  icono2 (opcional): segundo motivo, en una insignia verde junto al grande (misma lista),
  puntos: [{"t": título, "d": texto opcional}] (máximo 4), nota (opcional)
  idioma ("es" por defecto, "eu" para euskera: cambia la frase del pie), pie (opcional: frase del pie a medida)

Requiere Playwright con Chromium y la fuente Poppins instalada. El logo va en logo.png,
junto a este archivo. Si un texto no cabe, el script avisa con DESBORDA y hay que acortarlo.
"""
import asyncio, base64, html, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
LOGO = "data:image/png;base64," + base64.b64encode(open(os.path.join(AQUI, "logo.png"), "rb").read()).decode()
TRAZOS = {  # iconos de Material Design (licencia Apache 2.0), en un lienzo de 24 x 24
    "avion": "M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z",
    "casa": "M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z",
    "reloj": "M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z",
    "maleta": "M17 6h-2V3c0-.55-.45-1-1-1h-4c-.55 0-1 .45-1 1v3H7c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2 0 .55.45 1 1 1s1-.45 1-1h6c0 .55.45 1 1 1s1-.45 1-1c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zM9.5 18H8V9h1.5v9zm3.25 0h-1.5V9h1.5v9zm.75-12h-3V3.5h3V6zM16 18h-1.5V9H16v9z",
    "calendario": "M17 12h-5v5h5v-5zM16 1v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2h-1V1h-2zm3 18H5V8h14v11z",
    "documento": "M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z",
    "euro": "M15 18.5c-2.51 0-4.68-1.42-5.76-3.5H15v-2H8.58c-.05-.33-.08-.66-.08-1s.03-.67.08-1H15V9H9.24C10.32 6.92 12.5 5.5 15 5.5c1.61 0 3.09.59 4.23 1.57L21 5.3C19.41 3.87 17.3 3 15 3c-3.92 0-7.24 2.51-8.48 6H3v2h3.06c-.04.33-.06.66-.06 1 0 .34.02.67.06 1H3v2h3.52c1.24 3.49 4.56 6 8.48 6 2.31 0 4.41-.87 6-2.3l-1.78-1.77c-1.13.98-2.6 1.57-4.22 1.57z",
    "escudo": "M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z",
    "mazo": "M1 21h12v2H1zM5.245 8.07l2.83-2.827 14.14 14.142-2.828 2.828zM12.317 1l5.657 5.656-2.83 2.83-5.654-5.66zM3.825 9.485l5.657 5.657-2.828 2.828-5.657-5.657z",
    "cancelado": "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zM4 12c0-4.42 3.58-8 8-8 1.85 0 3.55.63 4.9 1.69L5.69 16.9C4.63 15.55 4 13.85 4 12zm8 8c-1.85 0-3.55-.63-4.9-1.69L18.31 7.1C19.37 8.45 20 10.15 20 12c0 4.42-3.58 8-8 8z",
    "candado": "M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z",
    "tarjeta": "M20 4H4c-1.11 0-1.99.89-1.99 2L2 18c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V6c0-1.11-.89-2-2-2zm0 14H4v-6h16v6zm0-10H4V6h16v2z",
    "consulta": "M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z",
    "nube": "M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96z",
}
def svg(nombre, color="#00E887"):
    giro = ' style="transform:rotate(45deg)"' if nombre == "avion" else ""
    return f'<svg viewBox="0 0 24 24"{giro}><path fill="{color}" d="{TRAZOS.get(nombre, TRAZOS["avion"])}"/></svg>'
CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Poppins,'Segoe UI',sans-serif;color:#0B1F44;background:#fff;overflow:hidden}
.kicker{color:#00E887;font-weight:700;letter-spacing:.2em;text-transform:uppercase}
.disco{position:absolute;border-radius:50%;background:#0A4496}
.disco svg{position:absolute}
.rastro{position:absolute;border:0;border-top:6px dotted #00E887;transform-origin:left center}
.pie{display:flex;align-items:center;justify-content:space-between;background:#fff}
.pie img{display:block}
/* tarjeta 1600x900 */
.tarjeta{width:1600px;height:900px;display:flex;flex-direction:column}
.tarjeta .cab{flex:1;background:#003378;color:#fff;padding:0 90px;position:relative;overflow:hidden;display:flex;flex-direction:column;justify-content:center;min-height:0}
.tarjeta .kicker{font-size:30px}
.tarjeta h1{font-size:104px;line-height:1.1;font-weight:700;margin-top:34px;max-width:1010px}
.tarjeta h1.m{font-size:94px} .tarjeta h1.s{font-size:82px}
.tarjeta .sub{font-size:44px;line-height:1.3;font-weight:400;color:#DCE6F7;margin-top:34px;max-width:900px}
.tarjeta .disco{width:520px;height:520px;right:-70px;top:115px}
.tarjeta .disco svg{width:200px;height:200px;left:200px;top:60px}
.tarjeta .rastro{width:430px;left:1050px;top:585px;transform:rotate(-38deg)}
.tarjeta .pie{height:150px;padding:0 90px}
.tarjeta .pie img{height:54px}
.tarjeta .pie span{font-size:30px;color:#55678A}
/* infografía 1080x1350 */
.info{width:1080px;height:1350px;display:flex;flex-direction:column}
.info .cab{background:#003378;color:#fff;padding:66px 70px 60px;position:relative;overflow:hidden}
.info .kicker{font-size:22px}
.info h1{font-size:62px;line-height:1.12;font-weight:700;margin-top:22px;max-width:690px}
.info h1.m{font-size:54px} .info h1.s{font-size:46px}
.info .sub{font-size:30px;line-height:1.3;color:#DCE6F7;margin-top:22px;max-width:630px}
.info .disco{width:360px;height:360px;right:-55px;top:10px}
.info .disco svg{width:120px;height:120px;left:150px;top:70px}
.info .rastro{width:270px;left:735px;top:330px;transform:rotate(-40deg)}
.info .cuerpo{flex:1;padding:50px 70px 30px;display:flex;flex-direction:column;justify-content:space-evenly;min-height:0;overflow:hidden}
.punto{display:flex;gap:30px;align-items:flex-start}
.marca{flex:none;width:64px;height:64px;border-radius:50%;background:#00E887;color:#003378;font-weight:700;font-size:30px;display:flex;align-items:center;justify-content:center}
.marca svg{width:34px;height:34px}
.punto h2{font-size:40px;line-height:1.2;font-weight:700;color:#003378;padding-top:6px}
.punto p{font-size:28px;line-height:1.35;margin-top:8px;color:#1F2B45}
.nota{font-size:21px;color:#55678A;padding-left:94px}
.tarjeta .disco.centro svg{width:240px;height:240px;left:105px;top:140px}
.info .disco.centro svg{width:160px;height:160px;left:72px;top:100px}
.insignia{position:absolute;border-radius:50%;background:#00E887;display:flex;align-items:center;justify-content:center;border:8px solid #003378}
.tarjeta .insignia{width:190px;height:190px;left:1105px;top:430px} .tarjeta .insignia svg{width:104px;height:104px}
.info .insignia{width:124px;height:124px;left:776px;top:186px} .info .insignia svg{width:68px;height:68px}
.info .pie{height:170px;padding:0 70px;background:#EDF1F8}
.info .pie img{height:42px;mix-blend-mode:multiply}
.info .pie div{text-align:right}
.info .pie b span{font-size:inherit;color:inherit} .info .pie b .seg{white-space:nowrap} .info .pie b{display:block;font-size:24px;color:#003378}
.info .pie span{font-size:22px;color:#1F2B45}
"""
PIE = {"es": "Consulta gratuita · Solo cobramos si ganamos", "eu": "Kontsulta doan · Irabazten badugu bakarrik kobratzen dugu"}
CHECK = '<svg viewBox="0 0 24 24"><path fill="none" stroke="#003378" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" d="M5 12.5l4.5 4.5L19 7.5"/></svg>'

def e(s): return html.escape(str(s or ""))
def talla(t): return "s" if len(t) > 46 else ("m" if len(t) > 30 else "")
def cabecera(p):
    icono = p.get("icono", "avion")
    if icono not in TRAZOS: icono = "avion"
    rastro = '<hr class="rastro">' if icono == "avion" and p.get("icono2") not in TRAZOS else ""
    insignia = f'<div class="insignia">{svg(p["icono2"], "#003378")}</div>' if p.get("icono2") in TRAZOS else ""
    return (f'<div class="cab"><div class="disco{"" if icono == "avion" else " centro"}">{svg(icono)}</div>{rastro}{insignia}'
            f'<div class="kicker">{e(p["kicker"])}</div><h1 class="{talla(p["titular"])}">{e(p["titular"])}</h1>'
            + (f'<div class="sub">{e(p["sub"])}</div>' if p.get("sub") else "") + "</div>")
def tarjeta(p):
    return f'<div class="tarjeta">{cabecera(p)}<div class="pie"><img src="{LOGO}"><span>erreklamatu.com</span></div></div>'
def infografia(p):
    filas = ""
    for n, pt in enumerate(p.get("puntos", [])[:4], 1):
        marca = CHECK if p.get("marcas") == "checks" else str(n)
        filas += (f'<div class="punto"><div class="marca">{marca}</div><div><h2>{e(pt["t"])}</h2>'
                  + (f'<p>{e(pt["d"])}</p>' if pt.get("d") else "") + "</div></div>")
    nota = f'<div class="nota">{e(p["nota"])}</div>' if p.get("nota") else ""
    return (f'<div class="info">{cabecera(p)}<div class="cuerpo">{filas}{nota}</div>'
            f'<div class="pie"><img src="{LOGO}"><div><b>{frase_pie(p.get("pie") or PIE.get(p.get("idioma","es"), PIE["es"]))}</b>'
            f'<span>944 027 596 · info@erreklamatu.com</span></div></div></div>')
# Pie de la infografía (Sergio, 9/10/2026): la frase va en una línea; si no cabe, se parte por el «·»
# (una parte en cada línea) y nunca a media frase. Lo decide el navegador midiendo el texto.
def frase_pie(t):
    return '<span class="sep"> · </span>'.join(f'<span class="seg">{e(x)}</span>' for x in t.split(" · "))
PARTE_PIE = ("<script>window.__partePie=function(){document.querySelectorAll('.info .pie b').forEach(function(b){"
             "var g=b.querySelector('.seg'),lh=g?g.getBoundingClientRect().height:0;"
             "if(lh&&b.getBoundingClientRect().height>lh*1.5){b.querySelectorAll('.sep').forEach(function(s){s.outerHTML='<br>'})}})}</script>")
def pagina(cuerpo): return f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{cuerpo}{PARTE_PIE}</body></html>'

async def main(specs, salida):
    from playwright.async_api import async_playwright
    os.makedirs(salida, exist_ok=True)
    async with async_playwright() as pw:
        nav = await pw.chromium.launch(executable_path=os.environ.get("CHROME") or None)
        for p in specs:
            for nombre, w, h, fn, sel in (("tarjeta", 1600, 900, tarjeta, ".cab"), ("infografia", 1080, 1350, infografia, ".cuerpo")):
                pg = await nav.new_page(viewport={"width": w, "height": h})
                await pg.set_content(pagina(fn(p)))
                await pg.evaluate("()=>document.fonts.ready.then(()=>window.__partePie&&window.__partePie())")
                await pg.wait_for_timeout(150)
                desborda = await pg.evaluate("s=>{const c=document.querySelector(s);return c.scrollHeight>c.clientHeight+1}", sel)
                ruta = os.path.join(salida, f'{p["id"]}-{nombre}.png')
                await pg.screenshot(path=ruta)
                print(("DESBORDA  " if desborda else "ok        ") + ruta)
                await pg.close()
        await nav.close()

if __name__ == "__main__":
    asyncio.run(main(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2]))
