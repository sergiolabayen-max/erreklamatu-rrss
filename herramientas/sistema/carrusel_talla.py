#!/usr/bin/env python3
"""Genera carruseles de imágenes de Erreklamatu (1080 x 1350, proporción 4:5) a partir de una especificación JSON.

Uso:  python3 carrusel.py specs.json carpeta_salida [id,id]
Cada carrusel de specs.json produce <id>-01.png, <id>-02.png… y <id>-x.png (la portada sin «Desliza», para X).

Campos de cada carrusel:
  id, kicker (antetítulo, sale en todas las imágenes), icono (motivo de la portada; misma lista que render.py),
  tema ("claro" por defecto u "oscuro": color de las imágenes interiores), slides: lista de imágenes, en orden.
Tipos de imagen ("tipo"):
  portada  -> titulo, sub (opcional)
  Un carrusel con "video": true sale sin la flecha de «desliza» en el pie: es para montar las imágenes en un vídeo.
  En punto, "denso": true reduce un poco el cuerpo (40 px) y abre el interlineado: solo si Sergio lo pide para una imagen cargada.
  En punto, cifras, mito y resena, "antetitulo" (opcional) sustituye al kicker en esa imagen: sirve para marcar secciones
  («Se mantiene», «Mejora», «Letra pequeña»).
  punto    -> num (opcional: número o "check"), titulo, texto (lista de párrafos, opcional), lista (opcional), ref (opcional)
  cifras   -> titulo, filas: [[cifra, explicación], …] (máximo 3), texto (opcional), ref
  mito     -> mito, realidad, texto (opcional), ref
  cierre   -> titulo, texto, lineas (dos o tres frases con visto), ref (fuentes)
  resena   -> cita (el texto de la reseña, tal cual), nombre (nombre de pila e inicial), origen ("Reseña en Google"),
              comentario (lo que hay detrás: el valor o la ventaja del servicio que esa reseña muestra), estrellas (5 por defecto)
Un carrusel con "idioma": "eu" pone en euskera los rótulos fijos («Irristatu», «Honen atzean», «Google-ko iritzia»).
  foto     -> foto (ruta de la imagen), pos (qué parte de la foto se ve si hay que recortarla: "50% 30%"), antetitulo (opcional;
              si falta, el kicker), titulo, titulo_px (opcional: tamaño del titular en píxeles, si Sergio lo pide más grande; 80 de serie), sub (opcional), lineas (opcional). La foto va arriba, a todo el ancho, y el texto
              debajo: nada tapa las caras. Sirve de portada de un carrusel o de imagen única (un carrusel de una sola imagen).
En los textos, *así* resalta (subrayado de rotulador en claro; verde en oscuro) y **así** pone negrita.
"ref" es la fuente de lo que afirma esa imagen (norma, sentencia o declaración): va en pequeño, abajo.

Requiere Playwright con Chromium y la fuente Poppins. logo.png, junto a este archivo.
Si un texto no cabe, el script avisa con DESBORDA y hay que acortarlo: nunca se reduce la letra para que quepa más.
"""
import asyncio, base64, html, json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from render import TRAZOS                      # mismos iconos que las infografías

