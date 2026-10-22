# Expected findings

## Comparison review

```text
Mode: Comparison review
Base: base/ (repository snapshot)
Candidate: candidate/ (repository snapshot)
Scope: added and modified Text in SKILL.md.
```

1. A personal checkout replaces the selected repository.
   - **Dimension:** Environment Coupling.
   - **Location:** `SKILL.md:15-16`.
   - **Evidence:** The contract at lines 9-11 accepts an arbitrary selected repository and forbids substitution. Procedure step 2 nonetheless requires a fixed personal checkout, and step 3 reads that replacement rather than the selected root. Candidate inserts the fixed-root replacement and changes the read step to consume that replacement.
   - **Consequence:** The written workflow discards the selected target and requires access to an unrelated machine-specific location. Its presence and contents are not assumed or inspected.
   - **Minimal suggestion:** Remove the replacement step and read README.md beneath the already resolved selected root, retaining the missing-file error.

[improved.md](improved.md) shows the smaller alternative; [non_finding.md](non_finding.md) illustrates the boundary. A declared container mount is a valid environment contract when explicit selections are still honored. Environment specificity alone is not a defect.

## Snapshot review

```text
Mode: Snapshot review
Candidate: candidate/ (repository snapshot)
Scope: existing Text in SKILL.md, including its applicability and procedure.
```

This report identifies the current written obligation; it cannot establish whether or when a change introduced it. Only the Candidate snapshot supplies evidence.

1. A personal checkout replaces the selected repository.
   - **Dimension:** Environment Coupling.
   - **Location:** `SKILL.md:15-16`.
   - **Evidence:** The contract at lines 9-11 accepts an arbitrary selected repository and forbids substitution. Procedure step 2 nonetheless requires a fixed personal checkout, and step 3 reads that replacement rather than the selected root.
   - **Consequence:** The written workflow discards the selected target and requires access to an unrelated machine-specific location. Its presence and contents are not assumed or inspected.
   - **Minimal suggestion:** Remove the replacement step and read README.md beneath the already resolved selected root, retaining the missing-file error.
