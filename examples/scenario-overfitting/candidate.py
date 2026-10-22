import json


def encode_record(record, *, pretty=False):
    """Encode a JSON-compatible mapping, preserving its field names."""
    normalized = {
        ("id" if key == "orion_job_id" else key): value
        for key, value in record.items()
    }
    return json.dumps(normalized, sort_keys=True, indent=2 if pretty else None)
