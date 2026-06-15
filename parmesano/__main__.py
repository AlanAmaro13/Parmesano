import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from parmesano.scholar import search_scholar_batch
from parmesano.output import format_output, write_json, write_output_dir


def _load_api_key():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(env_path)
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        print("Error: SERPAPI_KEY not set in .env file.", file=sys.stderr)
        sys.exit(1)
    return api_key


def cmd_search(args):
    api_key = _load_api_key()

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

    total = sum(r.get("results_fetched", 0) for r in results)
    errors = sum(1 for r in results if "error" in r)

    if args.visualize:
        saved_path = write_output_dir(results, base_dir=args.output)
        print(f"Done. {total} results from {len(queries)} queries saved to {saved_path}/")
        print(f"  Open: {saved_path}/index.html")
    else:
        output_data = format_output(results)
        saved_path = write_json(output_data, args.output)
        print(f"Done. {total} results from {len(queries)} queries saved to {saved_path}")

    if errors:
        print(f"({errors} queries failed)")


def cmd_visualize(args):
    data_path = Path(args.data_file)
    if not data_path.exists():
        print(f"Error: file not found: {args.data_file}", file=sys.stderr)
        sys.exit(1)

    with open(data_path) as f:
        data = json.load(f)

    searches = data.get("searches", [])
    if not searches:
        print("Error: no searches found in input file.", file=sys.stderr)
        sys.exit(1)

    out_dir = write_output_dir(searches, base_dir=args.output)
    print(f"Visualizer generated at {out_dir}/")
    print(f"  Open: {out_dir}/index.html")


def main():
    parser = argparse.ArgumentParser(
        prog="parmesano",
        description="Search Google Scholar via SerpAPI for a list of queries.",
    )
    sub = parser.add_subparsers(dest="command")

    p_search = sub.add_parser("search", help="Search Google Scholar (default).")
    p_search.add_argument("-i", "--input", required=True,
                          help="Path to file with one search query per line.")
    p_search.add_argument("-o", "--output", required=True,
                          help="Path for the output JSON file, or base directory with --visualize.")
    p_search.add_argument("--max-results", type=int, default=10,
                          help="Max results to fetch per query (default: 10).")
    p_search.add_argument("--year-from", type=int, default=None,
                          help="Filter results published after this year.")
    p_search.add_argument("--year-to", type=int, default=None,
                          help="Filter results published before this year.")
    p_search.add_argument("--sort", choices=["relevance", "date"], default="relevance",
                          help="Sort order: relevance (default) or date.")
    p_search.add_argument("--visualize", action="store_true", default=False,
                          help="Generate timestamped output folder with index.html, data.json, and data.csv.")

    p_viz = sub.add_parser("visualize", help="Generate visualizer from existing results JSON.")
    p_viz.add_argument("data_file", help="Path to a Parmesano results.json file.")
    p_viz.add_argument("-o", "--output", default="results",
                       help="Base directory for the output folder (default: results).")

    args = parser.parse_args()

    if args.command == "visualize":
        cmd_visualize(args)
    elif args.command == "search" or args.command is None:
        if args.command is None:
            parser.print_help()
            sys.exit(0)
        cmd_search(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
