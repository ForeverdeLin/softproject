# 评分维度2：数据库+UI完成度（15%）

## 一、数据库设计

### 1.1 数据库选型

**选择SQLite作为开发环境数据库**

**选择理由**：
- ✅ 无需安装，零配置
- ✅ 适合中小型应用
- ✅ 支持完整的SQL功能
- ✅ 易于迁移到MySQL（生产环境）

**位置**：`docs/作业文档/实验报告.txt` 第6.1节

### 1.2 数据库表设计

#### 1.2.1 users（用户表）
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    student_id VARCHAR(64) UNIQUE NOT NULL,
    name VARCHAR(128) NOT NULL,
    email VARCHAR(256),
    password_hash VARCHAR(256) NOT NULL,
    phone VARCHAR(64),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**字段说明**：
- `id`：主键，自增
- `student_id`：学号，唯一索引
- `name`：姓名
- `email`：邮箱
- `password_hash`：密码哈希值（加密存储）
- `phone`：联系电话
- `created_at`：创建时间

**位置**：`app/database/models_db.py` - UserDB类

#### 1.2.2 lost_items（失物表）
```sql
CREATE TABLE lost_items (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    item_name VARCHAR(256) NOT NULL,
    category VARCHAR(64) NOT NULL,
    lost_location VARCHAR(256) NOT NULL,
    lost_time DATETIME NOT NULL,
    description TEXT,
    color VARCHAR(64),
    brand VARCHAR(128),
    is_resolved BOOLEAN DEFAULT 0
);
```

**字段说明**：
- `id`：主键
- `user_id`：发布用户ID（外键）
- `item_name`：物品名称
- `category`：类别（钱包/手机/书籍/其他）
- `lost_location`：丢失地点
- `lost_time`：丢失时间
- `description`：描述
- `color`：颜色
- `brand`：品牌
- `is_resolved`：是否已解决

**位置**：`app/database/models_db.py` - LostItemDB类

#### 1.2.3 found_items（招领表）
```sql
CREATE TABLE found_items (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    item_name VARCHAR(256) NOT NULL,
    category VARCHAR(64) NOT NULL,
    found_location VARCHAR(256) NOT NULL,
    found_time DATETIME NOT NULL,
    description TEXT,
    color VARCHAR(64),
    brand VARCHAR(128),
    is_resolved BOOLEAN DEFAULT 0
);
```

**字段说明**：类似失物表，包含拾获地点和时间

**位置**：`app/database/models_db.py` - FoundItemDB类

#### 1.2.4 match_records（匹配记录表）
```sql
CREATE TABLE match_records (
    id INTEGER PRIMARY KEY,
    lost_item_id INTEGER NOT NULL,
    found_item_id INTEGER NOT NULL,
    match_score FLOAT NOT NULL,
    match_reason TEXT,
    is_notified BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**字段说明**：
- `lost_item_id`：失物ID（外键）
- `found_item_id`：招领ID（外键）
- `match_score`：匹配分数（0-100）
- `match_reason`：匹配原因
- `is_notified`：是否已通知
- `created_at`：创建时间

**位置**：`app/database/models_db.py` - MatchRecordDB类

#### 1.2.5 notifications（通知表）
```sql
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    notification_type VARCHAR(64) NOT NULL,
    title VARCHAR(256) NOT NULL,
    content TEXT NOT NULL,
    related_item_id INTEGER,
    related_match_id INTEGER,
    is_read BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**字段说明**：
- `user_id`：接收通知的用户ID（外键）
- `notification_type`：通知类型（match/reminder/announcement）
- `title`：通知标题
- `content`：通知内容
- `related_item_id`：相关物品ID
- `related_match_id`：相关匹配记录ID
- `is_read`：是否已读
- `created_at`：创建时间

**位置**：`app/database/models_db.py` - NotificationDB类

### 1.3 数据关系

**外键关系**：
- `lost_items.user_id` → `users.id`
- `found_items.user_id` → `users.id`
- `match_records.lost_item_id` → `lost_items.id`
- `match_records.found_item_id` → `found_items.id`
- `notifications.user_id` → `users.id`

**关系类型**：
- 一对多：User → LostItem/FoundItem
- 多对多：LostItem ↔ FoundItem（通过MatchRecord）

### 1.4 索引设计

为提高查询性能，在以下字段创建索引：

- `users.student_id`：唯一索引（登录查询）
- `lost_items.category`：索引（类别搜索）
- `lost_items.lost_time`：索引（时间排序）
- `found_items.category`：索引（类别搜索）
- `match_records.lost_item_id`：索引（匹配查询）
- `match_records.found_item_id`：索引（匹配查询）

**位置**：`app/database/models_db.py` - 使用SQLAlchemy的Index定义

### 1.5 数据库操作

#### 1.5.1 ORM框架
- **使用SQLAlchemy 2.1.0**作为ORM框架
- **优势**：避免直接SQL，防止SQL注入，代码更安全

#### 1.5.2 DatabaseManager类
- **职责**：封装所有数据库操作
- **核心方法**：
  - `create_lost_item()`：创建失物记录
  - `create_found_item()`：创建招领记录
  - `get_all_found_items()`：获取所有招领信息
  - `create_match_record()`：创建匹配记录
  - `get_match_records_by_lost_item()`：获取匹配结果
  - `get_user_notifications()`：获取用户通知

**位置**：`app/database/db_manager.py`

---

## 二、UI完成度

### 2.1 页面数量与功能

#### 2.1.1 页面列表（12个页面）

1. **index.html** - 首页
   - 失物/招领列表展示
   - 支持搜索、筛选、排序
   - 响应式设计

2. **login.html** - 登录页
   - 用户登录表单
   - 表单验证
   - 错误提示

