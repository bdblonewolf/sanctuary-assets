# Painted irregular pine-canopy silhouette atlases (2x2 tiles, 512px), keep-blacks palettes.
import numpy as np, zlib
from PIL import Image, ImageDraw
from scipy import ndimage
T=512; SS=2
PAL={ # sRGB: deep, sh, mid, li, rim (+snow)
 'summer':dict(deep=(6,12,9),sh=(14,25,18),mid=(27,43,27),li=(44,64,34),rim=(64,84,42)),
 'pine_autumn':dict(deep=(7,12,9),sh=(16,25,17),mid=(29,42,26),li=(47,60,31),rim=(68,78,38)),
 'rust':dict(deep=(14,7,4),sh=(40,18,8),mid=(90,40,14),li=(132,66,24),rim=(156,90,34)),
 'kit_winter':dict(deep=(9,18,15),sh=(19,36,29),mid=(34,54,43),li=(48,70,55),rim=(64,84,68),snow=(104,114,120)),
 'ring_winter':dict(deep=(7,13,12),sh=(15,28,24),mid=(28,42,38),li=(46,60,56),rim=(64,76,76),snow=(206,214,228)),
 'dead':dict(deep=(7,7,7),sh=(15,14,13),mid=(25,24,22),li=(37,34,30),rim=(47,43,37)),
}
def lerp(a,b,t): return a+(b-a)*t[...,None]
def blot(rng,h,w,sc):
    a=rng.random((max(2,int(h/sc))+2,max(2,int(w/sc))+2)).astype(np.float32)
    return np.asarray(Image.fromarray(a,'F').resize((w,h),Image.BICUBIC))

def tier_poly(rng,cx,yb,yt,half,h_t,dead):
    L=[]
    # right flank from apex down to skirt tip: outward-pointing needle tufts
    m=max(6,int((yb-yt)/3))
    L.append((cx+rng.normal(0,half*0.03),yt))
    for i in range(1,m+1):
        v=i/m; y=yt+(yb-yt)*v; x=cx+half*v**0.85
        if i%2: x+=half*0.10*rng.random()*(0.4+v); y+=h_t*0.05*rng.random()
        L.append((x,y))
    tip=(cx+half*(1.04+0.06*rng.random()), yb+h_t*(0.10+0.12*rng.random()))
    L.append(tip)
    # skirt underside right->left: wavy with short drooping tufts
    n=max(8,int(half*2/4))
    for i in range(1,n):
        u=1-i/n*2; x=cx+u*half*0.98
        y=yb+h_t*(0.02+0.10*(1-abs(u))**1.5)
        y+= h_t*0.10*rng.random() if i%2 else -h_t*0.06*rng.random()
        if dead and rng.random()<0.35: y-=h_t*0.35*rng.random()
        L.append((x,y))
    L.append((cx-half*(1.04+0.06*rng.random()), yb+h_t*(0.10+0.12*rng.random())))
    for i in range(m,0,-1):
        v=i/m; y=yt+(yb-yt)*v; x=cx-half*v**0.85
        if i%2: x-=half*0.10*rng.random()*(0.4+v); y+=h_t*0.05*rng.random()
        L.append((x,y))
    return L

