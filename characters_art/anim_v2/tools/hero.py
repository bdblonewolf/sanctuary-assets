from rt import *; from trans import *; from exp import export
import json, os
A='/workspace/sanctuary-assets/'; OUT=A+'characters_art/anim_v2/'
K=Body(A+'models/knight_anim_v10b.glb','knight')
if K.thigh_r is None or K.thigh_r<0.04 or K.thigh_r>0.2: K.thigh_r=0.10
print('knight',K.info())
W=Body(A+'characters_art/npcs/martsirt/wolcen.glb','wolcen',A+'characters_art/bodies/male_brute_heavy.glb')
names=[a.name for a in K.sk.g.animations]
LOWER=('Hips','LeftUpLeg','LeftLeg','LeftFoot','LeftToeBase','LeftToe_End','RightUpLeg','RightLeg','RightFoot','RightToeBase','RightToe_End')
upper_idx=[j for j,n in enumerate(K.sk.names) if n[len(M):] not in LOWER]
clips=[]; info={}
def kclip(n):
    ts,Q,T,_=K.sk.clip(n); return ts,Q,T[:,K.i('Hips')].copy()
for n in names:
    if n.endswith('_draw') or n.endswith('_sheath') or n=='bow_equip':
        ts,Q,h=kclip(n); clips.append((n+'__up',ts,Q,None,upper_idx)); info[n+'__up']=round(float(ts[-1]),3)
# gs_sheath = reversed gs_draw
ts,Q,h=kclip('gs_draw'); Qr=Q[::-1].copy(); hr=h[::-1].copy()
clips.append(('gs_sheath',ts,Qr,hr,None)); clips.append(('gs_sheath__up',ts,Qr,None,upper_idx)); info['gs_sheath']=info['gs_sheath__up']=round(float(ts[-1]),3)
# gs_walk: legs+hips from ss_walk, spine from ss_walk, shoulders/arms/hands from gs_idle (held pose, looped)
tw,Qw,hw=kclip('ss_walk'); tg,Qg,hg=kclip('gs_idle')
Qgw=np.stack([Qg[int(round((t%tg[-1])*FPS))%len(Qg)] for t in tw])
Qn=Qw.copy()
for j,n in enumerate(K.sk.names):
    b=n[len(M):]
    if any(b.startswith(p) for p in ('LeftShoulder','LeftArm','LeftForeArm','LeftHand','RightShoulder','RightArm','RightForeArm','RightHand')): Qn[:,j]=Qgw[:,j]
clips.append(('gs_walk',tw,Qn,hw,None)); info['gs_walk']=round(float(tw[-1]),3)
# sit set from wolcen sit onto knight
ts,Q,T,_=W.sk.clip('sit'); Ls,hs=retarget(W,K,Q,T); Ls,hs,dy=seat_fix(K,Ls,hs)
ti,Li,hi=kclip('town_idle'); hi=ground_standing(K,Li,hi,9)
t,L,h,dz=sit_down(K,Li,hi,Ls,hs); clips.append(('sit_down',t,L,h,None))
clips.append(('sit',ts,Ls,hs,None))
t2,L2,h2,_=stand_up(K,Li,hi,Ls,hs); clips.append(('stand_up',t2,L2,h2,None))
ts2,Q2,T2,_=W.sk.clip('sit_talk'); Lt,ht=retarget(W,K,Q2,T2); Lt,ht,_=seat_fix(K,Lt,ht); clips.append(('sit_talk',ts2,Lt,ht,None))
val={}
for c in clips:
    if c[0] in ('sit_down','sit','stand_up','sit_talk','gs_walk'):
        GQ,GP=fk(K,c[2],c[3]); cc,_=contact(K,GP)
        up=np.minimum(GP[:,K.i('LeftUpLeg'),1],GP[:,K.i('RightUpLeg'),1])-K.thigh_r
        val[c[0]]=dict(dur=round(float(c[1][-1]),3),foot_contact_cm=[round(float(cc.min()*100),2),round(float(cc.max()*100),2)],seat_underside_y_end=round(float(up[-1]),3))
        info[c[0]]=round(float(c[1][-1]),3)
export(K.sk,clips,OUT+'hero_extra.glb')
res=dict(file='hero_extra.glb',bytes=os.path.getsize(OUT+'hero_extra.glb'),clips=info,stand_offset_m=round(dz,3),seat_height_m=SEAT,knight=K.info(),validation=val)
json.dump(res,open('/workspace/animv2/hero.json','w'),indent=1,default=float); print(json.dumps(res,indent=1,default=float))
