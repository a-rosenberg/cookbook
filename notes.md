```html<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title | lower }} | nora's kitchen</title>
  <link rel="stylesheet" href="../static/styles.css">
</head>
<body>
  <div class="container">
    <a href="../index.html" class="back-button">← back to recipes</a>

    <div class="banner">
      <h1 class="recipe-title">{{ title | lower }}</h1>
    </div>

    {% if introduction %}
    <section class="section-card">
      <h2>introduction</h2>
      <p>{{ introduction }}</p>
    </section>
    {% endif %}

    <section class="section-card">
      <h2>ingredients</h2>
      <ul>
        {% for item in ingredients %}
        <li>{{ item }}</li>
        {% endfor %}
      </ul>
    </section>

    <section class="section-card">
      <h2>instructions</h2>
      <ol>
        {% for step in instructions %}
        <li>{{ step }}</li>
        {% endfor %}
      </ol>
    </section>

    {% if notes %}
    <section class="section-card">
      <h2>notes</h2>
      <p>{{ notes }}</p>
    </section>
    {% endif %}
  </div>
</body>
</html>
```