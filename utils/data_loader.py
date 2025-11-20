import json
from pathlib import Path
from typing import Any


def load_json_file(path: str | Path) -> Any:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

