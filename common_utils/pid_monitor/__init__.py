# @Date     : 2025/9/8 15:44
# @Author   : q275343119
# @File     : __init__.py
# @Description: PID监控模块初始化文件
"""
PID监控模块

提供进程内存使用情况的实时监控功能。

主要功能:
- 监控指定PID的内存使用情况
- 支持RSS(常驻内存)、VMS(虚拟内存)监控
- 支持详细模式, 显示USS(独立内存)和内存百分比
- 支持自定义监控间隔
- 记录和显示峰值内存使用

使用示例:
    from common_utils.pid_monitor import monitor_memory, get_memory_usage

    # 监控指定进程
    monitor_memory(1234, interval=1, detailed=True)

    # 获取单次内存使用情况
    memory_info = get_memory_usage(1234, detailed=True)
"""

from .monitor import format_bytes, get_memory_usage, main, monitor_memory

__all__ = ["format_bytes", "get_memory_usage", "main", "monitor_memory"]
