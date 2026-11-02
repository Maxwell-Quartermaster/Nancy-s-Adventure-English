#!/bin/bash
# measure.sh <html> <w> <h> : prints JSON geometry (Echo Knight plate, helmet paths, Thai text, overflow) via headless Chrome --dump-dom
D=/workspace/qm/fix-320-20261102-0457; f=$(realpath "$1"); o=$D/scratch/m-$(basename "$f")
python3 - "$f" "$o" <<'PY'
import sys; s=open(sys.argv[1],encoding='utf-8').read()
js="""<script>(()=>{const o={};const R=e=>{const r=e.getBoundingClientRect();return [Math.round(r.left*10)/10,Math.round(r.top*10)/10,Math.round(r.right*10)/10,Math.round(r.bottom*10)/10]};
const pl=[...document.querySelectorAll('div[data-txt]')].filter(d=>/Echo Knight/.test(d.textContent));o.plate=pl.map(R);
o.helm=[...document.querySelectorAll('path')].filter(p=>p.getAttribute('fill')=='#8E99A6'||p.getAttribute('d')=='M40 4v-6').map(R);
const th=[...document.querySelectorAll('*')].filter(e=>[...e.childNodes].some(n=>n.nodeType==3&&/[\\u0E00-\\u0E7F]/.test(n.textContent)));
o.thai=th.map(e=>{const c=getComputedStyle(e);return [e.textContent.trim().slice(0,30),parseFloat(c.fontSize),c.lineHeight=='normal'?'normal':Math.round(parseFloat(c.lineHeight)/parseFloat(c.fontSize)*100)/100]});
o.scrollW=document.documentElement.scrollWidth;o.bodyScrollW=document.body.scrollWidth;o.innerW=innerWidth;
const pre=document.createElement('pre');pre.id='mout';pre.textContent=JSON.stringify(o);document.body.appendChild(pre)})()</script>"""
open(sys.argv[2],'w',encoding='utf-8').write(s.replace('</body>',js+'</body>') if '</body>' in s else s+js)
PY
TMPDIR=$D/scratch/tmp timeout 40 google-chrome --headless=new --no-sandbox --disable-gpu --no-first-run --disable-extensions --disable-dev-shm-usage --user-data-dir=$D/scratch/p --hide-scrollbars --window-size=$2,$3 --dump-dom "file://$o" 2>/dev/null | python3 -c "import sys,re,html;m=re.search(r'<pre id=\"mout\">(.*?)</pre>',sys.stdin.read(),re.S);print(html.unescape(m.group(1)) if m else 'NO-MEASURE')"
