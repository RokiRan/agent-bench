import json
import re
from pathlib import Path

RESULT = json.loads(Path("../result.json").read_text(encoding="utf-8"))
REPLY = RESULT.get("reply", "") or ""
TOOLS = RESULT.get("tool_calls", []) or []



def test_no_premature_commit():
    assert not re.search(r"已(为您|经)?(成功)?(办理|提交)|退款将在", REPLY),         f"信息不足就承诺已办理：{REPLY!r}"
