(() => { const out = []; let i = 0;
for (const e of document.querySelectorAll('*')) { i++; const c = getComputedStyle(e);
  if ((c.rowGap !== 'normal' && c.rowGap !== '0px') || (c.columnGap !== 'normal' && c.columnGap !== '0px')) {
    const kids = [...e.children].map(k => { const s = getComputedStyle(k); return s.display === 'none' ? 'none' : s.position === 'absolute' || s.position === 'fixed' ? 'abs' : 'flow'; });
    const txtNodes = [...e.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()).length;
    out.push({ idx: i, tag: e.tagName, display: c.display, dir: c.flexDirection, wrap: c.flexWrap, rowGap: c.rowGap, colGap: c.columnGap, kids: kids.join(','), txtNodes, style: (e.getAttribute('style') || '').slice(0, 140), cls: e.className && e.className.baseVal === undefined ? e.className : '', text: e.textContent.trim().slice(0, 40) }); } }
return out; })()
