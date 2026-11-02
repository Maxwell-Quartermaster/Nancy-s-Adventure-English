# Asset depth (b): mirror mock, Word Meadow at 390 (park and pond layouts), current vs mirrored (Watchman Idea 1, zoneRuns odd).
# Render only, from the t439u stage html (scenes/stage/html). Scene art flips left-right; the hero keeps its facing (its spot mirrors),
# emoji props, any text and the glyph/clock/number SVGs (door-13, floor-4, clock-530, clock-930, money-50, number-14..19, anything with
# digits or letters) never flip; the UI (top bar, zone chip, card) is untouched. Usage: python3 mirror_mock.py
import re, sys, os
sys.argv = ['x']; sys.path.insert(0, '/workspace/v608build/scenes')
STG = '/workspace/v608build/scenes/stage/html/'; OUT = '/workspace/v608build/round2/asset-depth/'
GLYPH = ('door-13', 'floor-4', 'clock-530', 'clock-930', 'money-50', 'number-1')   # never flipped (ids or names)
def mirror(doc, W=390):
    i = doc.find("data-st='"); j = doc.find("data-tap=1 role='button'", i)
    pre, world, post = doc[:i], doc[i:j], doc[j:]
    a = "transform:scale(1.00000);transform-origin:0 0"; assert world.count(a) == 1
    world = world.replace(a, f"transform:matrix(-1,0,0,1,{W},0);transform-origin:0 0")
    n = {'hero': 0, 'emoji': 0, 'glyph': 0, 'text': len(re.findall('<text', world))}
    def flip_back(m):   # counter-flip in place (about its own centre) so it reads the right way round
        tag = m.group(0); return tag.replace("style='", "style='transform:scaleX(-1);", 1)
    # hero wrapper: the div right before the data-hero svg
    k = world.find('data-hero='); h0 = world.rfind("<div class='abs' style='", 0, k)
    world = world[:h0] + flip_back(re.match(r"<div class='abs' style='[^']*'", world[h0:])) + world[h0 + re.match(r"<div class='abs' style='[^']*'", world[h0:]).end():]; n['hero'] += 1
    def prop(m):
        body = world[m.end():m.end() + 12]; name = m.group(1)
        emoji = not body.startswith('<'); glyph = any(g in name for g in GLYPH)
        if emoji or glyph:
            n['emoji' if emoji else 'glyph'] += 1; return m.group(0).replace("style='", "style='transform:scaleX(-1);", 1)
        return m.group(0)
    world = re.sub(r"<div class='abs' data-hit=1 data-pn='([^']+)'[^>]*>", prop, world)
    # tap areas follow their props
    post = re.sub(r"(data-tap=1 role='button' data-name='[^']+' aria-label='[^']+' style='left:)([0-9.]+)px;(top:[0-9.]+px;width:)([0-9.]+)px",
                  lambda m: f"{m.group(1)}{W - float(m.group(2)) - float(m.group(4)):.1f}px;{m.group(3)}{m.group(4)}px", post.split("<div class='abs' data-ui=1", 1)[0]) + "<div class='abs' data-ui=1" + post.split("<div class='abs' data-ui=1", 1)[1]
    return pre + world + post, n
if __name__ == '__main__':
    import stage_v608 as ST
    for name in ('B-meadow-listen-and-find', 'A-meadow-evening-pond'):
        doc = open(STG + name + '-390x844.html').read(); m, n = mirror(doc)
        for tag, d in (('now', doc), ('mirrored', m)):
            f = OUT + f'mirror-{name}-{tag}-390x844'; open(f + '.html', 'w').write(d); ST.shot(d, f + '.png', 390, 844)
        print(name, n)
