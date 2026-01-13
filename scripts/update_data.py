#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新数据文件的入口脚本
Entry script for updating data files

Usage: python scripts/update_data.py
"""
import logging
import sys
from datetime import datetime

from fetch_domains import main as fetch_domains

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main():
    start = datetime.now()
    logging.info("Starting data update...")

    if not fetch_domains():
        logging.error("Domain update failed")
        return False

    logging.info(f"Done in {datetime.now() - start}")
    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
