import json,copy
WV='/workspace/sanctuary_env/world_v1/exits/work/'
AUD=json.load(open('/workspace/sanctuary/design/audit/worlds.json'))
EXTF=json.load(open('/workspace/sanctuary_art/maps/extract/world_extract.json'))
F=json.load(open('world_full.json')); QN={v:k for k,v in F['U'].items()}; U=EXTF['U']
A2=copy.deepcopy(AUD)
def setex(z,to,**kw):
    e=next(q for q in A2[z]['exits'] if q['to']==to); e.update(kw)
mp=json.load(open('out/martsirt_exits_patch.json'))['exits_set'][0]['new']
setex('town','coast',x=mp['x'],y=mp['y'],sx=mp['sx'],sy=mp['sy'])
for z in ['coast','wild','desert','mires','briarE','lut','sink']:
    p=json.load(open('out/%s_exits_patch.json'%z))
    for s in p['exits_set']:
        setex(z,s['match']['to'],**{k:v for k,v in s['new'].items() if k in('x','y','sx','sy')})
json.dump(A2,open('v2in/worlds_v2.json','w'))
E2=copy.deepcopy(EXTF)
for z in ['wild','desert','mires']:
    a=json.load(open('after_%s.json'%z)); e=E2['worlds'][z]; old=F['worlds'][z]['tiles']
    # only the tiles the patch changed are remapped (keeps extract-vs-live differences elsewhere untouched)
    for i,(o,n) in enumerate(zip(old,a['tiles'])):
        if o!=n: e['tiles'][i]=U[QN[n]]
    e['exits']=a['exits']; e['props']=a['props']
json.dump(E2,open('v2in/world_extract_v2.json','w'))
json.dump(json.load(open('after_coast.json')),open('v2in/coast_world_after_v2.json','w'))
print({z:[(e['to'],e['x'],e['y'],e.get('sx'),e.get('sy')) for e in A2[z]['exits'] if e['to'] in('coast','town','briarE','wild','lut','desert','sink','mires')] for z in ['town','coast','wild','briarE','desert','lut','mires','sink']})
