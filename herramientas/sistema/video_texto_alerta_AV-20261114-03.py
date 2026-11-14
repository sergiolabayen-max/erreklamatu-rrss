#!/usr/bin/env python3
"""Vídeo de texto animado (sin voz) para alertas de actualidad: aviso AV-20261114-03, cierre del espacio aéreo de EE. UU. (13/11).
Uso: python3 video_huelga.py carpeta_salida
Escenas en HTML (Poppins, colores de marca), animadas por tiempo con JS y capturadas fotograma a fotograma con Playwright (30 fps).
Música: sintonía «viva» (sintonia.py). Zonas seguras: lo importante entre y=330 y y=1500 (las redes tapan arriba y abajo).
"""
import asyncio, base64, json, os, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
SIS = os.environ.get("SISTEMA", os.path.join(AQUI, "../repo/herramientas/sistema"))
LOGO = "data:image/png;base64," + base64.b64encode(open(os.path.join(SIS, "logo-alta.png"), "rb").read()).decode()
FPS = 30
# (inicio, fin) de cada escena en segundos
ESC = [(0, 3.8), (3.8, 9.8), (9.8, 15.0), (15.0, 19.8), (19.8, 27.0), (27.0, 34.0), (34.0, 38.6), (38.6, 43.0)]
DUR = ESC[-1][1]
AV = '<svg viewBox="0 0 24 24" style="transform:rotate(45deg)"><path fill="#00E887" d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/></svg>'
CK = '<svg viewBox="0 0 24 24"><path fill="none" stroke="#003378" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round" d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
NO = '<svg viewBox="0 0 24 24"><path fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" d="M6 6l12 12M18 6L6 18"/></svg>'
HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1920px;overflow:hidden;font-family:Poppins,sans-serif;background:#003378;color:#fff}}
#bg{{position:absolute;inset:0;background:radial-gradient(circle at 80% 18%,#0A4496 0,#0A4496 22%,transparent 22.2%),#003378}}
.rastro{{position:absolute;left:-200px;top:250px;width:1500px;border-top:8px dotted rgba(0,232,135,.35);transform:rotate(-24deg)}}
.avion{{position:absolute;width:150px;height:150px}}
.e{{position:absolute;left:0;right:0;top:330px;bottom:420px;padding:0 90px;display:flex;flex-direction:column;justify-content:center;opacity:0}}
.k{{font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#00E887;font-size:34px}}
.h{{font-weight:700;font-size:92px;line-height:1.06;letter-spacing:-.01em}}
.h em{{font-style:normal;color:#00E887}}
.big{{font-weight:700;font-size:420px;line-height:.9;color:#00E887;letter-spacing:-.03em}}
.sub{{font-size:52px;line-height:1.25;color:#DCE6F7;margin-top:24px}}
.raya{{width:130px;height:12px;border-radius:6px;background:#00E887;margin:40px 0}}
.fila{{display:flex;align-items:center;gap:30px;background:#fff;color:#003378;border-radius:28px;padding:28px 36px;margin-top:24px}}
.fila b{{font-size:96px;line-height:1;min-width:120px;text-align:center;color:#003378}}
.fila div{{font-size:44px;line-height:1.2;font-weight:600}}
.fila div span{{display:block;font-size:34px;font-weight:400;color:#55678A}}
.barra{{display:flex;align-items:center;gap:26px;margin-top:30px}}
.barra .n{{font-size:80px;font-weight:700;width:90px;color:#00E887}}
.barra .l{{height:84px;border-radius:16px;background:#fff;color:#003378;font-size:44px;font-weight:700;display:flex;align-items:center;padding:0 30px;white-space:nowrap}}
.ok{{display:flex;gap:30px;align-items:flex-start;margin-top:38px}}
.ok i{{flex:none;width:84px;height:84px;border-radius:50%;background:#00E887;display:flex;align-items:center;justify-content:center}}
.ok i svg{{width:50px;height:50px}}
.ok i.no{{background:#E5484D}}
.ok p{{font-size:58px;line-height:1.18;font-weight:700}}
.ok p span{{display:block;font-size:40px;font-weight:400;color:#DCE6F7;margin-top:8px}}
#fin{{position:absolute;inset:0;background:#fff;opacity:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:#003378;padding:0 80px}}
#fin img{{width:760px}}
#fin .t1{{font-size:64px;font-weight:700;margin-top:80px;line-height:1.15}}
#fin .chk{{margin-top:50px;font-size:46px;font-weight:600;line-height:1.6}}
#fin .chk em{{font-style:normal;background:linear-gradient(transparent 60%,#00E887 60%,#00E887 92%,transparent 92%)}}
#fin .tel{{font-size:120px;font-weight:700;margin-top:60px;letter-spacing:-.01em}}
#fin .web{{font-size:44px;color:#55678A;margin-top:16px}}
.big2{{white-space:nowrap;font-weight:700;font-size:168px;line-height:1;color:#00E887;letter-spacing:-.02em;margin:10px 0 20px}}
.fila b.hr{{font-size:64px;min-width:190px}}
#fin .legal{{position:absolute;bottom:430px;left:80px;right:80px;font-size:28px;color:#55678A}}
#prog{{position:absolute;left:0;top:0;height:10px;background:#00E887}}
</style></head><body>
<div id="bg"></div><hr class="rastro"><div class="avion" id="av">{AV}</div>
<div class="e" id="e0"><div class="k">¿Volabas a EE. UU.?</div><div class="big2">4 h 21 min</div>
  <div class="h">sin un solo despegue en <em>Estados Unidos</em></div><div class="sub" style="font-size:44px">Fallo de su control aéreo · viernes 13</div></div>
<div class="e" id="e1"><div class="k">Qué pasó (hora peninsular)</div>
  <div class="fila"><b class="hr">21:54</b><div>Viernes<span>La FAA para todos los despegues en EE. UU.</span></div></div>
  <div class="fila"><b class="hr">2:15</b><div>Sábado<span>Levanta la orden, 4 h 21 min después</span></div></div>
  <div class="fila"><b class="hr">⚠</b><div>La causa<span>Fallos de comunicación en varios centros de control</span></div></div></div>
<div class="e" id="e2"><div class="k">Por qué</div><div class="h">Equipos de telecomunicaciones <em>antiguos y sobrecargados</em></div><div class="raya"></div>
  <div class="sub">Lo dice el secretario de Transporte de EE. UU., Sean Duffy. No hay indicios de ciberataque, aunque se investiga.</div></div>
<div class="e" id="e3"><div class="k">Viajeros afectados</div><div class="big2">+7.000</div>
  <div class="h">vuelos cancelados en <em>todo EE. UU.</em></div><div class="sub">Cifra provisional de NBC News. Recolocar aviones y tripulaciones puede llevar días.</div></div>
<div class="e" id="e4"><div class="k">Desde el Estado español</div><div class="h" style="font-size:76px">Eurocontrol frena las salidas <em>hacia EE. UU.</em></div>
  <div class="fila"><b class="hr">✈</b><div>Madrid y Barcelona<span>con Nueva York (JFK), Newark y Miami</span></div></div>
  <div class="fila"><b class="hr">!</b><div>Iberia<span>avisa de cambios en su programación</span></div></div>
  <div class="sub" style="font-size:38px">Los vuelos ya en el aire siguieron hasta su destino. No hay cifra de vuelos afectados.</div></div>
<div class="e" id="e5"><div class="k">¿Y tus derechos?</div>
  <div class="ok"><i>{CK}</i><p>Reembolso u otro vuelo<span>Tú eliges</span></p></div>
  <div class="ok"><i>{CK}</i><p>Comida y, si toca pasar la noche, hotel</p></div>
  <div class="ok"><i class="no">{NO}</i><p>Compensación: no<span>Un fallo del control aéreo es una circunstancia extraordinaria</span></p></div>
  <div class="sub" style="font-size:36px">En vuelos que salen de la UE o con aerolínea europea.</div></div>
<div class="e" id="e6"><div class="k">Consejo</div><div class="h">Pide otro vuelo a la aerolínea <em>antes de comprar tú otro billete</em></div><div class="raya"></div>
  <div class="sub">Y guarda los avisos de cancelación y los tiques de lo que pagues.</div></div>
<div id="fin"><img src="{LOGO}"><div class="t1">¿Te han cancelado o retrasado el vuelo?</div>
  <div class="chk"><em>Consulta gratuita</em><br><em>Solo cobramos si ganamos</em></div>
  <div class="tel">944 027 596</div><div class="web">erreklamatu.com</div>
  <div class="legal">Reglamento (CE) 261/2004 · Fuentes: Demócrata, Infobae y NBC News</div></div>
<div id="prog"></div>
<script>
const ESC={json.dumps(ESC)}, DUR={DUR};
const ease=x=>1-Math.pow(1-Math.min(Math.max(x,0),1),3);
function vis(el,t,a,b){{ // entra 0.35 s, sale 0.3 s
  const i=ease((t-a)/0.35), o=t>b-0.3?ease((t-(b-0.3))/0.3):0;
  el.style.opacity=(i*(1-o)).toFixed(3); el.style.transform=`translateY(${{(1-i)*60-o*40}}px)`; return i; }}
window.render=function(t){{
  for(let n=0;n<7;n++){{ const el=document.getElementById('e'+n),[a,b]=ESC[n];
    if(n===0){{ // la portada ya se ve entera en el fotograma 0
      const o=t>b-0.3?ease((t-(b-0.3))/0.3):0; el.style.opacity=(1-o).toFixed(3); el.style.transform=`scale(${{1+0.04*Math.sin(Math.min(t,1.2)/1.2*Math.PI)}}) translateY(${{-o*40}}px)`;
    }} else vis(el,t,a,b);
    if(false) el.querySelectorAll('.l').forEach((l,k)=>{{const p=ease((t-a-0.3-k*0.25)/0.6); l.style.width=(Math.max(p,0.02)*l.dataset.w)+'px'; l.style.color=p>0.7?'#003378':'transparent';}});
    if(n===1||n===4||n===5) el.querySelectorAll('.fila,.ok').forEach((f,k)=>{{const p=ease((t-a-0.25-k*0.45)/0.4); f.style.opacity=p; f.style.transform=`translateX(${{(1-p)*80}}px)`;}});
  }}
  const fa=ESC[7][0]; document.getElementById('fin').style.opacity=ease((t-fa)/0.35);
  const av=document.getElementById('av'); const u=(t%6)/6; av.style.left=(-160+u*1400)+'px'; av.style.top=(300-u*330)+'px';
  document.getElementById('prog').style.width=(t/DUR*1080)+'px';
}};
render(0);
</script></body></html>"""

async def main(out):
    from playwright.async_api import async_playwright
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "video.html"), "w").write(HTML)
    sil = os.path.join(out, "silencio.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", sil], stdin=subprocess.PIPE)
    async with async_playwright() as pw:
        nav = await pw.chromium.launch(); pg = await nav.new_page(viewport={"width": 1080, "height": 1920})
        await pg.set_content(HTML); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(300)
        n = int(DUR * FPS)
        for f in range(n):
            await pg.evaluate(f"render({f / FPS})")
            ff.stdin.write(await pg.screenshot(type="png"))
            if f in [0]+[int((b-0.6)*FPS) for a,b in ESC]:
                await pg.screenshot(path=os.path.join(out, f"cuadro-{f:04d}.png"))
        await nav.close()
    ff.stdin.close(); ff.wait()
    mus = os.path.join(out, "musica.wav")
    subprocess.run(["python3", os.path.join(SIS, "sintonia.py"), mus, str(DUR), "viva", str(DUR - ESC[7][0])], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", sil, "-i", mus, "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                    "-shortest", "-movflags", "+faststart", os.path.join(out, "video.mp4")], check=True)
    print("ok", os.path.join(out, "video.mp4"))

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))
