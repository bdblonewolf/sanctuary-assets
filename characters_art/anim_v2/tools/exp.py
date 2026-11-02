import pygltflib, numpy as np, struct
from gl import acc
def export(body_sk, clips, out, extra_q=None):
    """clips: list of (name, times(F), L(F,J,4), hips(F,3) or None, joints subset idx list or None)"""
    g0=body_sk.g; sk=body_sk
    g=pygltflib.GLTF2(); g.asset=pygltflib.Asset(version='2.0',generator='sanctuary anim_v2 (Blender 4.2 + numpy)')
    blob=bytearray()
    def add(arr,type_,minmax=False):
        arr=np.ascontiguousarray(arr,dtype=np.float32)
        while len(blob)%4: blob.append(0)
        off=len(blob); blob.extend(arr.tobytes())
        g.bufferViews.append(pygltflib.BufferView(buffer=0,byteOffset=off,byteLength=arr.nbytes))
        a=pygltflib.Accessor(bufferView=len(g.bufferViews)-1,componentType=5126,count=arr.shape[0],type=type_)
        if minmax: a.min=[float(arr.min())]; a.max=[float(arr.max())]
        g.accessors.append(a); return len(g.accessors)-1
    # nodes: root + joints
    J=len(sk.joints); nodes=[]
    rootname=g0.nodes[sk.rootnode].name if sk.rootnode is not None else 'Armature'
    nodes.append(pygltflib.Node(name=rootname,children=[1+sk.par.index(-1)]))
    for j in range(J):
        n0=g0.nodes[sk.joints[j]]
        n=pygltflib.Node(name=n0.name,translation=list(map(float,sk.T[j])),rotation=list(map(float,sk.Q[j])),
                         children=[1+c for c in sk.children[j]] or None)
        if np.abs(sk.S[j]-1).max()>1e-6: n.scale=list(map(float,sk.S[j]))
        nodes.append(n)
    g.nodes=nodes
    ibm=acc(g0,g0.skins[0].inverseBindMatrices) if g0.skins[0].inverseBindMatrices is not None else None
    sk_=pygltflib.Skin(joints=list(range(1,J+1)),skeleton=1,name='armature')
    if ibm is not None:
        a=add(ibm,'MAT4'); sk_.inverseBindMatrices=a
    g.skins=[sk_]
    g.scenes=[pygltflib.Scene(nodes=[0])]; g.scene=0
    hips=1+sk.par.index(-1)
    for name,ts,L,H,sub in clips:
        an=pygltflib.Animation(name=name,channels=[],samplers=[])
        ti=add(np.asarray(ts)[:,None],'SCALAR',True)
        js=range(J) if sub is None else sub
        for j in js:
            q=L[:,j].copy()
            for k in range(1,len(q)):
                if np.dot(q[k],q[k-1])<0: q[k]=-q[k]
            oi=add(q,'VEC4')
            an.samplers.append(pygltflib.AnimationSampler(input=ti,output=oi,interpolation='LINEAR'))
            an.channels.append(pygltflib.AnimationChannel(sampler=len(an.samplers)-1,target=pygltflib.AnimationChannelTarget(node=1+j,path='rotation')))
        if H is not None:
            oi=add(H,'VEC3')
            an.samplers.append(pygltflib.AnimationSampler(input=ti,output=oi,interpolation='LINEAR'))
            an.channels.append(pygltflib.AnimationChannel(sampler=len(an.samplers)-1,target=pygltflib.AnimationChannelTarget(node=hips,path='translation')))
        g.animations.append(an)
    while len(blob)%4: blob.append(0)
    g.buffers=[pygltflib.Buffer(byteLength=len(blob))]
    g.set_binary_blob(bytes(blob)); g.save_binary(out)
