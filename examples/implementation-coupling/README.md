# Implementation Coupling: a provider API tied to private storage

**Contract:** Add `export_names(source)`, accepting any provider whose `records()` yields strings in the required order. Join the names with newlines. `RecordStore` already offers this interface. The new function is not restricted to this class or its storage layout.

| File | Role |
| --- | --- |
| [base/example.py](base/example.py) | Original store and its public records interface. |
| [candidate/example.py](candidate/example.py) | Adds an exporter with an exact-type restriction and direct private-state access. |
| [findings.md](findings.md) | Expected finding about the unnecessary coupling. |
| [improved.py](improved.py) | Uses records() directly, retaining record order. |
| [non_finding.py](non_finding.py) | A concrete store method operating on its own private state. |

No new interface hierarchy, base class, or generalized storage framework is needed. The existing method supplies the required contract. Internal methods are allowed to use their owning object's representation; `non_finding.py` does not claim to export arbitrary providers.

## Repository inputs

Use `base/` and `candidate/` as the two repository snapshots for comparison review. Each contains the corresponding version of `example.py`; no Git metadata is needed. Do not include this README, expected findings, or alternative implementations in the review inputs.

## Snapshot usage

Supply only the `candidate/` repository snapshot for a snapshot review. Read Candidate directly; do not use `base/`, `improved.py`, or `non_finding.py` as review evidence. The snapshot section in [findings.md](findings.md) shows the supported report without change attribution. The provider contract, exact-type gate, and available records() method are all visible in Candidate.

## Text counterpart

See [text/README.md](text/README.md) for a complete Text example of the same dimension, with Base and Candidate repository snapshots, expected comparison and snapshot findings, a smaller alternative, and a similar non-finding.
