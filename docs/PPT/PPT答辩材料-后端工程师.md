# 后端工程师 - PPT答辩材料

## 📋 岗位职责

### 主要职责
- Flask应用开发与架构设计
- 数据库设计与ORM操作
- RESTful API接口实现
- 用户认证与会话管理系统
- 业务逻辑实现与数据验证

---

## 📊 PPT展示内容

### 1. 工作职责概述
```
┌─────────────────────────────────────┐
│  后端工程师 - 核心职责              │
├─────────────────────────────────────┤
│  • Flask应用架构设计                 │
│  • 数据库设计与SQLAlchemy ORM        │
│  • RESTful API开发（10+接口）        │
│  • 用户认证与权限管理                │
│  • 业务逻辑与数据验证                │
└─────────────────────────────────────┘
```

### 2. 技术实现

#### 2.1 Flask应用架构
- **主程序**：`app/main.py` - 应用初始化与API路由
- **Web路由**：`app/web/routes.py` - 12个页面路由
- **蓝图设计**：模块化架构，分离API与Web界面

#### 2.2 数据库设计
- **ORM框架**：SQLAlchemy 2.1.0
- **数据表**：4个核心表（users, lost_items, found_items, match_records）
- **数据库管理**：`DatabaseManager`类封装所有CRUD操作
- **会话管理**：使用Session模式，确保数据一致性

#### 2.3 API接口实现
```
已实现10+ RESTful API接口：
✓ POST /api/lost          - 发布失物
✓ POST /api/found         - 发布招领
✓ GET  /api/lost          - 获取失物列表
✓ GET  /api/found         - 获取招领列表
✓ GET  /api/matches/:id   - 获取匹配结果
✓ GET  /api/notifications - 获取通知列表
✓ POST /api/notifications/:id/read - 标记已读
```

#### 2.4 认证系统
- **密码加密**：使用Werkzeug进行密码哈希
- **会话管理**：Flask Session实现用户登录状态
- **权限控制**：`@login_required`装饰器保护敏感路由
- **用户服务**：`AuthService`封装注册、登录逻辑

### 3. 核心功能实现

#### 3.1 数据持久化
- 失物/招领信息的增删改查
- 匹配记录的自动生成与存储
- 通知系统的数据管理

#### 3.2 业务逻辑
- 数据验证与错误处理
- 跨域访问支持（CORS）
- 智能体匹配结果集成
- 通知系统触发机制

### 4. 技术亮点

✅ **模块化设计**：采用Blueprint实现代码分离  
✅ **ORM封装**：统一的数据库操作接口  
✅ **RESTful规范**：标准化的API设计  
✅ **安全性**：密码加密、会话管理、权限控制  
✅ **可扩展性**：易于添加新功能和接口  

---

## 🎤 口头讲述内容（1分钟版本）

**大家好，我是后端工程师黄丽莹。**

我负责系统的后端开发，主要包括三个方面：

**第一，Flask应用架构设计。** 我使用Flask框架搭建了完整的Web应用，采用Blueprint实现模块化，分离了API和Web界面，代码结构清晰。

**第二，数据库设计与操作。** 我使用SQLAlchemy ORM设计了4个核心数据表，并封装了DatabaseManager类，统一管理所有数据库操作，包括失物、招领、匹配记录和用户信息的增删改查。

**第三，API接口与认证系统。** 我实现了10多个RESTful API接口，支持失物招领的发布、查询和匹配。同时开发了完整的用户认证系统，包括注册、登录、会话管理和权限控制，使用密码加密确保安全性。

整个后端系统采用模块化设计，代码规范，易于维护和扩展。谢谢大家！

---

## 📝 详细工作内容（备用）

### 实现思路

1. **架构设计**
   - 采用MVC模式，分离业务逻辑与视图
   - 使用Flask Blueprint实现模块化
   - 统一的错误处理机制

2. **数据库设计**
   - 分析业务需求，设计4个核心表
   - 使用SQLAlchemy ORM避免直接SQL
   - 实现数据模型与业务模型的转换

3. **API设计**
   - 遵循RESTful规范
   - 统一的JSON响应格式
   - 完善的错误处理

4. **安全设计**
   - 密码使用Werkzeug加密存储
   - Session管理用户登录状态
   - 装饰器实现权限控制

### 实现方法

1. **Flask应用初始化**
   ```python
   - 创建Flask应用实例
   - 配置CORS支持跨域
   - 注册Blueprint
   - 定义API路由
   ```

2. **数据库操作封装**
   ```python
   - DatabaseManager类统一管理
   - 使用Session模式
   - 实现CRUD方法
   - 数据模型转换
   ```

3. **认证系统实现**
   ```python
   - AuthService处理注册登录
   - SessionManager管理会话
   - @login_required装饰器
   - 密码哈希存储
   ```

### 关键技术点

- **Flask 2.3.2**：轻量级Web框架
- **SQLAlchemy 2.1.0**：ORM框架
- **Werkzeug**：密码加密工具
- **Flask-CORS**：跨域访问支持
- **Blueprint**：模块化架构

### 工作量统计

- **代码文件**：5个核心文件（main.py, routes.py, db_manager.py, auth_service.py, session_manager.py）
- **API接口**：10+个RESTful接口
- **数据库表**：4个核心表
- **代码行数**：约1500+行

