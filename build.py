import os
import json
import shutil
from jinja2 import Environment, FileSystemLoader

def build_recipes(json_dir='recipes', template_dir='templates', output_dir='docs'):
    env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)
    recipe_tpl = env.get_template('recipe.html')
    index_tpl = env.get_template('index.html')

    # Recreate entire output directory
    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(os.path.join(output_dir, 'recipes'), exist_ok=True)

    # Copy static assets
    shutil.copytree('static', os.path.join(output_dir, 'static'))

    recipes = []

    for filename in sorted(os.listdir(json_dir)):
        if not filename.endswith('.json'):
            continue

        name = os.path.splitext(filename)[0]
        html_file = f"{name}.html"
        out_path = os.path.join(output_dir, 'recipes', html_file)

        with open(os.path.join(json_dir, filename), 'r', encoding='utf-8') as f:
            data = json.load(f)

        html = recipe_tpl.render(
            title=data.get('title', ''),
            introduction=data.get('introduction', ''),
            ingredients=data.get('ingredients', []),
            instructions=data.get('instructions', []),
            notes=data.get('notes', ''),
            tags=data.get('tags', [])
        )

        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)

        recipes.append({
            'title': data.get('title', ''),
            'filename': f"recipes/{html_file}",
            'ingredients': data.get('ingredients', []),
            'vegan': 'vegan' in data.get('tags', []),
            'tags': data.get('tags', []),
        })

    # Generate index page
    index_html = index_tpl.render(recipes=recipes)
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

    print(f"Generated site with {len(recipes)} recipes.")

if __name__ == '__main__':
    build_recipes()
