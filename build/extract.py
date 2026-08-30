"""Extract dashboard entries from the hand-coded category pages into a catalog."""
import json, re, glob, os
from bs4 import BeautifulSoup

REPO = '/home/claude/mr'
CATS = {}
ENTRIES = []

VAL = r'(?:[^;"]|\([^)]*\))+'          # a CSS value, tolerating parens

def prop(style, name, default=''):
    """Read one declaration's value: last *valid* wins.

    Two pills in the source carry a truncated trailing declaration
    (`background:rgba(24,119,242` with no closing paren). Chrome's error
    recovery turns those into an opaque fill that matches the text colour,
    rendering the label invisible. Skipping unbalanced values restores the
    tint the author intended.
    """
    ms = [m.strip() for m in
          re.findall(rf'(?:^|;)\s*{name}\s*:\s*({VAL})', style or '')]
    for v in reversed(ms):
        if v.count('(') == v.count(')'):
            return v
    return default


def inner(el):
    """Inner HTML, preserving inline markup (<strong>, <em>, links)."""
    if not el:
        return ''
    return re.sub(r'\s+', ' ', ''.join(str(c) for c in el.contents)).strip()


def txt(el):
    return re.sub(r'\s+', ' ', el.get_text(' ', strip=True)).strip() if el else ''

for path in sorted(glob.glob(f'{REPO}/marketing-dashboards/*/index.html')):
    slug = os.path.basename(os.path.dirname(path))
    if slug == 'marketing-dashboards':
        continue
    soup = BeautifulSoup(open(path, encoding='utf-8').read(), 'html.parser')

    head = {
        'title': txt(soup.title),
        'description': (soup.find('meta', attrs={'name': 'description'}) or {}).get('content', ''),
        'canonical': (soup.find('link', rel='canonical') or {}).get('href', ''),
        'og_image': (soup.find('meta', property='og:image') or {}).get('content', ''),
        'robots': (soup.find('meta', attrs={'name': 'robots'}) or {}).get('content', ''),
    }

    h1 = soup.find('h1')
    # h1 has form: "Main text<br><span>accent tail</span>"
    h1_span = h1.find('span') if h1 else None
    h1_accent = txt(h1_span)
    if h1_span:
        h1_span.extract()
    h1_main = txt(h1)

    eyebrow_el = h1.find_previous('div') if h1 else None
    intro_el = h1.find_next('p') if h1 else None

    # hero pills: the div of spans right after the intro paragraph
    pills = []
    if intro_el:
        pill_wrap = intro_el.find_next_sibling('div')
        if pill_wrap:
            for s in pill_wrap.find_all('span'):
                st = s.get('style', '')
                pills.append({'text': txt(s),
                              'bg': prop(st, 'background', 'rgba(0,212,255,.1)'),
                              'fg': prop(st, 'color', 'var(--accent)')})

    # prose sections: every h2 + the paragraphs following it, EXCLUDING card grid
    grid = None
    for d in soup.find_all('div'):
        st = d.get('style', '')
        if 'grid-template-columns:repeat(auto-fill' in st.replace(' ', ''):
            grid = d
            break

    sections = []
    for h2 in soup.find_all('h2'):
        paras = []
        for sib in h2.find_next_siblings():
            if sib.name == 'h2':
                break
            if sib.name == 'p':
                paras.append({'html': inner(sib),
                              'mb': prop(sib.get('style', ''), 'margin-bottom') or None})
            if sib.name == 'div' and sib.find('a', class_='affiliate-cta'):
                break
        hst = h2.get('style', '')
        hsize = re.search(r'font-size:([\d.]+rem)', hst)
        hmargin = re.search(r'margin(?:-bottom)?:([^;"]+)', hst)
        sections.append({'heading': txt(h2), 'paragraphs': paras,
                         'h_size': hsize.group(1) if hsize else '1.15rem',
                         'h_margin': hmargin.group(0) if hmargin else 'margin-bottom:.65rem'})

    # affiliate CTA block (footer "consider a dedicated tool")
    ctas = [{'label': txt(a), 'url': a['href']}
            for a in soup.find_all('a', class_='affiliate-cta')]

    # count label above the grid
    count_label = ''
    if grid:
        prev = grid.find_previous_sibling('div')
        if prev:
            count_label = txt(prev)

    CATS[slug] = {
        'slug': slug,
        'head': head,
        'eyebrow': txt(eyebrow_el),
        'h1_main': h1_main,
        'h1_accent': h1_accent,
        'intro': txt(intro_el),
        'hero_pills': pills,
        'count_label': count_label,
        'sections': sections,
        'footer_ctas': ctas,
    }

    # ---- cards ----
    cards = grid.find_all('a', recursive=False) if grid else []
    for i, a in enumerate(cards):
        divs = a.find_all('div', recursive=False)
        preview = divs[0] if divs else None
        preview_style = preview.get('style', '') if preview else ''
        img = preview.find('img') if preview else None
        svg = preview.find('svg') if preview else None

        # header row: badge initials, name, vendor, price
        namewrap = a.find('div', style=re.compile(r'font-size:1\.05rem'))
        name = txt(namewrap)
        vendor = txt(namewrap.find_next_sibling('div')) if namewrap else ''
        badge = a.find('div', style=re.compile(r'width:32px'))
        badge_initials = txt(badge)
        badge_style = badge.get('style', '') if badge else ''
        badge_color = badge_bg = ''
        if badge:
            st = badge.get('style', '')
            badge_color = prop(st, 'color')
            badge_bg = prop(st, 'background')

        price_el = a.find('span', style=re.compile(r'white-space:nowrap'))
        price = txt(price_el)
        price_style = price_el.get('style', '') if price_el else ''
        pst = price_style
        price_bg = prop(pst, 'background')
        price_fg = prop(pst, 'color')

        blurb_el = a.find('p')
        tags_wrap = blurb_el.find_next_sibling('div') if blurb_el else None
        tags = [txt(s) for s in tags_wrap.find_all('span')] if tags_wrap else []

        cta_el = a.find('div', style=re.compile(r'font-size:\.75rem'))
        cta_style = cta_el.get('style', '') if cta_el else ''
        cst = cta_style
        cta_color = prop(cst, 'color', 'var(--accent)')

        ENTRIES.append({
            'id': f'{slug}-{i+1:02d}',
            'category': slug,
            'position': i + 1,
            'name': name,
            'vendor': vendor,
            'badge_initials': badge_initials,
            'badge_color': badge_color,
            'badge_bg': badge_bg,
            'badge_style': badge_style,
            'price_style': price_style,
            'cta_style': cta_style,
            'card_style': a.get('style', ''),
            'url': a.get('href', ''),
            'price_tier': price,
            'price_bg': price_bg,
            'price_fg': price_fg,
            'blurb': txt(blurb_el),
            'tags': tags,
            'cta_label': txt(cta_el),
            'cta_color': cta_color,
            'preview_style': preview_style,
            'image_src': img.get('src') if img else None,
            'image_alt': img.get('alt') if img else None,
            'image_onerror': img.get('onerror') if img else None,
            'image_style': img.get('style') if img else None,
            'image_loading': img.get('loading') if img else None,
            'has_inline_svg': svg is not None,
            'rel': ' '.join(a.get('rel', [])),
            # to be filled by triage
            'link_type': None,
            'verified_on': None,
            'screenshot': None,
            'alt': None,
        })

