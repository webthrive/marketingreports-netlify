"""Apply verified replacement URLs and copy fixes for google-ads and facebook-ads.

Every replacement below was fetched and confirmed to be a single template page
a visitor can actually obtain, per Colin's rule. Card copy is rewritten wherever
it claimed a set of templates or a platform specificity the template lacks.
"""
import json

d = json.load(open('dashboards.json'))
by_id = {e['id']: e for e in d['entries']}

FIX = {
 # --- google-ads ---
 'google-ads-02': dict(
   url='https://supermetrics.com/template-gallery/looker-studio-google-ads',
   name='Google Ads Report Template',
   blurb=("Supermetrics' Google Ads template for Looker Studio. Clicks, impressions, "
          "conversions and cost, broken down by device, geography and campaign. Free "
          "template; the Supermetrics connector is a paid subscription after the trial."),
   note='replaced dead slug looker-studio-google-ads-performance-dashboard'),
 'google-ads-04': dict(
   name='Google Ads KPI Dashboard',
   blurb=("Catchr's Google Ads KPI template covering performance, campaign analysis, "
          "keyword reporting and audience insights across nine metrics and eight "
          "dimensions. Free template; connector needs a Catchr plan after the 14-day trial."),
   note='copy fix — page is one template, not the "10+" the card claimed'),
 'google-ads-07': dict(
   url='https://www.databloo.com/templates/google-ads-report-template/',
   name='Google Ads Overview Report',
   price_tier='€99',
   blurb=("Data Bloo's premium multi-page Google Ads report. Campaign, keyword and "
          "creative breakdowns with an agency-ready layout. One-off purchase, no "
          "subscription."),
   note='narrowed from /report-templates/google-ads/ gallery to the product page'),
 'google-ads-08': dict(
   url='https://www.reportingninja.com/data-studio-templates/google-ads-report-template',
   name='Google Ads Report Template',
   blurb=("Reporting Ninja's free Google Ads template for Looker Studio. Opens directly "
          "in Looker Studio via 'Get the template'; connecting live data needs a "
          "Reporting Ninja account (15-day trial)."),
   note='replaced dead /looker-studio-templates/ path'),
 # --- facebook-ads ---
 'facebook-ads-01': dict(
   url='https://app.coupler.io/templates/4350aa90-8bb9-11ef-9f3b-9b166a69cafc/preview',
   name='Facebook Ads Dashboard',
   blurb=("Coupler.io's Facebook Ads dashboard — clicks, cost, ad frequency, plus "
          "demographic and geographic breakdowns. Previewable before signup."),
   note='replaced dead slug URL with the live UUID preview'),
 'facebook-ads-04': dict(
   name='Facebook (Meta) Ads Dashboard',
   blurb=("Catchr's four-page Meta Ads template for Looker Studio — campaign "
          "performance, creative analysis, audience demographics and funnel view. "
          "Free template; connector needs a Catchr plan after the 14-day trial."),
   note='copy fix — page is one 4-page template, not the "10+" the card claimed'),
 'facebook-ads-06': dict(
   url='https://www.databloo.com/templates/facebook-ads-looker-studio-template/',
   name='Facebook Ads Report Template',
   price_tier='€199',
   blurb=("Data Bloo's premium Facebook Ads report for Looker Studio. Multi-page "
          "campaign, creative and audience analysis with a client-ready layout. "
          "One-off purchase."),
   note='narrowed from /report-templates/facebook-ads/ gallery to the product page'),
}

for eid, patch in FIX.items():
    e = by_id[eid]
    note = patch.pop('note')
    if 'url' in patch:
        e['previous_url'] = e['url']
    e.update(patch)
    e['link_type'] = 'individual'
    e['liveness'] = 'LIVE'
    e['verified_on'] = '2026-08-30'
    e['triage_note'] = note
    e.pop('copy_fix_needed', None)
    e.pop('replacement_url', None)

json.dump(d, open('dashboards.json', 'w'), indent=2)

for cat in ('google-ads', 'facebook-ads'):
    rows = sorted([e for e in d['entries'] if e['category'] == cat], key=lambda e: e['position'])
    dead = sum(1 for e in rows if e['liveness'] == 'DEAD')
    gal = sum(1 for e in rows if e['link_type'] == 'gallery')
    print(f"{cat}: {len(rows)} cards | dead {dead} | gallery {gal} | "
          f"live individual {sum(1 for e in rows if e['liveness']=='LIVE' and e['link_type']=='individual')}")
