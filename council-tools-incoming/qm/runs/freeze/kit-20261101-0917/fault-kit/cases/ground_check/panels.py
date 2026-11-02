"""Auditor fault kit: split a contact sheet into its panels at the cream gaps (kit-side, so a whole-sheet tool can be judged per panel).
Background = the sheet colour at (H/2, 15). A panel column is one where < 90% of the middle 65% of rows is background; a panel is a
run of such columns > 60 px wide; its rows are the longest run where both its frame edges (3 px) are not background."""
import numpy as np
from PIL import Image
def runs(mask, minlen):
    out = []; s = None
    for i in range(len(mask) + 1):
        v = i < len(mask) and mask[i]
        if v and s is None: s = i
        if not v and s is not None:
            if i - s >= minlen: out.append((s, i - 1))
            s = None
    return out
def split(path):
    im = Image.open(path).convert('RGB'); a = np.asarray(im).astype(int); H, W, _ = a.shape; bg = a[H // 2, 15]
    cream = np.abs(a - bg).max(axis=2) <= 6
    cols = runs(cream[int(H * .15):int(H * .8)].mean(axis=0) < .9, 61); boxes = []
    for x0, x1 in cols:
        rr = runs((~cream[:, x0:x0 + 3]).all(axis=1) & (~cream[:, x1 - 2:x1 + 1]).all(axis=1), 1)   # rows where the panel's own left and right frame edges are not background
        y0, y1 = max(rr, key=lambda r: r[1] - r[0]); boxes.append((x0, y0, x1 + 1, y1 + 1))
    return im, boxes
