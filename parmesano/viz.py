import json
import csv
import io


_CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
    --bg: #0f0f1a; --card-bg: #1a1a2e; --card-hover: #16213e;
    --text: #e0e0e0; --text-muted: #8b8b9e; --link: #4fc3f7;
    --accent: #e94560; --accent-warm: #f5a623; --accent-cool: #6c757d;
    --border: #2a2a4a; --header-bg: #0a0a14;
    --font: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --radius: 8px; --transition: 0.2s ease;
}
body { background: var(--bg); color: var(--text); font-family: var(--font); }
a { color: var(--link); text-decoration: none; }
a:hover { text-decoration: underline; }

header {
    background: var(--header-bg); border-bottom: 1px solid var(--border);
    padding: 12px 24px; display: flex; align-items: center; justify-content: space-between;
    position: sticky; top: 0; z-index: 10;
}
header h1 { font-size: 1.2rem; font-weight: 600; }
header .stats { color: var(--text-muted); font-size: 0.85rem; }

#layout { display: grid; grid-template-columns: 300px 1fr; height: calc(100vh - 53px); }

#sidebar {
    background: var(--card-bg); border-right: 1px solid var(--border);
    overflow-y: auto; padding: 0;
}
#sidebar .search-box { padding: 12px; border-bottom: 1px solid var(--border); }
#sidebar .search-box input {
    width: 100%; padding: 8px 12px; border-radius: var(--radius);
    border: 1px solid var(--border); background: var(--bg); color: var(--text);
    font-size: 0.9rem; outline: none;
}
#sidebar .search-box input:focus { border-color: var(--link); }

.query-item {
    padding: 14px 16px; border-bottom: 1px solid var(--border);
    cursor: pointer; transition: background var(--transition);
}
.query-item:hover { background: var(--card-hover); }
.query-item.active { background: var(--card-hover); border-left: 3px solid var(--accent); padding-left: 13px; }
.query-item .q-text { font-size: 0.9rem; margin-bottom: 4px; word-break: break-word; }
.query-item .q-meta { font-size: 0.78rem; color: var(--text-muted); }

#sidebar .sidebar-footer {
    padding: 12px 16px; border-top: 1px solid var(--border);
    font-size: 0.78rem; color: var(--text-muted);
}

#main { overflow-y: auto; padding: 24px; }
#main .toolbar {
    display: flex; align-items: center; gap: 12px; margin-bottom: 20px;
    flex-wrap: wrap;
}
#main .toolbar input {
    flex: 1; min-width: 200px; padding: 8px 12px; border-radius: var(--radius);
    border: 1px solid var(--border); background: var(--card-bg); color: var(--text);
    font-size: 0.9rem; outline: none;
}
#main .toolbar input:focus { border-color: var(--link); }
#main .toolbar select {
    padding: 8px 12px; border-radius: var(--radius);
    border: 1px solid var(--border); background: var(--card-bg); color: var(--text);
    font-size: 0.85rem; outline: none; cursor: pointer;
}
#main .query-header { margin-bottom: 20px; }
#main .query-header h2 { font-size: 1.15rem; font-weight: 500; margin-bottom: 4px; }
#main .query-header .qh-meta { font-size: 0.82rem; color: var(--text-muted); }

.paper-card {
    background: var(--card-bg); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 16px 20px; margin-bottom: 12px;
    transition: border-color var(--transition), transform var(--transition);
}
.paper-card:hover { border-color: var(--link); transform: translateY(-1px); }
.paper-card .pc-header { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 8px; }
.paper-card .pc-cites {
    flex-shrink: 0; min-width: 60px; text-align: center;
    padding: 4px 8px; border-radius: var(--radius);
    font-size: 0.85rem; font-weight: 700;
}
.paper-card .pc-cites.hot { background: rgba(233,69,96,0.15); color: var(--accent); }
.paper-card .pc-cites.warm { background: rgba(245,166,35,0.15); color: var(--accent-warm); }
.paper-card .pc-cites.cool { background: rgba(108,117,125,0.15); color: var(--accent-cool); }
.paper-card .pc-title { font-size: 1rem; font-weight: 500; line-height: 1.4; }
.paper-card .pc-title a { color: var(--text); }
.paper-card .pc-title a:hover { color: var(--link); text-decoration: none; }
.paper-card .pc-meta { font-size: 0.82rem; color: var(--text-muted); margin-bottom: 6px; }
.paper-card .pc-snippet {
    font-size: 0.85rem; color: var(--text-muted); line-height: 1.5;
    margin-top: 8px; padding-top: 8px; border-top: 1px solid var(--border);
}
.paper-card .pc-badges { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }
.paper-card .pc-badge {
    font-size: 0.72rem; padding: 2px 8px; border-radius: 12px;
    background: rgba(79,195,247,0.12); color: var(--link);
}
.paper-card .pc-badge.pdf { background: rgba(233,69,96,0.12); color: var(--accent); }
.paper-card .pc-badge.type { background: rgba(108,117,125,0.2); color: var(--text-muted); }

