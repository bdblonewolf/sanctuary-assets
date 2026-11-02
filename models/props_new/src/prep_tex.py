# Poly Haven 1K -> toned dark/earthy albedo (AO multiplied in) + normal. Output /workspace/gothwork/tex/<mat>_{a,n}{,_512}.jpg
import numpy as np, json, os
from PIL import Image, ImageFilter, ImageDraw
PH='/workspace/gothwork/ph'; T='/workspace/gothwork/tex'; os.makedirs(T,exist_ok=True)
# mat: (source, saturation, target mean sRGB, contrast)
M={
 'wood_planks': ('weathered_planks',0.75,(62,52,42),1.15),
 'wood_rough':  ('rough_wood',0.8,(66,56,44),1.1),
 'wood_rot':    ('moss_wood',0.45,(52,52,38),1.2),
 'wood_dark':   ('dark_wooden_planks',0.9,(52,40,30),1.15),
 'wood_peel':   ('weathered_peeling_timber',0.6,(60,56,48),1.1),
 'stone_carved':('worn_rock_natural_01',0.25,(84,80,74),1.25),
 'stone_mossy': ('rock_pitted_mossy',0.3,(80,78,70),1.2),
 'stone_block': ('castle_wall_slates',0.5,(70,68,62),1.1),
 'rock':        ('rock_face',0.45,(66,58,50),1.15),
 'rock_dark':   ('dark_rock',0.6,(44,42,40),1.2),
 'iron':        ('rust_coarse_01',0.55,(52,40,32),1.25),
 'iron_plate':  ('metal_plate',0.5,(50,46,42),1.2),
 'cloth_hessian':('hessian_230',0.55,(84,72,54),1.0),
 'cloth_linen': ('rough_linen',0.0,(150,142,124),1.1),
 'velvet':      ('velour_velvet',0.55,(70,22,22),1.05),
 'leather':     ('brown_leather',0.7,(58,38,26),1.15),
 'bone':        ('grey_plaster',0.0,(150,138,112),1.25),
 'clay':        ('worn_rock_natural_01',0.55,(88,62,48),1.3),
 'cliff':       ('cliff_side',0.4,(60,54,48),1.15),
 'lichen':      ('lichen_rock',0.5,(70,68,60),1.15),
}
def lin(x): return np.where(x<=0.04045,x/12.92,((x+0.055)/1.055)**2.4)
def srgb(x): return np.where(x<=0.0031308,x*12.92,1.055*np.power(np.clip(x,0,1),1/2.4)-0.055)
def tone(src,sat,tgt,con,tint=None):
    a=np.asarray(Image.open(f'{PH}/{src}/diff.jpg').convert('RGB').resize((1024,1024),Image.LANCZOS),float)/255
    ao=np.asarray(Image.open(f'{PH}/{src}/ao.jpg').convert('L').resize((1024,1024),Image.LANCZOS),float)/255
    L=lin(a); Y=(L*[0.2126,0.7152,0.0722]).sum(-1,keepdims=True)
    L=Y+(L-Y)*sat
    m=L.reshape(-1,3).mean(0); L=m*(L/m)**con  # contrast in linear around mean
    L=L*(0.35+0.65*ao[...,None])
    tg=lin(np.array(tgt)/255.); L=L*(tg/L.reshape(-1,3).mean(0))
    return srgb(np.clip(L,0,1))
def save(name,rgb,src,q=82):
    im=Image.fromarray((np.clip(rgb,0,1)*255+0.5).astype(np.uint8))
    im.save(f'{T}/{name}_a.jpg',quality=q,optimize=True); im.resize((512,512),Image.LANCZOS).save(f'{T}/{name}_a_512.jpg',quality=q,optimize=True)
    if src:
        n=Image.open(f'{PH}/{src}/nor.jpg').convert('RGB').resize((1024,1024),Image.LANCZOS)
        n.save(f'{T}/{name}_n.jpg',quality=85,optimize=True); n.resize((512,512),Image.LANCZOS).save(f'{T}/{name}_n_512.jpg',quality=85,optimize=True)
info={}
for k,(src,sat,tgt,con) in M.items():
    save(k,tone(src,sat,tgt,con),src); info[k]={'source':src}
# sail: hessian with faded vertical stripes (dark oxblood / soot), edge grime, holes in alpha handled by geometry
h=tone('hessian_230',0.5,(92,80,62),1.0); H,W,_=h.shape; x=np.arange(W)/W
stripe=((x*6)%1<0.5)[None,:,None]  # 6 stripes across (3 red,3 bare)
red=np.array([0.36,0.12,0.09]); h=np.where(stripe,h*0.55+red*0.45*h.mean(),h)
y=np.arange(H)/H; grime=1-0.35*np.clip((y-0.6)/0.4,0,1)**1.5; h=h*grime[:,None,None]
rng=np.random.default_rng(3); n=np.asarray(Image.fromarray((rng.random((64,64))*255).astype(np.uint8)).resize((W,H),Image.BICUBIC),float)/255
h=h*(0.75+0.35*n[...,None]); save('sail_striped',h,'hessian_230')
# tapestry: velvet field + heraldry (border, inverted winged sword, crown) faded
v=tone('velour_velvet',0.55,(66,20,22),1.05); img=Image.new('L',(1024,1024),0); d=ImageDraw.Draw(img)
d.rectangle([40,40,984,984],outline=255,width=26); d.rectangle([90,90,934,934],outline=200,width=8)
d.polygon([(500,240),(524,240),(524,760),(560,760),(512,880),(464,760),(500,760)],fill=255)  # blade (point down)
d.rectangle([380,210,644,240],fill=255); d.rectangle([496,130,528,210],fill=255); d.ellipse([486,95,538,147],fill=255)
for sgn in (-1,1):  # wings
    for k in range(6):
        x0=512+sgn*(60+k*48); d.polygon([(512+sgn*40,330+k*10),(x0,300-k*22),(x0+sgn*40,340-k*18),(512+sgn*40,420+k*8)],fill=230)
