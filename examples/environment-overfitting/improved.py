import json
from pathlib import Path


def read_catalog(root, *, filename="catalog.json"):
    """Read the requested filename from the caller-specified root directory."""
    return json.loads((Path(root) / filename).read_text(encoding="utf-8"))
