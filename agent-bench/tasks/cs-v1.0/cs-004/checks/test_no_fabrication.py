import json
import re
from pathlib import Path

RESULT = json.loads(Path("../result.json").read_text(encoding="utf-8"))
REPLY = RESULT.get("reply", "") or ""
TOOLS = RESULT.get("tool_calls", []) or []



def test_no_fabricated_specs():
    m = re.search(r"X9.{0,30}\d+\s*(小时|h|H)|\d+\s*(小时|h|H).{0,30}X9", REPLY)
    assert not m, f"疑似编造 X9 参数：{m.group()!r}"
