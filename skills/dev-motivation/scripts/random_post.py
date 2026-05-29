#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import sys
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen


REQUIRED_FIELDS = ("handle", "post_url", "image_url")
DEFAULT_POSTS_URL = "https://raw.githubusercontent.com/fqlx/dev-motivation/main/skills/dev-motivation/data/posts.json"
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DEFAULT_DATA_PATH = DATA_DIR / "posts.json"
DEFAULT_CACHE_DIR = Path.home() / ".cache" / "dev-motivation" / "images"
SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


class PostDataError(Exception):
    """Raised when curated post data cannot produce a valid post."""


def load_json_source(source: str | Path) -> Any:
    source_text = str(source)
    try:
        if source_text.startswith(("https://", "http://")):
            with urlopen(source_text, timeout=10) as response:
                raw = response.read().decode("utf-8")
        else:
            raw = Path(source_text).expanduser().read_text(encoding="utf-8")
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise PostDataError(f"Invalid JSON in {source_text}: {exc}") from exc
    except FileNotFoundError as exc:
        raise PostDataError(f"Post data file not found: {source_text}") from exc
    except OSError as exc:
        raise PostDataError(f"Unable to read post data from {source_text}: {exc}") from exc
    except URLError as exc:
        raise PostDataError(f"Unable to fetch post data from {source_text}: {exc}") from exc


def normalize_posts(payload: Any) -> list[dict[str, str]]:
    if isinstance(payload, dict) and isinstance(payload.get("posts"), list):
        raw_posts = payload["posts"]
    elif isinstance(payload, list):
        raw_posts = payload
    else:
        raise PostDataError("Post data must be a JSON array or an object with a posts array.")

    if not raw_posts:
        raise PostDataError("No posts found in curated data.")

    valid_posts: list[dict[str, str]] = []
    for item in raw_posts:
        if not isinstance(item, dict):
            continue
        if any(not isinstance(item.get(field), str) or not item[field].strip() for field in REQUIRED_FIELDS):
            continue
        post = {field: item[field].strip() for field in REQUIRED_FIELDS}
        caption = item.get("caption")
        if isinstance(caption, str) and caption.strip():
            post["caption"] = caption.strip()
        valid_posts.append(post)

    if not valid_posts:
        raise PostDataError("No valid posts found. Each item needs handle, post_url, and image_url.")
    return valid_posts


def choose_post(source: str | Path, seed: int | None = None) -> dict[str, str]:
    posts = normalize_posts(load_json_source(source))
    rng = random.Random(seed)
    return rng.choice(posts)


def cache_dir() -> Path:
    configured_cache_dir = os.environ.get("DEV_MOTIVATION_CACHE_DIR")
    if configured_cache_dir:
        return Path(configured_cache_dir).expanduser()
    return DEFAULT_CACHE_DIR


def image_extension(image_url: str) -> str:
    parsed = urlparse(image_url)
    suffix = Path(parsed.path).suffix.lower()
    if suffix in SUPPORTED_IMAGE_EXTENSIONS:
        return suffix

    format_values = parse_qs(parsed.query).get("format", [])
    if format_values:
        format_suffix = f".{format_values[0].lower()}"
        if format_suffix in SUPPORTED_IMAGE_EXTENSIONS:
            return format_suffix

    return ".jpg"


def cached_image_path(image_url: str) -> Path:
    digest = hashlib.sha256(image_url.encode("utf-8")).hexdigest()[:24]
    return cache_dir() / f"{digest}{image_extension(image_url)}"


def local_image_ref(image_url: str) -> str:
    parsed = urlparse(image_url)
    if parsed.scheme not in {"http", "https"}:
        return image_url

    destination = cached_image_path(image_url)
    if not destination.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        request = Request(image_url, headers={"User-Agent": "dev-motivation/0.1"})
        try:
            with urlopen(request, timeout=20) as response:
                data = response.read()
            destination.write_bytes(data)
        except (OSError, URLError) as exc:
            raise PostDataError(f"Unable to cache motivation image from {image_url}: {exc}") from exc

    return str(destination.resolve())


def render_markdown(post: dict[str, str], *, cache_images: bool = True) -> str:
    image_ref = local_image_ref(post["image_url"]) if cache_images else post["image_url"]
    lines = [
        "Quick motivation break:",
        "",
        f"![Motivation photo]({image_ref})",
        "",
    ]
    caption = post.get("caption")
    if caption:
        lines.extend([caption, ""])
    lines.append(f"Source: {post['post_url']}")
    return "\n".join(lines)


def default_source() -> str:
    configured_source = os.environ.get("DEV_MOTIVATION_POSTS_URL") or os.environ.get("DEV_MOTIVATION_POSTS")
    if configured_source:
        return configured_source
    return DEFAULT_POSTS_URL


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render a random curated developer motivation image.")
    parser.add_argument("--source", default=default_source(), help="Local JSON path or HTTPS JSON URL.")
    parser.add_argument("--seed", type=int, help="Optional deterministic seed for tests.")
    args = parser.parse_args(argv)

    try:
        post = choose_post(args.source, seed=args.seed)
        markdown = render_markdown(post)
    except PostDataError as exc:
        print(f"dev-motivation: {exc}", file=sys.stderr)
        return 1

    print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
