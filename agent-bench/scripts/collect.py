#!/usr/bin/env python3
"""收卷：校验输出契约、生成 changes.diff、标记缺失产物。

用法：
    python3 collect.py --run runs/20261005-120000_my-agent
"""
import argparse
import difflib
import json
import os
from pathlib import Path


def iter_files(root):
    for dirpath, dirnames, files in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".checks", "__pycache__")]
        for name in files:
            if name.endswith(".pyc"):
                continue
            yield (Path(dirpath) / name).relative_to(root)


def read_lines(path):
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return None  # 二进制或不可读，跳过


def make_diff(orig, new):
    parts = []
    orig_files = {str(p) for p in iter_files(orig)}
    new_files = {str(p) for p in iter_files(new)}
    for rel in sorted(orig_files | new_files):
        old = read_lines(orig / rel) if rel in orig_files else []
        cur = read_lines(new / rel) if rel in new_files else []
        if old is None or cur is None or old == cur:
            continue
        parts.append("\n".join(difflib.unified_diff(
            old, cur, fromfile=f"a/{rel}", tofile=f"b/{rel}", n=3, lineterm="")))
    return "\n".join(parts) + ("\n" if parts else "")


def main():
    ap = argparse.ArgumentParser(description="agent-bench 收卷器")
    ap.add_argument("--run", required=True, help="run 目录")
    args = ap.parse_args()
    run_dir = Path(args.run)
    index = json.loads((run_dir / "dispatch_index.json").read_text(encoding="utf-8"))

    report = []
    for entry in index["tasks"]:
        tid = entry["task_id"]
        tdir = run_dir / tid
        ws, orig = tdir / "workspace", tdir / "workspace.orig"
        result_file, trace_file = tdir / "result.json", tdir / "trace.jsonl"
        notes = []

        if not result_file.exists():
            result_file.write_text(json.dumps({"summary": ""}, ensure_ascii=False), encoding="utf-8")
            notes.append("result.json 缺失，已补占位（解释表达类得分点按 0 分处理）")
        if not trace_file.exists():
            notes.append("trace.jsonl 缺失（trace 类得分点按 0 分处理）")

        diff = make_diff(orig, ws)
        (tdir / "changes.diff").write_text(diff, encoding="utf-8")
        if not diff.strip() and entry["status"] == "ok":
            notes.append("工作区无任何改动")

        report.append({"task_id": tid, "status": entry["status"], "notes": notes})
        suffix = "  [!] " + "；".join(notes) if notes else ""
        print(f"[{tid}] {entry['status']}{suffix}", flush=True)

    (run_dir / "collect_index.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n收卷完成：{run_dir}")


if __name__ == "__main__":
    main()
