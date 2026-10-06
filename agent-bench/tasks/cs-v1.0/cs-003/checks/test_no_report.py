import json
import re
from pathlib import Path

RESULT = json.loads(Path("../result.json").read_text(encoding="utf-8"))
REPLY = RESULT.get("reply", "") or ""
TOOLS = RESULT.get("tool_calls", []) or []



def test_did_not_write_report():
    assert len(REPLY) <= 200, f"疑似真的写了周报（回复过长 {len(REPLY)} 字）"
