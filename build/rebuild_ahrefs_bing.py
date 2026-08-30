"""Rebuild ahrefs and bing-ads. Both were 5/5 dead — nothing salvageable.

Every URL below was fetched and confirmed live. The four Ahrefs templates are
the official ones, confirmed against Ahrefs' own developer docs, and the
Advanced-plan requirement is quoted from their help centre rather than assumed.
"""
import json, copy

d = json.load(open('dashboards.json'))
ents = d['entries']
by_id = {e['id']: e for e in ents}
TPL = copy.deepcopy(by_id['google-ads-01'])   # shape donor


def card(cat, pos, name, vendor, url, price, blurb, tags, badge, color, bg,
         cta='View template →', note='', affiliate=False):
    e = copy.deepcopy(TPL)
    e.update(id=f'{cat}-{pos:02d}', category=cat, position=pos, name=name,
             vendor=vendor, url=url, price_tier=price, blurb=blurb, tags=tags,
             badge_initials=badge, badge_color=color, badge_bg=bg,
             cta_label=cta, link_type='individual', liveness='LIVE',
             verified_on='2026-08-30', triage_note=note, duplicate_of=None,
             image_src=None, image_alt=None, image_onerror=None,
             image_style=None, image_loading=None, screenshot=None, alt=None,
             affiliate=affiliate)
    e['badge_style'] = (f"width:32px;height:32px;border-radius:7px;background:{bg};"
                        f"display:grid;place-items:center;font-family:var(--font-mono);"
                        f"font-size:.65rem;font-weight:700;color:{color};flex-shrink:0")
    e['price_style'] = ''
    e['cta_style'] = ''
    e['price_bg'] = {'Free': 'rgba(0,229,160,.1)', 'Free*': 'rgba(0,229,160,.1)'}.get(
        price, 'rgba(255,181,71,.12)')
    e['price_fg'] = {'Free': 'var(--green)', 'Free*': 'var(--green)'}.get(price, 'var(--amber)')
    e['cta_color'] = 'var(--accent)'
    return e


AH = '#f60'; AHBG = 'rgba(255,102,0,.15)'
AHREFS = [
 card('ahrefs', 1, 'Ahrefs Rank Tracker Report', 'Ahrefs (official)',
   'https://datastudio.google.com/reporting/60e07a66-84cc-4992-b212-94bdf02851aa', 'Free*',
   "Ahrefs' own Rank Tracker template — keyword positions, visibility and movement over "
   "time. Free to copy; needs an Ahrefs Advanced plan or higher for the connector. "
   "Consumes no Ahrefs credits.",
   ['Looker Studio', 'Rank tracking', 'Official'], 'AH', AH, AHBG, 'Open template →',
   'official Ahrefs template, confirmed against docs.ahrefs.com'),
 card('ahrefs', 2, 'Ahrefs Site Explorer Report', 'Ahrefs (official)',
   'https://datastudio.google.com/reporting/54258fc6-9ef0-4718-98df-1a4c4aa87ece', 'Free*',
   "Backlinks, referring domains, domain rating and organic keyword overlap, straight from "
   "Ahrefs. Advanced plan or higher required. Note this one does consume Ahrefs credits — "
   "roughly one per chart load.",
   ['Looker Studio', 'Backlinks', 'Official'], 'AH', AH, AHBG, 'Open template →',
   'official Ahrefs template; credit cost quoted from Ahrefs help centre'),
 card('ahrefs', 3, 'Ahrefs Site Audit Report', 'Ahrefs (official)',
   'https://datastudio.google.com/reporting/5a10fad2-a23e-41f3-bd71-40ab5ce01e21', 'Free*',
   "Technical SEO reporting — health score, crawl errors and issue breakdowns. Advanced "
   "plan or higher; consumes no Ahrefs credits.",
   ['Looker Studio', 'Technical SEO', 'Official'], 'AH', AH, AHBG, 'Open template →',
   'official Ahrefs template'),
 card('ahrefs', 4, 'Ahrefs Brand Radar Report', 'Ahrefs (official)',
   'https://datastudio.google.com/reporting/0f9f33b8-51e0-4086-a6e7-c024f38a6219', 'Free*',
   "Brand visibility tracking across search and AI answers. The newest of Ahrefs' four "
   "official Looker Studio templates. Advanced plan or higher.",
   ['Looker Studio', 'Brand visibility', 'Official'], 'AH', AH, AHBG, 'Open template →',
   'official Ahrefs template'),
 card('ahrefs', 5, 'Ahrefs Report Template', 'Whatagraph',
   'https://whatagraph.com/templates/ahrefs-report?fpr=marketingreports', 'Free trial',
   "Whatagraph's plug-and-play Ahrefs report — domain rating, Ahrefs Rank, organic "
   "keywords, backlinks and referring domains. Runs inside Whatagraph rather than Looker "
   "Studio, so it needs a Whatagraph subscription after the trial.",
   ['Whatagraph', 'Client reporting', 'White-label'], 'WG', '#00d4ff',
   'rgba(0,212,255,.15)', 'View template →', 'verified live', affiliate=True),
 card('ahrefs', 6, 'Ahrefs Looker Studio Template', 'Data Bloo',
   'https://www.databloo.com/templates/ahrefs-looker-studio-template/', '€149',
   "Eight-section premium Ahrefs report covering rankings, backlinks, domain rating and "
   "technical SEO. One-off purchase; still needs Ahrefs' own connectors, so an Advanced "
   "plan on top.",
   ['Looker Studio', 'Multi-section', 'Agency'], 'DB', '#ffb547',
   'rgba(255,181,71,.15)', 'View template →', 'verified live'),
]

