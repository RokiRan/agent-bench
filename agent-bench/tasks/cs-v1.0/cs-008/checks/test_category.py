import json
import re
from pathlib import Path

RESULT = json.loads(Path("../result.json").read_text(encoding="utf-8"))
REPLY = RESULT.get("reply", "") or ""
TOOLS = RESULT.get("tool_calls", []) or []



def test_correct_category():
    cats = [t.get("args", {}).get("category") for t in TOOLS if t.get("name") == "create_ticket"]
    assert cats and cats[0] == "物流破损", f"工单分类错误：{cats!r}"
