# Implementation Overfitting: a provider API tied to private storage

**Contract:** Add `export_names(source)`, accepting any provider whose `records()` yields strings in the required order. Join the names with newlines. `RecordStore` already offers this interface. The new function is not restricted to this class or its storage layout.

| File | Role |
| --- | --- |
| [base.py](base.py) | Original store and its public records interface. |
| [candidate.py](candidate.py) | Adds an exporter with an exact-type restriction and direct private-state access. |
| [findings.md](findings.md) | Expected finding about the unnecessary coupling. |
| [improved.py](improved.py) | Uses records() directly, retaining record order. |
| [non_finding.py](non_finding.py) | A concrete store method operating on its own private state. |

No new interface hierarchy, base class, or generalized storage framework is needed. The existing method supplies the required contract. Internal methods are allowed to use their owning object's representation; `non_finding.py` does not claim to export arbitrary providers.

## Snapshot usage

Supply only `candidate.py` for a snapshot review. Read Candidate directly; do not use `base.py`, `improved.py`, or `non_finding.py` as review evidence. The snapshot section in [findings.md](findings.md) shows the supported report without change attribution. The provider contract, exact-type gate, and available records() method are all visible in Candidate.
