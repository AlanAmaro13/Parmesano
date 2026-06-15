# Parmesano

Search Google Scholar via SerpAPI for a list of queries.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your SerpAPI key from https://serpapi.com/manage-api-key
```

## Usage

Write one query per line in a file:

```
Artificial Intelligence
X Ray Diffraction
Large Language Models
```

Then run:

```bash
python -m parmesano -i queries.txt -o results.json
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `-i`, `--input` | *(required)* | File with one query per line |
| `-o`, `--output` | *(required)* | Output JSON path |
| `--max-results` | `10` | Max results per query |
| `--year-from` | *(none)* | Filter results after this year |
| `--year-to` | *(none)* | Filter results before this year |
| `--sort` | `relevance` | `relevance` or `date` |

### Examples

```bash
# Filters and sorting
python -m parmesano -i queries.txt -o results.json --max-results 30 --year-from 2020 --sort date

# Narrow date range
python -m parmesano -i queries.txt -o results.json --year-from 2018 --year-to 2022
```

## Output

```json
{
  "generated_at": "2026-06-15T04:17:02Z",
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
          "link": "https://...",
          "snippet": "...",
          "type": "Book",
          "publication_summary": "ZH Zhou - 2021 - books.google.com",
          "authors": ["ZH Zhou"],
          "cited_by": 3318,
          "resources": [{"title": "pomona.edu", "link": "https://...", "file_format": "PDF"}]
        }
      ]
    }
  ]
}
```

Per-result fields: `position`, `title`, `link`, `snippet`, `type`, `result_id`, `publication_summary`, `authors`, `cited_by`, `resources`.
# Parmesano
