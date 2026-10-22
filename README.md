<div align="center">

<h1>Deoverfit</h1>

<p><strong>A lightweight code review Skill for unnecessary specialization, redundancy, and overengineering.</strong></p>

<p><strong>English</strong> · <a href="README.zh-CN.md">简体中文</a></p>

</div>

## What is this?

Deoverfit is a focused static review Skill for coding agents. It checks application code and self-evolved algorithms for assumptions, defensive branches, and abstractions the task does not need. Every finding includes code evidence, a concrete consequence, and the smallest useful change suggestion.

Review your current workspace, a source file, or a named **Candidate**. Add an optional **Base** to focus on changes, and an optional **Task** to explain intent. The output is a review report; Deoverfit leaves the code as it is.

## Why Deoverfit?

You ask an agent for scrambled eggs. It serves a steak. You correct it:

> **You:** I wanted scrambled eggs.
>
> **Agent:** Fixed: scrambled eggs **(steak-free edition)**.

The correction has become part of the dish's name. In code, a similar exchange might leave a `disable_steak` parameter, a rejection already covered by an allowlist, or an explanation of an old mistake embedded in the public API.

Now consider the coding version. You ask an agent to load a required configuration file. It adds retries and a fallback to default settings. You clarify:

> **You:** The config is required. If it's missing, report the error and stop startup. Don't silently switch to defaults and keep running.

The agent adds `strict=True`. The retry and fallback machinery stays, behind the new flag. The requirement got clearer; the code gained another mode to understand and maintain.

**What did the code pick up that the task never needed?**

These stories illustrate the kinds of issues to look for. An actual review establishes what is unnecessary from the available code and contracts, without guessing a prior conversation. Deoverfit does not edit code, add or run tests, or conduct benchmarks and performance experiments; static review cannot establish out-of-sample performance.

