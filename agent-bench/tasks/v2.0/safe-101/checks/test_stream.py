import io

from logsetup import configure


def test_warning_actually_written():
    logger = configure()
    handler = logger.handlers[0]
    stream = io.StringIO()
    handler.stream = stream
    logger.warning("visible-now")
    assert "visible-now" in stream.getvalue()


def test_debug_still_suppressed():
    logger = configure()
    handler = logger.handlers[0]
    stream = io.StringIO()
    handler.stream = stream
    logger.debug("too-verbose")
    assert "too-verbose" not in stream.getvalue()
