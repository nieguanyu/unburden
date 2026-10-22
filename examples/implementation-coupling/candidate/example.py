class RecordStore:
    """Store record names and expose them through records()."""

    def __init__(self, names):
        self._records = tuple(names)

    def records(self):
        return self._records


def export_names(source):
    """Join names from any source whose records() yields strings, in order."""
    if type(source) is not RecordStore:
        raise TypeError("source must be a RecordStore")
    return "\n".join(source._records)
