# Procedural fx ground decals (blood/goo/lava). Shared masks tinted per variant. CC0 (original work).
import numpy as np, json, trimesh
from PIL import Image, ImageFilter
N=512; O='/workspace/sanctuary_art/fx_decals/'; T=O+'textures/'; G=O+'glb/'
y,x=np.mgrid[0:N,0:N]/(N-1)*2-1; R=np.hypot(x,y)
def lf(c,s):
    g=np.random.RandomState(s).rand(c,c); return np.asarray(Image.fromarray((g*255).astype(np.uint8)).resize((N,N),Image.BICUBIC),float)/255
def fbm(s): return 0.5*lf(6,s)+0.3*lf(16,s+1)+0.2*lf(48,s+2)
def blur(a,r): return np.asarray(Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)),float)/255
def metaballs(seed,nb,rad,spread,drops,drip):
    r=np.random.RandomState(seed); f=np.zeros((N,N))
    for i in range(nb):
        cx,cy=r.normal(0,spread,2); rr=r.uniform(*rad); f+=rr*rr/((x-cx)**2+(y-cy)**2+1e-4)
    for i in range(drops):  # droplets, radial spray
        a=r.uniform(0,6.283); d=r.uniform(0.3,0.85); rr=r.uniform(0.006,0.03)
        f+=rr*rr/((x-d*np.cos(a))**2+(y-d*np.sin(a))**2+1e-4)
    for i in range(drip):   # drip/streak trails: line of shrinking balls
        a=r.uniform(0,6.283); L=r.uniform(0.3,0.7); rr=r.uniform(0.02,0.045)
        for t in np.linspace(0.15,L,14):
            f+=(rr*(1-t/L*0.7))**2/((x-t*np.cos(a))**2+(y-t*np.sin(a))**2+1e-4)
    f*=0.85+0.3*fbm(seed+7)  # noisy edges
    m=np.clip((f-1)/0.25,0,1)*np.clip((0.97-R)*12,0,1)
    return blur(m,1.0)
def normal_from(h,s=6):
    gy,gx=np.gradient(h*s); n=np.dstack([-gx,-gy,np.ones_like(h)]); n/=np.linalg.norm(n,axis=2,keepdims=True)
    return ((n*0.5+0.5)*255).astype(np.uint8)
def save(name,col,alpha,rough,height,emis=None):
    Image.fromarray(np.dstack([np.clip(col,0,1)*255,alpha*255]).astype(np.uint8),'RGBA').save(T+name+'_bc.png',optimize=True)
    Image.fromarray(normal_from(height)).save(T+name+'_n.png',optimize=True)
    orm=np.dstack([np.ones_like(rough)*(1-0.3*(1-height)),rough,np.zeros_like(rough)])  # R=AO G=rough B=metal
    Image.fromarray((orm*255).astype(np.uint8)).save(T+name+'_orm.png',optimize=True)
    if emis is not None: Image.fromarray((np.clip(emis,0,1)*255).astype(np.uint8)).save(T+name+'_e.png',optimize=True)
def tint(m,dark,light,s):
    n=fbm(s); k=(0.6*blur(m,6)+0.4*n)[...,None]; return np.array(dark)/255*(1-k)+np.array(light)/255*k
# shared masks
M={'thin_a':metaballs(1,6,(0.04,0.09),0.15,90,5),'thin_b':metaballs(2,8,(0.03,0.08),0.2,120,3),'thin_c':metaballs(3,4,(0.05,0.1),0.1,70,8),
   'thick_a':metaballs(4,14,(0.08,0.15),0.2,25,2),'thick_b':metaballs(5,18,(0.07,0.14),0.25,15,4),
   'pool':metaballs(6,10,(0.16,0.24),0.12,12,0),'goo_a':metaballs(7,12,(0.08,0.15),0.22,40,6),'goo_b':metaballs(8,9,(0.06,0.12),0.2,60,3)}
