import json
from pathlib import Path
from datetime import datetime


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
