# 校园失物招领智能匹配系统

基于规则型智能体的校园失物招领系统，实现失物与招领信息的智能匹配。

## 📋 项目简介

本项目是《软件工程》课程期末大作业，采用面向对象方法开发，嵌入规则型智能体实现感知-决策-执行闭环。

### 核心特性

- ✅ **用户认证系统**：注册、登录、会话管理
- ✅ **信息发布**：发布失物/招领信息
- ✅ **智能匹配**：规则型智能体自动匹配（5条匹配规则）
- ✅ **匹配结果展示**：按匹配度排序展示匹配结果
- ✅ **通知系统**：匹配通知、提醒通知、系统公告
- ✅ **Web界面**：12个完整页面，支持响应式设计
- ✅ **数据库持久化**：SQLite数据库存储
- ✅ **RESTful API**：支持客户端共享数据

## 🚀 一键启动

### 方式1：EXE可执行文件（推荐）

**使用打包好的EXE文件**：

1. **下载EXE文件**：`dist/失物招领系统-服务器.exe和对应数据库文件`
2. **双击运行**：EXE文件
3. **访问系统**：浏览器打开 `http://localhost:5000`

**特点**：
- ✅ 无需安装Python或Docker
- ✅ 双击即可运行
- ✅ 所有依赖已打包

**详细说明**：查看 [打包说明-服务器.md](打包说明-服务器.md)




### 方式2：Docker容器化部署（备选）

**前置要求**：
- Docker Desktop（Windows/Mac）或 Docker + Docker Compose（Linux）
- 确保5000端口未被占用

**启动步骤**：

```bash
# 1. 克隆仓库
git clone https://github.com/ForeverdeLin/softproject.git
cd softproject

# 2. 使用Docker Compose一键启动
docker-compose up -d

# 3. 查看日志
docker-compose logs -f

# 4. 访问系统
# 浏览器打开：http://localhost:5000
```

**停止服务**：

```bash
# 停止并删除容器
docker-compose down

# 停止并删除容器和数据卷（注意：会删除数据库）
docker-compose down -v
```



## 🛠️ 本地开发环境

### 前置要求

- Python 3.8+
- pip

### 安装步骤

```powershell
# 1. 创建虚拟环境（Windows PowerShell）
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务器
python -m app.main

# 4. 访问系统
# 浏览器打开：http://localhost:5000
```

### Linux/Mac 安装

```bash
# 1. 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务器
python -m app.main
```

## 📁 项目结构

```
softProject/
├── app/                    # 应用代码（核心）
│   ├── agent/             # 🤖 智能体模块
│   │   ├── matcher.py     # 匹配引擎（5条规则）
│   │   ├── rule_agent.py  # 规则型智能体
│   │   └── notification_agent.py  # 通知智能体
│   ├── database/          # 💾 数据库模块
│   │   ├── db.py         # 数据库连接
│   │   ├── db_manager.py # 数据库操作
│   │   └── models_db.py  # 数据库表模型
│   ├── auth/              # 🔐 认证模块
│   │   ├── auth_service.py      # 认证服务
│   │   └── session_manager.py   # 会话管理
│   ├── web/               # 🌐 Web界面模块
│   │   ├── routes.py      # Web路由
│   │   ├── templates/     # HTML模板
│   │   └── static/        # 静态文件
│   ├── main.py           # Flask主程序
│   └── models.py         # 业务模型
├── scripts/               # 📜 运行脚本
├── docs/                  # 📚 文档
│   ├── 计划/             # 项目计划
│   ├── 报告/             # 项目报告
│   ├── 说明/             # 使用说明
│   └── 作业文档/         # 作业报告
├── database.db           # SQLite数据库
├── Dockerfile            # Docker镜像构建文件（备选）
├── docker-compose.yml    # Docker Compose配置（备选）
├── build_exe.py          # EXE打包脚本
├── 打包服务器.bat        # 一键打包脚本
├── requirements.txt      # Python依赖
└── README.md            # 本文件
```

## 🎯 核心功能

### 1. 用户管理
- 用户注册（学号、姓名、密码、联系方式）
- 用户登录/登出
- 会话管理

### 2. 信息发布
- 发布失物信息（名称、类别、地点、时间、特征描述）
- 发布招领信息

### 3. 智能匹配（核心功能）

**规则型智能体**实现感知-决策-执行循环：

- **感知阶段**：读取失物/招领信息，从数据库获取相关数据
- **决策阶段**：应用5条匹配规则
  1. 类别匹配（40分）
  2. 地点相似度（25分）
  3. 时间匹配度（20分）
  4. 特征相似度（15分）
  5. 综合评分（总分≥40分才记录）
- **执行阶段**：生成匹配结果，保存到数据库

### 4. 匹配结果展示
- 按匹配度排序
- 显示匹配原因
- 查看详细信息

### 5. 通知系统
- 匹配成功自动通知（高匹配度≥80分发送紧急通知）
- 未解决提醒（超过7天/14天）
- 系统公告
- 通知管理（标记已读、查询未读数量）

### 6. RESTful API
- 支持客户端共享数据
- 10+个API接口
- CORS跨域支持

