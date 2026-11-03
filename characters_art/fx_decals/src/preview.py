import json, numpy as np
from PIL import Image, ImageDraw
O='/workspace/sanctuary_art/fx_decals/'; T=O+'textures/'
fl=Image.open('/workspace/sanctuary_env/backup_v4_2_cleanup/outdoor/src_tex/dry_ground_rocks_diff.jpg').convert('RGB').resize((320,320))
fl=Image.fromarray((np.asarray(fl,float)*0.35).astype(np.uint8))
names=[s[0] for s in json.load(open(O+'src/spec.json'))]+['lava_tile']
C=5; W=320; sheet=Image.new('RGB',(C*W,((len(names)+C-1)//C)*(W+24)),(10,10,10)); d=ImageDraw.Draw(sheet)
for i,n in enumerate(names):
    t=fl.copy().convert('RGBA'); bc=Image.open(T+n+'_bc.png').convert('RGBA').resize((W,W))
    if n=='lava_tile': t=bc
    else:
        t.alpha_composite(bc)
        try:
            e=np.asarray(Image.open(T+n+'_e.png').convert('RGB').resize((W,W)),float)*np.asarray(bc,float)[...,3:]/255
            t=Image.fromarray(np.clip(np.asarray(t.convert('RGB'),float)+e*0.6,0,255).astype(np.uint8)).convert('RGBA')
        except FileNotFoundError: pass
    x,y=(i%C)*W,(i//C)*(W+24); sheet.paste(t.convert('RGB'),(x,y)); d.text((x+6,y+W+5),n,fill=(200,190,170))
sheet.save(O+'preview_sheet.png')
