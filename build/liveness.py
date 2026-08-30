"""Record verified liveness per URL, checked 2026-08-30 via WebFetch."""
import json, collections

DEAD = [
 "https://app.coupler.io/templates/bing-ads-dashboard",
 "https://app.coupler.io/templates/email-marketing-dashboard",
 "https://app.coupler.io/templates/facebook-ads-performance-dashboard",
 "https://app.coupler.io/templates/google-search-console-dashboard",
 "https://app.coupler.io/templates/hubspot-marketing-dashboard",
 "https://app.coupler.io/templates/linkedin-ads-performance-dashboard",
 "https://app.coupler.io/templates/shopify-sales-dashboard",
 "https://app.coupler.io/templates/social-media-dashboard",
 "https://portermetrics.com/en/templates/ahrefs-dashboard/",
 "https://portermetrics.com/en/templates/bing-ads/",
 "https://portermetrics.com/en/templates/seo-agency-dashboard/",
 "https://supermetrics.com/template-gallery/looker-studio-ahrefs",
 "https://supermetrics.com/template-gallery/looker-studio-ahrefs-backlinks",
 "https://supermetrics.com/template-gallery/looker-studio-facebook-instagram-organic",
 "https://supermetrics.com/template-gallery/looker-studio-google-ads-performance-dashboard",
 "https://supermetrics.com/template-gallery/looker-studio-hubspot",
 "https://supermetrics.com/template-gallery/looker-studio-mailchimp",
 "https://supermetrics.com/template-gallery/looker-studio-microsoft-advertising",
 "https://www.catchr.io/template/looker-studio-templates/hubspot",
 "https://www.catchr.io/template/looker-studio-templates/mailchimp",
 "https://www.catchr.io/template/looker-studio-templates/microsoft-bing-ads",
 "https://www.databloo.com/report-templates/hubspot/",
 "https://www.databloo.com/report-templates/linkedin-ads/",
 "https://www.reportingninja.com/looker-studio-templates/google-ads-dashboard/",
 "https://www.dataslayer.ai/blog/google-ads-dashboard-template",
 "https://www.dataslayer.ai/blog/bing-ads-dashboard-template",
 "https://coupler.io/blog/ahrefs-google-sheets-integration/",
]
GALLERY = [
 "https://portermetrics.com/en/templates/email-marketing/",
 "https://portermetrics.com/en/templates/hubspot/",
 "https://portermetrics.com/en/templates/linkedin-ads/",
 "https://portermetrics.com/en/templates/social-media/",
 "https://portermetrics.com/en/templates/google-ads/",
 "https://portermetrics.com/en/templates/facebook-ads/",
 "https://radyant.io/tools/free-google-ads-looker-studio-templates/",
 "https://www.databloo.com/report-templates/facebook-ads/",
 "https://www.databloo.com/report-templates/google-ads/",
]
OTHER = {"https://portermetrics.com/en/templates/google-search-console/":
         "no longer a template page - now a Claude MCP connector page"}

# Replacements confirmed live.
REPLACE = {
 "https://supermetrics.com/template-gallery/looker-studio-google-ads-performance-dashboard":
   "https://supermetrics.com/template-gallery/looker-studio-google-ads",
}

d = json.load(open('dashboards.json'))
for e in d['entries']:
    u = e['url']
    if u in DEAD:
        e['liveness'] = 'DEAD'; e['link_type'] = 'dead'
    elif u in OTHER:
        e['liveness'] = 'MOVED'; e['link_type'] = 'moved'; e['triage_note'] = OTHER[u]
    elif u in GALLERY:
        e['liveness'] = 'LIVE'; e['link_type'] = 'gallery'
    else:
        e['liveness'] = 'LIVE'
    e['verified_on'] = '2026-08-30'
    if u in REPLACE:
        e['replacement_url'] = REPLACE[u]
json.dump(d, open('dashboards.json', 'w'), indent=2)

E = d['entries']
print("=== CARD-LEVEL IMPACT (60 cards) ===")
for k, v in collections.Counter(e['link_type'] for e in E).most_common():
    print(f"  {k:12s} {v:3d} cards")
print()
uniq = collections.Counter(e['url'] for e in E)
print(f"unique URLs: {len(uniq)}   dead: {len(DEAD)}   ({100*len(DEAD)/len(uniq):.0f}% of destinations)")
print(f"cards pointing at a dead URL: {sum(1 for e in E if e['liveness']=='DEAD')} of 60")
print()
print("=== DEAD BY CATEGORY ===")
bycat = collections.defaultdict(lambda: [0, 0])
for e in E:
    bycat[e['category']][1] += 1
    if e['liveness'] == 'DEAD':
        bycat[e['category']][0] += 1
for c in sorted(bycat, key=lambda c: -bycat[c][0] / bycat[c][1]):
    dead, tot = bycat[c]
    bar = '#' * dead + '.' * (tot - dead)
    print(f"  {c:24s} {dead}/{tot}  {bar}")
print()
print("=== WHAT ACTUALLY WORKS ===")
good = [e for e in E if e['liveness'] == 'LIVE' and e['link_type'] == 'individual']
print(f"  live + individual dashboard cards: {len(good)}")
print(f"  unique destinations among them:    {len(set(e['url'] for e in good))}")
