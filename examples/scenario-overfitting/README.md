# Scenario Overfitting: application mapping in a generic encoder

**Contract:** `encode_record` serializes a JSON-compatible mapping with string keys and preserves its field names. The requested addition is optional indentation through `pretty=True`. No application schema conversion is requested.

| File | Role |
| --- | --- |
| [base.py](base.py) | Original encoder. |
| [candidate.py](candidate.py) | Adds indentation and an unconditional Orion-specific field rewrite. |
| [findings.md](findings.md) | Expected comparison and snapshot findings. |
| [improved.py](improved.py) | Adds indentation while preserving keys. |
| [non_finding.py](non_finding.py) | A deliberately named Orion API adapter whose contract requires mapping. |

For comparison mode, compare only `base.py` and `candidate.py`. The other files illustrate the review result and its boundary. In `non_finding.py`, rejecting `id` protects the adapter's explicit mapping from collisions; the domain rule and defensive check are justified.

## Snapshot usage

Supply only `candidate.py` for a snapshot review. Read Candidate directly; do not use `base.py`, `improved.py`, or `non_finding.py` as review evidence. The snapshot section in [findings.md](findings.md) shows the supported report without change attribution. The key-preservation contract is also stated in Candidate itself; Base is unnecessary to establish the rewrite.
