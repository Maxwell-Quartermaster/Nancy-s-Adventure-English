(() => { const o = {}; const R = e => { const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom].map(v => Math.round(v * 10) / 10) };
 o.plate = [...document.querySelectorAll('div[data-txt]')].filter(d => /Echo Knight/.test(d.textContent)).map(R);
 o.helm = [...document.querySelectorAll('path')].filter(p => p.getAttribute('fill') == '#8E99A6' || p.getAttribute('d') == 'M40 4v-6').map(R);
 const th = [...document.querySelectorAll('body *')].filter(e => [...e.childNodes].some(n => n.nodeType == 3 && /[\u0E00-\u0E7F]/.test(n.textContent)));
 o.thai = th.map(e => { const c = getComputedStyle(e); const fs = parseFloat(c.fontSize); return [e.textContent.trim().slice(0, 24), fs, c.lineHeight == 'normal' ? 'normal' : Math.round(parseFloat(c.lineHeight) / fs * 100) / 100, e.getBoundingClientRect().width > 0] });
 o.thaiMinPx = Math.min(...o.thai.filter(t => t[3]).map(t => t[1])); o.thaiMinLH = Math.min(...o.thai.filter(t => t[3] && t[2] != 'normal').map(t => t[2])); o.thaiLHnormal = o.thai.filter(t => t[3] && t[2] == 'normal').length;
 o.scrollW = document.documentElement.scrollWidth; o.innerW = innerWidth; o.hOverflow = o.scrollW > innerWidth;
 const P = o.plate[0]; const hit = (a, b) => a[0] < b[2] && b[0] < a[2] && a[1] < b[3] && b[1] < a[3];
 const pe = [...document.querySelectorAll('div[data-txt]')].find(d => /Echo Knight/.test(d.textContent));
 if (P) { o.plateHits = [...document.querySelectorAll('svg, [data-name], [data-pn], [data-hero], [data-txt], [data-tap]')].filter(e => !pe.contains(e) && !e.contains(pe) && getComputedStyle(e).visibility != 'hidden').map(e => [e.tagName + (e.dataset.name || e.dataset.pn || e.dataset.hero || '') + ':' + (e.textContent || '').trim().slice(0, 16), R(e)]).filter(x => hit(x[1], P) && x[1][2] - x[1][0] < 300);
  const chip = [...document.querySelectorAll('div')].filter(d => /^Echo Forest/.test(d.textContent.trim()) && !/Knight/.test(d.textContent)).map(R).sort((a, b) => (a[2] - a[0]) - (b[2] - b[0]))[0]; o.chip = chip; o.chipGap = chip ? Math.round((P[1] - chip[3]) * 10) / 10 : null;
  o.helmGap = o.helm.length ? Math.round(Math.min(...o.helm.map(hr => Math.max(hr[0] - P[2], P[0] - hr[2], hr[1] - P[3], P[1] - hr[3]))) * 10) / 10 : null; }
 return o; })()
