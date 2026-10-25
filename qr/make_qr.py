#!/usr/bin/env python3
"""Draw the site's QR code in the wrapper style.

    python3 qr/make_qr.py            # writes qr/whiterabbit-qr.svg and qr/card.html

The QR (error correction H) is printed in wrapper blue with round modules, the three
finder eyes are rounded squares with a red centre, and the papercut rabbit from
index.html sits on a milk badge in the middle. card.html puts it on a wrapper-style
card; render it with render.js.
"""
import pathlib, re, segno

URL = "https://dsaad68.github.io/whiterabbit/"
HERE = pathlib.Path(__file__).resolve().parent
BLUE, INK, RED, MILK = "#1D4EA6", "#13295C", "#E1252B", "#FBF6E9"
QUIET = 2   # modules of white margin; the card adds more

qr = segno.make(URL, error="h", micro=False, boost_error=False)
m = [list(r) for r in qr.matrix]
n = len(m)

# the rabbit from the page, with its line weights written in (the page sets them in CSS)
page = (HERE.parent / "index.html").read_text(encoding="utf-8")
sym = re.search(r'<symbol id="rabbit-sym" viewBox="0 0 240 170">(.*?)</symbol>', page, re.S).group(1)
sym = sym.replace('class="k-back"', 'stroke-width="6"').replace('class="k-main"', 'stroke-width="6"').replace('class="k-line"', 'stroke-width="4"').replace(' class="rb"', "")

# keep-out: the three finders (with separator) and the centre badge
def in_finder(r, c):
    return (r < 8 and c < 8) or (r < 8 and c >= n - 8) or (r >= n - 8 and c < 8)

bw, bh = 13, 9                       # badge size in modules (the rabbit is 240 x 170)
br0, bc0 = (n - bh) // 2, (n - bw) // 2
def in_badge(r, c):
    return br0 <= r < br0 + bh and bc0 <= c < bc0 + bw

parts = []
for r in range(n):
    for c in range(n):
        if m[r][c] and not in_finder(r, c) and not in_badge(r, c):
            parts.append(f'<circle cx="{c + QUIET + .5}" cy="{r + QUIET + .5}" r=".46"/>')

def eye(r, c):
    x, y = c + QUIET, r + QUIET
    return (f'<rect x="{x + .5}" y="{y + .5}" width="6" height="6" rx="1.9" fill="none" stroke="{BLUE}" stroke-width="1"/>'
            f'<rect x="{x + 2}" y="{y + 2}" width="3" height="3" rx="1" fill="{RED}"/>')

eyes = eye(0, 0) + eye(0, n - 7) + eye(n - 7, 0)
bx, by = bc0 + QUIET + .35, br0 + QUIET + .35
badge = (f'<rect x="{bx}" y="{by}" width="{bw - .7}" height="{bh - .7}" rx="2.2" fill="{MILK}" stroke="{BLUE}" stroke-width=".28"/>'
         f'<svg x="{bx + .9}" y="{by + .55}" width="{bw - 2.5}" height="{bh - 1.8}" viewBox="0 0 240 170">'
         f'<g stroke-linejoin="round" stroke-linecap="round">{sym}</g></svg>')

size = n + 2 * QUIET
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size * 16}" height="{size * 16}" '
       f'role="img" aria-label="QR code for {URL}"><title>{URL}</title>'
       f'<rect width="{size}" height="{size}" fill="#fff"/>'
       f'<g fill="{BLUE}">{"".join(parts)}</g>{eyes}{badge}</svg>')
(HERE / "whiterabbit-qr.svg").write_text(svg, encoding="utf-8")

candy = (HERE.parent / "index.html").read_text(encoding="utf-8")
candy = re.search(r'<symbol id="candy-sym" viewBox="0 0 170 68">(.*?)</symbol>', candy, re.S).group(1)
candy = candy.replace("var(--end, #fff)", "#fff").replace("url(#candyShade)", "none")

rab = '<svg viewBox="0 0 240 170"><g stroke-linejoin="round" stroke-linecap="round">' + sym.replace('stroke-width="6"', 'stroke-width="11"').replace('stroke-width="4"', 'stroke-width="5"') + '</g></svg>'
unit = f'<span>{rab}大白兔<em>WHITE RABBIT</em>奶糖<em>CREAMY CANDY</em></span>'
run = f'<div class="run">{unit * 4}</div>'

card = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,300..900,0..100,0..1;1,9..144,300..900,0..100,0..1&family=Figtree:wght@400;500;600;700&family=ZCOOL+QingKe+HuangYou&display=block">
<style>
* {{ box-sizing: border-box; margin: 0; }}
html, body {{ background: #fff; }}
.card {{ width: 1080px; height: 1350px; position: relative; overflow: hidden; background: #fff; color: {INK};
  display: flex; flex-direction: column; font-family: Figtree, sans-serif; }}
.band {{ height: 76px; overflow: hidden; border-block: 2.5px solid {BLUE}; flex: none; }}
.band .run {{ display: flex; height: 100%; align-items: center; white-space: nowrap; transform: translateX(-60px); }}
.band .run > span {{ display: inline-flex; align-items: center; gap: 24px; padding-right: 24px; font: 400 31px/1 "ZCOOL QingKe HuangYou"; color: {BLUE}; letter-spacing: .06em; }}
.band .run > span em {{ font: 700 20px/1 Fraunces; font-style: normal; letter-spacing: .18em; color: {RED}; font-variation-settings: "SOFT" 100, "opsz" 24; }}
.band svg {{ width: 54px; height: 39px; }}
.band.b2 .run {{ transform: translateX(-330px); }}
.body {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 0 80px 8px; text-align: center; }}
.eyebrow {{ font: 600 22px/1.2 Figtree; letter-spacing: .16em; text-transform: uppercase; color: {RED}; }}
h1 {{ margin-top: 18px; display: flex; align-items: baseline; gap: 26px; line-height: .9; }}
h1 .zh {{ font: 400 118px/1 "ZCOOL QingKe HuangYou"; color: {BLUE}; letter-spacing: .02em; }}
h1 .lat {{ font: 700 74px/1 Fraunces; font-variation-settings: "SOFT" 100, "WONK" 1, "opsz" 144; letter-spacing: -.02em; color: {INK}; }}
h1 .lat em {{ font-style: italic; font-weight: 400; color: {RED}; }}
.qr {{ margin-top: 44px; width: 720px; height: 720px; padding: 22px; background: #fff; border-radius: 40px;
  box-shadow: 0 0 0 2.5px {BLUE}, 0 0 0 14px #fff, 0 0 0 16.5px {RED}; }}
.qr svg {{ width: 100%; height: 100%; display: block; }}
.scan {{ margin-top: 50px; font: 600 27px/1.2 Figtree; letter-spacing: .04em; color: {INK}; display: flex; gap: 18px; align-items: center; }}
.scan i {{ width: 7px; height: 7px; border-radius: 50%; background: {RED}; }}
.scan .zhs {{ font-family: "ZCOOL QingKe HuangYou"; font-weight: 400; font-size: 31px; color: {BLUE}; }}
.url {{ margin-top: 14px; font: 500 25px/1.2 Figtree; color: {BLUE}; letter-spacing: .01em; }}
.candy {{ position: absolute; width: 170px; height: 68px; }}
</style></head><body>
<div class="card">
  <div class="band">{run}</div>
  <div class="body">
    <p class="eyebrow">Shanghai · creamy candy since 1959</p>
    <h1><span class="zh">大白兔</span><span class="lat">White <em>Rabbit</em></span></h1>
    <div class="qr">{svg}</div>
    <p class="scan">Scan to unwrap <i></i> Scannen &amp; auspacken <i></i> <span class="zhs">扫一扫</span></p>
    <p class="url">dsaad68.github.io/whiterabbit</p>
  </div>
  <svg class="candy" style="left:-44px; top:560px; transform: rotate(-24deg)" viewBox="0 0 170 68">{candy}</svg>
  <svg class="candy" style="right:-46px; top:930px; transform: rotate(18deg)" viewBox="0 0 170 68">{candy}</svg>
  <div class="band b2">{run}</div>
</div>
</body></html>"""
(HERE / "card.html").write_text(card, encoding="utf-8")
print(f"version {qr.version}, {n}x{n} modules, ECC {qr.error}; badge {bw}x{bh} = {bw * bh / n / n:.1%} of the symbol")
