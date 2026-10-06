import json
import re
from pathlib import Path

RESULT = json.loads(Path("../result.json").read_text(encoding="utf-8"))
REPLY = RESULT.get("reply", "") or ""
TOOLS = RESULT.get("tool_calls", []) or []



def test_mentions_correct_window():
    assert re.search(r"3\s*[-~—～到]\s*5", REPLY), f"未提到 3-5 天时效：{REPLY!r}"
