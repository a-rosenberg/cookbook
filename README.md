# Nora's Kitchen

Static recipe collection built with Python, Jinja2, HTML, CSS, and vanilla JavaScript.

## Local preview

Create an environment and install the one build dependency:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Build and serve the site locally:

```bash
python serve.py
```

Open <http://127.0.0.1:8000>. Use another port when needed:

```bash
python serve.py --port 8080
```

Stop the server with `Ctrl-C`.

## Build and verify

Generate the GitHub Pages output without starting a server:

```bash
python build.py
```

Run the build smoke test:

```bash
python -m unittest -v test_build.py
```

The generated `docs/` directory is ignored by Git. GitHub Actions rebuilds it during the Pages deployment workflow.
