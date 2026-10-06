import logging

from logsetup import configure


def test_warning_passes_handler():
    logger = configure()
    handler = logger.handlers[0]
    assert handler.level <= logging.WARNING