## 🔧 技术栈

- **后端**：Python 3.9 + Flask 2.3.2
- **数据库**：SQLite（开发）/ MySQL（生产可选）
- **ORM**：SQLAlchemy 2.1.0
- **认证**：Werkzeug（密码加密）
- **前端**：HTML5 + CSS3 + JavaScript + Bootstrap 5
- **部署**：EXE可执行文件打包（PyInstaller）/ Docker（备选）

## 📊 数据库设计

### 数据表（5个）

1. **users** - 用户表
   - id, student_id, name, password_hash, email, phone, created_at

2. **lost_items** - 失物表
   - id, user_id, item_name, category, lost_location, lost_time, description, color, brand, is_resolved

3. **found_items** - 招领表
   - id, user_id, item_name, category, found_location, found_time, description, color, brand, is_resolved

4. **match_records** - 匹配记录表
   - id, lost_item_id, found_item_id, match_score, match_reason, is_notified, created_at

5. **notifications** - 通知表
   - id, user_id, notification_type, title, content, related_item_id, related_match_id, is_read, created_at

## 🧪 测试

### 运行测试脚本

```bash
# 测试数据库初始化
python scripts/test_db_init.py

# 命令行测试
python scripts/run_demo.py

# Web服务测试
python scripts/run_server_demo.py
```

## 📖 使用说明

### 基本流程

1. **注册账号**：访问 `/register` 注册
2. **登录系统**：访问 `/login` 登录
3. **发布失物**：登录后访问 `/post_lost` 发布失物信息
4. **查看匹配**：系统自动匹配，访问 `/matches/<lost_id>` 查看结果
5. **发布招领**：登录后访问 `/post_found` 发布招领信息

### API接口

**核心接口**：
- `POST /api/lost` - 发布失物
- `POST /api/found` - 发布招领
- `GET /api/lost` - 获取失物列表
- `GET /api/found` - 获取招领列表
- `GET /api/matches/<lost_id>` - 获取匹配结果

**通知接口**：
- `GET /api/notifications` - 获取用户通知列表
- `POST /api/notifications/<id>/read` - 标记通知为已读
- `GET /api/notifications/unread-count` - 获取未读通知数量

详细说明见：[API接口说明.md](docs/说明/API接口说明.md)

## 📚 文档

### 作业文档
- **需求分析**：[01-选题与需求分析.md](docs/作业文档/01-选题与需求分析.md)
- **UML建模**：[02-UML系统建模.md](docs/作业文档/02-UML系统建模.md)
- **智能体设计专章**：[16-智能体设计专章.md](docs/作业文档/16-智能体设计专章.md)
- **评分维度文档**：
  - [评分维度1-面向对象建模+代码规范.md](docs/作业文档/评分维度1-面向对象建模+代码规范.md)
  - [评分维度2-数据库+UI完成度.md](docs/作业文档/评分维度2-数据库+UI完成度.md)
  - [评分维度3-智能体功能+性能.md](docs/作业文档/评分维度3-智能体功能+性能.md)
  - [评分维度4-测试+部署+文档.md](docs/作业文档/评分维度4-测试+部署+文档.md)

### 项目文档
- **项目说明**：[项目说明.md](docs/说明/项目说明.md)
- **API接口说明**：[API接口说明.md](docs/说明/API接口说明.md)
- **数据库说明**：[数据库查看说明.md](docs/说明/数据库查看说明.md)
- **部署说明**：[打包说明-服务器.md](打包说明-服务器.md) / [Docker部署说明.md](docs/说明/Docker部署说明.md)

### 测试报告
- **测试报告**：[测试报告.md](docs/报告/测试报告.md)

## 🐛 常见问题

### Q: EXE文件无法运行？
A: 检查：
1. 端口5000是否被占用
2. 防火墙是否允许5000端口
3. 查看 `error.log` 文件获取详细错误信息

### Q: 数据库报错？
A: 删除 `database.db` 文件，重新运行程序会自动创建

### Q: 如何查看数据库内容？
A: 运行 `python scripts/查看数据库.py` 或使用SQLite工具

### Q: 如何修改端口？
A: 修改 `app/main.py` 中的端口配置，或使用环境变量

### Q: Docker启动失败？（备选方案）
A: 检查：
1. Docker是否正常运行
2. 5000端口是否被占用
3. 查看日志：`docker-compose logs`



## 📈 项目统计

- **代码行数**：4300+行（前端2000+，后端1500+，测试800+）
- **页面数量**：12个完整页面
- **API接口**：10+个RESTful接口
- **数据表**：5个核心表
- **测试用例**：17个（通过率100%）
- **匹配准确率**：96%（≥80%，满足要求）
- **响应时间**：< 1秒（满足要求）

## 🔗 相关链接

- **GitHub仓库**：https://github.com/ForeverdeLin/softproject
- **项目文档**：`docs/` 目录

## 👥 团队信息

本项目为《软件工程》课程期末大作业。



## 📄 许可证

本项目仅用于课程作业，不用于商业用途。

---

**项目已可用，开始使用吧！** 🎉

如有问题，请查看文档或提交Issue。