.empty-state { text-align: center; padding: 60px 20px; color: var(--text-muted); }
.empty-state .icon { font-size: 3rem; margin-bottom: 12px; }
.empty-state p { font-size: 0.95rem; }

@media (max-width: 768px) {
    #layout { grid-template-columns: 1fr; }
    #sidebar { display: none; }
    #sidebar.open { display: block; position: fixed; top: 53px; left: 0; bottom: 0; width: 280px; z-index: 20; }
}
"""

_JS = """
const DATA = __DATA_PLACEHOLDER__;

let currentQueryIdx = 0;
let sortBy = 'citations';
let filterText = '';

function getCitesClass(c) {
    if (c === undefined || c === null || c === 0) return '';
    if (c >= 1000) return 'hot';
    if (c >= 100) return 'warm';
    return 'cool';
}

function formatCites(c) {
    if (c === undefined || c === null) return '-';
    if (c >= 1000) return (c/1000).toFixed(1) + 'k';
    return String(c);
}

function renderSidebar() {
    const el = document.getElementById('query-list');
    el.innerHTML = DATA.searches.map((s, i) => {
        const count = s.results_fetched || s.results.length || 0;
        const err = s.error ? ' ⚠' : '';
        const active = i === currentQueryIdx ? ' active' : '';
        return `<div class="query-item${active}" data-idx="${i}">
            <div class="q-text">${esc(s.query)}${err}</div>
            <div class="q-meta">${count} papers · ${s.total_results ? s.total_results.toLocaleString() : '?'} total</div>
        </div>`;
    }).join('');
}

function renderPapers() {
    const s = DATA.searches[currentQueryIdx];
    const header = document.getElementById('query-header');
    const papers = document.getElementById('papers');
    const filter = document.getElementById('filter-input');
    if (filter) filter.value = filterText;

    if (!s || s.error) {
        header.innerHTML = `<h2>${esc(s?.query || '')}</h2><div class="qh-meta" style="color:var(--accent)">Error: ${esc(s?.error || 'Unknown')}</div>`;
        papers.innerHTML = '';
        return;
    }

    header.innerHTML = `<h2>${esc(s.query)}</h2>
        <div class="qh-meta">${s.results_fetched || 0} papers fetched · ${(s.total_results || 0).toLocaleString()} total indexed by Scholar</div>`;

    let results = [...(s.results || [])];

    if (filterText) {
        const q = filterText.toLowerCase();
        results = results.filter(r =>
            (r.title || '').toLowerCase().includes(q) ||
            (r.snippet || '').toLowerCase().includes(q) ||
            (r.authors || []).some(a => a.toLowerCase().includes(q)) ||
            (r.publication_summary || '').toLowerCase().includes(q)
        );
    }

    if (sortBy === 'citations') {
        results.sort((a, b) => (b.cited_by || 0) - (a.cited_by || 0));
    } else if (sortBy === 'title') {
        results.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
    } else if (sortBy === 'position') {
        results.sort((a, b) => (a.position || 0) - (b.position || 0));
    }

    if (results.length === 0) {
        papers.innerHTML = `<div class="empty-state"><div class="icon">📭</div><p>No papers match your filter</p></div>`;
        return;
    }

    papers.innerHTML = results.map(r => {
        const cites = r.cited_by;
        const cls = getCitesClass(cites);
        const ptype = r.type || '';
        const badges = [];
        if (ptype) badges.push(`<span class="pc-badge type">${esc(ptype)}</span>`);
        if (r.resources) {
            r.resources.forEach(res => {
                const fmt = (res.file_format || '').toLowerCase();
                badges.push(`<a class="pc-badge ${fmt === 'pdf' ? 'pdf' : ''}" href="${esc(res.link)}" target="_blank" title="${esc(res.title || '')}">${esc(res.file_format || 'Resource')}</a>`);
            });
        }

        return `<div class="paper-card">
            <div class="pc-header">
                <div class="pc-cites ${cls}">${formatCites(cites)}</div>
                <div>
                    <div class="pc-title"><a href="${esc(r.link || '#')}" target="_blank">${esc(r.title || 'Untitled')}</a></div>
                    <div class="pc-meta">${esc(r.publication_summary || '')}${r.authors && r.authors.length ? ' · ' + esc(r.authors.slice(0,4).join(', ')) : ''}</div>
                    ${badges.length ? '<div class="pc-badges">' + badges.join('') + '</div>' : ''}
                </div>
            </div>
            ${r.snippet ? '<div class="pc-snippet">' + esc(r.snippet) + '</div>' : ''}
        </div>`;
    }).join('');
}

