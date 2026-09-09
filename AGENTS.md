# AGENTS.md

## Project overview

Nora's Kitchen is a static recipe site built with Python, Jinja2, HTML, CSS, and vanilla JavaScript.

## Source of truth

- Current recipe content lives in `recipes/*.json`.
- Use `templates/` for page structure and `static/` for CSS, JavaScript, and image assets.
- `archive/` contains historical recipe-book sources and build tooling. Do not modify it unless the task explicitly concerns the historical pipeline.
- `docs/` is generated output and is ignored by Git. Do not edit generated files directly.

## Development

- Install dependencies with `python3 -m venv .venv`, activate the environment, and run `python -m pip install -r requirements.txt`.
- Run `python serve.py` for a local preview.
- Run `python build.py` to generate the static site without starting a server.

## Recipe changes

- Add or edit recipes as JSON files under `recipes/`.
- Preserve the existing recipe JSON shape and filename-based recipe IDs.
- Update templates or build logic only when the requested behavior affects the site globally.

## Verification

After changes, run:

```bash
python -m unittest -v test_build.py
```

For site or template changes, also run:

```bash
python build.py
```

Do not overwrite unrelated user changes in the working tree.
