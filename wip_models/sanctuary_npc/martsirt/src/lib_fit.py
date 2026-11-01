# quick workbench fit renders: exec at end of an npc script when STAGE=='fit'
def fit_render(out,views=(('front',0),('side',90),('back',180),('q',35)),focus=None,res=(700,900)):
    sc=bpy.context.scene; sc.render.engine='BLENDER_WORKBENCH'; sc.render.resolution_x,sc.render.resolution_y=res
    sh=sc.display.shading; sh.light='STUDIO'; sh.color_type='OBJECT'; sh.show_cavity=True; sh.cavity_type='BOTH'
    cols={}
    for o in bpy.data.objects:
        if o.type=='MESH': o.color=(0.8,0.7,0.6,1)
    import colorsys
    for k,(o,mat,wfn,kind) in enumerate(PIECES):
        h=(hash(str(mat))%997)/997.0; r,g,b=colorsys.hsv_to_rgb(h,0.45,0.75); o.color=(r,g,b,1)
    cam=bpy.data.objects.new('cam',bpy.data.cameras.new('cam')); link(cam); sc.camera=cam
    ctr=Vector((0,0,1.0)) if focus is None else Vector(focus[0]); dist=4.2 if focus is None else focus[1]
    cam.data.lens=50
    for nm,az in views:
        a=D(az); cam.location=ctr+Vector((math.sin(a)*dist,-math.cos(a)*dist,0.05))
        d=ctr-cam.location; cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
        sc.render.filepath=out+'_'+nm+'.png'; bpy.ops.render.render(write_still=True)