def pine(rng,canvas,cx,base,h,w,pal,snow=0.0,dead=False,dk=1.0):
    rgb,al,nzA,nzB=canvas
    S=SS
    dk=dk*(0.78+0.27*rng.random())
    pal={k:np.array(v,float)*dk if k!='snow' else np.array(v,float)*min(1,dk*1.05) for k,v in pal.items()}
    ntier=int(rng.integers(6,10)) if not dead else int(rng.integers(8,13))
    lean=rng.normal(0,0.035)*h
    top=base-h
    trunk_w=max(2,w*0.05)
    # trunk (mostly hidden)
    d=ImageDraw.Draw(Image.new('L',(1,1)))
    for k in range(ntier):
        t0=k/ntier
        h_t=h/ntier*(1.5 if k<ntier-1 else 1.3)
        yb=base-h*t0*0.93 - h_t*0.10 + (rng.random()-0.5)*h/ntier*0.55
        yt=max(top, yb-h_t*(1.25+0.25*rng.random()))
        if k==ntier-1: yt=top
        cxt=cx+lean*t0
        half=w*0.5*(1-t0*0.92)**0.9*(0.85+0.28*rng.random())
        if dead: half*=0.7+0.4*rng.random()
        P=tier_poly(rng,cxt,yb,yt,half,h_t,dead)
        xs=[p[0] for p in P]; ys=[p[1] for p in P]
        x0=int(max(0,np.floor(min(xs)*S)-2)); x1=int(min(rgb.shape[1],np.ceil(max(xs)*S)+2))
        y0=int(max(0,np.floor(min(ys)*S)-2)); y1=int(min(rgb.shape[0],np.ceil(max(ys)*S)+2))
        if x1<=x0 or y1<=y0: continue
        im=Image.new('L',(x1-x0,y1-y0),0); dr=ImageDraw.Draw(im)
        dr.polygon([(x*S-x0,y*S-y0) for x,y in P],fill=255)
        if dead:
            for _ in range(int(half/1.5)):
                x=cxt+(rng.random()*2-1)*half*0.85; y=yb-(yb-yt)*rng.random()*0.7
                r=(0.05+rng.random()*0.16)*half
                dr.ellipse([(x-r)*S-x0,(y-r*0.5)*S-y0,(x+r)*S-x0,(y+r*0.5)*S-y0],fill=0)
            for _ in range(2):
                s=rng.choice([-1,1]); yy0=yb-(yb-yt)*0.3
                dr.line([(cxt*S-x0,yy0*S-y0),((cxt+s*half*(1.1+0.3*rng.random()))*S-x0,(yy0+h_t*0.3*rng.random())*S-y0)],fill=255,width=max(1,int(0.9*S)))
        m=np.asarray(im,float)/255
        yy,xx=np.mgrid[y0:y1,x0:x1]/S
        ty=np.clip((yy-yt)/max(yb-yt,1e-3),0,1.3)
        tx=np.clip((xx-cxt)/max(half,1e-3),-1.2,1.2)
        nA=nzA[y0:y1,x0:x1]; nB=nzB[y0:y1,x0:x1]
        band=h*0.93/ntier
        e=(yy-(yb-band*1.05))/(band*1.25)          # 0 just under the tier above, 1 at own skirt
        e=np.where(k==ntier-1, ty, e)
        side=np.clip(0.5-tx*0.5,0,1)               # sun from the left
        prof=np.clip(1-np.abs(e-0.38)/0.5,0,1)**0.9 # lit branch tops mid-band
        lit=(0.18+0.82*side**1.2)*(0.55+0.45*prof)+0.22*(nA-0.5)+0.10*(nB-0.5)
        lit=np.clip(lit,0,1)
        c=lerp(pal['sh'],pal['mid'],np.clip(lit*1.7,0,1))
        c=lerp(c,pal['li'],np.clip(lit*2.0-0.85,0,1))
        c=lerp(c,pal['rim'],np.clip((lit-0.80)*4,0,1)*np.clip(-tx-0.1,0,1))
        shade=np.clip((0.08-e)/0.08,0,1)*0.30*np.clip(nA*1.6,0,1) + np.clip((e-0.84)/0.16,0,1)*0.65
        c=lerp(c,pal['deep'],np.clip(shade*(0.6 if snow>0.9 else 1.0)+0.12*(nB>0.75),0,1))
        if snow>0 and 'snow' in pal:
            sm=np.clip(1-np.abs(e-0.40)/(0.32 if snow<0.9 else 0.62),0,1)*(0.6+0.4*side)+0.85*(nA-0.5)+0.35*(nB-0.5)+0.25*np.clip(0.6-abs(tx),-1,1)-0.1
            if k==ntier-1: sm=np.maximum(sm,np.clip((0.35-ty)/0.35,0,1))
            tsnow=0.55+0.45*rng.random()
            sm=np.clip((sm-(0.42 if snow<0.9 else 0.20))*3,0,1)*min(snow,1.0)*tsnow
            sc=lerp(pal['snow']*0.78,pal['snow'],side)
            c=lerp(c,sc,sm)
        R=rgb[y0:y1,x0:x1]; A=al[y0:y1,x0:x1]
        R[:]=R*(1-m[...,None])+c*m[...,None]; A[:]=np.maximum(A,m)

