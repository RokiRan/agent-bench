from config import DEFAULTS
from loader import load_config


def test_defaults_when_empty():
    assert load_config({}) == DEFAULTS


def test_unrelated_env_ignored():
    assert load_config({"OTHER_X": "1"}) == DEFAULTS
