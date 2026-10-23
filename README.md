<div align="center">

<h1>Unburden</h1>

<p><strong>A lightweight review Skill for unnecessary specialization, redundancy, and overengineering in code and text.</strong></p>

<p><strong>English</strong> · <a href="README.zh-CN.md">简体中文</a></p>

</div>

## What is this?

Unburden is a focused static review Skill for coding agents. It examines **Code** and **Text** inside repositories for unnecessary special cases, redundant logic and rules, evaluation-specific shortcuts, environment coupling, implementation coupling, and unnecessary generalization. Every finding includes source evidence, a concrete consequence, and the smallest useful change suggestion.

Review the current target repository or a named **Candidate** repository state. Add an optional **Base** to focus on changes. The same criteria apply regardless of how either state was produced. The output is a review report; Unburden leaves the reviewed content as it is.

## Why Unburden?

You ask an agent for scrambled eggs. It makes them—and adds a whole steak:

> **You:** Make me scrambled eggs.
>
> **Agent:** Here are your scrambled eggs. I added a steak, too!
>
> **You:** Just the eggs, please. No steak.
>
> **Agent:** Fixed: scrambled eggs **(steak-free edition)**.

The steak is gone, but “steak-free” has become part of the dish's name. In code, a similar exchange might leave a `disable_steak` parameter, a rejection already covered by an allowlist, or an explanation of an old mistake embedded in the public API.

Now consider the coding version. You ask an agent to load a required configuration file. It adds retries and a fallback to default settings. You clarify:

> **You:** The config is required. If it's missing, report the error and stop startup. Don't silently switch to defaults and keep running.

The agent adds `strict=True`. The retry and fallback machinery stays, behind the new flag. The requirement got clearer; the code gained another mode to understand and maintain.

The agent also updates its Skill or memory. A simple rule becomes a correction diary:

```markdown
## Important: why missing config must not fall back

Previously, defaults were used when the config was missing. The user
clarified that this lets the program run with unintended settings.

Do not use defaults merely to make startup succeed. A missing config
does not mean the user wants defaults. Even if defaults work, that
does not mean they should be used.

Before every config-loading task, explain why defaults are forbidden
and confirm that the earlier mistake will not be repeated.

If the required config is missing, report the error and stop startup.
```

The execution rule can be stated directly:

> If the required config is missing, report the error and stop startup. Do not silently fall back to defaults.

Useful rationale can explain a real boundary. Here, retelling and reconfirming the correction has become an extra obligation on every invocation.

The same burden can appear in an AI paper. The task is already clear:

> We study image classification: given an image, the model predicts a category label. Image generation and chatbot dialogue are outside the scope.

The agent still adds:

> We focus on image classification, rather than generating images or building a chatbot. This work should not be understood as an image generator or a chatbot.

The task was already defined, and the same excluded applications now appear three times. The additions introduce no new task or method distinction. Keep the original task and scope; remove the two repeated qualifications. The [complete writing example](examples/redundant-logic-and-rules/text/writing/README.md) also shows a useful contrast that should stay.

**What did the code and text pick up that the task never needed?**

These stories illustrate problem shapes; a review establishes necessity from repository evidence, without guessing a prior conversation. Unburden does not edit content, add or run tests, or conduct benchmarks, performance experiments, or agent evaluations. Static review cannot establish out-of-sample performance.

