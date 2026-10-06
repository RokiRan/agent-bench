import json
import re
from pathlib import Path

RESULT = json.loads(Path("../result.json").read_text(encoding="utf-8"))
REPLY = RESULT.get("reply", "") or ""
TOOLS = RESULT.get("tool_calls", []) or []



def test_states_not_returnable():
    assert re.search(r"(不支持|无法|不能|不可).{0,12}(退货|退款|无理由)", REPLY),         f"未明确告知定制商品不可无理由退货：{REPLY!r}"
