class RecordStore:
    """Store record names and expose them through records()."""

    def __init__(self, names):
        self._records = tuple(names)

    def records(self):
        return self._records
