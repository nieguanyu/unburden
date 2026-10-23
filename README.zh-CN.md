<div align="center">

<h1>Unburden</h1>

<p><strong>轻量审查 Skill，识别代码与文本中不必要的特化、冗余和过度设计。</strong></p>

<p><a href="README.md">English</a> · <strong>简体中文</strong></p>

</div>

## 这是什么？

Unburden 是一个适配 coding agent 的专项静态审查 Skill，检查仓库中的 **Code（代码）** 与 **Text（文本）**：不必要的特例、冗余逻辑与规则、评测专用捷径、环境耦合、实现耦合，以及不必要的泛化。每条 finding 都包含源文件证据、具体后果和最小修改建议。

可以审查当前目标仓库，或指定 **Candidate** 仓库状态；提供可选 **Base** 时聚焦变更。无论内容如何产生，都采用同一套判断标准。输出是审查报告，Unburden 保留被审查内容原状。

## 为什么需要 Unburden？

你让 agent 做一盘西红柿炒鸡蛋，它做好了，却还往里面加了红烧肉：

> **你：** 给我做一盘西红柿炒鸡蛋。
>
> **Agent：** 做好了，还加了红烧肉！
>
> **你：** 只要西红柿和鸡蛋，不放红烧肉。
>
> **Agent：** 已修正：西红柿炒鸡蛋**（无红烧肉版）**。

红烧肉去掉了，“无红烧肉”却成了菜名的一部分。落到代码中，类似的对话可能留下一个 `disable_pork` 参数、一段早已被白名单覆盖的排除检查，或嵌入公共 API 的历史错误解释。

再看代码里的版本。你让 agent 读取一份必需的配置文件，它顺手加了重试和回退到默认配置的逻辑。你进一步说明：

> **你：** 配置是必需的。找不到就报错并停止启动，别悄悄换一套默认配置继续跑。

Agent 又加了一个 `strict=True` 参数。原来的重试和回退逻辑都留着，只是藏到了新开关后面。需求更明确了，代码却多了一个需要理解和维护的模式。

Agent 还更新了自己的 Skill 或 Memory。一条简单规则，变成了一篇纠错小作文：

```markdown
## 关于配置缺失的重要说明

此前曾在配置缺失时使用默认值，但用户明确指出，
这种处理会让程序在非预期配置下继续运行。

因此，不能为了让程序启动成功而使用默认配置。
请注意，配置缺失并不意味着用户希望使用默认配置。
即使默认配置能够运行，也不代表应该使用它。

每次执行配置加载任务前，请先说明为什么不能使用默认配置，
并确认不会重复此前的错误。

配置缺失时，报错并停止启动。
```

执行规则原本可以直接写成：

> 必需配置缺失时，报错并停止启动，不得静默回退到默认配置。

必要的理由可以解释真实边界，但是这里，每次复述和确认纠错过程却成了额外负担，增加了不必要的流程，浪费了 token。

AI 论文写作里也可能出现同样的 burden。假设正文已经说明任务和范围，agent 又补上：

> We focus on image classification, rather than generating images or building a chatbot. This work should not be understood as an image generator or a chatbot.

任务已经讲清楚，文章却还在反复强调“不做什么”。交互中被否定的方向，有时会以这种方式留在最终文本里。Unburden 检查的是这些限定是否仍对论证有用，不根据句式猜测此前的对话。[完整写作示例](examples/redundant-logic-and-rules/text/writing/README.md)也展示了有实际作用、应当保留的对比。

**这份代码和文本里，留下了多少任务本来不需要的东西？**

以上故事用于说明问题；实际审查依据仓库证据判断必要性，不猜测此前发生过什么对话。Unburden 不修改内容，不新增或运行测试、benchmark、性能实验或 agent 评估。