H={k:blur(v,5)*(0.9+0.1*fbm(20)) for k,v in M.items()}
spec=[]
def mk(name,mk_,dark,light,rgh,em=None,blend='BLEND'):
    m=M[mk_]; h=H[mk_]; col=tint(m,dark,light,hash(name)%100); rough=rgh+0.15*fbm(30)*(1-h)
    e=None
    if em: e=(h**2*fbm(40))[...,None]*np.array(em)/255
    save(name,col,m,rough,h,e); spec.append((name,blend,e is not None))
for s in 'abc': mk('blood_splatter_thin_'+s,'thin_'+s,(70,4,6),(140,12,12),0.25)
mk('blood_splatter_thick_a','thick_a',(40,2,4),(110,8,10),0.15); mk('blood_splatter_thick_b','thick_b',(40,2,4),(110,8,10),0.15)
mk('blood_pool_a','pool',(35,1,3),(95,6,8),0.08)
mk('blackblood_goo_a','goo_a',(8,4,4),(45,10,12),0.1); mk('blackblood_goo_b','goo_b',(10,8,6),(50,20,14),0.12)
mk('green_goo_a','goo_a',(30,60,10),(110,170,30),0.12); mk('green_goo_b','goo_b',(30,60,10),(110,170,30),0.12)
mk('toxic_pool_a','pool',(70,90,15),(180,200,40),0.1,em=(140,190,30))
# lava: voronoi crack crust + glow
def voronoi_edges(seed,n,tile=True):
    r=np.random.RandomState(seed); p=r.rand(n,2); u=np.mgrid[0:N,0:N].transpose(1,2,0)/N
    d=[]
    for ox in (-1,0,1):
        for oy in (-1,0,1):
            q=p+[ox,oy]
            d.append(np.sqrt(((u[:,:,None,:]-q[None,None])**2).sum(-1)))
    d=np.sort(np.concatenate(d,2),2); return d[...,1]-d[...,0]
def lava(seed,mask):
    e=voronoi_edges(seed,40); crack=np.clip(1-e/0.025,0,1)
    core=crack if mask is None else np.clip(crack+np.clip(1-R/0.45,0,1)**1.5*1.2,0,1)
    glow=np.clip(core*(0.7+0.5*fbm(seed+3)),0,1)
    crust=np.array([22,16,14])/255*(0.6+0.8*fbm(seed+5))[...,None]
    hot=np.array([255,90,10])/255*(1-glow[...,None])+np.array([255,220,90])/255*glow[...,None]
    col=crust*(1-glow[...,None])+hot*glow[...,None]; emis=hot*glow[...,None]
    return col,emis,glow,1-glow
m=metaballs(9,10,(0.18,0.25),0.1,0,0); col,emis,g,h=lava(9,m)
save('lava_pool_a',col,m,0.85-0.6*g,h*blur(m,5),emis); spec.append(('lava_pool_a','BLEND',True))
col,emis,g,h=lava(10,None)  # tileable (voronoi wraps; fbm lf is not periodic -> use periodic noise)
def pnoise(c,s): g=np.random.RandomState(s).rand(c,c); g=np.tile(g,(3,3)); im=Image.fromarray((g*255).astype(np.uint8)).resize((N*3,N*3),Image.BICUBIC); return np.asarray(im,float)[N:2*N,N:2*N]/255
e=voronoi_edges(10,40); glow=np.clip(np.clip(1-e/0.03,0,1)*(0.7+0.5*pnoise(8,3)),0,1)
crust=np.array([22,16,14])/255*(0.6+0.8*pnoise(12,5))[...,None]
hot=np.array([255,90,10])/255*(1-glow[...,None])+np.array([255,220,90])/255*glow[...,None]
Image.fromarray((np.clip(crust*(1-glow[...,None])+hot*glow[...,None],0,1)*255).astype(np.uint8)).save(T+'lava_tile_bc.png')
Image.fromarray((np.clip(hot*glow[...,None],0,1)*255).astype(np.uint8)).save(T+'lava_tile_e.png')
Image.fromarray(normal_from(1-glow)).save(T+'lava_tile_n.png')
json.dump(spec,open(O+'src/spec.json','w'))
print('textures ok',len(spec))
