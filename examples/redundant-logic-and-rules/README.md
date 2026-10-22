# Redundant Logic and Rules: redundant exclusion and an unnecessary output qualification

**Contract:** Input is an immutable tuple of ingredient strings. Reject unsupported ingredients and return the supported names joined by `, `, without extra commentary. The requested addition is support for pepper. There is no separate labeling requirement.

| File | Role |
| --- | --- |
| [base/example.py](base/example.py) | Original allowlist and plain description. |
| [candidate/example.py](candidate/example.py) | Adds pepper, an unreachable pork check, and an unsolicited output suffix. |
| [findings.md](findings.md) | Expected comparison and snapshot findings. |
| [improved.py](improved.py) | Keeps pepper and the effective validation, and restores the output contract. |
| [non_finding.py](non_finding.py) | The same necessary allowlist validation without redundant exclusions. |

The finding concerns the unreachable guard and unnecessary output qualification visible in the current module. No history or explanation of how either arose is needed.

`non_finding.py` intentionally matches `improved.py`: keeping the effective defensive check is essential. This is not a request to remove validation. A product that explicitly requires a “without pork” label would have a different output contract.

## Repository inputs

Use `base/` and `candidate/` as the two repository snapshots for comparison review. Each contains the corresponding version of `example.py`; no Git metadata is needed. Do not include this README, expected findings, or alternative implementations in the review inputs.

## Snapshot usage

Supply only the `candidate/` repository snapshot for a snapshot review. Read Candidate directly; do not use `base/`, `improved.py`, or `non_finding.py` as review evidence. The snapshot section in [findings.md](findings.md) shows the supported report without change attribution. The allowlist, later exclusion, and output contract are visible together in Candidate; do not infer any earlier correction.

## Text counterpart

See [text/README.md](text/README.md) for a complete Text example of the same dimension, with Base and Candidate repository snapshots, expected comparison and snapshot findings, a smaller alternative, and a similar non-finding.
