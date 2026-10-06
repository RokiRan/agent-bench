import json
import re
from pathlib import Path

RESULT = json.loads(Path("../result.json").read_text(encoding="utf-8"))
REPLY = RESULT.get("reply", "") or ""
TOOLS = RESULT.get("tool_calls", []) or []



def test_correct_order_referenced():
    tool_hit = any(t.get("name") == "query_order"
                   and t.get("args", {}).get("order_id") == "SF123456789" for t in TOOLS)
    assert tool_hit or "SF123456789" in REPLY,         f"未承接上文订单号 SF123456789：tools={TOOLS!r} reply={REPLY!r}"
