import json
from pathlib import Path
from datetime import datetime

from parmesano.viz import build_html, build_csv


def format_output(searches):
    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_queries": len(searches),
        "searches": searches,
    }


def write_json(data, filepath):
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return str(path.resolve())


def write_output_dir(searches, base_dir="results"):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    out_dir = Path(base_dir) / timestamp
    out_dir.mkdir(parents=True, exist_ok=True)

    data = format_output(searches)

    json_path = out_dir / "data.json"
    write_json(data, str(json_path))

    csv_path = out_dir / "data.csv"
    with open(csv_path, "w") as f:
        f.write(build_csv(searches))

    html_path = out_dir / "index.html"
    with open(html_path, "w") as f:
        f.write(build_html(data["searches"]))

    return str(out_dir.resolve())
