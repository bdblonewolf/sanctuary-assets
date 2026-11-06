import glob,numpy as np
from PIL import Image
def s2l(x): x=x/255.0; return np.where(x<=0.04045,x/12.92,((x+0.055)/1.055)**2.4)
sky=np.array([0x9f,0xb3,0xc4])
for b in sorted(glob.glob('shots/*_before.png')):
    a=b.replace('_before','_after')
    A=np.asarray(Image.open(b).convert('RGB')).astype(float); B=np.asarray(Image.open(a).convert('RGB')).astype(float)
    # pixels that are not sky in both
    m=(np.abs(A-sky).sum(-1)>40)&(np.abs(B-sky).sum(-1)>40)
    la=(s2l(A)@[0.2126,0.7152,0.0722])[m]; lb=(s2l(B)@[0.2126,0.7152,0.0722])[m]
    print(f"{b.split('/')[-1][:-11]:34s} mean {lb.mean()/la.mean():.2f}  p5 {np.percentile(lb,5)/max(np.percentile(la,5),1e-5):.2f}")
