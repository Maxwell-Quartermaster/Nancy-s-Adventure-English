# occlusion sweep: every text run, emoji, svg and picture plate; sample 3x3 points; who is on top?
import subprocess,re,sys,os,json,html as H
JS=r"""<script>window.addEventListener('load',function(){setTimeout(function(){
var W=%W%,Hh=%H%,out=[];
function lab(e){if(!e)return 'null';var t=(e.innerText||e.textContent||'').trim().replace(/\s+/g,' ').slice(0,24);return (e.getAttribute&&e.getAttribute('data-name')||e.tagName.toLowerCase())+(t?':"'+t+'"':'');}
function hidden(e){for(var n=e;n&&n.nodeType==1;n=n.parentElement){if(n.getAttribute('aria-hidden')=='true')return true;}return false;}
function paints(e){var t=e.tagName.toLowerCase();if(/^(path|circle|rect|ellipse|polygon|polyline|line|text|use|image|img)$/.test(t))return true;if(t=='svg'||t=='g')return false;var cs=getComputedStyle(e);if(parseFloat(cs.opacity)==0||cs.visibility=='hidden')return false;
 function a(c){var m=c.match(/rgba?\(([^)]+)\)/);if(!m)return 0;var p=m[1].split(',');return p.length>3?parseFloat(p[3]):1;}
 if(a(cs.backgroundColor)>0.05||cs.backgroundImage!='none')return true;if(parseFloat(cs.borderTopWidth)>0&&a(cs.borderTopColor)>0.05)return true;
 if([].some.call(e.childNodes,function(n){return n.nodeType==3&&n.textContent.trim()}))return true;return false;}
function rel(a,b){return a===b||a.contains(b)||b.contains(a);}
function grp(e){for(var n=e;n&&n.nodeType==1;n=n.parentElement){if(n.hasAttribute('data-tap')||n.getAttribute('role')=='button'||n.hasAttribute('data-name'))return n;}return e;}
var items=[];
var tw=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,null);var n;
while(n=tw.nextNode()){if(!n.textContent.trim())continue;var p=n.parentElement;if(!p||/SCRIPT|STYLE|PRE/.test(p.tagName))continue;var cs=getComputedStyle(p);if(cs.visibility=='hidden'||cs.display=='none'||parseFloat(cs.opacity)==0)continue;
 var r=document.createRange();r.selectNodeContents(n);var rs=r.getClientRects();for(var i=0;i<rs.length;i++){var q=rs[i];if(q.width<3||q.height<3)continue;items.push({k:'text',e:p,r:q,t:n.textContent.trim().slice(0,24)});}}
[].forEach.call(document.querySelectorAll('svg'),function(s){if(s.parentElement&&s.parentElement.closest('svg'))return;var q=s.getBoundingClientRect();if(q.width<8||q.height<8)return;items.push({k:'svg',e:s,r:q,t:lab(s.parentElement)});});
[].forEach.call(document.querySelectorAll('[data-tap],[role=button],[data-hit]'),function(s){var q=s.getBoundingClientRect();if(q.width<8||q.height<8)return;items.push({k:'tap',e:s,r:q,t:lab(s)});});
items.forEach(function(it){var q=it.r,cov={},nc=0,ns=0,off=0;
 for(var a=0;a<3;a++)for(var b=0;b<3;b++){var x=q.left+q.width*(0.2+0.3*a),y=q.top+q.height*(0.2+0.3*b);ns++;
  if(x<0||y<0||x>=W||y>=Hh){off++;continue;}
  var st=document.elementsFromPoint(x,y),top=null;
  for(var z=0;z<st.length;z++){var c=st[z];if(c.id=='OCC'||c===document.body||c===document.documentElement)continue;if(rel(c,it.e)){top=c;break;}if(paints(c)){top=c;break;}}
  if(!top)continue;
  if(rel(top,it.e)||rel(grp(top),grp(it.e)))continue;
  nc++;var L=lab(grp(top));cov[L]=(cov[L]||0)+1;}
 if(nc>=2||off>=2){out.push({k:it.k,t:it.t,el:lab(grp(it.e)),hid:hidden(it.e),r:[q.left|0,q.top|0,q.right|0,q.bottom|0],cov:cov,nc:nc,off:off});}
});
var pre=document.createElement('pre');pre.id='OCC';pre.textContent=JSON.stringify(out);document.body.appendChild(pre);},500);});</script>"""
def run(f,w,h):
    s=open(f).read(); j=JS.replace('%W%',str(w)).replace('%H%',str(h)); s=s.replace('</body>',j+'</body>') if '</body>' in s else s+j
    p='/tmp/aud608/oc/'+re.sub(r'[^\w.-]','_',f[-120:]); os.makedirs('/tmp/aud608/oc',exist_ok=True); open(p,'w').write(s)
    import tempfile,shutil
    _ud=tempfile.mkdtemp(prefix='occl-ud-')
    try:
        r=subprocess.run(['google-chrome','--headless=new','--no-sandbox','--disable-gpu','--virtual-time-budget=2500','--window-size=700,1200','--dump-dom','file://'+p],capture_output=True,text=True,timeout=120,env=dict(os.environ,TMPDIR=_ud))
    finally:
        shutil.rmtree(_ud,ignore_errors=True)
    m=re.search(r'<pre id="OCC">(.*?)</pre>',r.stdout,re.S)
    print('=====',f,w,h,flush=True)
    if not m: print('  NO-OUTPUT'); return
    for d in json.loads(H.unescape(m.group(1))): print('  ',json.dumps(d,ensure_ascii=False))
for line in sys.stdin:
    a=line.split()
    if len(a)==3: run(a[0],int(a[1]),int(a[2]))
