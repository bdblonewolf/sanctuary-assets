def build_proc(role,coat,cfg):
    C=cfg['coat_colors'][coat]
    m=bpy.data.materials.new(f'proc_{role}_{coat}'); m.use_nodes=True; nt=m.node_tree; N=nt.nodes; Lk=nt.links
    p=N['Principled BSDF']
    def node(t,**kw):
        n=N.new(t)
        for k,v in kw.items(): setattr(n,k,v)
        return n
    def ramp(inp,stops):
        r=node('ShaderNodeValToRGB'); cr=r.color_ramp
        cr.elements[0].position=stops[0][0]; cr.elements[0].color=stops[0][1]
        cr.elements[1].position=stops[-1][0]; cr.elements[1].color=stops[-1][1]
        for pos,col in stops[1:-1]:
            e=cr.elements.new(pos); e.color=col
        Lk.new(inp,r.inputs[0]); return r
    def mix(a,b,fac,mode='MIX'):
        mx=node('ShaderNodeMix',data_type='RGBA',blend_type=mode); 
        if isinstance(fac,float): mx.inputs[0].default_value=fac
        else: Lk.new(fac,mx.inputs[0])
        for i,v in ((6,a),(7,b)):
            if isinstance(v,tuple): mx.inputs[i].default_value=v
            else: Lk.new(v,mx.inputs[i])
        return mx.outputs[2]
    tc=node('ShaderNodeTexCoord'); S=cfg.get('tex_scale',1.0)
    obj=tc.outputs['Object']
    # fur strand coords: stretched along body (Y)
    mp=node('ShaderNodeMapping'); Lk.new(obj,mp.inputs[0]); mp.inputs['Scale'].default_value=(90*S,14*S,90*S)
    fn=node('ShaderNodeTexNoise'); fn.inputs['Scale'].default_value=1.0; fn.inputs['Detail'].default_value=8; fn.inputs['Roughness'].default_value=0.7; Lk.new(mp.outputs[0],fn.inputs['Vector'])
    big=node('ShaderNodeTexNoise'); big.inputs['Scale'].default_value=4*S; big.inputs['Detail'].default_value=4; Lk.new(obj,big.inputs['Vector'])
    mange_n=node('ShaderNodeTexNoise'); mange_n.inputs['Scale'].default_value=3.2*S; mange_n.inputs['Detail'].default_value=10; mange_n.inputs['Roughness'].default_value=0.65; Lk.new(obj,mange_n.inputs['Vector'])
    mt=cfg.get('mange',0.6)
    mange=ramp(mange_n.outputs['Fac'],[(mt,(0,0,0,1)),(mt+0.035,(1,1,1,1))])
    vor=node('ShaderNodeTexVoronoi',feature='DISTANCE_TO_EDGE'); vor.inputs['Scale'].default_value=9*S; vor.inputs['Randomness'].default_value=1.0
    wn=node('ShaderNodeTexNoise'); wn.inputs['Scale'].default_value=6*S; Lk.new(obj,wn.inputs['Vector'])
    vv=node('ShaderNodeMix',data_type='VECTOR'); vv.inputs[0].default_value=0.45; Lk.new(obj,vv.inputs[4]); Lk.new(wn.outputs['Color'],vv.inputs[5]); Lk.new(vv.outputs[1],vor.inputs['Vector'])
    vline=ramp(vor.outputs['Distance'],[(0.0,(1,1,1,1)),(cfg.get('vein_w',0.018),(0,0,0,1))])
    vmask_n=node('ShaderNodeTexNoise'); vmask_n.inputs['Scale'].default_value=1.6*S; vmask_n.inputs['Detail'].default_value=3; Lk.new(obj,vmask_n.inputs['Vector'])
    vt=cfg.get('vein_cov',0.52)
    vmask=ramp(vmask_n.outputs['Fac'],[(vt,(0,0,0,1)),(vt+0.08,(1,1,1,1))])
    veins=mix(vline.outputs[0],vmask.outputs[0],1.0,'MULTIPLY')
    sor=node('ShaderNodeTexVoronoi',feature='F1'); sor.inputs['Scale'].default_value=14*S; Lk.new(obj,sor.inputs['Vector'])
    sore=ramp(sor.outputs['Distance'],[(0.0,(1,1,1,1)),(0.16,(1,1,1,1)),(0.22,(0,0,0,1))])
    sore=mix(sore.outputs[0],mange.outputs[0],1.0,'MULTIPLY')   # sores only inside mange
    bumpH=None
    vein_col=tuple(cfg.get('vein_color',(0.06,0.01,0.03,1)))
    glow=tuple(cfg.get('glow',(0.9,0.18,0.04,1)))
    if role in ('fur','fur_light','fur_dark'):
        base=C['base'] if role=='fur' else (C['light'] if role=='fur_light' else C['dark'])
        b0=tuple(x*0.55 for x in base[:3])+(1,); b1=tuple(min(1,x*1.35) for x in base[:3])+(1,)
        strand=ramp(fn.outputs['Fac'],[(0.3,b0),(0.7,b1)])
        col=mix(strand.outputs[0],big.outputs['Color'],0.12,'OVERLAY')
        sxyz=node('ShaderNodeSeparateXYZ'); Lk.new(obj,sxyz.inputs[0])
        zr=node('ShaderNodeMapRange'); Lk.new(sxyz.outputs[2],zr.inputs[0]); zr.inputs[1].default_value=cfg.get('saddle_z',[0.5,0.85])[0]*cfg['height']; zr.inputs[2].default_value=cfg.get('saddle_z',[0.5,0.85])[1]*cfg['height']
        sad=ramp(zr.outputs[0],[(0.0,(1,1,1,1)),(1.0,tuple(C.get('saddle',[0.6,0.6,0.6]))[:3]+(1,))])
        col=mix(col,sad.outputs[0],1.0,'MULTIPLY')
        dirt=ramp(big.outputs['Fac'],[(0.35,(1,1,1,1)),(0.75,tuple(cfg.get('dirt',(0.45,0.38,0.32)))+(1,))])
        col=mix(col,dirt.outputs[0],1.0,'MULTIPLY')
        skin=tuple(cfg.get('skin',(0.16,0.09,0.08,1)))
        skin_n=ramp(big.outputs['Fac'],[(0.3,skin),(0.7,tuple(x*0.6 for x in skin[:3])+(1,))])
        col=mix(col,skin_n.outputs[0],mange.outputs[0])
        col=mix(col,(0.22,0.025,0.015,1),sore)
        col=mix(col,vein_col,veins)
        Lk.new(col,p.inputs['Base Color'])
        rgh=mix((0.82,0.82,0.82,1),(0.55,0.55,0.55,1),mange.outputs[0]); rgh=mix(rgh,(0.25,0.25,0.25,1),sore)
        Lk.new(rgh,p.inputs['Roughness'])
        em=mix((0,0,0,1),tuple(x*cfg.get('vein_glow',0.35) for x in glow[:3])+(1,),veins)
        Lk.new(em,p.inputs['Emission Color']); p.inputs['Emission Strength'].default_value=1.0
        # bump: fur strands (off on mange), sores raised, veins raised
        h=mix(fn.outputs['Fac'],(0.5,0.5,0.5,1),mange.outputs[0])
        h=mix(h,(0.9,0.9,0.9,1),sore); h=mix(h,(0.85,0.85,0.85,1),veins)
        bp=node('ShaderNodeBump'); bp.inputs['Strength'].default_value=cfg.get('bump',0.45); bp.inputs['Distance'].default_value=0.01
        Lk.new(h,bp.inputs['Height']); Lk.new(bp.outputs[0],p.inputs['Normal'])
    elif role=='eye':
        p.inputs['Base Color'].default_value=(0.02,0.01,0.0,1); p.inputs['Roughness'].default_value=0.1
        p.inputs['Emission Color'].default_value=tuple(cfg.get('eye_glow',(1.0,0.32,0.05,1))); p.inputs['Emission Strength'].default_value=1.0
    elif role in ('nose','hoof','horn','tusk','claw','skin'):
        cols={'nose':(0.015,0.012,0.012,1),'hoof':(0.03,0.025,0.02,1),'horn':(0.16,0.13,0.10,1),'tusk':(0.42,0.36,0.26,1),'claw':(0.05,0.045,0.04,1),'skin':tuple(cfg.get('skin',(0.16,0.09,0.08,1)))}
        rg={'nose':0.3,'hoof':0.6,'horn':0.55,'tusk':0.45,'claw':0.5,'skin':0.55}
        c0=cols[role]
        g=node('ShaderNodeTexNoise'); g.inputs['Scale'].default_value=30*S; g.inputs['Detail'].default_value=10; Lk.new(obj,g.inputs['Vector'])
        r=ramp(g.outputs['Fac'],[(0.3,tuple(x*0.5 for x in c0[:3])+(1,)),(0.75,tuple(min(1,x*1.5) for x in c0[:3])+(1,))])
        col=r.outputs[0]
        if role in ('horn','tusk','hoof'):
            stain=ramp(big.outputs['Fac'],[(0.4,(1,1,1,1)),(0.7,(0.35,0.12,0.08,1))])  # blood/dirt stain
            col=mix(col,stain.outputs[0],1.0,'MULTIPLY')
        if role=='skin':
            col=mix(col,(0.22,0.025,0.015,1),sore); col=mix(col,vein_col,veins)
            em=mix((0,0,0,1),tuple(x*cfg.get('vein_glow',0.35) for x in glow[:3])+(1,),veins); Lk.new(em,p.inputs['Emission Color'])
        Lk.new(col,p.inputs['Base Color']); p.inputs['Roughness'].default_value=rg[role]
        bp=node('ShaderNodeBump'); bp.inputs['Strength'].default_value=0.3; Lk.new(g.outputs['Fac'],bp.inputs['Height']); Lk.new(bp.outputs[0],p.inputs['Normal'])
    return m
