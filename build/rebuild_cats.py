"""Finish google-ads and facebook-ads: split bundles, narrow galleries, drop dead ends.

Rule applied throughout: a card links to ONE dashboard a visitor can actually get.
Where a vendor only offers a generic multi-platform template, the copy says so
rather than implying platform specificity the template does not have.
"""
import json, copy

d = json.load(open('dashboards.json'))
by_id = {e['id']: e for e in d['entries']}
ents = d['entries']


def clone(src_id, **over):
    e = copy.deepcopy(by_id[src_id])
    e.update(over)
    e['liveness'] = 'LIVE'; e['link_type'] = 'individual'
    e['verified_on'] = '2026-08-30'; e['duplicate_of'] = None
    e.pop('copy_fix_needed', None); e.pop('replacement_url', None)
    return e


def drop(eid, why):
    e = by_id[eid]
    ents.remove(e)
    print(f"  DROPPED {eid}: {e['name'][:40]} — {why}")


# ---- google-ads-03: Radyant "3-pack" gallery -> 4 individual free templates ----
RADYANT = [
 ("Google Ads E-Commerce Template",
  "https://datastudio.google.com/reporting/66b5455b-1c08-47b0-84c9-727942673f3b",
  "ROAS, revenue and purchase tracking for e-commerce Google Ads accounts. Opens "
  "straight in Looker Studio — free, no email required, native Google Ads connector.",
  ["Looker Studio", "E-commerce", "ROAS"]),
 ("Google Ads Lead Gen Template",
  "https://datastudio.google.com/reporting/53e19458-4089-4852-8f17-eb8ab2dda3b2",
  "Lead volume, cost per lead and conversion trends for lead-gen accounts. Free and "
  "ungated — copy it directly in Looker Studio.",
  ["Looker Studio", "Lead gen", "CPL"]),
 ("Google Ads Lead Gen + Offline Conversions",
  "https://datastudio.google.com/reporting/b079b59c-75ce-404b-80dd-05c67f7ee7e1",
  "Lead-gen reporting with offline conversion tracking, for accounts importing "
  "closed-won data back into Google Ads. Free, no signup.",
  ["Looker Studio", "Offline conversions", "Lead gen"]),
 ("Google Ads Keyword Insights",
  "https://datastudio.google.com/reporting/2b610f3c-f909-4d1c-a7b1-7c5e9ff446d3",
  "Keyword-level performance — spend, conversions and search term drill-down. Free "
  "and ungated in Looker Studio.",
  ["Looker Studio", "Keywords", "Search terms"]),
]
src = by_id['google-ads-03']
pos = src['position']
ents.remove(src)
for i, (name, url, blurb, tags) in enumerate(RADYANT):
    ents.append(clone('google-ads-04',
        id=f'google-ads-03{chr(97+i)}', position=pos + i * 0.1,
        name=name, url=url, blurb=blurb, tags=tags,
        vendor='Radyant', badge_initials='RY', price_tier='Free',
        cta_label='Open template →',
        triage_note='split from Radyant 4-template bundle page; direct Looker Studio report'))
print(f"  SPLIT google-ads-03 (Radyant bundle) -> {len(RADYANT)} individual free templates")

# ---- Porter Metrics galleries -> one individual template each, copy made honest ----
by_id['google-ads-05'].update(
  url='https://portermetrics.com/en/templates/google-looker-studio/ppc-kpis-porter-reports/',
  name='PPC KPIs Report',
  vendor='Porter Metrics',
  blurb=("Porter's PPC KPI template — CTR, CPA, conversion rate and spend. Works across "
         "Google Ads, Meta, LinkedIn, TikTok and X from one report, so it suits "
         "multi-channel accounts more than Google-only ones. Free download."),
  tags=['Looker Studio', 'Multi-platform', 'KPIs'],
  link_type='individual', liveness='LIVE', verified_on='2026-08-30',
  triage_note='narrowed from Porter gallery; copy corrected — template is multi-platform, not Google-specific')
by_id['facebook-ads-03'].update(
  url='https://portermetrics.com/en/templates/google-looker-studio/ppc-creative-performance-porter-reports/',
  name='PPC Creative Performance Report',
  vendor='Porter Metrics',
  blurb=("Creative-level performance reporting — which ads and assets actually drive "
         "results. Covers Meta alongside Google, LinkedIn and TikTok from one template. "
         "Free download, white-label ready."),
  tags=['Looker Studio', 'Creative', 'Multi-platform'],
  link_type='individual', liveness='LIVE', verified_on='2026-08-30',
  triage_note='narrowed from Porter gallery; copy corrected — template is multi-platform')
print("  NARROWED google-ads-05 and facebook-ads-03 (Porter galleries -> individual templates)")

# ---- facebook-ads-07: Dataslayer article -> the Looker Studio template it hosts ----
by_id['facebook-ads-07'].update(
  url='https://lookerstudio.google.com/u/0/reporting/cfd2397f-eace-420e-80ac-1b20e0b2c577/template',
  name='Meta Ads Performance Dashboard',
  blurb=("Seven-KPI Meta Ads dashboard — reach, impressions, link clicks and CTR, with "
         "campaign, placement and demographic breakdowns. Opens as a Looker Studio "
         "template you copy directly."),
  link_type='individual', liveness='LIVE', verified_on='2026-08-30',
  previous_url='https://www.dataslayer.ai/blog/meta-ads-performance-dashboard',
  triage_note='was a blog article; now links to the Looker Studio template the article hosts')
print("  REPOINTED facebook-ads-07 (article -> the template it hosts)")

# ---- drops ----
drop('google-ads-06', 'Dataslayer page 404s and they publish no replacement template page')
drop('facebook-ads-08', 'duplicate of facebook-ads-01, and its URL was already dead')

# renumber
for cat in ('google-ads', 'facebook-ads'):
    rows = sorted([e for e in ents if e['category'] == cat], key=lambda e: e['position'])
    for i, e in enumerate(rows, 1):
        e['position'] = i
        e['id'] = f'{cat}-{i:02d}'

json.dump(d, open('dashboards.json', 'w'), indent=2)

print()
for cat in ('google-ads', 'facebook-ads'):
    rows = sorted([e for e in ents if e['category'] == cat], key=lambda e: e['position'])
    print(f"=== {cat}: {len(rows)} cards ===")
    for e in rows:
        print(f"  {e['position']}. {e['name'][:42]:42s} {e['vendor'][:16]:16s} {e['price_tier']:6s} {e['link_type']}")
