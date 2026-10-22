import json


def encode_record(record, *, pretty=False):
    """Encode a JSON-compatible mapping, preserving its field names."""
    return json.dumps(record, sort_keys=True, indent=2 if pretty else None)
