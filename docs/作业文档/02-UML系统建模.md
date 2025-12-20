# UML 系统建模文档

## 一、用例图（Use Case Diagram）

### 1.1 用例图说明

系统主要参与者：
- **普通用户**：注册用户，可以发布失物/招领信息
- **系统管理员**：管理用户、审核信息
- **智能体系统**：自动匹配失物与招领信息

主要用例：
1. 用户注册/登录
2. 发布失物信息
3. 发布招领信息
4. 智能匹配（智能体）
5. 查看匹配结果
6. 搜索查询
7. 个人信息管理
8. 标记已解决

### 1.2 用例图（PlantUML格式）

```plantuml
@startuml
left to right direction

actor "普通用户" as User
actor "系统管理员" as Admin
rectangle "校园失物招领系统" {
  usecase "用户注册" as UC1
  usecase "用户登录" as UC2
  usecase "发布失物信息" as UC3
  usecase "发布招领信息" as UC4
  usecase "智能匹配" as UC5
  usecase "查看匹配结果" as UC6
  usecase "搜索查询" as UC7
  usecase "查看个人信息" as UC8
  usecase "修改个人信息" as UC9
  usecase "标记已解决" as UC10
  usecase "查看历史记录" as UC11
  usecase "用户管理" as UC12
  usecase "信息审核" as UC13
}

User --> UC1
User --> UC2
User --> UC3
User --> UC4
User --> UC5
User --> UC6
User --> UC7
User --> UC8
User --> UC9
User --> UC10
User --> UC11

Admin --> UC2
Admin --> UC12
Admin --> UC13

UC3 ..> UC5 : <<include>>
UC4 ..> UC5 : <<include>>
UC5 ..> UC6 : <<include>>

@enduml
```

### 1.3 用例详细描述

#### UC1: 用户注册
- **参与者**：普通用户
- **前置条件**：无
- **后置条件**：用户账号创建成功
- **基本流程**：
  1. 用户输入学号、姓名、密码、联系方式
  2. 系统验证信息格式
  3. 检查学号是否已注册
  4. 创建用户账号
  5. 返回注册成功

#### UC2: 用户登录
- **参与者**：普通用户、系统管理员
- **前置条件**：用户已注册
- **后置条件**：用户登录成功，获得访问权限
- **基本流程**：
  1. 用户输入学号和密码
  2. 系统验证账号密码
  3. 创建会话
  4. 跳转到主页

#### UC3: 发布失物信息
- **参与者**：普通用户
- **前置条件**：用户已登录
- **后置条件**：失物信息保存到数据库，触发智能匹配
- **基本流程**：
  1. 用户填写失物信息（名称、类别、地点、时间、特征描述）
  2. 可选上传图片
  3. 系统保存信息
  4. 触发智能匹配用例

#### UC4: 发布招领信息
- **参与者**：普通用户
- **前置条件**：用户已登录
- **后置条件**：招领信息保存到数据库，触发智能匹配
- **基本流程**：
  1. 用户填写招领信息（名称、类别、地点、时间、特征描述）
  2. 可选上传图片
  3. 系统保存信息
  4. 触发智能匹配用例

#### UC5: 智能匹配（核心用例）
- **参与者**：智能体系统
- **前置条件**：有新的失物或招领信息发布
- **后置条件**：生成匹配结果列表
- **基本流程**：
  1. 智能体感知：读取新发布的信息
  2. 从数据库获取所有相关记录
  3. 提取特征（类别、地点、时间、颜色等）
  4. 应用匹配规则：
     - 规则1：类别匹配
     - 规则2：地点相似度
     - 规则3：时间匹配度
     - 规则4：特征相似度
     - 规则5：综合评分
  5. 生成匹配结果（按匹配度排序）
  6. 保存匹配记录
  7. 发送通知（可选）

---

## 二、类图（Class Diagram）

### 2.1 类图说明

系统核心类：
1. **User（用户类）**：用户信息管理
2. **LostItem（失物类）**：失物信息
3. **FoundItem（招领类）**：招领信息
4. **MatchRecord（匹配记录类）**：匹配结果记录
5. **RuleAgent（规则智能体类）**：核心智能体
6. **Matcher（匹配引擎类）**：匹配算法实现
7. **DatabaseManager（数据库管理类）**：数据库操作
8. **NotificationService（通知服务类）**：消息通知

### 2.2 类图（PlantUML格式）

