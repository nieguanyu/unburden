# Review dimensions

These six lenses apply to both comparison and snapshot reviews. They do not establish that a program is statistically overfit, reveal its development history, or require one finding per category. A finding needs Candidate code evidence, an applicable contract, a concrete consequence, and a minimal useful change. Comparison findings must also be tied to the delta; snapshot findings describe existing issues without claiming they are newly introduced. Use the reporting rules in [review-guidelines.md](review-guidelines.md).

## 1. Scenario Overfitting

**Question:** Does a general capability now require assumptions from one application that its contract does not require?

Look for application names, tenant identifiers, schema rewrites, domain imports, or implicit defaults embedded in shared code. Trace how the assumption affects a supported caller. A specific identifier is a lead, not proof.

**Evidence sufficient for a finding:** A general JSON encoder rewrites one application's field names while its contract promises to preserve input keys. Candidate code shows the rewrite and its effect on the public encoder. In comparison mode, the diff also ties the issue to the change.

**Do not flag:** An explicitly named application adapter, a business rule in a domain module, a documented schema migration, or a capability intentionally restricted to one domain. Do not replace a valid specialized API with an invented universal one.

**Minimal direction:** Keep the shared behavior faithful to its contract; place a necessary application mapping in the existing application boundary or make the already-required choice explicit.

## 2. Trajectory Overfitting

**Question:** Is there correction-shaped residue whose redundancy or contract mismatch is provable from the final code?

The dimension's name refers to a possible source of residue, not an observable history. Inspect duplicated exclusions, guards rendered unreachable by earlier validation, obsolete fallback branches, and user-facing phrases such as “without X” when they contradict the ordinary output contract. Those shapes alone are not findings.

**Evidence sufficient for a finding:** An exhaustive allowlist rejects an ingredient before a later check for that same excluded ingredient; the second check cannot run for the documented input type. Or a new correction-specific phrase is appended to an output whose documented format excludes it.

State “the guard is unreachable after the allowlist” rather than “the agent added this after a user complained.” Do not seek intermediate commits or conversations to validate the category. If the available source cannot establish an issue, omit it; a snapshot review cannot identify when the residue appeared.

**Do not flag:** Necessary validation at an independent trust boundary, a reachable fallback with distinct semantics, a compatibility guard, a required exclusion, or a legitimate user-facing safety label. Repeated checks across mutable state or separate processes may have different purposes.

**Minimal direction:** Remove only the provably redundant check or restore the intended output. Preserve the effective validation, compatibility behavior, and required exclusions.

## 3. Test Overfitting

**Question:** Does production behavior depend on the test or evaluation context instead of the supported input semantics?

Inspect harness detection, fixture IDs, canned results, and narrow input branches that bypass the actual computation. Existing tests and fixture files may be read for evidence, but do not add, change, or run them.

**Evidence sufficient for a finding:** A public word counter returns a constant whenever `PYTEST_CURRENT_TEST` is set. An algorithm returns a stored answer selected by a fixture identifier rather than solving the documented input problem. Identify an actual code path and its consequence; a familiar-looking constant is insufficient.

**Do not flag:** Explicit test doubles outside the production path, deterministic seeds, supported dependency injection, lookup tables that implement a domain contract, known mathematical cases, or tuned algorithm thresholds. A known benchmark shape alone does not prove test-specific behavior.

**Minimal direction:** Remove the harness or fixture shortcut and retain the real computation. Do not demand new evaluations or assert unmeasured generalization improvements.

## 4. Environment Overfitting

**Question:** Does the implementation accidentally depend on one developer's environment beyond its declared deployment contract?

Inspect machine-specific paths, usernames, local executables, ambient working directories, and configuration overrides. Show how an undeclared dependency enters a supported path. Do not assume cross-platform support if the project only supports one platform.

**Evidence sufficient for a finding:** A function that accepts a catalog root now replaces it with a developer's absolute path whenever that local file happens to exist, making caller configuration ineffective.

**Do not flag:** Package-relative resources, documented configuration and defaults, required OS APIs, explicit platform adapters, or an intentionally fixed deployment location. Environment configuration can be a legitimate interface.

**Minimal direction:** Honor the existing explicit configuration or use an appropriate package-relative resource location. Avoid creating a new configuration framework for a single accidental path.

## 5. Implementation Overfitting

**Question:** Is a capability tied to incidental implementation details when a suitable supported contract is already available?

Inspect concrete-type checks, private-state access, storage layouts, and assumptions about incidental execution order. Establish which boundary is meant to be independent and what existing interface satisfies the capability. Private access inside its owning implementation is ordinary code.

**Evidence sufficient for a finding:** An exporter promised to accept providers with `records()` rejects everything except one concrete store class and reads that class's private tuple, although `records()` supplies exactly the needed data.

**Do not flag:** Internal methods using their own state, a deliberate concrete-type API, ownership invariants, necessary representation-specific algorithms, or verified ordering requirements. Do not request an interface merely to avoid every concrete dependency.

**Minimal direction:** Use the available public contract or remove the unnecessary restriction. Preserve ordering, laziness, error behavior, and ownership where those are part of the contract.

## 6. Speculative Generalization

**Question:** Is there extension machinery with no reachable variation and a concrete simplification that preserves the current contract?

Inspect unused options, disconnected registries, duplicate dispatch layers, and abstraction stacks whose internal choices are all fixed. Trace all relevant registration and call sites before claiming they are unused. A small diff, one implementation, or missing documentation alone does not establish unnecessary complexity.

**Evidence sufficient for a finding:** A private registry is recreated inside every greeting call with one fixed renderer, queried with a constant key, and has no registration path; an options object carries fields never read by any reachable code. The fixed behavior can be expressed directly while retaining every supported argument.

**Do not flag:** A public extension contract, multiple reachable implementations, external registrations, dependency inversion at a real boundary, required compatibility, or a simple helper that improves clarity. “We might not need it” is not evidence.

**Minimal direction:** Collapse the demonstrably fixed dispatch or remove unused internal options. Do not redesign the API or remove supported extension hooks based only on local call counts.

## Evolved algorithms and overlap

Base and Candidate are source-version roles. Candidate may be a self-evolved algorithm submitted to improve solution quality or runtime, with no feature implementation task. Review Candidate alone in snapshot mode or against an explicitly supplied Base in comparison mode. Individual algorithm files are sufficient inputs; evolution traces and evaluation scores are not required.

Apply the same evidence bar to evolved algorithm code. A constant may be a meaningful threshold, a numerical tolerance, or a learned parameter. Branches for sparse inputs or small instances may be valid algorithms. Do not infer overfitting from these shapes or claim that a simpler alternative has the same quality or runtime without evidence available in the code and contract.

Changes to heuristics, scoring, and search are expected in this setting. A difference from Base is not by itself evidence of a defect or overfitting, and reverting such a change is not automatically a valid simplification.

Report observable mechanisms such as a fixture-specific answer override, an ignored solver parameter, or an unnecessary dependency on a local file. Describe the mechanism rather than an empirical performance conclusion. Preserve intentional heuristics unless the finding establishes a separate concrete problem.

Choose the primary dimension that best explains the fix. For example, a test-harness environment check is usually Test Overfitting; it does not need a second Environment Overfitting finding. An unreachable defensive branch may also be implementation redundancy; report it once.
