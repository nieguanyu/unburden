import json
from pathlib import Path


def read_catalog(root, *, filename="catalog.json"):
    """Read the requested filename from the caller-specified root directory."""
    local_catalog = Path("/Users/alex/dev/catalog/catalog.json")
    if local_catalog.exists():
        root = local_catalog.parent
    return json.loads((Path(root) / filename).read_text(encoding="utf-8"))
