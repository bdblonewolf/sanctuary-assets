"""Give unnamed mesh nodes (created by gltf-transform under animated prop nodes) the name <parent>_mesh. JSON-only edit."""
import json,struct,sys
b=open(sys.argv[1],'rb').read(); L=struct.unpack('<I',b[12:16])[0]; j=json.loads(b[20:20+L]); rest=b[20+L:]
par={c:i for i,n in enumerate(j['nodes']) for c in n.get('children',[])}
for i,n in enumerate(j['nodes']):
    if 'name' not in n and i in par: n['name']=j['nodes'][par[i]].get('name','node')+('_mesh' if 'mesh' in n else '_xf')
js=json.dumps(j,separators=(',',':')).encode(); js+=b' '*((4-len(js)%4)%4)
out=b[:8]+struct.pack('<I',12+8+len(js)+len(rest))+struct.pack('<I',len(js))+b'JSON'+js+rest
open(sys.argv[2],'wb').write(out)
