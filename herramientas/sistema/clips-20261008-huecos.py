import json,sys,re
S='/tmp/claude-0/-home-claude-erreklamatu-rrss/e7eefa61-a30f-57c7-bc2e-7996fd2458cc/scratchpad'
sys.path.insert(0,S+'/m9'); import defs
mapa=json.load(open(S+'/aud/mapa.json')); inv={v:k for k,v in mapa.items()}
cob=json.load(open(S+'/fp/cobertura.json'))['fuentes']
k2s={'a14':'s17','a3':'s18','a11':'s19','v2':'s14','v3':'s15','v4':'s16','inf':'s20','qa':'s13'}
extra={}
for v,pid,k,tit,tramos,op in defs.C:
    if v not in k2s: continue
    for t in tramos: extra.setdefault(k2s[v],[]).append((t[0],t[1],pid))
out={}
for src,o in cob.items():
    s=inv[src]; hs=[list(h) for h in o['huecos']]
    for a,b,pid in extra.get(s,[]):
        nh=[]
        for h0,h1 in hs:
            if b<=h0 or a>=h1: nh.append([h0,h1]); continue
            if a-h0>0.3: nh.append([h0,a])
            if h1-b>0.3: nh.append([b,h1])
        hs=nh
    out[s]=dict(src=src,dur=o['dur'],huecos=[[round(a,1),round(b,1)] for a,b in hs])
json.dump(out,open('huecos.json','w'),ensure_ascii=False,indent=1)
def segs(s):
    r=[]
    for l in open(f'{S}/aud/{s}.txt'):
        m=re.match(r'\[\s*([\d.]+)-\s*([\d.]+)\] (.*)',l)
        if m: r.append((float(m.group(1)),float(m.group(2)),m.group(3)))
    return r
tot=0
for s in sorted(out):
    o=out[s]; sg=segs(s)
    print(f"\n######## {s} {o['src'][:70]} ({o['dur']} s)")
    for a,b in o['huecos']:
        t=[x for x in sg if x[1]>a-0.5 and x[0]<b+0.5]
        habla=sum(min(x[1],b)-max(x[0],a) for x in t if min(x[1],b)>max(x[0],a))
        tot+=b-a
        print(f"  -- hueco {a}-{b} ({b-a:.0f} s; voz {habla:.0f} s)")
        for x in t: print(f"     [{x[0]:.1f}-{x[1]:.1f}] {x[2]}")
print('TOTAL',round(tot))