function esc(s) {
    if (!s) return '';
    const d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
}

function selectQuery(idx) {
    currentQueryIdx = idx;
    filterText = '';
    renderSidebar();
    renderPapers();
}

document.addEventListener('DOMContentLoaded', () => {
    renderSidebar();
    renderPapers();

    document.getElementById('query-list').addEventListener('click', e => {
        const item = e.target.closest('.query-item');
        if (item) selectQuery(parseInt(item.dataset.idx));
    });

    document.getElementById('filter-input').addEventListener('input', e => {
        filterText = e.target.value;
        renderPapers();
    });

    document.getElementById('sort-select').addEventListener('change', e => {
        sortBy = e.target.value;
        renderPapers();
    });
});
"""


_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Parmesano Results</title>
<style>__CSS__</style>
</head>
<body>
<header>
    <h1>🧀 Parmesano</h1>
    <div class="stats" id="header-stats"></div>
</header>
<div id="layout">
    <aside id="sidebar">
        <div class="search-box">
            <input id="sidebar-search" type="text" placeholder="Filter queries..." oninput="
                const q = this.value.toLowerCase();
                document.querySelectorAll('#query-list .query-item').forEach(el => {
                    el.style.display = el.textContent.toLowerCase().includes(q) ? '' : 'none';
                });
            ">
        </div>
        <div id="query-list"></div>
        <div class="sidebar-footer" id="sidebar-footer"></div>
    </aside>
    <section id="main">
        <div class="toolbar">
            <input id="filter-input" type="text" placeholder="Filter papers by title, author, snippet...">
            <select id="sort-select">
                <option value="citations">Citations ↓</option>
                <option value="title">Title A-Z</option>
                <option value="position">Position</option>
            </select>
        </div>
        <div id="query-header" class="query-header"></div>
        <div id="papers"></div>
    </section>
</div>
<script>
__JS__
(function() {
    const d = DATA;
    const total = d.searches.reduce((s, q) => s + (q.results_fetched || q.results.length || 0), 0);
    document.getElementById('header-stats').textContent = d.searches.length + ' queries · ' + total + ' papers · ' + d.generated_at;
    document.getElementById('sidebar-footer').textContent = d.searches.length + ' queries · ' + total + ' papers';
})();
</script>
</body>
</html>
"""


def build_html(searches):
    data_json = json.dumps({"searches": searches}, ensure_ascii=False)
    js = _JS.replace("__DATA_PLACEHOLDER__", data_json)

    html = _HTML_TEMPLATE
    html = html.replace("__CSS__", _CSS)
    html = html.replace("__JS__", js)
    return html


def build_csv(searches):
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["query", "position", "title", "authors", "year",
                      "cited_by", "type", "link", "publication_summary", "snippet"])

    for s in searches:
        query = s.get("query", "")
        for r in s.get("results", []):
            writer.writerow([
                query,
                r.get("position", ""),
                r.get("title", ""),
                "; ".join(r.get("authors", [])),
                _extract_year(r.get("publication_summary", "")),
                r.get("cited_by", ""),
                r.get("type", ""),
                r.get("link", ""),
                r.get("publication_summary", ""),
                r.get("snippet", ""),
            ])

    return buf.getvalue()


def _extract_year(summary):
    if not summary:
        return ""
    for token in summary.split(" - "):
        token = token.strip()
        if token.isdigit() and 1900 <= int(token) <= 2100:
            return token
    import re
    m = re.search(r"\b(19|20)\d{2}\b", summary)
    return m.group(0) if m else ""
