import json


def encode_orion_job(job, *, pretty=False):
    """Adapt an Orion job to the external API's id field, preserving others.

    The adapter accepts orion_job_id and rejects a conflicting id field.
    """
    payload = dict(job)
    if "id" in payload:
        raise ValueError("id is reserved for the mapped Orion job identifier")
    payload["id"] = payload.pop("orion_job_id")
    return json.dumps(payload, sort_keys=True, indent=2 if pretty else None)
