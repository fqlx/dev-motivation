---
name: dev-motivation
description: "Use occasionally as a reward after meaningful development milestones: pushing a lot of code, opening an important PR, finishing deep focused work, passing verification after hard debugging, repeated failures, or long work stretches. Also use when the user subtly asks for a break, reset, boost, or motivation. Do not use for routine small edits."
---

# Dev Motivation

Show a curated SFW motivation image as a brief reward when it would help the developer's flow.

## When To Use

- After completing a substantial task.
- After pushing a lot of code or landing a meaningful implementation.
- After opening an important PR or preparing a major change for review.
- After a deep focused work block, especially if the user seems tired or proud of the progress.
- After fixing a difficult bug or failing test.
- After a long investigation or repeated failed attempts.
- During a difficult stretch when the developer seems stuck or fatigued.
- After verification passes following meaningful work.
- When the user uses subtle break language such as needing a reset, boost, breather, reward, or saying the work was a grind.
- When the user explicitly asks for motivation.

## Frequency Rules

- Keep this rare. In ordinary work, do not show more than once per session.
- In long sessions, prefer at least 30 to 60 minutes between images.
- After major milestones such as a substantial push, important PR, or hard verification pass, prefer showing one unless a motivation image was shown recently.
- At softer eligible moments, use a low random chance, around 20% to 30%.
- Do not interrupt urgent requests, code review findings, security-sensitive work, or concise status updates.
- Do not show images after routine small edits, trivial commands, or every response.

## How To Render One

Run the script from this skill directory:

```bash
python3 scripts/random_post.py
```

By default, the script reads the curated list from the GitHub-hosted `posts.json` file in `fqlx/dev-motivation`.

Copy the script output into the response exactly as Markdown. The script caches the selected remote image locally and emits an absolute local image path for Codex to render. Do not scrape X/Twitter, profile pages, media tabs, or post HTML. The curated data must include direct image URLs for caching and X post URLs for attribution.
