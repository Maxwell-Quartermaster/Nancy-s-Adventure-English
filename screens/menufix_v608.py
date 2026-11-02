# Watchman sweep P1-P4 (spec 6.2 :68/:227): hearth in the top-right corner, 16 pt from both edges (56 pt at 390, 44 pt at 320);
# at 320 the menu buttons are 288 wide at left 16 (16 pt margins); hearth bubbles hang under the hearth with the tail at the top right;
# the open-from-home bubble sits at top 160 (under the banner, over the sky), clear of the hero.
def apply(M):
    _bub0 = M.bubble
    def hearth(x=None, y=None):
        se = M.w == 320; d = 44 if se else 56
        return (f"<div data-tap=1 data-name='hearth' style='position:absolute;left:{M.w-16-d}px;top:16px;width:{d}px;height:{d}px;box-sizing:border-box;border-radius:50%;background:#F6E9C8;border:3px solid #10170F;box-shadow:inset 0 0 0 3px #E8B84A,0 3px 0 #10170F;display:flex;align-items:center;justify-content:center'>"
                f"<svg width='{24 if se else 30}' height='{22 if se else 28}' viewBox='0 0 30 28'><path d='M15 26L3 14Q-2 7 4 3t11 4q5-8 11-4t-1 11z' fill='#FFCC33' stroke='#10170F' stroke-width='2.5' stroke-linejoin='round'/></svg></div>")
    def hub(extra=''):
        se = M.w == 320; x, bw = (16, 288) if se else (70, 250)
        return M.page('a', M.rbtn(M.T['titleMap']['en'], M.T['titleMap']['th'], x, M.h - 230 + (34 if se else 0), bw) + M.rbtn(M.T['character']['en'], M.T['character']['th'], x, M.h - 136 + (36 if se else 0), bw) + hearth() + extra)
    def hbubble(inner, bw):   # hangs under the hearth, tail at the top right pointing up at it
        se = M.w == 320; d = 44 if se else 56; bw = min(bw, M.w - 32)
        tail = (f"<svg width='28' height='16' style='position:absolute;right:{d//2-14+0}px;top:-15px' viewBox='0 0 28 16'><path d='M0 16L14 1 28 16' fill='#F6E9C8' stroke='#10170F' stroke-width='2'/><path d='M3 16h22' stroke='#E8B84A' stroke-width='3'/></svg>")
        return _bub0(inner + tail, M.w - 16 - bw, 16 + d + 12, bw)
    M.hearth, M.hub, M.hbubble = hearth, hub, hbubble
    return M
