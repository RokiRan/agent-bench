#!/usr/bin/env python3
"""自测用假 Agent：直接把 gold 答案应用到工作区，并模拟一次验证运行。

仅用于验证评测管线（dispatch -> collect -> score -> report）是否工作，
不代表任何真实能力。设环境变量 AB_NOOP=1 可切换为"交白卷"模式（负向用例）。
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("需要 PyYAML：pip install pyyaml")


def apply_patch(patch_text, ws):
    """应用整文件级 unified diff（生成时上下文为全文件，每个 hunk 即完整新内容）。"""
    buf = {}
    current = None
    for line in patch_text.splitlines():
        if line.startswith("+++ "):
            path = line[4:].strip()
            if path.startswith("b/"):
                path = path[2:]
            current = path
            buf[current] = []
        elif line.startswith(("--- ", "@@", "diff ", "index ", "new file", "old mode", "new mode")):
            continue
        elif current is not None:
            if line.startswith("-"):
                continue
            buf[current].append(line[1:] if line[:1] in (" ", "+") else line)
    for path, lines in buf.items():
        target = ws / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task-dir", required=True)
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--result", required=True)
    ap.add_argument("--trace", required=True)
    args = ap.parse_args()
    ws = Path(args.workspace)
    task = yaml.safe_load((Path(args.task_dir) / "task.yaml").read_text(encoding="utf-8"))
    noop = os.environ.get("AB_NOOP") == "1"

    # 客服专项（cs-*）：产出为 result.json 的 reply / tool_calls
    if not noop and task.get("gold_result"):
        gr = task["gold_result"]
        result_obj = {"summary": gr.get("summary", "已完成客服回复"),
                      "reply": gr.get("reply", ""),
                      "tool_calls": gr.get("tool_calls", [])}
        Path(args.result).write_text(
            json.dumps(result_obj, ensure_ascii=False, indent=2), encoding="utf-8")
        log = [{"type": "tool_call", "tool": "knowledge_search", "ok": True}]
        Path(args.trace).write_text(
            "\n".join(json.dumps(l, ensure_ascii=False) for l in log) + "\n", encoding="utf-8")
        return

    if not noop:
        if task.get("gold_patch"):
            apply_patch(task["gold_patch"], ws)
        for rel in task.get("gold_delete", []):
            p = ws / rel
            if p.exists():
                p.unlink()

    # 模拟一次验证运行并写入轨迹
    if (ws / "tests").is_dir():
        cmd = [sys.executable, "-m", "pytest", "tests", "-q"]
        cmd_text = "python3 -m pytest tests -q"
    else:
        cmd = [sys.executable, "-c", "print('self-check ok')"]
        cmd_text = "python3 -c self-check"
    proc = subprocess.run(cmd, cwd=ws, capture_output=True, text=True)
    log = [{"type": "tool_call", "tool": "bash", "cmd": cmd_text, "ok": proc.returncode == 0}]
    Path(args.trace).write_text(
        "\n".join(json.dumps(l, ensure_ascii=False) for l in log) + "\n", encoding="utf-8")

    summary = "" if noop else "根因：题干所述缺陷；改动：按需求修改对应代码；验证：运行 python3 -m pytest 通过。"
    Path(args.result).write_text(
        json.dumps({"summary": summary}, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
