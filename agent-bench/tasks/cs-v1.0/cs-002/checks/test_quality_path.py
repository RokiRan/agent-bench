import json
import re
from pathlib import Path

RESULT = json.loads(Path("../result.json").read_text(encoding="utf-8"))
REPLY = RESULT.get("reply", "") or ""
TOOLS = RESULT.get("tool_calls", []) or []



def test_mentions_quality_exception():
    assert "质量" in REPLY, f"未给出质量问题退换的例外路径：{REPLY!r}"
