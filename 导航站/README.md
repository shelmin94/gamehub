# 具身智能人形机器人导航站

这是一个为机器人企业产品经理设计的导航平台，提供行业资讯和技术参考。项目采用轻量级Flask实现，针对资源受限环境（2GB内存）进行了优化。

## 主要功能

- 分类浏览：多层次的网站分类系统，包括主分类和子分类
- 搜索功能：支持关键词搜索，可在网站名称、描述和标签中匹配
- 推荐资源：首页展示各分类的高质量精选资源
- 标签系统：通过标签快速定位特定主题的资源
- 链接检查：定期检查收录网站的有效性，确保内容时效性

## 技术栈

- **后端**：Flask (轻量级Web框架)
- **前端**：HTML5 + CSS3 + 原生JavaScript
- **数据存储**：JSON文件（无需数据库）
- **依赖管理**：Pip (requirements.txt)

## 项目结构

```
robot_nav/
│
├── app.py                 # 主应用入口
├── link_checker.py        # 链接检查工具
├── requirements.txt       # 项目依赖
├── README.md              # 项目说明
│
├── data/                  # 数据文件目录
│   ├── sites.json         # 导航站点数据
│   └── status.json        # 链接状态数据
│
├── static/                # 静态资源
│   ├── css/               # 样式文件
│   │   └── style.css      # 主样式文件
│   ├── js/                # JavaScript文件
│   │   └── main.js        # 主JS文件
│   └── images/            # 图片资源
│
└── templates/             # HTML模板
    ├── base.html          # 基础模板
    ├── index.html         # 首页
    ├── category.html      # 分类页面
    ├── search.html        # 搜索结果页面
    └── about.html         # 关于页面
```

## 安装与启动

1. 克隆仓库：
   ```
   git clone https://github.com/your-username/robot-nav.git
   cd robot-nav
   ```

2. 创建虚拟环境（可选但推荐）：
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

4. 启动应用：
   ```
   python app.py
   ```

5. 访问网站：
   在浏览器中打开 http://127.0.0.1:5000

## 链接检查工具使用

链接检查工具用于定期验证收录网站的有效性，保证导航站的内容质量。

- 立即执行检查：
  ```
  python link_checker.py --now
  ```

- 设置定时检查任务：
  ```
  python link_checker.py --schedule
  ```
  默认每天凌晨2点自动执行检查

## 性能优化

为适应资源受限环境，项目采取了以下优化措施：

- 使用JSON文件存储数据，避免数据库额外开销
- 最小化CSS/JS，减少传输大小
- 图片懒加载，优化首屏加载速度
- 合理的缓存策略，减少重复处理
- 分批处理链接检查，控制内存使用

## 扩展性考虑

项目设计保持简单，同时预留了未来功能扩展的可能性：

- 用户反馈系统：收集用户对网站资源的评价和建议
- 管理界面：简化内容维护和链接状态监控
- 数据可视化：展示网站资源分布和使用情况
- 个性化推荐：基于用户浏览历史推荐相关资源 