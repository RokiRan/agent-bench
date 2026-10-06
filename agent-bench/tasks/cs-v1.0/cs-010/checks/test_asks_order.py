import json
import re
from pathlib import Path

RESULT = json.loads(Path("../result.json").read_text(encoding="utf-8"))
REPLY = RESULT.get("reply", "") or ""
TOOLS = RESULT.get("tool_calls", []) or []



def test_asks_for_order_info():
    assert ("订单号" in REPLY or "订单编号" in REPLY), f"未询问订单信息：{REPLY!r}"
    assert ("？" in REPLY or "?" in REPLY), f"没有提出澄清问题：{REPLY!r}"
