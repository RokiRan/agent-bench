#!/usr/bin/env python3
"""分发：按 adapter 配置逐题调用被测 Agent 的 CLI 做题。

用法：
    python3 dispatch.py --agent my-agent [--suite v1.0] [--runs-dir runs] [--only fix-001 ...]

每题：复制独立工作区 -> 写 prompt.txt -> 执行 adapter 命令（cwd=工作区，超时熔断）。
产物：{runs_dir}/{时间戳}_{agent}/{task_id}/{workspace, workspace.orig, prompt.txt, agent.log, ...}
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("需要 PyYAML：pip install pyyaml")

SKILL_ROOT = Path(__file__).resolve().parent.parent


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    ap = argparse.ArgumentParser(description="agent-bench 任务分发器")
    ap.add_argument("--agent", required=True, help="被测方名（config/agents/{name}.yaml）")
    ap.add_argument("--suite", default=None, help="题库版本，默认读 config/bench.yaml")
    ap.add_argument("--runs-dir", default="runs", help="评测产物输出目录")
    ap.add_argument("--only", nargs="*", default=None, help="只跑指定 task_id（调试用）")
    args = ap.parse_args()

    bench = load_yaml(SKILL_ROOT / "config" / "bench.yaml")
    suite = args.suite or bench.get("suite_default", "v1.0")
    adapter_path = SKILL_ROOT / "config" / "agents" / f"{args.agent}.yaml"
    if not adapter_path.exists():
        sys.exit(f"adapter 不存在：{adapter_path}\n请参照 config/agents/my-agent.yaml 的注释创建。")
    adapter = load_yaml(adapter_path)

    tasks_dir = SKILL_ROOT / "tasks" / suite
    if not tasks_dir.is_dir():
        sys.exit(f"题库不存在：{tasks_dir}")

    run_id = datetime.now().strftime("%Y%m%d-%H%M%S") + "_" + args.agent
    run_dir = Path(args.runs_dir).resolve() / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    index = {
        "run_id": run_id,
        "agent": args.agent,
        "suite": suite,
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "tasks": [],
    }

    for task_dir in sorted(p for p in tasks_dir.iterdir() if (p / "task.yaml").exists()):
        task = load_yaml(task_dir / "task.yaml")
        tid = task["task_id"]
        if args.only and tid not in args.only:
            continue
        tdir = run_dir / tid
        ws = tdir / "workspace"
        shutil.copytree(task_dir / task.get("workspace", "workspace"), ws)
        shutil.copytree(ws, tdir / "workspace.orig")  # 快照，供 collect 生成 diff
        prompt_file = tdir / "prompt.txt"
        prompt_file.write_text(task["prompt"].strip() + "\n", encoding="utf-8")
        result_file = tdir / "result.json"
        trace_file = tdir / "trace.jsonl"

        cmd = adapter["command"].format(
            prompt_file=prompt_file,
            workspace=ws,
            result_file=result_file,
            trace_file=trace_file,
            task_dir=task_dir,
            skill_root=SKILL_ROOT,
        )
        env = dict(os.environ)
        env.update({k: os.path.expandvars(str(v)) for k, v in (adapter.get("env") or {}).items()})
        timeout = int(task.get("limits", {}).get("timeout_s", adapter.get("timeout_s", 600)))

        t0 = time.time()
        try:
            proc = subprocess.run(cmd, shell=True, cwd=ws, env=env, timeout=timeout,
                                  capture_output=True, text=True)
            status = "ok" if proc.returncode == 0 else f"error(exit={proc.returncode})"
            log = (proc.stdout or "") + "\n--- stderr ---\n" + (proc.stderr or "")
        except subprocess.TimeoutExpired:
            status = "timeout"
            log = f"超过 {timeout}s，已熔断"
        elapsed = round(time.time() - t0, 1)
        (tdir / "agent.log").write_text(log, encoding="utf-8")
        index["tasks"].append({"task_id": tid, "status": status, "elapsed_s": elapsed})
        print(f"[{status:>12}] {tid} ({elapsed}s)", flush=True)

    (run_dir / "dispatch_index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n分发完成，run 目录：{run_dir}")


if __name__ == "__main__":
    main()
