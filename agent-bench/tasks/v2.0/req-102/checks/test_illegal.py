import pytest

from order_fsm import transition


@pytest.mark.parametrize("state,event", [
    ("created", "ship"),
    ("created", "confirm"),
    ("paid", "pay"),
    ("shipped", "pay"),
    ("shipped", "cancel"),
    ("completed", "cancel"),
    ("completed", "pay"),
    ("cancelled", "pay"),
])
def test_illegal_transitions(state, event):
    with pytest.raises(ValueError, match="非法状态迁移"):
        transition(state, event)
