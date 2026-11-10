# alexeykatin.xyz

Personal site of Alexey Katin: a professional profile (Home, About, Projects, CV) and an archive of old
Russian travel notes from japanforayear.ru at `/memories/`. Astro static site on Cloudflare Workers static assets.

## Layout

| Path | What |
|---|---|
| `web/src/pages/` | Pages: `index`, `about`, `cv`, `projects/`, `memories/` (timeline + one page per note), `404` |
| `web/src/layouts/Base.astro` | Shared head, header menu, theme switch, footer |
| `web/src/styles/site.css` | All styles; dark and light theme tokens |
| `web/src/content/memories/<stem>/` | One old post: `index.md` plus its photos `01.jpg`, `02.jpg`, ... |
| `web/src/lib/memories.js` | Loads the notes and their photos, Russian dates |
| `web/public/` | Static files: headshot, research figures, `_redirects`, `robots.txt`, favicon |
| `tools/convert_memories.py` | Regenerates `web/src/content/memories/` from the static mirror of japanforayear.ru |
| `design/` (local only, gitignored) | Approved HTML mockups; they point at the local mirror, so they stay off GitHub |

## Commands

```
cd web
npm ci
npm run dev       # http://localhost:4321
npm run build     # -> web/dist
npm run preview
```

Regenerate the notes (overwrites `web/src/content/memories/`, reads the mirror only):

```
python -I tools/convert_memories.py
```

## Deploy

`.github/workflows/deploy.yml` builds and runs `wrangler deploy` on every push to `main` that touches `web/`.
It needs the repository secret `CLOUDFLARE_API_TOKEN` and the repository variable `CF_ACCOUNT_ID`.
See `docs/DOCUMENTATION.md` for the domain move.
