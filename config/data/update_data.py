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
from check_domains import main as check_domains

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
    """
    try:
        # 获取脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # 切换到脚本所在目录
        os.chdir(script_dir)
        logging.info(f"工作目录已切换到: {script_dir}")
        return True
    except Exception as e:
        logging.error(f"设置环境失败: {str(e)}")
        return False

def update_all_data():
    """
    更新所有数据文件
    """
    try:
        # 记录开始时间
        start_time = datetime.now()
        logging.info("开始更新数据...")

        # 1. 更新 User-Agents
        logging.info("1. 开始更新 User-Agents...")
        update_user_agents()
        
        # 2. 更新 Google 域名列表
        logging.info("2. 开始更新 Google 域名列表...")
        update_domains()
        
        # 3. 检查域名可用性
        logging.info("3. 开始检查域名可用性...")
        check_domains()

        # 记录完成时间和耗时
        end_time = datetime.now()
        duration = end_time - start_time
        logging.info(f"数据更新完成！总耗时: {duration}")
        
        return True
    except Exception as e:
        logging.error(f"更新过程出错: {str(e)}")
        return False

def main():
    """
    主函数
    """
    if not setup_environment():
        sys.exit(1)
    
    if not update_all_data():
        sys.exit(1)
    
    logging.info("所有操作已完成")

if __name__ == "__main__":
    main() 