```plantuml
@startuml

class User {
  -int user_id
  -String student_id
  -String name
  -String password_hash
  -String email
  -String phone
  -DateTime created_at
  +register()
  +login()
  +update_profile()
  +get_user_info()
}

class LostItem {
  -int item_id
  -int user_id
  -String item_name
  -String category
  -String lost_location
  -DateTime lost_time
  -String description
  -String color
  -String brand
  -String image_path
  -String contact
  -bool is_resolved
  -DateTime created_at
  +create_lost_item()
  +update_item()
  +mark_resolved()
  +get_item_info()
}

class FoundItem {
  -int item_id
  -int user_id
  -String item_name
  -String category
  -String found_location
  -DateTime found_time
  -String description
  -String color
  -String brand
  -String image_path
  -String contact
  -bool is_resolved
  -DateTime created_at
  +create_found_item()
  +update_item()
  +mark_resolved()
  +get_item_info()
}

class MatchRecord {
  -int match_id
  -int lost_item_id
  -int found_item_id
  -float match_score
  -String match_reason
  -bool is_notified
  -DateTime created_at
  +create_match_record()
  +update_notification_status()
  +get_match_details()
}

class RuleAgent {
  -Matcher matcher
  -DatabaseManager db_manager
  -NotificationService notification_service
  +perceive(lost_item: LostItem, found_items: List<FoundItem>)
  +decide(lost_item: LostItem, found_item: FoundItem): float
  +execute(matches: List<MatchRecord>)
  +match_cycle(lost_item: LostItem)
}

class Matcher {
  +match_by_category(lost: LostItem, found: FoundItem): float
  +match_by_location(lost: LostItem, found: FoundItem): float
  +match_by_time(lost: LostItem, found: FoundItem): float
  +match_by_features(lost: LostItem, found: FoundItem): float
  +calculate_total_score(lost: LostItem, found: FoundItem): float
  +extract_features(item: LostItem | FoundItem): dict
}

class DatabaseManager {
  -Connection connection
  +connect()
  +disconnect()
  +create_user(user: User): bool
  +get_user_by_id(user_id: int): User
  +get_user_by_student_id(student_id: String): User
  +create_lost_item(item: LostItem): bool
  +create_found_item(item: FoundItem): bool
  +get_all_found_items(): List<FoundItem>
  +get_all_lost_items(): List<LostItem>
  +create_match_record(record: MatchRecord): bool
  +get_match_records_by_lost_item(lost_item_id: int): List<MatchRecord>
}

class NotificationService {
  +send_match_notification(user: User, match: MatchRecord)
  +send_email_notification(email: String, message: String)
}

' 关系定义
User "1" --> "*" LostItem : 发布
User "1" --> "*" FoundItem : 发布
LostItem "1" --> "*" MatchRecord : 匹配
FoundItem "1" --> "*" MatchRecord : 匹配
RuleAgent --> Matcher : 使用
RuleAgent --> DatabaseManager : 使用
RuleAgent --> NotificationService : 使用
DatabaseManager --> User : 管理
DatabaseManager --> LostItem : 管理
DatabaseManager --> FoundItem : 管理
DatabaseManager --> MatchRecord : 管理

@enduml
```

### 2.3 核心类详细设计

#### 2.3.1 User类
```python
class User:
    """用户类 - 管理用户信息"""
    def __init__(self, student_id, name, password, email, phone):
        self.user_id = None
        self.student_id = student_id
        self.name = name
        self.password_hash = self._hash_password(password)
        self.email = email
        self.phone = phone
        self.created_at = datetime.now()
    
    def register(self):
        """注册新用户"""
        pass
    
    def login(self, password):
        """用户登录验证"""
        pass
    
    def update_profile(self, **kwargs):
        """更新个人信息"""
        pass
```

#### 2.3.2 LostItem类
```python
class LostItem:
    """失物类 - 失物信息"""
    def __init__(self, user_id, item_name, category, 
                 lost_location, lost_time, description, 
                 color=None, brand=None, image_path=None):
        self.item_id = None
        self.user_id = user_id
        self.item_name = item_name
        self.category = category
        self.lost_location = lost_location
        self.lost_time = lost_time
        self.description = description
        self.color = color
        self.brand = brand
        self.image_path = image_path
        self.is_resolved = False
        self.created_at = datetime.now()
    
    def create_lost_item(self):
        """创建失物记录"""
        pass
    
    def mark_resolved(self):
        """标记为已解决"""
        self.is_resolved = True
```

