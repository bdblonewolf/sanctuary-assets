# throw_1h: overhand one-hand javelin throw, 31 f @30fps, release f14. Base = Mixamo sword-and-shield idle (static frame),
# hand-keyed torso/hip layers + aimed arm directions (world space; character faces -Y, its right side is -X).
exec(open('/workspace/sanctuary_art/monsters/humanoid_v2/foot_clamp.py').read())
N=31; REL=14
base0=retarget('Sword and Shield Pack/sword and shield idle.fbx',[1.0])[0]
base=[base0]*N
spec={'rot':{
  'Hips':[[0,0,0,0],[3,0,0,0],[10,0,0,-6],[12,0,0,-4],[REL,0,0,22],[18,0,0,28],[22,0,0,22],[N-1,0,0,0]],
  'Spine':[[0,0,0,0],[3,0,0,0],[10,-6,0,-7],[12,-5,0,-5],[REL,6,0,11],[18,10,0,13],[22,8,0,9],[N-1,0,0,0]],
  'Spine1':[[0,0,0,0],[3,0,0,0],[10,-5,0,-7],[12,-4,0,-5],[REL,6,0,11],[18,9,0,12],[22,7,0,8],[N-1,0,0,0]],
  'Spine2':[[0,0,0,0],[3,0,0,0],[10,-4,0,-6],[12,-3,0,-4],[REL,5,0,10],[18,7,0,10],[22,5,0,7],[N-1,0,0,0]],
  'Head':[[0,0,0,0],[10,6,0,22],[12,5,0,18],[REL,-6,0,-40],[18,-8,0,-44],[22,-5,0,-30],[N-1,0,0,0]]},
 'hip':[[0,0,0,0],[4,0,0.01,-0.01],[10,0,0.07,-0.03],[12,0,0.06,-0.03],[REL,0,-0.05,-0.02],[18,0,-0.09,-0.05],[22,0,-0.07,-0.04],[N-1,0,0,0]]}
ov=overlay_from(spec)
# arm direction keys: [frame, upperarm dir, forearm dir] ; None = keep base
RA=[[0,None,None],[3,None,None],[10,(-0.75,0.55,0.35),(-0.15,0.55,0.82)],[12,(-0.7,0.45,0.55),(-0.05,0.25,0.97)],
    [REL,(-0.3,-0.7,0.65),(-0.1,-0.9,0.42)],[18,(0.05,-0.8,-0.45),(0.35,-0.65,-0.6)],[22,(-0.1,-0.5,-0.85),(0.1,-0.6,-0.8)],[N-1,None,None]]
LA=[[0,None,None],[3,None,None],[10,(0.35,-0.88,0.3),(0.15,-0.97,0.2)],[12,(0.35,-0.88,0.3),(0.15,-0.97,0.2)],
    [REL,(0.55,0.15,-0.82),(0.2,-0.55,-0.8)],[18,(0.5,0.25,-0.83),(0.25,-0.4,-0.88)],[N-1,None,None]]
def bdir_w(n):
    pb=arm.pose.bones[P+n]; return ((kw@pb.tail)-(kw@pb.head)).normalized()
def aim(n,d):
    pb=arm.pose.bones[P+n]; cur=bdir_w(n); q=cur.rotation_difference(Vector(d).normalized())
    h=pb.head.copy(); R=(kwi.to_3x3()@q.to_matrix()@kw.to_3x3()).normalized().to_4x4()
    pb.matrix=Matrix.Translation(h)@R@Matrix.Translation(-h)@pb.matrix; bpy.context.view_layer.update()
def arm_layer(keys,up,fo,i):
    # find segment, blend between base (None) and target dirs
    cu=bdir_w(up); 
    def dirat(k,which):
        v=k[1+which]; return Vector(v).normalized() if v else None
    for a,b in zip(keys,keys[1:]):
        if a[0]<=i<=b[0]:
            t=smooth((i-a[0])/(b[0]-a[0])) if b[0]>a[0] else 1
            for w,bn in ((0,up),(1,fo)):
                cur=bdir_w(bn); da=dirat(a,w) or cur; db=dirat(b,w) or cur
                d=da.slerp(db,t) if hasattr(da,'slerp') else da.lerp(db,t)
                aim(bn,d.normalized())
            return
clamp=None
def post(i,n):
    arm_layer(RA,'RightArm','RightForeArm',i); arm_layer(LA,'LeftArm','LeftForeArm',i)
    clamp(i,n)
clamp=make_foot_clamp(base0)
bake('throw_1h',base,overlay=ov,post=post)
REPORT['_new_clips']=['throw_1h']
rep=clip_report('throw_1h') if False else None
# measure hand speed for the release frame and lowest vertex
mute_all(); act=bpy.data.actions['throw_1h']; arm.animation_data.action=act; rows=[]
for i in range(N):
    sc.frame_set(i+1); bpy.context.view_layer.update(); rows.append((kw@arm.pose.bones[P+'RightHand'].head).copy())
sp=[0]+[(rows[i]-rows[i-1]).length*30 for i in range(1,N)]
arm.animation_data.action=None
REPORT['throw_1h']={'frames':N,'duration_s':round(N/30,3),'windup_peak_frame':12,'release_frame':REL,'follow_through_end':22,
  'right_hand_speed_mps':[round(x,2) for x in sp],'peak_hand_speed_frame':int(max(range(N),key=lambda i:sp[i])),
  'hand_z_at_release':round(rows[REL].z,3),'source':'hand-keyed (no free throw clip in the packs) over Mixamo sword and shield idle pose'}
print('REP',REPORT['throw_1h'])
