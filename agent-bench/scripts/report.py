#!/usr/bin/env python3
"""报告：汇总 score_detail.json，生成 Markdown 评测报告。

用法：
    python3 report.py --run <run_dir> [--baseline <对照run目录>]
"""
import argparse
import json
from pathlib import Path


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fmt_delta(delta):
    if delta is None:
        return "—"
    return f"{delta:+d}" if delta else "0"


def main():
    ap = argparse.ArgumentParser(description="agent-bench 报告生成器")
    ap.add_argument("--run", required=True, help="run 目录")
    ap.add_argument("--baseline", default=None, help="对照 run 目录（如 Claude Code 的同题库结果）")
    args = ap.parse_args()
    run_dir = Path(args.run)

    detail = load_json(run_dir / "score_detail.json")
    if detail.get("pending"):
        raise SystemExit("还有未判定的 checklist/trace 项，先完成 score.py --phase judged")
    dispatch = load_json(run_dir / "dispatch_index.json")
    collect = load_json(run_dir / "collect_index.json") if (run_dir / "collect_index.json").exists() else []
    elapsed = round(sum(t.get("elapsed_s", 0) for t in dispatch["tasks"]) / 60, 1)

    base = None
    if args.baseline:
        base = load_json(Path(args.baseline) / "summary.json")
        if base["suite"] != detail["suite"]:
            raise SystemExit(f"题库版本不一致（{base['suite']} vs {detail['suite']}），分数不可比")

    base_dims = (base or {}).get("per_dimension", {})
    lines = []
    lines.append(f"# 评测报告：{detail['agent']}")
    lines.append("")
    lines.append(f"题库：{detail['suite']}　run：{detail['run_id']}　评分器：{detail.get('judge_version')}　做题耗时：{elapsed}min")
    lines.append("")
    lines.append(f"## 总分：{detail['total']} / 100")
    if base:
        lines.append("")
        diff = detail["total"] - base["total"]
        lines.append(f"对照基线 {base['agent']}：{base['total']} 分（{fmt_delta(diff)}）")
    lines.append("")
    lines.append("## 维度得分")
    lines.append("")
    header = "| 维度 | 得分 | 满分 |"
    sep = "|---|---|---|---|"
    if base:
        header += " 较基线 |"
        sep += "---|"
    lines.append(header)
    lines.append(sep)
    for dim, agg in detail["per_dimension"].items():
        row = f"| {dim} | {agg['score']} | {agg['full']} |"
        if base:
            b = base_dims.get(dim, {}).get("score")
            row += f" {fmt_delta(agg['score'] - b) if b is not None else '—'} |"
        lines.append(row)
    lines.append("")

    lines.append("## 扣分明细")
    lines.append("")
    any_deduction = False
    for tid, entry in detail["tasks"].items():
        for item in entry["items"]:
            if item["score"] < item["points"]:
                any_deduction = True
                lost = item["points"] - item["score"]
                ev = item["evidence"].replace("\n", " ")[:200]
                lines.append(f"- **{tid}**（-{lost}）{item['item']}：{ev}")
    if not any_deduction:
        lines.append("- 无扣分")
    lines.append("")

    lines.append("## 红线")
    lines.append("")
    red = {tid: e["red_line"] for tid, e in detail["tasks"].items() if e["red_line"]}
    if red:
        for tid, desc in red.items():
            lines.append(f"- 🔴 **{tid}**：{desc}（该题判 0 分）")
    else:
        lines.append("- 本轮无命中")
    lines.append("")

    flags = [(tid, f) for tid, e in detail["tasks"].items() for f in e["flags"]]
    notes = [(c["task_id"], n) for c in collect for n in c.get("notes", [])]
    failures = [(tid, e["failure_class"]) for tid, e in detail["tasks"].items() if e["failure_class"]]
    if flags or notes or failures:
        lines.append("## 需要关注")
        lines.append("")
        for tid, f in flags:
            lines.append(f"- ⚠️ {tid}：{f}")
        for tid, fc in failures:
            lines.append(f"- ⚠️ {tid}：分发异常（{fc}），整题 0 分")
        for tid, n in notes:
            lines.append(f"- ⚠️ {tid}：{n}")
        lines.append("")

    out = run_dir / "report.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"报告已生成：{out}")
    print(f"总分：{detail['total']}/100")


if __name__ == "__main__":
    main()
