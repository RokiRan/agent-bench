"""配置加载：环境变量覆盖默认值。"""
import os

from config import DEFAULTS

PREFIX = "AP_"


def load_config(env=None):
    """返回配置字典。环境变量 APP_HOST / APP_PORT / APP_DEBUG 覆盖默认值。"""
    env = os.environ if env is None else env
    cfg = dict(DEFAULTS)
    for key, value in env.items():
        if key.startswith(PREFIX):
            cfg[key[len(PREFIX):].lower()] = value
    return cfg
