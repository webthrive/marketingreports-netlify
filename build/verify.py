#!/usr/bin/env python3
"""Semantic diff: does the generated page carry the same content as the original?

Compares meaning, not bytes: head metadata, hero copy, prose sections, and every
card's name/vendor/url/price/blurb/tags. Formatting differences are expected and ignored.
"""
import glob, os, re, sys
from bs4 import BeautifulSoup

REPO = '/home/claude/mr'
OUT = '/home/claude/build/out'

def norm(s):
    return re.sub(r'\s+', ' ', (s or '')).strip()

def fingerprint(path):
    soup = BeautifulSoup(open(path, encoding='utf-8').read(), 'html.parser')
    fp = {}
    fp['title'] = norm(soup.title.get_text() if soup.title else '')
    for n in ('description', 'robots'):
        m = soup.find('meta', attrs={'name': n})
        fp[f'meta:{n}'] = norm(m.get('content') if m else '')
    can = soup.find('link', rel='canonical')
    fp['canonical'] = can.get('href') if can else ''
    for p in ('og:title', 'og:description', 'og:url', 'og:image'):
        m = soup.find('meta', property=p)
        fp[p] = norm(m.get('content') if m else '')

    h1 = soup.find('h1')
    fp['h1'] = norm(h1.get_text(' ') if h1 else '')
    fp['h2s'] = [norm(h.get_text(' ')) for h in soup.find_all('h2')]

    # all body prose paragraphs, in order
    main = soup.find('main')
    fp['paragraphs'] = [norm(p.get_text(' ')) for p in main.find_all('p')] if main else []

    # cards
    grid = None
    for d in soup.find_all('div'):
        if 'grid-template-columns:repeat(auto-fill' in d.get('style', '').replace(' ', ''):
            grid = d
            break
    cards = []
    for a in (grid.find_all('a', recursive=False) if grid else []):
        nm = a.find('div', style=re.compile(r'font-size:1\.05rem'))
        badge = a.find('div', style=re.compile(r'width:32px'))
        price = a.find('span', style=re.compile(r'white-space:nowrap'))
        blurb = a.find('p')
        tw = blurb.find_next_sibling('div') if blurb else None
        cards.append({
            'url': a.get('href'),
            'name': norm(nm.get_text() if nm else ''),
            'vendor': norm(nm.find_next_sibling('div').get_text()) if nm and nm.find_next_sibling('div') else '',
            'badge': norm(badge.get_text() if badge else ''),
            'price': norm(price.get_text() if price else ''),
            'blurb': norm(blurb.get_text() if blurb else ''),
            'tags': [norm(s.get_text()) for s in tw.find_all('span')] if tw else [],
        })
    fp['cards'] = cards

    # affiliate CTAs
    fp['ctas'] = [(norm(a.get_text()), a.get('href')) for a in soup.find_all('a', class_='affiliate-cta')]
    return fp


# Content we changed on purpose after the migration was proven lossless.
# Anything NOT listed here that differs is an unintended regression.
INTENTIONAL = {
    'ahrefs': {'title', 'meta:description', 'og:title', 'og:description', 'h1', 'h2s'},
}

fails = 0
for src in sorted(glob.glob(f'{REPO}/marketing-dashboards/*/index.html')):
    slug = os.path.basename(os.path.dirname(src))
    gen = f'{OUT}/marketing-dashboards/{slug}/index.html'
    if not os.path.exists(gen):
        print(f'MISSING  {slug}'); fails += 1; continue
    a, b = fingerprint(src), fingerprint(gen)
    allowed = INTENTIONAL.get(slug, set())
    diffs, intended = [], []
    for k in a:
        if a[k] != b.get(k):
            (intended if k in allowed else diffs).append(k)
    if intended and not diffs:
        print(f'OK*      {slug}  ({len(a["cards"])} cards) - intentional edits: {sorted(intended)}')
        continue
    if diffs:
        fails += 1
        print(f'DIFF     {slug}: {diffs}')
        for k in diffs:
            av, bv = a[k], b.get(k)
            if isinstance(av, list) and isinstance(bv, list):
                for i, (x, y) in enumerate(zip(av, bv)):
                    if x != y:
                        print(f'    [{i}] orig: {str(x)[:150]}')
                        print(f'         gen: {str(y)[:150]}')
                if len(av) != len(bv):
                    print(f'    length {len(av)} -> {len(bv)}')
            else:
                print(f'    orig: {str(av)[:180]}')
                print(f'     gen: {str(bv)[:180]}')
    else:
        print(f'OK       {slug}  ({len(a["cards"])} cards, {len(a["paragraphs"])} paras)')

print()
print('FAILED' if fails else 'ALL PAGES SEMANTICALLY IDENTICAL')
sys.exit(1 if fails else 0)
