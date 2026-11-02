# Auditor: copy a doc and append a measuring script (copy only)
import sys; s=open(sys.argv[1],encoding='utf-8').read()
js=r"""<script>(function(){var o={};function R(e){var r=e.getBoundingClientRect();return [Math.round(r.left*10)/10,Math.round(r.top*10)/10,Math.round(r.right*10)/10,Math.round(r.bottom*10)/10]}
var pl=[].slice.call(document.querySelectorAll('div[data-txt]')).filter(function(d){return d.children.length&&/Echo Knight/.test(d.textContent)});o.plate=pl.map(R);
var P=pl.length?pl[0].getBoundingClientRect():null;
o.helm=[].slice.call(document.querySelectorAll('path')).filter(function(p){return p.getAttribute('fill')=='#8E99A6'||p.getAttribute('d')=='M40 4v-6'}).map(R);
o.hits=[];if(P){[].slice.call(document.querySelectorAll('svg,svg *')).forEach(function(e){var r=e.getBoundingClientRect();if(r.width&&r.left<P.right&&r.right>P.left&&r.top<P.bottom&&r.bottom>P.top)o.hits.push([e.tagName,(e.getAttribute('d')||'').slice(0,20),e.getAttribute('fill'),R(e)])})}
var th=[].slice.call(document.querySelectorAll('*')).filter(function(e){return [].slice.call(e.childNodes).some(function(n){return n.nodeType==3&&/[\u0E00-\u0E7F]/.test(n.textContent)})});
o.thai=th.map(function(e){var c=getComputedStyle(e);return [e.textContent.trim().slice(0,20),parseFloat(c.fontSize),c.lineHeight=='normal'?'normal':Math.round(parseFloat(c.lineHeight)/parseFloat(c.fontSize)*100)/100]});
o.thaiMinPx=Math.min.apply(null,o.thai.map(function(t){return t[1]}));o.thaiNormal=o.thai.filter(function(t){return t[2]=='normal'}).length;o.thaiMinLH=Math.min.apply(null,o.thai.filter(function(t){return t[2]!='normal'}).map(function(t){return t[2]}));
o.scrollW=document.documentElement.scrollWidth;o.bodyScrollW=document.body.scrollWidth;o.innerW=innerWidth;
var pre=document.createElement('pre');pre.id='mout';pre.style.display='none';pre.textContent=JSON.stringify(o);document.body.appendChild(pre)})()</script>"""
open(sys.argv[2],'w',encoding='utf-8').write(s.replace('</body>',js+'</body>') if '</body>' in s else s+js)
