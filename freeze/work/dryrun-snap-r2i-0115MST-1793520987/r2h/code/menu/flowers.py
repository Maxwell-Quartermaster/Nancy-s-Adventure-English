# Shared t527u flower -> tuft code (menus, extended map, and the map screens 05/07/08/09). Moved out of build_menu.py unchanged.
import re
# Maxwell t527u / Watchman: the five-petal circle flowers (5 petals r 2.4 + yellow centre r 1.8, no stem) that come in with the map art (parts.py)
# become the three-blade grass tuft (fix_r2h.tuft, the 11-12 / W24 / 48 style), base at the flower's bottom edge. Real flower art is not touched.
FLOWER = re.compile(r"<g stroke='none'>(?:<circle cx='[\d.]+' cy='[\d.]+' r='2\.4' fill='#[0-9A-Fa-f]{6}'/>){5}<circle cx='([\d.]+)' cy='([\d.]+)' r='1\.8' fill='#FFD54F'/></g>")
def tuft(x, y, col='#0F3A14'):
    return (f"<path d='M{x-6:g} {y:g}q1-7 -2-10M{x-1:g} {y:g}q-1-9 1-14M{x+4:g} {y:g}q0-7 4-10' stroke='{col}' stroke-width='2.5' fill='none' "
            f"stroke-linecap='round' data-deco='tuft'/>")
FLOG = []
def deflower(name, doc):
    n = [0]
    def r(m): n[0] += 1; return tuft(round(float(m.group(1)), 1), round(float(m.group(2)) + 5, 1))
    doc = FLOWER.sub(r, doc)
    if n[0]: FLOG.append(f'{name}: {n[0]} five-petal circle flowers -> tufts (t527u)')
    return doc
