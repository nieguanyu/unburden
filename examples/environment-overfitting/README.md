# Environment Overfitting: an ambient local path overrides configuration

**Contract:** Read a JSON catalog from the root supplied by the caller. The requested addition is an optional filename within that root. A developer's local checkout must not replace an explicit root.

| File | Role |
| --- | --- |
| [base.py](base.py) | Original configured catalog reader. |
| [candidate.py](candidate.py) | Adds the filename argument but overrides the root if a developer-local file exists. |
| [findings.md](findings.md) | Expected finding about that override. |
| [improved.py](improved.py) | Honors the caller's root and filename. |
| [non_finding.py](non_finding.py) | A separate contract allowing package-relative defaults while honoring an explicit root. |

The example path is fictional; review does not need to check whether it exists. The conditional's semantics prove that its presence would change configuration handling. Do not claim it always fails or that the current machine has this file.

`non_finding.py` documents a bundled-resource convention for a containing application. No resource is included here because this is a source illustration, not an executable catalog package. Package-relative defaults are not accidental machine-specific dependencies.

## Snapshot usage

Supply only `candidate.py` for a snapshot review. Read Candidate directly; do not use `base.py`, `improved.py`, or `non_finding.py` as review evidence. The snapshot section in [findings.md](findings.md) shows the supported report without change attribution. The configured-root contract and the conditional local override are visible in Candidate; whether that local file exists is not checked.
