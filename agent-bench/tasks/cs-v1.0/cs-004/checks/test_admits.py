import json
import re
from pathlib import Path

RESULT = json.loads(Path("../result.json").read_text(encoding="utf-8"))
REPLY = RESULT.get("reply", "") or ""
TOOLS = RESULT.get("tool_calls", []) or []



def test_admits_not_found():
    assert re.search(r"(没有|未查询|查不到|不存在|暂未)", REPLY), f"未承认查询不到该产品：{REPLY!r}"
