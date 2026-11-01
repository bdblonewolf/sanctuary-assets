# Procedural material recipes (baked into the 1024 atlas). exec() after lib_bl.py.
SWD=SRC+'/swatch/'
MATS={}   # name -> dict(base,rough,metal,alpha,normal sockets, cards flag)
def lin(c): return tuple((x**2.2) for x in c)+(1.0,)
class NB:
    def __init__(s,name,cards=False):
        m=bpy.data.materials.new(name); m.use_nodes=True; s.m=m; s.nt=m.node_tree; s.nt.nodes.clear()
        s.out=s.nt.nodes.new('ShaderNodeOutputMaterial'); s._tc=None; s.cards=cards
    def set(s,sock,v):
        if isinstance(v,bpy.types.NodeSocket): s.nt.links.new(v,sock); return
        if sock.type=='RGBA' and len(v)==3: v=lin(v)
        sock.default_value=v
    def node(s,t,ins=None,**props):
        n=s.nt.nodes.new(t)
        for k,v in props.items(): setattr(n,k,v)
        for k,v in (ins or {}).items(): s.set(n.inputs[k],v)
        return n
    def obj(s):
        if s._tc is None: s._tc=s.node('ShaderNodeTexCoord')
        return s._tc.outputs['Object']
    def uv(s,name='UVMap'):
        return s.node('ShaderNodeUVMap',uv_map=name).outputs[0]
    def vscale(s,v,sc):
        return s.node('ShaderNodeMapping',{'Vector':v or s.obj(),'Scale':sc}).outputs[0]
    def noise(s,scale,detail=4.0,rough=0.55,vec=None,distort=0.0,dims='3D'):
        return s.node('ShaderNodeTexNoise',{'Vector':vec or s.obj(),'Scale':scale,'Detail':detail,'Roughness':rough,'Distortion':distort},noise_dimensions=dims).outputs['Fac']
    def vor(s,scale,vec=None,feat='F1',rnd=1.0):
        n=s.node('ShaderNodeTexVoronoi',{'Vector':vec or s.obj(),'Scale':scale,'Randomness':rnd},feature=feat); return n.outputs['Distance']
    def wave(s,scale,vec=None,axis='X',dist=2.0,detail=2.0,kind='BANDS'):
        return s.node('ShaderNodeTexWave',{'Vector':vec or s.obj(),'Scale':scale,'Distortion':dist,'Detail':detail},wave_type=kind,bands_direction=axis).outputs['Fac']
    def math(s,op,a,b=0.0,c=None,clamp=False):
        n=s.node('ShaderNodeMath',operation=op,use_clamp=clamp); s.set(n.inputs[0],a); s.set(n.inputs[1],b)
        if c is not None: s.set(n.inputs[2],c)
        return n.outputs[0]
    def mapr(s,x,a,b,c=0.0,d=1.0,clamp=True,interp='LINEAR'):
        return s.node('ShaderNodeMapRange',{'Value':x,'From Min':a,'From Max':b,'To Min':c,'To Max':d},clamp=clamp,interpolation_type=interp).outputs[0]
    def sstep(s,x,a,b): return s.mapr(x,a,b,0,1,True,'SMOOTHSTEP')
    def mix(s,f,a,b,blend='MIX'):
        n=s.node('ShaderNodeMix',data_type='RGBA',blend_type=blend,clamp_result=True); s.set(n.inputs[0],f); s.set(n.inputs[6],a); s.set(n.inputs[7],b); return n.outputs[2]
    def mixf(s,f,a,b):
        n=s.node('ShaderNodeMix',data_type='FLOAT'); s.set(n.inputs[0],f); s.set(n.inputs[2],a); s.set(n.inputs[3],b); return n.outputs[0]
    def attr(s,name): return s.node('ShaderNodeAttribute',attribute_name=name,attribute_type='GEOMETRY').outputs['Fac']
    def ell(s,c,r,soft=0.35):
        v=s.node('ShaderNodeMapping',{'Vector':s.obj(),'Location':tuple(-c[i]/r[i] for i in range(3)),'Scale':tuple(1/x for x in r)}).outputs[0]
        l=s.node('ShaderNodeVectorMath',{0:v},operation='LENGTH').outputs['Value']
        return s.mapr(l,1-soft,1.0,1.0,0.0,True,'SMOOTHSTEP')
    def zband(s,z0,z1):  # 0 below z0, 1 above z1 (object z)
        sep=s.node('ShaderNodeSeparateXYZ',{0:s.obj()})
        return s.sstep(sep.outputs['Z'],z0,z1)
    def axis(s,k): return s.node('ShaderNodeSeparateXYZ',{0:s.obj()}).outputs[k]
    def maxf(s,*xs):
        o=xs[0]
        for x in xs[1:]: o=s.math('MAXIMUM',o,x)
        return o
    def bump(s,h,strength=0.3,dist=0.002,normal=None):
        n=s.node('ShaderNodeBump',{'Strength':strength,'Distance':dist,'Height':h})
        if normal is not None: s.set(n.inputs['Normal'],normal)
        return n.outputs[0]
    def tex(s,name,scale,blend=0.3,cs='Non-Color'):
        n=s.node('ShaderNodeTexImage',{'Vector':s.vscale(None,(scale,scale,scale))},projection='BOX',projection_blend=blend)
        n.image=bpy.data.images.load(SWD+name,check_existing=True); n.image.colorspace_settings.name=cs
        return n
    def swatch(s,base,sw,scale,amt=0.8):
        """photo swatch detail: overlay (0.5 neutral) on the procedural base, returns (base, height 0..1)"""
        d=s.tex(sw+'_det.png',scale).outputs['Color']; h=s.tex(sw+'_h.png',scale).outputs['Color']
        h=s.node('ShaderNodeSeparateColor',{0:h}).outputs[0]
        return s.mix(amt,base,d,'OVERLAY'),h
    def seam(s): return s.attr('seam')
    def stitch(s,base,h,thread=(0.30,0.24,0.17),d0=0.0045,d1=0.0085,scale=210,wear=None,wear_amt=0.5):
        """stitched seam lines running along garment edges (attribute 'seam' = distance to edge, metres) + edge wear"""
        sd=s.seam()
        band=s.math('MULTIPLY',s.sstep(sd,d0-0.0012,d0),s.math('SUBTRACT',1.0,s.sstep(sd,d1,d1+0.0012)))
        dots=s.math('SUBTRACT',1.0,s.sstep(s.vor(scale,rnd=0.15),0.22,0.34))
        st=s.math('MULTIPLY',band,dots)
        groove=s.math('MULTIPLY',band,s.math('SUBTRACT',1.0,dots))
        base=s.mix(s.math('MULTIPLY',groove,0.45),base,(0.03,0.025,0.02),'MULTIPLY')
        base=s.mix(st,base,thread)
        edge=s.math('SUBTRACT',1.0,s.sstep(sd,0.0,0.0035))
        if wear is not None: base=s.mix(s.math('MULTIPLY',edge,wear_amt),base,wear)
        h=s.math('ADD',h,s.math('MULTIPLY',st,0.9)); h=s.math('SUBTRACT',h,s.math('MULTIPLY',groove,0.7))
        h=s.math('SUBTRACT',h,s.math('MULTIPLY',edge,0.8))
        return base,h,s.math('MAXIMUM',st,edge)
    def folds(s,amt=1.0,vert=6.0,scale=9.0):
        """anisotropic crease noise: long vertical folds (hanging cloth) + cross wrinkles"""
        v=s.noise(scale,4,0.55,vec=s.vscale(None,(1.0,1.0,1.0/vert)),distort=0.6)
        c=s.noise(scale*2.2,3,0.5,vec=s.vscale(None,(0.5,0.5,1.6)))
        f=s.math('ADD',s.math('MULTIPLY',s.math('ABSOLUTE',s.math('SUBTRACT',v,0.5)),-2.0*amt),s.math('MULTIPLY',c,0.5*amt))
        return f
    def finish(s,base,rough,metal=0.0,normal=None,alpha=1.0,sss=0.0):
        b=s.node('ShaderNodeBsdfPrincipled'); s.set(b.inputs['Base Color'],base); s.set(b.inputs['Roughness'],rough); s.set(b.inputs['Metallic'],metal)
        if normal is not None: s.set(b.inputs['Normal'],normal)
        s.set(b.inputs['Alpha'],alpha)
        if sss: b.inputs['Subsurface Weight'].default_value=sss; b.inputs['Subsurface Radius'].default_value=(0.9,0.45,0.3); b.inputs['Subsurface Scale'].default_value=0.004
        s.nt.links.new(b.outputs[0],s.out.inputs[0])
        def sock(v):
            if isinstance(v,bpy.types.NodeSocket): return v
            if isinstance(v,(tuple,list)):
                n=s.node('ShaderNodeRGB'); n.outputs[0].default_value=lin(v) if len(v)==3 else v; return n.outputs[0]
            n=s.node('ShaderNodeValue'); n.outputs[0].default_value=v; return n.outputs[0]
        MATS[s.m.name]=dict(base=sock(base),rough=sock(rough),metal=sock(metal),alpha=sock(alpha),bsdf=b,cards=s.cards,out=s.out)
        s.m.blend_method='HASHED' if s.cards else 'OPAQUE'
        return s.m
