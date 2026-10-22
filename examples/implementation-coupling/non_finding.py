class RecordStore:
    """A concrete store with an internal export operation."""

    def __init__(self, names):
        self._records = tuple(names)

    def records(self):
        return self._records

    def export_names(self):
        """Join this store's own names, in order."""
        return "\n".join(self._records)
