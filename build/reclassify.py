"""Re-classify gallery links using what the live pages actually are.

The URL-shape heuristic was wrong about Catchr: those pages are single
templates, not galleries. The problem there is the card copy overclaiming
("10+ templates"), not the destination.
"""
import json

d = json.load(open('dashboards.json'))

# Verified by fetching the live pages.
CATCHR_IS_SINGLE = True     # catchr.io/template/looker-studio-templates/<x> = one template
PORTER_IS_GALLERY = True    # portermetrics.com/en/templates/<x>/ = paginated listing

for e in d['entries']:
    host = e['url'].split('/')[2].replace('www.', '')
    if host == 'catchr.io' and e['link_type'] == 'gallery':
        e['link_type'] = 'individual'
        e['triage_note'] = 'VERIFIED single template page; card copy overclaims a set'
        e['copy_fix_needed'] = True
    elif host == 'portermetrics.com':
        e['triage_note'] = ('VERIFIED gallery (paginated). Porter individual templates are '
                            'generic multi-platform PPC, not platform-specific')

json.dump(d, open('dashboards.json', 'w'), indent=2)

import collections
c = collections.Counter(e['link_type'] for e in d['entries'])
print("RECLASSIFIED:", dict(c))
print("cards needing copy rewrite (link is fine):",
      sum(1 for e in d['entries'] if e.get('copy_fix_needed')))
