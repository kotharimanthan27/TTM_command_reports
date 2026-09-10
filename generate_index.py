import os


def generate_index():
    files = []
    for entry in os.listdir('.'):
        if not os.path.isfile(entry):
            continue
        if entry.startswith('.') or entry.lower() == 'index.html':
            continue
        lower = entry.lower()
        if lower.endswith('.html') or lower.endswith('.xlsx') or lower.endswith('.log'):
            files.append(entry)

    files = sorted(files, reverse=True)

    list_items = ""
    for file in files:
        lower = file.lower()
        if lower.endswith('.html'):
            label = f"Open report ({file})"
        elif lower.endswith('.xlsx'):
            label = f"Download workbook ({file})"
        else:
            label = f"Open log ({file})"

        list_items += f'        <li><a href="{file}">{label}</a></li>\n'

    html_content = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Automation Reports</title>
    <style>
      body {{
        font-family: Arial, sans-serif;
        line-height: 1.5;
        margin: 0;
        padding: 32px;
        color: #1f2933;
        background: #f7f9fb;
      }}

      main {{
        max-width: 840px;
        margin: 0 auto;
      }}

      h1 {{
        margin: 0 0 24px;
      }}

      ul {{
        list-style: none;
        padding: 0;
        margin: 0;
      }}

      li {{
        margin: 12px 0;
      }}

      a {{
        color: #0067b8;
        font-size: 18px;
        text-decoration: none;
      }}

      a:hover {{
        text-decoration: underline;
      }}
    </style>
  </head>
  <body>
    <main>
      <h1>Automation Reports</h1>
      <ul>
{list_items}      </ul>
    </main>
  </body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"index.html regenerated with {len(files)} files.")


if __name__ == "__main__":
    generate_index()
