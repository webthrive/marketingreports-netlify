"""The /reporting-tools/ hub page.

This URL is in the site-wide nav on every page but had no index file, so it
returned 404. Content comes from the catalog's `reporting_tools` list.
"""
import html

E = html.escape
ARROW = '→'


def card(t):
    return (
        f'      <a href="/reporting-tools/{t["slug"]}/" style="background:var(--bg-card);'
        'padding:1.6rem;display:flex;flex-direction:column;gap:.7rem;text-decoration:none;'
        'transition:background .15s" '
        'onmouseover="this.style.background=\'var(--bg-elevated)\'" '
        'onmouseout="this.style.background=\'var(--bg-card)\'">\n'
        '        <div style="display:flex;align-items:center;justify-content:space-between;gap:.5rem">\n'
        '          <div style="display:flex;align-items:center;gap:.7rem">\n'
        f'            <div style="width:38px;height:38px;border-radius:8px;background:{t["bg"]};'
        'display:grid;place-items:center;font-family:var(--font-mono);font-size:.7rem;'
        f'font-weight:700;color:{t["color"]};flex-shrink:0">{E(t["badge"])}</div>\n'
        '            <div>\n'
        '              <div style="font-size:1.15rem;font-weight:600;color:var(--text);'
        f'line-height:1.2">{E(t["name"])}</div>\n'
        '              <div style="font-family:var(--font-mono);font-size:.72rem;'
        f'color:var(--text-dim);margin-top:.15rem">{E(t["tagline"])}</div>\n'
        '            </div>\n'
        '          </div>\n'
        '          <span style="font-family:var(--font-mono);font-size:.65rem;font-weight:700;'
        'padding:.25rem .55rem;border-radius:3px;background:var(--bg-elevated);'
        f'color:var(--text-muted);white-space:nowrap;flex-shrink:0">{E(t["price"])}</span>\n'
        '        </div>\n'
        '        <p style="font-size:.95rem;color:var(--text-muted);line-height:1.65;'
        f'margin:0">{E(t["verdict"])}</p>\n'
        '        <div style="font-family:var(--font-mono);font-size:.75rem;color:var(--accent);'
        f'margin-top:.2rem">Read the review {ARROW}</div>\n'
        '      </a>'
    )


TITLE = 'Marketing Reporting Tools Reviewed 2026 | MarketingReports.io'
DESC = ('Hands-on reviews of the main marketing reporting platforms — Databox, Whatagraph, '
        'Supermetrics, Looker Studio and Klipfolio — what each is good at and who it suits.')


def schema(site, tools):
    return {
        "@context": "https://schema.org", "@type": "CollectionPage",
        "name": TITLE, "description": DESC, "url": f"{site}/reporting-tools/",
        "publisher": {"@type": "Organization", "name": "MarketingReports.io", "url": site},
        "hasPart": [{"@type": "Review", "name": f"{t['name']} Review 2026",
                     "url": f"{site}/reporting-tools/{t['slug']}/",
                     "itemReviewed": {"@type": "SoftwareApplication", "name": t['name']}}
                    for t in tools],
    }


def body(tools):
    cards = '\n'.join(card(t) for t in tools)
    return (
        '<main><div class="page-wrap">\n'
        '    <div style="padding:3rem 0 2.5rem;border-bottom:1px solid var(--border);max-width:780px">\n'
        '      <div style="font-family:var(--font-mono);font-size:.65rem;font-weight:700;'
        'color:var(--accent);letter-spacing:.1em;text-transform:uppercase;margin-bottom:.75rem;'
        'display:flex;align-items:center;gap:.5rem"><span style="display:block;width:20px;'
        'height:2px;background:var(--accent)"></span>Reporting Tools</div>\n'
        '      <h1 style="font-family:var(--font-mono);font-size:clamp(1.6rem,3vw,2.4rem);'
        'font-weight:700;line-height:1.15;letter-spacing:-0.025em;margin-bottom:1rem">'
        'Marketing Reporting Tools<br><span style="color:var(--accent)">Reviewed in 2026</span></h1>\n'
        '      <p style="color:var(--text-muted);font-size:1.05rem;line-height:1.8;max-width:640px;'
        'margin-bottom:1.5rem">Five platforms most marketing teams end up choosing between. '
        'Each review covers what the tool is genuinely good at, where the pricing bites, and the '
        'kind of team it actually suits — written from hands-on use rather than a feature matrix.</p>\n'
        '    </div>\n'
        '    <div style="font-family:var(--font-mono);font-size:.65rem;font-weight:700;'
        'color:var(--text-dim);text-transform:uppercase;letter-spacing:.1em;padding:.5rem 0 1rem;'
        f'border-bottom:1px solid var(--border);margin-bottom:1.5rem">{len(tools)} Tools Reviewed</div>\n'
        '    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));'
        'gap:1px;background:var(--border);border:1px solid var(--border);'
        'border-radius:var(--radius-lg);overflow:hidden;margin-bottom:3rem">\n'
        f'{cards}\n'
        '    </div>\n'
        '    <div style="max-width:100%;padding-bottom:4rem">\n'
        '      <h2 style="font-family:var(--font-mono);font-size:1.15rem;font-weight:700;'
        'color:var(--text);margin-bottom:.65rem;padding-left:.8rem;border-left:3px solid var(--accent);'
        'letter-spacing:-0.01em">Looking for Free Templates Instead?</h2>\n'
        '      <p style="color:var(--text-muted);font-size:1.05rem;line-height:1.8;margin-bottom:1rem">'
        'If you are not ready to pay for a reporting platform, the '
        '<a href="/marketing-dashboards/" style="color:var(--accent)">marketing dashboards directory</a> '
        'collects free and paid templates by platform — Google Ads, Meta, LinkedIn, Shopify, '
        'Search Console and more.</p>\n'
        '    </div>\n'
        '  </div></main>\n</body>\n</html>'
    )
