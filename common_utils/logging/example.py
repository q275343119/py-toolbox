# -*- coding: utf-8 -*-
# @Date     : 2024/08/23
# @Author   : AI Assistant
# @File     : example.py
# @Description: 日志模块使用示例

from common_utils.logging.logger import logging


def main():
    logging.debug("这是一个调试日志（INFO 级别下不会显示）")
    logging.info("这是一个信息日志")
    logging.warning("这是一个警告日志")
    logging.error("这是一个错误日志")


if __name__ == "__main__":
    main()
