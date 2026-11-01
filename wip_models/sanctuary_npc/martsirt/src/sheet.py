# contact sheet: python3 sheet.py <prefix> <out.jpg>  (labelled, clip rows x frames)
import sys,glob,re
from PIL import Image,ImageDraw,ImageFont
pre,out=sys.argv[1],sys.argv[2]; fs=sorted(glob.glob(pre+'_clip_*_*.png'))
clips={}
for f in fs:
    m=re.match(re.escape(pre)+r'_clip_(.+)_(\d+)\.png',f); clips.setdefault(m[1],[]).append(f)
order=['idle','walk','talk','sit','sit_talk','work_hammer','work_write','sleep']
names=[c for c in order if c in clips]+[c for c in clips if c not in order]
tw,th=320,427; cols=4; cells=[(n,i,f) for n in names for i,f in enumerate(sorted(clips[n]))]
rows=(len(cells)+cols-1)//cols; S=Image.new('RGB',(cols*tw,rows*th),(20,18,16)); d=ImageDraw.Draw(S)
try: ft=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
except: ft=ImageFont.load_default()
for k,(n,i,f) in enumerate(cells):
    im=Image.open(f).convert('RGB').resize((tw,th)); x,y=(k%cols)*tw,(k//cols)*th; S.paste(im,(x,y)); d.text((x+8,y+6),f'{n} #{i+1}',fill=(240,220,180),font=ft)
S.save(out,quality=88); print('SHEET',out,len(cells))
