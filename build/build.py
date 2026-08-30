#!/usr/bin/env python3
"""Generate MarketingReports.io category pages, index, and sitemap from dashboards.json.

Usage:  python3 build.py [--out DIR]
Source of truth is dashboards.json. Do not hand-edit generated pages.
"""
import json, os, html, argparse, datetime, re
import hub

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://marketingreports.io'
GTM = 'GTM-WH8BJSG'
STYLE = open(os.path.join(HERE, '_style.html'), encoding='utf-8').read()
DATA = json.load(open(os.path.join(HERE, 'dashboards.json'), encoding='utf-8'))

E = html.escape

# Colors used by the price badge, keyed by tier text.
TIER_STYLE = {
    'Free':   ('rgba(0,229,160,.1)',   'var(--green)'),
    'Free*':  ('rgba(0,229,160,.1)',   'var(--green)'),
    'Freemium': ('rgba(0,212,255,.1)', 'var(--accent)'),
    'Paid':   ('rgba(255,181,71,.12)', 'var(--amber)'),
}
def tier_style(t):
    return TIER_STYLE.get(t, ('rgba(120,120,120,.12)', 'var(--text-muted)'))


def head(title, desc, url, extra_schema=None):
    schema = extra_schema or {
        "@context": "https://schema.org", "@type": "CollectionPage",
        "name": title, "description": desc, "url": url,
        "publisher": {"@type": "Organization", "name": "MarketingReports.io",
                      "url": SITE},
    }
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{GTM}');</script>
<!-- End Google Tag Manager -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="canonical" href="{E(url)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="MarketingReports.io">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{E(url)}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<script type="application/ld+json">
{json.dumps(schema, indent=2)}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Rubik:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
{STYLE}
  <script src="/assets/components.js" defer></script>
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
'''


def card(e):
    """One dashboard card. Screenshot when we have one, placeholder SVG until then."""
    bg = e.get('price_bg') or tier_style(e['price_tier'])[0]
    fg = e.get('price_fg') or tier_style(e['price_tier'])[1]
    ph = DATA['placeholders'].get(e.get('placeholder'), '')

    if e.get('screenshot'):
        # Phase 2: self-hosted screenshot with real alt text.
        alt = e.get('alt') or f"{e['name']} dashboard template by {e['vendor']}"
        preview = (
            f'<picture>'
            f'<source srcset="{E(e["screenshot"].replace(".png", ".webp"))}" type="image/webp">'
            f'<img src="{E(e["screenshot"])}" alt="{E(alt)}" width="380" height="140" '
            f'loading="lazy" decoding="async" '
            f'style="position:absolute;top:0;left:0;width:100%;height:100%;'
            f'object-fit:cover;object-position:top left;display:block">'
            f'</picture>'
        )
    elif e.get('image_src'):
        # Not yet re-shot: keep the original remote image exactly as it was,
        # layered over the placeholder SVG. Phase 2 replaces these per entry.
        attrs = [f'src="{E(e["image_src"])}"', f'alt="{E(e.get("image_alt") or "")}"']
        if e.get('image_loading'):
            attrs.append(f'loading="{E(e["image_loading"])}"')
        if e.get('image_onerror'):
            attrs.append(f'onerror="{E(e["image_onerror"], quote=True)}"')
        if e.get('image_style'):
            attrs.append(f'style="{E(e["image_style"])}"')
        preview = ph + '\n<img ' + ' '.join(attrs) + '>'
    else:
        preview = ph

    tags = ''.join(
        '<span style="font-family:var(--font-mono);font-size:.65rem;color:var(--text-dim);'
        'background:var(--bg-elevated);border:1px solid var(--border);padding:.2rem .45rem;'
        f'border-radius:3px">{E(t)}</span>' for t in e['tags'])

    rel = e.get('rel') or 'noopener'
    if e.get('affiliate'):
        rel = 'noopener sponsored nofollow'

    return f'''      <a href="{E(e['url'])}" target="_blank" rel="{rel}" style="background:var(--bg-card);padding:1.4rem;display:flex;flex-direction:column;gap:.65rem;text-decoration:none;transition:background .15s" onmouseover="this.style.background='var(--bg-elevated)'" onmouseout="this.style.background='var(--bg-card)'">
        <div style="{E(e.get('preview_style') or 'width:100%;height:0;padding-bottom:37%;background:var(--bg-elevated);border-radius:6px;overflow:hidden;margin-bottom:-.1rem;position:relative')}">
{preview}
        </div>
        <div style="display:flex;align-items:center;justify-content:space-between;gap:.5rem">
          <div style="display:flex;align-items:center;gap:.6rem">
            <div style="{E(e.get('badge_style') or "width:32px;height:32px;border-radius:7px;background:rgba(180,100,255,.15);display:grid;place-items:center;font-family:var(--font-mono);font-size:.55rem;font-weight:700;color:var(--accent);flex-shrink:0")}">{E(e['badge_initials'])}</div>
            <div>
              <div style="font-size:1.05rem;font-weight:600;color:var(--text);line-height:1.25">{E(e['name'])}</div>
              <div style="font-family:var(--font-mono);font-size:.72rem;color:var(--text-dim);margin-top:.1rem">{E(e['vendor'])}</div>
            </div>
          </div>
          <span style="{E(e.get('price_style') or f"font-family:var(--font-mono);font-size:.65rem;font-weight:700;padding:.25rem .55rem;border-radius:3px;background:{bg};color:{fg};white-space:nowrap;flex-shrink:0")}">{E(e['price_tier'])}</span>
        </div>
        <p style="font-size:.95rem;color:var(--text-muted);line-height:1.65">{E(e['blurb'])}</p>
        <div style="display:flex;gap:.4rem;flex-wrap:wrap">{tags}</div>
        <div style="{E(e.get('cta_style') or f"font-family:var(--font-mono);font-size:.75rem;color:{e.get('cta_color') or 'var(--accent)'};margin-top:.3rem")}">{E(e['cta_label'])}</div>
      </a>'''


def category_page(slug):
    c = DATA['categories'][slug]
    entries = sorted((e for e in DATA['entries'] if e['category'] == slug),
                     key=lambda e: e['position'])
    h = c['head']
    out = [head(h['title'], h['description'], h['canonical'])]

    pills = ''.join(
        '<span style="font-family:var(--font-mono);font-size:.6rem;font-weight:700;'
        f'padding:.25rem .6rem;border-radius:3px;background:{p["bg"]};color:{p["fg"]}">{E(p["text"])}</span>'
        for p in c['hero_pills'])

    out.append(f'''<main><div class="page-wrap">
    <div style="padding:3rem 0 2.5rem;border-bottom:1px solid var(--border);max-width:780px">
      <div style="font-family:var(--font-mono);font-size:.65rem;font-weight:700;color:var(--accent);letter-spacing:.1em;text-transform:uppercase;margin-bottom:.75rem;display:flex;align-items:center;gap:.5rem"><span style="display:block;width:20px;height:2px;background:var(--accent)"></span>{E(c['eyebrow'])}</div>
      <h1 style="font-family:var(--font-mono);font-size:clamp(1.6rem,3vw,2.4rem);font-weight:700;line-height:1.15;letter-spacing:-0.025em;margin-bottom:1rem">{E(c['h1_main'])}<br><span style="color:var(--accent)">{E(c['h1_accent'])}</span></h1>
      <p style="color:var(--text-muted);font-size:1.05rem;line-height:1.8;max-width:640px;margin-bottom:1.5rem">{E(c['intro'])}</p>
      <div style="display:flex;gap:.5rem;flex-wrap:wrap">{pills}</div>
    </div>''')

    # First prose section sits above the grid; the rest sit below it.
    secs = c['sections']
    above, below = (secs[:1], secs[1:]) if secs else ([], [])

    for s in above:
        paras = ''.join(
            '<p style="color:var(--text-muted);font-size:1.05rem;line-height:1.8'
            + (f';margin-bottom:{p["mb"]}' if p.get('mb') else '')
            + f'">{p["html"]}</p>' for p in s['paragraphs'])
        out.append(f'''    <div style="padding:2rem 0 1rem;max-width:100%">
      <h2 style="font-family:var(--font-mono);font-size:1.15rem;font-weight:700;color:var(--text);margin-bottom:.65rem;padding-left:.8rem;border-left:3px solid var(--accent);letter-spacing:-0.01em">{E(s['heading'])}</h2>
      {paras}
    </div>''')

    # Count label is derived, never hand-written — it can't drift from the catalog.
    n = len(entries)
    label = re.sub(r'^\d+', str(n), c['count_label']) if c['count_label'] else f'{n} Templates'
    out.append(f'''    <div style="font-family:var(--font-mono);font-size:.65rem;font-weight:700;color:var(--text-dim);text-transform:uppercase;letter-spacing:.1em;padding:.5rem 0 1rem;border-bottom:1px solid var(--border);margin-bottom:1.5rem">{E(label)}</div>''')

    out.append('    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1px;background:var(--border);border:1px solid var(--border);border-radius:var(--radius-lg);overflow:hidden;margin-bottom:3rem">')
    out.extend(card(e) for e in entries)
    out.append('    </div>')

    if below or c['footer_ctas']:
        out.append('    <div style="max-width:100%;padding-bottom:4rem">')
        for s in below:
            out.append(f'      <h2 style="font-family:var(--font-mono);font-size:{s["h_size"]};font-weight:700;color:var(--text);{s["h_margin"]};padding-left:.8rem;border-left:3px solid var(--accent);letter-spacing:-0.01em">{E(s["heading"])}</h2>')
            for p in s['paragraphs']:
                mb = f';margin-bottom:{p["mb"]}' if p.get('mb') else ''
                out.append(f'      <p style="color:var(--text-muted);font-size:1.05rem;line-height:1.8{mb}">{p["html"]}</p>')
        if c['footer_ctas']:
            out.append('      <div style="display:flex;gap:1rem;flex-wrap:wrap">')
            for i, cta in enumerate(c['footer_ctas']):
                extra = '' if i == 0 else ';background:var(--bg-elevated);color:var(--text);box-shadow:none;border:1px solid var(--border)'
                out.append(f'        <a href="{E(cta["url"])}" class="affiliate-cta" target="_blank" rel="noopener sponsored nofollow" style="font-size:.65rem;padding:.45rem .9rem{extra}">{E(cta["label"])}</a>')
            out.append('      </div>')
        out.append('    </div>')

    out.append('  </div></main>\n</body>\n</html>')
    return '\n'.join(out)


def sitemap(pages):
    today = datetime.date.today().isoformat()
    urls = ''.join(
        f'  <url>\n    <loc>{E(u)}</loc>\n    <lastmod>{today}</lastmod>\n  </url>\n'
        for u in pages)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f'{urls}</urlset>\n')


def robots():
    return (f'User-agent: *\nAllow: /\n\n'
            f'Sitemap: {SITE}/sitemap.xml\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(HERE, 'out'))
    a = ap.parse_args()

    written = []
    for slug in DATA['categories']:
        d = os.path.join(a.out, 'marketing-dashboards', slug)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(category_page(slug))
        written.append(slug)
    print(f'wrote {len(written)} category pages')

    tools = DATA['reporting_tools']
    os.makedirs(os.path.join(a.out, 'reporting-tools'), exist_ok=True)
    open(os.path.join(a.out, 'reporting-tools', 'index.html'), 'w', encoding='utf-8').write(
        head(hub.TITLE, hub.DESC, f'{SITE}/reporting-tools/', hub.schema(SITE, tools))
        + hub.body(tools))
    print('wrote /reporting-tools/ hub (was a 404)')

    # Sitemap URLs all derive from the catalog, so it cannot drift from the site.
    urls = ([SITE + p for p in DATA['static_pages']]
            + [f'{SITE}/marketing-dashboards/{s}/' for s in DATA['categories']]
            + [f'{SITE}/reporting-tools/{t["slug"]}/' for t in tools]
            + [SITE + p for p in DATA['blog_posts']])
    seen, ordered = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u); ordered.append(u)
    open(os.path.join(a.out, 'sitemap.xml'), 'w', encoding='utf-8').write(sitemap(ordered))
    open(os.path.join(a.out, 'robots.txt'), 'w', encoding='utf-8').write(robots())
    print(f'wrote sitemap.xml ({len(ordered)} urls) and robots.txt')
    print(f'-> {a.out}')


if __name__ == '__main__':
    main()