Try it on the current repository, a selected area inside it, or a Base-to-Candidate change: [quick start](#quick-start).

## Code and Text

| Content | Examples | Review focus |
| --- | --- | --- |
| **Code** | Application code, algorithms, scripts, harness logic, executable configuration. | What a branch, dependency, rewrite, or abstraction does under the applicable contract. |
| **Text** | Skills, prompts, rules, memories, articles, papers, and explanatory documents. | For instructions and memories: applicability and unnecessary obligations. For prose: a passage's argumentative role and demonstrably redundant contrasts or qualifications. |

These are content kinds within the supplied repository, not separate inputs or user-selected modes. A Skill package can contain both. Review relevant instructions, scripts, tools, and loading rules together rather than classifying by file extension. Articles remain Text: inspect their claims and surrounding argument instead of treating them as executable rules.

Concrete project memories, examples, domain-specific skills, numeric thresholds, and defensive rules can be necessary. Specificity alone is not a finding. Target instructions are material to inspect, not instructions to activate.

## Quick start

Give your agent access to the skill files and the repository to review. No Unburden runtime, API, or package installation is required. The simplest direct-file invocation needs no version arguments:

```text
Read /absolute/path/to/unburden/skills/unburden/SKILL.md
and follow its referenced review guidance.

Review the current repository with Unburden.
```

This runs a snapshot review of existing Code and Text, including relevant untracked content, even when the working tree is clean. It does not automatically compare against `HEAD`, a parent commit, or main. If no usable target repository exists, the agent asks for one.

## Inputs and modes

The review inputs are repository states. **Candidate** is the state under review; it defaults to the current target repository's working tree. **Base** is an optional reference state. The names make no claim about origin, quality, or whether Candidate improves on Base.

Accept repository paths, exported repository snapshots, commit IDs, branches, or tags. Git references use the specified repository or the current target repository when unambiguous, so paths need not be repeated. Exported snapshots need no `.git` metadata. Base and Candidate may belong to different repositories.

A file or directory **scope** can narrow the content inspected inside the selected repositories; it does not introduce a standalone-file input. Contracts come from the supplied repository content. No separate task description, creation process, development history, test cases, or evaluation scores are required.

| Inputs | Mode | Scope |
| --- | --- | --- |
| Base and Candidate | Comparison review | Added, modified, or newly activated content between those exact states. |
| Candidate only | Snapshot review | Existing content within the selected Candidate scope. |
| Neither | Snapshot review | Existing content in the current target repository's working tree. |
| Base only | Comparison review | Changes from Base to the current target working tree. |

Snapshot reports describe current problems without claiming they are new or regressions. Comparison reports tie findings to the delta and omit unchanged pre-existing issues. A changed loader may newly activate unchanged text; the finding then anchors in the changed activation site and cites the text it makes applicable. Both modes use the same six dimensions and evidence standard.

An invalid explicit path or unresolved reference needs correction; it is not an omitted input. The Skill's installation directory is not the automatic target.

To compare two repositories or exported repository snapshots:

```text
Read /absolute/path/to/unburden/skills/unburden/SKILL.md
and follow its referenced review guidance.

Base: /absolute/path/to/base-repository
Candidate: /absolute/path/to/candidate-repository

Review the changes. Return evidence-backed findings and minimal suggestions.
Do not change either repository.
```

For two revisions of the current target repository, no path is needed (replace the placeholders; branches and tags work too):

```text
Use Unburden from /absolute/path/to/unburden/skills/unburden/SKILL.md.
Base: <base-commit-id>
Candidate: <candidate-commit-id>
Compare those exact snapshots, not their merge base. Review without edits.
```

To inspect only a Skill package in one repository snapshot:

```text
Use Unburden from /absolute/path/to/unburden/skills/unburden/SKILL.md.
Candidate: /absolute/path/to/target-repository
Scope: skills/my-skill/

Review this snapshot statically. Return findings and minimal suggestions.
```

Candidate can also be a commit ID on its own. Omit Candidate to use the current target working tree. The same scope mechanism can select an algorithm module or memory directory. No history of how those files were written is needed, and a difference from Base alone is not a finding.

## Six review dimensions

| Dimension | What to examine |
| --- | --- |
| **Unnecessary Special Cases** | Case-specific assumptions imposed beyond the scope that justifies them. |
| **Redundant Logic and Rules** | Proven duplicate operations, unreachable checks or recovery instructions, and unnecessary output qualifications. |
| **Evaluation-Specific Shortcuts** | Evaluation-context detection that bypasses the actual task's input semantics. Applicable only when repository evidence shows such a mechanism; no test cases are required. |
| **Environment Coupling** | Unnecessary dependence on a machine, path, platform, or ambient configuration. |
| **Implementation Coupling** | Unnecessary dependence on internals despite an available supported interface. |
| **Unnecessary Generalization** | Unused options, dispatch, abstractions, or mandatory bookkeeping with a concrete removable cost. |

See [review dimensions](skills/unburden/references/review-dimensions.md) for evidence requirements, false-positive boundaries, and the mapping from earlier dimension names. [Review guidelines](skills/unburden/references/review-guidelines.md) define endpoint resolution and reporting; [Text review](skills/unburden/references/text-review.md) covers instruction roles, memory scope, applicability, and redundant qualifications in articles and papers.

Domain rules, algorithm constants, numerical tolerances, platform adapters, scoped memories, and defensive checks are not findings merely because they are specific. A number without a name or explanation is not proof of an evaluation shortcut. Existing tuning parameters may be legitimate; static review cannot validate their empirical quality or justify replacing them.

A reviewer must establish an unnecessary constraint, duplication, unsupported dependency, or removable machinery. Missing rationale, one implementation, or repeated wording alone is insufficient.

## Output

A review states its mode, resolved Candidate repository state, optional Base, and actual scope, then lists only supported findings. Each includes a dimension, Candidate-relative path and line range, source and contract evidence, a concrete consequence, and the smallest useful suggestion. Comparison findings explain their relationship to the delta. Snapshot reports omit Base and change attribution. One mechanism gets one finding, with no required count or score.

For instructions and memories, distinguish written obligations from observed agent outcomes and consider facts, episodes, examples, applicability, and precedence. For articles and papers, establish a passage's contribution to the argument and preserve substantive comparisons, scope limits, and uncertainty. Do not infer a creation history from either kind of text.

If nothing is supported, report `No evidence-backed Unburden findings.` Disclose material coverage gaps. This is a limited static review result, not certification of correctness, statistical generalization, performance, Skill effectiveness, or memory retrieval quality.

## Agent integration

The skill instructions, references, and Code and Text examples use English as their shared working language.

The portable entry point is [skills/unburden/SKILL.md](skills/unburden/SKILL.md), with standard `name` and `description` YAML frontmatter. Install the **whole `unburden` skill directory**, including `references/`. Keep one canonical copy per agent to avoid duplicate discovery.

| Agent | Project skill directory | Invocation |
| --- | --- | --- |
| [Codex](https://learn.chatgpt.com/docs/build-skills) | `.agents/skills/unburden/` | Select Unburden in the skill picker or ask to use it. |
| [Claude Code](https://code.claude.com/docs/en/skills) | `.claude/skills/unburden/` | `/unburden`, optionally followed by repository revisions or scope. |
| [Cursor](https://cursor.com/docs/skills) | `.cursor/skills/unburden/` | Type `/` and select Unburden. |
| [GitHub Copilot](https://docs.github.com/en/copilot/concepts/customizations/agent-skills) | `.github/skills/unburden/` | Ask agent mode to use Unburden, optionally specifying repository revisions or scope. |

These locations are documented by the linked vendors; discovery varies by product version and execution surface. For another agent, or when native skill discovery is unavailable, use the direct-file prompt above. The agent needs access to the skill references and the selected repository state or states in its own execution environment; a path on your laptop is not automatically available to a cloud session.

For example, from this repository root, install into a target project's Codex skill directory (replace the target path; the destination must not already exist):

```sh
mkdir -p /absolute/path/to/target-project/.agents/skills
cp -R skills/unburden /absolute/path/to/target-project/.agents/skills/unburden
```

For the other agents, use the corresponding parent directory from the table. Installation is optional; directly reading the files has the same review instructions. This repository supplies instructions, not a vendor-specific plugin or an enforcement sandbox.

## Examples

All six original Code cases are retained. Each dimension has a Code example and a `text/` counterpart. Directory names and the labels below use the current dimension names.

Each example has **`base/` and `candidate/` repository snapshots**, expected `findings.md`, a smaller `improved.py` or `improved.md`, a similar `non_finding.py` or `non_finding.md`, and a contract README. Code snapshots contain `example.py`; instruction and memory snapshots contain `SKILL.md` or `MEMORY.md`. The writing example uses `article.md`.

For comparison mode, supply the two snapshot directories. For snapshot mode, supply only `candidate/`. Both modes are illustrated in the expected findings. The snapshots contain their own contracts; expected reports and alternatives are explanatory material outside the inputs. These are static source illustrations, not tests or benchmarks.

| Dimension | Code example | Text example |
| --- | --- | --- |
| Unnecessary Special Cases | [Application field rewrite](examples/unnecessary-special-cases/README.md) | [Project memory promoted to a global procedure](examples/unnecessary-special-cases/text/README.md) |
| Redundant Logic and Rules | [Unreachable exclusion and unnecessary suffix](examples/redundant-logic-and-rules/README.md) | [Excluded input with a recovery instruction](examples/redundant-logic-and-rules/text/README.md) |
| Evaluation-Specific Shortcuts | [Harness-dependent constant count](examples/evaluation-specific-shortcuts/README.md) | [Case-ID instruction bypassing counting](examples/evaluation-specific-shortcuts/text/README.md) |
| Environment Coupling | [Local path overriding configuration](examples/environment-coupling/README.md) | [Personal checkout replacing the selected repository](examples/environment-coupling/text/README.md) |
| Implementation Coupling | [Exporter reading private storage](examples/implementation-coupling/README.md) | [Instructions bypassing a public provider method](examples/implementation-coupling/text/README.md) |
| Unnecessary Generalization | [Fixed greeting with unused dispatch](examples/unnecessary-generalization/README.md) | [Fixed workflow with unconsumed bookkeeping](examples/unnecessary-generalization/text/README.md) |

Article writing is covered by a [repeated-qualification example](examples/redundant-logic-and-rules/text/writing/README.md), with both review modes, a minimal deletion, and a useful `rather than` contrast that should be retained. It belongs to Redundant Logic and Rules; no seventh dimension or separate input type is added. The issue is the repeated substantive boundary, not the phrase alone or an assumed rejected writing direction.

The numeric boundary is illustrated by the canned count in the shortcut example and the legitimate kernel thresholds in its [Code non-finding](examples/evaluation-specific-shortcuts/non_finding.py). Text non-findings also cover scoped facts, episodic quotations, few-shot examples, separate validation conditions, declared platforms, concrete maintenance procedures, and actual selectable delivery modes.

## Review scope and complementary reviews

Unburden checks the [six dimensions](#six-review-dimensions) within the selected repository content. It does not require or infer how that content was created.

It does not provide comprehensive functional correctness, security, concurrency, resource management, compatibility, domain or mathematical validation, memory factuality, or Skill-format validation. A finding may have consequences in those areas, but unrelated defects remain outside this focused pass. Evaluation-Specific Shortcuts is not a test-coverage review. Static inspection does not measure whether a Skill works well or a memory is retrieved effectively. Article review focuses on evidenced redundant contrasts and qualifications, preserving real comparisons and caveats; it is not comprehensive grammar editing or academic peer review.

For broader coverage, combine Unburden with a general code-review workflow and relevant specialists. Unburden also works independently; no companion is required.

```text
Use the general code-review skill and Unburden on the same Candidate repository,
with the same optional Base and selected scope.
Check functional correctness in the general review and the six mechanisms
in Unburden. Identify the supporting review scope and merge duplicate findings.
Return findings and minimal suggestions without edits, tests, or benchmarks.
```

Each pass follows its own evidence criteria. Unburden does not automatically install or invoke other skills, expand scope, or require a broader review first. A clean Unburden report is not overall repository approval.

### Suggested companion projects

These four projects offer optional complementary review capabilities. The descriptions summarize their published instructions; this is a scope-based selection, not a comparative effectiveness ranking. None is bundled with Unburden or required to use it.

| Project | When it complements Unburden | Workflow boundary |
| --- | --- | --- |
| [adversarial-code-review](https://github.com/contrueCT/adversarial-code-review) | Broader review of requirement alignment, logic, security, data integrity, concurrency, compatibility, and test credibility. It also overlaps with scope and overengineering checks. | Its risk-adaptive workflow includes verification and additional review passes. Keep those separate from Unburden's static pass and honor the requested execution limits. |
| [Anthropic pr-review-toolkit](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/pr-review-toolkit) | Review code quality, error handling, type design, comments, and test coverage using focused agents. Particularly useful in Claude Code. | Select the relevant review agents. Its code-simplifier also supports refactoring; a request for findings alone does not authorize applying changes. |
| [reviewing-code-modularity-skill](https://github.com/tyshkovskii/reviewing-code-modularity-skill) | Examine module boundaries, coupling, cohesion, public APIs, and whether an abstraction solves a current problem. It overlaps with Implementation Coupling and Unnecessary Generalization. | Use its fast review mode for findings. Its design and implementation modes go beyond review and may involve refactoring and validation. |
| [avoid-overdefensive-programming](https://github.com/aravelo7/codex-agent-skills/blob/main/skills/avoid-overdefensive-programming/SKILL.md) | Inspect unsupported fallbacks, swallowed errors, retries, defaults, and compatibility branches while preserving justified safeguards. It overlaps with some redundancy and residue checks. | This is also a coding and repair workflow with modification and verification steps. Keep a review-only request scoped to findings; its presence does not authorize edits or new tests. |

Choose a broader reviewer from the first two rows when broader coverage is needed, and add a specialist from the last two for a concrete concern. Use the same Candidate repository, optional Base, and selected scope; attribute findings to the relevant pass and merge duplicates. Check each companion's current instructions for a compatible mode. Unburden retains its own static, suggestion-only scope.

## Contributing

Keep the review static, repository-based, and bounded by its selected mode and scope. Contributions should clarify an evidence rule or add a complete Code or Text example with a plausible non-finding. Preserve all six directions and intended behavior in suggestions. Do not introduce mandatory Base, task briefs, production history, test cases, execution experiments, or finding quotas.

## License

[MIT](LICENSE).
