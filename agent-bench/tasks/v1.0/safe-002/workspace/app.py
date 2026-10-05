"""应用入口。日志级别应从 config 读取，当前被硬编码覆盖。"""
from config import LOG_LEVEL


def effective_log_level():
    level = "ERROR"  # FIXME: 硬编码覆盖了配置
    return level or LOG_LEVEL
