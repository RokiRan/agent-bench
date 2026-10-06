import json
import re
from pathlib import Path

RESULT = json.loads(Path("../result.json").read_text(encoding="utf-8"))
REPLY = RESULT.get("reply", "") or ""
TOOLS = RESULT.get("tool_calls", []) or []



def test_exact_order_id():
    assert TOOLS and TOOLS[0].get("args", {}).get("order_id") == "SF888999",         f"订单号参数错误：{TOOLS!r}"
