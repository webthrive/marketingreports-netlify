# Deployment

The site is a static HTML build deployed on **Vercel** from the `main` branch
of `webthrive/marketingreports`. There is no build step — Vercel serves the
repo root as-is.

## Header configuration

Headers live in `vercel.json`. Three security headers plus cache policy:

| Header | Value | Why |
|---|---|---|
| `X-Frame-Options` | `DENY` | Stops the site being iframed into a clickjacking wrapper. |
| `X-Content-Type-Options` | `nosniff` | Stops browsers guessing content types. |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Sends the origin, not the full path, to affiliate destinations. |
| `Cache-Control` (HTML) | `max-age=0, s-maxage=3600, must-revalidate` | Edge caches for an hour; browsers always revalidate, so a fix ships immediately. |
| `Cache-Control` (`/assets/*`) | `max-age=31536000, immutable` | Fingerprinted assets never change. |

## There is no netlify.toml any more

The repo used to carry a `netlify.toml` declaring `X-Frame-Options`,
`X-Content-Type-Options` and a cache policy. The site deploys on Vercel, which
does not read that file, so **none of those headers ever reached a request** —
the file looked like configuration and did nothing. It has been deleted rather
than kept, because a config file that silently does nothing is worse than no
config file. `vercel.json` is now the only place headers are defined.

## Generated pages

The ten `/marketing-dashboards/*/` category pages, `/reporting-tools/`,
`sitemap.xml` and `robots.txt` are **generated** from `build/dashboards.json`.
Do not hand-edit them — edit the catalog and run:

    python3 build/build.py --out out

`build/verify.py` will fail if a generated page in the repo has drifted from
what the catalog produces.
