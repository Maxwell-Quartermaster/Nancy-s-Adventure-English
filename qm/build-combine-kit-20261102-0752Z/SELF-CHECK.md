**Quartermaster:** SELF-CHECK for Build. Run these after generating each stage, and all of them after stage 4. The expected numbers below come from the file (PASTE `5e1666fe6f7189d3886686749335b3ee`, `cards.json` md5 `8d209ec5d2701b4d1f77e73457dd8fcb`). Any mismatch is a stop-and-ask, never a silent fix.
**Quartermaster:** Hashes are SHA-256 of the UTF-8 string with nothing added, so `crypto.subtle.digest('SHA-256', …)` can check them in `window.__test()`. A `\n` inside a verse is a real newline character.

## A. Card data

| # | Check | Expected |
|---|---|---|
| A1 | `cards.json` byte check | md5 `8d209ec5d2701b4d1f77e73457dd8fcb` (with trailing newline: `12d973cf0af5c6edc7dbbffa828bd481`); SHA-256 `0d4abf2d603a0b8ceeffac18515e2c0162b038a9657ab5f1438f768e0f0b3480` |
| A2 | `cards.length` | 211 (= `meta.totalCards` 211, `meta.writtenCards` 211) |
| A3 | unique `id`s | 211, duplicates 0 |
| A4 | cards per zone (by prefix) | phonics 26, colors-shapes 24, sight-words 24, numbers 24, baby-hospital 31, maxwell-says 32, kitchen 50 |
| A5 | resolved `type` (after `meta.typeByZone`, then `picture`) | picture 126, say-it 74, server-talk 10, two-answer 1 (sum 211) |
| A6 | explicit `type:"say-it"` cards | 37 (= `meta.sayItTotal`; the other 37 say-it cards are Kitchen cards via `meta.typeByZone`) |
| A7 | picture cards | 126: emoji 73, `svg:` 39, `null` fallback 14 (= `meta.pics`) |
| A8 | `personal` true (after defaults) | 80 (= `meta.personalCards`) |
| A9 | `nursePhrase` true | 10: bh-01 to bh-10 |
| A10 | `thDef` present | 18 (= `meta.thDefCards`) |
| A11 | `fill:true` (Inn examples, Example tag) | ms-04, ms-05, ms-06 |
| A12 | `thStatus:"SIGNED OFF"` | fd-01, fd-02, fd-03, fd-04, fd-05, fd-06; every other card resolves to `NEEDS NANCY` |
| A13 | two-answer card | `ms-31` only, 2 `choices`, 2 `prompts` |
| A14 | `needsMaxwell` | 7: ms-04, ms-05, ms-06, bh-30, ms-28, ms-29, ms-30 (= `meta.needsMaxwellCount` 7) |
| A15 | `meta.outings` | 11: ms-01, ms-02, ms-05, fd-29, fd-30, fd-31, bh-01, bh-02, bh-05, ms-11, ms-12 |
| A16 | every card id in Part 1 exists in `cards` | 0 missing |

## B. Zones, map, bosses

| # | Check | Expected |
|---|---|---|
| B1 | `zones.length`, order | 7: phonics, colors-shapes, numbers, sight-words, baby-hospital, maxwell-says, kitchen |
| B2 | prefixes | phonics `ph`, colors-shapes `cs`, numbers `nm`, sight-words `sw`, baby-hospital `bh`, maxwell-says `ms`, kitchen `fd cv` |
| B3 | `startZone` | `phonics` only |
| B4 | bosses | 5 zones with 10 cards each (phonics, colors-shapes, numbers, sight-words, baby-hospital); maxwell-says and kitchen `boss: null` |
| B5 | `mapLayout.regions` | 4: r1 Word Meadow [phonics, sight-words]; r2 Golden Fields [colors-shapes, numbers]; r3 Home Lake [maxwell-says, kitchen, baby-hospital]; r4 Echo Forest [soundDuel] |
| B6 | zone clips + boss clips + reward clips | 7 + 5 + 5 = 17 (skipped silently if missing) |

## C. Verses (16) and Jesus words (6): text must be byte-identical

