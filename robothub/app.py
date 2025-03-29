#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_robot_nav')

# 添加全局上下文处理器，提供当前年份
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

# 数据文件路径
DATA_FILE = 'data/sites.json'

# 确保数据目录存在
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

def load_sites():
    """加载网站数据"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_sites(sites):
    """保存网站数据"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(sites, f, ensure_ascii=False, indent=2)

def get_categories():
    """获取所有分类"""
    sites = load_sites()
    categories = {}
    
    for site in sites:
        category = site.get('category', '未分类')
        if category not in categories:
            categories[category] = []
        categories[category].append(site)
    
    return categories

@app.route('/')
def index():
    """首页"""
    categories = get_categories()
    # 获取各分类的前4个网站用于展示
    showcase = {}
    for category, sites in categories.items():
        showcase[category] = sorted(sites, key=lambda x: x.get('rating', 0), reverse=True)[:4]
    
    return render_template('index.html', categories=categories, showcase=showcase)

@app.route('/category/<category_name>')
def category(category_name):
    """分类页面"""
    sites = load_sites()
    category_sites = [site for site in sites if site.get('category') == category_name]
    
    # 获取子分类（如果有）
    subcategories = set()
    for site in category_sites:
        if 'subcategory' in site:
            subcategories.add(site['subcategory'])
    
    return render_template(
        'category.html', 
        category=category_name,
        sites=category_sites,
        subcategories=sorted(list(subcategories))
    )

@app.route('/search')
def search():
    """搜索功能"""
    query = request.args.get('q', '').lower()
    if not query:
        return redirect(url_for('index'))
    
    sites = load_sites()
    results = []
    
    for site in sites:
        # 在网站名称、描述、标签中搜索
        if (query in site.get('name', '').lower() or
            query in site.get('description', '').lower() or
            any(query in tag.lower() for tag in site.get('tags', []))):
            results.append(site)
    
    # 获取所有分类以便在无结果时显示
    categories = get_categories()
    
    return render_template('search.html', query=query, results=results, categories=categories)

@app.route('/about')
def about():
    """关于页面"""
    return render_template('about.html')

# 仅在直接运行此脚本时启动应用
if __name__ == '__main__':
    # 如果数据文件不存在，创建示例数据
    if not os.path.exists(DATA_FILE):
        example_sites = [
            {
                "id": "1",
                "name": "Boston Dynamics",
                "url": "https://www.bostondynamics.com",
                "description": "世界领先的动态机器人技术公司，著名产品包括Atlas人形机器人",
                "category": "研究与学术",
                "tags": ["机器人", "仿生学", "动态控制"],
                "rating": 5,
                "image": "boston_dynamics.png"
            },
            {
                "id": "2",
                "name": "UBTECH Robotics",
                "url": "https://www.ubtrobot.com",
                "description": "优必选，中国领先的人形机器人制造商",
                "category": "产品与企业",
                "tags": ["机器人", "人工智能", "消费级机器人"],
                "rating": 4.5,
                "image": "ubtech.png"
            },
            {
                "id": "3",
                "name": "IEEE Spectrum Robotics",
                "url": "https://spectrum.ieee.org/robotics",
                "description": "机器人技术的权威新闻和分析",
                "category": "新闻与资讯",
                "tags": ["新闻", "技术分析", "趋势"],
                "rating": 4.8,
                "image": "ieee_spectrum.png"
            },
            {
                "id": "4",
                "name": "ROS (Robot Operating System)",
                "url": "https://www.ros.org",
                "description": "机器人操作系统，最流行的机器人软件平台",
                "category": "开源项目与社区",
                "tags": ["开源", "软件", "操作系统"],
                "rating": 5,
                "image": "ros.png"
            }
        ]
        save_sites(example_sites)
    
    app.run(debug=True) 