3. **register.html** - 注册页
   - 用户注册表单
   - 信息验证
   - 密码强度提示

4. **post_lost.html** - 发布失物
   - 失物信息发布表单
   - 多字段输入
   - 表单验证

5. **post_found.html** - 发布招领
   - 招领信息发布表单
   - 多字段输入
   - 表单验证

6. **matches.html** - 匹配结果页
   - 显示智能匹配结果
   - 按匹配度排序
   - 显示匹配原因

7. **lost_detail.html** - 失物详情页
   - 失物详细信息展示
   - 匹配结果链接
   - 操作按钮

8. **found_detail.html** - 招领详情页
   - 招领详细信息展示
   - 操作按钮

9. **notifications.html** - 通知中心
   - 通知列表展示
   - 已读/未读状态
   - 标记已读功能

10. **profile.html** - 用户主页
    - 用户发布记录
    - 统计信息
    - 个人信息管理

11. **about.html** - 关于我们
    - 团队介绍
    - 项目说明

12. **base.html** - 基础模板
    - 统一页面布局
    - 导航栏
    - 页脚

**位置**：`app/web/templates/`

### 2.2 前端技术栈

#### 2.2.1 HTML5
- 语义化标签
- 表单验证
- 响应式设计

#### 2.2.2 CSS3
- 自定义样式：`app/web/static/css/style.css`
- Bootstrap 5框架集成
- 响应式布局
- 现代化UI设计

#### 2.2.3 JavaScript
- 原生JavaScript实现交互
- AJAX异步请求
- 表单验证
- 动态内容加载

**位置**：`app/web/static/js/main.js`

#### 2.2.4 Bootstrap 5
- 响应式框架
- 组件库（按钮、表单、卡片等）
- 网格系统

### 2.3 UI设计特点

#### 2.3.1 响应式设计
- ✅ 适配PC端（桌面浏览器）
- ✅ 适配移动端（手机、平板）
- ✅ 使用Bootstrap网格系统
- ✅ 媒体查询优化

#### 2.3.2 用户体验
- ✅ 统一的视觉风格
- ✅ 清晰的页面层次
- ✅ 友好的错误提示
- ✅ 流畅的操作流程
- ✅ 加载状态提示

#### 2.3.3 交互功能
- ✅ 搜索与筛选
- ✅ 表单验证
- ✅ AJAX异步请求
- ✅ 实时通知更新
- ✅ 分页功能

### 2.4 模板引擎

#### 2.4.1 Jinja2模板引擎
- Flask内置模板引擎
- 模板继承（base.html）
- 变量传递和渲染
- 条件判断和循环

**示例**：
```jinja2
{% extends "base.html" %}
{% block content %}
    <h1>失物列表</h1>
    {% for item in lost_items %}
        <div class="card">
            <h3>{{ item.item_name }}</h3>
            <p>类别：{{ item.category }}</p>
            <p>地点：{{ item.lost_location }}</p>
        </div>
    {% endfor %}
{% endblock %}
```

### 2.5 UI完成度统计

#### 2.5.1 页面完成度
- **总页面数**：12个
- **已完成页面**：12个
- **完成率**：100%

#### 2.5.2 功能完成度
- ✅ 用户注册/登录
- ✅ 发布失物/招领
- ✅ 查看匹配结果
- ✅ 搜索和筛选
- ✅ 通知中心
- ✅ 个人主页
- ✅ 响应式设计

#### 2.5.3 代码统计
- **HTML模板**：12个文件
- **CSS文件**：1个主样式文件（约500行）
- **JavaScript文件**：1个主交互文件（约300行）
- **总代码量**：约2000+行

---

## 三、数据库+UI集成

### 3.1 数据流

```
用户操作 → Web界面 → Flask路由 → DatabaseManager → SQLite数据库
                ↓
           返回数据 → Jinja2渲染 → HTML页面 → 用户看到结果
```

### 3.2 关键功能实现

#### 3.2.1 发布失物流程
1. 用户在`post_lost.html`填写表单
2. 提交到`/api/lost`接口
3. DatabaseManager保存到数据库
4. 触发智能匹配
5. 返回匹配结果，显示在`matches.html`

#### 3.2.2 查看匹配结果流程
1. 用户在首页点击"查看匹配结果"
2. 路由到`/matches/<lost_id>`
3. DatabaseManager查询匹配记录
4. Jinja2渲染`matches.html`
5. 显示匹配列表（按分数排序）

#### 3.2.3 通知中心流程
1. 智能体生成匹配后，创建通知记录
2. 用户在`notifications.html`查看通知
3. DatabaseManager查询用户通知
4. 显示通知列表，支持标记已读

---

## 四、总结

### 4.1 数据库完成度
✅ **表设计**：5个核心表，结构完整  
✅ **关系设计**：外键关系清晰  
✅ **索引优化**：关键字段建立索引  
✅ **ORM使用**：SQLAlchemy，代码安全  
✅ **数据持久化**：SQLite，数据可靠  

### 4.2 UI完成度
✅ **页面数量**：12个完整页面  
✅ **功能完整**：所有核心功能都有对应页面  
✅ **响应式设计**：适配多种设备  
✅ **用户体验**：界面美观，交互流畅  
✅ **技术栈**：HTML5 + CSS3 + JavaScript + Bootstrap 5  

### 4.3 集成完成度
✅ **数据流**：数据库与UI无缝集成  
✅ **功能实现**：所有功能都正常工作  
✅ **代码质量**：代码规范，结构清晰  

---

**文档位置**：
- 数据库设计详细内容：`docs/作业文档/实验报告.txt` 第6章
- UI设计详细内容：`docs/作业文档/实验报告.txt` 第8章
- 前端代码：`app/web/templates/` 和 `app/web/static/`
- 数据库代码：`app/database/`

