import os
import json
import shutil
from jinja2 import Environment, FileSystemLoader

def build_recipes(json_dir='recipes', template_dir='templates', output_dir='docs'):
    env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)
    recipe_tpl = env.get_template('recipe.html')
    index_tpl = env.get_template('index.html')

    # Clean and prepare output
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(os.path.join(output_dir, 'static'))

    # Copy CSS
    shutil.copy('static/styles.css', os.path.join(output_dir, 'static', 'styles.css'))

    recipes = []
    for fname in sorted(os.listdir(json_dir)):
        if not fname.endswith('.json'):
            continue
        data = json.load(open(os.path.join(json_dir, fname), 'r', encoding='utf-8'))
        name = os.path.splitext(fname)[0]
        outfile = f"recipes/{name}.html"

        # Render recipe page
        html = recipe_tpl.render(
            title=data.get('title',''),
            introduction=data.get('introduction',''),
            ingredients=data.get('ingredients',[]),
            instructions=data.get('instructions',[]),
            notes=data.get('notes','')
        )
        out_path = os.path.join(output_dir, outfile)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        open(out_path, 'w', encoding='utf-8').write(html)

        # Include ingredients for search
        recipes.append({
            'title': data.get('title',''),
            'filename': outfile,
            'ingredients': data.get('ingredients',[])
        })

    # Render index page
    index_html = index_tpl.render(recipes=recipes)
    open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8').write(index_html)

    print(f"Generated docs with {len(recipes)} recipes.")

if __name__ == '__main__':
    build_recipes()