#!/usr/bin/env python3
"""Tarjetas «Erreklamatu en los medios» (1080 × 1350) para difundir una aparición en prensa.
Uso: python3 tarjeta_medios.py spec.json carpeta
spec: {id, medio, fecha, formato ("Entrevista", "Noticia", "Audio", "Vídeo"), titular (literal del medio), cita (literal del abogado),
       resumen (una frase nuestra), abogado, cargo, foto (ruta), variantes: ["cita","titular"]}
La cabecera del medio es tipográfica (sin su logotipo), con el nombre tal cual lo escribe el medio.
"""
import asyncio, base64, html, json, os, sys
AQUI=os.path.dirname(os.path.abspath(__file__))
SIS=os.environ.get("SISTEMA", os.path.join(AQUI,"../repo/herramientas/sistema"))
def b64(p,mime): return f"data:{mime};base64,"+base64.b64encode(open(p,"rb").read()).decode()
LOGO=b64(os.path.join(SIS,"logo-alta.png"),"image/png")
e=lambda s: html.escape(str(s or ""))
CSS="""*{box-sizing:border-box;margin:0;padding:0}body{width:1080px;height:1350px;overflow:hidden;font-family:Poppins,sans-serif}
.s{width:1080px;height:1350px;position:relative;overflow:hidden}
.k{font-weight:700;letter-spacing:.2em;text-transform:uppercase;font-size:24px;color:#00E887}
.medio{display:inline-flex;align-items:center;gap:16px;background:#fff;color:#0B1F44;border-radius:14px;padding:14px 22px;font-weight:700;font-size:34px}
.medio small{font-weight:500;font-size:22px;color:#55678A;letter-spacing:.04em}
.pie{position:absolute;left:0;right:0;bottom:0;height:150px;background:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 70px}
.pie img{height:46px}.pie span{font-size:24px;color:#003378;font-weight:600}
/* variante cita */
.cita{background:#003378;color:#fff}
.cita .foto{position:absolute;right:0;bottom:150px;width:470px;height:752px;background-size:cover;background-position:50% 0}
.cita .foto:before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,#003378 0,rgba(0,51,120,.55) 30%,rgba(0,51,120,0) 60%),linear-gradient(180deg,#003378 0,rgba(0,51,120,0) 22%)}
.cita .foto{filter:saturate(.9)}
.cita .top{position:absolute;left:70px;top:70px;right:70px;display:flex;flex-direction:column;gap:22px;align-items:flex-start}
.cita .q{position:absolute;left:70px;top:300px;width:640px}
.cita .comillas{font-size:200px;line-height:.6;color:#00E887;font-weight:700;height:90px}
.cita blockquote{font-size:58px;line-height:1.16;font-weight:700;letter-spacing:-.01em}
.cita blockquote em{font-style:normal;color:#00E887}
.cita .quien{margin-top:34px;font-size:28px;line-height:1.3;color:#DCE6F7}.cita .quien b{color:#fff;display:block;font-size:32px}
/* variante titular */
.tit{background:#F4F7FC}
.tit .band{position:absolute;left:0;right:0;top:0;height:520px;background:#003378}
.tit .top{position:absolute;left:70px;top:64px;right:70px;display:flex;justify-content:space-between;align-items:center}
.tit .papel{position:absolute;left:70px;right:70px;top:170px;background:#fff;border-radius:22px;box-shadow:0 22px 60px rgba(0,25,70,.28);padding:46px 50px 50px;transform:rotate(-1.2deg)}
.tit .papel .cab{display:flex;justify-content:space-between;align-items:baseline;border-bottom:3px solid #0B1F44;padding-bottom:14px;margin-bottom:26px}
.tit .papel .cab b{font-size:36px;color:#0B1F44}.tit .papel .cab span{font-size:22px;color:#55678A}
.tit .papel .sec{font-size:20px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#C0261C;margin-bottom:14px}
.tit .papel h1{font-size:50px;line-height:1.14;color:#0B1F44;letter-spacing:-.01em}
.tit .papel h1 em{font-style:normal;background:linear-gradient(transparent 58%,#00E887 58%,#00E887 92%,transparent 92%)}
.tit .abajo{position:absolute;left:70px;right:70px;top:820px;display:flex;gap:34px;align-items:center}
.tit .abajo .av{flex:none;width:250px;height:250px;border-radius:50%;background-size:300%;background-position:52% 4%;background-repeat:no-repeat;background-color:#E4E6EA;border:8px solid #00E887}
.tit .abajo p{font-size:40px;line-height:1.3;color:#0B1F44;font-weight:600}.tit .abajo p small{display:block;font-size:26px;font-weight:400;color:#55678A;margin-top:8px}

/* variante cara (v2, 12/11/2026: Sergio pidió solo la cara, bien centrada, sobre el modelo 1) */
.cara{background:#003378;color:#fff}
.cara .top{position:absolute;left:70px;right:70px;top:60px;display:flex;flex-direction:column;align-items:center;gap:20px}
.cara .medio{white-space:nowrap}
.cara .disco{position:absolute;right:-160px;top:-160px;width:560px;height:560px;border-radius:50%;background:#0A4496}
.cara .av{position:absolute;left:50%;top:225px;width:330px;height:330px;margin-left:-165px;border-radius:50%;background-size:cover;background-position:50% 50%;border:10px solid #00E887;box-shadow:0 18px 40px rgba(0,0,0,.35)}
.cara .quien{position:absolute;left:70px;right:70px;top:580px;text-align:center;font-size:28px;color:#DCE6F7;line-height:1.3}
.cara .quien b{display:block;color:#fff;font-size:36px}
.cara .q{position:absolute;left:80px;right:80px;top:690px;bottom:170px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}
.cara .comillas{font-size:170px;line-height:.55;height:70px;color:#00E887;font-weight:700}
.cara blockquote{font-size:60px;line-height:1.15;font-weight:700;letter-spacing:-.01em}
.cara blockquote em{font-style:normal;color:#00E887}
"""
def pie(s): return f'<div class="pie"><img src="{LOGO}"><span>{e(s.get("pie","Consulta gratuita · 944 027 596"))}</span></div>'
def v_cita(s,foto):
    return (f'<div class="s cita"><div class="foto" style="background-image:url({foto})"></div><div class="top"><div class="k">Erreklamatu en los medios</div>'
            f'<div class="medio">{e(s["medio"])}<small>{e(s["formato"])} · {e(s["fecha"])}</small></div></div>'
            f'<div class="q"><div class="comillas">“</div><blockquote>{s["cita_html"]}</blockquote><div class="quien"><b>{e(s["abogado"])}</b>{e(s["cargo"])}</div></div>{pie(s)}</div>')