Try it on your current workspace, a single algorithm file, or a Base-to-Candidate change: [quick start](#quick-start).

## Quick start

Give your agent access to the skill files and the code to review. No Deoverfit runtime, API, or package installation is required. The simplest direct-file invocation needs no version arguments:

```text
Read /absolute/path/to/deoverfit/skills/deoverfit/SKILL.md
and follow its referenced review guidance.

Review the current workspace with Deoverfit.
```

This runs a snapshot review of existing code, including relevant untracked source, even if the working tree is clean. It does not automatically compare against `HEAD`, a parent commit, or the main branch. If no usable target workspace exists, the agent asks for a target.

## Inputs and modes

**Candidate** is the version under review: a feature change, a manual optimization, or code produced by an algorithm self-evolution process to improve performance. It defaults to the current target project's working tree. **Base** is an optional reference version. Neither needs to be a complete repository, and the name Candidate makes no claim that it is better than Base.

Paths are optional. Source versions can be files, directories, repository snapshots, commit IDs, branches, or tags. Git references use the specified repository or the current target repository when unambiguous. A commit ID requires repository context; it does not require repeating the repository path when that context is already available.

**Task** is an optional, free-text description of the intended change or optimization objective and any constraints to preserve. A sentence is enough; no fixed template, development history, or evaluation scores are required. It can explain why Base becomes Candidate, or what Candidate is intended to do in a snapshot review. Use a task already supplied in the conversation without asking the user to repeat it.

Task does not select the review mode. Supplying only Task still reviews the current workspace in snapshot mode. Omitting it never blocks an otherwise usable review: rely on visible contracts and code evidence, and omit findings that would require guessing the intent. Missing Task is not itself a finding.

| Inputs | Mode | Scope |
| --- | --- | --- |
| Base and Candidate | Comparison review | Added and modified code between those exact versions. |
| Candidate only | Snapshot review | Existing code within the selected Candidate scope. |
| Neither | Snapshot review | Existing code in the current target project's working tree. |
| Base only | Comparison review | Changes from Base to the current target project's working tree. |

In snapshot mode, report what is observable in the code without claiming an issue is new or a regression. In comparison mode, tie each finding to the delta and omit unchanged pre-existing issues. All six dimensions and the same evidence standard apply in both modes. A supplied but invalid path or unresolved reference needs correction; it is not treated as an omitted input.

To compare two source directories:

```text
Read /absolute/path/to/deoverfit/skills/deoverfit/SKILL.md
and follow its referenced review guidance.

Base: /absolute/path/to/base-repository
Candidate: /absolute/path/to/candidate-repository
Task: Add optional output formatting while preserving field names and defaults.

Review only added and modified code. Return evidence-backed findings
and minimal change suggestions. Do not change either repository.
```

For two commits of the current target repository, no path is needed (replace the placeholders with actual commit IDs; branches and tags work too):

```text
Use Deoverfit from /absolute/path/to/deoverfit/skills/deoverfit/SKILL.md.
Base: <base-commit-id>
Candidate: <candidate-commit-id>
Compare those exact snapshots, not their merge base. Review without edits.
```

For a self-evolved algorithm stored as an individual source file, Base can be omitted:

```text
Use Deoverfit from /absolute/path/to/deoverfit/skills/deoverfit/SKILL.md.
Candidate: /absolute/path/to/evolved/algorithm.py

Task: Improve solution quality while preserving the input format and feasibility rules.
Review this snapshot statically for unnecessary specialization,
redundancy, and overengineering. Return findings and minimal suggestions.
```

Add `Base: /absolute/path/to/reference/algorithm.py` to the last prompt when you want to review changes instead. Candidate can also be a commit ID on its own to review that committed snapshot without a comparison.

Replace example paths, revisions, and Task descriptions with your own; omit Task entirely when unnecessary. Exported snapshots need no `.git` metadata. No evolution trace, development transcript, intermediate commits, or evaluation scores are needed. Task and other supplied requirements help establish intent but are not mandatory inputs. A claimed performance gain is context, not proof of generality.

An algorithm candidate may intentionally change heuristics, scoring, or search behavior. Differences from Base alone are not findings. Deoverfit reviews evidence in the code; it does not verify claimed performance gains or require new experiments.

## Six review dimensions

| Dimension | What to examine |
| --- | --- |
| Scenario Overfitting | Project-specific assumptions leaking into a more general capability. |
| Trajectory Overfitting | Observable correction-shaped residue, redundant guards, or exclusions in the final code; no claim about how it arose. |
| Test Overfitting | Behavior coupled to test harnesses, fixture identities, or canned expected outputs instead of the input contract. |
| Environment Overfitting | Accidental dependence on a developer's filesystem, machine, or local configuration. |
| Implementation Overfitting | A capability coupled to incidental internal types, storage, or execution order rather than its available contract. |
| Speculative Generalization | Unused extension machinery or abstractions with a concrete, removable cost in the current implementation. |

See [review dimensions](skills/deoverfit/references/review-dimensions.md) for evidence requirements and false-positive boundaries, and [review guidelines](skills/deoverfit/references/review-guidelines.md) for comparison and reporting.

Domain logic, algorithm thresholds, numerical tolerances, platform adapters, and defensive checks are not findings merely because they are specific. A reviewer must show an unnecessary constraint, duplication, unsupported dependency, or other concrete consequence. Absence of a written requirement alone does not prove overengineering.

## Output

A review identifies its mode, resolved Candidate, optional Base, and reviewed scope, then lists only supported findings. Each finding includes its dimension, a Candidate path and line range, relevant code and contract evidence, the concrete consequence, and the smallest useful change. Comparison findings also explain their relationship to the delta. Snapshot reports omit Base and do not attribute issues to a change. One issue gets one finding even when several dimensions apply. There is no required finding count or score.

If nothing is supported, report `No evidence-backed Deoverfit findings.` This is a limited static review result, not a certification of correctness, generality, or performance. Disclose inaccessible files or incomplete review scope.

## Agent integration

The skill instructions, references, and source examples use English as their shared working language.

The portable entry point is [skills/deoverfit/SKILL.md](skills/deoverfit/SKILL.md), with standard `name` and `description` YAML frontmatter. Install the **whole `deoverfit` skill directory**, including `references/`. Keep one canonical copy per agent to avoid duplicate discovery.

| Agent | Project skill directory | Invocation |
| --- | --- | --- |
| [Codex](https://learn.chatgpt.com/docs/build-skills) | `.agents/skills/deoverfit/` | Select Deoverfit in the skill picker or ask to use it. |
| [Claude Code](https://code.claude.com/docs/en/skills) | `.claude/skills/deoverfit/` | `/deoverfit`, optionally followed by source versions or scope. |
| [Cursor](https://cursor.com/docs/skills) | `.cursor/skills/deoverfit/` | Type `/` and select Deoverfit. |
| [GitHub Copilot](https://docs.github.com/en/copilot/concepts/customizations/agent-skills) | `.github/skills/deoverfit/` | Ask agent mode to use Deoverfit, optionally specifying source versions or scope. |

These locations are documented by the linked vendors; discovery varies by product version and execution surface. For another agent, or when native skill discovery is unavailable, use the direct-file prompt above. The agent needs access to the skill references and the selected source version or versions in its own execution environment; a path on your laptop is not automatically available to a cloud session.

For example, from this repository root, install into a target project's Codex skill directory (replace the target path; the destination must not already exist):

```sh
mkdir -p /absolute/path/to/target-project/.agents/skills
cp -R skills/deoverfit /absolute/path/to/target-project/.agents/skills/deoverfit
```

For the other agents, use the corresponding parent directory from the table. Installation is optional; directly reading the files has the same review instructions. This repository supplies instructions, not a vendor-specific plugin or an enforcement sandbox.

## Examples

Each directory contains `base.py`, `candidate.py`, `findings.md`, `improved.py`, and `non_finding.py`, plus a short README stating the local contract. The latter two are explanatory alternatives, not additional review inputs. The Python snippets are self-contained source examples, not a test suite or benchmark.

For comparison mode, provide `base.py` and `candidate.py`. For snapshot mode, provide only `candidate.py`; each `findings.md` also shows a snapshot report supported without reading Base or the alternative implementations.

| Dimension | Example |
| --- | --- |
| Scenario Overfitting | [JSON encoder with an application-specific field rewrite](examples/scenario-overfitting/README.md) |
| Trajectory Overfitting | [An unreachable exclusion and correction-shaped output](examples/trajectory-overfitting/README.md) |
| Test Overfitting | [Word count replaced by a constant under a test harness](examples/test-overfitting/README.md) |
| Environment Overfitting | [Caller-provided catalog location displaced by a local path](examples/environment-overfitting/README.md) |
| Implementation Overfitting | [An exporter tied to a concrete store's private storage](examples/implementation-overfitting/README.md) |
| Speculative Generalization | [A fixed greeting with unused extension machinery](examples/speculative-generalization/README.md) |

## Review scope and complementary reviews

Deoverfit is a focused review pass for the [six dimensions below](#six-review-dimensions). Use it to check whether a shared capability carries unnecessary application assumptions, an agent-generated change adds redundant defenses or unused abstractions, or an evolved algorithm depends on fixtures or accidental environment details.

It does not attempt comprehensive coverage of functional correctness, security, concurrency, resource management, compatibility, or domain and mathematical correctness. A Deoverfit finding may have consequences in these areas, but an unrelated bug does not become a Deoverfit finding merely because it is serious. Test Overfitting examines test-dependent behavior; it does not assess overall test coverage or test-suite quality.

For a broader code review, combine Deoverfit with a general code-review skill or workflow, adding security or domain-specific review where appropriate. Deoverfit can also be used independently for its focused scope; no particular companion skill is required or bundled.

For example, when a general code-review skill is available:

```text
Use the general code-review skill and Deoverfit on the same Candidate,
with the same optional Base, Task, and source scope.
Check functional correctness in the general review, and apply Deoverfit's
six dimensions in the focused review. Identify which scope supports each
finding and merge duplicate findings about the same issue.
Return findings and minimal suggestions without edits, tests, or benchmarks.
```

Each pass follows its own evidence criteria. Deoverfit does not automatically install or invoke other skills, expand the requested scope, or make a broader review a prerequisite. `No evidence-backed Deoverfit findings.` means no supported issue was found within this focused static review; it is not overall code approval.

### Suggested companion projects

These four projects offer optional complementary review capabilities. The descriptions summarize their published instructions; this is a scope-based selection, not a comparative effectiveness ranking. None is bundled with Deoverfit or required to use it.

| Project | When it complements Deoverfit | Workflow boundary |
| --- | --- | --- |
| [adversarial-code-review](https://github.com/contrueCT/adversarial-code-review) | Broader review of requirement alignment, logic, security, data integrity, concurrency, compatibility, and test credibility. It also overlaps with scope and overengineering checks. | Its risk-adaptive workflow includes verification and additional review passes. Keep those separate from Deoverfit's static pass and honor the requested execution limits. |
| [Anthropic pr-review-toolkit](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/pr-review-toolkit) | Review code quality, error handling, type design, comments, and test coverage using focused agents. Particularly useful in Claude Code. | Select the relevant review agents. Its code-simplifier also supports refactoring; a request for findings alone does not authorize applying changes. |
| [reviewing-code-modularity-skill](https://github.com/tyshkovskii/reviewing-code-modularity-skill) | Examine module boundaries, coupling, cohesion, public APIs, and whether an abstraction solves a current problem. It overlaps with Implementation Overfitting and Speculative Generalization. | Use its fast review mode for findings. Its design and implementation modes go beyond review and may involve refactoring and validation. |
| [avoid-overdefensive-programming](https://github.com/aravelo7/codex-agent-skills/blob/main/skills/avoid-overdefensive-programming/SKILL.md) | Inspect unsupported fallbacks, swallowed errors, retries, defaults, and compatibility branches while preserving justified safeguards. It overlaps with some redundancy and residue checks. | This is also a coding and repair workflow with modification and verification steps. Keep a review-only request scoped to findings; its presence does not authorize edits or new tests. |

Choose a broader reviewer from the first two rows when broader coverage is needed, and add a specialist from the last two for a concrete concern. Use the same Candidate, optional Base and Task, and source scope; attribute findings to the relevant pass and merge duplicates. Check each companion's current instructions for a compatible mode. Deoverfit retains its own static, suggestion-only scope.

## Contributing

Keep the review static and bounded by its selected mode and source scope. A useful contribution makes an evidence rule clearer or adds a concrete example with a plausible non-finding. Preserve intended behavior in suggested simplifications. Avoid adding mandatory Base or Task inputs, execution, tests, historical inputs, or findings quotas.

## License

[MIT](LICENSE).
