# Dev Motivation

## Install

```bash
codex plugin marketplace add FQLX/dev-motivation
```

Dev Motivation is a Codex plugin that occasionally shows a curated SFW motivation image after hard development work.

It does not scrape X/Twitter. The plugin reads its curated post list from GitHub by default and embeds direct `pbs.twimg.com` image URLs with source X post attribution.

## What It Does

- Shows motivation images rarely, after meaningful progress or difficult work.
- Uses the GitHub-hosted curated list in `skills/dev-motivation/data/posts.json`.
- Keeps the source X post URL attached for attribution.

## Add Posts

Add entries to `skills/dev-motivation/data/posts.json`, then commit and push.

Each entry needs:

- `handle`
- `post_url`
- `image_url`

Optional:

- `caption`
- `tags`