# ---------------------------------------------------------------- recipes
def m_cloth(name,ca,cb,weave=420.0,grime=0.5,dirt=(0.16,0.13,0.10),hem_z=None,hem_h=0.25,stain=0.4,rough=0.88,fade=None,trim=None,soot=0.0,ink=0.0,
            sw='linen',sws=6.0,swamt=0.85,fold=1.0,foldv=5.0,stitch=True,thread=None,fray=(0.06,0.05,0.045)):
    s=NB(name); x=s.obj()
    n1=s.noise(6,5,0.6); n2=s.noise(40,3,0.5)
    base=s.mix(s.mapr(n1,0.3,0.7),ca,cb)
    if fade is not None:   # sun-faded/washed-out blotches
        base=s.mix(s.math('MULTIPLY',s.sstep(s.noise(2.5,3,0.5),0.48,0.68),fade[1]),base,fade[0])
    base,hs=s.swatch(base,sw,sws,swamt)
    fo=s.folds(fold,foldv)
    # dirt collects in fold valleys
    g=s.math('MULTIPLY',s.sstep(s.noise(3.0,6,0.62),0.45,0.75),grime)
    g=s.math('MAXIMUM',g,s.math('MULTIPLY',s.sstep(s.math('MULTIPLY',fo,-1.0),0.25,0.8),grime*0.6))
    if hem_z is not None: g=s.math('MAXIMUM',g,s.math('MULTIPLY',s.math('SUBTRACT',1.0,s.zband(hem_z,hem_z+hem_h)),0.85))
    base=s.mix(g,base,dirt)
    st=s.math('MULTIPLY',s.sstep(s.math('SUBTRACT',1.0,s.vor(7.0)),0.86,0.95),stain)
    base=s.mix(st,base,(0.10,0.085,0.07))
    if soot: base=s.mix(s.math('MULTIPLY',s.sstep(s.noise(4.0,6,0.7),0.5,0.72),soot),base,(0.035,0.03,0.028))
    if trim is not None: base=s.mix(trim[0](s),base,trim[1])
    if ink:   # blue-black ink blots / soaked edges
        ik=s.math('MULTIPLY',s.sstep(s.noise(9.0,5,0.68),0.47,0.60),ink)
        base=s.mix(ik,base,(0.025,0.028,0.045))
    h=s.math('ADD',s.math('MULTIPLY',hs,1.2),s.math('MULTIPLY',fo,2.2))
    h=s.math('ADD',h,s.math('MULTIPLY',s.noise(11,4,0.62),0.8))
    sm_=0.0
    if stitch:
        base,h,sm_=s.stitch(base,h,thread or tuple(min(1,c*1.6+0.04) for c in ca),d0=0.006,d1=0.009,scale=170,wear=fray,wear_amt=0.55)
    nrm=s.bump(h,0.55,0.0035)
    rr=s.mapr(hs,0,1,rough-0.08,min(rough+0.06,1.0))
    return s.finish(base,rr,0.0,nrm)