def paint_tile(seed,pal_names,snow=0.0,dead=False,rust_frac=0.0):
    rng=np.random.default_rng(seed)
    W=H=T; Wb,Hb=W*SS,H*SS
    rgb=np.zeros((Hb,Wb,3)); al=np.zeros((Hb,Wb))
    nzA=blot(rng,Hb,Wb,14*SS)*0.6+blot(rng,Hb,Wb,4*SS)*0.4
    nzB=ndimage.gaussian_filter(rng.random((Hb,Wb)),(0.7*SS,2.0*SS)); nzB=(nzB-nzB.min())/(np.ptp(nzB)+1e-6)
    cv=(rgb,al,nzA,nzB)
    # back row: darker (never lighter) and shorter; front row: taller, irregular
    yy0,xx0=np.mgrid[0:Hb,0:Wb]/SS
    back_ridge=H*0.42+np.asarray(Image.fromarray(rng.random((1,24)).astype(np.float32),'F').resize((Wb,1),Image.BICUBIC))[0]*H*0.18
    xc0=np.arange(Wb)/SS; fall=np.clip(np.minimum(xc0-W*0.10,W*0.90-xc0)/(W*0.12),0,1)
    back_ridge=H-(H-back_ridge)*np.sqrt(fall)
    bm=(yy0>back_ridge[None,:])&(fall[None,:]>0)
    pal0={k:np.array(v,float) for k,v in PAL[pal_names[0]].items()}
    rgb[bm]=(pal0['deep']*0.55)[None,:]*(0.8+0.4*nzA[bm])[:,None]; al[bm]=1.0
    g=10  # keep every tree fully inside the tile: no straight vertical cuts at card edges
    trunks=[]
    for row,n,hs,dk in [('back',int(rng.integers(6,9)),0.92,0.55),('front',int(rng.integers(5,7)),1.0,1.0)]:
        hs_=[H*(0.50+0.42*rng.random())*hs if not (row=='front' and rng.random()<0.3) else H*(0.88+0.09*rng.random()) for _ in range(n)]
        for i,h in enumerate(hs_):
            w=h*(0.34+0.14*rng.random())
            lo=g+w*0.54; hi=W-g-w*0.54
            if hi<=lo: w=(W-2*g)/1.1; lo=hi=W/2
            x=lo+(hi-lo)*((i+0.15+0.7*rng.random())/n)
            pn=pal_names[0]
            if rust_frac>0 and rng.random()<rust_frac*(1.0 if (row=='back' or rust_frac>=1.0) else 0.5): pn='rust'
            pine(rng,cv,x,H-1-rng.random()*H*0.02,h,w,PAL[pn],snow=snow,dead=dead,dk=dk)
            trunks.append((x,w))
    # dense undergrowth between the outer trees (rounded ends, no hard cut)
    yy,xx=np.mgrid[0:Hb,0:Wb]/SS
    xl=min(x-w*0.30 for x,w in trunks); xr=max(x+w*0.30 for x,w in trunks)
    ridge=H*0.80+np.asarray(Image.fromarray(rng.random((1,48)).astype(np.float32),'F').resize((Wb,1),Image.BICUBIC))[0]*H*0.07+(rng.random(Wb)**4)*H*0.05
    xc=np.arange(Wb)/SS
    endfall=np.clip(np.minimum(xc-xl,xr-xc)/(W*0.10),0,1)
    ridge=H-(H-ridge)*np.sqrt(endfall)
    band=(yy>ridge[None,:]).astype(float)*(endfall[None,:]>0)
    pal={k:np.array(v,float) for k,v in PAL[pal_names[0]].items()}
    bt=np.clip((yy-ridge[None,:])/(H-ridge[None,:]+1e-3),0,1)
    bc=lerp(lerp(pal['mid'],pal['sh'],np.clip(bt*3,0,1)),pal['deep'],np.clip(bt*1.5-0.3,0,1))
    bc=bc*(0.85+0.3*(nzA-0.5))[...,None]
    newm=band*(1-al)
    rgb[:]=rgb*(1-newm[...,None])+bc*newm[...,None]; al[:]=np.maximum(al,band)
    mod=np.clip(0.92+0.10*(nzB-0.5),0.80,1.0)   # brush grain, darken-only
    out=np.dstack([np.clip(rgb*mod[...,None],0,255),al*255]).astype(np.uint8)
    return Image.fromarray(out,'RGBA').resize((W,H),Image.LANCZOS)

def bleed(im):
    a=np.asarray(im).astype(np.float32); m=a[...,3]>8
    idx=ndimage.distance_transform_edt(~m,return_distances=False,return_indices=True)
    a[...,:3]=a[...,:3][idx[0],idx[1]]
    return Image.fromarray(a.astype(np.uint8),'RGBA')

