# Deoverfit

[English](README.md) | **简体中文**

你让 agent 做一盘西红柿炒鸡蛋，它却端来一盘红烧肉。你纠正它：

> **你：** 我要的是西红柿炒鸡蛋。
>
> **Agent：** 已修正：西红柿炒鸡蛋**（无红烧肉版）**。

那次纠正，成了菜名的一部分。落到代码中，类似的对话可能留下一个 `disable_pork` 参数、一段早已被白名单覆盖的排除检查，或嵌入公共 API 的历史错误解释。

再看代码里的版本。你让 agent 读取一份必需的配置文件，它顺手加了重试和回退到默认配置的逻辑。你进一步说明：

> **你：** 配置是必需的。找不到就报错并停止启动，别悄悄换一套默认配置继续跑。

Agent 又加了一个 `strict=True` 参数。原来的重试和回退逻辑都留着，只是藏到了新开关后面。需求更明确了，代码却多了一个需要理解和维护的模式。

**这份代码里，留下了多少任务本来不需要的东西？**

Deoverfit 是一个适配 coding agent 的轻量代码审查 Skill，检查应用代码修改和演化算法中的不必要特化、冗余与过度设计：这个分支究竟在保护什么？共享 API 带进了谁的假设？这层抽象现在有什么用途？每条 finding 都需要代码证据，并给出最小修改建议。

这些故事用于说明问题形态。实际审查仍依据可见代码和契约判断哪些逻辑不必要，不猜测此前发生过什么对话。Deoverfit 不修改代码，不新增或运行测试、benchmark、性能实验；静态审查无法证明样本外表现。

