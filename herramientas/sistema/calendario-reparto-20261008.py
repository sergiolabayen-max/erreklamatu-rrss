import json,glob,re,datetime as D,collections as C,sys
S='/tmp/claude-0/-home-claude-erreklamatu-rrss/e7eefa61-a30f-57c7-bc2e-7996fd2458cc/scratchpad/'
P=[json.load(open(f)) for f in sorted(glob.glob(S+'cal1240/publicaciones/*.json'))]
A=[p for p in P if p['estado'] in('Aprobada','Programada')]
INI=D.date(2026,10,9); FIN=D.date(2027,6,30)
def caso(p):
  u=(p.get('url_web') or ''); t=(p['tema']+' '+p['titular']).lower()
  if p['area']=='Banca' or '/bancos/' in u or 'bank' in u:
    if 'phishing' in u or p['pilar']=='Phishing' or 'estafa' in t or 'ziber' in t: return 'phishing'
    if 'hipoteca' in u or 'hipoteka' in u or 'hipoteca' in t: return 'hipoteca'
    if 'revolving' in u: return 'revolving'
    return 'banca-otros'
  if p['area'] in('Marca','Otros'): return 'marca' if p['area']=='Marca' else 'otros'
  if 'retrasado' in u or 'atzerapena' in u: return 'retraso'
  if 'cancelado' in u or 'bertan-behera' in u: return 'cancelacion'
  if 'equipaje' in u or 'ekipajea' in u: return 'equipaje'
  if 'overbooking' in u: return 'overbooking'
  if 'reclamaciones-' in u: return 'aerolinea'
  return 'vuelos-general'
SEAS=re.compile(r'temporal|mal tiempo|viento|meteorol|ciclón|nieve|kirk|árbol|ekaitz|eguraldi|huracán',re.I)
def ventana(p):
  s=p['tema']+' '+p['titular']
  if 'Navidad' in s: return (D.date(2026,12,1),D.date(2026,12,20))
  if SEAS.search(s): return (D.date(2026,11,1),D.date(2027,3,15))
  return (INI,FIN)
def fecha(p): return D.datetime.fromisoformat(p['fecha_objetivo'])
fijas=[p for p in A if p['estado']=='Programada' or p.get('fecha_objetivo_redes') or fecha(p).date()>FIN]
mov=[p for p in A if p not in fijas]
ocup=C.Counter(fecha(p).date() for p in fijas)
dias=[INI+D.timedelta(i) for i in range((FIN-INI).days+1)]
libres=[d for d in dias if not ocup[d]]
nhuecos=len(libres)-len(mov)
# huecos repartidos de forma uniforme
step=len(libres)/max(nhuecos,1)
hue=set(libres[int((k+0.5)*step)] for k in range(nhuecos)) if nhuecos>0 else set()
slots=[d for d in libres if d not in hue]
N=len(slots)
def vid(p): return (p.get('video_origen') or '').strip() or None
attrs={'vid':(vid,4),'caso':(caso,2.5),'idioma':(lambda p:p['idioma'],2),'area':(lambda p:p['area'],2),'formato':(lambda p:p['formato'],1),'enfoque':(lambda p:p['enfoque'],1)}
tot={a:C.Counter(f(p) for p in mov) for a,(f,w) in attrs.items()}
placed={a:C.Counter() for a in attrs}
last={}; prev=None; res={}
fixd=C.defaultdict(list)
for p in fijas: fixd[fecha(p).date()].append(p)
fixv=C.defaultdict(list)
for p in fijas:
  if vid(p): fixv[vid(p)].append(fecha(p).date())
