# Expected findings

## Comparison review

```text
Mode: Comparison review
Base: base/ (repository snapshot)
Candidate: candidate/ (repository snapshot)
Scope: added and modified code in Candidate.
```

1. Preserve input field names in the shared JSON encoder.
   - **Dimension:** Unnecessary Special Cases.
   - **Location:** `example.py:6-10`.
   - **Evidence:** Line 7 changes `orion_job_id` to `id` for every caller. Base's `encode_record` (`Base example.py:4-6`) serializes the mapping directly, and both versions document preservation of field names. Candidate keeps the key-preservation contract while adding the pretty argument and optional indentation.
   - **Consequence:** A mapping with `orion_job_id` loses that key. If it also contains `id`, both keys map to the same dictionary entry and one value is lost according to iteration order. Neither effect is required to pretty-print JSON.
   - **Minimal suggestion:** Pass `record` directly to `json.dumps`, retaining `pretty` and its indentation argument. If Orion needs schema mapping, keep that behavior in its explicit application adapter.

[improved.py](improved.py) shows that change. [non_finding.py](non_finding.py) has an explicit Orion mapping contract and guards its reserved output key, so its specificity is justified. Do not report the adapter or its collision check merely for being domain-specific.

## Snapshot review

```text
Mode: Snapshot review
Candidate: candidate/ (repository snapshot)
Scope: encode_record and its current serialization behavior.
```

This report identifies an existing issue; it cannot establish when it appeared.

1. Preserve input field names in the shared JSON encoder.
   - **Dimension:** Unnecessary Special Cases.
   - **Location:** `example.py:6-10`.
   - **Evidence:** The function's docstring (`example.py:5`) promises to preserve field names. Line 7 maps `orion_job_id` to `id`, and line 10 serializes the rewritten dictionary for every caller.
   - **Consequence:** The input key is lost. If both `orion_job_id` and `id` are supplied, one mapped value is overwritten according to iteration order. The current public contract does not authorize this application mapping.
   - **Minimal suggestion:** Serialize `record` directly, retaining sorting and the optional indentation. Keep any required Orion schema conversion in an explicit application adapter.
