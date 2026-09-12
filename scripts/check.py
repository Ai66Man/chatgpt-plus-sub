from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
root=Path(__file__).resolve().parent.parent/'docs'
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=set();self.refs=[];self.h1=0;self.images=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id' in d:self.ids.add(d['id'])
  if tag=='h1':self.h1+=1
  if tag in ['a','link','img','script']:
   value=d.get('href',d.get('src'))
   if value:self.refs.append(value)
  if tag=='img':assert d.get('alt'), 'image needs alt'
pages={p:Page(p.read_text()) for p in root.glob('*.html')}
for p,data in pages.items():
 assert data.h1==1,(p.name,'heading')
 for ref in data.refs:
  u=urlsplit(ref)
  if u.scheme or u.netloc:continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  assert target.exists(),(p.name,ref,'missing file')
  if u.fragment and target in pages:assert unquote(u.fragment) in pages[target].ids,(p.name,ref,'missing anchor')
 text=p.read_text()
 assert '/Users/' not in text and 'gtag(' not in text
print(f'PASS: {len(pages)} pages; local links, anchors, assets, heading structure and private-path checks.')
