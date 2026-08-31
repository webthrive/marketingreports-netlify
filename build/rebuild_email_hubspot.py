"""Rebuild email-marketing and hubspot-marketing. Both were 4-of-5 / 4-of-6 dead.

Every URL fetched and confirmed as a single obtainable template.

Coupler.io is deliberately absent from both. Their slug URLs are dead and they no
longer publish an obtainable single template for these platforms — the current
coupler.io/marketing-dashboards/* pages are signup-gated funnels listing several
dashboards, which fails the one-card-one-dashboard rule.
"""
import json, copy

d = json.load(open('dashboards.json'))
ents = d['entries']
by_id = {e['id']: e for e in ents}
TPL = copy.deepcopy(by_id['google-ads-01'])


def card(cat, pos, name, vendor, url, price, blurb, tags, badge, color, bg,
         cta='View template →', note='', affiliate=False):
    e = copy.deepcopy(TPL)
    e.update(id=f'{cat}-{pos:02d}', category=cat, position=pos, name=name,
             vendor=vendor, url=url, price_tier=price, blurb=blurb, tags=tags,
             badge_initials=badge, badge_color=color, badge_bg=bg, cta_label=cta,
             link_type='individual', liveness='LIVE', verified_on='2026-08-30',
             triage_note=note, duplicate_of=None, image_src=None, image_alt=None,
             image_onerror=None, image_style=None, image_loading=None,
             screenshot=None, alt=None, affiliate=affiliate)
    e['badge_style'] = (f"width:32px;height:32px;border-radius:7px;background:{bg};"
                        "display:grid;place-items:center;font-family:var(--font-mono);"
                        f"font-size:.65rem;font-weight:700;color:{color};flex-shrink:0")
    e['price_style'] = ''; e['cta_style'] = ''; e['cta_color'] = 'var(--accent)'
    free = price.startswith('Free')
    e['price_bg'] = 'rgba(0,229,160,.1)' if free else 'rgba(255,181,71,.12)'
    e['price_fg'] = 'var(--green)' if free else 'var(--amber)'
    return e


SM, SMBG = '#b464ff', 'rgba(180,100,255,.15)'
CA, CABG = '#00d4ff', 'rgba(0,212,255,.15)'
WG, WGBG = '#00e5a0', 'rgba(0,229,160,.15)'
WS, WSBG = '#4285f4', 'rgba(66,133,244,.15)'
DB, DBBG = '#ffb547', 'rgba(255,181,71,.15)'
PM, PMBG = '#ff5f7e', 'rgba(255,95,126,.15)'

EMAIL = [
 card('email-marketing', 1, 'Mailchimp Campaign Overview', 'Catchr',
   'https://www.catchr.io/template/looker-studio-templates/template-mailchimp-campaign-overview',
   'Free*',
   "Campaign-level email reporting — sends, opens, clicks, unique clicks, open and click "
   "rate, new subscribers and unsubscribes. Free template; the Catchr connector needs a "
   "subscription after the 14-day trial.",
   ['Looker Studio', 'Mailchimp', 'Campaigns'], 'CA', CA, CABG, 'View template →',
   'replaces dead catchr /mailchimp slug'),
 card('email-marketing', 2, 'Mailchimp Email Campaign Report', 'Supermetrics',
   'https://supermetrics.com/template-gallery/looker-studio-mailchimp-email-campaign-overview',
   'Free*',
   "Open and click rate by campaign, benchmarked against industry averages — useful when "
   "you want context rather than bare numbers. Free template; Supermetrics connector "
   "required after the trial.",
   ['Looker Studio', 'Benchmarks', 'Mailchimp'], 'SM', SM, SMBG, 'View template →',
   'replaces dead looker-studio-mailchimp slug'),
 card('email-marketing', 3, 'Klaviyo Email Report', 'Supermetrics',
   'https://supermetrics.com/template-gallery/looker-studio-klaviyo-email-marketing', 'Free*',
   "Klaviyo campaign performance, list and audience growth, and engagement trends. Built "
   "for ecommerce senders. Free template; connector required after the trial.",
   ['Looker Studio', 'Klaviyo', 'Ecommerce'], 'SM', SM, SMBG, 'View template →',
   'verified live'),
 card('email-marketing', 4, 'Klaviyo Responsive Dashboard', 'Catchr',
   'https://www.catchr.io/template/looker-studio-templates/klaviyo-responsive-dashboard',
   'Free*',
   "Emails received, opens, clicks, spam complaints and bounces alongside open and click "
   "rate. Deliverability gets more attention here than in most Klaviyo templates.",
   ['Looker Studio', 'Deliverability', 'Klaviyo'], 'CA', CA, CABG, 'View template →',
   'verified live'),
 card('email-marketing', 5, 'Klaviyo Looker Studio Dashboard', 'Windsor.ai',
   'https://windsor.ai/klaviyo-looker-studio-dashboard/', 'Free',
   "Delivery, open and click rates with subscriber trends and revenue by campaign — one of "
   "the few free options that ties email back to revenue.",
   ['Looker Studio', 'Revenue', 'Klaviyo'], 'WS', WS, WSBG, 'View template →',
   'verified live'),
 card('email-marketing', 6, 'Klaviyo Dashboard Template', 'Whatagraph',
   'https://whatagraph.com/templates/klaviyo-dashboard?fpr=marketingreports', 'Free trial',
   "Open, click and conversion rate with revenue attribution and deliverability. Runs "
   "inside Whatagraph rather than Looker Studio, so it needs a subscription after the trial.",
   ['Whatagraph', 'Attribution', 'Client reporting'], 'WG', WG, WGBG, 'View template →',
   'verified live', affiliate=True),
 card('email-marketing', 7, 'Mailchimp Looker Studio Template', 'Data Bloo',
   'https://www.databloo.com/templates/mailchimp-looker-studio-template/', '€69',
   "Audience growth and bounce tracking plus campaign delivery, open, click and "
   "unsubscribe rates. One-off purchase, no connector subscription.",
   ['Looker Studio', 'Audience growth', 'One-off'], 'DB', DB, DBBG, 'View template →',
   'verified live; narrowed from a gallery'),
]

