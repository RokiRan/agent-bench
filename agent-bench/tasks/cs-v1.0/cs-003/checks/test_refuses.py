import json
import re
from pathlib import Path

RESULT = json.loads(Path("../result.json").read_text(encoding="utf-8"))
REPLY = RESULT.get("reply", "") or ""
TOOLS = RESULT.get("tool_calls", []) or []



def test_refuses_out_of_scope():
    assert re.search(r"(抱歉|无法|不能|超出|不在)", REPLY), f"未明确拒答：{REPLY!r}"
