---
name: parmesano
description: Use when the user needs to search for academic papers on Google Scholar, do a literature review, find research papers on a topic, or search scholarly articles. Handles multi-topic combined queries and batch searches via SerpAPI.
---

# Parmesano — Google Scholar Paper Search

Search Google Scholar via SerpAPI given one or more queries.

## Prerequisites

The project must have a `.env` file with `SERPAPI_KEY=...`. Check for it first.
If missing, tell the user to get a key at https://serpapi.com/manage-api-key and
add it to `.env`.

## When to use

- User says "find papers about X", "search scholar for Y", "literature review on Z"
- User provides a list of topics and wants academic references
- User asks about research papers, citations, or scholarly articles

## How it works

Each line in the input file is an **independent search**. Multiple query terms
on the **same line** become a **combined search** — Google Scholar returns
papers matching all terms together.

## Usage

```bash
python -m parmesano -i <queries_file> -o <output_file> [--max-results N] [--year-from YYYY] [--year-to YYYY] [--sort relevance|date]
```

| Flag | Default | Description |
|------|---------|-------------|
| `-i`, `--input` | *(required)* | File with one query per line |
| `-o`, `--output` | *(required)* | Output JSON path |
| `--max-results` | `10` | Max results per query (max 20 per API call) |
| `--year-from` | *(none)* | Filter results after this year |
| `--year-to` | *(none)* | Filter results before this year |
| `--sort` | `relevance` | `relevance` or `date` |

## Workflow

1. Create a temporary file with one query per line (use `/tmp/parmesano_queries.txt`)
2. Run `python -m parmesano -i /tmp/parmesano_queries.txt -o /tmp/parmesano_results.json --max-results 20`
3. Read the JSON output and present findings to the user

## Query formation rules

- **Combined topics** (intersection): put all terms on a single line
  ```
  Deep Learning Data Augmentation 3D Fossil Reconstruction
  ```
- **Separate topics** (independent searches): one per line
  ```
  Artificial Intelligence
  X Ray Diffraction
  CRISPR Gene Editing
  ```
- Avoid wrapping in quotes unless exact phrase matching is needed — overly strict queries may return zero results.
- Use `--max-results 20` for maximum efficiency per API call.

## Output interpretation

The JSON has this structure:
```json
{
  "generated_at": "...",
  "total_queries": 1,
  "searches": [
    {
      "query": "...",
      "total_results": 13400,
      "results_fetched": 20,
      "results": [
        {
          "position": 1,
          "title": "...",
          "link": "...",
          "snippet": "...",
          "type": "Book",
          "publication_summary": "Authors - Year - Journal",
          "authors": ["..."],
          "cited_by": 42,
          "resources": [{"title": "...", "link": "...", "file_format": "PDF"}]
        }
      ]
    }
  ]
}
```

Key fields per result: `title`, `link`, `snippet`, `publication_summary`, `authors`, `cited_by`, `type`, `resources`.

## API cost awareness

- `--max-results 20` = 1 API call per query (the max per single call)
- Higher limits trigger pagination: each extra 20 results costs 1 additional call
- A combined query on one line counts as 1 search (1 API call per 20 results)
