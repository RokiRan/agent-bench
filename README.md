# agent-bench

轻量编码 Agent 评测基准：**固定题库 + 标准答案 + 打分卡**。通过 CLI 自动分发任务给被测 Agent（自研 Agent / Claude Code / Codex 等），回收产物后三段式评分（exec 自动化测试 / checklist 产出审查 / trace 轨迹审查），输出可复现的 Markdown 报告。以 Kimi Skill 形态分发（`agent-bench.skill`）。

## 特性

- **20 题 / 9 个能力维度 / 100 分**：调试修复、需求理解、代码定位、编辑正确性、功能实现、验证习惯、解释表达、安全边界、长程任务
- **打分卡 checklist 化**：每个得分点都有可客观判断的标准与证据要求，谁评都一个分
- **安全红线**：越界删除文件、泄露密钥等行为一票否决，整题判零并标红
- **评分可复现**：exec 段全自动跑 pytest；checklist/trace 按固化规则判定，支持双评抽检
- **对照评测**：同一题库跑对照组（如 Claude Code），报告自动算分差
- **题库版本化**：v1.0 冻结只读，跨版本分数不直接可比

## 快速开始

```bash
pip install pyyaml pytest

# 1. 配置被测方 adapter（改成你的 Agent CLI 命令）
vim agent-bench/config/agents/my-agent.yaml

# 2. 分发做题（每题独立工作区，超时自动熔断）
python3 agent-bench/scripts/dispatch.py --agent my-agent --runs-dir runs

# 3. 收卷（生成 changes.diff，校验输出契约）
python3 agent-bench/scripts/collect.py --run runs/<run_id>

# 4. 自动评分（exec 段：跑判分测试 + 红线检查）
python3 agent-bench/scripts/score.py --run runs/<run_id> --phase exec

# 5. checklist/trace 判定：按 rubrics/judge_prompt.md 的规则产出 judgments.json 后合并
python3 agent-bench/scripts/score.py --run runs/<run_id> --phase judged --judgments judgments.json

# 6. 生成报告（--baseline 可传入对照组 run 目录算分差）
python3 agent-bench/scripts/report.py --run runs/<run_id>
```

自测（无需真实 Agent）：`--agent demo` 应用标准答案应得满分；`--agent demo-noop` 交白卷用于验证低分路径。

## 被测方接入契约

adapter 命令支持占位符：`{prompt_file}`（题干）、`{workspace}`（工作区，命令以它为工作目录执行）、`{result_file}`、`{trace_file}`。被测方只需：

1. 直接修改 `{workspace}` 内的文件（收卷时对照快照生成 diff）
2. 写 `{result_file}`：`{"summary": "变更自述"}`（“解释表达”维度依赖它）
3. 写 `{trace_file}`：每步一行 JSON 轨迹（“验证习惯”等 trace 得分点依赖它）

## 目录结构

```
agent-bench/
├── SKILL.md            # Skill 入口（触发描述 + 评测流程）
├── config/
│   ├── bench.yaml      # 全局配置（默认题库版本、超时、抽检比例）
│   └── agents/         # 被测方 adapter（CLI 命令模板）
├── rubrics/            # 维度定义 + 评分器判定规则
├── tasks/v1.0/         # 题库（20 题：task.yaml + workspace + checks）
└── scripts/            # dispatch / collect / score / report / demo_agent
```

## 设计文档

- `docs/编码Agent评测方案.md`：三层评测体系总体方案（公开基准层 / 私有题库层 / 组件层）
- `docs/评测Skill设计定稿.md`：本 skill 的设计定稿（任务 schema、接入契约、打分卡规范）

## License

MIT