AUT=[dict(pal_names=['pine_autumn']),dict(pal_names=['pine_autumn'],rust_frac=0.35),dict(pal_names=['pine_autumn'],rust_frac=0.65),dict(pal_names=['pine_autumn'],rust_frac=1.0)]
VARIANTS={
 'kit_summer':[dict(pal_names=['summer'])]*4,
 'ring_summer':[dict(pal_names=['summer'])]*4,
 'kit_autumn':AUT,'ring_autumn':AUT,
 'kit_winter':[dict(pal_names=['kit_winter'],snow=0.45)]*4,
 'ring_winter':[dict(pal_names=['ring_winter'],snow=1.0)]*4,
 'kit_dead':[dict(pal_names=['dead'],dead=True)]*4,
}
SEEDKEY={'kit_summer':'summer','ring_summer':'summer','kit_autumn':'autumn','ring_autumn':'autumn','kit_dead':'dead'}
def build(key):
    atlas=Image.new('RGBA',(T*2,T*2))
    for i,v in enumerate(VARIANTS[key]):
        t=paint_tile(zlib.crc32(f'{SEEDKEY.get(key,key)}{i}'.encode()),**v)
        a=np.asarray(t).copy(); g=6; a[:,:g,3]=0; a[:,-g:,3]=0; a[:g,:,3]=0
        atlas.paste(Image.fromarray(a,'RGBA'),((i%2)*T,(i//2)*T))
    atlas=bleed(atlas)
    import json
    o=json.load(open('/tmp/orig_lum2.json'))[key]
    a=np.asarray(atlas).astype(np.float64); rgb=a[...,:3]/255
    lin=np.where(rgb<=0.04045,rgb/12.92,((rgb+0.055)/1.055)**2.4)
    m=a[...,3]>127; L=(lin@[0.2126,0.7152,0.0722])
    cal=m; oc=o
    if key.endswith('autumn'):   # calibrate the pines on the green cones (summer stats) so autumn greens are never lighter
        cal=m&~((lin[...,0]>1.6*lin[...,1])&(lin[...,0]>0.04)); oc=json.load(open('/tmp/orig_lum2.json'))[key.replace('autumn','summer')]
    tgt=0.92*oc['mean']/0.93
    gn=1.0
    try: tgt*=json.load(open('/workspace/treecards/render_gain.json')).get(key,1.0)
    except FileNotFoundError: pass
    for _ in range(40):
        Lg=np.minimum(L[cal]*gn,1); gn*=tgt/Lg.mean()
    gp5=o['p5']/max(np.percentile(L[m],5),1e-6)   # gain allowed at the black end
    knee=np.percentile(L[m],35); w=np.clip(L/knee,0,1)
    src=atlas
    for cap in [0.95,0.85,0.75,0.65,0.55,0.45,0.35,0.28,0.22,0.16,0.10]:
        g=np.minimum(gn,gp5*cap)*(1-w)+gn*w
        l2=np.clip(lin*g[...,None],0,1)
        srgb=np.where(l2<=0.0031308,l2*12.92,1.055*l2**(1/2.4)-0.055)
        b_=a.copy(); b_[...,:3]=np.round(srgb*255)
        atlas=Image.fromarray(b_.astype(np.uint8),'RGBA')
        q=atlas.quantize(colors=256,method=Image.Quantize.FASTOCTREE,dither=Image.Dither.NONE).convert('RGBA')
        qa=np.asarray(q).astype(float); qm=qa[...,3]>127; ql=qa[...,:3][qm]/255
        ql=np.where(ql<=0.04045,ql/12.92,((ql+0.055)/1.055)**2.4)@[0.2126,0.7152,0.0722]*0.93
        if np.percentile(ql,5)<=0.97*o['p5'] and ql.mean()<=o['mean']: break
    print(key,'gain',round(gn,2),'cap',cap,'p5',round(np.percentile(ql,5)/o['p5'],2),'mean',round(ql.mean()/o['mean'],2))
    atlas.save(f'atlas_{key}_full.png')
    q=atlas.quantize(colors=256,method=Image.Quantize.FASTOCTREE,dither=Image.Dither.NONE)
    pal=np.array(q.getpalette(rawmode='RGBA'),float).reshape(-1,4)
    pl=pal[:,:3]/255; pl=np.where(pl<=0.04045,pl/12.92,((pl+0.055)/1.055)**2.4)
    PL=pl@[0.2126,0.7152,0.0722]
    idx=np.asarray(q); amask=pal[idx][...,3]>127
    for sc in np.linspace(1,0.5,26):   # darken only the darkest palette entries until p5 <= original
        fac=np.where(PL*0.93<o['p5']*1.6,sc,1.0)
        p5=np.percentile((PL*fac)[idx][amask]*0.93,5)
        if p5<=0.97*o['p5']: break
    l2=pl*fac[:,None]; sr=np.where(l2<=0.0031308,l2*12.92,1.055*l2**(1/2.4)-0.055)
    pal[:,:3]=np.round(sr*255)
    q.putpalette(pal.astype(np.uint8).ravel().tolist(),rawmode='RGBA')
    q.save(f'atlas_{key}.png',optimize=True)
    print(key,'palette toe',round(float(sc),2))
    bg=Image.new('RGBA',atlas.size,(150,170,190,255)); bg.alpha_composite(atlas); bg.convert('RGB').resize((512,512)).save(f'/tmp/prev_{key}.jpg')
if __name__=='__main__':
    import sys
    from multiprocessing import Pool
    keys=sys.argv[1:] or list(VARIANTS)
    with Pool(7) as p: p.map(build,keys)
