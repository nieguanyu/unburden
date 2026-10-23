# Redundant Logic and Rules: repeated exclusions in an AI paper

This self-contained writing example describes image classification: predicting one category label for an image. The content is illustrative prose, not an experiment to execute or a reported result to validate. Each repository snapshot contains its own task definition and scope.

| Path | Role |
| --- | --- |
| [base/article.md](base/article.md) | Original snapshot defining classification and excluding image generation and chatbot dialogue. |
| [candidate/article.md](candidate/article.md) | Adds useful per-category accuracy reporting, then repeats the same exclusions twice. |
| [findings.md](findings.md) | Expected comparison and snapshot reports. |
| [improved.md](improved.md) | Retains the reporting addition and original scope without the two repetitions. |
| [non_finding.md](non_finding.md) | A meaningful contrast distinguishing a category label from object bounding boxes. |

For comparison review, supply `base/` and `candidate/` as repository snapshots. For snapshot review, supply only `candidate/`. Both inputs contain their own argumentative context. This README, expected findings, and alternatives are explanatory material outside those inputs; no separate task, earlier drafts, or reviewer conversations are needed.

The finding depends on repeating an already explicit scope in a short passage, not on the phrase `rather than` or on disliking negative statements. In the non-finding, the contrast defines the model's output: a category label instead of an object's location. Removing it would remove a meaningful distinction. Caveats in independently read sections can also have separate purposes.

The minimal deletion preserves the task, its scope, and both overall and per-category accuracy reporting. The finding makes no claim that a user previously rejected image generation or chatbot development.

See the [instruction-text counterpart](../README.md) and [Code counterpart](../../README.md). The six dimensions, repository-only inputs, and report fields are unchanged.