HUBSPOT = [
 card('hubspot-marketing', 1, 'HubSpot Marketing Performance', 'Supermetrics',
   'https://supermetrics.com/template-gallery/looker-studio-hubspot-marketing-performance',
   'Free*',
   "Lifecycle stages, source attribution and email campaign performance in one view — the "
   "closest thing to a full marketing-side HubSpot report. Free template; connector "
   "required after the trial.",
   ['Looker Studio', 'Lifecycle', 'Attribution'], 'SM', SM, SMBG, 'View template →',
   'replaces dead looker-studio-hubspot slug'),
 card('hubspot-marketing', 2, 'HubSpot Content Marketing', 'Supermetrics',
   'https://supermetrics.com/template-gallery/looker-studio-hubspot-content-marketing',
   'Free*',
   "Blog engagement, lead-generation tracking and content funnel performance. Pairs well "
   "with the marketing performance template rather than duplicating it.",
   ['Looker Studio', 'Content', 'Funnel'], 'SM', SM, SMBG, 'View template →',
   'verified live'),
 card('hubspot-marketing', 3, 'HubSpot Overview', 'Catchr',
   'https://www.catchr.io/template/looker-studio-templates/template-hubspot-overview',
   'Free*',
   "Open deals, contract value, company sessions and CRM ownership — a sales-side view "
   "rather than a marketing one. Free template; connector needs a plan after the trial.",
   ['Looker Studio', 'Deals', 'CRM'], 'CA', CA, CABG, 'View template →',
   'replaces dead catchr /hubspot slug'),
 card('hubspot-marketing', 4, 'HubSpot Report Template', 'Porter Metrics',
   'https://portermetrics.com/en/templates/google-looker-studio/hubspot-porter-reports/',
   'Free',
   "Conversion rates, traffic, deal stages and lead scores. Free download, white-label "
   "ready — and unlike most Porter templates this one is genuinely HubSpot-specific.",
   ['Looker Studio', 'Deal stages', 'White-label'], 'PM', PM, PMBG, 'View template →',
   'narrowed from Porter gallery; HubSpot-specific, not generic PPC'),
 card('hubspot-marketing', 5, 'HubSpot Sales Pipeline Dashboard', 'Windsor.ai',
   'https://windsor.ai/looker-studio-hubspot-dashboard-template/', 'Free',
   "Sales pipeline with contact categorisation and industry and geography breakdowns. "
   "Useful when marketing needs to show pipeline contribution, not just leads.",
   ['Looker Studio', 'Pipeline', 'Segmentation'], 'WS', WS, WSBG, 'View template →',
   'verified live'),
 card('hubspot-marketing', 6, 'HubSpot Marketing Hub Dashboard', 'Windsor.ai',
   'https://windsor.ai/hubspot-marketing-dashboard-template-looker-studio/', 'Free',
   "Real-time campaign KPIs pulled from HubSpot Marketing Hub. The lighter of Windsor's "
   "two HubSpot templates — start here if you only need campaign numbers.",
   ['Looker Studio', 'Campaign KPIs', 'Real-time'], 'WS', WS, WSBG, 'View template →',
   'verified live'),
 card('hubspot-marketing', 7, 'HubSpot Dashboard', 'Whatagraph',
   'https://whatagraph.com/hubspot-dashboard?fpr=marketingreports', 'Free trial',
   "Customer behaviour, email click-through, engagement and bounces, plus lifecycle "
   "stages. Runs inside Whatagraph; needs a subscription after the trial.",
   ['Whatagraph', 'Lifecycle', 'Client reporting'], 'WG', WG, WGBG, 'View template →',
   'verified live', affiliate=True),
]

for cat, rows in (('email-marketing', EMAIL), ('hubspot-marketing', HUBSPOT)):
    old = [e for e in ents if e['category'] == cat]
    for e in old:
        ents.remove(e)
    ents.extend(rows)
    print(f"{cat}: {len(old)} cards -> {len(rows)} verified live")

json.dump(d, open('dashboards.json', 'w'), indent=2)
