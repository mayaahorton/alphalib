import csv
import os
from textwrap import dedent

GRID_HTML_FILENAME = "grid_items.html"
PROJECT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    body {{
      margin: 0;
      font-family: sans-serif;
      line-height: 1.6;
      background: #f9f9f9;
      color: #333;
      padding: 40px;
      max-width: 800px;
      margin: auto;
    }}
    h1 {{
      font-size: 2em;
      margin-bottom: 0.5em;
    }}
    img {{
      max-width: 100%;
      height: auto;
      display: block;
      margin: 20px 0;
      border: 1px solid #ccc;
      border-radius: 4px;
    }}
    a.back-link {{
      display: inline-block;
      margin-top: 30px;
      text-decoration: none;
      color: #0077cc;
    }}
    a.back-link:hover {{
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <img src="images/{image}" alt="{title}">
  <p><strong>Description:</strong> {description}</p>
  <a class="back-link" href="index.html">&larr; Back to gallery</a>
</body>
</html>
"""

def read_csv(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def generate_grid_html(projects):
    html_lines = []
    for idx, project in enumerate(projects, start=1):
        img = project['image']
        title = project['project_title']
        html_lines.append(
            f'    <div class="grid-item"><a href="project{idx}.html">'
            f'<img src="images/{img}" alt="{title}"></a></div>'
        )
    return '\n'.join(html_lines)

def generate_project_pages(projects):
    for idx, project in enumerate(projects, start=1):
        html = PROJECT_TEMPLATE.format(
            title=project['project_title'],
            image=project['image'],
            description=project.get('description', '')
        )
        with open(f"project{idx}.html", "w", encoding="utf-8") as f:
            f.write(html)

def generate_all(csv_file, rows=9, cols=9):
    projects = read_csv(csv_file)
    total_required = rows * cols
    if len(projects) < total_required:
        print(f"Warning: Only {len(projects)} items found, but grid requires {total_required}.")
        print("   Grid will be partially filled.")
    elif len(projects) > total_required:
        print(f"Note: {len(projects)} items found, trimming to first {total_required}.")
        projects = projects[:total_required]

    # Generate grid and project pages
    grid_html = generate_grid_html(projects)
    with open(GRID_HTML_FILENAME, "w", encoding="utf-8") as f:
        f.write(grid_html)
    print(f"{GRID_HTML_FILENAME} created with {len(projects)} grid items.")

    generate_project_pages(projects)
    print(f"{len(projects)} project pages generated (project1.html → project{len(projects)}.html)")

if __name__ == "__main__":
    # Customize grid size here
    generate_all("projects.csv", rows=4, cols=3)