| # | Check | Expected |
|---|---|---|
| C1 | verse count | 16 = 10 `verses.weekly` + 1 `verses.rest` + 5 `zones[].boss.scroll` (= `meta.versesVerified` 16); all `status:"VERIFIED"` |
| C2 | daily cycle | 40 = 10 weekly + 30 in `daily-verses.json`; day 41 shows verse 1 |
| C3 | Jesus words | 6 in `jesusWords`, all given at start; `jesusWordsFallback` 2 |
| C4 | attribution | `verses.attribution.esv` SHA-256 `3c24f2aaea8894bbf9048a329ba6f9a13a938689933ecb70b21c5efc930fe726`; `.thsv11` `3f36b8f2a4122d34fb647ce567ddfaaaaf12b6bcc250acecf9f64b9a1e165e72`; `esvTag` "(ESV)", `thsv11Tag` "(THSV11)" |
| C5 | no `cost`/`price` field anywhere | 0 (also none in `state`) |

| # | Where | Ref | SHA-256 `en` | SHA-256 `th` |
|---|---|---|---|---|
| 1 | weekly | Psalm 23:1 | `f1705f7a9f458f3af425d0e9349a63c083a427fe4a8187d5c5edf526ef7f1359` | `a8644331ac55acf72237214f39790ba2dc957085150f13bf3722beeef814e302` |
| 2 | weekly | Philippians 4:13 | `487c8dabbe69e71ae936cd6ee678aa7689b84cc41d16d280ed00108a6e3b99a6` | `56d1f514847ab0a8d5184954e1014bb3633ccb38e55476f550c84311c509dcb9` |
| 3 | weekly | Isaiah 41:10 | `4674974e42c4f623b02d49598d03c383379f89da0540bf91a738281c55aea30c` | `9f70f2ea2933b8fce8730c21e150166eac355eabb7cdc99741e57b841b6a4043` |
| 4 | weekly | Proverbs 3:5 | `1ec2d679747dc325d9280757ef037a62065d4ba6557fb1f5592f2105d85e47e1` | `9d9f5efb7307e308ba120b073494d191477729c0a6cd48a0af8f7fd2a57a752b` |
| 5 | weekly | John 3:16 | `32e40b04d0b88fd0d930834ebe4d9f5f6550bceee01b31ecace16afe6185fe2f` | `4d7693976837d541e7ae0988d67575231fe50e918e8bb2fc24a91727c0e5b8cf` |
| 6 | weekly | Psalm 139:14 | `57c4e1aa185268f1eaa5390107b04118008eb1d1f90e210539592bb1e64138c7` | `d5ccbe09ce996aedeb0f845d9bcaa79ea84f2a59fccbc5341a4729d4cde67246` |
| 7 | weekly | Joshua 1:9 | `c5ae6ffe8dc4b620c04f062d1d071ef75d68a760d4b39c599d88be1bb4695aad` | `b28b2e4ba52ce2705bf5daae091ff0305b259a119afb212f4f43792844245c1c` |
| 8 | weekly | Luke 2:11 | `2ec801016ce3732005294b96b48db1226ee7945cf99231eacd786e8e822ef98f` | `debfabbac6ae25bdf9e2939050e99fe466a0e36eff96901aceb401a9372cd48e` |
| 9 | weekly | Romans 8:28 | `1d77ca32bca082b65d620a949f5a51e72d08201f1406e42fffb67509ebf0263c` | `1b245ce6778954817562e3f5d639e85942f86b852556b26900df898566ac4602` |
| 10 | weekly | Psalm 46:1 | `8764b05191b61f1eb9dde110bb6dbfaebcedca4238a5f63f8ed400c6278f72e5` | `4e937b33dd3c4d4e33146a099f9ab7f3dd2457110a4dd7ca038e289a550998cd` |
| 11 | rest | Matthew 11:28 | `f676da3d0b8c154dd85fe4a2c7a83213cfc69d1cb50a1147aa3d311c15992bf7` | `f7f61a967a85cc6961ad543c6db8d63d9bded0f9eb5ceb1cc5d1ed8a389bb7d8` |
| 12 | boss:phonics | Genesis 1:1 | `e1e1f5e1738c9f78a106da32b1b203168c41b74d4a4f8d3e0ef4d1f7759ea766` | `e697ceabb277e44ec0d4a5a531ab2e898ee71b43f8e719875398a383b2d7d31e` |
| 13 | boss:colors-shapes | Genesis 9:13 | `026b526d0a4b8b116603f707cab87bb7d517ba5e7d7a34aca90531c1cabd55c1` | `36d14074de8261784d37df0b770e1420c3404b4a00a7e24e7fc49217f48efe07` |
| 14 | boss:numbers | John 6:9 | `7d6b4a7b4119e43e0d78bfabed0592ba03308780c74e26d5afd79c23f1a92cfe` | `4f10818adf958f78ca5d6127afd974f18b0af4cc286db3dca85b7985ba7be5d5` |
| 15 | boss:sight-words | 1 Samuel 17:45 | `a2c5ea0419e979bdd9e85da53c2087eb878ebcc3b8883fdeda1e9f0b1226d055` | `2088b11140ad3a5eff68545885fde609da065a56141395bf31fe01095c566504` |
| 16 | boss:baby-hospital | Isaiah 40:11 | `e33fd062ffe74888b4ddafa37b5cdc0d2560fff2c4369f83e9fb500190473289` | `71046ef814e03db41e20ffa1a7ddc367061f4a42d366308621436e589d60e8c5` |

