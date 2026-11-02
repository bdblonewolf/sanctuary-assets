# replace zero/non-unit TANGENT vectors in a GLB in place (degenerate UVs) with an orthogonal unit tangent
import sys,json,struct,numpy as np
for fn in sys.argv[1:]:
    b=bytearray(open(fn,'rb').read()); n=struct.unpack('<I',b[12:16])[0]; J=json.loads(b[20:20+n]); bin0=20+n+8; fixed=0
    for m in J['meshes']:
        for p in m['primitives']:
            if 'TANGENT' not in p['attributes']: continue
            a=J['accessors'][p['attributes']['TANGENT']]; bv=J['bufferViews'][a['bufferView']]
            na=J['accessors'][p['attributes']['NORMAL']]; nbv=J['bufferViews'][na['bufferView']]
            o=bin0+bv.get('byteOffset',0)+a.get('byteOffset',0); c=a['count']
            T=np.frombuffer(bytes(b[o:o+c*16]),np.float32).reshape(c,4).copy()
            no=bin0+nbv.get('byteOffset',0)+na.get('byteOffset',0); N=np.frombuffer(bytes(b[no:no+c*12]),np.float32).reshape(c,3)
            L=np.linalg.norm(T[:,:3],axis=1); bad=np.abs(L-1)>1e-3
            for i in np.where(bad)[0]:
                nn=N[i]; ref=np.array([1,0,0]) if abs(nn[0])<0.9 else np.array([0,1,0]); t=ref-nn*np.dot(ref,nn); t/=np.linalg.norm(t)
                T[i]=[*t,1.0]
            if bad.any(): b[o:o+c*16]=T.astype(np.float32).tobytes(); fixed+=int(bad.sum())
    open(fn,'wb').write(b); print(fn,'fixed',fixed)
