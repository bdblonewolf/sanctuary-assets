# procedural gore atlas 512: u<0.75 flesh disc (radial), u>=0.75 bone strip (top 20% marrow); blood decal overlay from fx_decals
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, sobel
rng=np.random.default_rng(7); N=512
def fbm(sh,oct=5,seed=0):
    r=np.random.default_rng(seed); o=np.zeros(sh)
    for i in range(oct):
        s=2**i; n=r.random((sh[0]//(64//min(s,32))+2, sh[1]//(64//min(s,32))+2))
        n=np.array(Image.fromarray((n*255).astype(np.uint8)).resize((sh[1],sh[0]),Image.BICUBIC))/255.
        o+=n/(s**0.7)
    o-=o.min(); return o/o.max()
y,x=np.mgrid[0:N,0:N]/N
bc=np.zeros((N,N,3)); h=np.zeros((N,N)); rough=np.zeros((N,N)); ao=np.ones((N,N))
# flesh region: centre (0.375,0.5), radius in u 0.36, v 0.48
u=(x-0.375)/0.36; v=(y-0.5)/0.48; r=np.sqrt(u*u+v*v)
n1=fbm((N,N),6,1); n2=fbm((N,N),6,2); fib=gaussian_filter(rng.random((N,N)),(0.6,3.0)); fib=(fib-fib.min())/(fib.max()-fib.min())
lump=gaussian_filter(rng.random((N,N)),2.5); lump=(lump-lump.min())/(lump.max()-lump.min())
muscle=np.array([0.42,0.05,0.045])[None,None]*(0.35+0.9*n1[...,None]*lump[...,None])*(0.7+0.5*fib[...,None])
fat=np.array([0.52,0.40,0.26])[None,None]*(0.5+0.5*n2[...,None])
crust=np.array([0.09,0.025,0.02])[None,None]*(0.6+0.8*n2[...,None])
rr=r+0.12*(n1-0.5)
wf=0.7*np.clip((rr-0.76)/0.04,0,1)*np.clip((0.86-rr)/0.04,0,1)*(0.4+0.6*n2)
wc=np.clip((rr-0.86)/0.06,0,1)
col=muscle*(1-wf[...,None])+fat*wf[...,None]; col=col*(1-wc[...,None])+crust*wc[...,None]
hh=0.4*n1+0.25*fib+0.5*lump+0.4*wf-0.2*wc
# blood decal overlay (clotted dark, wet)
try:
    d=np.array(Image.open('/tmp/sa_dmg/characters_art/fx_decals/textures/blood_splatter_thick_a_bc.png').convert('RGBA').resize((N,N)))/255.
    a=d[...,3:4]*0.85; col=col*(1-a)+d[...,:3]*0.45*a; hh=hh+0.3*a[...,0]
except Exception as e: print('decal',e); a=np.zeros((N,N,1))
fl=x<0.75
bc[fl]=col[fl]; h[fl]=hh[fl]; rough[fl]=(0.28+0.25*n2+0.45*wc-0.15*a[...,0])[fl]; ao[fl]=(1-0.35*np.clip(1-r,0,1)**3)[fl]
# bone strip
bx=(x-0.75)/0.25; streak=gaussian_filter(rng.random((N,N)),(6,0.8)); streak=(streak-streak.min())/(streak.max()-streak.min())
bone=np.array([0.62,0.56,0.44])[None,None]*(0.75+0.35*streak[...,None])*(0.85+0.2*n2[...,None])
grime=np.clip(n1-0.55,0,1)[...,None]*1.5; bone=bone*(1-grime)+np.array([0.25,0.06,0.04])*grime
mar=y<0.2; marrow=np.array([0.3,0.08,0.05])[None,None]*(0.6+0.6*n1[...,None])
# bloody base on bone (bottom 35%)
bb=np.clip((y-0.6)/0.25,0,1)[...,None]*(0.6+0.4*n2[...,None]); bone=bone*(1-bb)+np.array([0.22,0.02,0.02])*bb
bs=~fl
bc[bs]=bone[bs]; h[bs]=(0.4*streak+0.2*n1)[bs]; rough[bs]=(0.55+0.2*n2-0.3*bb[...,0])[bs]
m2=bs&mar; bc[m2]=marrow[m2]; h[m2]=(0.3*n1)[m2]; rough[m2]=0.3
h=gaussian_filter(h,0.8)
gx=sobel(h,1); gy=sobel(h,0); s=3.0
nm=np.stack([-gx*s,gy*s,np.ones_like(h)],-1); nm/=np.linalg.norm(nm,axis=-1,keepdims=True)
Image.fromarray((np.clip(bc*1.25,0,1)**(1/1.3)*255).astype(np.uint8)).save('textures/gore_atlas_bc.png')
Image.fromarray(((nm*0.5+0.5)*255).astype(np.uint8)).save('textures/gore_atlas_n.png')
orm=np.stack([ao,np.clip(rough,0.05,1),np.zeros_like(h)],-1)
Image.fromarray((orm*255).astype(np.uint8)).save('textures/gore_atlas_orm.png')
print('ok')
