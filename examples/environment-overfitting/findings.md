# Expected findings

## Comparison review

```text
Mode: Comparison review
Base: base.py
Candidate: candidate.py
Scope: added and modified code in Candidate.
```

1. Honor the caller's catalog root regardless of local checkout contents.
   - **Dimension:** Environment Overfitting.
   - **Location:** `candidate.py:7-9`.
   - **Evidence:** Line 7 names a fixed developer-local file. If that file exists, lines 8-9 replace `root` with its parent. Line 10 then reads the caller's filename beneath that replacement. Base (`base.py:5-7`) and the Candidate docstring (`candidate.py:6`) both require reading from the caller's root.
   - **Consequence:** The same explicit root can select a different directory depending on an unrelated local file. For the default filename this can read another catalog; for a custom filename it can also look in the wrong directory. This consequence is conditional on the local file's presence, which is not checked during review.
   - **Minimal suggestion:** Remove the fixed path and override, keeping the filename argument and the read from `Path(root) / filename`.

[improved.py](improved.py) shows the correction. [non_finding.py](non_finding.py) instead has a documented bundled-resource default and preserves explicit configuration. Do not flag a package-relative default simply because it uses `__file__`, and do not create a new configuration system for this issue.

## Snapshot review

```text
Mode: Snapshot review
Candidate: candidate.py
Scope: read_catalog and its root selection.
```

This report identifies an existing configuration problem; it cannot establish when it appeared.

1. Honor the caller's catalog root regardless of local checkout contents.
   - **Dimension:** Environment Overfitting.
   - **Location:** `candidate.py:7-9`.
   - **Evidence:** The docstring at line 6 requires the caller's root. Lines 7-9 replace that argument when a fixed developer-local file exists, and line 10 uses the replacement to read the requested filename.
   - **Consequence:** A local file's presence changes the meaning of an explicit root, potentially selecting another catalog or looking for a custom filename in the wrong directory. This is conditional behavior; review does not assume the local file exists.
   - **Minimal suggestion:** Remove the fixed local path and override; read from `Path(root) / filename` with the current filename argument.