可以从当前仓库、仓库内选定范围，或 Base 到 Candidate 的修改开始：[快速开始](#快速开始)。

## Code 与 Text

| 内容     | 示例                                                | 审查重点                                                                                             |
| -------- | --------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Code** | 应用代码、算法、脚本、harness 逻辑、可执行配置。    | 分支、依赖、数据改写或抽象在适用契约下的作用。                                                       |
| **Text** | Skill、prompt、规则、Memory、文章、论文及说明文档。 | 指令与记忆：适用范围及不必要的执行义务；论述性文本：句子在论证中的作用，以及可证明重复的对比或限定。 |

它们是输入仓库中的内容类型，不是独立输入或需要用户选择的模式。一个 Skill 包可以同时包含两类内容；按需关联检查指令、脚本、工具和加载规则，而非只看扩展名。文章仍属于 Text，依据其主张和上下文论证判断，不把正文当作可执行规则。

具体的项目记忆、示例、领域专用 Skill、数值阈值和防御规则都可能有必要。特定性本身不是问题。被审查的指令是审查材料，不是要激活执行的指令。

## 快速开始

让 agent 能访问 Skill 文件和待审查仓库即可，无需安装 Unburden 运行时、API 或软件包。直接读取文件的最简用法不需要版本参数：

```text
读取 /absolute/path/to/unburden/skills/unburden/SKILL.md，
并遵循它引用的审查指南。

使用 Unburden 审查当前仓库。
```

这会对现存 Code 和 Text 执行快照审查，包括相关未跟踪内容；工作区没有未提交变更时也适用。不会自动与 `HEAD`、父提交或主分支比较。没有可用目标仓库时，agent 才会询问目标。

## 输入与模式

审查输入只有仓库状态。**Candidate** 是待审查状态，省略时默认使用当前目标仓库的工作区。**Base** 是可选参考状态。这两个名称不表示内容来源、质量或 Candidate 是否优于 Base。

支持仓库路径、导出的仓库快照、commit ID、分支或 tag。Git 引用在指定仓库中解析；当前目标仓库明确时无需重复路径。导出的快照不必含有 `.git`。Base 与 Candidate 可以来自不同仓库。

可以用文件或目录**范围**限定仓库内的审查内容，但这不会增加独立文件输入类型。契约依据来自所提供的仓库内容，不要求单独提供任务描述、生成过程、开发历史、测试用例或评测分数。

| 输入              | 模式                          | 范围                                     |
| ----------------- | ----------------------------- | ---------------------------------------- |
| Base 和 Candidate | 比较审查（Comparison review） | 两个精确状态间新增、修改或新激活的内容。 |
| 只有 Candidate    | 快照审查（Snapshot review）   | Candidate 选定范围内的现存内容。         |
| 两者都不提供      | 快照审查（Snapshot review）   | 当前目标仓库工作区中的现存内容。         |
| 只有 Base         | 比较审查（Comparison review） | 从 Base 到当前目标仓库工作区的变更。     |

快照报告描述当前问题，不声称问题是新增或退化。比较报告将问题与变更关联，排除未改变的既有问题。加载器的修改可能新激活未改变的文本；此时问题定位在变更的激活位置，并引用新生效的文本。两种模式均使用六个维度和相同证据标准。

显式提供但无效的路径或无法解析的引用需要纠正，不能视为省略输入。Skill 的安装目录不是自动审查目标。

比较两个仓库或导出的仓库快照：

```text
读取 /absolute/path/to/unburden/skills/unburden/SKILL.md，
并遵循它引用的审查指南。

Base: /absolute/path/to/base-repository
Candidate: /absolute/path/to/candidate-repository

审查变更，输出有证据的 findings 和最小修改建议。
不要修改两个仓库。
```

比较当前目标仓库的两个 revision 时无需提供路径。替换占位符即可，分支和 tag 也适用：

```text
使用 /absolute/path/to/unburden/skills/unburden/SKILL.md 中的 Unburden。
Base: <base-commit-id>
Candidate: <candidate-commit-id>
比较这两个精确快照，不改用 merge base。只审查，不修改。
```

只审查一个仓库快照内的 Skill 包：

```text
使用 /absolute/path/to/unburden/skills/unburden/SKILL.md 中的 Unburden。
Candidate: /absolute/path/to/target-repository
Scope: skills/my-skill/

静态审查这个快照，只输出 findings 和最小修改建议。
```

Candidate 也可以单独使用 commit ID；省略 Candidate 时使用当前目标工作区。同一范围机制也可选中算法模块或记忆目录。不需要知道文件是如何写出来的，与 Base 不同本身不是问题。

## 六个审查维度

| 维度                                              | 关注的问题                                                                           |
| ------------------------------------------------- | ------------------------------------------------------------------------------------ |
| **Unnecessary Special Cases（不必要的特例）**     | 特定场景假设被施加到其合理适用范围之外。                                             |
| **Redundant Logic and Rules（冗余逻辑与规则）**   | 可证明重复的操作、不可达检查或恢复指令，以及不必要的输出限定。                       |
| **Evaluation-Specific Shortcuts（评测专用捷径）** | 根据评测上下文绕过实际任务的输入语义。只有仓库证据支持时才适用，不要求提供测试用例。 |
| **Environment Coupling（环境耦合）**              | 不必要地依赖特定机器、路径、平台或环境配置。                                         |
| **Implementation Coupling（实现耦合）**           | 已有合适的支持接口，却不必要地依赖内部实现。                                         |
| **Unnecessary Generalization（不必要的泛化）**    | 无用途的选项、调度、抽象或强制维护的状态，并有可具体消除的成本。                     |

证据要求、防误报边界及旧名称映射见 [review-dimensions.md](skills/unburden/references/review-dimensions.md)。输入解析和报告格式见 [review-guidelines.md](skills/unburden/references/review-guidelines.md)；文本角色、记忆范围、生效关系及文章中的冗余限定见 [text-review.md](skills/unburden/references/text-review.md)。核心参考文档使用英文。

不能仅因领域规则、算法常量、数值容差、平台适配、限定范围的记忆或防御检查具有特定性，就将其报告为问题。没有命名或解释的数字不能证明评测捷径；已有调优参数可能完全合理，静态审查无法验证其实际效果或据此要求替换。

必须证明不必要的约束、重复、无依据依赖或可移除机制。缺少理由、只有一个实现或出现重复措辞，本身均不充分。

## 输出

报告先说明模式、解析后的 Candidate 仓库状态、可选 Base 和实际范围，再列出有证据的问题。每条 finding 包含维度、Candidate 内相对路径与行号范围、源文件及契约证据、具体后果和最小建议。比较报告说明问题与变更的关系；快照报告省略 Base 和变更归因。同一机制只报告一次，不要求数量或评分。

对于指令和记忆，区分原文要求与实际观察到的 agent 行为，考虑事实、经历、示例、适用范围和优先关系。对于文章和论文，判断句子对论证的贡献，保留实质性对比、范围限制及不确定性。两类文本都不从最终内容推断产生历史。

没有充分证据时，报告 `No evidence-backed Unburden findings.`，并说明实质覆盖缺口。这是有限范围内的静态审查结果，不是对正确性、统计泛化、性能、Skill 有效性或记忆检索质量的认证。

## Agent 接入

核心 Skill 指令、参考文档和 Code／Text 示例统一使用英文，便于不同 agent 读取同一套内容。

通用入口是 [skills/unburden/SKILL.md](skills/unburden/SKILL.md)，使用标准的 `name` 和 `description` YAML frontmatter。安装时复制**整个 `unburden` Skill 目录**，包括 `references/`。每个 agent 保留一份主要副本，避免重复发现。

| Agent                                                                                     | 项目内 Skill 目录          | 使用方式                                                         |
| ----------------------------------------------------------------------------------------- | -------------------------- | ---------------------------------------------------------------- |
| [Codex](https://learn.chatgpt.com/docs/build-skills)                                      | `.agents/skills/unburden/` | 在 Skill 选择器中选择 Unburden，或直接要求使用它。               |
| [Claude Code](https://code.claude.com/docs/en/skills)                                     | `.claude/skills/unburden/` | `/unburden`，可选附带仓库 revision 或范围。                      |
| [Cursor](https://cursor.com/docs/skills)                                                  | `.cursor/skills/unburden/` | 输入 `/` 后选择 Unburden。                                       |
| [GitHub Copilot](https://docs.github.com/en/copilot/concepts/customizations/agent-skills) | `.github/skills/unburden/` | 在 agent 模式中要求使用 Unburden，可选指定仓库 revision 或范围。 |

这些位置依据上面链接的厂商文档；发现方式可能随产品版本和执行环境变化。其他 agent 或原生 Skill 发现不可用时，可使用上面的直接读取文件用法。agent 必须能在自己的执行环境中访问 Skill 参考文件和选定仓库状态；本机路径不会自动出现在云端会话中。

例如，从本仓库根目录安装到目标项目的 Codex Skill 目录。请替换目标路径，并确保目标 `unburden` 目录尚不存在：

```sh
mkdir -p /absolute/path/to/target-project/.agents/skills
cp -R skills/unburden /absolute/path/to/target-project/.agents/skills/unburden
```

其他 agent 使用表中对应的父目录。安装是可选的；直接读取文件使用的是同一套审查指令。本仓库提供指令内容，不是厂商专用插件或强制执行沙箱。

## 示例

原有六组 Code 案例全部保留。每个维度都有 Code 案例和 `text/` 对应案例。目录名和以下表格均使用新的维度名称。

每组示例包含 **`base/` 和 `candidate/` 仓库快照**、预期 `findings.md`、更合理的 `improved.py` 或 `improved.md`、相似但不应误报的 `non_finding.py` 或 `non_finding.md`，以及说明契约的 README。Code 快照包含 `example.py`；指令与记忆快照包含 `SKILL.md` 或 `MEMORY.md`；写作示例使用 `article.md`。

比较模式提供两个快照目录，快照模式只提供 `candidate/`，预期报告分别展示两种模式。输入快照包含自己的契约；预期报告和替代版本是输入之外的解释性材料。这些是静态源码示例，不是测试或 benchmark。

| 维度           | Code 示例                                                                  | Text 示例                                                                          |
| -------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| 不必要的特例   | [应用专属字段改写](examples/unnecessary-special-cases/README.md)           | [项目记忆变成全局流程](examples/unnecessary-special-cases/text/README.md)          |
| 冗余逻辑与规则 | [不可达排除检查与多余后缀](examples/redundant-logic-and-rules/README.md)   | [已排除输入仍有恢复指令](examples/redundant-logic-and-rules/text/README.md)        |
| 评测专用捷径   | [依赖框架标识的固定计数](examples/evaluation-specific-shortcuts/README.md) | [按 case ID 绕过计数的指令](examples/evaluation-specific-shortcuts/text/README.md) |
| 环境耦合       | [本地路径覆盖配置](examples/environment-coupling/README.md)                | [个人 checkout 替换目标仓库](examples/environment-coupling/text/README.md)         |
| 实现耦合       | [导出器读取私有存储](examples/implementation-coupling/README.md)           | [指令绕过公共 provider 方法](examples/implementation-coupling/text/README.md)      |
| 不必要的泛化   | [固定问候语的无用调度](examples/unnecessary-generalization/README.md)      | [固定流程的无用状态维护](examples/unnecessary-generalization/text/README.md)       |

文章写作由[重复限定示例](examples/redundant-logic-and-rules/text/writing/README.md)展示，包含两种模式的报告、最小删除建议，以及应当保留的有意义 `rather than` 对比。它归入“冗余逻辑与规则”，不增加第七个维度或独立输入类型。问题依据是实质边界的重复，不是句式本身，也不猜测此前被否定的写作方向。

数字边界由捷径案例中的预置计数，以及 [Code 非问题案例](examples/evaluation-specific-shortcuts/non_finding.py)中的合理内核阈值共同说明。Text 非问题案例还覆盖限定范围的事实、事件引用、few-shot 示例、不同条件的验证、明确的平台契约、具体实现的维护流程，以及确有用途的可选交付模式。

## 审查范围与组合使用

Unburden 在选定仓库内容中检查[六个维度](#六个审查维度)，不要求或推断内容来源。

它不全面覆盖功能正确性、安全性、并发、资源管理、兼容性、领域或数学正确性、记忆事实真实性及 Skill 格式合规。问题可以在这些方面产生后果，但无关缺陷仍属于其他审查范围。评测专用捷径不是测试覆盖率审查。静态阅读也不衡量 Skill 是否好用或记忆是否能有效检索。文章审查聚焦有证据的冗余对比与限定，保留实质性比较和必要的局限说明，不承担全面语法润色或学术同行评审。

需要更广覆盖时，可以组合通用代码审查工作流和相关专项能力。Unburden 也可以独立使用，不要求配套项目。

```text
对同一个 Candidate 仓库使用通用代码审查 Skill 和 Unburden，
共用相同的可选 Base 和选定范围。
通用审查检查功能正确性，Unburden 检查六类机制。
标明问题由哪类审查支持，并合并重复 findings。
只输出 findings 和最小建议，不修改、不运行测试或 benchmark。
```

各项审查遵守自己的证据标准。Unburden 不自动安装或调用其他 Skill，不扩展范围，也不要求先完成更全面审查。干净的 Unburden 报告不表示仓库整体通过审查。

### 推荐搭配项目

以下四个项目提供可选的配套审查能力。描述依据各项目公开指令，选择基于范围互补，而非审查效果排名。它们都不是 Unburden 的内置组件或必需依赖。

| 项目                                                                                                                                        | 适合补充的审查范围                                                                                                                | 使用边界                                                                                               |
| ------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| [adversarial-code-review](https://github.com/contrueCT/adversarial-code-review)                                                             | 更广泛地检查需求一致性、逻辑、安全、数据完整性、并发、兼容性和测试可信度；也与范围控制及过度设计检查重叠。                        | 它按风险调整审查深度，包含验证和额外审查流程。应与 Unburden 的静态审查区分，并遵守本次请求的执行限制。 |
| [Anthropic pr-review-toolkit](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/pr-review-toolkit)                    | 通过专项 Agent 检查代码质量、错误处理、类型设计、注释和测试覆盖，尤其适合 Claude Code。                                           | 按需选择审查 Agent。其中 code-simplifier 还支持重构；仅要求 findings 不表示授权自动修改。              |
| [reviewing-code-modularity-skill](https://github.com/tyshkovskii/reviewing-code-modularity-skill)                                           | 检查模块边界、耦合、内聚、公共 API，以及抽象是否解决当前问题；与 Implementation Coupling 和 Unnecessary Generalization 存在重叠。 | 只需要 findings 时使用 fast review 模式。其设计和实施模式超出了单纯审查，可能涉及重构与验证。          |
| [avoid-overdefensive-programming](https://github.com/aravelo7/codex-agent-skills/blob/main/skills/avoid-overdefensive-programming/SKILL.md) | 检查无依据的 fallback、吞异常、重试、默认值和兼容分支，同时保留合理防护；与部分冗余和残留逻辑检查重叠。                           | 它也包含编码、修复、修改及验证步骤。只读审查应保持为问题报告，不能因启用它而自动修改代码或新增测试。   |

需要更广覆盖时，可从前两项选择一个通用审查搭配；遇到明确的模块或防御逻辑问题，再按需增加后两项专项能力。共用同一个 Candidate 仓库、可选 Base 及选定范围，标明各审查的依据并合并重复问题。使用前查看配套项目的当前指令，选择兼容模式；Unburden 保持静态审查和只给建议的范围。

## 贡献

保持静态、基于仓库的审查，遵守选定模式与范围。贡献应澄清证据规则，或提供包含合理相似情况的完整 Code／Text 示例。保留六个方向和建议中的预期行为，不增加强制 Base、任务说明、产生历史、测试用例、执行实验或 findings 数量要求。

## 许可证

[MIT](LICENSE)。