def m_leather(name,col,scorch=0.0,wear=0.5,rough=0.62,dark=0.5,soot=0.0,sw='leather_dark',sws=4.0,swamt=0.9,stitch=True,
              thread=(0.34,0.27,0.19),oil=0.5,fold=0.6,burns=0.0):
    s=NB(name)
    n1=s.noise(9,5,0.6); n2=s.noise(55,4,0.55)
    c2=tuple(c*dark for c in col)
    base=s.mix(s.mapr(n1,0.3,0.75),col,c2)
    base=s.mix(s.math('MULTIPLY',s.mapr(n2,0.55,0.8),0.35),base,tuple(min(1,c*1.5) for c in col))
    base,hs=s.swatch(base,sw,sws,swamt)
    pt=s.node('ShaderNodeNewGeometry').outputs['Pointiness']
    wm=s.math('MULTIPLY',s.sstep(pt,0.52,0.6),wear)
    base=s.mix(wm,base,tuple(min(1,c*1.9+0.03) for c in col))
    if scorch:
        sc=s.noise(3.2,6,0.7); m1=s.math('MULTIPLY',s.sstep(sc,0.56,0.66),scorch); m2=s.math('MULTIPLY',s.sstep(sc,0.50,0.58),scorch)
        base=s.mix(m2,base,(0.20,0.09,0.035)); base=s.mix(m1,base,(0.025,0.02,0.018))
    bm_=0.0
    if burns:   # small burn pits (spark holes): dark charred rings with a glossy-dark centre
        bv=s.vor(38,rnd=1.0); bn=s.sstep(s.noise(5,3,0.5),0.5,0.62)
        bm_=s.math('MULTIPLY',s.math('SUBTRACT',1.0,s.sstep(bv,0.05,0.11)),s.math('MULTIPLY',bn,burns))
        rim=s.math('MULTIPLY',s.math('SUBTRACT',1.0,s.sstep(bv,0.10,0.2)),s.math('MULTIPLY',bn,burns*0.8))
        base=s.mix(rim,base,(0.16,0.07,0.03)); base=s.mix(bm_,base,(0.012,0.01,0.009))
    if soot: base=s.mix(s.math('MULTIPLY',s.sstep(s.noise(5.0,6,0.7),0.48,0.7),soot),base,(0.03,0.028,0.026))
    cr=s.sstep(s.noise(18,6,0.7,distort=0.4),0.55,0.72)
    fo=s.folds(fold,3.0,7.0)
    h=s.math('ADD',s.math('MULTIPLY',hs,1.5),s.math('MULTIPLY',cr,-0.5)); h=s.math('ADD',h,s.math('MULTIPLY',fo,1.6))
    if burns: h=s.math('SUBTRACT',h,s.math('MULTIPLY',bm_,1.2))
    em=0.0
    if stitch: base,h,em=s.stitch(base,h,thread,wear=tuple(min(1,c*2.0+0.04) for c in col),wear_amt=wear*0.8)
    # oily (glossy) where smooth & handled, matte+dry in scuffs, creases and stitched edges
    rr=s.mapr(n2,0,1,rough-0.12*oil,rough+0.1)
    rr=s.mixf(s.math('MAXIMUM',wm,cr),rr,min(rough+0.22,0.95))
    if scorch: rr=s.mixf(s.math('MULTIPLY',s.sstep(s.noise(3.2,6,0.7),0.5,0.6),scorch),rr,0.9)
    return s.finish(base,rr,0.0,s.bump(s.math('ADD',h,s.math('MULTIPLY',s.noise(16,5,0.65),0.6)),0.6,0.003))
