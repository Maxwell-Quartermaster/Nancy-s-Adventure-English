#!/bin/bash
cd /workspace/qm/cards-flexgap-20261102-0519
for s in 390x844 375x667 320x568; do w=${s%x*}; h=${s#*x}
  FREEZE=1 node tools/cdp.mjs $w $h png/before-$w html/base-$w/*.html > runs/geo-base-$w.jsonl || echo FAIL base $w
  FREEZE=1 node tools/cdp.mjs $w $h png/after-$w html/new-$w/*.html > runs/geo-new-$w.jsonl || echo FAIL new $w; done
FREEZE=1 node tools/cdp.mjs 320 568 png/fit320-before html/fit320-base/*.html > runs/geo-fit320-base.jsonl || echo FAIL fb
FREEZE=1 node tools/cdp.mjs 320 568 png/fit320-after html/fit320-new/*.html > runs/geo-fit320-new.jsonl || echo FAIL fn
echo DONE
