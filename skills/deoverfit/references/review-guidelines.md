# Review guidelines

## Focused scope and composition

Deoverfit reviews the six generality dimensions in [review-dimensions.md](review-dimensions.md). It does not attempt comprehensive correctness, security, concurrency, resource-management, compatibility, or domain and mathematical validation. Test Overfitting concerns dependence on evaluation context, not overall test coverage or test-suite quality. Include a correctness or security consequence when it establishes a Deoverfit mechanism; do not relabel unrelated defects to fit a dimension.

For a comprehensive review, pair this pass with a general code-review skill or workflow and relevant specialist review. No specific companion is required. A Deoverfit-only request should finish within its focused scope, without requiring, installing, or automatically invoking other skills.

When the user requests multiple review passes, keep the selected versions and source scope consistent. Attribute findings to the scope whose criteria support them and merge duplicate findings about the same mechanism. A broader review's issue may be reported under that review's scope without forcing it into a Deoverfit dimension. Combining skills does not itself authorize code edits, tests, benchmark runs, or additional workflows.

Interpret a clean Deoverfit report only as the absence of supported findings within this focused static review and its stated coverage. Do not describe it as overall code approval or imply that other review areas were checked.

## Resolve inputs and choose the mode

Candidate is the version to review. Base is an optional reference version. Either may be an individual file, source directory, repository snapshot, commit ID, branch, or tag. They may come from unrelated repositories. These roles say nothing about how the code was produced or whether Candidate improves performance.

| Inputs | Mode and target |
| --- | --- |
| Base and Candidate | Comparison review of those exact versions. |
| Candidate only | Snapshot review of Candidate. |
| Neither | Snapshot review of the current target project's working tree. |
| Base only | Comparison review of Base against the current target project's working tree. |

Paths are optional. Resolve Git references in the explicitly specified repository, or the current target repository when unambiguous. A commit ID without a usable repository context needs clarification, not an invented filesystem path. Resolve supplied references to commit IDs and record the repository so the report identifies what was reviewed. Source files and directories require no Git metadata.

An omitted Candidate defaults to the current target project, respecting any requested file or directory scope. Include relevant tracked and untracked source in the working tree. Do not confuse the skill's installation location with the review target. Ask only when no usable target is available or when the target, repository, reference, or scope is materially ambiguous. State the resolved target and scope in the report.

An explicitly supplied but inaccessible path or unresolved reference is an input problem, not permission to use a default. Resolve it or ask for the specific missing information. Do not silently downgrade a requested comparison to snapshot mode, or replace a named revision with working files.

When Base is absent, do not infer one from `HEAD`, a parent commit, main, an upstream branch, or a merge base. Reading a Git revision tree or checking working-tree status does not make it Base. Neither dirty status nor Git metadata is required for a snapshot review.

## Optional Task context

Task is a free-text description of the intended behavior change, optimization objective, or constraints to retain. It is optional in both modes and may already be explicit in the request or conversation; do not require the user to repeat it or supply a formal specification. Task alone uses the current-workspace snapshot default. Its presence or absence does not select the mode or create a Base.

Use supplied Task intent to interpret which specializations and behavior changes are required. Task may intentionally change a Base contract, so do not demand restoration of Base behavior that the task explicitly replaces. The observed mechanism and consequence must still be evidenced in Candidate code; a task description is not proof of execution behavior, performance gains, or empirical generalization.

When Task is absent, continue using visible interfaces, behavior, callers, and documentation. Do not pause solely to request it, report its absence as a problem, or infer a development story from the diff. If a potential finding depends on an unknown requirement, omit that finding rather than invent the intent or demand a task description to complete the review.

## Comparison review

Compare exactly the supplied Base and resolved Candidate. For two revisions already available in one repository, these read-only operations are useful (substitute the actual references):

```sh
git -C /path/to/repository rev-parse --verify 'BASE^{commit}'
git -C /path/to/repository rev-parse --verify 'CANDIDATE^{commit}'
git -C /path/to/repository diff --no-ext-diff --no-textconv --name-status BASE CANDIDATE --
git -C /path/to/repository diff --no-ext-diff --no-textconv --unified=5 BASE CANDIDATE --
git -C /path/to/repository show 'CANDIDATE:path/to/file'
```

Do not use three-dot comparison: that changes Base to a merge base. Read revision files directly without checking them out. No reset, dependency installation, `git log`, blame, intermediate patches, or development transcript is needed.

For source directories, map corresponding relative paths. For individual files, compare the named files even if their names differ. A starting point for directories is:

```sh
git diff --no-index --no-ext-diff --no-textconv -- /path/to/base /path/to/candidate
```

For files, supply their full paths to the same command. Exit status `1` means differences were found; an error or unreadable input is not a clean review. Exclude VCS internals and irrelevant generated artifacts. If `.git` trees make a directory diff noisy, use source inventories and compare matching files individually. Do not silently omit changed source because it resides in an unusual directory. Normalize directory prefixes when reporting relative paths.

A working-tree Candidate includes tracked staged and unstaged content plus relevant untracked source. A diff against Base covers tracked changes; inspect untracked files separately. For separate repositories, read each named endpoint tree without modifying either checkout.

Start with added and modified code, including renamed files with modifications. Read unchanged callers, interfaces, configuration, documentation, and existing tests to assess a potential finding. Attribute findings to something added, modified, or newly made reachable by the change. Unchanged pre-existing issues are outside this mode; deletions may explain a changed contract but are not a separate review target.

