# new textures for props_new -> /workspace/pnwork/tex : rug_a/n, map_a, runes_a(+ emissive strip)
import numpy as np, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
T='/workspace/pnwork/tex'; B1='/workspace/sanctuary_env/batch1_interactables/v2/src/tex'
rng=np.random.default_rng(7); random.seed(7)
FONT='/usr/share/fonts/truetype/sand-box/google/Cormorant Garamond/CormorantGaramond-VariableFont_wght.ttf'
def f(sz):
    ft=ImageFont.truetype(FONT,sz)
    try: ft.set_variation_by_name('Bold')
    except Exception: pass
    return ft
def lin(x): return np.where(x<=0.04045,x/12.92,((x+0.055)/1.055)**2.4)
def srgb(x): return np.where(x<=0.0031308,x*12.92,1.055*np.power(np.clip(x,0,1),1/2.4)-0.055)
def noise(n,scale,oct=4,seed=0):
    r=np.random.default_rng(seed); acc=np.zeros((n,n)); a=1; tot=0
    for o in range(oct):
        s=max(2,int(scale*2**o)); g=r.random((s,s)); im=Image.fromarray((g*255).astype(np.uint8)).resize((n,n),Image.BICUBIC)
        acc+=a*np.asarray(im,float)/255; tot+=a; a*=0.5
    return acc/tot
# ---------------- RUG (1024, whole rug once; 2.4 x 1.6 m) ----------------
N=1024; W,H=N,int(N*2/3)
fib=np.asarray(Image.open(f'{B1}/dirty_carpet_diff.jpg').convert('L').resize((512,512),Image.LANCZOS),float)/255
fib=np.tile(fib,(2,2))[:H,:W]; fib=fib/fib.mean()
img=Image.new('RGB',(W,H),(44,12,11)); d=ImageDraw.Draw(img)
gold=(96,74,40); dark=(22,9,8); blue=(22,24,32); red2=(64,18,15)
# borders
for k,(m,c) in enumerate([(0,dark),(18,gold),(26,blue),(70,gold),(78,red2)]):
    d.rectangle([m,m,W-1-m,H-1-m],fill=c)
# border motif (diamonds/crenels in the blue band)
for x in range(40,W-40,34):
    for y in (48,H-48):
        d.polygon([(x,y-12),(x+12,y),(x,y+12),(x-12,y)],fill=gold)
for y in range(48+34,H-48-20,34):
    for x in (48,W-48):
        d.polygon([(x,y-12),(x+12,y),(x,y+12),(x-12,y)],fill=gold)
# central medallion
cx,cy=W//2,H//2
for r,c in [(200,dark),(186,gold),(176,blue),(140,gold),(130,red2),(70,gold),(60,dark)]:
    d.ellipse([cx-r*1.35,cy-r,cx+r*1.35,cy+r],fill=c)
for a in range(16):
    t=a*math.pi/8; x=cx+math.cos(t)*158*1.35; y=cy+math.sin(t)*158
    d.ellipse([x-10,y-10,x+10,y+10],fill=red2)
for k in range(4):
    t=k*math.pi/2+math.pi/4; x=cx+math.cos(t)*45*1.35; y=cy+math.sin(t)*45
    d.ellipse([x-26,y-26,x+26,y+26],fill=red2)
d.polygon([(cx-120,cy),(cx,cy-60),(cx+120,cy),(cx,cy+60)],outline=gold,width=5)
# corner spandrels
for sx,sy in [(1,1),(-1,1),(1,-1),(-1,-1)]:
    ox=110 if sx>0 else W-110; oy=110 if sy>0 else H-110
    d.pieslice([ox-90,oy-90,ox+90,oy+90],0,360,fill=None,outline=gold,width=8)
    d.ellipse([ox-30,oy-30,ox+30,oy+30],fill=blue)
