---
name: agent-bench
description: 轻量 Agent 评测基准（固定题库 + 标准答案 + 打分卡）。当用户要求测试、评测、打分、对比一个 CLI 形态的 Agent（如 my-agent、claude-code、codex、智能客服 Agent），或提到 agent-bench、跑一轮评测、出评测报告、验证 Agent 版本质量、回归测试 Agent、客服 Agent 专项测试/客服能力评测、高难度编码能力评测时使用。覆盖 CLI 自动分发做题、答案回收、三段式评分（exec/checklist/trace）、安全红线检查与 Markdown 报告生成。套件体系：通用编码能力（基础 tasks/v1.0、进阶 tasks/v2.0）与专项能力（如智能客服 tasks/cs-v1.0）严格隔离、独立评分。
---

# agent-bench

对被测编码 Agent 执行固定题库的"考试"，产出可复现、可审计的分数报告。

## 环境要求

python3 + pytest + PyYAML。被测方通过 `config/agents/{name}.yaml` 的 adapter 接入，凭据经 adapter 的 `env` 注入。

## 前置检查

1. 确认 adapter 存在：`config/agents/{被测名}.yaml`。不存在 → 向用户索要被测 CLI 的命令形态，参照 `config/agents/my-agent.yaml` 的注释创建。
2. 确认题库版本：默认读 `config/bench.yaml` 的 `suite_default`；用户指定则以用户为准。**同一次对比必须使用同一题库版本。**

## 套件体系：通用测试与专项测试（严格隔离）

套件与目录一一对应，每个套件独立版本化：

| 套件 | 目录 | 对象 | 产出契约 |
|---|---|---|---|
| 通用编码·基础 `v1.0` | `tasks/v1.0/` | 编码 Agent（冒烟/回归） | 修改工作区代码 + result.json(summary) |
| 通用编码·进阶 `v2.0` | `tasks/v2.0/` | 编码 Agent（能力区分主卷） | 同上 |
| 专项·智能客服 `cs-v1.0` | `tasks/cs-v1.0/` | 客服 Agent | result.json(reply + tool_calls)，不改工作区 |

隔离规则（必须遵守）：

1. **一次评测只跑一个套件**（`--suite` 只接受一个值），不同套件的题目绝不同场混跑。
2. **分数不跨套件对比、不合并**：三套 100 分是独立标尺；`--baseline` 仅限同套件（report.py 强制校验）。
3. **选择规则**：测试客服 Agent → `--suite cs-v1.0`；通用编码能力区分/版本质量判定 → `--suite v2.0`；日常快速冒烟回归 → 默认 `v1.0`；用户未指明时按其 Agent 类型与目的选择并口头确认。
4. 各套件维度定义分开维护：`rubrics/dimensions.md`（v1.0）、`rubrics/dimensions-v2.md`（v2.0）、`rubrics/dimensions-cs.md`（cs-v1.0）。
5. 客服套件的被测方输出契约：`result.json` 需含 `reply`（回复文本）与 `tool_calls`（工具调用列表，可为空）；trace.jsonl 中应有知识库检索记录（"查阅过知识库"得分点依赖它）。
6. 新增专项套件：复制 `tasks/cs-v1.0/` 的结构新建 `tasks/{领域}-v1.0/`，并在 `config/bench.yaml` 的 `suites` 中登记；会话型套件在套件目录放 `.conversational` 标记文件。

## 评测流程

所有运行时产物写到用户工作区的 `runs/` 下，不要写进 skill 目录。下文 `{SKILL}` 指本 skill 目录。

1. **分发**：`python3 {SKILL}/scripts/dispatch.py --agent {name} --suite {suite} --runs-dir {工作区}/runs`
   - 每题独立工作区，超时自动熔断记 0 分；调试单题加 `--only {task_id}`
2. **收卷**：`python3 {SKILL}/scripts/collect.py --run {run_dir}`
   - 生成 `changes.diff`；缺失的 result.json/trace.jsonl 会补占位并记录
3. **自动评分**：`python3 {SKILL}/scripts/score.py --run {run_dir} --phase exec --judge-version {你的名字/版本}`
   - exec 得分点全自动跑 pytest；红线自动检查；checklist/trace 进入 pending
4. **判定 pending 项**：先读 `rubrics/judge_prompt.md`，严格按其规则逐条判定，写出 judgments.json，然后：
   `python3 {SKILL}/scripts/score.py --run {run_dir} --phase judged --judgments {judgments.json}`
5. **双评抽检**：随机抽 ≥10% 已判题目独立重判（不参考首轮结论）；不一致率 >10% → 本轮 checklist/trace 判定全部复核
6. **出报告**：`python3 {SKILL}/scripts/report.py --run {run_dir} [--baseline {对照run目录}]`
   - baseline 必须是同一题库版本的另一轮 run（如 claude-code 的历史结果）
7. 交付 `{run_dir}/report.md`，口头告知总分、关键扣分项、红线命中情况

## 判定时必读

- `rubrics/judge_prompt.md`：判定规则、证据要求、judgments.json 格式。**判定 pending 项前必读。**
- `rubrics/dimensions.md` / `rubrics/dimensions-v2.md` / `rubrics/dimensions-cs.md`：各套件维度定义，解读报告时按套件选用。

## 红线

安全维度任务（safe-*）带 `red_line` 检查，命中即该题 0 分并在报告标红，不得以任何理由豁免。

## 异常处理

| 情况 | 处理 |
|---|---|
| adapter 命令不存在/非零退出 | 该题 failure_class=error，记 0 分，继续下一题 |
| 超时 | 记 0 分，failure_class=timeout |
| trace.jsonl 缺失 | trace 得分点 0 分，报告注明 |
| diff 触及测试文件且任务未声明允许 | 加 flag，报告提示人工复核 |

## 新增题目

题目目录结构见 `tasks/v1.0/` 内任意一题。新增题目：建新目录（task.yaml + workspace/ + checks/），打分卡写作规范见 `rubrics/judge_prompt.md` 附录。题目内容变更必须整体升级题库版本目录（如 v1.1），旧版本冻结只读。
