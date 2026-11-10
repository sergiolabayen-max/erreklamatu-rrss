# python3 ctx.py s14 60 126 [s15 0 52 ...]  -> transcripción de ese tramo y piezas que ya lo usan
import json,sys,re
S='/tmp/claude-0/-home-claude-erreklamatu-rrss/e7eefa61-a30f-57c7-bc2e-7996fd2458cc/scratchpad'
sys.path.insert(0,S+'/m9'); import defs
mapa=json.load(open(S+'/aud/mapa.json'))
cob=json.load(open(S+'/fp/cobertura.json'))['piezas']
k2s={'a14':'s17','a3':'s18','a11':'s19','v2':'s14','v3':'s15','v4':'s16','inf':'s20','qa':'s13'}
use={}
for pid,o in cob.items():
    s=[k for k,v in mapa.items() if v==o['src']][0]
    for a,b in o['tramos']: use.setdefault(s,[]).append((a,b,pid))
for v,pid,k,tit,tramos,op in defs.C:
    if v in k2s:
        for t in tramos: use.setdefault(k2s[v],[]).append((t[0],t[1],pid))
est={}
import glob
for f in glob.glob(S+'/p4/publicaciones/*.json'):
    d=json.load(open(f)); est[d['id']]=d['estado'][:4]
A=sys.argv[1:]
for i in range(0,len(A),3):
    s,a,b=A[i],float(A[i+1]),float(A[i+2])
    print(f'#### {s} {a}-{b}')
    u=sorted((x for x in use.get(s,[]) if x[1]>a and x[0]<b))
    print('   usan:',' '.join(f'{p}({est.get(p,"?")}){x:.0f}-{y:.0f}' for x,y,p in u))
    for l in open(f'{S}/aud/{s}.txt'):
        m=re.match(r'\[\s*([\d.]+)-\s*([\d.]+)\] (.*)',l)
        if m and float(m.group(2))>a and float(m.group(1))<b: print(f'   [{float(m.group(1)):.1f}-{float(m.group(2)):.1f}] {m.group(3)}')
