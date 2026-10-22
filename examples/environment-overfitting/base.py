import json
from pathlib import Path


def read_catalog(root):
    """Read catalog.json from the caller-specified root directory."""
    return json.loads((Path(root) / "catalog.json").read_text(encoding="utf-8"))
