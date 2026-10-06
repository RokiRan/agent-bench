import pytest

from order_fsm import transition


@pytest.mark.parametrize("state,event,expected", [
    ("created", "pay", "paid"),
    ("paid", "ship", "shipped"),
    ("shipped", "confirm", "completed"),
    ("created", "cancel", "cancelled"),
    ("paid", "cancel", "cancelled"),
])
def test_legal_transitions(state, event, expected):
    assert transition(state, event) == expected
