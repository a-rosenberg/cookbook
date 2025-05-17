import re
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass, asdict


@dataclass
class Recipe:
    date: str
    title: str
    introduction: str
    ingredients: List[str]
    instructions: List[str]
    notes: str

    def to_dict(self) -> Dict:
        """Convert Recipe dataclass to a JSON-serializable dict."""
        return asdict(self)


def extract_date(html: str) -> str:
    """
    Extract and ISO-format the date from an HTML snippet.

    Expects a <p align="right">MM.DD.YYYY</p> tag.
    """
    match = re.search(r'<p\s+align="right">(.*?)</p>', html)
    raw = match.group(1).strip() if match else ""

    try:
        clean_date = datetime.strptime(raw, '%m.%d.%Y').strftime('%Y-%m-%d') if raw else ""
    except ValueError:
        clean_date = datetime.strptime(raw, '%Y.%m.%d').strftime('%Y-%m-%d') if raw else ""
    return clean_date

def extract_title(html: str) -> str:
    """
    Extract the recipe title from the <h1> tag.
    """
    match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE)
    return match.group(1).strip() if match else ""


def extract_ingredients(html: str) -> List[str]:
    """
    Pull the bullet-list under '### ingredients' and return each as a string.
    """
    block = re.search(r'### ingredients\s*([\s\S]*?)\s*### instructions', html)
    if not block:
        return []
    lines = block.group(1).splitlines()
    return [line.lstrip('- ').strip().replace('–', '-').replace('—', '-') for line in lines if line.strip().startswith('-')]



def normalize_step(step: str, typos: Dict[str, str] = None) -> str:
    """
    Apply rule-based normalization to a single instruction line:
      - Turn “350F” (or any number + F) into “350°F”
      - Convert numeric ranges “30-32” into en-dash “30–32”
      - Fix common typos via a lookup dict
      - Normalize special dashes (en/em) to standard dash
    """
    # 1) Normalize en/em dashes to regular dash
    step = step.replace('–', '-').replace('—', '-')

    # 2) Fahrenheit: any integer/decimal + optional space + 'F' → '°F'
    step = re.sub(r'(\d+(?:\.\d+)?)\s*F\b', r'\1°F', step)

    # 3) Numeric ranges: digits - digits → digits–digits
    step = re.sub(
        r'(?P<a>\d+(?:\.\d+)?)\s*-\s*(?P<b>\d+(?:\.\d+)?)',
        r'\g<a>–\g<b>',
        step
    )

    # 4) Typos: e.g. 'depent' → 'dependent', 'chococlate' → 'chocolate'
    if typos is None:
        typos = {
            'depent': 'dependent',
            'chococlate': 'chocolate',
        }
    for wrong, right in typos.items():
        # word-boundary replace, case-insensitive
        step = re.sub(rf'\b{re.escape(wrong)}\b', right, step, flags=re.IGNORECASE)

    return step



def extract_instructions(html: str) -> List[str]:
    """
    Pull the numbered steps under '### instructions', strip the leading digits,
    and apply rule-based normalization. Works even if there's no ### notes.
    """
    match = re.search(
        r'### instructions\s*([\s\S]*?)(?:### notes|$)',
        html,
        re.IGNORECASE
    )
    if not match:
        return []

    raw_block = match.group(1)
    steps = []
    for line in raw_block.splitlines():
        if m := re.match(r'^\s*\d+\.\s*(.*)', line):
            step = m.group(1).strip()
            steps.append(normalize_step(step))

    return steps




def extract_notes(html: str) -> str:
    """
    Grab everything after '### notes' and collapse into one clean paragraph.
    """
    block = re.search(r'### notes\s*([\s\S]*)$', html)
    if not block:
        return ""
    raw = ' '.join(block.group(1).split()).replace('–', '-')
    # minor typo fixes
    return raw.replace('chococlate', 'chocolate').replace('flag.', 'flag.')


def parse_recipe_html(html: str) -> Recipe:
    """
    Parse the full HTML text of one recipe into a Recipe object.
    """
    return Recipe(
        date=extract_date(html),
        title=extract_title(html),
        introduction="",
        ingredients=extract_ingredients(html),
        instructions=extract_instructions(html),
        notes=extract_notes(html),
    )


if __name__ == "__main__":
    folder_path = '/Users/aaron.rosenberg/Projects/cookbook/recipes'
    output_dir = Path('/recipes')
    folder = Path(folder_path)
    recipes: List[Dict] = []

    for html_file in folder.glob("*.md"):
        print(html_file)
        html_text = html_file.read_text(encoding="utf-8")
        recipe = parse_recipe_html(html_text)

        recipe_dict = recipe.to_dict()
        recipe_to_write = json.dumps(recipe_dict, indent=2, ensure_ascii=False)

        raw_title = recipe_dict['title']
        # 1) remove any character that isn’t A–Z or space
        sanitized = re.sub(r'[^A-Za-z ]+', '', raw_title)
        # 2) collapse multiple spaces, trim edges, then replace spaces with hyphens
        filename = re.sub(r'\s+', ' ', sanitized).strip().replace(' ', '-') + '.json'

        output_path = output_dir / filename

        with open(output_path, 'w', encoding='utf-8') as f:
        # with open(output_path, 'w') as f:
            f.write(recipe_to_write)

        recipes.append(recipe_dict)

    # with open(output_path, "w", encoding="utf-8") as f:
    #     json.dump(recipes, f, indent=2, ensure_ascii=False)

    import pandas as pd

    df = pd.DataFrame.from_records(recipes)
    df.to_csv('recipe_df.csv', index=False)