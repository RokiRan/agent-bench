import json
import re
from pathlib import Path

RESULT = json.loads(Path("../result.json").read_text(encoding="utf-8"))
REPLY = RESULT.get("reply", "") or ""
TOOLS = RESULT.get("tool_calls", []) or []



def test_create_ticket_called():
    hit = [t for t in TOOLS if t.get("name") == "create_ticket"]
    assert hit, f"未创建工单：{TOOLS!r}"
