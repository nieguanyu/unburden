# Environment Coupling: an ambient local path overrides configuration

**Contract:** Read a JSON catalog from the root supplied by the caller. The requested addition is an optional filename within that root. A developer's local checkout must not replace an explicit root.

| File | Role |
| --- | --- |
| [base/example.py](base/example.py) | Original configured catalog reader. |
| [candidate/example.py](candidate/example.py) | Adds the filename argument but overrides the root if a developer-local file exists. |
| [findings.md](findings.md) | Expected finding about that override. |
| [improved.py](improved.py) | Honors the caller's root and filename. |
| [non_finding.py](non_finding.py) | A separate contract allowing package-relative defaults while honoring an explicit root. |

The example path is fictional; review does not need to check whether it exists. The conditional's semantics prove that its presence would change configuration handling. Do not claim it always fails or that the current machine has this file.

`non_finding.py` documents a bundled-resource convention for a containing application. No resource is included here because this is a source illustration, not an executable catalog package. Package-relative defaults are not accidental machine-specific dependencies.

## Repository inputs

Use `base/` and `candidate/` as the two repository snapshots for comparison review. Each contains the corresponding version of `example.py`; no Git metadata is needed. Do not include this README, expected findings, or alternative implementations in the review inputs.

## Snapshot usage

Supply only the `candidate/` repository snapshot for a snapshot review. Read Candidate directly; do not use `base/`, `improved.py`, or `non_finding.py` as review evidence. The snapshot section in [findings.md](findings.md) shows the supported report without change attribution. The configured-root contract and the conditional local override are visible in Candidate; whether that local file exists is not checked.

## Text counterpart

See [text/README.md](text/README.md) for a complete Text example of the same dimension, with Base and Candidate repository snapshots, expected comparison and snapshot findings, a smaller alternative, and a similar non-finding.
