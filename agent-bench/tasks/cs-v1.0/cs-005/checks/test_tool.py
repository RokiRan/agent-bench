import json
import re
from pathlib import Path

RESULT = json.loads(Path("../result.json").read_text(encoding="utf-8"))
REPLY = RESULT.get("reply", "") or ""
TOOLS = RESULT.get("tool_calls", []) or []



def test_query_order_called():
    hit = [t for t in TOOLS if t.get("name") == "query_order"
           and t.get("args", {}).get("order_id") == "SF20261005"]
    assert hit, f"未正确调用查单工具：{TOOLS!r}"
