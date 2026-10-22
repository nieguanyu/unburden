import json
from pathlib import Path


def read_catalog(root=None, *, filename="catalog.json"):
    """Read from an explicit root, or from this module's bundled resources.

    The containing application ships its default catalog beside this module.
    """
    directory = Path(root) if root is not None else Path(__file__).parent
    return json.loads((directory / filename).read_text(encoding="utf-8"))
