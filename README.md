# Dev Motivation

Dev Motivation is a Codex plugin that occasionally shows a curated SFW motivation image after hard development work.

It does not scrape X/Twitter. The recommended setup is the link approach: provide direct `pbs.twimg.com` image URLs for embedding and source X post URLs for attribution.

## Install

Clone the plugin into Codex's local plugin directory:

```bash
mkdir -p "$HOME/plugins"
git clone https://github.com/FQLX/dev-motivation.git "$HOME/plugins/dev-motivation"
```

Register it in your personal Codex marketplace:

```bash
mkdir -p "$HOME/.agents/plugins"
python3 - <<'PY'
import json
from pathlib import Path

marketplace_path = Path.home() / ".agents" / "plugins" / "marketplace.json"
entry = {
    "name": "dev-motivation",
    "source": {
        "source": "local",
        "path": "./plugins/dev-motivation"
    },
    "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
    },
    "category": "Productivity"
}

if marketplace_path.exists():
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
else:
    marketplace = {
        "name": "personal",
        "interface": {
            "displayName": "Personal"
        },
        "plugins": []
    }

marketplace["name"] = marketplace.get("name") or "personal"
marketplace.setdefault("interface", {}).setdefault("displayName", "Personal")
plugins = marketplace.setdefault("plugins", [])

for index, plugin in enumerate(plugins):
    if isinstance(plugin, dict) and plugin.get("name") == "dev-motivation":
        plugins[index] = entry
        break
else:
    plugins.append(entry)

marketplace_path.write_text(json.dumps(marketplace, indent=2) + "\n", encoding="utf-8")
print(f"Registered dev-motivation in {marketplace_path}")
PY
```

Restart Codex or start a new Codex session so the plugin skill is loaded.

## Update

```bash
git -C "$HOME/plugins/dev-motivation" pull --ff-only
```

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

For an X post like:

```text
https://x.com/asiancutiesss/status/2059865534103961919/photo/1
```

use the post URL as `post_url` and the direct media URL as `image_url`:

```json
{
  "handle": "asiancutiesss",
  "post_url": "https://x.com/asiancutiesss/status/2059865534103961919/photo/1",
  "image_url": "https://pbs.twimg.com/media/HJYcr31WAAQE9re.jpg",
  "caption": "Curated motivation break.",
  "tags": ["motivation", "x-link"]
}
```

## Bundled Posts

The plugin ships with curated posts in:

```text
skills/dev-motivation/data/posts.json
```

To add more bundled posts, append entries to that file and commit the change.

## Local List

To keep your own private list outside the plugin repo, copy `skills/dev-motivation/data/posts.json`, replace or add entries, and set:

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

From a fresh clone, you can run:

```bash
cd "$HOME/plugins/dev-motivation"
python3 skills/dev-motivation/scripts/random_post.py --seed 1
```

## Behavior

The skill tells agents to keep image insertion rare: after meaningful progress, difficult debugging, repeated failed attempts, or long work stretches. It should not appear after routine edits or in every response.
