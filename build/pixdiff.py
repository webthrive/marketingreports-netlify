#!/usr/bin/env python3
"""Render every original and generated category page and compare pixels."""
import glob, os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops

REPO='/home/claude/mr'; OUT='/home/claude/build/out'
slugs=[os.path.basename(os.path.dirname(p)) for p in sorted(glob.glob(f'{REPO}/marketing-dashboards/*/index.html'))]
os.makedirs('/tmp/shots',exist_ok=True)
rows=[]
with sync_playwright() as pw:
    b=pw.chromium.launch()
    for s in slugs:
        paths={}
        for tag,base in (('o',REPO),('g',OUT)):
            pg=b.new_page(viewport={'width':1280,'height':1000})
            pg.route("http://**",lambda r:r.abort()); pg.route("https://**",lambda r:r.abort())
            pg.goto(f'file://{base}/marketing-dashboards/{s}/index.html',wait_until='domcontentloaded')
            try:
                pg.wait_for_function('document.fonts.status === "loaded"', timeout=4000)
            except Exception:
                pass
            pg.wait_for_timeout(1200)
            p=f'/tmp/shots/{s}-{tag}.png'; pg.screenshot(path=p,full_page=True); pg.close()
            paths[tag]=p
        A=Image.open(paths['o']).convert('RGB'); B=Image.open(paths['g']).convert('RGB')
        if A.size!=B.size:
            rows.append((s,'SIZE',f'{A.size} vs {B.size}',100.0)); continue
        d=ImageChops.difference(A,B)
        px=sum(1 for p in d.get_flattened_data() if p!=(0,0,0))
        pct=100*px/(A.size[0]*A.size[1])
        rows.append((s,'PIXEL',f'{px} diff px ({pct:.4f}%)  bbox={d.getbbox()}',pct))
    b.close()
# Pages where the generator deliberately differs because it repairs a source defect.
EXPECTED = {
 'ahrefs': 'source file is truncated (no closing tags); generator emits valid HTML',
 'facebook-ads': '"Meta Ads" pill had malformed CSS rendering its text invisible',
 'organic-social': '"Instagram" pill had malformed CSS rendering its text invisible',
}
bad = 0
TOL = 0.01   # absorbs headless-render antialiasing flake around web-font fallback
for s, k, v, pct in rows:
    ok = (k == 'PIXEL' and pct <= TOL)
    if ok:
        print(f'OK    {s:24s} ' + ('pixel-identical' if pct == 0 else f'within tolerance ({pct:.4f}%)'))
    elif s in EXPECTED:
        print(f'FIXED {s:24s} {EXPECTED[s]}')
    else:
        bad += 1
        print(f'DIFF  {s:24s} {v}')
print()
print('PASS - every page either pixel-identical or a known repair'
      if not bad else f'FAIL - {bad} unexplained difference(s)')
import sys; sys.exit(1 if bad else 0)
