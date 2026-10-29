import json,datetime as D,collections as C,glob
S='/tmp/claude-0/-home-claude-erreklamatu-rrss/e7eefa61-a30f-57c7-bc2e-7996fd2458cc/scratchpad/'
pl=json.load(open(S+'cal/plan.json'))
P={}
for f in glob.glob(S+'cal1240/publicaciones/*.json'):
  x=json.load(open(f)); P[x['id']]=x
FR={'Mañana':('09',[12,24,37,48,5,52]),'Mediodía':('13',[8,21,33,46,14,39]),'Tarde':('18',[6,19,31,43,27,52]),'Noche':('21',[4,17,28,41,11,35])}
dpid={v[:10]:p for p,v in pl['res'].items()}
dias=sorted(set(list(dpid)+pl['huecos']))
cnt=C.Counter(); out={}; hu={}; prevf=None; use=C.Counter()
for d in dias:
  wd=D.date.fromisoformat(d).weekday(); pid=dpid.get(d); p=P.get(pid)
  def cost(f):
    c=3*cnt[(f,'wd',wd)]+2*cnt[(f,)]
    if p: c+=cnt[(f,'fmt',p['formato'])]+cnt[(f,'area',p['area'])]+cnt[(f,'id',p['idioma'])]
    if f==prevf: c+=2
    return c
  f=min(FR,key=lambda f:(cost(f),list(FR).index(f)))
  h,mins=FR[f]; m=mins[use[f]%len(mins)]; use[f]+=1
  t=f"{d}T{h}:{m:02d}"; prevf=f
  cnt[(f,'wd',wd)]+=1; cnt[(f,)]+=1
  if p:
    for k,v in (('fmt',p['formato']),('area',p['area']),('id',p['idioma'])): cnt[(f,k,v)]+=1
    out[pid]=(t,f)
  else: hu[d]=(t,f)
print({k:v for k,v in cnt.items() if len(k)==1})
print(sorted((k[0],k[2],v) for k,v in cnt.items() if len(k)==3 and k[1]=='wd'))
print(sorted((k[0],k[2],v) for k,v in cnt.items() if len(k)==3 and k[1] in('fmt','area','id')))
json.dump(dict(res=out,huecos=hu),open(S+'cal/plan_horas.json','w'),ensure_ascii=False)