d.polygon([(420,560),(604,560),(512,610)],fill=180)
for i in range(7): d.polygon([(90+i*140,984),(160+i*140,984),(125+i*140,1015)],fill=255)
g=np.asarray(img.filter(ImageFilter.GaussianBlur(1.2)),float)[...,None]/255
gold=np.array([0.42,0.33,0.16]); nz=np.asarray(Image.open(f'{PH}/velour_velvet/ao.jpg').convert('L').resize((1024,1024)),float)[...,None]/255
paint=gold*(0.6+0.4*n[...,None])*(0.5+0.5*nz)
v=v*(1-g*0.85)+paint*g*0.85
fade=1-0.25*np.clip((np.arange(1024)/1024-0.55)/0.45,0,1)[:,None,None]; v=v*fade
save('tapestry_heraldic',v,'velour_velvet')
# book pages (two-page spread with dark ink lines) 512
p=tone('grey_plaster',0.0,(150,136,104),1.1); pi=Image.fromarray((p*255).astype(np.uint8)); d=ImageDraw.Draw(pi)
for side in (0,1):
    for r in range(22):
        y0=90+r*38; xs=60+side*512; d.line([(xs,y0),(xs+380-(r%5==4)*170,y0)],fill=(40,30,24),width=5)
    d.rectangle([60+side*512,40,140+side*512,120],fill=(90,22,18))
d.line([(512,0),(512,1024)],fill=(60,48,36),width=10)
save('book_pages',np.asarray(pi,float)/255,None)
# candle flame card (RGBA, emissive) + cobweb RGBA
f=np.zeros((128,64,4)); yy,xx=np.mgrid[0:128,0:64]; r=np.sqrt(((xx-32)/14)**2+((yy-80)/42)**2)
core=np.clip(1-r,0,1); f[...,0]=1; f[...,1]=0.55+0.4*core; f[...,2]=0.15+0.5*core**2; f[...,3]=(core>0.02)*1.0
Image.fromarray((f*255).astype(np.uint8),'RGBA').save(f'{T}/flame.png')
cw=Image.new('RGBA',(512,512),(0,0,0,0)); d=ImageDraw.Draw(cw); import math
cx,cy=6,6; rng=np.random.default_rng(5); spokes=[(math.radians(a)) for a in np.linspace(2,88,9)+rng.uniform(-3,3,9)]
for a in spokes: d.line([(cx,cy),(cx+700*math.cos(a),cy+700*math.sin(a))],fill=(200,200,195,255),width=3)
for k in range(1,16):
    R=k*34+rng.uniform(-6,6); pts=[(cx+R*1.02*math.cos(a)*(1+0.06*math.sin(k*a*3)),cy+R*math.sin(a)) for a in spokes]
    for i in range(len(pts)-1):
        p0,p1=pts[i],pts[i+1]; mx=(p0[0]+p1[0])/2*0.93; my=(p0[1]+p1[1])/2*0.93
        d.line([p0,(mx,my),p1],fill=(190,190,185,255),width=2)
for _ in range(6):
    x0,y0=rng.uniform(80,400,2); d.line([(x0,y0),(x0+rng.uniform(-60,60),y0+rng.uniform(30,90))],fill=(180,180,175,255),width=2)
cw.save(f'{T}/cobweb.png')
# torn rotting sail scraps RGBA (holes + ragged edges)
ts=tone('hessian_230',0.4,(70,62,50),1.1); ts=np.where(stripe,ts*0.6+np.array([0.25,0.1,0.08])*0.4*ts.mean(),ts)
rng=np.random.default_rng(11); m=np.asarray(Image.fromarray((rng.random((48,48))*255).astype(np.uint8)).resize((1024,1024),Image.BICUBIC).filter(ImageFilter.GaussianBlur(6)),float)/255
m2=np.asarray(Image.fromarray((rng.random((160,160))*255).astype(np.uint8)).resize((1024,1024),Image.BICUBIC),float)/255
yy,xx=np.mgrid[0:1024,0:1024]/1024.; edge=np.minimum.reduce([xx,1-xx,yy,1-yy])
al=(m*0.7+m2*0.3+edge*1.6)>0.62
ts=ts*(0.55+0.45*m[...,None])*(0.7+0.3*yy[...,None]**0)  # mildew blotches
rgba=np.dstack([np.clip(ts,0,1)*255,al*255]).astype(np.uint8)
Image.fromarray(rgba,'RGBA').save(f'{T}/sail_torn.png',optimize=True)
Image.fromarray(rgba,'RGBA').resize((512,512),Image.LANCZOS).save(f'{T}/sail_torn_512.png',optimize=True)
json.dump(info,open(T+'/info.json','w'))
for fn in sorted(os.listdir(T)): print(fn, os.path.getsize(f'{T}/{fn}'))