a=lin(np.asarray(img,float)/255)
wear=noise(H if H>W else W,6,5,3)[:H,:W]; wear=np.clip((wear-0.55)*3,0,1)
grime=noise(W,3,4,9)[:H,:W]
a=a*(fib[...,None]**1.1)*(0.75+0.5*grime[...,None])
a=a*(1-0.55*wear[...,None])+np.array([0.025,0.02,0.016])*wear[...,None]
Y=(a*[0.2126,0.7152,0.0722]).sum(-1,keepdims=True); a=(Y+(a-Y)*0.72)*0.62
a=srgb(np.clip(a,0,1)); Image.fromarray((a*255).astype(np.uint8)).save(f'{T}/rug_a.jpg',quality=88)
nr=Image.open(f'{B1}/dirty_carpet_nor.jpg').convert('RGB').resize((512,512),Image.LANCZOS)
nn=Image.new('RGB',(1024,1024)); [nn.paste(nr,(x,y)) for x in (0,512) for y in (0,512)]
nn.crop((0,0,W,H)).resize((512,342)).save(f'{T}/rug_n_512.jpg',quality=88)
# ---------------- MAP "The known roads" (1024x768) ----------------
W,H=1024,768
pl=np.asarray(Image.open('/workspace/gothwork/ph/rough_linen/diff.jpg').convert('L').resize((W,W),Image.LANCZOS),float)[:H]/255
n1=noise(W,4,5,11)[:H]; n2=noise(W,16,3,12)[:H]
base=np.stack([0.62,0.53,0.38])[None,None,:]*(0.8+0.3*n1[...,None])*(0.9+0.12*(pl[...,None]/pl.mean()))
yy,xx=np.mgrid[0:H,0:W]; vig=((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2; base=base*(1-0.45*np.clip(vig-0.35,0,1)[...,None])
stain=np.clip((noise(W,5,4,21)[:H]-0.62)*4,0,1); base=base*(1-0.25*stain[...,None])
img=Image.fromarray((np.clip(base,0,1)*255).astype(np.uint8)); d=ImageDraw.Draw(img)
ink=(46,30,18); faint=(92,70,46); red=(110,28,18)
# coast line on west (sea at left), with hatching
coast=[(185+28*math.sin(y/55)+14*math.sin(y/19),y) for y in range(0,H+10,10)]
d.line(coast,fill=ink,width=3)
for (x,y) in coast[::1]:
    for k in range(1,5): d.line([(x-k*14,y),(x-k*14-8,y+3)],fill=faint,width=1)
# isle
isl=[(85+40*math.cos(t)+8*math.sin(5*t),600+28*math.sin(t)) for t in np.linspace(0,2*math.pi,40)]
d.line(isl+[isl[0]],fill=ink,width=2)
# places (x,y,name)
P={'Martsirt':(470,330),'Briarwood':(560,190),'Briarwood East':(760,170),'Ashen Coast':(320,420),'Bastion':(360,560),'Bluffs':(430,660),
   'Blackwater Isle':(85,600),'Highmarket':(700,430),'Cinder Barrens':(870,560),'Qadren':(820,330),'The Dunes':(690,280),'Flotsam':(270,610)}
roads=[('Martsirt','Briarwood'),('Briarwood','Briarwood East'),('Martsirt','Ashen Coast'),('Ashen Coast','Bastion'),('Bastion','Bluffs'),
       ('Martsirt','Highmarket'),('Highmarket','Cinder Barrens'),('Briarwood','The Dunes'),('The Dunes','Qadren'),('Qadren','Highmarket'),('Ashen Coast','Flotsam')]
def dashed(p,q,seg=12,gap=7,w=3,col=ink,wob=10,seed=0):
    r=random.Random(seed); L=math.dist(p,q); n=max(2,int(L/6)); pts=[]
    nx,ny=(q[1]-p[1])/L,-(q[0]-p[0])/L; ph=r.random()*6
    for i in range(n+1):
        t=i/n; s=math.sin(t*math.pi)*wob*math.sin(ph+t*3)
        pts.append((p[0]+(q[0]-p[0])*t+nx*s,p[1]+(q[1]-p[1])*t+ny*s))
    acc=0; on=True; cur=[pts[0]]
    for a,b in zip(pts,pts[1:]):
        acc+=math.dist(a,b); cur.append(b)
        if on and acc>seg: d.line(cur,fill=col,width=w); cur=[b]; acc=0; on=False
        elif not on and acc>gap: cur=[b]; acc=0; on=True
for i,(a,b) in enumerate(roads): dashed(P[a],P[b],seed=i)
d.line([(P['Ashen Coast'][0]-20,P['Ashen Coast'][1]+30),(125,590)],fill=faint,width=2)  # sea lane
# mountains / trees glyphs
for k in range(26):
    x=random.uniform(760,990); y=random.uniform(95,150); s=random.uniform(12,20)
    d.line([(x-s,y+s*0.6),(x,y-s*0.6),(x+s,y+s*0.6)],fill=ink,width=2)
for k in range(40):
    x=random.uniform(500,640); y=random.uniform(125,178); s=random.uniform(5,8)
    d.ellipse([x-s,y-s,x+s,y+s],outline=faint,width=2)
for name,(x,y) in P.items():
    big=name=='Martsirt'
    if big: d.rectangle([x-9,y-9,x+9,y+9],outline=red,width=3); d.line([(x-5,y),(x+5,y)],fill=red,width=2)
    else: d.ellipse([x-6,y-6,x+6,y+6],fill=ink)
    ft=f(34 if big else 25); tw=d.textlength(name,font=ft); ty=y-44 if name=='Blackwater Isle' else y+10
    d.text((x-tw/2,ty),name,font=ft,fill=red if big else ink)
ft=f(56); t='The Known Roads'; tw=d.textlength(t,font=ft); d.text((W/2-tw/2,22),t,font=ft,fill=ink)
# compass rose
cx,cy=930,680
for a in range(8):
    t=a*math.pi/4; L=46 if a%2==0 else 26
    d.polygon([(cx,cy),(cx+math.cos(t+0.25)*12,cy+math.sin(t+0.25)*12),(cx+math.cos(t)*L,cy+math.sin(t)*L)],fill=ink)
d.text((cx-8,cy-82),'N',font=f(30),fill=ink)
d.rectangle([12,12,W-13,H-13],outline=ink,width=3); d.rectangle([22,22,W-23,H-23],outline=faint,width=1)
img=img.filter(ImageFilter.GaussianBlur(0.6))
a=np.asarray(img,float)/255; a=a*(0.92+0.1*n2[...,None]); a=np.clip(a*0.82,0,1)  # aged / darker for game lighting
Image.fromarray((a*255).astype(np.uint8)).save(f'{T}/map_a.jpg',quality=88)
# ---------------- RUNES strip (512x64) emissive mask for well heal ----------------
W,H=1024,128; img=Image.new('L',(W,H),0); d=ImageDraw.Draw(img)
for i in range(16):
    x0=i*64+32; r=random.Random(i)
    for k in range(r.randint(3,5)):
        a=(x0+r.randint(-18,18),r.randint(24,104)); b=(x0+r.randint(-18,18),r.randint(24,104)); d.line([a,b],fill=255,width=7)
    d.ellipse([x0-5,10,x0+5,20],fill=255)
img=img.filter(ImageFilter.GaussianBlur(2.2))
m=np.asarray(img,float)/255; rgb=np.stack([0.35*m,0.85*m,0.75*m],-1)
Image.fromarray((np.clip(rgb,0,1)*255).astype(np.uint8)).save(f'{T}/runes_e.png')
print('ok')
