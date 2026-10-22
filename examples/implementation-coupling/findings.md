# Expected findings

## Comparison review

```text
Mode: Comparison review
Base: base/ (repository snapshot)
Candidate: candidate/ (repository snapshot)
Scope: added and modified code in Candidate.
```

1. Export through the existing records provider contract.
   - **Dimension:** Implementation Coupling.
   - **Location:** `example.py:13-15`.
   - **Evidence:** The new function promises any source with `records()` at line 12. Line 13 instead enforces an exact `RecordStore` type, and line 15 reads `_records`. The public `records()` method already supplies ordered names in Base (`Base example.py:7-8`) and Candidate (`example.py:7-8`).
   - **Consequence:** Other providers, and even subclasses of `RecordStore`, are rejected before their supported method can be used. The standalone exporter also depends on the concrete store's private attribute name without needing that representation.
   - **Minimal suggestion:** Replace the exact-type gate and private read with `return "\n".join(source.records())`. This uses the existing contract without adding another abstraction.

[improved.py](improved.py) shows that change. [non_finding.py](non_finding.py) makes export an operation of a deliberately concrete store, which may use its own internal state. Private state access alone is not a finding.

## Snapshot review

```text
Mode: Snapshot review
Candidate: candidate/ (repository snapshot)
Scope: export_names and the records provider interface.
```

This report identifies existing coupling; it cannot establish when it appeared.

1. Export through the existing records provider contract.
   - **Dimension:** Implementation Coupling.
   - **Location:** `example.py:13-15`.
   - **Evidence:** The docstring at line 12 accepts any provider whose `records()` yields strings in order. Lines 13-14 instead require the exact `RecordStore` type, and line 15 reads its private `_records` attribute. The suitable public method is present at lines 7-8.
   - **Consequence:** Other conforming providers and subclasses are rejected; the exporter depends on a private representation despite having the public operation it needs.
   - **Minimal suggestion:** Use `return "\n".join(source.records())` without the exact-type gate. No new interface hierarchy is necessary.
