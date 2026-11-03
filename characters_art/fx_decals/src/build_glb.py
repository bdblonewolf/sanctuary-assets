import numpy as np, json, trimesh
from PIL import Image
from trimesh.visual.material import PBRMaterial
O='/workspace/sanctuary_art/fx_decals/'; T=O+'textures/'
def mat(n,blend,em,rough):
    I=lambda s:Image.open(T+f'{n}_{s}.png')
    kw=dict(name='m_'+n,baseColorTexture=I('bc'),normalTexture=I('n'),metallicRoughnessTexture=I('orm'),
            metallicFactor=0.0,roughnessFactor=rough,alphaMode=blend,doubleSided=False)
    if em: kw.update(emissiveTexture=I('e'),emissiveFactor=[1,1,1])
    return PBRMaterial(**kw)
uvq=np.array([[0,1],[1,1],[1,0],[0,0]],float)
for n,blend,em in json.load(open(O+'src/spec.json')):
    s=0.75 if 'thin' in n else 1.0  # 1.5m / 2m
    v=np.array([[-s,0.01,s],[s,0.01,s],[s,0.01,-s],[-s,0.01,-s]])
    m=trimesh.Trimesh(v,[[0,1,2],[0,2,3]],process=False)
    m.visual=trimesh.visual.TextureVisuals(uv=uvq,material=mat(n,blend,em,1.0))
    m.export(O+f'glb/{n}.glb')
# lava pool: irregular sunken disc, rings x segments
r=np.random.RandomState(3); S=32; rings=[0,0.35,0.65,0.85,1.0,1.15]; depth=[-0.08,-0.08,-0.07,-0.05,0.0,0.01]
rad=1.0+0.15*np.sin(np.linspace(0,6.283,S,endpoint=False)*3+1)+r.uniform(-0.06,0.06,S)
V=[[0,depth[0],0]];UV=[[0.5,0.5]]
for ri in range(1,len(rings)):
    for j in range(S):
        a=j/S*6.283; rr=rings[ri]*rad[j]*0.9; V.append([rr*np.cos(a),depth[ri],rr*np.sin(a)]); UV.append([0.5+rr*np.cos(a)/2.3,0.5-rr*np.sin(a)/2.3])
F=[]
for j in range(S): F.append([0,1+(j+1)%S,1+j])
for ri in range(1,len(rings)-1):
    b0=1+(ri-1)*S;b1=1+ri*S
    for j in range(S):
        k=(j+1)%S; F+= [[b0+j,b0+k,b1+j],[b0+k,b1+k,b1+j]]
m=trimesh.Trimesh(np.array(V),np.array(F),process=False)
if m.face_normals[:,1].mean()<0: m.invert()
m.visual=trimesh.visual.TextureVisuals(uv=np.array(UV),material=mat('lava_pool_a','MASK',True,1.0))
m.export(O+'glb/lava_pool_a.glb'); print('lava tris',len(F))
