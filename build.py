import json
import shutil
from collections import Counter
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


PROJECT_ROOT = Path(__file__).resolve().parent


def build_recipes(json_dir=None, template_dir=None, output_dir=None):
    """Build the static site from recipe JSON files."""
    json_path = Path(json_dir) if json_dir else PROJECT_ROOT / "recipes"
    template_path = Path(template_dir) if template_dir else PROJECT_ROOT / "templates"
    output_path = Path(output_dir) if output_dir else PROJECT_ROOT / "docs"

    env = Environment(loader=FileSystemLoader(str(template_path)), autoescape=True)
    recipe_tpl = env.get_template("recipe.html")
    index_tpl = env.get_template("index.html")

    # Generated output is disposable and is ignored by Git. Preserve the
    # tracked placeholder so an empty output directory remains versioned.
    preserve_gitkeep = (output_path / ".gitkeep").is_file()
    shutil.rmtree(output_path, ignore_errors=True)
    (output_path / "recipes").mkdir(parents=True, exist_ok=True)
    shutil.copytree(PROJECT_ROOT / "static", output_path / "static")
    if preserve_gitkeep:
        (output_path / ".gitkeep").touch()

    recipes = []
    tag_counts = Counter()

    for source_path in sorted(json_path.glob("*.json"), key=lambda path: path.name.casefold()):
        recipe_id = source_path.stem
        html_file = f"{recipe_id}.html"

        with source_path.open("r", encoding="utf-8") as recipe_file:
            data = json.load(recipe_file)

        tags = data.get("tags", [])
        for tag in tags:
            tag_counts[tag] += 1

        recipe_tpl_data = {
            "title": data.get("title", ""),
            "introduction": data.get("introduction", ""),
            "ingredients": data.get("ingredients", []),
            "instructions": data.get("instructions", []),
            "notes": data.get("notes", ""),
            "tags": tags,
            "recipe_id": recipe_id,
        }
        (output_path / "recipes" / html_file).write_text(
            recipe_tpl.render(**recipe_tpl_data), encoding="utf-8"
        )

        recipes.append(
            {
                "title": data.get("title", ""),
                "filename": f"recipes/{html_file}",
                "ingredients": data.get("ingredients", []),
                "vegan": "vegan" in tags,
                "tags": tags,
            }
        )

    tag_summary = [
        {"name": tag, "count": count}
        for tag, count in sorted(tag_counts.items(), key=lambda item: (-item[1], item[0]))
    ]
    index_html = index_tpl.render(
        recipes=recipes,
        total_recipes=len(recipes),
        tag_counts=tag_summary,
    )
    (output_path / "index.html").write_text(index_html, encoding="utf-8")

    print(f"Generated site with {len(recipes)} recipes.")


if __name__ == "__main__":
    build_recipes()
