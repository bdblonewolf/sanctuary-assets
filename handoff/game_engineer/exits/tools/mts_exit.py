import json,math,collections,numpy as np
from mts import M,PL,SOL,WAT,LIFE,W,H
OX,OY=M['origin']
CTRL=[(81.0,147.0),(79.9,149.0),(75.5,149.9),(68.5,150.2),(61.0,150.3),(55.0,150.7),(51.0,151.5),(49.2,153.6)]
def catmull(P,n=8):
    out=[];P=[P[0]]+P+[P[-1]]
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=map(np.array,P[i-1:i+3])
        for k in range(n):
            t=k/n;out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t**3))
    out.append(np.array(P[-2]));return [tuple(map(float,p)) for p in out]
TRAIL=catmull(CTRL)
WIDTH=4.0
NEW_EXIT=dict(x=49.6,y=152.4); ARRIVE=[53.8,150.9]
def dist_solid(x,y,r=4):
    best=9
    for yy in range(int(y)-r,int(y)+r+1):
        for xx in range(int(x)-r,int(x)+r+1):
            if 0<=xx<W and 0<=yy<H and SOL[yy,xx]:
                dx=max(xx-x,0,x-(xx+1));dy=max(yy-y,0,y-(yy+1));best=min(best,math.hypot(dx,dy))
    return best
def checks():
    r={}
    ds=[dist_solid(x,y) for x,y in TRAIL if y>149.3]   # earlier points sit in the 2 m gate mouth (towers either side)
    r['trail_min_clear_to_solid_m']=round(min(ds),2)
    r['trail_min_clear_gate_mouth_m']=round(min(dist_solid(x,y) for x,y in TRAIL if y<=149.3),2)
    r['trail_min_clear_to_life_props_m']=round(min(math.hypot(x-a,y-b) for x,y in TRAIL for a,b,k in LIFE),2)
    r['trail_inside_map']=all(0<x<W and 0<y<H for x,y in TRAIL)
    # walk BFS on 0.25 m grid with hero radius .2 + life props as 0.5 m discs
    st=.25;nx,ny=int(W/st),int(H/st)
    def blk(px,py):
        for ox,oy in((0,0),(.2,0),(-.2,0),(0,.2),(0,-.2)):
            tx,ty=int(px+ox),int(py+oy)
            if not(0<=tx<W and 0<=ty<H) or SOL[ty,tx]: return True
        return any(math.hypot(px-a,py-b)<.7 for a,b,k in LIFE if abs(px-a)<1 and abs(py-b)<1)
    s=(int(M['spawn'][0]/st),int(M['spawn'][1]/st));seen={s};q=collections.deque([s])
    while q:
        c=q.popleft()
        for d in((1,0),(-1,0),(0,1),(0,-1)):
            n=(c[0]+d[0],c[1]+d[1])
            if n in seen or not(0<=n[0]<nx and 0<=n[1]<ny) or blk((n[0]+.5)*st,(n[1]+.5)*st): continue
            seen.add(n);q.append(n)
    def ok(p,rad=1.2): return any((int((p[0]+dx)/st),int((p[1]+dy)/st)) in seen for dx in np.arange(-rad,rad+.01,.25) for dy in np.arange(-rad,rad+.01,.25))
    r['spawn_reaches_new_coast_exit']=ok((NEW_EXIT['x'],NEW_EXIT['y']))
    r['spawn_reaches_arrival']=ok(ARRIVE,.3)
    r['spawn_reaches_all_exits']={e['to']:ok((e['x'],e['y'])) for e in M['exits']}
    r['spawn_reaches_npcs']={k:ok(v) for k,v in M['npcs'].items()}
    r['trail_samples_blocked']=sum(blk(x,y) for x,y in TRAIL[2:])
    return r
if __name__=='__main__':
    print(json.dumps(checks(),indent=1))