# ---- dedupe the inline placeholder SVGs (14 unique across 60 cards) ----
import hashlib
PLACEHOLDERS = {}
order = {}
for path in sorted(glob.glob(f'{REPO}/marketing-dashboards/*/index.html')):
    slug = os.path.basename(os.path.dirname(path))
    order[slug] = []
    for m in re.finditer(r'<svg\b.*?</svg>', open(path, encoding='utf-8').read(), re.S):
        key = 'ph-' + hashlib.md5(m.group(0).encode()).hexdigest()[:6]
        PLACEHOLDERS[key] = m.group(0)
        order[slug].append(key)
for e in ENTRIES:
    e['placeholder'] = order[e['category']][e['position'] - 1]

json.dump({'categories': CATS, 'entries': ENTRIES, 'placeholders': PLACEHOLDERS},
          open('/home/claude/build/dashboards.json', 'w'), indent=2)

print(f'categories: {len(CATS)}')
print(f'entries:    {len(ENTRIES)}')
missing = [e['id'] for e in ENTRIES if not e['name'] or not e['url']]
print(f'incomplete: {missing or "none"}')
print(f'with img:   {sum(1 for e in ENTRIES if e["image_src"])}')
print(f'with svg:   {sum(1 for e in ENTRIES if e["has_inline_svg"])}')
print(f'placeholders (deduped): {len(PLACEHOLDERS)}')
