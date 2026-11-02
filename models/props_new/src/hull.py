# clinker hull generator (ship frame: x=beam, s=length (+ = bow), z=up). Blender coords: (x, -s, z)
import numpy as np, math
class HullSpec:
    def __init__(s,L=13.0,B=1.6,keel_mid=-0.55,keel_rise=0.95,gun_mid=1.0,gun_rise=1.0,nst=8,ncol=48,th=0.035,tin=0.045,tend=0.985,bow_exp=2.4,stern_exp=2.4,bow_rake=0.0,stern_rake=0.0):
        s.__dict__.update(locals()); del s.__dict__['s']
    def B_(s,t):
        e=np.where(np.asarray(t)>0,s.bow_exp,s.stern_exp)
        return s.B*np.clip(1-np.abs(t)**e,0,1)**0.85
    def rake_s(s,t,v):  # planking ends follow a raked stem: shift ends outward with height
        a=abs(t); f=max(0.0,(a-0.6)/0.4)**2; r=s.bow_rake if t>0 else -s.stern_rake
        return r*f*max(v,0.0)**0.9
    def keel(s,t): return s.keel_mid+s.keel_rise*np.abs(t)**2.5
    def gun(s,t): return s.gun_mid+s.gun_rise*np.abs(t)**3
    def sec(s,t,v):
        b=s.B_(t); x=b*(1-(1-v)**2.2)**0.9; z=s.keel(t)+(s.gun(t)-s.keel(t))*v
        return x,z
    def nrm(s,t,v):
        e=1e-3; x0,z0=s.sec(t,max(v-e,0)); x1,z1=s.sec(t,min(v+e,1)); dx,dz=x1-x0,z1-z0; n=np.array([dz,-dx]); return n/max(np.linalg.norm(n),1e-9)
    def inner_halfwidth(s,t,z):
        vs=np.linspace(0,1,200); X=[s.sec(t,v) for v in vs]; xs=np.array([a for a,b in X]); zs=np.array([b for a,b in X])
        if z<=zs[0]: return 0.0
        return float(np.interp(z,zs,xs))-s.tin
def build(H,keep=None,lower_mat_strakes=3,side_sign=(1,-1)):
    """returns dict of (V,F,UV) lists keyed: 'outer_lo','outer_hi','inner','cap'. keep(side,k,j)->bool for strake k, column cell j"""
    T=np.linspace(-H.tend,H.tend,H.ncol+1); vb=np.linspace(0,1,H.nst+1)
    out={k:([],[],[]) for k in ('outer_lo','outer_hi','inner','cap')}
    def add(key,quads_pts,quads_uv,flip):
        V,F,UV=out[key]
        for P,U in zip(quads_pts,quads_uv):
            o=len(V); V.extend(P); UV.extend(U); f=[o,o+1,o+2,o+3]; F.append(f[::-1] if flip else f)
    def P(sd,t,v,off):
        x,z=H.sec(t,v); n=H.nrm(t,v); return (sd*(x+n[0]*off), -(t*H.L/2+H.rake_s(t,v)), z+n[1]*off)
    # girth param for uv (approx)
    for sd in side_sign:
        flip=(sd<0)
        for k in range(H.nst):
            key='outer_lo' if k<lower_mat_strakes else 'outer_hi'
            v0,v1=vb[k],vb[k+1]
            for j in range(H.ncol):
                if keep and not keep(sd,k,j): continue
                t0,t1=T[j],T[j+1]
                # band: bottom edge offset th (sticks out), top edge 0 ; quad (t0,v0)->(t1,v0)->(t1,v1)->(t0,v1)
                pts=[P(sd,t0,v0,H.th),P(sd,t1,v0,H.th),P(sd,t1,v1,0),P(sd,t0,v1,0)]
                g0=k*0.33; g1=(k+1)*0.33
                uv=[(g0,t0*H.L/2/2.5),(g0,t1*H.L/2/2.5),(g1,t1*H.L/2/2.5),(g1,t0*H.L/2/2.5)]
                add(key,[pts],[uv],not flip)
                # step under this strake's lower edge: from previous strake top (off 0) to this bottom (off th)
                if k>0:
                    sp=[P(sd,t0,v0,0),P(sd,t1,v0,0),P(sd,t1,v0,H.th),P(sd,t0,v0,H.th)]
                    add(key,[sp],[[(g0-0.02,u[1]) for u in uv[:2]]+[(g0,u[1]) for u in uv[:2]][::-1]],not flip)
                # inner skin
                ip=[P(sd,t0,v0,-H.tin),P(sd,t1,v0,-H.tin),P(sd,t1,v1,-H.tin),P(sd,t0,v1,-H.tin)]
                add('inner',[ip],[uv],flip)
                if k==H.nst-1:
                    cp=[P(sd,t0,1,0),P(sd,t1,1,0),P(sd,t1,1,-H.tin),P(sd,t0,1,-H.tin)]
                    add('cap',[cp],[[(0,uv[0][1]),(0,uv[1][1]),(0.05,uv[1][1]),(0.05,uv[0][1])]],flip)
    return out
