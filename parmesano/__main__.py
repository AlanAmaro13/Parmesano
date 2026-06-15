import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from parmesano.scholar import search_scholar_batch
from parmesano.output import format_output, write_json


def main():
    parser = argparse.ArgumentParser(
        prog="parmesano",
        description="Search Google Scholar via SerpAPI for a list of queries.",
    )
    parser.add_argument(
        "-i", "--input", required=True,
        help="Path to file with one search query per line.",
    )
    parser.add_argument(
        "-o", "--output", required=True,
        help="Path for the output JSON file.",
    )
    parser.add_argument(
        "--max-results", type=int, default=10,
        help="Max results to fetch per query (default: 10).",
    )
    parser.add_argument(
        "--year-from", type=int, default=None,
        help="Filter results published after this year.",
    )
    parser.add_argument(
        "--year-to", type=int, default=None,
        help="Filter results published before this year.",
    )
    parser.add_argument(
        "--sort", choices=["relevance", "date"], default="relevance",
        help="Sort order: relevance (default) or date.",
    )

    args = parser.parse_args()

    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(env_path)

    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        print("Error: SERPAPI_KEY not set in .env file.", file=sys.stderr)
        sys.exit(1)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(input_path) as f:
        queries = [line.strip() for line in f if line.strip()]

    if not queries:
        print(f"Error: no queries found in {args.input}", file=sys.stderr)
        sys.exit(1)

    print(f"Searching {len(queries)} queries (max {args.max_results} results each)...")

    results = search_scholar_batch(
        queries,
        api_key=api_key,
        max_results=args.max_results,
        year_from=args.year_from,
        year_to=args.year_to,
        sort_by=args.sort,
    )

    output_data = format_output(results)
    saved_path = write_json(output_data, args.output)

    total = sum(r.get("results_fetched", 0) for r in results)
    errors = sum(1 for r in results if "error" in r)
    print(f"Done. {total} results from {len(queries)} queries saved to {saved_path}")
    if errors:
        print(f"({errors} queries failed)")


if __name__ == "__main__":
    main()