def v_tit(s,foto):
    return (f'<div class="s tit"><div class="band"></div><div class="top"><div class="k">Erreklamatu en los medios</div><div class="k" style="color:#fff;letter-spacing:.1em">{e(s["fecha"])}</div></div>'
            f'<div class="papel"><div class="cab"><b>{e(s["medio"])}</b><span>{e(s["formato"])}</span></div><div class="sec">{e(s.get("seccion",""))}</div><h1>{s["titular_html"]}</h1></div>'
            f'<div class="abajo"><div class="av" style="background-image:url({foto})"></div><p>{e(s["resumen"])}<small>{e(s["abogado"])}, {e(s["cargo"])}</small></p></div>{pie(s)}</div>')
def v_cara(s,foto):
    cara=b64(s["cara"],"image/jpeg")
    return (f'<div class="s cara"><div class="disco"></div><div class="top"><div class="k">Erreklamatu en los medios</div>'
            f'<div class="medio">{e(s["medio"])}<small>{e(s["formato"])} · {e(s["fecha"])}</small></div></div>'
            f'<div class="av" style="background-image:url({cara})"></div><div class="quien"><b>{e(s["abogado"])}</b>{e(s["cargo"])}</div>'
            f'<div class="q"><div class="comillas">“</div><blockquote>{s["cita_html"]}</blockquote></div>{pie(s)}</div>')
async def main(spec,out):
    from playwright.async_api import async_playwright
    os.makedirs(out,exist_ok=True); foto=b64(spec["foto"],"image/jpeg")
    async with async_playwright() as pw:
        nav=await pw.chromium.launch(); pg=await nav.new_page(viewport={"width":1080,"height":1350})
        for v,fn in (("cita",v_cita),("titular",v_tit),("cara",v_cara)):
            if v not in spec.get("variantes",["cita","titular"]): continue
            await pg.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{fn(spec,foto)}</body></html>')
            await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(200)
            r=os.path.join(out,f'{spec["id"]}-medios-{v}.png'); await pg.screenshot(path=r); print("ok",r)
        await nav.close()
if __name__=="__main__": asyncio.run(main(json.load(open(sys.argv[1])),sys.argv[2]))
