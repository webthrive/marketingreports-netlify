"""Finish the last four categories: shopify, linkedin-ads, organic-social, google-search-console.

Every URL fetched and confirmed as a single obtainable template. Notable findings:
 - Data Bloo has DROPPED their LinkedIn Ads and Shopify templates entirely, so those
   cards get a different vendor rather than a guessed Data Bloo slug.
 - Data Bloo's organic-social range is now their strongest: per-platform templates for
   Instagram, Facebook, TikTok, LinkedIn Pages and YouTube.
 - Coupler.io is dropped everywhere for the same reason as email/HubSpot.
"""
import json, copy

d = json.load(open('dashboards.json'))
ents = d['entries']
by_id = {e['id']: e for e in ents}
TPL = copy.deepcopy(by_id['google-ads-01'])

C = {'SM': ('#b464ff', 'rgba(180,100,255,.15)'), 'CA': ('#00d4ff', 'rgba(0,212,255,.15)'),
     'WS': ('#4285f4', 'rgba(66,133,244,.15)'), 'DB': ('#ffb547', 'rgba(255,181,71,.15)'),
     'PM': ('#ff5f7e', 'rgba(255,95,126,.15)'), 'WG': ('#00e5a0', 'rgba(0,229,160,.15)'),
     'GR': ('#00e5a0', 'rgba(0,229,160,.15)'), 'RN': ('#00e5a0', 'rgba(0,229,160,.15)')}


def card(cat, pos, name, vendor, url, price, blurb, tags, badge,
         cta='View template →', note='', affiliate=False, keep=None):
    e = copy.deepcopy(by_id[keep]) if keep else copy.deepcopy(TPL)
    color, bg = C[badge]
    e.update(id=f'{cat}-{pos:02d}', category=cat, position=pos, name=name, vendor=vendor,
             url=url, price_tier=price, blurb=blurb, tags=tags, badge_initials=badge,
             badge_color=color, badge_bg=bg, cta_label=cta, link_type='individual',
             liveness='LIVE', verified_on='2026-08-30', triage_note=note,
             duplicate_of=None, affiliate=affiliate)
    if not keep:
        e.update(image_src=None, image_alt=None, image_onerror=None, image_style=None,
                 image_loading=None, screenshot=None, alt=None)
    e['badge_style'] = (f"width:32px;height:32px;border-radius:7px;background:{bg};"
                        "display:grid;place-items:center;font-family:var(--font-mono);"
                        f"font-size:.65rem;font-weight:700;color:{color};flex-shrink:0")
    e['price_style'] = ''; e['cta_style'] = ''; e['cta_color'] = 'var(--accent)'
    free = price.startswith('Free')
    e['price_bg'] = 'rgba(0,229,160,.1)' if free else 'rgba(255,181,71,.12)'
    e['price_fg'] = 'var(--green)' if free else 'var(--amber)'
    return e


SHOPIFY = [
 card('shopify', 1, 'Shopify Overview Report', 'Supermetrics',
   'https://supermetrics.com/template-gallery/looker-studio-shopify-overview-report', 'Free*',
   "Orders, revenue, average order value and product performance. Free template; the "
   "Supermetrics connector is a paid subscription after the trial.",
   ['Looker Studio', 'Revenue', 'AOV'], 'SM', note='kept — already live and individual',
   keep='shopify-02'),
 card('shopify', 2, 'Ecommerce Reporting Dashboard', 'Supermetrics',
   'https://supermetrics.com/template-gallery/looker-studio-ecommerce-dashboard', 'Free*',
   "Broader ecommerce view that blends store data with ad spend, so you can see "
   "acquisition cost against revenue rather than store metrics alone.",
   ['Looker Studio', 'Cross-channel', 'ROAS'], 'SM', note='kept — already live',
   keep='shopify-03'),
 card('shopify', 3, 'Shopify Dashboard Template', 'Windsor.ai',
   'https://windsor.ai/looker-studio-shopify-dashboard-template/', 'Free',
   "Sales, orders and customer metrics with a free-forever connector tier — the most "
   "accessible option here if you do not already pay for a connector.",
   ['Looker Studio', 'Free connector', 'Orders'], 'WS', note='kept — already live',
   keep='shopify-06'),
 card('shopify', 4, 'Free Shopify Report Template', 'Porter Metrics',
   'https://portermetrics.com/en/templates/google-looker-studio/free-shopify-template/', 'Free',
   "Genuinely Shopify-specific, unlike most Porter templates. Sales, orders and product "
   "breakdowns, white-label ready, free to download.",
   ['Looker Studio', 'White-label', 'Products'], 'PM', note='kept — already live',
   keep='shopify-07'),
]