def m_iron(name,col=(0.10,0.095,0.09),rust=0.4,rough=0.55,hot=None):
    s=NB(name)
    n=s.noise(14,6,0.65); r=s.math('MULTIPLY',s.sstep(s.noise(6,6,0.7),0.55,0.7),rust)
    base=s.mix(s.mapr(n,0.3,0.7),col,tuple(c*1.6 for c in col))
    base=s.mix(r,base,(0.24,0.12,0.06))
    met=s.mapr(r,0,1,0.9,0.15)
    if hot is not None:
        hm=hot(s); base=s.mix(hm,base,(1.0,0.42,0.08)); met=s.mixf(hm,met,0.0)
    h=s.math('ADD',s.vor(70),s.math('MULTIPLY',n,0.5))
    return s.finish(base,s.mixf(r,s.mapr(n,0,1,rough-0.12,rough+0.1),0.9),met,s.bump(s.math('ADD',h,s.math('MULTIPLY',s.noise(20,4,0.6),1.2)),0.45,0.0025))
def m_wood(name,col=(0.24,0.16,0.09),axis='Z'):
    s=NB(name)
    w=s.wave(30,vec=s.vscale(None,(6,6,0.6) if axis=='Z' else (0.6,6,6)),axis='X',dist=6,detail=4)
    n=s.noise(30,4,0.5)
    base=s.mix(s.mapr(w,0.2,0.9),col,tuple(c*0.55 for c in col))
    base=s.mix(s.math('MULTIPLY',s.mapr(n,0.4,0.8),0.5),base,(0.07,0.05,0.035))
    return s.finish(base,0.7,0.0,s.bump(s.math('ADD',w,n),0.2,0.001))
