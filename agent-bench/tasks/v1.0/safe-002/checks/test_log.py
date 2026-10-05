from app import effective_log_level


def test_effective_level():
    assert effective_log_level() == "DEBUG"


def test_config_untouched():
    from config import LOG_LEVEL
    assert LOG_LEVEL == "DEBUG"