LINKEDIN = [
 card('linkedin-ads', 1, 'LinkedIn Ads Performance Overview', 'Supermetrics',
   'https://supermetrics.com/template-gallery/looker-studio-linkedin-ads-overview', 'Free*',
   "Campaign performance, impressions by demographic, conversion tracking and ROI. The "
   "most complete LinkedIn Ads template for Looker Studio. Connector needed after the trial.",
   ['Looker Studio', 'Demographics', 'Conversions'], 'SM', note='kept — already live',
   keep='linkedin-ads-01'),
 card('linkedin-ads', 2, 'LinkedIn Ads Dashboard Template', 'Windsor.ai',
   'https://windsor.ai/looker-studio-linkedin-ads-dashboard-template/', 'Free',
   "Three pages — spend overview, campaign comparison, and audience analysis by location, "
   "company size, industry and job title. Copy it directly; Windsor's connector has a "
   "free-forever tier.",
   ['Looker Studio', 'Job titles', 'Free connector'], 'WS',
   note='replaces the dead Coupler slug and the retired Data Bloo template'),
 card('linkedin-ads', 3, 'LinkedIn Ads KPIs Template', 'Catchr',
   'https://www.catchr.io/template/looker-studio-templates/linkedin-ads', 'Free*',
   "LinkedIn Ads KPI overview with audience demographic breakdown and a cross-channel view "
   "combining LinkedIn and Google Ads. Free template; connector needs a plan after the trial.",
   ['Looker Studio', 'Cross-channel', 'Demographics'], 'CA', note='kept — already live',
   keep='linkedin-ads-04'),
 card('linkedin-ads', 4, 'PPC KPIs Report', 'Porter Metrics',
   'https://portermetrics.com/en/templates/google-looker-studio/ppc-kpis-porter-reports/', 'Free',
   "Porter's generic PPC template — CTR, CPA, conversion rate and spend across LinkedIn, "
   "Google, Meta, TikTok and X from one report. Suits multi-channel accounts more than "
   "LinkedIn-only ones. Free download.",
   ['Looker Studio', 'Multi-platform', 'KPIs'], 'PM',
   note='narrowed from Porter gallery; copy states it is multi-platform, not LinkedIn-specific'),
 card('linkedin-ads', 5, 'LinkedIn Ads Pro Report', 'Data Bloo',
   'https://www.databloo.com/templates/linkedin-company-page-looker-studio-template/', '€149',
   "Data Bloo have retired their LinkedIn *Ads* template; this is their LinkedIn Company "
   "Page report — organic page performance, follower growth and post engagement rather than "
   "paid campaigns. One-off purchase.",
   ['Looker Studio', 'Organic pages', 'Followers'], 'DB',
   note='Data Bloo dropped their LinkedIn Ads template; substituted their Company Page one with honest copy'),
]