| # | Jesus words | SHA-256 `en` | SHA-256 `th` |
|---|---|---|---|
| 1 | John 15:9 | `093abe82cf29270999c20125673569564a14f516e5e1593eca81484cea73d771` | `019d3a4763f6da4787751a1da6c0d26b36d5e1aa3a01367bc04f0c1421d57c61` |
| 2 | Luke 12:7 | `d0b63a99cae0382e2f86bfee39e2444182fe00c6b12076154d12aa04db931f9e` | `7c5a28ab524ad83fbea5442006b1f5dcbfff70b30fafc58b4041707e1ac50c63` |
| 3 | John 14:1 | `4cef51ffef80eae9226b98758bd69fbf992958950aa28923d5aba9005daf7970` | `8bf7d07b1c2562cf7412911a69f939e60728c4fcec7bc2c786d1cd76fe0026d2` |
| 4 | John 10:11 | `a2fff2f43c92a1cdcaa563a19e7b9fca9e612a433103df1b932209877d833e30` | `39f1073d04caf0d5c6b034801d0c05843c17c884ee2f2a7040dd0fa7f353f5c4` |
| 5 | John 8:12 | `7e9976f466b8ebd4b99bc615a6f7eb0cc728afce8281985be032bf3ac26f3335` | `27b85bbc7dd6fd1bbd8eaaae5fdbd03b0726d27dcbe616bbeec59ba6f6a3b601` |
| 6 | John 15:11 | `99737378982cd6ce1da5dcfdc9df51c67a4c74b0d4e464f8f54c5373513a570d` | `c5f5b9f69911ae1437ff31ff4897ed7c34df29ba02efece08b44d89828d44376` |

## D. Strings, art, trophies

| # | Check | Expected |
|---|---|---|
| D1 | `uiText` keys | 98 (= `meta.uiTextEntries`); every key used somewhere in the UI |
| D2 | `encouragement` lines | 7 |
| D3 | `trophies` | 42 (= `meta.trophies`; by `meta.trophiesByCat`: gear 17, themes 14, gems 5, titles 6) |
| D4 | `soundDuel.pairs` | 30, of which 6 carry `pics` |
| D5 | `picPlan.svg` / `trophySvg` / `uiSvg` | 38 / 24 / 1 |
| D6 | supplied inline art (inline exactly, never redraw) | `inlineSvg` 5 (crib, front-desk, tie, towel, towel-white); `trophyInlineSvg` 3 (frame-gold, frame-silver, lanterns-blue); `uiInlineSvg` 7 (aura, nancy, sam, stone, sword, tex, title) |
| D7 | drawings Build makes | 55 = `svgDrawnCount` 33 + `trophySvgDrawnCount` 21 + 1 coin |
| D8 | `pantry.items` | 9 |
| D9 | `version` / `meta.version` | `v6-08` / `v6-08` |
| D10 | Thai untouched | every Thai string in the build equals its `cards.json` string byte for byte |

## E. Join-specific

| # | Check | Expected |
|---|---|---|
| E1 | no `<!-- Part N of 2` header text anywhere in the build | 0 |
| E2 | the build used both parts | every section 7 row in COMBINE-GUIDE resolves; 0 missing |
| E3 | joined prompt (if hashable) | md5 `5e1666fe6f7189d3886686749335b3ee`, 188,007 chars |

**Quartermaster:** Based on: snap-r2h-0021MDT, pointer f6dac2d0, PASTE 317e91ce (CURRENT-SNAP); kit built on candidate 5e1666fe (not yet frozen as pointer).
**Quartermaster:** Ready to paste: none. This is a draft kit, and CURRENT stays v5-37.
