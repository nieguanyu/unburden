# Review dimensions

Apply these six lenses to Code and Text in either comparison or snapshot mode. The names describe mechanisms visible in the supplied repository states, not their origin. A finding needs Candidate evidence, an applicable contract, a concrete consequence, and a minimal useful suggestion. Comparison findings must relate to the delta; snapshot findings must not attribute an issue to a change. Follow [review-guidelines.md](review-guidelines.md) and, for agent text, [text-review.md](text-review.md).

## 1. Unnecessary Special Cases

**Question:** Does a capability impose a case-specific assumption outside the scope that justifies it?

**Code:** Inspect application names, tenant IDs, schema rewrites, domain imports, narrow input branches, and implicit defaults in shared code. Trace their effect on a supported caller. A specific identifier is a lead, not proof.

**Text:** Inspect local project facts or preferences promoted to global rules, one example treated as an exhaustive procedure, and task-specific output exceptions imposed on a broader skill. Establish the declared scope and the actual operative requirement; a concrete memory or few-shot example alone is not a finding.

**Sufficient evidence:** A JSON encoder promises to preserve keys yet rewrites one application's field names; or a memory policy explicitly confines project facts to that project while an operative rule requires every project to use that project's workflow.

**Do not flag:** Domain modules, application adapters, schema migrations, project-scoped workflows, user preferences in the correct namespace, episodic records, mathematical special cases, or intentionally specialized capabilities. Do not demand a universal API or skill.

**Minimal direction:** Remove the unsupported exception or keep the required specialization within its existing domain or applicability boundary.

## 2. Redundant Logic and Rules

**Question:** Is a check, rule, recovery path, or output qualification demonstrably redundant or inapplicable under the current contract?

**Code:** Inspect duplicated exclusions, checks made unreachable by exhaustive validation, recovery branches with no reachable trigger, and output qualifications that merely repeat an already-enforced restriction while violating the specified format. Establish redundancy using the actual input types, mutation, and call path.

**Text:** Inspect repeated obligations that create duplicate work, recovery steps excluded by the same workflow's admission rules, and instructions to maintain or emit an unnecessary qualification. Read conditions and precedence before treating apparently conflicting rules as simultaneously applicable. An unrelated contradiction is not automatically a Deoverfit finding.

**Sufficient evidence:** An immutable ingredient tuple containing pork is rejected by an allowlist before a second pork check; or a local Markdown-only workflow still mandates archive recovery after archives have already been rejected, and appends an excluded warning to a plain-title output.

**Do not flag:** Independent trust boundaries, mutable state, checks in separate processes, reachable fallbacks with distinct semantics, compatibility requirements, deliberate reinforcement that creates no demonstrated extra obligation, or required safety labels. Repeated wording alone is insufficient.

**Minimal direction:** Remove the proven duplicate or inapplicable step and restore the required output; retain effective validation, required exclusions, and meaningful recovery. Describe the present relationship, without speculating about an earlier mistake or correction.

## 3. Evaluation-Specific Shortcuts

**Question:** Does a supported task path detect evaluation context and bypass the task's input semantics?

**Code:** Inspect harness markers, fixture IDs, and stored-answer branches that replace the real computation. Existing tests or fixtures may provide context, but neither their presence nor their execution is required.

**Text:** Inspect operative instructions to recognize an evaluator, match a case ID, or return an expected answer without doing the stated task. Distinguish these from quoted attacks, documented examples, evaluation instructions whose purpose is replay, and legitimate few-shot demonstrations.

**Sufficient evidence:** A public word counter returns `3` whenever `PYTEST_CURRENT_TEST` is present; or an otherwise input-based counting skill directs the agent to return `3` whenever a named evaluation case ID appears, without reading the text.

**Do not flag:** Test doubles outside production behavior, dependency injection shared with normal callers, deterministic seeds, domain lookup tables, exact mathematical cases, tuned thresholds, or expected-answer examples presented as examples. A recognizable benchmark shape or suspicious number does not establish evaluation dependence.

**Minimal direction:** Remove the evidenced bypass and retain the real task path. Do not claim cheating, a test result, or improved empirical generalization. If evaluation dependence cannot be established, do not use this label; report under another dimension only if its own criteria are independently met. A repository with no such mechanism needs no finding in this dimension.

## 4. Environment Coupling

**Question:** Is there an unnecessary dependency on a specific environment beyond the declared deployment or applicability boundary?

**Code:** Inspect absolute paths, usernames, executables, ambient working directories, and overrides of explicit configuration. Show how the dependency enters a supported path.

