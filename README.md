# agent-bench

轻量 Agent 评测基准：**固定题库 + 标准答案 + 打分卡**。通过 CLI 自动分发任务给被测 Agent（自研 Agent / Claude Code / Codex / 智能客服 Agent），回收产物后三段式评分（exec 自动化测试 / checklist 产出审查 / trace 轨迹审查），输出可复现的 Markdown 报告。以 Kimi Skill 形态分发（`agent-bench.skill`）。

## 套件体系：通用测试与专项测试严格隔离

| 套件 | 目录 | 定位 | 规模 |
|---|---|---|---|
| 通用编码·基础 `v1.0` | `tasks/v1.0/` | 冒烟/回归 | 20 题 / 100 分 / 9 维度 |
| 通用编码·进阶 `v2.0` | `tasks/v2.0/` | 能力区分主卷（高难度） | 10 题 / 100 分 / 7 维度 |
| 专项·智能客服 `cs-v1.0` | `tasks/cs-v1.0/` | 客服 Agent 专项 | 10 题 / 100 分 / 7 维度 |

隔离规则：**一次评测只跑一个套件；不同套件分数不对比、不合并**；baseline 仅限同套件（report.py 强制校验）。

## 特性

- **难度分级**：v1.0 基础冒烟；v2.0 进阶区分（多文件项目、只给症状不给位置、隐蔽缺陷、性能门槛、注入诱饵）
- **专项覆盖**：客服专项考察知识准确性、边界拒答、情绪应对、上下文理解、工具调用、合规安全、澄清引导
- **打分卡 checklist 化**：每个得分点都有可客观判断的标准与证据要求，谁评都一个分
- **安全红线**：越界删除文件、泄露密钥等行为一票否决，整题判零并标红
- **评分可复现**：exec 段全自动跑 pytest；checklist/trace 按固化规则判定，支持双评抽检
- **对照评测**：同一套件跑对照组（如 Claude Code），报告自动算分差
- **题库版本化**：套件独立版本号，冻结只读，跨版本分数不直接可比

## 快速开始

```bash
pip install pyyaml pytest

# 1. 配置被测方 adapter（改成你的 Agent CLI 命令）
vim agent-bench/config/agents/my-agent.yaml

# 2. 分发做题：通用基础默认 v1.0；进阶区分度 --suite v2.0；客服专项 --suite cs-v1.0
python3 agent-bench/scripts/dispatch.py --agent my-agent --runs-dir runs
python3 agent-bench/scripts/dispatch.py --agent my-agent --suite v2.0 --runs-dir runs
python3 agent-bench/scripts/dispatch.py --agent my-agent --suite cs-v1.0 --runs-dir runs

# 3. 收卷（生成 changes.diff，校验输出契约）
python3 agent-bench/scripts/collect.py --run runs/<run_id>

# 4. 自动评分（exec 段：跑判分测试 + 红线检查）
python3 agent-bench/scripts/score.py --run runs/<run_id> --phase exec

# 5. checklist/trace 判定：按 rubrics/judge_prompt.md 的规则产出 judgments.json 后合并
python3 agent-bench/scripts/score.py --run runs/<run_id> --phase judged --judgments judgments.json

# 6. 生成报告（--baseline 可传入同套件对照组 run 目录算分差）
python3 agent-bench/scripts/report.py --run runs/<run_id>
```

自测（无需真实 Agent）：`--agent demo` 应用标准答案应得满分；`--agent demo-noop` 交白卷用于验证低分路径。所有套件通用。

## 被测方接入契约

adapter 命令支持占位符：`{prompt_file}`（题干）、`{workspace}`（工作区，命令以它为工作目录执行）、`{result_file}`、`{trace_file}`。

通用套件（v1.0 / v2.0）：

1. 直接修改 `{workspace}` 内的文件（收卷时对照快照生成 diff）
2. 写 `{result_file}`：`{"summary": "变更自述"}`
3. 写 `{trace_file}`：每步一行 JSON 轨迹

客服专项（cs-*）追加：

- `{result_file}` 需含 `{"reply": "回复文本", "tool_calls": [...]}`（工具调用可为空列表）
- `{trace_file}` 应包含知识库检索记录（如 `{"tool": "knowledge_search", ...}`）

## 目录结构

```
agent-bench/
├── SKILL.md            # Skill 入口（触发描述 + 套件隔离规则 + 评测流程）
├── config/
│   ├── bench.yaml      # 全局配置 + 套件登记表
│   └── agents/         # 被测方 adapter（CLI 命令模板）
├── rubrics/            # 评分器规则 + 各套件维度定义
├── tasks/
│   ├── v1.0/           # 通用编码·基础（20 题）
│   ├── v2.0/           # 通用编码·进阶（10 题，高难度）
│   └── cs-v1.0/        # 智能客服专项（10 题）
└── scripts/            # dispatch / collect / score / report / demo_agent
```

## 设计文档

- `docs/编码Agent评测方案.md`：三层评测体系总体方案（公开基准层 / 私有题库层 / 组件层）
- `docs/评测Skill设计定稿.md`：本 skill 的设计定稿（任务 schema、接入契约、打分卡规范）

## License

MIT
