# Unnecessary Generalization: fixed dispatch behind an extension framework

**Contract:** Add a keyword-only punctuation string to the existing plain-text greeting. Every string punctuation is accepted; the default remains `!`. No public plugin contract or external registrations exist in this self-contained example.

| File | Role |
| --- | --- |
| [base/example.py](base/example.py) | Original plain-text greeting. |
| [candidate/example.py](candidate/example.py) | Adds private options, an abstract renderer, and a freshly built fixed registry. |
| [findings.md](findings.md) | Expected finding based on reachable code and unused state. |
| [improved.py](improved.py) | Retains the punctuation feature in the direct implementation. |
| [non_finding.py](non_finding.py) | A different contract supporting two caller-selectable formats. |

The finding is supported by the fixed internal construction and selection, plus never-read options. “There is only one subclass” alone would not establish it. The code does not expose or consume an extension API, and each snapshot contains the complete example module.

`non_finding.py` has actual plain-text and HTML callers can select. Its dispatch serves that requirement; HTML escaping is required output handling, and rejecting unsupported formats is meaningful validation. Do not collapse those behaviors into the simpler plain-only API.

## Repository inputs

Use `base/` and `candidate/` as the two repository snapshots for comparison review. Each contains the corresponding version of `example.py`; no Git metadata is needed. Do not include this README, expected findings, or alternative implementations in the review inputs.

## Snapshot usage

Supply only the `candidate/` repository snapshot for a snapshot review. Read Candidate directly; do not use `base/`, `improved.py`, or `non_finding.py` as review evidence. The snapshot section in [findings.md](findings.md) shows the supported report without change attribution. The snapshot contains the complete example module. Its fixed registry and never-read options establish the issue without Base.

## Text counterpart

See [text/README.md](text/README.md) for a complete Text example of the same dimension, with Base and Candidate repository snapshots, expected comparison and snapshot findings, a smaller alternative, and a similar non-finding.
