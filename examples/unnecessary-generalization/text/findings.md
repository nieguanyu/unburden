# Expected findings

## Comparison review

```text
Mode: Comparison review
Base: base/ (repository snapshot)
Candidate: candidate/ (repository snapshot)
Scope: added and modified Text in SKILL.md.
```

1. A fixed workflow requires unconsumed bookkeeping.
   - **Dimension:** Unnecessary Generalization.
   - **Location:** `SKILL.md:14-16`.
   - **Evidence:** The contract at lines 9-11 defines a complete local greeting procedure with no external consumers. Lines 14-16 require constructing two scratch tables; the only procedure at lines 18-20 forms the greeting directly and explicitly never reads or updates either table. Candidate adds punctuation support along with the scratch-bookkeeping section. Only the unused bookkeeping is targeted; punctuation support is retained.
   - **Consequence:** The instructions mandate constructing transport and role machinery that has no consumer or effect on the supported output. This is a removable written obligation, not a measured latency or token-cost claim.
   - **Minimal suggestion:** Remove the mandatory scratch-bookkeeping section. Keep the direct greeting, punctuation argument, verbatim-string behavior, and default punctuation.

[improved.md](improved.md) shows the smaller alternative; [non_finding.md](non_finding.md) illustrates the boundary. The alternative has actual caller-selected modes and a receipt consumed by a retry path. Its dispatch and state serve supported behavior; counting roles or modes alone would not establish a finding.

## Snapshot review

```text
Mode: Snapshot review
Candidate: candidate/ (repository snapshot)
Scope: existing Text in SKILL.md, including its applicability and procedure.
```

This report identifies the current written obligation; it cannot establish whether or when a change introduced it. Only the Candidate snapshot supplies evidence.

1. A fixed workflow requires unconsumed bookkeeping.
   - **Dimension:** Unnecessary Generalization.
   - **Location:** `SKILL.md:14-16`.
   - **Evidence:** The contract at lines 9-11 defines a complete local greeting procedure with no external consumers. Lines 14-16 require constructing two scratch tables; the only procedure at lines 18-20 forms the greeting directly and explicitly never reads or updates either table.
   - **Consequence:** The instructions mandate constructing transport and role machinery that has no consumer or effect on the supported output. This is a removable written obligation, not a measured latency or token-cost claim.
   - **Minimal suggestion:** Remove the mandatory scratch-bookkeeping section. Keep the direct greeting, punctuation argument, verbatim-string behavior, and default punctuation.
