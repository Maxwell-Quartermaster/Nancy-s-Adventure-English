# Scene stage check (stage_v608.py)

One design box (390x844) per scene, scaled as one piece; HUD and card at the phone size. Sizes: 390x844, 375x667, 320x568

## W24-walk-B
- fit pass 1: walker#0 ink [46.5, 437.5, 65.5, 481.5] moved +0.0, +2.5 pt
- fit pass 2: walker#0 ink [46.5, 440.0, 65.5, 484.0] moved +0.0, +0.0 pt
- scenery top (swing set, trees, walker, heroes) at 390: 325.1 pt; 320/375 shrink so it clears the banner
### 390x844: scale 1.000, offset 0.0, 0.0; HUD bottom 131, card top 640: PASS
- walker#0: ink 46.5,440.0-65.5,484.0; stand grass, centred 0..Sam: gap +0.0 px, anchor x inside ink [ok]
- hero: feet/bottom 628.8, card top 640.0 [ok]
### 375x667: scale 0.962, offset 0.0, -152.4; HUD bottom 131, card top 463: PASS
- walker#0: ink 44.5,270.5-63.0,312.5; stand grass, centred 0..Sam: gap +0.5 px, anchor x inside ink [ok]
- hero: feet/bottom 452.2, card top 463.0 [ok]
### 320x568: scale 0.759, offset 11.9, -122.0; HUD bottom 119, card top 364: PASS
- walker#0: ink 47.5,212.0-62.0,245.5; stand grass, centred 0..Sam: gap +0.0 px, anchor x inside ink [ok]
- hero: feet/bottom 355.5, card top 364.0 [ok]

TOTAL FAIL: 0