#### 2.3.3 RuleAgent类（核心智能体）
```python
class RuleAgent:
    """规则型智能体 - 实现感知-决策-执行循环"""
    def __init__(self):
        self.matcher = Matcher()
        self.db_manager = DatabaseManager()
        self.notification_service = NotificationService()
    
    def perceive(self, lost_item, found_items):
        """感知阶段：获取环境信息"""
        # 从数据库获取所有招领信息
        # 提取特征
        features = self.matcher.extract_features(lost_item)
        return found_items, features
    
    def decide(self, lost_item, found_item):
        """决策阶段：应用匹配规则"""
        score = self.matcher.calculate_total_score(lost_item, found_item)
        return score
    
    def execute(self, matches):
        """执行阶段：保存结果并发送通知"""
        for match in matches:
            self.db_manager.create_match_record(match)
            if match.match_score >= 60:
                # 发送高匹配度通知
                user = self.db_manager.get_user_by_id(match.lost_item.user_id)
                self.notification_service.send_match_notification(user, match)
    
    def match_cycle(self, lost_item):
        """完整的感知-决策-执行循环"""
        # 感知
        found_items, features = self.perceive(lost_item, None)
        
        # 决策
        matches = []
        for found_item in found_items:
            score = self.decide(lost_item, found_item)
            if score >= 40:  # 最低匹配阈值
                match = MatchRecord(
                    lost_item_id=lost_item.item_id,
                    found_item_id=found_item.item_id,
                    match_score=score,
                    match_reason=self._generate_reason(lost_item, found_item, score)
                )
                matches.append(match)
        
        # 按匹配度排序
        matches.sort(key=lambda x: x.match_score, reverse=True)
        
        # 执行
        self.execute(matches)
        
        return matches
```

#### 2.3.4 Matcher类（匹配引擎）
```python
class Matcher:
    """匹配引擎 - 实现各种匹配规则"""
    
    def match_by_category(self, lost, found):
        """规则1：类别匹配（40分）"""
        if lost.category == found.category:
            return 40.0
        return 0.0
    
    def match_by_location(self, lost, found):
        """规则2：地点相似度（25分）"""
        # 地点匹配逻辑
        if lost.lost_location == found.found_location:
            return 25.0
        elif self._is_nearby(lost.lost_location, found.found_location):
            return 20.0
        elif self._is_same_campus(lost.lost_location, found.found_location):
            return 15.0
        else:
            return 5.0
    
    def match_by_time(self, lost, found):
        """规则3：时间匹配度（20分）"""
        time_diff = abs((found.found_time - lost.lost_time).total_seconds() / 3600)
        if time_diff <= 24:
            return 20.0
        elif time_diff <= 72:
            return 15.0
        elif time_diff <= 168:
            return 10.0
        else:
            return 5.0
    
    def match_by_features(self, lost, found):
        """规则4：特征相似度（15分）"""
        score = 0.0
        # 颜色匹配（5分）
        if lost.color and found.color and lost.color == found.color:
            score += 5.0
        # 品牌匹配（5分）
        if lost.brand and found.brand and lost.brand == found.brand:
            score += 5.0
        # 描述关键词匹配（最多5分）
        score += self._keyword_match(lost.description, found.description, max_score=5.0)
        return min(score, 15.0)
    
    def calculate_total_score(self, lost, found):
        """规则5：综合评分"""
        category_score = self.match_by_category(lost, found)
        if category_score == 0:  # 类别不匹配，直接返回0
            return 0.0
        
        location_score = self.match_by_location(lost, found)
        time_score = self.match_by_time(lost, found)
        feature_score = self.match_by_features(lost, found)
        
        total = category_score + location_score + time_score + feature_score
        return total
```

---

## 三、顺序图（Sequence Diagram）

### 3.1 用户发布失物信息并触发智能匹配（核心流程）

```plantuml
@startuml
actor 用户
participant "Web界面" as UI
participant "LostItemController" as Controller
participant "DatabaseManager" as DB
participant "RuleAgent" as Agent
participant "Matcher" as Matcher
participant "NotificationService" as Notify

用户 -> UI: 填写失物信息并提交
UI -> Controller: create_lost_item(item_data)
Controller -> DB: create_lost_item(item)
DB -> DB: 保存到数据库
DB --> Controller: 返回item_id

Controller -> Agent: match_cycle(lost_item)

note over Agent: 感知阶段
Agent -> DB: get_all_found_items()
DB --> Agent: 返回所有招领信息列表

note over Agent: 决策阶段
loop 遍历每个招领信息
    Agent -> Matcher: calculate_total_score(lost, found)
    Matcher -> Matcher: match_by_category()
    Matcher -> Matcher: match_by_location()
    Matcher -> Matcher: match_by_time()
    Matcher -> Matcher: match_by_features()
    Matcher --> Agent: 返回匹配分数
    alt 匹配分数 >= 40
        Agent -> Agent: 创建MatchRecord对象
    end
end
Agent -> Agent: 按匹配度排序

note over Agent: 执行阶段
loop 遍历匹配结果
    Agent -> DB: create_match_record(match)
    DB --> Agent: 保存成功
    alt 匹配分数 >= 60
        Agent -> Notify: send_match_notification(user, match)
        Notify -> 用户: 发送通知消息
    end
end

Agent --> Controller: 返回匹配结果列表
Controller --> UI: 显示匹配结果
UI --> 用户: 展示匹配信息

@enduml
```