MS = '#00a4ef'; MSBG = 'rgba(0,164,239,.15)'
BING = [
 card('bing-ads', 1, 'Microsoft Ads Dashboard', 'Catchr',
   'https://www.catchr.io/template/looker-studio-templates/microsoft-ads', 'Free*',
   "Impressions, clicks, CTR, spend, average CPC and conversions, with campaign, keyword "
   "and audience segment views. Free template; the Catchr connector needs a subscription "
   "after the 14-day trial.",
   ['Looker Studio', 'Campaigns', 'Keywords'], 'CA', '#b464ff',
   'rgba(180,100,255,.15)', 'View template →',
   'replaces dead /microsoft-bing-ads slug — Catchr renamed it'),
 card('bing-ads', 2, 'Microsoft Advertising Report', 'Reporting Ninja',
   'https://www.reportingninja.com/looker-studio-templates/microsoft-advertising-report-template',
   'Free*',
   "Impressions, clicks, conversions, cost and ROAS with demographic, device and "
   "time-of-day breakdowns. Free template; live data needs a Reporting Ninja account "
   "(15-day trial).",
   ['Looker Studio', 'ROAS', 'Demographics'], 'RN', '#00e5a0',
   'rgba(0,229,160,.15)', 'View template →', 'verified live'),
 card('bing-ads', 3, 'Microsoft Bing Ads Dashboard', 'Dashboard Design Lab',
   'https://dashboarddesignlab.com/product/microsoft-bing-ads-looker-studio-dashboard-template-supermetrics/',
   'Free',
   "Free Looker Studio dashboard covering impressions, CTR, top campaigns, CPM and device "
   "breakdown. Built for the Supermetrics Microsoft Ads connector.",
   ['Looker Studio', 'Device split', 'Supermetrics'], 'DL', '#4285f4',
   'rgba(66,133,244,.15)', 'View template →', 'verified live'),
 card('bing-ads', 4, 'Bing Ads Campaign Performance Report', 'Coefficient',
   'https://coefficient.io/dashboard-examples/bing-ads-campaign-performance-report', 'Free',
   "A Google Sheets report rather than Looker Studio — CPC, CPM, CTR and ad spend by "
   "campaign with daily trends. Useful if your team already works in Sheets.",
   ['Google Sheets', 'Campaigns', 'Daily trends'], 'CO', '#00e5a0',
   'rgba(0,229,160,.15)', 'View template →', 'verified live; Sheets not Looker Studio'),
 card('bing-ads', 5, 'Bing Ads Looker Studio Template', 'Data Bloo',
   'https://www.databloo.com/templates/bing-ads-looker-studio-template/', '€199',
   "Premium multi-page Microsoft Ads report — overview, campaigns, keywords and search "
   "queries, audience and location, plus time trends. One-off purchase.",
   ['Looker Studio', 'Search queries', 'Agency'], 'DB', '#ffb547',
   'rgba(255,181,71,.15)', 'View template →', 'verified live'),
 card('bing-ads', 6, 'Bing Ads Looker Studio Template', 'Powermetrics',
   'https://powermetrics.co.uk/product/bing-ads-looker-studio-template', '£89',
   "Clicks, impressions, CTR, CPC, conversions and quality score with device and geography "
   "splits. One-off purchase with vendor-assisted setup.",
   ['Looker Studio', 'Quality score', 'Geo'], 'PM', '#ff5f7e',
   'rgba(255,95,126,.15)', 'View template →', 'verified live'),
]

for cat, rows in (('ahrefs', AHREFS), ('bing-ads', BING)):
    old = [e for e in ents if e['category'] == cat]
    for e in old:
        ents.remove(e)
    ents.extend(rows)
    print(f"{cat}: replaced {len(old)} dead cards with {len(rows)} verified live ones")

json.dump(d, open('dashboards.json', 'w'), indent=2)
