# Dev Motivation

Dev Motivation is a Codex plugin that occasionally shows a curated SFW motivation image after hard development work.

It does not scrape X/Twitter. You provide a curated JSON list with direct image URLs for embedding and source post URLs for attribution.

## Curated Data

Use either a JSON object with `posts`:

```json
{
  "posts": [
    {
      "handle": "creator_handle",
      "post_url": "https://x.com/creator_handle/status/123",
      "image_url": "https://pbs.twimg.com/media/example.jpg",
      "caption": "Optional short caption",
      "tags": ["focus", "milestone"]
    }
  ]
}
```

or a bare JSON array with the same objects.

Required fields are `handle`, `post_url`, and `image_url`.

## Local List

Copy `skills/dev-motivation/data/posts.example.json` somewhere private, replace the sample values, and set:

```bash
export DEV_MOTIVATION_POSTS="$HOME/dev-motivation-posts.json"
```

## GitHub-Hosted List

You can keep the curated JSON file in a GitHub repo and point the plugin at the raw file:

```bash
export DEV_MOTIVATION_POSTS_URL="https://raw.githubusercontent.com/<owner>/<repo>/<branch>/posts.json"
```

For private repos, prefer a local file path unless you already have a secure way to fetch the raw file.

## Manual Test

```bash
cd skills/dev-motivation
python3 scripts/random_post.py
```

## Behavior

The skill tells agents to keep image insertion rare: after meaningful progress, difficult debugging, repeated failed attempts, or long work stretches. It should not appear after routine edits or in every response.