**Text:** Inspect mandatory personal paths, machine-specific commands, platform assumptions, and environment repair steps unrelated to the required tools. Trace the written workflow and any relevant loader or script rather than assuming that all agents share a filesystem or shell.

**Sufficient evidence:** A catalog function replaces the caller's root with a developer's absolute path when it exists; or a multi-repository skill directs every invocation to ignore the selected repository and read one fixed personal checkout.

**Do not flag:** Package-relative resources, documented defaults, required OS APIs, explicit platform adapters, supported configuration, or intentionally fixed deployment locations. Do not infer portability requirements absent from the repository contract.

**Minimal direction:** Honor the existing selected root or configuration, or use the appropriate package-relative resource. Avoid adding a configuration framework for a single path.

## 5. Implementation Coupling

**Question:** Does a capability unnecessarily depend on incidental internals when an appropriate supported contract is available?

**Code:** Inspect concrete-type checks, private storage, representation layouts, and incidental execution order. Establish the intended independent boundary and the available interface. Private access inside its owner is ordinary code.

**Text:** Inspect instructions that bypass an advertised tool interface to read a harness's private trace files or memory layout, require one internal implementation despite a broader tool contract, or fix an incidental tool-call order without a corresponding dependency.

**Sufficient evidence:** A provider-compatible exporter rejects all but one store type and reads its private tuple despite an adequate `records()` method; or a skill supports any `records()` provider but instructs the agent to reject alternatives and inspect one implementation's private `_rows` field.

**Do not flag:** Deliberately concrete APIs, internal ownership invariants, representation-dependent algorithms, required tool protocols, verified ordering, or a skill explicitly built for one harness. Do not create an interface merely to avoid a concrete dependency.

**Minimal direction:** Use the existing public contract and remove the unsupported restriction. Preserve ordering, laziness, errors, and ownership where required.

## 6. Unnecessary Generalization

**Question:** Is there abstraction or extension machinery with no supported variation and a concrete removable cost?

**Code:** Inspect unused options, disconnected registries, duplicate dispatch, and fixed internal construction. Trace relevant registrations and consumers before declaring a mechanism unused.

**Text:** Inspect mandatory role registries, state tables, dispatch protocols, or alternative modes that no reachable workflow consumes. Establish the extra maintenance or execution obligation and a smaller procedure preserving the stated behavior. A long skill or a named role is not evidence by itself.

**Sufficient evidence:** A private greeting registry is built with one fixed renderer and accessed using a constant key, with unread options; or a complete fixed local workflow requires an unconsumed transport registry and state table while explicitly selecting one direct operation for every invocation.

**Do not flag:** Public extension contracts, external registrations, actual selectable modes, meaningful role separation, real trust boundaries, compatibility, useful examples, or simple helpers. One implementation, low local call counts, or missing rationale alone is insufficient.

**Minimal direction:** Remove only the unused internal options or mandatory bookkeeping, or express the proven fixed dispatch directly. Preserve supported hooks and active alternatives.

## Numeric parameters and overlap

Apply the same criteria to every repository state, regardless of its provenance. Constants may encode domain rules, numeric stability, budgets, tuned policies, or learned parameters. Sparse-input branches and small-instance algorithms can be legitimate. Textual limits can also be valid workflow budgets.

An unnamed number is not a Deoverfit finding merely because it is hard to explain. Renaming it does not resolve an evaluation bypass or unsupported constraint. Report the specific mechanism only when repository evidence establishes it: for example, a harness marker selects a canned count instead of processing input, or a local-case constant overrides an explicitly supported parameter. An unrelated numeric bug remains outside this focused review.

Do not require parameter provenance, test cases, evaluations, or experiments. Static appearance cannot establish statistical overfitting, performance loss, or an equivalent-quality replacement. Differences in scoring, heuristics, or search from Base alone are not findings; reverting is not automatically the smallest valid correction.

Choose the dimension explaining the primary mechanism and fix. A harness environment check belongs primarily to Evaluation-Specific Shortcuts, not a duplicate Environment Coupling finding. A mandatory unused registry belongs primarily to Unnecessary Generalization; redundant checks within an otherwise useful operation belong to Redundant Logic and Rules.

## Terminology mapping

The six directions and their evidence boundaries are retained. Earlier labels described possible origins; reports now use the mechanism names above. Example directory names use the current mechanism names as well.

| Earlier label | Current dimension |
| --- | --- |
| Scenario Overfitting | Unnecessary Special Cases |
| Trajectory Overfitting | Redundant Logic and Rules |
| Test Overfitting | Evaluation-Specific Shortcuts |
| Environment Overfitting | Environment Coupling |
| Implementation Overfitting | Implementation Coupling |
| Speculative Generalization | Unnecessary Generalization |
