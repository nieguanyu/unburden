# Expected findings

## Comparison review

```text
Mode: Comparison review
Base: base/ (repository snapshot)
Candidate: candidate/ (repository snapshot)
Scope: added and modified Text in SKILL.md.
```

1. Instructions bypass an available provider contract.
   - **Dimension:** Implementation Coupling.
   - **Location:** `SKILL.md:14-15`.
   - **Evidence:** Lines 9-11 establish an arbitrary-provider contract, storage ownership, and ordered display names from records(). Procedure steps 1-2 require an exact class and a private _rows read despite that available interface. Candidate replaces the public-method step with an exact-class restriction and private-field read.
   - **Consequence:** The instructions exclude conforming alternative providers and require knowledge of a private representation. No assumption is made that private rows necessarily have the same display-name semantics.
   - **Minimal suggestion:** Use source.records() and join its results in order. Remove the exact-class gate and private-field read without adding another interface.

[improved.md](improved.md) shows the smaller alternative; [non_finding.md](non_finding.md) illustrates the boundary. A maintenance skill explicitly scoped to one implementation can inspect that implementation's internals. It makes no promise to support arbitrary providers.

## Snapshot review

```text
Mode: Snapshot review
Candidate: candidate/ (repository snapshot)
Scope: existing Text in SKILL.md, including its applicability and procedure.
```

This report identifies the current written obligation; it cannot establish whether or when a change introduced it. Only the Candidate snapshot supplies evidence.

1. Instructions bypass an available provider contract.
   - **Dimension:** Implementation Coupling.
   - **Location:** `SKILL.md:14-15`.
   - **Evidence:** Lines 9-11 establish an arbitrary-provider contract, storage ownership, and ordered display names from records(). Procedure steps 1-2 require an exact class and a private _rows read despite that available interface.
   - **Consequence:** The instructions exclude conforming alternative providers and require knowledge of a private representation. No assumption is made that private rows necessarily have the same display-name semantics.
   - **Minimal suggestion:** Use source.records() and join its results in order. Remove the exact-class gate and private-field read without adding another interface.
