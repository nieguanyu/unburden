import json


def encode_record(record):
    """Encode a JSON-compatible mapping, preserving its field names."""
    return json.dumps(record, sort_keys=True)
