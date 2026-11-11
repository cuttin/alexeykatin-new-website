# alexeykatin.xyz: decisions and operations

## What the site is

- Main site: a professional profile. Menu: About / Projects / CV. Experience and education appear only on `/cv/`.
- `/memories/`: the 24 kept posts of the old WordPress blog japanforayear.ru (Russian, 2014-2021), as a timeline
  with category filters (Япония / Азия / США / Полезное). The R posts ("dplyr", "Немного об R") were dropped on purpose.
- The only link into `/memories/` is the "old travel notes" link on `/about/`. No menu item and no home-page link.
  The memories pages have no menu at all. They are still in the sitemap and indexable (deliberate).
- Never link lakeoutlook or crossingforecast from this site.

## Old URLs

`web/public/_redirects` (301): `/work.html` and `/work` go to `/projects/estuary-forecasting/`; `/fun.html` and
`/contact.html` go to `/about/`; `/cv_html_04-15-2021.html` goes to `/cv/`.
Old blog posts were at `japanforayear.ru/<stem>.html`; the same stem is the folder name here, so they live at
`/memories/<stem>/`. A redirect from the .ru domain is only possible while that domain is alive.

## How the notes were converted

`tools/convert_memories.py` reads the static mirror (`Documents/japanforayear-static/site`, made by `mirror.py`)
and writes Markdown. It keeps paragraph text, bold, links and video embeds; `<br>` becomes a paragraph break;
photo links to Yandex Fotki are dropped (the photo itself is copied locally); links to other kept posts are rewritten
to `/memories/<stem>/`, links to dropped pages keep their text only. Photos that are dead at the source are skipped
(2 in the kept posts: one in akvarium-osaki-kayukan, one in zamok-osaki-i-neboskreb-umeda).

What went wrong: 10 photos carry an EXIF Orientation tag (9 x value 6, 1 x value 3) although their pixels are
already upright. Astro's image service honours the tag and turned them sideways. The converter now resets the tag
to 1 in the copies (checked on a raw vs. EXIF contact sheet, 2026-11-10).

Astro converts every photo to WebP at build time; timeline thumbnails are 240 px wide.

## Theme switch

Dark is the default unless the system prefers light; the button (crossingforecast sun/moon icon) stores the choice
in localStorage (wrapped in try/catch). An inline script in `<head>` applies the stored theme before first paint.

## Domain and email

The site runs on its own Cloudflare account ("alexeykatin.xyz"); the test address is
https://alexeykatin.alexeykatin-xyz.workers.dev/. The first deploy went green on 2026-11-10.

alexeykatin.xyz is still registered at reg.ru, but since 2026-11-10 its nameservers are Cloudflare's
(chuck / magdalena.ns.cloudflare.com). Remaining steps:
1. In Cloudflare DNS, delete the four imported GitHub Pages records (three A 185.199.x.153 and the `www` CNAME),
   then right away add `alexeykatin.xyz` and `www.alexeykatin.xyz` as Custom domains on the `alexeykatin` Worker.
   Cloudflare refuses a custom domain while another record exists for the same name.
2. Turn off GitHub Pages on the old repo `cuttin/alexeykatin` and archive it.
3. Transfer the registration to Cloudflare Registrar: unlock at reg.ru, get the EPP code, enter it under Transfer
   Domains. The zone must be Active on Cloudflare first. DNSSEC is off, so no 24 h wait is needed.

The site's contact address is hello@alexeykatin.xyz. It only receives mail once Cloudflare Email Routing
forwards it to a real inbox (Email > Email Routing on the zone, which adds the MX and SPF records).