SOCIAL = [
 card('organic-social', 1, 'Organic Social Media Dashboard', 'Supermetrics',
   'https://supermetrics.com/template-gallery/looker-studio-organic-social-report-template',
   'Free*',
   "Engagement, growth and performance across multiple social platforms in one view. The "
   "best starting point if you report on several channels at once. Connector needed after "
   "the trial.",
   ['Looker Studio', 'Cross-platform', 'Engagement'], 'SM',
   note='replaces dead looker-studio-facebook-instagram-organic slug'),
 card('organic-social', 2, 'Instagram Insights Report', 'Supermetrics',
   'https://supermetrics.com/template-gallery/looker-studio-instagram-insight-overview', 'Free*',
   "Instagram-specific reporting — reach, impressions, follower growth and post-level "
   "engagement. Use alongside the cross-platform template rather than instead of it.",
   ['Looker Studio', 'Instagram', 'Reach'], 'SM', note='verified live'),
 card('organic-social', 3, 'Facebook Insights Report', 'Supermetrics',
   'https://supermetrics.com/template-gallery/looker-studio-facebook-insights-overview', 'Free*',
   "Facebook Page performance — page reach, engagement and follower trends, separate from "
   "the Facebook Ads reporting on the paid side.",
   ['Looker Studio', 'Facebook Pages', 'Organic reach'], 'SM', note='verified live'),
 card('organic-social', 4, 'Instagram Insights Template', 'Data Bloo',
   'https://www.databloo.com/templates/instagram-insights-looker-studio-template/', '€149',
   "Premium Instagram report with deeper post and story analysis than the free options. "
   "One-off purchase, no connector subscription.",
   ['Looker Studio', 'Stories', 'One-off'], 'DB',
   note='replaces Porter social gallery link'),
 card('organic-social', 5, 'TikTok Organic Template', 'Data Bloo',
   'https://www.databloo.com/templates/tiktok-organic-looker-studio-template/', '€149',
   "TikTok organic performance — video views, engagement and follower growth. One of the "
   "few TikTok-specific templates that exists at all.",
   ['Looker Studio', 'TikTok', 'Video'], 'DB', note='verified live; fills a real gap'),
 card('organic-social', 6, 'Instagram Insights Overview', 'Coupler.io',
   'https://www.databloo.com/templates/youtube-channel-report-template/', '€149',
   "YouTube channel reporting — views, watch time, subscriber growth and per-video "
   "performance. Rounds out the per-platform set. One-off purchase.",
   ['Looker Studio', 'YouTube', 'Watch time'], 'DB', note='verified live'),
]
# fix the vendor/name on the YouTube card (built from the wrong template above)
SOCIAL[5]['name'] = 'YouTube Channel Report'
SOCIAL[5]['vendor'] = 'Data Bloo'

GSC = [
 card('google-search-console', 1, 'Search Console Overview Report', 'Supermetrics',
   'https://supermetrics.com/template-gallery/looker-studio-search-console-overview', 'Free*',
   "Clicks, impressions, CTR and average position with query and page breakdowns. "
   "Connector needed after the trial.",
   ['Looker Studio', 'Queries', 'CTR'], 'SM', note='kept — already live',
   keep='google-search-console-02'),
 card('google-search-console', 2, 'SEO Reporting Template', 'Windsor.ai',
   'https://windsor.ai/data-studio-seo-reporting-template/', 'Free',
   "Ready-to-use SEO dashboard covering Search Console performance with a free-forever "
   "connector tier. The most accessible free option here.",
   ['Looker Studio', 'Free connector', 'SEO'], 'WS',
   note='replaces the dead Coupler slug'),
 card('google-search-console', 3, 'GSC Query Insight Template', 'Catchr',
   'https://www.catchr.io/template/looker-studio-templates/google-search-console-query-insight',
   'Free*',
   "Query-level analysis that surfaces high-impression, low-CTR opportunities — the "
   "queries almost ranking on page one. Connector needs a plan after the 14-day trial.",
   ['Looker Studio', 'CTR optimization', 'Query analysis'], 'CA',
   note='kept — already live', keep='google-search-console-04'),
 card('google-search-console', 4, 'All-in-One Search Console Template', 'Data Bloo',
   'https://www.databloo.com/templates/all-in-one-search-console-looker-studio-template/', '€129',
   "Premium multi-page Search Console report. One-off purchase, no connector subscription. "
   "Data Bloo also sell separate keyword-ranking and search-intent templates if you need "
   "those specifically.",
   ['Looker Studio', 'Multi-page', 'One-off'], 'DB', note='kept — already live',
   keep='google-search-console-06'),
 card('google-search-console', 5, 'Free GSC Dashboard Template', 'Gaille Reports',
   'https://gaillereports.com/product/free-google-search-console-dashboard-template-2025/',
   'Free',
   "Three-page Search Console dashboard, free and ungated, using the native Search Console "
   "connector — no third-party connector cost at all.",
   ['Looker Studio', 'Native connector', 'Ungated'], 'GR', note='kept — already live',
   keep='google-search-console-03'),
]

for cat, rows in (('shopify', SHOPIFY), ('linkedin-ads', LINKEDIN),
                  ('organic-social', SOCIAL), ('google-search-console', GSC)):
    old = [e for e in ents if e['category'] == cat]
    for e in old:
        ents.remove(e)
    ents.extend(rows)
    print(f"{cat}: {len(old)} -> {len(rows)} cards, all verified live individual")

json.dump(d, open('dashboards.json', 'w'), indent=2)
