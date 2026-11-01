# make generated swatches seamless and derive overlay-detail (0.5 neutral) + height maps
import numpy as np, sys
from PIL import Image
from scipy.ndimage import gaussian_filter
D='/workspace/sanctuary_npc/martsirt/src/swatch'
def seamless(a):
    h,w=a.shape[:2]; y=np.linspace(0,1,h)[:,None]; x=np.linspace(0,1,w)[None,:]
    wgt=(np.sin(np.pi*y)*np.sin(np.pi*x))**0.6
    r=np.roll(np.roll(a,h//2,0),w//2,1)
    return a*wgt[...,None]+r*(1-wgt[...,None])
def blur(a,s): return gaussian_filter(a,(s,s,0) if a.ndim==3 else s,mode='wrap')
for k,sig_c,sig_h,keep in (('leather_apron',40,3,0.6),('leather_dark',40,2.5,0.4),('linen',30,1.5,0.3),('wool',30,1.5,0.3),('skin',30,2.0,0.3)):
    a=np.asarray(Image.open(f'{D}/raw_{k}.jpg').convert('RGB').resize((1024,1024),Image.LANCZOS),np.float32)/255.0
    a=seamless(a)
    lo=blur(a,sig_c); det=a/np.maximum(lo,1e-3)
    det=det*(1-keep)+keep*(a/a.reshape(-1,3).mean(0))   # keep some of the large-scale blotches
    det=np.clip(0.5*det,0,1)
    L=a.mean(2); hp=L-gaussian_filter(L,sig_h*6,mode='wrap'); hp2=gaussian_filter(L,sig_h*0.5,mode='wrap')-gaussian_filter(L,sig_h*2,mode='wrap')
    h=hp/ (np.abs(hp).std()*4)+hp2/(np.abs(hp2).std()*4)
    h=np.clip(0.5+0.5*h/2,0,1)
    Image.fromarray((det*255).astype(np.uint8)).save(f'{D}/{k}_det.png')
    Image.fromarray((h*255).astype(np.uint8)).save(f'{D}/{k}_h.png')
    print(k,det.mean((0,1)),h.mean(),h.std())
