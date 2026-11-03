# attack2 = charge: N gallop cycles blending into the gore (attack)
run=clips['run']; att=clips['attack']
rl=run.frame_range[1]-run.frame_range[0]; al=att.frame_range[1]
ncyc=spec.get('cycles',2); bl=spec.get('blend',6)
start=int(round(ncyc*rl))-bl
end=int(round(start+al))
na=bpy.data.actions.new(cname)
paths={}
for fc in list(run.fcurves)+list(att.fcurves): paths.setdefault(fc.data_path,set()).add(fc.array_index)
def ev(act,dp,i,f):
    fc=act.fcurves.find(dp,index=i)
    if fc is None: return 1.0 if (dp.endswith('scale') or (dp.endswith('quaternion') and i==0)) else 0.0
    return fc.evaluate(f)
for dp,idx in paths.items():
    idx=sorted(idx)
    fcs=[na.fcurves.new(dp,index=i,action_group=dp.split('"')[1] if '"' in dp else '') for i in idx]
    for f in range(0,end+1):
        a=[ev(run,dp,i,run.frame_range[0]+(f%rl)) for i in idx]
        b=[ev(att,dp,i,max(0,f-start)) for i in idx]
        if f<=start: v=a
        elif f>=start+bl: v=b
        else:
            w=(f-start)/bl; w=w*w*(3-2*w)
            if dp.endswith('quaternion') and sum(x*y for x,y in zip(a,b))<0: b=[-x for x in b]
            v=[x*(1-w)+y*w for x,y in zip(a,b)]
        for fc,x in zip(fcs,v): fc.keyframe_points.insert(f,x,options={'FAST'})
for fc in na.fcurves: fc.update()
print('CHARGE frames',end+1,'gore starts',start)
