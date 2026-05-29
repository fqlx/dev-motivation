import json
import tempfile
import unittest
from pathlib import Path

import sys

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = PLUGIN_ROOT / "skills" / "dev-motivation" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import random_post


class RandomPostTests(unittest.TestCase):
    def write_posts(self, value):
        handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        with handle:
            if isinstance(value, str):
                handle.write(value)
            else:
                json.dump(value, handle)
        return Path(handle.name)

    def test_renders_markdown_for_valid_curated_post(self):
        path = self.write_posts([
            {
                "handle": "creator",
                "post_url": "https://x.com/creator/status/123",
                "image_url": "https://pbs.twimg.com/media/example.jpg",
                "caption": "Ship the hard thing",
                "tags": ["milestone"]
            }
        ])

        post = random_post.choose_post(path, seed=7)
        markdown = random_post.render_markdown(post)

        self.assertIn("![Motivation photo](https://pbs.twimg.com/media/example.jpg)", markdown)
        self.assertIn("Source: https://x.com/creator/status/123", markdown)
        self.assertIn("Ship the hard thing", markdown)

    def test_skips_invalid_entries(self):
        path = self.write_posts([
            {"handle": "missing-image", "post_url": "https://x.com/a/status/1"},
            {
                "handle": "creator",
                "post_url": "https://x.com/creator/status/123",
                "image_url": "https://pbs.twimg.com/media/example.jpg"
            }
        ])

        post = random_post.choose_post(path, seed=1)

        self.assertEqual(post["handle"], "creator")

    def test_empty_list_raises_clear_error(self):
        path = self.write_posts([])

        with self.assertRaisesRegex(random_post.PostDataError, "No posts found"):
            random_post.choose_post(path, seed=1)

    def test_invalid_json_raises_clear_error(self):
        path = self.write_posts("{not json")

        with self.assertRaisesRegex(random_post.PostDataError, "Invalid JSON"):
            random_post.choose_post(path, seed=1)


if __name__ == "__main__":
    unittest.main()
