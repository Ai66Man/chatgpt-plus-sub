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
static_files={p.name for p in (root.parent/'static').iterdir() if p.is_file()}
for name in static_files:
 assert (root/name).read_bytes()==(root.parent/'static'/name).read_bytes(), 'Static verification file changed'
pages={p:Page(p.read_text()) for p in root.glob('*.html') if p.name not in static_files}
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
# Verify the indexable URL graph and metadata against published output.
import json, re
import xml.etree.ElementTree as ET
base='https://ai66man.github.io/chatgpt-plus-sub/'
indexed=set(); titles=set(); descriptions=set(); inbound={p.name:0 for p in pages}
for p,data in pages.items():
 text=p.read_text()
 title=re.search(r'<title>(.*?)</title>',text).group(1)
 desc=re.search(r'<meta name="description" content="([^"]+)"',text).group(1)
 assert title not in titles,(p.name,'duplicate title')
 assert desc not in descriptions,(p.name,'duplicate description')
 titles.add(title);descriptions.add(desc)
 robots=re.findall(r'<meta name="robots" content="([^"]+)"',text)
 assert len(robots)==1,(p.name,'robots')
 canonical=re.findall(r'<link rel="canonical" href="([^"]+)"',text)
 expected=base+('' if p.stem=='index' else p.name)
 if p.stem=='404': assert not canonical
 else: assert canonical==[expected],(p.name,'canonical',canonical)
 if 'noindex' not in robots[0]: indexed.add(expected)
 for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text):
  schemas=json.loads(block)
  for schema in schemas:
   assert schema['@type'] not in ['Product','AggregateRating','Review'],p.name
 for ref in data.refs:
  path=urlsplit(ref).path
  if not urlsplit(ref).scheme and path in inbound and path!=p.name:inbound[path]+=1
sitemap={n.text for n in ET.parse(root/'sitemap.xml').findall('.//{*}loc')}
assert sitemap==indexed,('sitemap mismatch',sitemap^indexed)
assert all(count>0 for name,count in inbound.items() if name!='404.html'),inbound
for p in pages:
 assert 'data-conversion="shop"' not in p.read_text() or 'rel="sponsored nofollow"' in p.read_text()
assert '新购与升级' in (root/'chatgpt-pro.html').read_text()
assert 'href="chatgpt-pro.html">查看当前状态' in (root/'index.html').read_text()
print(f'PASS: {len(indexed)} indexable canonical URLs, unique metadata, JSON-LD, sitemap and incoming links.')
