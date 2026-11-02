from rt import *; from trans import *; from exp import export
import json, os, sys
A='/workspace/sanctuary-assets/characters_art/'; OUT=A+'anim_v2/'; os.makedirs(OUT,exist_ok=True)
W=Body(A+'npcs/martsirt/wolcen.glb','wolcen',A+'bodies/male_brute_heavy.glb'); Qs=Body(A+'npcs/martsirt/quill.glb','quill',A+'bodies/male_skinny.glb')
SRC={'wolcen':W,'quill':Qs}
bodies={n[:-4]:A+'bodies/'+n for n in sorted(os.listdir(A+'bodies'))}
bodies['ayla_phimn']=A+'npcs/ayla_phimn/ayla_phimn_body.glb'
def pick(n): return 'wolcen' if n in ('male_brute_heavy','male_brute_muscular','male_regular','male_vshape') else 'quill'
only=sys.argv[1:]
manifest={}
TARGET_SPEED=1.2
for bn,path in bodies.items():
    if only and bn not in only: continue
    b=Body(path,bn); src=SRC[pick(bn)]
    clips={}; info=dict(source_clips=src.name,**{k:float(v) if v is not None else None for k,v in b.info().items()})
    for c in ['idle','walk','talk','sit','sit_talk','sleep']:
        ts,Q,T,_=src.sk.clip(c)
        L,h=retarget(src,b,Q,T)
        if c in ('idle','walk','talk'): h=ground_standing(b,L,h,3 if c=='walk' else 9)
        else:
            if c=='sit': L,h,dy=seat_fix(b,L,h)
            else:
                # same hip shift as sit for continuity
                L,h,_=seat_fix(b,L,h)
        clips[c]=(ts,L,h)
    # loop-close: make last frame equal first for looping clips
    ts,L,h=clips['walk']; v=walk_speed(b,L,h,ts)
    info['walk_natural_speed_mps']=round(v,3); info['walk_natural_cycle_s']=round(float(ts[-1]),3)
    clips['walk_natural']=clips['walk']
    nd=ts[-1]*v/TARGET_SPEED
    clips['walk']=resample(L,h,ts,nd); info['walk_cycle_s']=round(float(nd),3); info['walk_speed_mps']=TARGET_SPEED
    tsw,Lw,hw=clips['walk']; info['walk_speed_check_mps']=round(walk_speed(b,Lw,hw,tsw),3)
    Li,hi=clips['idle'][1],clips['idle'][2]; Ls,hs=clips['sit'][1],clips['sit'][2]; Lz,hz=clips['sleep'][1],clips['sleep'][2]
    t,L,h,dz=sit_down(b,Li,hi,Ls,hs); clips['sit_down']=(t,L,h)
    t,L,h,_=stand_up(b,Li,hi,Ls,hs); clips['stand_up']=(t,L,h)
    clips['sit_to_sleep']=pose_blend(b,Ls,hs,Lz,hz,1.4)
    clips['sleep_to_sit']=pose_blend(b,Lz,hz,Ls,hs,1.0)
    info['stand_offset_m']=round(dz,3); info['seat_height_m']=SEAT
    # validation
    val={}
    for c,(t,L,h) in clips.items():
        GQ,GP=fk(b,L,h); cc,_=contact(b,GP)
        up=np.minimum(GP[:,b.i('LeftUpLeg'),1],GP[:,b.i('RightUpLeg'),1])-b.thigh_r
        val[c]=dict(frames=len(t),dur=round(float(t[-1]),3),foot_contact_min_cm=round(float(cc.min()*100),2),foot_contact_max_cm=round(float(cc.max()*100),2),
                    hips_y=[round(float(h[:,1].min()),3),round(float(h[:,1].max()),3)],
                    seat_underside_y=round(float(up[-1]),3) if c in('sit','sit_talk','sleep','sit_down') else None,
                    head_y=round(float(GP[:,b.i('Head'),1].mean()),3))
    info['validation']=val
    order=['idle','walk','walk_natural','talk','sit','sit_talk','sleep','sit_down','stand_up','sit_to_sleep','sleep_to_sit']
    export(b.sk,[(c,)+clips[c]+(None,) for c in order],OUT+'clips_%s.glb'%bn)
    info['file']='clips_%s.glb'%bn; info['bytes']=os.path.getsize(OUT+info['file'])
    manifest[bn]=info
    print(bn,json.dumps({k:v for k,v in info.items() if k!='validation'}))
    for c,v in val.items(): print('   ',c,v)
json.dump(manifest,open('/workspace/animv2/bodies_%s.json'%('_'.join(only) or 'all'),'w'),indent=1)
