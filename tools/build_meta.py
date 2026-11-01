"""Build share images, favicons, robots/sitemap and static /order/* pages.
Run after editing index.html:  python3 tools/build_meta.py"""
import re, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));os.chdir(R)
BASE="https://severed-signal.vercel.app"
F="/usr/share/fonts/truetype/sand-box/google/"
def font(sub,size):
  for root,_,fs in os.walk(F+sub):
    for f in sorted(fs):
      if f.endswith('.ttf') and 'Italic' in f: return ImageFont.truetype(os.path.join(root,f),size)
  raise SystemExit('font missing '+sub)
def card(src,title,line,out):
  im=Image.open(src).convert('RGB');w,h=im.size;s=max(1200/w,630/h)
  im=im.resize((int(w*s)+1,int(h*s)+1),Image.LANCZOS);x=(im.width-1200)//2;y=(im.height-630)//2
  im=im.crop((x,y,x+1200,y+630))
  g=Image.new('L',(1200,630));gd=ImageDraw.Draw(g)
  for i in range(1200):gd.line([(i,0),(i,630)],fill=int(235*max(0,1-i/760)))
  im=Image.composite(Image.new('RGB',im.size,(7,8,10)),im,g)
  d=ImageDraw.Draw(im);t=font('Cormorant Garamond',112);m=ImageFont.truetype(F+'JetBrains Mono/'+[f for f in os.listdir(F+'JetBrains Mono') if 'Italic' not in f][0],18)
  d.text((64,70),"SEVERED SIGNAL  ·  AN ART SERIES BY SETH",font=m,fill=(236,230,218))
  yy=300
  for i,part in enumerate(title.split('\n')):
    d.text((64+(90 if i else 0),yy-110+i*112),part,font=t,fill=(236,230,218) if i==0 else (230,57,70))
  d.rectangle([64,470,760,476],fill=(179,18,28))
  d.text((64,505),line,font=m,fill=(236,230,218))
  im.save(out,'JPEG',quality=84,optimize=True,progressive=True)
s=open('index.html').read()
orders={}
for n,name,k,lore in re.findall(r'\{"n": "(VIII|IX)", "name": "([^"]+)", "k": "(\w)", "lore": "([^"]+)"',s):
  first=re.search(r'"%s": \[\["(\w+)"'%k,s).group(1);orders[n]=(name,lore,first)
card('img/v5/hero.webp',"Severed\nSignal","A faith born after the networks went dark.",'og/home.jpg')
for n,(name,lore,first) in orders.items():
  card(f'img/v5/{first}.webp',name,f"Order {n} of the Severed Signal",f'og/order-{n.lower()}.jpg')
  p=s
  title=f"Order {n} · {name} — Severed Signal";url=f"{BASE}/order/{n.lower()}";img=f"{BASE}/og/order-{n.lower()}.jpg"
  desc=lore.replace('&','&amp;')
  p=re.sub(r'<title>.*?</title>',f'<title>{title}</title>',p,1)
  for prop,val in [('og:title',title),('twitter:title',title),('og:image:alt',title),('og:description',desc),('twitter:description',desc),('og:url',url),('og:image',img),('twitter:image',img)]:
    p=re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*'%re.escape(prop),lambda m:m.group(1)+val,p,1)
  p=re.sub(r'(<meta name="description" content=")[^"]*',lambda m:m.group(1)+desc,p,1)
  p=re.sub(r'<link rel="canonical" href="[^"]*">',f'<link rel="canonical" href="{url}">',p,1)
  p=p.replace('<link rel="preload" as="image" href="img/v5/hero.webp" fetchpriority="high">\n','')
  open(f'order/{n.lower()}.html','w').write(p)
# favicons
from cairosvg import svg2png
import io
for sz,out in [(180,'apple-touch-icon.png')]:
  svg2png(url='favicon.svg',write_to=out,output_width=sz,output_height=sz)
Image.open(io.BytesIO(svg2png(url='favicon.svg',output_width=64,output_height=64))).save('favicon.ico',sizes=[(16,16),(32,32),(48,48)])
open('robots.txt','w').write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
urls=[BASE+'/']+[f"{BASE}/order/{n.lower()}" for n in orders]
open('sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{u}</loc><lastmod>2026-11-01</lastmod></url>\n' for u in urls)+'</urlset>\n')
print('ok',list(orders))
