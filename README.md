# Parmesano

Batch search Google Scholar via SerpAPI. Give it a list of topics, get back structured paper metadata — titles, authors, citations, links, and more.

## Features

- Multi-query batch searches from a plain text file
- Combined multi-topic searches (intersection of terms on one line)
- Configurable result count with automatic pagination
- Year range filtering and relevance/date sorting
- Dark-theme HTML visualizer with search, sort, and filter
- CSV export for Excel/LibreOffice
- JSON output ready for downstream processing
- Error resilience: failed queries don't block the rest
- OpenCode skill integration (two skills, one pipeline)

## Prerequisites

- Python 3.8+
- A [SerpAPI key](https://serpapi.com/manage-api-key) (free tier available)

## Installation

```bash
git clone https://github.com/Alan-Amparo/Parmesano.git
cd Parmesano
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your key: SERPAPI_KEY=your_key_here
```

## Quick Start

```bash
echo 'Deep Learning Data Augmentation 3D Fossil Reconstruction' > queries.txt
python -m parmesano search -i queries.txt -o results.json --max-results 20
```

## Query Strategies

**Combined search** — one line, multiple terms. Google Scholar returns papers matching all terms:

```
Deep Learning Data Augmentation 3D Fossil Reconstruction
# → Papers at the intersection of all three topics
```

**Batch search** — one line per topic. Each runs independently:

```
Artificial Intelligence
X Ray Diffraction
CRISPR Gene Editing
# → Three separate result sets in one JSON
```

Avoid wrapping terms in double quotes unless you need exact phrase matching. Overly strict quoted queries often return zero results.

## CLI Reference

Parmesano has two subcommands:

### `search` — Run searches

```
python -m parmesano search -i <file> -o <file> [options]
```

| Flag | Default | Description |
|------|---------|-------------|
| `-i`, `--input` | *(required)* | File with one query per line |
| `-o`, `--output` | *(required)* | Output JSON path, or base directory with `--visualize` |
| `--max-results` | `10` | Max results per query (1–20: 1 API call; >20: paginated) |
| `--year-from` | *(none)* | Exclude results published before this year |
| `--year-to` | *(none)* | Exclude results published after this year |
| `--sort` | `relevance` | `relevance` (default, heavily weights citations) or `date` |
| `--visualize` | `off` | Generate timestamped output folder with HTML, JSON, and CSV |

### `visualize` — From existing JSON

```
python -m parmesano visualize <results.json> [-o results/]
```

Generates a timestamped output folder from a previously saved `results.json`.

### Examples

```bash
# Basic search → single JSON
python -m parmesano search -i queries.txt -o results.json

# Search + generate visualizer in timestamped folder
python -m parmesano search -i queries.txt -o results/ --visualize --max-results 20

# Get 50 results per query (3 API calls each: 20 + 20 + 10)
python -m parmesano search -i queries.txt -o results.json --max-results 50

# Recent papers since 2020, sorted by date
python -m parmesano search -i queries.txt -o results.json --year-from 2020 --sort date

# Narrow date range
python -m parmesano search -i queries.txt -o results.json --year-from 2018 --year-to 2022

# Visualize an existing results.json
python -m parmesano visualize results.json -o results/
```

## Output Format

```json
{
  "generated_at": "2026-06-15T04:17:02.676159Z",
  "total_queries": 2,
  "searches": [
    {
      "query": "Artificial Intelligence",
      "total_results": 6020000,
      "results_fetched": 10,
      "results": [
        {
          "position": 1,
          "title": "Machine learning",
          "link": "https://books.google.com/books?id=...",
          "snippet": "A comprehensive introduction to machine learning...",
          "type": "Book",
          "result_id": "EQ8shYj8Ai8J",
          "publication_summary": "ZH Zhou - 2021 - books.google.com",
          "authors": ["ZH Zhou"],
          "cited_by": 3318,
          "resources": [
            {
              "title": "pomona.edu",
              "link": "https://cs.pomona.edu/...",
              "file_format": "PDF"
            }
          ]
        }
      ]
    }
  ]
}
```

### Result Fields

| Field | Always present | Description |
|-------|:---:|-------------|
| `position` | Yes | Rank in search results |
| `title` | Yes | Paper title |
| `link` | Yes | URL to the paper |
| `snippet` | Yes | Text excerpt |
| `result_id` | Yes | SerpAPI internal ID |
| `type` | Yes | `Book`, `Pdf`, `Html`, `Ps`, etc. |
| `publication_summary` | Most | Authors, year, journal/publisher |
| `authors` | Most | List of author names |
| `cited_by` | Many | Citation count |
| `resources` | Some | Links to PDFs or other file formats |

## Visualizer

The `--visualize` flag generates a **self-contained HTML report** in a
timestamped folder. Open `index.html` in any browser — no server required.

```
results/2026-06-15_16-30-00/
├── index.html       # Dark-theme interactive visualizer
├── data.json        # Full structured results
└── data.csv         # Flat CSV (Excel/LibreOffice compatible)
```

### Features

- **Two-panel layout**: query list (left) · paper cards (right)
- **Citation badges**: hot (>1000) red, warm (>100) orange, cool (≤100) grey
- **Sort**: by citations (default), title A-Z, or position
- **Filter**: instant search across titles, authors, snippets
- **Query sidebar**: click to switch between queries, filter queries by name
- **Per-paper card**: title (clickable link), authors, publication info, snippet, type badge, resource links (PDF)
- **Error handling**: failed queries shown with error message
- **Responsive**: mobile-friendly layout
- **Zero dependencies**: single self-contained HTML file

### CSV Columns

`query`, `position`, `title`, `authors`, `year`, `cited_by`, `type`, `link`, `publication_summary`, `snippet`

## API Limits & Cost

| Limit | Value |
|-------|-------|
| Results per API call | **20** (SerpAPI `num` parameter max) |
| Per-query theoretical max | ~1,000 (Google Scholar's own cap) |
| Cached searches | Free, not counted toward quota |

Pagination is automatic. Each set of 20 results costs one API call.

## OpenCode Skills

Parmesano ships with two OpenCode skills that chain together into a full
literature review pipeline.

### Full Pipeline

```
Codebase → [queries-generator] → queries.txt → [parmesano] → results/
                                                               ├── index.html
                                                               ├── data.json
                                                               └── data.csv
```

In OpenCode, just say:

> *"Generate queries from this codebase and search them on Google Scholar"*

### `parmesano` Skill

Located at `.opencode/skills/parmesano/SKILL.md`. Runs the Parmesano CLI to
search Google Scholar. Handles batch queries, combined searches, pagination,
year filters, and JSON output.

### `queries-generator` Skill

Located at `.opencode/skills/queries-generator/SKILL.md`. Analyzes a codebase
through two reasoning layers:

**Layer 1 — Technical Extraction:** reads source code, model definitions,
training loops, and configs to identify every concrete technique actually
used (Dropout, BatchNorm, Adam, Transformers, Data Augmentation, etc.).

**Layer 2 — Scientific Expansion:** maps each technique to its academic
neighborhood — foundational papers, variants, alternatives, and theoretical 
underpinnings. Then generates 100 combined 2-4 term queries bridging
implementation to research.

Example: `nn.BatchNorm2d()` in code becomes queries like *"Batch Normalization
Internal Covariate Shift Training Stability"*, *"Layer Normalization Instance
Normalization Group Normalization"*, etc.

Restart opencode after cloning to load both skills.

## Project Structure

```
Parmesano/
├── parmesano/
│   ├── __init__.py          # Version info
│   ├── __main__.py          # CLI (search + visualize subcommands)
│   ├── scholar.py           # SerpAPI Scholar client + pagination
│   ├── output.py            # JSON/CSV/HTML output + folder generation
│   └── viz.py               # HTML visualizer template + CSV builder
├── .opencode/skills/parmesano/
│   └── SKILL.md             # Search execution skill
├── .opencode/skills/queries-generator/
│   └── SKILL.md             # Codebase-to-queries skill
├── SKILL.md                 # Root copy of parmesano skill
├── SKILL-queries-generator.md # Root copy of queries-generator skill
├── requirements.txt         # google-search-results, python-dotenv
├── .env.example             # SERPAPI_KEY template
├── queries.example.txt      # Sample query file
├── example.sh               # End-to-end usage script
└── README.md
```

## License

MIT
