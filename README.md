# Parmesano

Batch search Google Scholar via SerpAPI. Give it a list of topics, get back structured paper metadata — titles, authors, citations, links, and more.

## Features

- Multi-query batch searches from a plain text file
- Combined multi-topic searches (intersection of terms on one line)
- Configurable result count with automatic pagination
- Year range filtering and relevance/date sorting
- JSON output ready for downstream processing
- Error resilience: failed queries don't block the rest
- OpenCode skill integration

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
python -m parmesano -i queries.txt -o results.json --max-results 20
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

```
python -m parmesano -i <file> -o <file> [options]
```

| Flag | Default | Description |
|------|---------|-------------|
| `-i`, `--input` | *(required)* | File with one query per line |
| `-o`, `--output` | *(required)* | Output JSON path |
| `--max-results` | `10` | Max results per query (1–20: 1 API call; >20: paginated) |
| `--year-from` | *(none)* | Exclude results published before this year |
| `--year-to` | *(none)* | Exclude results published after this year |
| `--sort` | `relevance` | `relevance` (default, heavily weights citations) or `date` |

### Examples

```bash
# Basic search
python -m parmesano -i queries.txt -o results.json

# Get 50 results per query (3 API calls each: 20 + 20 + 10)
python -m parmesano -i queries.txt -o results.json --max-results 50

# Recent papers since 2020, sorted by date
python -m parmesano -i queries.txt -o results.json --year-from 2020 --sort date

# Narrow date range
python -m parmesano -i queries.txt -o results.json --year-from 2018 --year-to 2022
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

## API Limits & Cost

| Limit | Value |
|-------|-------|
| Results per API call | **20** (SerpAPI `num` parameter max) |
| Per-query theoretical max | ~1,000 (Google Scholar's own cap) |
| Cached searches | Free, not counted toward quota |

Pagination is automatic. Each set of 20 results costs one API call.

## OpenCode Skill

Parmesano ships with an OpenCode skill at `.opencode/skills/parmesano/SKILL.md`. It tells OpenCode how and when to run scholar searches on your behalf. Restart opencode to load it.

## Project Structure

```
Parmesano/
├── parmesano/
│   ├── __init__.py          # Version info
│   ├── __main__.py          # CLI entry point (argparse)
│   ├── scholar.py           # SerpAPI Scholar client + pagination
│   └── output.py            # JSON formatter
├── .opencode/skills/parmesano/
│   └── SKILL.md             # OpenCode skill definition
├── SKILL.md                 # Root copy (for portability)
├── requirements.txt         # google-search-results, python-dotenv
├── .env.example             # SERPAPI_KEY template
├── queries.example.txt      # Sample query file
├── example.sh               # End-to-end usage script
├── example/                 # SerpAPI documentation
└── README.md
```

## License

MIT
