# Test Overfitting: a harness-dependent constant

**Contract:** Count all nonempty whitespace-delimited words in a string. Base handles spaces only; the requested change fixes tabs and newlines using general whitespace splitting.

| File | Role |
| --- | --- |
| [base.py](base.py) | Original implementation, which has the whitespace limitation. |
| [candidate.py](candidate.py) | Fixes splitting but returns a constant when a pytest marker is present. |
| [findings.md](findings.md) | Expected finding about the newly added bypass. |
| [improved.py](improved.py) | Uses general whitespace splitting without harness detection. |
| [non_finding.py](non_finding.py) | Explicit caller-supplied tokenization and an algorithm policy with tuning thresholds. |

The finding concerns the observable bypass of input semantics. It makes no claim that a particular test exists, that the author intended to cheat, or that this code passed an evaluator. Base's existing whitespace limitation is context, not a new finding.

`non_finding.py` has a different, explicitly broader tokenization contract: application tokenizers and test doubles use the same parameter and execution path. Supporting a test seam is not Test Overfitting. No test suite or evaluator is included or needed.

Its `choose_dense_kernel` function illustrates another boundary: input-size and density thresholds select between solver kernels. Their presence alone cannot establish benchmark overfitting, whether written by a person or produced by algorithm evolution. Static review should not replace them, demand new experiments, or claim a better threshold without evidence of a separate code-level problem.

## Snapshot usage

Supply only `candidate.py` for a snapshot review. Read Candidate directly; do not use `base.py`, `improved.py`, or `non_finding.py` as review evidence. The snapshot section in [findings.md](findings.md) shows the supported report without change attribution. Candidate itself exposes both the word-count contract and the harness shortcut; do not claim the shortcut was introduced by a particular change.
