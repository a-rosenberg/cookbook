import os
import json
import shutil
from jinja2 import Environment, FileSystemLoader

def build_recipes(json_dir='recipes', template_dir='templates', output_dir='docs'):
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)
    recipe_tpl = env.get_template('recipe.html')
    index_tpl = env.get_template('index.html')

    # Clean and prepare output directory
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    # Copy entire static folder (including logo, styles, etc.)
    shutil.copytree('static', os.path.join(output_dir, 'static'))

    os.makedirs(os.path.join(output_dir, 'recipes'), exist_ok=True)

    # Generate recipe pages
    recipes = []
    for fname in sorted(os.listdir(json_dir)):
        if not fname.endswith('.json'):
            continue
        data = json.load(open(os.path.join(json_dir, fname), 'r', encoding='utf-8'))
        name = os.path.splitext(fname)[0]
        out_path = os.path.join(output_dir, 'recipes', f"{name}.html")
        html = recipe_tpl.render(
            title=data.get('title', ''),
            introduction=data.get('introduction', ''),
            ingredients=data.get('ingredients', []),
            instructions=data.get('instructions', []),
            notes=data.get('notes', '')
        )
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)

        recipes.append({
            'title': data.get('title', ''),
            'filename': f"recipes/{name}.html",
            'ingredients': data.get('ingredients', [])
        })

    # Generate index page
    index_html = index_tpl.render(recipes=recipes)
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

    print(f"Generated site with {len(recipes)} recipes.")

if __name__ == '__main__':
    build_recipes()