LOGO = "data:image/png;base64," + base64.b64encode(open(os.path.join(AQUI, "logo.png"), "rb").read()).decode()
NAVY, AZUL, VERDE, TINTA, GRIS, CLARO = "#003378", "#0A4496", "#00E887", "#0B1F44", "#55678A", "#F4F7FC"
W, H = 1080, 1350

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Poppins,'Segoe UI',sans-serif;width:1080px;height:1350px;overflow:hidden}
.s{width:1080px;height:1350px;position:relative;display:flex;flex-direction:column;overflow:hidden}
.claro{background:#F4F7FC;color:#0B1F44} .oscuro{background:#003378;color:#fff}
em{font-style:normal} strong{font-weight:700}
.claro em{background:linear-gradient(transparent 62%,#00E887 62%,#00E887 93%,transparent 93%);padding:0 4px;margin:0 -4px}
.oscuro em{color:#00E887}
.claro strong{color:#003378} .oscuro strong{color:#fff}
/* cabecera y pie comunes */
.cab{flex:none;height:150px;padding:0 84px;display:flex;align-items:center;justify-content:space-between}
.kicker{font-weight:700;letter-spacing:.2em;text-transform:uppercase;font-size:24px}
.claro .kicker{color:#0A4496} .oscuro .kicker{color:#00E887}
.cuenta{font-size:26px;font-weight:600;border-radius:40px;padding:8px 22px}
.claro .cuenta{background:#E3EAF6;color:#003378} .oscuro .cuenta{background:#0A4496;color:#fff}
.cuerpo{flex:1;min-height:0;padding:10px 84px 0;display:flex;flex-direction:column;justify-content:center;overflow:hidden}
.pie{flex:none;height:150px;padding:0 84px;display:flex;align-items:center;justify-content:space-between;gap:30px}
.ref{font-size:23px;line-height:1.35;max-width:780px}
.claro .ref{color:#55678A} .oscuro .ref{color:#B9C8E6}
.flecha{flex:none;width:76px;height:76px;border-radius:50%;background:#00E887;display:flex;align-items:center;justify-content:center}
.flecha svg{width:40px;height:40px}
/* punto */
.num{width:104px;height:104px;border-radius:50%;background:#00E887;color:#003378;font-weight:700;font-size:56px;display:flex;align-items:center;justify-content:center;margin-bottom:38px}
.num svg{width:58px;height:58px}
h2{font-size:74px;line-height:1.1;font-weight:700;letter-spacing:-.01em}
h2.m{font-size:64px} h2.xs{font-size:56px}
.claro h2{color:#003378}
.raya{width:110px;height:10px;border-radius:5px;background:#00E887;margin:36px 0 38px}
.oscuro .raya{background:#00E887}
p{font-size:44px;line-height:1.34}
p+p{margin-top:26px}
ul{list-style:none;margin-top:8px}
ul li{font-size:44px;line-height:1.28;padding-left:80px;position:relative;margin-top:30px}
ul li:first-child{margin-top:0}
p+ul{margin-top:34px}
ul li i{position:absolute;left:0;top:3px;width:52px;height:52px;border-radius:50%;background:#00E887;display:flex;align-items:center;justify-content:center}
ul li i svg{width:30px;height:30px}
/* imagen con mucho texto ("denso": true): cuerpo algo menor y más abierto */
.denso p{font-size:40px;line-height:1.42} .denso ul li{font-size:40px;line-height:1.4}
/* cifras */
.fila{display:flex;align-items:baseline;gap:34px;padding:26px 0;border-top:3px solid #DCE4F2}
.oscuro .fila{border-top-color:#0A4496}
.fila:first-of-type{border-top:0}
.fila b{flex:none;width:310px;font-size:88px;line-height:1;font-weight:700;letter-spacing:-.02em}
.claro .fila b{color:#003378} .oscuro .fila b{color:#00E887}
.fila span{font-size:38px;line-height:1.3}
.cifras p{margin-top:30px;font-size:38px}
/* mito */
.tag{display:inline-block;font-size:26px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;border-radius:10px;padding:10px 22px}
.tag.mito{background:#DCE4F2;color:#55678A} .oscuro .tag.mito{background:#0A4496;color:#B9C8E6}
.tag.real{background:#00E887;color:#003378}
.dicho{font-size:54px;line-height:1.2;font-weight:600;margin:26px 0 56px;color:#55678A;text-decoration:line-through;text-decoration-thickness:4px;text-decoration-color:#9AA9C4}
.oscuro .dicho{color:#B9C8E6;text-decoration-color:#6F86B5}
.verdad{font-size:50px;line-height:1.22;font-weight:700;margin-top:26px}
.claro .verdad{color:#003378}
.mito p{margin-top:28px;font-size:41px}
/* portada */
.portada{background:#003378;color:#fff}
.portada .disco{position:absolute;width:560px;height:560px;border-radius:50%;background:#0A4496;right:-150px;top:-120px}
.portada .disco svg{position:absolute;width:190px;height:190px;left:150px;top:230px}
.portada .cab{position:relative}
.portada .kicker{color:#00E887;font-size:27px}
.portada .cuerpo{justify-content:flex-end;padding-bottom:70px;position:relative}
.portada h1{font-size:104px;line-height:1.06;font-weight:700;letter-spacing:-.015em}
.portada h1.m{font-size:90px} .portada h1.xs{font-size:78px}
.portada h1 em{color:#00E887;background:none;padding:0;margin:0}
.portada .sub{font-size:42px;line-height:1.3;color:#DCE6F7;margin-top:34px;max-width:860px}
.banda{flex:none;height:150px;background:#fff;padding:0 84px;display:flex;align-items:center;justify-content:space-between}
.banda img{height:50px;display:block}
.desliza{display:flex;align-items:center;gap:18px;font-size:30px;font-weight:700;color:#003378}
.banda .web{font-size:28px;color:#55678A}
/* cierre */
.cierre{background:#003378;color:#fff}
.cierre .cuerpo{justify-content:center}
.cierre h2{font-size:78px;color:#fff}
.cierre h2 em{color:#00E887;background:none;padding:0;margin:0}
.cierre p{color:#DCE6F7}
.cierre .kicker{color:#00E887}
.caja{margin-top:44px;background:#0A4496;border-radius:28px;padding:38px 44px}
.caja div{font-size:36px;font-weight:600;padding-left:62px;position:relative;line-height:1.3}
.caja div+div{margin-top:18px}
.caja div i{position:absolute;left:0;top:3px;width:42px;height:42px;border-radius:50%;background:#00E887;display:flex;align-items:center;justify-content:center}
.caja div i svg{width:24px;height:24px}
.tel{font-size:92px;font-weight:700;letter-spacing:-.01em;margin-top:40px;line-height:1}
.cierre .ref{color:#B9C8E6;font-size:21px;max-width:none}
/* reseña */
.resena .estrellas{display:flex;gap:10px;margin-bottom:34px}
.resena .estrellas svg{width:58px;height:58px}
.resena .cita{font-size:50px;line-height:1.28;font-weight:600;color:#003378}
.resena .cita.media{font-size:44px} .resena .cita.larga{font-size:38px}
.resena .quien{font-size:30px;color:#55678A;margin-top:30px}
.resena .quien b{color:#0B1F44}
.resena .detras{margin-top:44px;background:#003378;color:#fff;border-radius:28px;padding:34px 40px}
.resena .detras span{display:block;font-size:22px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:#00E887;margin-bottom:12px}
.resena .detras p{font-size:36px;line-height:1.32;color:#fff}
/* foto: la foto arriba y el texto debajo, sin tapar a nadie */
.fotoS{background:#003378;color:#fff}
.fimg{flex:1;min-height:0;position:relative;background-size:cover;background-repeat:no-repeat}
.fimg:after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:150px;background:linear-gradient(rgba(0,51,120,0),#003378)}
.fimg .cuenta{position:absolute;right:84px;top:48px;background:#fff;color:#003378}
.fotoS .cuerpo{flex:none;padding:6px 84px 54px;justify-content:flex-start;overflow:visible}
.fotoS .kicker{color:#00E887;font-size:27px;margin-bottom:22px}
.fotoS h1{font-size:80px;line-height:1.08;font-weight:700;letter-spacing:-.015em}
.fotoS h1.m{font-size:70px} .fotoS h1.xs{font-size:60px}
.fotoS h1 em{color:#00E887;background:none;padding:0;margin:0}
.fotoS .sub{font-size:37px;line-height:1.32;color:#DCE6F7;margin-top:26px}
.fotoS .checks{display:flex;flex-wrap:wrap;gap:16px 34px;margin-top:30px}
.fotoS .checks div{font-size:33px;font-weight:600;padding-left:54px;position:relative;line-height:1.3}
.fotoS .checks i{position:absolute;left:0;top:2px;width:40px;height:40px;border-radius:50%;background:#00E887;display:flex;align-items:center;justify-content:center}
.fotoS .checks i svg{width:23px;height:23px}
"""
CHECK = '<svg viewBox="0 0 24 24"><path fill="none" stroke="#003378" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round" d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
FLECHA = '<svg viewBox="0 0 24 24"><path fill="none" stroke="#003378" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" d="M4 12h15M13 5.5l6.5 6.5-6.5 6.5"/></svg>'

def t(s):
    """Texto con marcas: *resalte* y **negrita**. Primero se escapa el HTML."""
    s = html.escape(str(s or ""), quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", s).replace("\n", "<br>")          # un salto de línea en el texto parte el renglón ahí
def plano(s): return re.sub(r"\*+", "", str(s or ""))
def talla(s, m, c): n = len(plano(s)); return "xs" if n > c else ("m" if n > m else "")   # «xs», no «s»: «s» es la clase de la imagen entera
def icono(nombre, color=VERDE):
    giro = ' style="transform:rotate(45deg)"' if nombre == "avion" else ""
    return f'<svg viewBox="0 0 24 24"{giro}><path fill="{color}" d="{TRAZOS.get(nombre, TRAZOS["avion"])}"/></svg>'
def cab(c, n, N, s=None): return f'<div class="cab"><div class="kicker">{t((s or {}).get("antetitulo") or c["kicker"])}</div><div class="cuenta">{n}/{N}</div></div>'
def pie(s, ultimo=False):
    return f'<div class="pie"><div class="ref">{t(s.get("ref", ""))}</div>' + ("" if ultimo else f'<div class="flecha">{FLECHA}</div>') + "</div>"
def parrafos(s): return "".join(f"<p>{t(x)}</p>" for x in ([s["texto"]] if isinstance(s.get("texto"), str) else s.get("texto", [])))
def lista(s): return ("<ul>" + "".join(f"<li><i>{CHECK}</i>{t(x)}</li>" for x in s["lista"]) + "</ul>") if s.get("lista") else ""

EU = {"Desliza": "Irristatu", "Lo que hay detrás": "Honen atzean", "Reseña en Google": "Google-ko iritzia"}
def L(c, txt):
    """Rótulos fijos: en euskera si el carrusel lleva "idioma": "eu"."""
    return EU.get(txt, txt) if c.get("idioma") == "eu" else txt
def portada(c, s, n, N, para_x=False):
    derecha = '<div class="web">erreklamatu.com</div>' if para_x else f'<div class="desliza">{L(c, "Desliza")} <div class="flecha">{FLECHA}</div></div>'
    return (f'<div class="s portada"><div class="disco">{icono(c.get("icono", "avion"))}</div>'
            f'<div class="cab"><div class="kicker">{t(c["kicker"])}</div></div>'
            f'<div class="cuerpo"><h1 class="{s.get("talla") or talla(s["titulo"], 44, 62)}">{t(s["titulo"])}</h1>'
            + (f'<div class="sub">{t(s["sub"])}</div>' if s.get("sub") else "") + "</div>"
            f'<div class="banda"><img src="{LOGO}">{derecha}</div></div>')
def punto(c, s, n, N):
    num = f'<div class="num">{CHECK if s.get("num") == "check" else t(s["num"])}</div>' if s.get("num") else ""
    return (f'<div class="s {c.get("tema", "claro")}{" denso" if s.get("denso") else ""}">{cab(c, n, N, s)}<div class="cuerpo">{num}'
            f'<h2 class="{talla(s["titulo"], 46, 70)}">{t(s["titulo"])}</h2><div class="raya"></div>{parrafos(s)}{lista(s)}</div>{pie(s, c.get("video"))}</div>')
def cifras(c, s, n, N):
    filas = "".join(f'<div class="fila"><b>{t(a)}</b><span>{t(b)}</span></div>' for a, b in s["filas"][:3])
    num = f'<div class="num">{t(s["num"])}</div>' if s.get("num") else ""
    return (f'<div class="s {c.get("tema", "claro")} cifras">{cab(c, n, N, s)}<div class="cuerpo">{num}'
            f'<h2 class="{talla(s["titulo"], 46, 70)}">{t(s["titulo"])}</h2><div class="raya"></div>{filas}{parrafos(s)}</div>{pie(s, c.get("video"))}</div>')
def mito(c, s, n, N):
    return (f'<div class="s {c.get("tema", "claro")} mito">{cab(c, n, N, s)}<div class="cuerpo">'
            f'<div><span class="tag mito">Mito</span></div><div class="dicho">{t(s["mito"])}</div>'
            f'<div><span class="tag real">Realidad</span></div><div class="verdad">{t(s["realidad"])}</div>{parrafos(s)}</div>{pie(s, c.get("video"))}</div>')
def cierre(c, s, n, N):
    lineas = "".join(f"<div><i>{CHECK}</i>{t(x)}</div>" for x in s.get("lineas", []))
    return (f'<div class="s cierre"><div class="cab"><div class="kicker">{t(c["kicker"])}</div><div class="cuenta" style="background:#0A4496;color:#fff">{n}/{N}</div></div>'
            f'<div class="cuerpo"><h2 class="{talla(s["titulo"], 40, 60)}">{t(s["titulo"])}</h2><div class="raya"></div>{parrafos(s)}'
            f'<div class="caja">{lineas}</div><div class="tel">944 027 596</div>'
            + (f'<div class="ref" style="margin-top:40px">{t(s["ref"])}</div>' if s.get("ref") else "") + "</div>"
            f'<div class="banda"><img src="{LOGO}"><div class="web">erreklamatu.com</div></div></div>')
ESTRELLA = '<svg viewBox="0 0 24 24"><path fill="#F5B400" d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>'
def resena(c, s, n, N):
    largo = len(plano(s["cita"])); cls = "larga" if largo > 230 else ("media" if largo > 150 else "")   # ojo: «s» es la clase de la imagen entera; no reutilizarla
    return (f'<div class="s claro resena">{cab(c, n, N, s)}<div class="cuerpo"><div class="estrellas">{ESTRELLA * int(s.get("estrellas", 5))}</div>'
            f'<div class="cita {cls}">«{t(s["cita"])}»</div><div class="quien"><b>{t(s["nombre"])}</b> · {t(s.get("origen") or L(c, "Reseña en Google"))}</div>'
            f'<div class="detras"><span>{L(c, "Lo que hay detrás")}</span><p>{t(s["comentario"])}</p></div></div>{pie(s, c.get("video"))}</div>')
_FOTOS = {}
def foto_uri(ruta):
    """La foto, reducida a 2000 px de lado mayor y metida en la página."""
    if ruta not in _FOTOS:
        import io
        from PIL import Image
        im = Image.open(ruta).convert("RGB"); im.thumbnail((2000, 2000)); b = io.BytesIO(); im.save(b, "JPEG", quality=90)
        _FOTOS[ruta] = "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
    return _FOTOS[ruta]
def foto(c, s, n, N, para_x=False):
    derecha = f'<div class="desliza">{L(c, "Desliza")} <div class="flecha">{FLECHA}</div></div>' if (N > 1 and n == 1 and not para_x) else '<div class="web">erreklamatu.com</div>'
    cuenta = f'<div class="cuenta">{n}/{N}</div>' if (N > 1 and n > 1) else ""
    lineas = ('<div class="checks">' + "".join(f"<div><i>{CHECK}</i>{t(x)}</div>" for x in s["lineas"]) + "</div>") if s.get("lineas") else ""
    return (f'<div class="s fotoS"><div class="fimg" style="background-image:url({foto_uri(s["foto"])});background-position:{s.get("pos", "50% 30%")}">{cuenta}</div>'
            f'<div class="cuerpo"><div class="kicker">{t(s.get("antetitulo") or c["kicker"])}</div><h1 class="{talla(s["titulo"], 34, 52)}"' + (f' style="font-size:{int(s["titulo_px"])}px"' if s.get("titulo_px") else "") + f'>{t(s["titulo"])}</h1>'
            + (f'<div class="sub">{t(s["sub"])}</div>' if s.get("sub") else "") + lineas + "</div>"
            f'<div class="banda"><img src="{LOGO}">{derecha}</div></div>')
TIPOS = {"resena": resena, "foto": foto, "portada": portada, "punto": punto, "cifras": cifras, "mito": mito, "cierre": cierre}
def pagina(cuerpo): return f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{cuerpo}</body></html>'

async def main(specs, salida, solo=()):
    from playwright.async_api import async_playwright
    os.makedirs(salida, exist_ok=True); mal = 0
    async with async_playwright() as pw:
        nav = await pw.chromium.launch()
        pg = await nav.new_page(viewport={"width": W, "height": H})
        for c in specs:
            if solo and c["id"] not in solo: continue
            N = len(c["slides"]); hechas = []
            for n, s in enumerate(c["slides"], 1):
                hechas.append((f'{n:02d}', TIPOS[s["tipo"]](c, s, n, N)))
            hechas.append(("x", TIPOS[c["slides"][0]["tipo"] if c["slides"][0]["tipo"] == "foto" else "portada"](c, c["slides"][0], 1, N, para_x=True)))
            for nombre, cuerpo in hechas:
                await pg.set_content(pagina(cuerpo)); await pg.wait_for_timeout(120)
                desborda = await pg.evaluate("()=>{const c=document.querySelector('.cuerpo'),f=document.querySelector('.fimg');const q=document.querySelector('.cita');return c.scrollHeight>c.clientHeight+1||(!!q&&q.getBoundingClientRect().right>1081-60)||[...document.querySelectorAll('.ref')].some(r=>r.scrollWidth>r.clientWidth+1)||(!!f&&f.clientHeight<560)}")
                ruta = os.path.join(salida, f'{c["id"]}-{nombre}.png')
                await pg.screenshot(path=ruta); mal += desborda
                print(("DESBORDA  " if desborda else "ok        ") + ruta, flush=True)
        await nav.close()
    print("imágenes que desbordan:", mal)

if __name__ == "__main__":
    asyncio.run(main(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2], sys.argv[3].split(",") if len(sys.argv) > 3 else ()))
