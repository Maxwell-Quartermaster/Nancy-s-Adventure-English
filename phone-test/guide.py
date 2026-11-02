# Phone-test guide for Maxwell (390 wide): the v6-08 three-file paste into Build. Build's own menus are not documented on the box, so the steps stay generic.
import subprocess, os, hashlib
W = '/workspace/'; N = 'nancys-adventure-english-v6-08'
F = [(N + '-PASTE.md', 'the game'), (N + '-daily-verses.json', 'the daily verses'), (N + '-title.svg', 'the title picture')]
def info(f):
    b = open(W + f, 'rb').read(); return len(b.decode('utf-8')), hashlib.md5(b).hexdigest()
rows = ''
for i, (f, what) in enumerate(F, 1):
    n, m = info(f); assert m[:8] in ('95a4d0fc', '81295c9f', 'bab91ec9')
    rows += (f"<div class='file'><div class='num'>{i}</div><div><div class='fn'>{f}</div><div class='sm'>{what} · {n:,} characters</div><div class='md5'>md5 {m}</div></div></div>")
step = lambda n, t, body: f"<div class='card'><div class='st'><span class='num'>{n}</span>{t}</div>{body}</div>"
pic = lambda p, cap: f"<figure><img src='{p}'><figcaption>{cap}</figcaption></figure>"
html = f"""<!doctype html><html><head><meta charset='utf-8'><style>
body{{margin:0;width:390px;background:#F4ECD8;font:16px/1.45 'DejaVu Sans',sans-serif;color:#3A2410}}
h1{{font:400 28px/1.15 'Lilita One',sans-serif;margin:18px 16px 4px}} .sub{{margin:0 16px 12px;font-size:14px}}
.card{{margin:12px 16px;background:#F6E9C8;border:2px solid #10170F;border-radius:14px;box-shadow:inset 0 0 0 3px #E8B84A,0 4px 0 #10170F;padding:14px}}
.st{{font:400 21px/1.2 'Lilita One',sans-serif;margin-bottom:6px;display:flex;align-items:center;gap:10px}}
.num{{flex:none;width:32px;height:32px;border-radius:50%;background:#FFCC33;border:2px solid #10170F;display:inline-flex;align-items:center;justify-content:center;font:400 18px 'Lilita One',sans-serif}}
.file{{display:flex;gap:10px;align-items:flex-start;margin:8px 0}} .fn{{font-weight:bold;font-size:14px;word-break:break-all}} .sm{{font-size:13px;color:#5A4A3A}}
\n.md5{{font:12px/1.4 'DejaVu Sans Mono',monospace;color:#3A2410;word-break:break-all}} .ok{{color:#2F7D3A;font-weight:bold}} .stop{{color:#7A1E12;font-weight:bold}}
figure{{margin:10px 0 0;text-align:center}} img{{width:230px;border:2px solid #10170F;border-radius:10px}} figcaption{{font-size:13px;margin-top:4px}}
.note{{margin:12px 16px 20px;font-size:12px;color:#5A4A3A}} ul{{margin:6px 0 0 0;padding-left:20px}} li{{margin:4px 0}}
</style></head><body>
<h1>Phone test: v6-08 in Build</h1>
<div class='sub'>Three files, three messages, in this order. Oct 31, 2026.</div>
{step('', 'Before you start', "<ul><li>Use a <b>new, empty</b> Build project. Never Nancy's real one.</li><li><b>The current version stays v5-37 until this test passes.</b></li><li>Have these three files on your phone:</li></ul>" + rows).replace("<span class='num'></span>", '')}
{step(1, 'Send file 1: the game', "<ul><li>Open a new message in Build.</li><li>Open file 1, copy <b>all</b> of its text, and paste it in.</li><li>Send, then <b>wait for Build's reply</b> before doing anything else.</li></ul>")}
{step(2, 'Send file 2: the verses', "<ul><li>New message. Copy <b>all</b> of file 2 and paste it in.</li><li>Send and wait for the reply.</li></ul>")}
{step(3, 'Send file 3: the title picture', "<ul><li>New message. Copy <b>all</b> of file 3 and paste it in.</li><li>Send and wait until Build says it is done.</li></ul>")}
{step(4, 'What success looks like', "<ul><li class='ok'>Each send goes through with no error and no 'too long' message.</li><li class='ok'>Build reports PASS for each of the four build stages.</li><li class='ok'>The app opens on the mountain title with 'Start your day' (the sky follows the clock).</li></ul>" + pic('01-title.png', 'Title screen') + pic('02-main-menu-verse-popup.png', 'Menu: verse of the day, English and Thai') + pic('05-map-day1.png', 'Adventure Map'))}
{step(5, 'If something looks wrong', "<ul><li class='stop'>An error on send, a 'too long' reply, or Build saying it shortened or summarized a file.</li><li class='stop'>A different title picture, missing Thai, or a verse that is cut off.</li><li>Stop there. Take a screenshot and send it with the step number. Don't paste again into the same project.</li></ul>")}
<div class='note'>Pictures are the v6-08 design renders; Build's drawing will differ in detail. Build's own menus and buttons aren't documented on this computer, so these steps describe what to send, not which buttons to press.</div>
</body></html>"""
open('phone-test-guide-390.html', 'w').write(html)
subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=2', '--window-size=390,4200', '--screenshot=' + os.getcwd() + '/_full.png', 'file://' + os.getcwd() + '/phone-test-guide-390.html'], capture_output=True, timeout=120)
from PIL import Image, ImageChops
im = Image.open('_full.png').convert('RGB'); bg = Image.new('RGB', im.size, (0xF4, 0xEC, 0xD8)); bb = ImageChops.difference(im, bg).getbbox()
im.crop((0, 0, im.width, min(im.height, bb[3] + 30))).save('phone-test-guide-390.png'); os.remove('_full.png'); print(im.size, bb)
