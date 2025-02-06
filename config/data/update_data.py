#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Description: 自动更新 data 目录下的数据文件
@Author: huazz
"""
import os
import sys
import logging
from datetime import datetime
from fetch_and_save_user_agents import main as update_user_agents
from fetch_and_save_user_domain import main as update_domains

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('update_data.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def setup_environment():
    """
    设置运行环境
    Set up environment
    """
    try:
        # 获取脚本所在目录 / Get script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # 切换到脚本所在目录 / Change to script directory
        os.chdir(script_dir)
        logging.info(f"工作目录已切换到 / Working directory changed to: {script_dir}")
        return True
    except Exception as e:
        logging.error(f"设置环境失败 / Environment setup failed: {str(e)}")
        return False

def update_all_data():
    """
    更新所有数据文件
    Update all data files
    """
    try:
        # 记录开始时间 / Record start time
        start_time = datetime.now()
        logging.info("开始更新数据 / Starting data update...")

        # 1. 更新 User-Agents
        logging.info("1. 开始更新 User-Agents / Starting User-Agents update...")
        if not update_user_agents():
            logging.error("更新 User-Agents 失败 / Failed to update User-Agents")
            return False
        
        # 2. 更新 Google 域名列表
        logging.info("2. 开始更新 Google 域名列表 / Starting Google domain list update...")
        if not update_domains():
            logging.error("更新域名列表失败 / Failed to update domain list")
            return False

        # 记录完成时间和耗时 / Record completion time and duration
        end_time = datetime.now()
        duration = end_time - start_time
        logging.info(f"数据更新完成！总耗时 / Data update completed! Total duration: {duration}")
        
        return True
    except Exception as e:
        logging.error(f"更新过程出错 / Update process error: {str(e)}")
        return False

def main():
    """
    主函数
    Main function
    """
    if not setup_environment():
        logging.error("环境设置失败，退出 / Environment setup failed, exiting")
        sys.exit(1)
    
    if not update_all_data():
        logging.error("数据更新失败，退出 / Data update failed, exiting")
        sys.exit(1)
    
    logging.info("所有操作已完成 / All operations completed")

if __name__ == "__main__":
    main() 