# @Date     : 2025/8/22 15:38
# @Author   : q275343119
# @File     : config_loader.py
# @Description:
# config/config_loader.py
import os
from pathlib import Path
from typing import Any, ClassVar

from dotenv import load_dotenv


class _ConfigLoader:
    _shared_state: ClassVar[dict] = {}  # Borg 模式: 所有实例共享状态

    def __init__(self, env_file: str = ".env"):
        self.__dict__ = self._shared_state
        if not hasattr(self, "_initialized"):
            self._initialized = True
            if Path(env_file).exists():
                load_dotenv(env_file, override=True)
            else:
                print(
                    f"⚠️ Warning: {env_file} not found, using only system environment variables."
                )

    def get(
        self, key: str, default: Any | None = None, cast: type | None = None
    ) -> Any:
        """
        获取配置项
        :param key: 环境变量名称
        :param default: 默认值, 如果配置不存在时使用
        :param cast: 类型转换函数, 如 int, float, bool
        """
        value = os.getenv(key, default)

        if value is None:
            return default

        if cast:
            try:
                if cast is bool:  # 特殊处理布尔值
                    return str(value).lower() in ("1", "true", "yes", "on")
                return cast(value)
            except Exception as e:
                raise ValueError(
                    f"❌ Failed to cast config {key}={value} to {cast}: {e}"
                ) from e

        return value


# 单例实例, 全局使用 config 即可
config = _ConfigLoader()
