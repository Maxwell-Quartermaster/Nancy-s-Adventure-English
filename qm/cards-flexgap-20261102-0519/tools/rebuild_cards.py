# rebuild_cards.py <src PASTE> <out>: Instructor DRAFT.md 5f3f2184 "1A lean + meta + spec cleanup" (:43-54), applied by exact-once replaces
import sys, json
src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b):
    global s
    c = s.count(a); assert c == 1, (c, a[:80]); s = s.replace(a, b)
import re
L = s.split('\n'); j = json.loads(L[426])
old = {}
for cid in ('bh-30', 'ms-28', 'ms-29', 'ms-30'):
    m = re.findall(r'\{"id":"' + cid + r'"[^{}]*\}', L[426]); assert len(m) == 1, (cid, m); old[cid] = m[0]
new = {
 'bh-30': '{"id":"bh-30","type":"say-it","en":"The baby is kicking.","th":"ลูกดิ้นค่ะ","respell":"thuh BAY-bee iz KIK-ing","personal":true}',
 'ms-28': '{"id":"ms-28","type":"say-it","en":"Here is your key.","th":"นี่กุญแจของคุณค่ะ","respell":"HEER iz yor KEE","personal":true}',
 'ms-29': '{"id":"ms-29","type":"say-it","en":"This is my husband.","th":"นี่สามีของฉันค่ะ","respell":"THIS iz mai HUZ-bund","personal":true}',
 'ms-30': '{"id":"ms-30","type":"say-it","en":"God is good.","th":"พระเจ้าทรงดีครับ","respell":"GOD iz GUD","faith":true,"personal":true}'}
for k in new: print('OLD', old[k]); rep(old[k], new[k])
rep('"emptySlots":["bh-30","ms-28","ms-29","ms-30"]', '"emptySlots":[]')
rep('"writtenCards":207', '"writtenCards":211'); rep('"sayItWritten":33', '"sayItWritten":37'); rep('"personalWritten":76', '"personalWritten":80')
rep('`mode: "english-first"`: 70 written plus the 4 empty slots (section 17).', '`mode: "english-first"`.')
rep('in `cards.json`: 207 written plus 4 empty personal slots. Format:', 'in `cards.json`. Format:')
rep(', personal, slot?, prompts?', ', personal, prompts?')
rep(' `slot` names an empty slot\'s topic.', '')
rep('Four empty say-it cards wait for Maxwell (`fill:true`, `personal:true`, empty `en`, `th`, `respell`), skipped until written, then sorted first:', 'Four personal say-it cards, Instructor drafts for Maxwell to confirm or edit, sorted first:')
open(out, 'w', encoding='utf-8').write(s)
print('len', len(s), 'delta', len(s) - len(open(src, encoding='utf-8').read()), 'bank', 188200 - len(s))
