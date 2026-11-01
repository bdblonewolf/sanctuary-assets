# hair strand card texture: RGBA, strands run vertically; root at the TOP of the image (uv v=1), tips at the bottom (v=0)
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
W,H=512,1024; rng=np.random.default_rng(7)
col=np.zeros((H,W)); alp=np.zeros((H,W))
yy=np.arange(H)
clumps=rng.uniform(40,W-40,14)
for i in range(230):
    x0=rng.choice(clumps)+rng.normal(0,9); 
    if x0<8 or x0>W-8: continue
    L=rng.uniform(0.55,1.0)*H            # strand length from the root
    amp=rng.uniform(2,7); fr=rng.uniform(1.2,3.5); ph=rng.uniform(0,6.3); drift=rng.normal(0,18)
    wdt=rng.uniform(2.0,4.2); br=rng.uniform(0.35,1.0)
    t=yy/H; x=x0+amp*np.sin(t*fr*6.283+ph)+drift*t**2
    taper=np.clip((L-yy)/(0.25*H),0,1)   # thin out to the tip
    for y in range(0,int(min(L,H))):
        w=wdt*(0.35+0.65*taper[y]); xs=int(x[y]-3); xe=int(x[y]+4)
        for xi in range(max(xs,0),min(xe,W)):
            d=abs(xi-x[y]); a=np.clip(w-d+0.5,0,1)*(0.55+0.45*taper[y])
            if a>alp[y,xi]: alp[y,xi]=a; col[y,xi]=br*(0.75+0.25*taper[y])
# soft side falloff so card edges never show a hard line
xx=np.arange(W)/W; side=np.clip(np.minimum(xx,1-xx)/0.12,0,1)
alp*=side[None,:]
col=gaussian_filter(col,0.6); 
img=np.dstack([col,col,col,alp]); img[...,:3]=np.where(alp[...,None]>0.02,img[...,:3],0.25)
Image.fromarray((np.clip(img,0,1)*255).astype(np.uint8),'RGBA').save('/workspace/sanctuary_npc/martsirt/src/swatch/strands.png')
print('ok',alp.mean())
