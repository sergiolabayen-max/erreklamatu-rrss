import json,glob,csv,re,statistics as st,collections
P={}
for f in glob.glob('db/publicaciones/*.json'):
    j=json.load(open(f)); d=j.get('data',j); P[d['id']]=d
pz={r['id']:r for r in csv.DictReader(open('piezas_publicadas.csv'))}
bid2p={}
for i,d in P.items():
    for k,v in list((d.get('buffer_ids') or {}).items())+list((d.get('buffer_ids_retirados') or {}).items() if isinstance(d.get('buffer_ids_retirados'),dict) else []):
        if isinstance(v,str): bid2p[v]=i
url2p={}
def key(u):
    m=re.search(r'instagram\.com/(?:reel|p)/([^/?]+)',u or '');
    if m: return 'ig:'+m.group(1)
    m=re.findall(r'(\d{9,})',u or '')
    return 'fb:'+m[-1] if m else None
for i,d in P.items():
    for k,v in (d.get('urls') or {}).items():
        if k in('instagram','facebook') and v: url2p[key(v)]=i
def sub(i):
    return pz[i]['sub']+(' EU' if pz[i]['idioma']=='Euskera' else '') if i in pz else '?'
out=collections.defaultdict(list)
# buffer
for net in ['x','tiktok','youtube']:
    for p in json.load(open(f'metrics/buffer_{net}.json')):
        i=bid2p.get(p['id']); m=p['metrics']
        v=m.get('impressions') if net=='x' else m.get('views')
        out[net].append(dict(id=i or '?',sub=sub(i) if i else '?',v=v,extra=m,sent=p['sentAt'][:16]))
for net,fn,vi,ui in [('ig_reel','metricool_ig_reels.json',3,2),('ig_post','metricool_ig_posts.json',5,2),('fb_reel','metricool_fb_reels.json',3,2),('fb_post','metricool_fb_posts.json',4,2)]:
    D=json.load(open('metrics/'+fn)); flds=[x['fieldId'] for x in D['fields']]
    for r in D['rows']:
        i=url2p.get(key(r[ui]))
        out[net].append(dict(id=i or '?',sub=sub(i) if i else '?',v=float(r[vi] or 0),extra=dict(zip(flds,r)),sent=r[0]))
json.dump(out,open('joined.json','w'),ensure_ascii=False)
for net,L in out.items():
    print('\n==',net,'n=',len(L),'sin casar',sum(1 for x in L if x['id']=='?'))
    g=collections.defaultdict(list)
    for x in L: g[x['sub']].append(x['v'] or 0)
    for s,vals in sorted(g.items(),key=lambda t:-st.median(t[1])):
        print(f"  {s:18} n={len(vals):2} mediana={st.median(vals):7.0f} media={st.mean(vals):7.0f} max={max(vals):6.0f}")
