# Asset depth (c): a council idea for v6-09 answering t442u (render only, not staged, 0 chars applied).
# Baby and Hospital today plays in the home room (screen 32 render); the idea: a calm check-up room on the same wall, floor and window:
# exam bed with a paper sheet (hip high), cabinet with a baby scale (blank readout), sink, curtain on a rail. No signs, names or alarms.
# Targets shown: the blanket on the bed (the ask, bh-18), the pill on the cabinet (bh-26), a glass of water on the sink (bh-23; no 🚰, it reads as a sign).
import sys, re
sys.argv = ['x']; sys.path.insert(0, '/workspace/v608build/screens')
import play_v608 as PV
Z = PV.Z; OUT = '/workspace/v608build/round2/asset-depth/'
INK = '#10170F'
# furniture (design 390 x 844; floor base 660; hero 124-212 x 505-703; card top 724)
CLINIC = ("<svg class='abs' data-deco='clinic' style='left:0;top:0' width='390' height='844' viewBox='0 0 390 844' fill='none' stroke='%s' stroke-width='3' stroke-linejoin='round' stroke-linecap='round'>" % INK +
  # curtain rail and a pulled-back curtain (right)
  "<path d='M226 392h160' stroke-width='4'/><circle cx='226' cy='392' r='4' fill='#9AA3AD'/>"
  "<path d='M348 394q-6 140 4 286h34V394z' fill='#8CCFC0'/><path d='M360 400q-4 130 2 278M372 400q4 130 0 278' stroke='#5FA597' stroke-width='2'/>"
  # sink on the left wall: basin, tap, pipe
  "<path d='M22 500h84l-8 26H30z' fill='#F4F4EF'/><path d='M60 526v40' stroke='#9AA3AD' stroke-width='5'/><path d='M60 526v40' stroke-width='1.5' opacity='.5'/>"
  "<path d='M44 500v-22h18v8' fill='none' stroke='#9AA3AD' stroke-width='6'/><path d='M44 500v-22h18v8' fill='none' stroke-width='1.5'/>"
  # cabinet with doors (left), baby scale on top (blank readout)
  "<path d='M16 592h96v80H16z' fill='#E9E4D8'/><path d='M64 596v72M54 628h4M70 628h4' stroke-width='2'/><path d='M12 586h104v8H12z' fill='#CFC8B8' stroke-width='2'/>"
  "<path d='M22 572h50l-4 14H26z' fill='#F4F4EF' stroke-width='2'/><path d='M30 560q17-10 34 0l-2 12H32z' fill='#BFE3F0' stroke-width='2'/><rect x='38' y='576' width='18' height='7' rx='2' fill='#DDEBDD' stroke-width='1.5'/>"
  # exam bed: metal legs, base, mattress, raised head, paper sheet
  "<path d='M252 628v50M366 628v50' stroke='#9AA3AD' stroke-width='6'/><path d='M252 628v50M366 628v50' stroke-width='2'/>"
  "<path d='M240 612h140v18H240z' fill='#6FA8C8'/><path d='M330 612l40-26 10 6-6 20z' fill='#6FA8C8'/>"
  "<path d='M248 607h86v5h-86z' fill='#FFFFFF' stroke-width='2'/><path d='M336 606l32-21' stroke='#FFFFFF' stroke-width='4'/>"
  "<ellipse cx='310' cy='684' rx='72' ry='6' fill='rgba(16,23,15,.18)' stroke='none'/><ellipse cx='64' cy='676' rx='54' ry='6' fill='rgba(16,23,15,.18)' stroke='none'/>"
  "</svg>")
QUILT = ("<svg width='100%' height='100%' viewBox='0 0 60 26' style='display:block;overflow:visible' fill='none' stroke='#10170F' stroke-width='2.5' stroke-linejoin='round'>"
         "<path d='M2 8h56v16H2z' fill='#F2A0A8'/><path d='M2 3h56v6H2z' fill='#F7C3C8'/><path d='M20 9v15M40 9v15M2 16h56' stroke='#C76F7A' stroke-width='1.5'/></svg>")
def prop(name, x, y, w, h, inner):   # a scene target with a contact shadow; tap area 44 pt+, centred
    return (f"<div class='abs' style='left:{x + w/2 - 18:.0f}px;top:{y + h - 3:.0f}px;width:36px;height:8px;border-radius:50%;background:rgba(16,23,15,.22)'></div>"
            f"<div class='abs' data-tap=1 role='button' data-name='{name}' aria-label='{name}' style='left:{x}px;top:{y}px;width:{w}px;height:{h}px;display:flex;align-items:flex-end;justify-content:center'>{inner}</div>")
EMO = lambda e, s: f"<div style='font-size:{s}px;line-height:1'>{e}</div>"
PROPS = (prop('blanket', 254, 568, 60, 44, "<div style='width:60px;height:26px'>" + QUILT + '</div>') +
         prop('pill', 72, 542, 44, 44, EMO('💊', 30)) + prop('water', 70, 452, 44, 48, "<svg width='24' height='32' viewBox='0 0 24 32' fill='none' stroke='#10170F' stroke-width='2.5' stroke-linejoin='round'><path d='M3 2h18l-2 28H5z' fill='#E6F4FA'/><path d='M4.5 12h15l-1.4 17H5.9z' fill='#8FD0EE' stroke='none'/><path d='M3 2h18l-2 28H5z'/></svg>"))
_obj, _hero, _ask = Z.obj, Z.hero, Z.ask_lines
L = dict(Z.L390); L['shelf'] = (-900, 438, 10); L['pegs'] = []
Z.L390 = L
Z.obj = lambda k, *a, **kw: '' if k in ('disc', 'tie', 'towel', 'desk', 'crib') else _obj(k, *a, **kw)
Z.hero = lambda *a, **kw: CLINIC + _hero(*a, **kw) + PROPS
Z.ask_lines = lambda c, en, th: [PV.tx('Please bring a blanket.', 'e22'), PV.tx('ขอผ้าห่มหน่อยค่ะ', 't17 nw')]
doc = PV.page(390, 844, Z.screen('lake', 'ask', 390, 844))
f = OUT + 'clinic-checkup-room-idea-390x844'; open(f + '.html', 'w').write(doc); PV.S.shot(doc, f + '.png', 390, 844, 'clinic390'); print(f)
