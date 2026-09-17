import os
import re
from collections import defaultdict
from urllib.parse import quote


def get_sort_key(base_name):
    match = re.search(r'(\d{2})-(\d{2})-(\d{4})[ _](\d{2})-(\d{2})-(\d{2})', base_name)
    if match:
        day, month, year, h, m, s = match.groups()
        return f"{year}-{month}-{day}_{h}:{m}:{s}"
    return base_name


def parse_metadata(base_name):
    lower = base_name.lower()
    if 'rhymes' in lower:
        category = 'Rhymes'
        badge_class = 'badge-rhymes'
    elif 'mini' in lower:
        category = 'Mini'
        badge_class = 'badge-mini'
    else:
        category = 'General'
        badge_class = 'badge-general'

    match = re.search(r'(\d{2}-\d{2}-\d{4})[ _](\d{2})-(\d{2})-(\d{2})', base_name)
    if match:
        date_str = match.group(1)
        time_str = f"{match.group(2)}:{match.group(3)}:{match.group(4)}"
        formatted_date = f"{date_str} &middot; {time_str}"
    else:
        formatted_date = "Report"

    return category, badge_class, formatted_date


def generate_index():
    groups = defaultdict(dict)
    all_files = []

    for entry in os.listdir('.'):
        if not os.path.isfile(entry) or entry.startswith('.') or entry.lower() == 'index.html':
            continue
        lower = entry.lower()
        if lower.endswith('.html') and entry != 'test_generate_index.py':
            base = entry[:-5]
            groups[base]['html'] = entry
            all_files.append(entry)
        elif lower.endswith('.xlsx'):
            base = entry[:-5]
            groups[base]['xlsx'] = entry
            all_files.append(entry)
        elif lower.endswith('.log'):
            base = entry[:-4]
            groups[base]['log'] = entry
            all_files.append(entry)

    sorted_groups = sorted(groups.items(), key=lambda x: get_sort_key(x[0]), reverse=True)

    categories = set()
    cards_html = ""

    for base, files in sorted_groups:
        category, badge_class, formatted_date = parse_metadata(base)
        categories.add(category)
        search_query = base.lower()

        # HTML action
        if 'html' in files:
            html_href = quote(files['html'])
            html_btn = f'<a href="{html_href}" class="btn btn-html" target="_blank">HTML Report</a>'
        else:
            html_btn = '<span class="btn btn-disabled">No HTML</span>'

        # Excel action
        if 'xlsx' in files:
            xlsx_href = quote(files['xlsx'])
            excel_btn = f'<a href="{xlsx_href}" class="btn btn-excel" download>Excel Workbook</a>'
        else:
            excel_btn = '<span class="btn btn-disabled">No Excel</span>'

        # Log action
        if 'log' in files:
            log_href = quote(files['log'])
            log_btn = f'<a href="{log_href}" class="btn btn-log" target="_blank">View Log</a>'
        else:
            log_btn = '<span class="btn btn-disabled">No Log</span>'

        cards_html += f"""        <div class="report-card" data-category="{category}" data-search="{search_query}">
          <div class="card-header">
            <span class="badge {badge_class}">{category}</span>
            <span class="report-date">{formatted_date}</span>
          </div>
          <h3 class="report-name">{base}</h3>
          <div class="card-actions">
            {html_btn}
            {excel_btn}
            {log_btn}
          </div>
        </div>\n"""

    filter_buttons_html = '<button class="filter-btn active" data-filter="all">All Reports</button>\n'
    for cat in sorted(categories):
        filter_buttons_html += f'          <button class="filter-btn" data-filter="{cat}">{cat}</button>\n'

    html_content = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>TTM Command Reports | Automation Dashboard</title>
    <meta name="description" content="Dashboard for accessing automation command reports and execution workbooks.">
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
      :root {{
        --bg-main: #f8fafc;
        --bg-card: #ffffff;
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --border-color: #e2e8f0;
        --primary: #4f46e5;
        --primary-hover: #4338ca;
        --success: #10b981;
        --success-hover: #059669;
        --disabled: #94a3b8;
        --disabled-bg: #f1f5f9;
        --font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      }}

      * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
      }}

      body {{
        font-family: var(--font-family);
        background-color: var(--bg-main);
        color: var(--text-primary);
        line-height: 1.5;
        padding: 40px 24px;
        min-height: 100vh;
      }}

      main {{
        max-width: 1080px;
        margin: 0 auto;
      }}

      header {{
        margin-bottom: 36px;
        text-align: center;
      }}

      .header-title {{
        font-size: 36px;
        font-weight: 800;
        letter-spacing: -0.025em;
        background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-fill-color: transparent;
        margin-bottom: 8px;
      }}

      .header-subtitle {{
        color: var(--text-secondary);
        font-size: 16px;
        font-weight: 500;
      }}

      /* Search and Filter Section */
      .controls {{
        display: flex;
        flex-direction: column;
        gap: 16px;
        background: var(--bg-card);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05);
        margin-bottom: 32px;
      }}

      .search-input {{
        width: 100%;
        padding: 14px 16px;
        font-family: var(--font-family);
        font-size: 15px;
        border: 1px solid var(--border-color);
        border-radius: 10px;
        background-color: #f8fafc;
        outline: none;
        transition: all 0.2s ease;
        color: var(--text-primary);
      }}

      .search-input:focus {{
        border-color: var(--primary);
        background-color: #fff;
        box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);
      }}

      .filters-wrapper {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        align-items: center;
      }}

      .filter-btn {{
        padding: 8px 16px;
        font-family: var(--font-family);
        font-size: 14px;
        font-weight: 600;
        border-radius: 8px;
        border: 1px solid var(--border-color);
        background: #fff;
        color: var(--text-secondary);
        cursor: pointer;
        transition: all 0.2s ease;
      }}

      .filter-btn:hover {{
        border-color: #cbd5e1;
        color: var(--text-primary);
      }}

      .filter-btn.active {{
        background: var(--primary);
        border-color: var(--primary);
        color: #fff;
      }}

      /* Reports Grid */
      .reports-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 20px;
      }}

      .report-card {{
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
        display: flex;
        flex-direction: column;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
      }}

      .report-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
      }}

      .card-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
      }}

      .badge {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        padding: 4px 10px;
        border-radius: 6px;
        letter-spacing: 0.05em;
      }}

      .badge-rhymes {{
        background-color: #fef3c7;
        color: #92400e;
      }}

      .badge-mini {{
        background-color: #d1fae5;
        color: #065f46;
      }}

      .badge-general {{
        background-color: #f1f5f9;
        color: #334155;
      }}

      .report-date {{
        font-size: 13px;
        font-weight: 500;
        color: var(--text-secondary);
      }}

      .report-name {{
        font-size: 15px;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 24px;
        flex-grow: 1;
        word-break: break-word;
        line-height: 1.4;
      }}

      .card-actions {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
        margin-top: auto;
      }}

      .btn {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 10px 8px;
        font-size: 12px;
        font-weight: 700;
        border-radius: 8px;
        text-decoration: none;
        transition: all 0.2s ease;
        text-align: center;
        border: none;
        cursor: pointer;
      }}

      .btn-html {{
        background-color: var(--primary);
        color: #fff;
      }}

      .btn-html:hover {{
        background-color: var(--primary-hover);
      }}

      .btn-excel {{
        background-color: var(--success);
        color: #fff;
      }}

      .btn-excel:hover {{
        background-color: var(--success-hover);
      }}

      .btn-log {{
        background-color: #f1f5f9;
        color: var(--text-secondary);
        border: 1px solid var(--border-color);
      }}

      .btn-log:hover {{
        background-color: #e2e8f0;
        color: var(--text-primary);
      }}

      .btn-disabled {{
        background-color: var(--disabled-bg);
        color: var(--disabled);
        cursor: not-allowed;
      }}

      /* Empty State */
      .empty-state {{
        grid-column: 1 / -1;
        text-align: center;
        padding: 48px 24px;
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        display: none;
      }}

      .empty-state h4 {{
        font-size: 18px;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 8px;
      }}

      .empty-state p {{
        font-size: 14px;
        color: var(--text-secondary);
      }}
    </style>
  </head>
  <body>
    <main>
      <header>
        <h1 class="header-title">TTM Command Reports</h1>
        <p class="header-subtitle">Access your latest automation test runs, Excel workbooks, and execution logs</p>
      </header>

      <section class="controls">
        <div class="search-wrapper">
          <input type="text" id="search-input" class="search-input" placeholder="Search reports by device, date, or test name...">
        </div>
        <div class="filters-wrapper">
          {filter_buttons_html}        </div>
      </section>

      <section class="reports-grid" id="reports-grid">
{cards_html}        <div class="empty-state" id="empty-state">
          <h4>No Reports Found</h4>
          <p>Try adjusting your search query or category filter</p>
        </div>
      </section>
    </main>

    <script>
      const searchInput = document.getElementById('search-input');
      const filterButtons = document.querySelectorAll('.filter-btn');
      const reportCards = document.querySelectorAll('.report-card');
      const emptyState = document.getElementById('empty-state');

      let activeFilter = 'all';
      let searchQuery = '';

      function filterReports() {{
        let visibleCount = 0;

        reportCards.forEach(card => {{
          const cardCategory = card.getAttribute('data-category');
          const cardSearch = card.getAttribute('data-search') || '';

          const matchesFilter = (activeFilter === 'all' || cardCategory === activeFilter);
          const matchesSearch = cardSearch.includes(searchQuery);

          if (matchesFilter && matchesSearch) {{
            card.style.display = 'flex';
            visibleCount++;
          }} else {{
            card.style.display = 'none';
          }}
        }});

        if (visibleCount === 0) {{
          emptyState.style.display = 'block';
        }} else {{
          emptyState.style.display = 'none';
        }}
      }}

      searchInput.addEventListener('input', (e) => {{
        searchQuery = e.target.value.toLowerCase().trim();
        filterReports();
      }});

      filterButtons.forEach(btn => {{
        btn.addEventListener('click', () => {{
          filterButtons.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          activeFilter = btn.getAttribute('data-filter');
          filterReports();
        }});
      }});
    </script>
  </body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"index.html regenerated with {len(sorted_groups)} report cards ({len(all_files)} total files).")


if __name__ == "__main__":
    generate_index()
