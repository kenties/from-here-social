#!/usr/bin/env python3
"""Render a From Here static post from a saved design spec.

usage: python3 tools/render.py '<json spec>' out.jpg
spec: {"base": "stage/batch-14/slot-109-base.jpg",
       "lines": ["Send a","Thanksgiving","moment."], "sz": 100, "y": 118,
       "sub": "to whoever's at your table.", "subY": 1122,
       "url": true, "urlY": 1190}
Text-free base is 1080x1350. Fonts are in stage/fonts. This is the same layout the
Studio editor previews, so keep the two in step.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ROOT, 'stage/fonts/SpaceGrotesk-SemiBold.ttf')
LIGHT = (246, 243, 236)
RUST = (226, 124, 80)
X = 92
MAXW = 1080 - 2 * X   # 896
PITCH = 1.06

def sg(sz): return ImageFont.truetype(FONT, sz)

def fit(lines, top):
    """Largest size <= top where the widest line fits."""
    for sz in range(top, 39, -2):
        f = sg(sz)
        if all(f.getlength(t) <= MAXW for t in lines): return sz
    return 40

def render(spec, out):
    t = Image.open(os.path.join(ROOT, spec['base'])).convert('RGB')
    d = ImageDraw.Draw(t)
    lines = [l for l in spec.get('lines', []) if l.strip()]
    if lines:
        sz = fit(lines, int(spec.get('sz', 100))); f = sg(sz)
        for k, s in enumerate(lines):
            d.text((X, int(spec.get('y', 118)) + int(k * sz * PITCH)), s, font=f, fill=LIGHT)
    if spec.get('sub', '').strip():
        sz = 44
        while sz > 24 and sg(sz).getlength(spec['sub']) > MAXW: sz -= 2
        d.text((X, int(spec.get('subY', 1122))), spec['sub'], font=sg(sz), fill=LIGHT)
    if spec.get('url'):
        f = sg(46); x = X; y = int(spec.get('urlY', 1190))
        for s, c in (('mailed', LIGHT), ('fromhere', RUST), ('.com', LIGHT)):
            d.text((x, y), s, font=f, fill=c); x += int(d.textlength(s, font=f))
    t.save(out, quality=88)

if __name__ == '__main__':
    render(json.loads(sys.argv[1]), sys.argv[2])
