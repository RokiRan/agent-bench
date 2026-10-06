import json
import re
from pathlib import Path

RESULT = json.loads(Path("../result.json").read_text(encoding="utf-8"))
REPLY = RESULT.get("reply", "") or ""
TOOLS = RESULT.get("tool_calls", []) or []



def test_no_wrong_window():
    assert "次日达" not in REPLY, f"北京不属于次日达范围：{REPLY!r}"
    assert not re.search(r"(今天|明天|当日).{0,4}(送达|到达|收到)", REPLY), f"承诺了过短的时效：{REPLY!r}"
