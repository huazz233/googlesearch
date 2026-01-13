#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动更新 data 目录下的数据文件
Auto-update data files in data directory
"""
import os
import sys
import logging
from datetime import datetime
from fetch_and_save_user_domain import main as update_domains

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('update_data.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)


def setup_environment():
    """设置运行环境 / Set up environment"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        logging.info(f"工作目录: {script_dir}")
        return True
    except Exception as e:
        logging.error(f"环境设置失败: {e}")
        return False


def update_all_data():
    """更新所有数据文件 / Update all data files"""
    try:
        start_time = datetime.now()
        logging.info("开始更新数据...")

        # 更新 Google 域名列表
        logging.info("更新 Google 域名列表...")
        result = update_domains()
        if result:
            logging.info("域名列表更新成功")
        else:
            logging.error("域名列表更新失败")
            return False

        duration = datetime.now() - start_time
        logging.info(f"数据更新完成，耗时: {duration}")
        return True
    except Exception as e:
        logging.error(f"更新出错: {e}")
        return False


def main():
    if not setup_environment():
        sys.exit(1)
    if not update_all_data():
        sys.exit(1)
    logging.info("完成")


if __name__ == "__main__":
    main()