### 3.2 用户查看匹配结果流程

```plantuml
@startuml
actor 用户
participant "Web界面" as UI
participant "MatchController" as Controller
participant "DatabaseManager" as DB
participant "MatchRecord" as Record

用户 -> UI: 点击查看匹配结果
UI -> Controller: get_match_results(lost_item_id)
Controller -> DB: get_match_records_by_lost_item(lost_item_id)
DB -> DB: 查询数据库
DB --> Controller: 返回MatchRecord列表
Controller -> Controller: 格式化数据
Controller --> UI: 返回匹配结果（含匹配度、原因）
UI --> 用户: 显示匹配列表

用户 -> UI: 点击查看详细信息
UI -> Controller: get_match_details(match_id)
Controller -> DB: get_match_details(match_id)
DB --> Controller: 返回详细信息
Controller --> UI: 返回失物和招领的完整信息
UI --> 用户: 显示详细信息

@enduml
```

### 3.3 智能体匹配决策详细流程

```plantuml
@startuml
participant "RuleAgent" as Agent
participant "Matcher" as Matcher
participant "LostItem" as Lost
participant "FoundItem" as Found

Agent -> Matcher: calculate_total_score(lost_item, found_item)

Matcher -> Matcher: match_by_category(lost, found)
note right: 规则1：类别匹配\n类别相同=40分，不同=0分
alt 类别不匹配
    Matcher --> Agent: 返回0分（直接排除）
else 类别匹配
    Matcher -> Matcher: match_by_location(lost, found)
    note right: 规则2：地点相似度\n同一地点=25分\n相邻区域=20分\n同校区=15分\n不同校区=5分
    
    Matcher -> Matcher: match_by_time(lost, found)
    note right: 规则3：时间匹配度\n24小时内=20分\n3天内=15分\n一周内=10分\n超过一周=5分
    
    Matcher -> Matcher: match_by_features(lost, found)
    note right: 规则4：特征相似度\n颜色匹配=5分\n品牌匹配=5分\n关键词匹配=最多5分
    
    Matcher -> Matcher: 计算总分
    note right: 规则5：综合评分\n总分 = 类别(40) + 地点(25) + 时间(20) + 特征(15)
    Matcher --> Agent: 返回总分
end

@enduml
```

---

## 四、UML建模总结

### 4.1 用例图总结
- **参与者**：2个（普通用户、系统管理员）
- **用例**：13个核心用例
- **关系**：包含关系（发布信息包含智能匹配）

### 4.2 类图总结
- **核心类**：8个主要类
- **关系类型**：
  - 关联关系：User与LostItem/FoundItem（一对多）
  - 组合关系：RuleAgent包含Matcher、DatabaseManager、NotificationService
  - 依赖关系：各类依赖DatabaseManager进行数据操作

### 4.3 顺序图总结
- **核心流程**：3个主要顺序图
  1. 发布失物并触发智能匹配（展示完整的感知-决策-执行循环）
  2. 查看匹配结果
  3. 智能体决策详细流程

### 4.4 智能体设计验证
✅ **感知阶段**：从数据库获取环境信息（失物/招领记录）  
✅ **决策阶段**：应用5种匹配规则（≥3种决策分支，满足要求）  
✅ **执行阶段**：保存结果、发送通知、更新状态  

---

## 五、下一步工作

1. ✅ **UML建模完成**（当前步骤）
2. ⏭️ **数据库详细设计**（ER图、表结构、索引设计）
3. ⏭️ **智能体算法详细实现**
4. ⏭️ **编码实现**

---

## 附录：PlantUML使用说明

1. 在线工具：http://www.plantuml.com/plantuml/uml/
2. VS Code插件：PlantUML
3. 导出格式：PNG、SVG、PDF