rest=list(mov)
for i,d in enumerate(slots):
  best=None
  for p in rest:
    w0,w1=ventana(p)
    if d<w0: continue
    sc=0
    for a,(f,w) in attrs.items():
      v=f(p)
      if v is None: continue
      sc+=w*(tot[a][v]*(i+1)/N-placed[a][v])/max(1,tot[a][v])**0.5
    # urgencia de la ventana
    left=sum(1 for s in slots[i:] if s<=w1)
    if w1<FIN: sc+=20/max(left,1)
    if left<=1: sc+=1000
    vec=[x for x in [prev]+fixd.get(d-D.timedelta(1),[])+fixd.get(d,[])+fixd.get(d+D.timedelta(1),[]) if x is not None]
    if p['enfoque']=='Comercial' and any(x['enfoque']=='Comercial' for x in vec): sc-=50
    for fd in fixv.get(vid(p),[]):
      g=abs((d-fd).days); ideal=len(dias)/tot['vid'].get(vid(p),1)
      if g<ideal*0.5: sc-=30*(1-g/(ideal*0.5))
    if prev is not None:
      if caso(p)==caso(prev): sc-=3
      if p['formato']==prev['formato']=='Carrusel': sc-=2
      if p['idioma']==prev['idioma']=='Euskera': sc-=5
    v=vid(p)
    if v and v in last:
      gap=(d-last[v]).days; ideal=len(dias)/tot['vid'][v]
      if gap<ideal*0.5: sc-=30*(1-gap/(ideal*0.5))
    if best is None or sc>best[0]: best=(sc,p)
  p=best[1]; rest.remove(p)
  hhmm=fecha(p).strftime('%H:%M')
  res[p['id']]=f"{d.isoformat()}T{hhmm}"
  for a,(f,w) in attrs.items():
    v=f(p)
    if v is not None: placed[a][v]+=1
  if vid(p): last[vid(p)]=d
  prev=p
assert not rest
json.dump(dict(res=res,huecos=sorted(x.isoformat() for x in hue),fijas=[p['id'] for p in fijas]),open(S+'cal/plan.json','w'))
# informe
M=C.defaultdict(lambda:C.Counter())
allp={p['id']:p for p in A}
for pid,f in list(res.items())+[(p['id'],p['fecha_objetivo']) for p in fijas]:
  if f[:10]>FIN.isoformat(): continue
  p=allp[pid]; m=f[:7]; M[m]['total']+=1; M[m][p['area']]+=1; M[m][p['idioma']]+=1; M[m][p['formato']]+=1; M[m][p['enfoque']]+=1
for h in hue: M[h.isoformat()[:7]]['HUECOS']+=1
for m in sorted(M): print(m,dict(M[m]))
print('huecos',len(hue),'fijas',len(fijas),'movidas',len(mov), 'dias',len(dias))
# comprobaciones
seq=sorted([(f,allp[i]) for i,f in res.items()]+[(p['fecha_objetivo'],p) for p in fijas if p['fecha_objetivo'][:10]<=FIN.isoformat()],key=lambda x:x[0])
cc=sum(1 for a,b in zip(seq,seq[1:]) if a[1]['enfoque']==b[1]['enfoque']=='Comercial'); print('comerciales seguidas',cc)
vv=C.defaultdict(list)
for f,p in seq:
  if vid(p): vv[vid(p)].append(f[:10])
mins=[]
for v,l in vv.items():
  ds=[D.date.fromisoformat(x) for x in l]; g=[(b-a).days for a,b in zip(ds,ds[1:])]
  if g: mins.append((min(g),len(l),v[:40]))
print('min separación por vídeo',sorted(mins)[:8])
for p in mov:
  w0,w1=ventana(p); d=D.date.fromisoformat(res[p['id']][:10])
  if not(w0<=d<=w1): print('FUERA VENTANA',p['id'])
fx=set(p['id'] for p in fijas)
for a,b in zip(seq,seq[1:]):
  if a[1]['enfoque']==b[1]['enfoque']=='Comercial': print('CC',a[0],a[1]['id'],'F' if a[1]['id'] in fx else '',b[0],b[1]['id'],'F' if b[1]['id'] in fx else '')
for v,l in vv.items():
  if v.startswith('Óscar Sánchez · SIML') or v.startswith('Jon Ortiz · Está'): print(v[:30],l)
