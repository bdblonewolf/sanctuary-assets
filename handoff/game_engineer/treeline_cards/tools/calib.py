import json,subprocess,glob,numpy as np,os
from PIL import Image
def s2l(x): x=x/255.0; return np.where(x<=0.04045,x/12.92,((x+0.055)/1.055)**2.4)
sky=np.array([0x9f,0xb3,0xc4])
PRE=['/workspace/sanctuary-assets/models/border_kit_v1/bk_'+k+'.glb' for k in ['forest_summer','forest_autumn','forest_winter','forest_dead','town_summer','town_dead']]
PRR=['/workspace/sanctuary-assets/models/outdoor/v5_maps/rect/backdrop_near_rect_'+k+'.glb' for k in ['weald_summer','weald_autumn','weald_winter','ascent_summer']]
def keyof(n):
    s=n.split('_')
    season=[x for x in s if x in ('summer','autumn','winter','dead')][0]
    kind='kit' if n.startswith('bk_') else 'ring'
    return kind+'_'+season
def run():
    subprocess.run('python3 paint.py >/dev/null',shell=True,check=True)
    subprocess.run(['python3','build_cards.py','calib_out/border_kit_v1']+PRE,check=True,capture_output=True)
    subprocess.run(['python3','build_cards.py','calib_out/rect']+PRR,check=True,capture_output=True)
    jobs=[j for j in json.load(open('/tmp/jobs.json'))]
    for j in jobs: j[0]=j[0].replace('/out_all/','/calib_out/')+'&only=trees'; j[1]=j[1].replace('shots/','calib_shots/')
    if not os.path.exists('calib_shots/weald_summer_ring_eye_before.png'):
        subprocess.run(['node','r/shot.js',json.dumps([j for j in jobs if '_before' in j[1]])],check=True,capture_output=True)
    subprocess.run(['node','r/shot.js',json.dumps([j for j in jobs if '_after' in j[1]])],check=True,capture_output=True)
    R={}
    for b in sorted(glob.glob('calib_shots/*_before.png')):
        n=b.split('/')[-1][:-11]
        if n in ('kit','ring'): continue
        a='calib_shots/'+n+'_after.png'
        A=np.asarray(Image.open(b).convert('RGB')).astype(float); B=np.asarray(Image.open(a).convert('RGB')).astype(float)
        ma=(np.abs(A-sky).sum(-1)>40); mb=(np.abs(B-sky).sum(-1)>40)
        la=(s2l(A)@[0.2126,0.7152,0.0722])[ma]; lb=(s2l(B)@[0.2126,0.7152,0.0722])[mb]
        R[n]=(lb.mean()/la.mean(), np.percentile(lb,5)/max(np.percentile(la,5),1e-5))
    return R
os.makedirs('calib_out/border_kit_v1',exist_ok=True); os.makedirs('calib_out/rect',exist_ok=True); os.makedirs('calib_shots',exist_ok=True)
G=json.load(open('render_gain.json')) if os.path.exists('render_gain.json') else {}
for it in range(int(os.environ.get('IT','4'))):
    R=run()
    per={}
    for n,(mr,p5) in R.items(): per.setdefault(keyof(n),[]).append(mr)
    print('iter',it,{k:round(max(v),2) for k,v in per.items()}, flush=True)
    for n,(mr,p5) in sorted(R.items()): print('   ',n,round(mr,2),'p5',round(p5,2))
    done=True
    for k,v in per.items():
        mx=max(v)
        if mx>0.97 or mx<0.85:
            G[k]=G.get(k,1.0)*0.92/mx; done=False
    json.dump(G,open('render_gain.json','w'),indent=1)
    if done: break
print(G)
