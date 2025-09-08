# @Date     : 2025/9/8 15:44
# @Author   : q275343119
# @File     : monitor.py
# @Description: 进程内存监控模块
# !/usr/bin/env python3
"""
监控指定PID内存使用情况的模块
支持实时监控进程的内存使用情况, 包括RSS常驻内存、VMS虚拟内存等信息
"""

import argparse
import sys
import time
from datetime import datetime

import psutil


def get_memory_usage(pid, detailed=False):
    """获取指定PID的内存使用情况

    Args:
        pid (int): 要监控的进程ID
        detailed (bool): 是否获取详细信息, 包括USS和内存百分比

    Returns:
        dict: 包含内存使用信息的字典, 失败时返回None
    """
    try:
        process = psutil.Process(pid)
        memory_info = process.memory_info()

        # 获取内存使用详情
        rss = memory_info.rss  # 常驻集大小 (Resident Set Size)
        vms = memory_info.vms  # 虚拟内存大小 (Virtual Memory Size)

        if detailed:
            # 获取更详细的内存信息(如果可用)
            try:
                memory_full_info = process.memory_full_info()
                uss = memory_full_info.uss  # 独立集大小 (Unique Set Size)
            except psutil.AccessDenied:
                uss = "N/A (requires elevated privileges)"

            # 获取内存百分比
            memory_percent = process.memory_percent()

            return {
                "rss": rss,
                "vms": vms,
                "uss": uss,
                "percent": memory_percent,
                "time": datetime.now(),
            }
        else:
            return {"rss": rss, "vms": vms, "time": datetime.now()}

    except psutil.NoSuchProcess:
        print(f"错误: PID {pid} 对应的进程不存在")
        return None
    except psutil.AccessDenied:
        print(f"错误: 没有权限访问 PID {pid} 的进程信息")
        return None


def format_bytes(bytes_value):
    """将字节转换为人类可读的格式

    Args:
        bytes_value: 字节数, 可以是数字或字符串

    Returns:
        str: 格式化后的字符串, 如 "1.23 MB"
    """
    if isinstance(bytes_value, str):
        return bytes_value

    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def monitor_memory(pid, interval=2, detailed=False):
    """监控指定PID的内存使用情况

    Args:
        pid (int): 要监控的进程ID
        interval (float): 监控刷新间隔, 单位秒
        detailed (bool): 是否显示详细信息
    """
    print(f"开始监控进程 {pid} 的内存使用情况 (刷新间隔: {interval}秒)")
    print("按 Ctrl+C 停止监控\n")

    if detailed:
        print(
            "时间戳                | RSS(常驻内存)     | VMS(虚拟内存)     | USS(独立内存)     | 内存百分比"
        )
        print(
            "-------------------------------------------------------------------------------------------"
        )
    else:
        print("时间戳                | RSS(常驻内存)     | VMS(虚拟内存)")
        print("---------------------------------------------------------------")

    max_rss = 0
    try:
        while True:
            memory_usage = get_memory_usage(pid, detailed)
            if memory_usage is None:
                break

            timestamp = memory_usage["time"].strftime("%Y-%m-%d %H:%M:%S")
            max_rss = max(max_rss, memory_usage["rss"])  # 修复: 添加空格
            rss_str = format_bytes(memory_usage["rss"])
            vms_str = format_bytes(memory_usage["vms"])

            if detailed:
                uss_str = format_bytes(memory_usage["uss"])
                percent_str = f"{memory_usage['percent']:.2f}%"
                print(
                    f"{timestamp} | {rss_str:<15} | {vms_str:<15} | {uss_str:<15} | {percent_str:<10}"
                )
            else:
                print(f"{timestamp} | {rss_str:<15} | {vms_str:<15}")

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n监控已停止")

    finally:
        print(f"峰值RSS: {format_bytes(max_rss)}")


def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(description="监控指定PID的内存使用情况")
    parser.add_argument("pid", type=int, help="要监控的进程ID")
    parser.add_argument(
        "-i", "--interval", type=float, default=2, help="监控刷新间隔(秒), 默认2秒"
    )
    parser.add_argument(
        "-d",
        "--detailed",
        action="store_true",
        help="显示详细内存信息(需要管理员权限)",
    )

    args = parser.parse_args()

    # 检查PID是否存在
    if not psutil.pid_exists(args.pid):
        print(f"错误: PID {args.pid} 不存在")
        sys.exit(1)

    monitor_memory(args.pid, args.interval, args.detailed)


if __name__ == "__main__":
    main()
