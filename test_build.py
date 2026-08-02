import json
import tempfile
import unittest
from html import unescape
from pathlib import Path
from urllib.parse import quote

from build import build_recipes


PROJECT_ROOT = Path(__file__).resolve().parent


class BuildSmokeTest(unittest.TestCase):
    def test_build_generates_complete_site(self):
        recipe_sources = sorted((PROJECT_ROOT / "recipes").glob("*.json"))

        with tempfile.TemporaryDirectory() as temporary_directory:
            output_dir = Path(temporary_directory)
            build_recipes(output_dir=output_dir)

            recipe_pages = sorted((output_dir / "recipes").glob("*.html"))
            self.assertEqual(len(recipe_pages), len(recipe_sources))
            self.assertTrue((output_dir / "index.html").is_file())
            self.assertTrue((output_dir / "static" / "nora_favicon.png").is_file())
            self.assertTrue((output_dir / "static" / "site.js").is_file())

            index_html = (output_dir / "index.html").read_text(encoding="utf-8")
            self.assertIn(f"{len(recipe_sources)}", index_html)
            self.assertIn("recipes worth making twice.", index_html)
            self.assertIn("browse the collection.", index_html)
            self.assertNotIn("ways to browse", index_html)

            for source_path in recipe_sources:
                with source_path.open("r", encoding="utf-8") as recipe_file:
                    recipe = json.load(recipe_file)
                page_path = output_dir / "recipes" / f"{source_path.stem}.html"
                self.assertTrue(page_path.is_file(), recipe.get("title", source_path.name))
                page_html = unescape(page_path.read_text(encoding="utf-8"))
                self.assertIn(recipe.get("title", "").lower(), page_html)
                for tag in recipe.get("tags", []):
                    self.assertIn(f"../index.html?tag={quote(tag)}", page_html)


if __name__ == "__main__":
    unittest.main()
