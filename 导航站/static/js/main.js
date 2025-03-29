// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
  // 搜索功能
  const searchForm = document.querySelector('.search-form');
  if (searchForm) {
    searchForm.addEventListener('submit', function(e) {
      const searchInput = this.querySelector('input');
      if (!searchInput.value.trim()) {
        e.preventDefault();
      }
    });
  }

  // 子分类筛选功能
  const subcategoryBtns = document.querySelectorAll('.subcategory-btn');
  if (subcategoryBtns.length > 0) {
    subcategoryBtns.forEach(btn => {
      btn.addEventListener('click', function() {
        const subcategory = this.dataset.subcategory;
        const siteCards = document.querySelectorAll('.site-card');
        
        // 重置所有按钮状态
        subcategoryBtns.forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        
        // 如果选择"全部"，显示所有卡片
        if (subcategory === 'all') {
          siteCards.forEach(card => {
            card.style.display = 'flex';
          });
          return;
        }
        
        // 否则按子分类筛选
        siteCards.forEach(card => {
          if (card.dataset.subcategory === subcategory) {
            card.style.display = 'flex';
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }

  // 视图切换功能（网格/列表）
  const viewToggleBtns = document.querySelectorAll('.view-toggle-btn');
  const sitesContainer = document.querySelector('.sites-grid');
  
  if (viewToggleBtns.length > 0 && sitesContainer) {
    viewToggleBtns.forEach(btn => {
      btn.addEventListener('click', function() {
        const viewType = this.dataset.view;
        
        // 重置所有按钮状态
        viewToggleBtns.forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        
        // 切换视图
        if (viewType === 'grid') {
          sitesContainer.classList.remove('sites-list');
          sitesContainer.classList.add('sites-grid');
        } else {
          sitesContainer.classList.remove('sites-grid');
          sitesContainer.classList.add('sites-list');
        }
      });
    });
  }

  // 给站点卡片添加点击事件，点击整个卡片都可以跳转
  const siteCards = document.querySelectorAll('.site-card');
  siteCards.forEach(card => {
    const link = card.querySelector('a.site-title');
    if (link) {
      const linkUrl = link.getAttribute('href');
      card.addEventListener('click', function(e) {
        // 不干扰卡片内其他可点击元素
        if (e.target.tagName !== 'A') {
          window.open(linkUrl, '_blank');
        }
      });
    }
  });

  // 图片加载错误处理
  const siteImages = document.querySelectorAll('.site-image');
  siteImages.forEach(img => {
    img.addEventListener('error', function() {
      // 设置一个默认的背景颜色和图标
      this.style.backgroundColor = '#f0f0f0';
      this.style.backgroundImage = 'none';
      this.innerHTML = '<div style="height:100%;display:flex;align-items:center;justify-content:center;color:#aaa;">暂无图片</div>';
    });
  });
}); 