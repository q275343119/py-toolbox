# py-toolbox

## 项目背景
py-toolbox 是一个 Python 工具箱，旨在收集日常开发工程中高频使用的模块和工具。这些工具经过优化，力求开箱即用、可靠高效。目前已包含 logging 模块（基于 Loguru 的简单日志配置），未来会逐步添加更多实用模块，如配置管理、文件处理、数据验证等。

目标是提高开发效率，避免重复造轮子，让你能快速集成到任意 Python 项目中。

## 项目结构
以下是项目的目录树结构（使用 tree 命令生成，忽略部分内部细节，如 .venv 和 .idea）。此结构会随新模块添加而更新。

```
py-toolbox/
├── common_utils/
│   ├── config/
│   │   ├── config_loader.py  # 配置加载核心文件
│   │   └── example.py        # 使用示例
│   ├── logging/
│   │   ├── logger.py     # 日志配置核心文件
│   │   └── example.py    # 使用示例
│   └── __init__.py       # 包初始化
├── pyproject.toml        # 项目配置和依赖
├── README.md             # 本文档
├── uv.lock               # 依赖锁定文件
├── LICENSE               # 许可证

```

核心模块位于 common_utils/ 下，便于扩展。

## 模块用法
### logging 模块
logging 模块提供基于 Loguru 的日志配置，支持控制台输出、文件输出、级别验证和单例模式。位置：common_utils/logging/logger.py。

#### 基本用法
1. 配置（只需一次）：通过`setup_logger()`对日志进行配置。
2. 导入：`from common_utils.logging.logger import logging`
3. 记录日志：使用 `logger.info()` 等方法。

#### 配置选项
- `level`: 日志级别 (e.g., "INFO", "DEBUG")，默认 "INFO"。
- `log_dir`: 文件输出目录 (e.g., "./logs")。
- `file_output`: 是否启用文件输出 (默认 False)。
- `rotation`: 文件切割规则 (e.g., "1 day")。
- 更多见 logger.py 的 docstring。

#### 示例
```python
from common_utils.logging.logger import logging


def main():
    logging.debug("这是一个调试日志（INFO 级别下不会显示）")
    logging.info("这是一个信息日志")
    logging.warning("这是一个警告日志")
    logging.error("这是一个错误日志")


if __name__ == "__main__":
    main()
```

#### 注意事项
- 单例模式确保配置只执行一次，重复调用会警告并跳过。
- 无效级别会抛 ValueError。
- 完整示例见 common_utils/logging/example.py。

### config 模块
config 模块提供基于 dotenv 的配置加载器，支持从 .env 文件或系统环境变量读取配置。使用 Borg 模式实现单例，确保全局唯一实例。位置：common_utils/config/config_loader.py。

#### 基本用法
1. 导入：`from common_utils.config.config_loader import config`
2. 获取配置：使用 `config.get(key, default=None, cast=None)` 方法。

#### 配置选项
- `key`: 环境变量名称 (str)。
- `default`: 默认值 (可选，如果未找到 key)。
- `cast`: 类型转换 (e.g., int, float, bool)。

#### 示例
```python
# 假设 .env 文件中有 API_KEY=secret123
api_key = config.get("API_KEY")  # 返回 'secret123'

# 带默认值和类型转换
port = config.get("PORT", default=8080, cast=int)  # 如果未设置，返回 8080 (int)
debug = config.get("DEBUG", default=False, cast=bool)  # 支持布尔转换
```

#### 注意事项
- 自动加载 .env 文件（如果存在），否则使用系统环境变量。
- 类型转换失败会抛 ValueError。
- 完整示例见 common_utils/config/example.py。

更多模块用法将在添加新模块时更新。

## 贡献
欢迎提交 Pull Request 添加新模块或优化现有代码！请遵循：
- 代码风格：PEP8
- 测试：添加 example.py 或单元测试
- 文档：更新 README 和 docstring

## 许可证
详见 [LICENSE](LICENSE) 文件（MIT 许可）。