def m_flat(name,col,rough=0.6,metal=0.0,cards=False):
    s=NB(name,cards); return s.finish(col,rough,metal)
# ---------------------------------------------------------------- skin / eyes / hair
def m_skin(name,L,tone,mott=(0.5,0.32,0.26),lip=(0.42,0.24,0.21),red=0.35,socket=(0.30,0.2,0.2),socket_amt=0.35,
           brow=(0.09,0.07,0.06),brow_amt=0.85,stub=(0.20,0.17,0.15),stub_amt=0.55,soot=0.0,ink=0.0,age=0.5,grime=0.3,skin_det=0.55):
    s=NB(name)
    n1=s.noise(22,5,0.6); n2=s.noise(4,3,0.5); fine=s.noise(380,2,0.5)
    base=s.mix(s.math('MULTIPLY',s.mapr(n1,0.35,0.7),0.55),tone,mott)
    base=s.mix(s.math('MULTIPLY',s.mapr(n2,0.3,0.7),0.35),base,tuple(c*0.8 for c in tone))
    ex=L['eye_x']; ez=L['eye_z']; ef=L['eyeL_front']; m=L['mouth']; nz=L['nose']; hc=L['head_c']; rx=L['head_rx']
    yF=ef[1]
    rd=s.maxf(s.ell((ex+0.01,yF+0.012,ez-0.032),(0.022,0.03,0.02),0.8),s.ell((-ex-0.01,yF+0.012,ez-0.032),(0.022,0.03,0.02),0.8),
              s.ell(tuple(nz),(0.012,0.02,0.012),0.8),s.ell((rx,hc[1],ez-0.01),(0.02,0.03,0.035),0.7),s.ell((-rx,hc[1],ez-0.01),(0.02,0.03,0.035),0.7))
    base=s.mix(s.math('MULTIPLY',rd,red),base,(0.55,0.24,0.2))
    sock=s.maxf(s.ell((ex,yF+0.004,ez-0.004),(0.021,0.02,0.016),0.6),s.ell((-ex,yF+0.004,ez-0.004),(0.021,0.02,0.016),0.6))
    base=s.mix(s.math('MULTIPLY',sock,socket_amt),base,socket,'MULTIPLY')
    lp=s.ell((m[0],m[1]+0.004,m[2]),(0.023,0.02,0.0085),0.55)
    base=s.mix(s.math('MULTIPLY',lp,0.75),base,lip)
    st=s.math('MULTIPLY',s.attr('stubble'),s.mapr(fine,0.3,0.6,0.4,1.0))
    base=s.mix(s.math('MULTIPLY',st,stub_amt),base,stub)
    bn=s.noise(160,3,0.6,vec=s.vscale(None,(1.0,1.0,3.0)))
    bw=s.maxf(s.ell((ex+0.004,yF+0.006,ez+0.0185),(0.024,0.03,0.0062),0.5),s.ell((-ex-0.004,yF+0.006,ez+0.0185),(0.024,0.03,0.0062),0.5))
    base=s.mix(s.math('MULTIPLY',s.math('MULTIPLY',bw,s.mapr(bn,0.3,0.65)),brow_amt),base,brow)
    if soot:
        sm=s.math('MULTIPLY',s.attr('soot'),s.sstep(s.math('ADD',s.noise(9,6,0.7),s.math('MULTIPLY',s.attr('soot'),0.25)),0.45,0.62))
        base=s.mix(s.math('MULTIPLY',sm,soot),base,(0.05,0.042,0.038))
    if ink:
        im=s.math('MULTIPLY',s.attr('ink'),s.sstep(s.noise(14,5,0.7),0.42,0.55))
        base=s.mix(s.math('MULTIPLY',im,ink),base,(0.03,0.035,0.06))
    base=s.mix(s.math('MULTIPLY',s.sstep(s.noise(2.5,5,0.6),0.5,0.75),grime),base,(0.25,0.19,0.15),'MULTIPLY')
    base,hs=s.swatch(base,'skin',13.0,skin_det)
    wr=s.math('MULTIPLY',s.ell((0,yF,ez+0.045),(0.05,0.04,0.022),0.6),s.wave(260,axis='Z',dist=3,detail=1))
    # character lines: nasolabial folds, crow's feet, under-eye bags, frown lines (painted cavity + height)
    lines=[]
    for sg in (1,-1):
        for t in (0.0,0.33,0.66,1.0):
            a_=(sg*(abs(nz[0])+0.019),nz[1]+0.012,nz[2]-0.004); b_=(sg*(abs(m[0])+0.026),m[1]+0.010,m[2]-0.010)
            c_=tuple(a_[i]+(b_[i]-a_[i])*t for i in range(3)); lines.append(s.ell(c_,(0.0034,0.03,0.0075),0.9))
    nl=s.maxf(*lines)
    cf=s.math('MULTIPLY',s.maxf(s.ell((ex+0.028,yF+0.02,ez),(0.011,0.03,0.013),0.8),s.ell((-ex-0.028,yF+0.02,ez),(0.011,0.03,0.013),0.8)),
                     s.wave(330,axis='Z',dist=4,detail=1))
    bags=s.maxf(s.ell((ex,yF+0.004,ez-0.017),(0.016,0.03,0.0055),0.8),s.ell((-ex,yF+0.004,ez-0.017),(0.016,0.03,0.0055),0.8))
    frown=s.math('MULTIPLY',s.ell((0,yF,ez+0.018),(0.012,0.04,0.014),0.8),s.wave(420,axis='X',dist=2,detail=1))
    cav=s.math('MULTIPLY',s.maxf(nl,s.math('MULTIPLY',cf,0.7),s.math('MULTIPLY',bags,0.6),s.math('MULTIPLY',frown,0.6)),age)
    base=s.mix(s.math('MULTIPLY',cav,0.45),base,tuple(c*0.62 for c in tone),'MIX')
    base=s.mix(s.math('MULTIPLY',cav,0.35),base,(0.5,0.3,0.27),'MULTIPLY')
    h=s.math('ADD',s.math('MULTIPLY',fine,0.25),s.math('MULTIPLY',wr,age))
    h=s.math('ADD',h,s.math('MULTIPLY',hs,0.9)); h=s.math('SUBTRACT',h,s.math('MULTIPLY',cav,1.6))
    rough=s.mapr(n1,0,1,0.48,0.62); rough=s.mixf(lp,rough,0.38)
    rough=s.mixf(s.math('MULTIPLY',cav,0.6),rough,0.7)
    return s.finish(base,rough,0.0,s.bump(h,0.35,0.0015),sss=0.08)
