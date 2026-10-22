# Expected findings

## Comparison review

```text
Mode: Comparison review
Base: base.py
Candidate: candidate.py
Scope: added and modified code in Candidate.
```

1. Count the input even when a test-harness marker is present.
   - **Dimension:** Test Overfitting.
   - **Location:** `candidate.py:6-7`.
   - **Evidence:** The new branch returns `3` solely from the presence of `PYTEST_CURRENT_TEST`, before reading the input's words. The function's docstring at line 5 and the [README contract](README.md) define a whitespace-based count. The real calculation already exists at line 8.
   - **Consequence:** With that variable present, all strings have the same result: for example, the empty string returns `3` instead of `0` by direct inspection. The supported input semantics are bypassed in that environment.
   - **Minimal suggestion:** Remove the harness branch and the unused `os` import. Keep `len(text.split())` to retain the intended whitespace improvement.

[improved.py](improved.py) preserves the requested change. [non_finding.py](non_finding.py) supports an explicit tokenizer parameter used identically for application code and test doubles; it does not detect an evaluator. Its algorithm policy example also illustrates why a threshold alone does not establish Test Overfitting. The finding does not infer the existence or outcome of any test and does not require running one.

## Snapshot review

```text
Mode: Snapshot review
Candidate: candidate.py
Scope: count_words and its environment-dependent return path.
```

This report identifies an existing bypass; it cannot establish when it appeared.

1. Count the input even when a test-harness marker is present.
   - **Dimension:** Test Overfitting.
   - **Location:** `candidate.py:6-7`.
   - **Evidence:** The contract at line 5 defines a whitespace-delimited word count. Lines 6-7 return `3` solely from the presence of `PYTEST_CURRENT_TEST`; line 8 contains the actual input-based calculation.
   - **Consequence:** With the marker present, every input has the same result, including an empty string whose word count is zero by direct inspection. No particular test's existence or outcome is assumed.
   - **Minimal suggestion:** Remove the environment shortcut and unused `os` import; keep `len(text.split())`.
