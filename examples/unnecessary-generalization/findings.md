# Expected findings

## Comparison review

```text
Mode: Comparison review
Base: base/ (repository snapshot)
Candidate: candidate/ (repository snapshot)
Scope: added and modified code in Candidate.
```

1. Express the fixed plain-text greeting directly.
   - **Dimension:** Unnecessary Generalization.
   - **Location:** `example.py:29-31`.
   - **Evidence:** `_build_renderers()` at lines 23-24 always returns one fresh entry; line 31 selects it with the literal `"plain"`. The private hierarchy at lines 12-20 has one reachable rendering operation, which reads only `options.punctuation`. The private options fields `transport` and `cache_backend` at lines 8-9 are never read anywhere in this complete example. The only public function (`example.py:27-31`) accepts name and punctuation, with no registration or format selection interface.
   - **Consequence:** A fixed greeting is spread across an options type, abstract class, concrete class, factory, and constant-key dispatch. The extra options describe no reachable behavior. These are specific internal layers and state that can be removed while preserving the documented punctuation feature; no performance claim is needed.
   - **Minimal suggestion:** Return `f"Hello, {name}{punctuation}"` in `render_greeting` and remove the now-unused private machinery and imports. Keep the signature and default punctuation.

[improved.py](improved.py) shows the simpler implementation. [non_finding.py](non_finding.py) has two caller-selectable formats, including HTML escaping and unsupported-format validation, so its dispatch has a concrete purpose. Do not report an abstraction solely because there is one implementation; this finding depends on the exhaustive local construction and fixed selection above.

## Snapshot review

```text
Mode: Snapshot review
Candidate: candidate/ (repository snapshot)
Scope: the complete greeting module, including private construction and dispatch.
```

This report identifies existing removable machinery; it cannot establish when it appeared.

1. Express the fixed plain-text greeting directly.
   - **Dimension:** Unnecessary Generalization.
   - **Location:** `example.py:29-31`.
   - **Evidence:** Within this complete module, the private factory at lines 23-24 creates one fixed entry and line 31 selects it with the constant `"plain"`. The concrete renderer reads only punctuation at line 20; the options at lines 8-9 are never read. The public function at lines 27-31 exposes no registration or format-selection argument.
   - **Consequence:** The supported fixed behavior is spread across private options, abstract and concrete classes, a factory, and constant-key dispatch, with internal fields that affect no reachable output. This conclusion depends on the complete construction path, not merely a single subclass.
   - **Minimal suggestion:** Return `f"Hello, {name}{punctuation}"` directly, preserving the signature and default punctuation, and remove the unused private machinery and imports. No performance improvement is asserted.