可以从当前工作区、单个算法文件，或 Base 到 Candidate 的修改开始：[快速开始](#快速开始)。

README 提供中英文版本。核心 Skill 指令、参考文档和源码示例统一使用英文，便于不同 agent 读取同一套内容。

## 审查范围与组合使用

Deoverfit 是围绕[六个审查维度](#六个审查维度)展开的专项审查。它适合检查：共享能力是否混入不必要的应用假设，agent 产生的修改是否带来冗余防御或无用抽象，以及演化算法是否依赖特定测试样例或偶然的环境细节。

它不承诺全面覆盖功能正确性、安全性、并发、资源管理、兼容性，以及领域与数学正确性。Deoverfit 的问题可以在这些方面产生后果，但不能仅因一个无关缺陷很严重，就把它归入 Deoverfit。Test Overfitting 检查的是代码对测试或评测上下文的依赖，不是整体测试覆盖率或测试集质量。

需要更全面的代码审查时，可以搭配通用代码审查 Skill 或工作流，并按需增加安全或领域专项审查。Deoverfit 也可以独立完成其范围内的审查，不强制依赖或内置任何配套 Skill。

例如，已有通用代码审查 Skill 时，可以这样使用：

```text
对同一个 Candidate 使用通用代码审查 Skill 和 Deoverfit，
共用相同的可选 Base、Task 和源码范围。
通用审查检查功能正确性，Deoverfit 按六个维度完成专项审查。
标明每条问题由哪类审查证据支持，并合并同一问题的重复报告。
只输出 findings 和最小修改建议，不修改代码、不运行测试或 benchmark。
```

各项审查分别遵守自己的证据标准。Deoverfit 不会自动安装或调用其他 Skill，不会扩展请求范围，也不会要求先完成其他审查。`No evidence-backed Deoverfit findings.` 只表示本次专项静态审查没有发现证据充分的问题，不代表代码整体通过审查。

### 推荐搭配项目

以下四个项目提供可选的配套审查能力。描述依据各项目公开指令，选择基于范围互补，而非审查效果排名。它们都不是 Deoverfit 的内置组件或必需依赖。

| 项目 | 适合补充的审查范围 | 使用边界 |
| --- | --- | --- |
| [adversarial-code-review](https://github.com/contrueCT/adversarial-code-review) | 更广泛地检查需求一致性、逻辑、安全、数据完整性、并发、兼容性和测试可信度；也与范围控制及过度设计检查重叠。 | 它按风险调整审查深度，包含验证和额外审查流程。应与 Deoverfit 的静态审查区分，并遵守本次请求的执行限制。 |
| [Anthropic pr-review-toolkit](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/pr-review-toolkit) | 通过专项 Agent 检查代码质量、错误处理、类型设计、注释和测试覆盖，尤其适合 Claude Code。 | 按需选择审查 Agent。其中 code-simplifier 还支持重构；仅要求 findings 不表示授权自动修改。 |
| [reviewing-code-modularity-skill](https://github.com/tyshkovskii/reviewing-code-modularity-skill) | 检查模块边界、耦合、内聚、公共 API，以及抽象是否解决当前问题；与 Implementation Overfitting 和 Speculative Generalization 存在重叠。 | 只需要 findings 时使用 fast review 模式。其设计和实施模式超出了单纯审查，可能涉及重构与验证。 |
| [avoid-overdefensive-programming](https://github.com/aravelo7/codex-agent-skills/blob/main/skills/avoid-overdefensive-programming/SKILL.md) | 检查无依据的 fallback、吞异常、重试、默认值和兼容分支，同时保留合理防护；与部分冗余和残留逻辑检查重叠。 | 它也包含编码、修复、修改及验证步骤。只读审查应保持为问题报告，不能因启用它而自动修改代码或新增测试。 |

需要更广覆盖时，可从前两项选择一个通用审查搭配；遇到明确的模块或防御逻辑问题，再按需增加后两项专项能力。共用同一个 Candidate、可选 Base 和 Task 以及源码范围，标明各审查的依据并合并重复问题。使用前查看配套项目的当前指令，选择兼容模式；Deoverfit 保持静态审查和只给建议的范围。

## 快速开始

让 agent 能访问 Skill 文件和待审查源码即可，无需安装 Deoverfit 运行时、API 或软件包。直接读取文件的最简用法不需要版本参数：

```text
读取 /absolute/path/to/deoverfit/skills/deoverfit/SKILL.md，
并遵循它引用的审查指南。

使用 Deoverfit 审查当前工作区。
```

这会对当前代码执行快照审查，包括相关的未跟踪源码；工作区没有未提交变更时也适用。它不会自动与 `HEAD`、父提交或主分支比较。没有可用目标工作区时，agent 才会询问审查目标。

## 输入与模式

**Candidate** 是待审查版本，可以来自功能开发、人工优化，或为提升表现而进行的算法自进化。省略时，默认使用当前目标项目的工作区。**Base** 是可选的参考版本。两者都不必是完整仓库，Candidate 这个名称也不表示它已经优于 Base。

路径不是必填项。源码版本可以是文件、目录、仓库快照、commit ID、分支或 tag。Git 引用在指定仓库中解析；当前目标仓库明确时，也可以直接使用该仓库。commit ID 需要仓库上下文，但上下文已经明确时，无需重复提供仓库路径。

**Task** 是可选的自由文本，描述预期修改、优化目标及需要保留的约束。一句话即可，无需固定模板、开发历史或评测分数。它可以解释从 Base 到 Candidate 想完成什么，也可以说明快照审查中的 Candidate 应具备什么行为。对话中已经明确提供的任务无需重复填写。

Task 不决定审查模式。只提供 Task 时，仍默认对当前工作区进行快照审查。省略 Task 不会阻止对可用目标的审查：以可见契约和代码证据为依据，跳过必须猜测意图才能成立的问题。缺少 Task 本身不是问题。

| 输入 | 模式 | 范围 |
| --- | --- | --- |
| Base 和 Candidate | 比较审查（Comparison review） | 两个指定版本之间新增和修改的代码。 |
| 只有 Candidate | 快照审查（Snapshot review） | Candidate 选定范围内的现存代码。 |
| 两者都不提供 | 快照审查（Snapshot review） | 当前目标项目工作区中的现存代码。 |
| 只有 Base | 比较审查（Comparison review） | 从 Base 到当前目标项目工作区的变更。 |

快照模式只报告当前代码中可观察的问题，不声称问题是新增或退化。比较模式将问题与变更关联，并排除未改变的既有问题。两种模式均保留六个维度，采用相同的证据标准。显式提供但无效的路径或无法解析的引用需要纠正，不能视为省略输入。

比较两个源码目录：

```text
读取 /absolute/path/to/deoverfit/skills/deoverfit/SKILL.md，
并遵循它引用的审查指南。

Base: /absolute/path/to/base-repository
Candidate: /absolute/path/to/candidate-repository
Task: 增加可选的输出格式化，保留字段名和默认行为。

只审查新增和修改代码，输出有证据的 findings 和最小修改建议。
不要修改两个仓库。
```

比较当前目标仓库的两个 commit 时，可以不提供路径。将占位符替换成实际 commit ID；分支和 tag 也适用：

```text
使用 /absolute/path/to/deoverfit/skills/deoverfit/SKILL.md 中的 Deoverfit。
Base: <base-commit-id>
Candidate: <candidate-commit-id>
比较这两个精确版本，不改用 merge base。只审查，不修改代码。
```

审查存为单个源码文件的自进化算法时，可以省略 Base：

```text
使用 /absolute/path/to/deoverfit/skills/deoverfit/SKILL.md 中的 Deoverfit。
Candidate: /absolute/path/to/evolved/algorithm.py

Task: 提升解的质量，同时保留输入格式和可行性规则。
对该快照中的不必要特化、冗余和过度设计进行静态审查。
只输出 findings 和最小修改建议。
```

需要比较变更时，在上一个请求中增加 `Base: /absolute/path/to/reference/algorithm.py`。也可以只提供 Candidate 的 commit ID，单独审查该提交的快照。

将示例路径、版本和 Task 替换成自己的内容；不需要时直接省略 Task。导出的源码快照不必含有 `.git`。无需提供演化轨迹、开发对话、中间提交或评测分数。Task 和其他已提供需求可以帮助判断意图，但不是必填输入。声称表现提升只能作为背景，不能证明泛化能力。

算法 Candidate 可以有意改变启发式、评分或搜索行为。与 Base 不同本身不是问题。Deoverfit 检查代码中的证据，不验证所声称的性能提升，也不要求新增实验。

## Agent 接入

通用入口是 [skills/deoverfit/SKILL.md](skills/deoverfit/SKILL.md)，使用标准的 `name` 和 `description` YAML frontmatter。安装时复制**整个 `deoverfit` Skill 目录**，包括 `references/`。每个 agent 保留一份主要副本，避免重复发现。

| Agent | 项目内 Skill 目录 | 使用方式 |
| --- | --- | --- |
| [Codex](https://learn.chatgpt.com/docs/build-skills) | `.agents/skills/deoverfit/` | 在 Skill 选择器中选择 Deoverfit，或直接要求使用它。 |
| [Claude Code](https://code.claude.com/docs/en/skills) | `.claude/skills/deoverfit/` | `/deoverfit`，可选附带源码版本或范围。 |
| [Cursor](https://cursor.com/docs/skills) | `.cursor/skills/deoverfit/` | 输入 `/` 后选择 Deoverfit。 |
| [GitHub Copilot](https://docs.github.com/en/copilot/concepts/customizations/agent-skills) | `.github/skills/deoverfit/` | 在 agent 模式中要求使用 Deoverfit，可选指定源码版本或范围。 |

这些位置依据上面链接的厂商文档；发现方式可能随产品版本和执行环境变化。其他 agent 或原生 Skill 发现不可用时，可使用上面的直接读取文件用法。agent 必须能在自己的执行环境中访问 Skill 参考文件和选定源码；本机路径不会自动出现在云端会话中。

例如，从本仓库根目录安装到目标项目的 Codex Skill 目录。请替换目标路径，并确保目标 `deoverfit` 目录尚不存在：

```sh
mkdir -p /absolute/path/to/target-project/.agents/skills
cp -R skills/deoverfit /absolute/path/to/target-project/.agents/skills/deoverfit
```

其他 agent 使用表中对应的父目录。安装是可选的；直接读取文件使用的是同一套审查指令。本仓库提供指令内容，不是厂商专用插件或强制执行沙箱。

## 六个审查维度

| 维度 | 关注的问题 |
| --- | --- |
| Scenario Overfitting（场景过拟合） | 更通用的能力中泄漏了项目特定假设。 |
| Trajectory Overfitting（轨迹过拟合） | 当前代码中可证明的纠正式残留、冗余检查或排除逻辑，不推断其产生历史。 |
| Test Overfitting（测试过拟合） | 行为依赖测试框架、样例标识或预存答案，而非输入契约。 |
| Environment Overfitting（环境过拟合） | 偶然依赖开发者的文件系统、机器或本地配置。 |
| Implementation Overfitting（实现过拟合） | 能力依赖偶然的内部类型、存储或执行顺序，而非可用契约。 |
| Speculative Generalization（推测性泛化） | 扩展机制或抽象在当前实现中没有实际用途，并存在可具体消除的复杂性。 |

证据要求与误报边界见 [review-dimensions.md](skills/deoverfit/references/review-dimensions.md)（英文）；输入解析、比较方式和报告格式见 [review-guidelines.md](skills/deoverfit/references/review-guidelines.md)（英文）。

不能仅因领域规则、算法阈值、数值容差、平台适配或防御检查具有特定性，就将它们报告为问题。必须说明不必要的限制、重复、无依据依赖或其他具体后果。没有书面需求本身不能证明过度设计。

## 输出

报告先说明模式、解析后的 Candidate、可选 Base 和实际审查范围，再列出有证据的问题。每条 finding 包含维度、Candidate 文件与行号范围、相关代码和契约证据、具体后果，以及最小修改建议。比较模式还说明问题与变更的关系。快照报告省略 Base，不将问题归因于某次修改。同一根因即使涉及多个维度，也只报告一次，不要求固定数量或评分。

没有足够证据时，报告 `No evidence-backed Deoverfit findings.`。这是有限范围内的静态审查结果，不是对正确性、通用性或性能的认证。无法访问的文件或未覆盖的实质范围需要说明。

## 示例

每个目录包含 `base.py`、`candidate.py`、`findings.md`、`improved.py`、`non_finding.py`，以及说明局部契约的 README。`improved.py` 和 `non_finding.py` 是解释性对照，不是额外必需输入。Python 文件是源码示例，不是测试集或 benchmark。

比较模式提供 `base.py` 和 `candidate.py`。快照模式只提供 `candidate.py`；各目录的 `findings.md` 均包含无需读取 Base 或其他对照实现即可成立的快照报告。

| 维度 | 示例（英文） |
| --- | --- |
| Scenario Overfitting | [通用 JSON 编码器中的应用专属字段改写](examples/scenario-overfitting/README.md) |
| Trajectory Overfitting | [不可达的排除检查与纠正式输出](examples/trajectory-overfitting/README.md) |
| Test Overfitting | [在测试框架环境下返回常量的词数统计](examples/test-overfitting/README.md) |
| Environment Overfitting | [本地路径覆盖调用方配置的目录](examples/environment-overfitting/README.md) |
| Implementation Overfitting | [导出器依赖具体存储类的私有状态](examples/implementation-overfitting/README.md) |
| Speculative Generalization | [固定问候语外的无实际扩展用途的调度机制](examples/speculative-generalization/README.md) |

## 贡献

保持静态审查，并遵守选定模式与源码范围。欢迎澄清证据规则，或提供包含合理相似情况的新示例。修改建议应保留预期行为。不要增加强制 Base 或 Task 输入、执行要求、测试、历史材料或 findings 数量要求。

## 许可证

[MIT](LICENSE)。
