import json
import re
from pathlib import Path

RESULT = json.loads(Path("../result.json").read_text(encoding="utf-8"))
REPLY = RESULT.get("reply", "") or ""
TOOLS = RESULT.get("tool_calls", []) or []



def test_exactly_one_correct_tool():
    assert len(TOOLS) == 1, f"应只调用一个工具，实际：{TOOLS!r}"
    assert TOOLS[0].get("name") == "query_order", f"工具不对：{TOOLS!r}"
