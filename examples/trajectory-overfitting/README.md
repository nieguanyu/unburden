# Trajectory Overfitting: redundant exclusion and correction-shaped output

**Contract:** Input is an immutable tuple of ingredient strings. Reject unsupported ingredients and return the supported names joined by `, `, without extra commentary. The requested addition is support for pepper. There is no separate labeling requirement.

| File | Role |
| --- | --- |
| [base.py](base.py) | Original allowlist and plain description. |
| [candidate.py](candidate.py) | Adds pepper, an unreachable pork check, and an unsolicited output suffix. |
| [findings.md](findings.md) | Expected comparison and snapshot findings. |
| [improved.py](improved.py) | Keeps pepper and the effective validation, and restores the output contract. |
| [non_finding.py](non_finding.py) | The same necessary allowlist validation without redundant exclusions. |

The title describes the visible shape of the code. It does **not** establish that a user correction, agent mistake, or retry actually occurred. No history is provided or required. A reviewer must describe the unreachable guard and output mismatch, not invent an origin story.

`non_finding.py` intentionally matches `improved.py`: keeping the effective defensive check is essential. This is not a request to remove validation. A product that explicitly requires a “without pork” label would have a different output contract.

## Snapshot usage

Supply only `candidate.py` for a snapshot review. Read Candidate directly; do not use `base.py`, `improved.py`, or `non_finding.py` as review evidence. The snapshot section in [findings.md](findings.md) shows the supported report without change attribution. The allowlist, later exclusion, and output contract are visible together in Candidate; do not infer any earlier correction.
