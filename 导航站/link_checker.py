#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import requests
import logging
import time
from datetime import datetime
import schedule

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('link_checker.log'),
        logging.StreamHandler()
    ]
)

# 数据文件路径
DATA_FILE = 'data/sites.json'
STATUS_FILE = 'data/status.json'

def load_sites():
    """加载网站数据"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def load_status():
    """加载链接状态数据"""
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_status(status_data):
    """保存链接状态数据"""
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(status_data, f, ensure_ascii=False, indent=2)

def check_link(url, timeout=10):
    """检查链接是否有效"""
    try:
        # 使用HEAD请求减少数据传输
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        
        # 如果HEAD请求失败，尝试GET请求
        if response.status_code >= 400:
            response = requests.get(url, timeout=timeout, allow_redirects=True)
            
        return {
            'status_code': response.status_code,
            'is_valid': 200 <= response.status_code < 400,
            'checked_at': datetime.now().isoformat(),
            'error': None
        }
    except requests.RequestException as e:
        return {
            'status_code': None,
            'is_valid': False,
            'checked_at': datetime.now().isoformat(),
            'error': str(e)
        }

def check_all_links(batch_size=20, delay=1):
    """检查所有网站链接"""
    sites = load_sites()
    status_data = load_status()
    
    logging.info(f"开始检查 {len(sites)} 个网站链接")
    
    # 分批处理，避免同时发起大量请求
    for i in range(0, len(sites), batch_size):
        batch = sites[i:i+batch_size]
        logging.info(f"检查批次 {i//batch_size + 1}/{(len(sites)-1)//batch_size + 1} ({len(batch)} 个链接)")
        
        for site in batch:
            site_id = site['id']
            url = site['url']
            
            logging.info(f"检查链接: {url}")
            result = check_link(url)
            
            # 更新状态数据
            if site_id not in status_data:
                status_data[site_id] = {
                    'history': [],
                    'consecutive_failures': 0
                }
                
            # 记录检查历史
            status_data[site_id]['history'].append(result)
            
            # 只保留最近10次检查记录
            if len(status_data[site_id]['history']) > 10:
                status_data[site_id]['history'] = status_data[site_id]['history'][-10:]
                
            # 更新连续失败次数
            if not result['is_valid']:
                status_data[site_id]['consecutive_failures'] += 1
                logging.warning(f"链接失效: {url}, 状态码: {result['status_code']}, 错误: {result['error']}")
                
                # 连续失败5次以上发出严重警告
                if status_data[site_id]['consecutive_failures'] >= 5:
                    logging.error(f"严重警告: {url} 已连续失效 {status_data[site_id]['consecutive_failures']} 次，建议下架")
            else:
                status_data[site_id]['consecutive_failures'] = 0
                logging.info(f"链接正常: {url}, 状态码: {result['status_code']}")
            
            # 添加间隔，避免请求过于频繁
            time.sleep(delay)
        
    # 保存状态数据
    save_status(status_data)
    logging.info("链接检查完成")
    
    # 生成简单报告
    generate_report(status_data)

def generate_report(status_data):
    """生成链接检查报告"""
    total = len(status_data)
    valid = sum(1 for site_id in status_data if status_data[site_id]['history'] and status_data[site_id]['history'][-1]['is_valid'])
    invalid = total - valid
    
    # 找出连续失败次数较多的链接
    critical = [site_id for site_id in status_data if status_data[site_id]['consecutive_failures'] >= 3]
    
    with open('link_check_report.txt', 'w', encoding='utf-8') as f:
        f.write(f"链接检查报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"总计检查: {total} 个链接\n")
        f.write(f"有效链接: {valid} 个\n")
        f.write(f"无效链接: {invalid} 个\n\n")
        
        if critical:
            f.write("需要注意的链接:\n")
            sites = load_sites()
            site_map = {site['id']: site for site in sites}
            
            for site_id in critical:
                site = site_map.get(site_id, {'name': 'Unknown', 'url': 'Unknown'})
                failures = status_data[site_id]['consecutive_failures']
                last_check = status_data[site_id]['history'][-1]
                
                f.write(f"- {site['name']} ({site['url']})\n")
                f.write(f"  连续失败: {failures} 次\n")
                f.write(f"  最近检查: {last_check['checked_at']}\n")
                if last_check['status_code']:
                    f.write(f"  状态码: {last_check['status_code']}\n")
                if last_check['error']:
                    f.write(f"  错误信息: {last_check['error']}\n")
                f.write("\n")
    
    logging.info(f"报告已生成: link_check_report.txt")

def schedule_checks():
    """设置定时检查任务"""
    # 每天凌晨2点运行检查
    schedule.every().day.at("02:00").do(check_all_links)
    
    logging.info("链接检查任务已安排")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='链接检查工具')
    parser.add_argument('--now', action='store_true', help='立即执行检查')
    parser.add_argument('--schedule', action='store_true', help='设置定时检查任务')
    
    args = parser.parse_args()
    
    if args.now:
        check_all_links()
    elif args.schedule:
        schedule_checks()
    else:
        parser.print_help() 