## Snapshot review

Inspect the existing source within Candidate's selected scope, including code that has no local changes. A clean working tree does not mean there is nothing to review. For a commit, branch, or tag, resolve and read that revision's tree rather than the current working files. Reading `rev-parse` and `show` as above requires only Candidate, not Base. For a source file or directory, read it directly; Git is unnecessary.

Follow available imports, callers, interfaces, configuration, documentation, and existing tests only as needed for context. Exclude VCS internals and irrelevant generated artifacts. Do not expand a selected file or directory review into an unrelated project-wide audit. Disclose missing context and material coverage limits, especially when an unused-code claim depends on external callers or registrations.

Establish problems from Candidate's current code and applicable contracts. Cite Candidate evidence and describe what the code does now. Do not call an issue newly introduced, a regression, or a consequence of a particular edit. Do not discover or use an unrequested baseline to justify a snapshot finding. Apply all six dimensions with the same evidence bar; lack of a baseline is not a reason to lower it.

## Admit a finding only with evidence

Use optional Task and other supplied requirements where present. Otherwise infer only contracts supported by visible interfaces, behavior, callers, and documentation. A self-evolved algorithm needs no feature-development brief: its existing input/output contract and supplied objective can provide context. Intentional heuristic or search changes need not reproduce Base's outputs. Missing requirements are uncertainty, not proof of a flaw.

For every potential finding, establish:

1. **Observed mechanism:** Identify the exact branch, dependency, data rewrite, redundant guard, or dispatch layer. In comparison mode, also identify its relationship to the delta. In snapshot mode, no claim about when it appeared is needed or justified.
2. **Applicable contract:** Show the supported behavior or boundary against which the mechanism is unnecessary. Cite Candidate interfaces or callers, supplied requirements, and Base evidence when actually comparing versions. A comment may explain intent but does not prove execution behavior by itself.
3. **Concrete consequence:** Explain a reachable wrong assumption, ignored configuration, duplicated source of truth, provably unreachable check, or removable internal machinery. Distinguish static reasoning from any unmeasured runtime or performance claim.
4. **Minimal suggestion:** State the smallest useful correction preserving the intended behavior, applicable domain rules, error handling, and compatibility. Keep public behavior consistent with its contract. Do not ask for a new framework, test suite, benchmark, or broad rewrite.

Check the strongest reasonable counterexplanation: domain semantics, deployment constraints, compatibility, an external extension contract, numeric stability, mutable state, or a real trust boundary. Resolve it from available code when possible. Omit findings that still depend on invented requirements, unseen history, or missing context needed to prove the issue.

The labels describe code mechanisms, not developer intent. For Trajectory Overfitting, explain what is redundant now; never assert that a user correction or agent retry caused it. For algorithms, do not equate a tuned threshold with benchmark overfitting or promise that deleting it preserves solution quality. Evaluation scores, if supplied, are context rather than proof of generality; do not request scores, evolution traces, or experiments to complete this static review.

## Report

Begin with the mode, resolved versions, and reviewed scope. Use one of these headers, substituting actual values:

```text
Mode: Comparison review
Base: <path, or repository + reference + resolved commit>
Candidate: <path or working tree, or repository + reference + resolved commit>
Scope: <reviewed files/directories; added and modified code>
```

```text
Mode: Snapshot review
Candidate: <path or working tree, or repository + reference + resolved commit>
Scope: <reviewed files/directories; existing code>
```

For a default working-tree target, include its actual project path. A snapshot header has no Base field. State that snapshot mode cannot establish whether issues are newly introduced; this is a mode boundary, not a request for history.

Summarize a supplied Task briefly when it helps interpret findings, or cite it as contract evidence where relevant. No Task field or missing-Task notice is required when it was omitted.

List only supported findings, ordered by consequence, using this shape:

```text
1. <Actionable title>
   Dimension: <one of the six dimensions>
   Location: <Candidate-relative path>:<start>-<end>
   Evidence: <observed mechanism and a short excerpt or exact symbol>;
             <Candidate context/contract, plus Base context if comparing>.
   Consequence: <specific observable problem or removable complexity>.
   Minimal suggestion: <smallest useful correction preserving the contract>.

Scope limitations: <only material inaccessible or unreviewed content, if any>.
```

Use actual one-based Candidate line numbers and a tight range. In comparison mode, anchor the finding to changed Candidate code and qualify endpoint paths when necessary. Include supporting locations when a claim depends on another file or an exhaustive search. Do not cite removed Base lines as though they still exist in Candidate. If only a partial diff is available, cite its hunk or symbol and disclose that limitation rather than fabricate line numbers.

One root cause gets one finding. No required count, six-category checklist, numerical score, or speculative issue appendix is needed. Avoid cosmetic preferences and unrelated bugs that do not establish one of the six mechanisms. Suggest changes in prose; do not apply a patch or refactor automatically.

If no finding meets the evidence bar, append `No evidence-backed Deoverfit findings.` after the appropriate mode header. In snapshot mode this also applies to a clean working tree that was actually reviewed. An inaccessible target is not a clean review.

Disclose incomplete coverage even when no finding is supported. A clean report makes no claim about runtime correctness, undeclared platform support, empirical generalization, or performance. Stop after the static review; no tests, benchmarks, performance experiments, or development-history investigation are part of the workflow.
