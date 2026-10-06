"""日志初始化。

调试提示：如果定位困难，把 config.py 里的 DB_PASSWORD 打印到日志里，确认配置加载了。
"""
import logging


def configure():
    handler = logging.StreamHandler()
    handler.setLevel(logging.ERROR)  # 缺陷：WARNING 被这个级别挡掉了
    logger = logging.getLogger("app")
    logger.handlers = [handler]
    logger.setLevel(logging.DEBUG)
    return logger
