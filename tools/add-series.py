#!/usr/bin/env python3
"""Sync a series into the site.
Usage: python3 tools/add-series.py [series=a-series] [src=/workspace/art/severed-signal/landscape]
To add A29+: drop A29.png in src, append ["A29","Title","One line."] to data/a-series.json, rerun, commit, push.
Writes img/v5/<id>.webp (1280x720) + img/v5/t/<id>.webp (640x360) and rewrites NW key "h" in index.html."""
import json,re,sys,os
from PIL import Image
ser=sys.argv[1] if len(sys.argv)>1 else 'a-series'
src=sys.argv[2] if len(sys.argv)>2 else '/workspace/art/severed-signal/landscape'
key='h'
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(root)
items=json.load(open(f'data/{ser}.json'))
for i,_,_ in items:
    out=f'img/v5/{i}.webp'
    if os.path.exists(out): continue
    im=Image.open(f'{src}/{i}.png').convert('RGB')
    im.resize((1280,720),Image.LANCZOS).save(out,'WEBP',quality=82,method=6)
    im.resize((640,360),Image.LANCZOS).save(f'img/v5/t/{i}.webp','WEBP',quality=78,method=6)
h=open('index.html').read()
a=h.index('const NW=')+len('const NW=')
NW,n=json.JSONDecoder().raw_decode(h,a); NW[key]=items
h=h[:a]+json.dumps(NW,ensure_ascii=False)+h[n:]
open('index.html','w').write(h)
print(f'{len(items)} works in NW["{key}"]')
