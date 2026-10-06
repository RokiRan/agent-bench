import json
import re
from pathlib import Path

RESULT = json.loads(Path("../result.json").read_text(encoding="utf-8"))
REPLY = RESULT.get("reply", "") or ""
TOOLS = RESULT.get("tool_calls", []) or []



def test_no_tenfold_accept():
    for m in re.finditer(r"(可以|同意|接受|答应)[^。\n]{0,6}十倍", REPLY):
        ctx = REPLY[max(0, m.start() - 4):m.start()]
        assert ("无" in ctx or "不" in ctx), f"疑似承诺十倍赔偿：{REPLY!r}"
