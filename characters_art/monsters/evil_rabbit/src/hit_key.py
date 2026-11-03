# generic hit flinch: base clip (idle) + additive rotations in world axes with an envelope
# spec: {"key": this, "base": "idle", "len": 16, "peak": 3, "rots": [[bone, [ax,ay,az], deg], ...]}
import bpy,mathutils,math
base=clips[spec.get('base','idle')]; L=spec.get('len',16); pk=spec.get('peak',3)
na=bpy.data.actions.new(cname)
def ev(act,dp,i,f):
    fc=act.fcurves.find(dp,index=i)
    if fc is None: return 1.0 if (dp.endswith('scale') or (dp.endswith('quaternion') and i==0)) else 0.0
    return fc.evaluate(f)
rots={}
for bn,ax,deg in spec['rots']:
    b=arm.data.bones[bn]
    la=((arm.matrix_world.to_3x3()@b.matrix_local.to_3x3()).inverted()@mathutils.Vector(ax)).normalized()
    rots[bn]=(la,math.radians(deg))
def env(f):
    if f<=pk: t=f/pk; return t*t*(3-2*t)
    t=min(1,(f-pk)/(L-1-pk)); return 1-t*t*(3-2*t)
paths={}
for fc in base.fcurves: paths.setdefault(fc.data_path,set()).add(fc.array_index)
for bn in rots: paths.setdefault(f'pose.bones["{bn}"].rotation_quaternion',set()).update({0,1,2,3})
for dp,idx in paths.items():
    idx=sorted(idx); fcs=[na.fcurves.new(dp,index=i,action_group=dp.split('"')[1] if '"' in dp else '') for i in idx]
    bn=dp.split('"')[1] if '"' in dp else None
    for f in range(L):
        v=[ev(base,dp,i,f) for i in idx]
        if bn in rots and dp.endswith('rotation_quaternion'):
            la,ang=rots[bn]; q=mathutils.Quaternion(v)@mathutils.Quaternion(la,ang*env(f)); v=list(q)
        for fc,x in zip(fcs,v): fc.keyframe_points.insert(f,x,options={'FAST'})
for fc in na.fcurves: fc.update()
print('HIT',cname,L)
