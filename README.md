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
│   ├── pid_monitor/
│   │   ├── monitor.py    # 进程监控核心文件
│   │   └── __init__.py   # 模块初始化
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

### pid_monitor 模块
pid_monitor 模块提供进程内存使用情况的实时监控功能，支持对指定PID进程的内存监控和分析。位置：common_utils/pid_monitor/monitor.py。

#### 基本用法
1. 导入：`from common_utils.pid_monitor import monitor_memory, get_memory_usage`
2. 监控进程：使用 `monitor_memory(pid, interval, detailed)` 进行实时监控。
3. 获取内存信息：使用 `get_memory_usage(pid, detailed)` 获取单次内存使用情况。

#### 主要功能
- **实时监控**：持续监控指定进程的内存使用情况
- **内存指标**：支持 RSS(常驻内存)、VMS(虚拟内存) 监控
- **详细模式**：显示 USS(独立内存) 和内存百分比（需要管理员权限）
- **峰值记录**：自动记录并显示监控期间的峰值内存使用
- **自定义间隔**：支持自定义监控刷新间隔

#### 示例
```python
from common_utils.pid_monitor import monitor_memory, get_memory_usage

# 实时监控进程（每2秒刷新一次）
monitor_memory(1234, interval=2, detailed=False)

# 详细模式监控（显示更多内存信息）
monitor_memory(1234, interval=1, detailed=True)

# 获取单次内存使用情况
memory_info = get_memory_usage(1234, detailed=True)
if memory_info:
    print(f"RSS内存: {memory_info['rss']} 字节")
    print(f"虚拟内存: {memory_info['vms']} 字节")
```

#### 命令行使用
```bash
# 基本监控
python -m common_utils.pid_monitor.monitor 1234

# 自定义刷新间隔（每0.5秒）
python -m common_utils.pid_monitor.monitor 1234 -i 0.5

# 详细模式（需要管理员权限）
python -m common_utils.pid_monitor.monitor 1234 -d
```

#### 参数说明
- `pid` (int): 要监控的进程ID
- `interval` (float): 监控刷新间隔，单位秒，默认2秒
- `detailed` (bool): 是否显示详细信息，包括USS内存和百分比

#### 注意事项
- 需要安装 psutil 依赖包。
- 详细模式可能需要管理员权限才能访问USS内存信息。
- 监控过程中按 Ctrl+C 可以停止监控并显示峰值信息。
- 如果进程不存在或没有访问权限，会显示相应错误信息。

更多模块用法将在添加新模块时更新。

## 代码质量检查
项目集成了基于 **Ruff** 的自动化代码质量检查工具，帮助保持代码的一致性和质量。

### 安装 Ruff
由于项目使用 uv 管理，请通过以下方式安装 ruff：

```bash
# 使用 uv 添加 ruff 作为开发依赖
uv add --dev ruff

# 或者全局安装 ruff
uv tool install ruff

# 传统方式安装
pip install ruff
```

### 使用 Ruff 检查代码
项目已在 `pyproject.toml` 中配置了 ruff 规则，可以直接使用：

```bash
# 检查代码问题
ruff check .

# 检查并自动修复可修复的问题
ruff check . --fix

# 只检查格式是否正确（不修改文件）
ruff format . --check

# 格式化代码
ruff format .

# 显示详细检查信息
ruff check . --show-source

# 检查特定文件
ruff check common_utils/
```

### 快速开始代码检查
在开发过程中，建议的工作流程：

```bash
# 1. 开发完成后，先检查代码问题
ruff check .

# 2. 自动修复可修复的问题
ruff check . --fix

# 3. 格式化代码
ruff format .

# 4. 最后再检查一遍确保没问题
ruff check .
```

### 检查规则说明
项目配置了以下检查规则（详见 `pyproject.toml` 的 `[tool.ruff]` 部分）：

| 规则类型 | 说明 | 示例 |
|---------|------|------|
| **E/W** | pycodestyle 错误和警告 | 空格、缩进、行长度 |
| **F** | Pyflakes 检查 | 未使用的导入、变量 |
| **I** | import 排序检查 | 导入顺序标准化 |
| **N** | PEP8 命名规范 | 函数、类名格式 |
| **UP** | Python 版本升级建议 | 使用新语法特性 |
| **B** | 常见 bug 检查 | 可能的逻辑错误 |
| **C4** | 列表/字典推导式优化 | 性能优化建议 |
| **PIE/SIM** | 代码简化建议 | 简化复杂表达式 |
| **PTH** | 建议使用 pathlib | 现代路径处理 |
| **RUF** | Ruff 特有规则 | 工具特定优化 |

### 代码风格标准
- **行长度**: 最大 88 字符
- **引号**: 使用双引号 `"`
- **缩进**: 4 个空格
- **尾部逗号**: 保留（便于版本控制）
- **目标版本**: Python 3.12+

## 持续集成 (CI/CD)

### GitHub Actions 自动检查
项目配置了 GitHub Actions 来自动检查所有提交和 Pull Request 的代码质量。

#### 自动触发条件
- 📤 **推送到主分支** (main/master)
- 🔄 **创建或更新 Pull Request**  
- 🎯 **手动触发** (workflow_dispatch)

#### 检查内容
每次代码提交都会自动执行以下检查：

```yaml
✅ 环境配置 (uv + Python 3.12)
🔍 Ruff 代码质量检查  
📐 Ruff 代码格式检查
```

#### 查看检查结果
1. 在仓库页面点击 **Actions** 标签
2. 查看最近的工作流运行状态
3. 点击具体的运行查看详细日志

#### 检查失败处理
如果 CI 检查失败：
```bash
# 本地运行相同的检查
ruff check .
ruff format . --check

# 修复问题
ruff check . --fix
ruff format .

# 重新提交
git add .
git commit -m "fix: 修复代码质量问题"
git push
```

#### 状态徽章
您可以在项目中添加 CI 状态徽章：
```markdown
![Lint](https://github.com/您的用户名/py-toolbox/workflows/Lint/badge.svg)
```

### 本地预检查
建议在提交前先本地检查，避免 CI 失败：
```bash
# 快速检查脚本
ruff check . --fix && ruff format . && ruff check .
```

## 贡献
欢迎提交 Pull Request 添加新模块或优化现有代码！请遵循：

### 开发要求
- **代码风格**: 使用 ruff 检查和格式化代码
- **测试**: 添加 example.py 演示用法
- **文档**: 更新 README 和 docstring
- **类型注解**: 为函数添加类型提示

### 提交前检查清单
在提交代码前，请确保通过以下检查：

```bash
# 1. 本地代码质量检查
ruff check . --fix    # 修复问题
ruff format .         # 格式化代码
ruff check .          # 确认无问题

# 2. 测试功能
python -m common_utils.logging.example
python -m common_utils.config.example  
python -m common_utils.pid_monitor.monitor --help

# 3. 提交代码
git add .
git commit -m "feat: 添加新功能"
git push
```

### 代码质量标准
- ✅ **通过 CI 检查**: 所有 GitHub Actions 检查都必须通过
- 📝 **完整文档**: 添加完整的 docstring 和使用示例
- 🎯 **遵循规范**: 符合 PEP8 和项目代码风格
- 🏷️ **类型注解**: 为函数参数和返回值添加类型提示
- 🧪 **功能验证**: 提供 example.py 演示用法

## 许可证
详见 [LICENSE](LICENSE) 文件（MIT 许可）。
