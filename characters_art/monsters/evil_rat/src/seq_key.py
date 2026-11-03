# generic: concatenate source clips (already in `clips` or src_actions names) with smooth crossfades
# spec: {"key": this, "seq": [[clip_or_action, f0, f1], ...], "blend": 5}
import bpy
bl=spec.get('blend',5)
segs=[]
for (an,s0,s1) in spec['seq']:
    act=clips.get(an) or bpy.data.actions[an]
    segs.append((act,s0,s1))
paths={}
for act,_,_ in segs:
    for fc in act.fcurves: paths.setdefault(fc.data_path,set()).add(fc.array_index)
def ev(act,dp,i,f):
    fc=act.fcurves.find(dp,index=i)
    if fc is None: return 1.0 if (dp.endswith('scale') or (dp.endswith('quaternion') and i==0)) else 0.0
    return fc.evaluate(f)
# timeline: segment k starts at T[k]; overlaps previous by bl
T=[0]; 
for k,(a,s0,s1) in enumerate(segs[:-1]): T.append(T[-1]+(s1-s0)-bl)
end=T[-1]+segs[-1][2]-segs[-1][1]
na=bpy.data.actions.new(cname)
for dp,idx in paths.items():
    idx=sorted(idx)
    fcs=[na.fcurves.new(dp,index=i,action_group=dp.split('"')[1] if '"' in dp else '') for i in idx]
    for f in range(0,int(end)+1):
        k=max(j for j in range(len(segs)) if T[j]<=f)
        a,s0,s1=segs[k]; v=[ev(a,dp,i,s0+f-T[k]) for i in idx]
        if k>0 and f<T[k]+bl:
            p,p0,p1=segs[k-1]; u=[ev(p,dp,i,min(p1,p0+f-T[k-1])) for i in idx]
            w=(f-T[k])/bl; w=w*w*(3-2*w)
            if dp.endswith('quaternion') and sum(x*y for x,y in zip(u,v))<0: v=[-x for x in v]
            v=[x*(1-w)+y*w for x,y in zip(u,v)]
        for fc,x in zip(fcs,v): fc.keyframe_points.insert(f,x,options={'FAST'})
for fc in na.fcurves: fc.update()
print('SEQ',cname,'frames',int(end)+1,'starts',T)