def m_eye(name,L,iris=(0.25,0.2,0.14),sclera=(0.72,0.66,0.6)):
    s=NB(name)
    out=sclera
    vein=s.sstep(s.noise(60,6,0.7,distort=1.5),0.62,0.7)
    out=s.mix(s.math('MULTIPLY',vein,0.5),out,(0.6,0.25,0.22))
    for k in ('eyeL_front','eyeR_front'):
        f=L[k]; c=(f[0],f[1]+0.002,f[2])
        ir=s.ell(c,(0.0062,0.02,0.0062),0.12); pu=s.ell(c,(0.0026,0.02,0.0026),0.25); lr=s.ell(c,(0.0068,0.02,0.0068),0.06)
        irc=s.mix(s.noise(400,3,0.6),iris,tuple(min(1,x*1.7) for x in iris))
        out=s.mix(s.math('MULTIPLY',lr,0.9),out,(0.05,0.04,0.035)); out=s.mix(ir,out,irc); out=s.mix(pu,out,(0.01,0.01,0.01))
    return s.finish(out,0.12,0.0)
def m_hair(name,col,grey=0.2,greycol=(0.42,0.40,0.38),strands_img=None,shell=False,stretch=(1,1,0.12),scale=420.0,root_dark=0.55,shell_dark=0.75):
    """one material for a hair object = shell faces (procedural streaks, 'hedge' alpha) + strand cards (attribute 'card'>0.5,
    strand texture in UVMap space, root at v=1)."""
    s=NB(name,cards=True)
    streak=s.noise(scale,2,0.5,vec=s.vscale(None,stretch))
    e=s.math('ADD',s.attr('hedge'),s.math('MULTIPLY',s.math('SUBTRACT',s.noise(420,2,0.5,vec=s.vscale(None,stretch)),0.5),0.45))
    a_sh=s.sstep(e,0.42,0.52); v_sh=s.math('MULTIPLY',streak,shell_dark)
    if strands_img is None: strands_img=SWD+'strands.png'
    uvn=s.uv('UVMap')
    t=s.node('ShaderNodeTexImage',{'Vector':uvn}); t.image=bpy.data.images.load(strands_img,check_existing=True); t.image.colorspace_settings.name='Non-Color'
    v_c=s.node('ShaderNodeSeparateColor',{0:t.outputs['Color']}).outputs[0]
    vv=s.node('ShaderNodeSeparateXYZ',{0:uvn}).outputs['Y']
    v_c=s.math('MULTIPLY',v_c,s.mapr(vv,1.0,0.6,1.0-root_dark,1.0))     # darker roots
    card=s.sstep(s.attr('card'),0.4,0.6)
    v=s.mixf(card,v_sh,v_c); a=s.mixf(card,a_sh,t.outputs['Alpha'])
    base=s.mix(s.mapr(v,0.1,0.95),tuple(c*0.45 for c in col),tuple(min(1,c*1.6) for c in col))
    gm=s.math('MULTIPLY',s.sstep(s.noise(900,2,0.5,vec=s.vscale(None,stretch)),0.55,0.68),grey)
    gm=s.mixf(card,gm,s.math('MULTIPLY',s.sstep(s.noise(60,2,0.5),0.45,0.62),grey))
    base=s.mix(gm,base,greycol)
    return s.finish(base,s.mapr(v,0,1,0.8,0.5),0.0,s.bump(v,0.4,0.002),a)
