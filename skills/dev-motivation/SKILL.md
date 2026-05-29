---
name: dev-motivation
description: Use rarely after substantial coding progress, difficult debugging, repeated failures, or long work stretches when a developer could use a brief motivation image. Do not use for routine small edits.
---

# Dev Motivation

Show a curated SFW motivation image only when it would help the developer's flow.

## When To Use

- After completing a substantial task.
- After fixing a difficult bug or failing test.
- After a long investigation or repeated failed attempts.
- During a difficult stretch when the developer seems stuck or fatigued.
- After verification passes following meaningful work.
- When the user explicitly asks for motivation.

## Frequency Rules

- Keep this rare. In ordinary work, do not show more than once per session.
- In long sessions, prefer at least 30 to 60 minutes between images.
- At eligible moments, use a low random chance, around 10% to 20%.
- Do not interrupt urgent requests, code review findings, security-sensitive work, or concise status updates.
- Do not show images after routine small edits, trivial commands, or every response.

## How To Render One

Run the script from this skill directory:

```bash
python3 scripts/random_post.py
```

By default, the script reads the curated list from the GitHub-hosted `posts.json` file in `FQLX/dev-motivation`.

Copy the script output into the response exactly as Markdown. Do not scrape X/Twitter, profile pages, media tabs, or post HTML. The curated data must include direct image URLs for embedding and X post URLs for attribution.
