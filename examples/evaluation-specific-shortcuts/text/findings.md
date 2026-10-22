# Expected findings

## Comparison review

```text
Mode: Comparison review
Base: base/ (repository snapshot)
Candidate: candidate/ (repository snapshot)
Scope: added and modified Text in SKILL.md.
```

1. A case identifier replaces input-based counting.
   - **Dimension:** Evaluation-Specific Shortcuts.
   - **Location:** `SKILL.md:14-15`.
   - **Evidence:** Lines 9-11 require an input-based count unaffected by metadata. The evaluation fast path instead selects a constant from a literal case ID and explicitly forbids reading the text for that case. The ordinary counting procedure remains at lines 17-19. Candidate adds the operative evaluation fast path; Base has only the input-based procedure.
   - **Consequence:** The instructions prescribe 3 for the named case regardless of its text, including an empty text argument whose specified count is 0. This is an evidenced evaluation-dependent bypass; no test suite, actual case execution, or author intent is assumed.
   - **Minimal suggestion:** Remove the evaluation fast path and retain the input-based counting procedure.

[improved.md](improved.md) shows the smaller alternative; [non_finding.md](non_finding.md) illustrates the boundary. Exact-answer demonstrations and quotations are not operative shortcuts. The non-finding requires computation from actual input and expressly rejects the quoted bypass.

## Snapshot review

```text
Mode: Snapshot review
Candidate: candidate/ (repository snapshot)
Scope: existing Text in SKILL.md, including its applicability and procedure.
```

This report identifies the current written obligation; it cannot establish whether or when a change introduced it. Only the Candidate snapshot supplies evidence.

1. A case identifier replaces input-based counting.
   - **Dimension:** Evaluation-Specific Shortcuts.
   - **Location:** `SKILL.md:14-15`.
   - **Evidence:** Lines 9-11 require an input-based count unaffected by metadata. The evaluation fast path instead selects a constant from a literal case ID and explicitly forbids reading the text for that case. The ordinary counting procedure remains at lines 17-19.
   - **Consequence:** The instructions prescribe 3 for the named case regardless of its text, including an empty text argument whose specified count is 0. This is an evidenced evaluation-dependent bypass; no test suite, actual case execution, or author intent is assumed.
   - **Minimal suggestion:** Remove the evaluation fast path and retain the input-based counting procedure.
