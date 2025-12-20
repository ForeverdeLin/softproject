# API接口说明文档

## 📋 概述

本文档说明如何使用服务器API接口，让客户端能够共享失物招领数据。

**服务器地址：** `http://localhost:5000` （或你的服务器IP地址）

**所有API接口都支持跨域访问（CORS），客户端可以从任何域名访问。**

---

## 🔑 API接口列表

### 1. 获取所有失物列表

**接口：** `GET /api/lost`

**说明：** 获取服务器上所有失物信息，供客户端同步数据

**请求参数：**
- `include_resolved` (可选): `true` 或 `false`，是否包含已解决的失物，默认为 `false`

**响应示例：**
```json
{
  "success": true,
  "count": 10,
  "data": [
    {
      "id": 1,
      "user_id": 1,
      "item_name": "黑色钱包",
      "category": "钱包",
      "lost_location": "图书馆三楼",
      "lost_time": "2024-01-15T10:30:00",
      "description": "黑色真皮钱包，内有身份证",
      "color": "黑色",
      "brand": null,
      "is_resolved": false
    },
    ...
  ]
}
```

**使用示例：**
```bash
# 获取所有未解决的失物
curl http://localhost:5000/api/lost

# 获取所有失物（包括已解决的）
curl http://localhost:5000/api/lost?include_resolved=true
```

**JavaScript示例：**
```javascript
// 获取所有失物数据
fetch('http://localhost:5000/api/lost')
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      console.log(`获取到 ${data.count} 条失物信息`);
      data.data.forEach(item => {
        console.log(item.item_name, item.lost_location);
      });
    }
  });
```

---

### 2. 获取所有招领列表

**接口：** `GET /api/found`

**说明：** 获取服务器上所有招领信息，供客户端同步数据

**请求参数：**
- `include_resolved` (可选): `true` 或 `false`，是否包含已解决的招领，默认为 `false`

**响应示例：**
```json
{
  "success": true,
  "count": 5,
  "data": [
    {
      "id": 1,
      "user_id": 2,
      "item_name": "黑色钱包",
      "category": "钱包",
      "found_location": "图书馆三楼",
      "found_time": "2024-01-15T11:00:00",
      "description": "黑色真皮钱包",
      "color": "黑色",
      "brand": null,
      "is_resolved": false
    },
    ...
  ]
}
```

**使用示例：**
```bash
# 获取所有未解决的招领
curl http://localhost:5000/api/found

# 获取所有招领（包括已解决的）
curl http://localhost:5000/api/found?include_resolved=true
```

---

### 3. 获取单个失物信息

**接口：** `GET /api/lost/<lost_id>`

**说明：** 根据ID获取单个失物的详细信息

**路径参数：**
- `lost_id`: 失物ID

**响应示例：**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": 1,
    "item_name": "黑色钱包",
    "category": "钱包",
    "lost_location": "图书馆三楼",
    "lost_time": "2024-01-15T10:30:00",
    "description": "黑色真皮钱包，内有身份证",
    "color": "黑色",
    "brand": null,
    "is_resolved": false
  }
}
```

**使用示例：**
```bash
curl http://localhost:5000/api/lost/1
```

---

### 4. 获取单个招领信息

**接口：** `GET /api/found/<found_id>`

**说明：** 根据ID获取单个招领的详细信息

**路径参数：**
- `found_id`: 招领ID

**响应示例：**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": 2,
    "item_name": "黑色钱包",
    "category": "钱包",
    "found_location": "图书馆三楼",
    "found_time": "2024-01-15T11:00:00",
    "description": "黑色真皮钱包",
    "color": "黑色",
    "brand": null,
    "is_resolved": false
  }
}
```

**使用示例：**
```bash
curl http://localhost:5000/api/found/1
```

---

### 5. 发布失物（已存在）

**接口：** `POST /api/lost`

**说明：** 发布新的失物信息到服务器

**请求体：**
```json
{
  "user_id": 1,
  "item_name": "黑色钱包",
  "category": "钱包",
  "lost_location": "图书馆三楼",
  "lost_time": "2024-01-15T10:30:00",
  "description": "黑色真皮钱包，内有身份证",
  "color": "黑色",
  "brand": null
}
```

**响应示例：**
```json
{
  "lost_id": 1,
  "matches": [
    {
      "found_item_id": 2,
      "score": 85.5
    }
  ]
}
```

---

### 6. 发布招领（已存在）

**接口：** `POST /api/found`

**说明：** 发布新的招领信息到服务器

**请求体：**
```json
{
  "user_id": 2,
  "item_name": "黑色钱包",
  "category": "钱包",
  "found_location": "图书馆三楼",
  "found_time": "2024-01-15T11:00:00",
  "description": "黑色真皮钱包",
  "color": "黑色",
  "brand": null
}
```

**响应示例：**
```json
{
  "found_id": 1
}
```

---

### 7. 获取匹配结果（已存在）

**接口：** `GET /api/matches/<lost_id>`

**说明：** 获取指定失物的匹配结果

**路径参数：**
- `lost_id`: 失物ID

**响应示例：**
```json
{
  "matches": [
    {
      "lost_item_id": 1,
      "found_item_id": 2,
      "match_score": 85.5,
      "match_reason": "score=85.5",
      "created_at": "2024-01-15T10:35:00"
    }
  ]
}
```

---

### 8. 获取用户通知列表

**接口：** `GET /api/notifications`

**说明：** 获取用户的通知列表（匹配通知、提醒通知、系统公告）

**请求参数：**
- `user_id` (必需): 用户ID
- `unread_only` (可选): `true` 或 `false`，是否只获取未读通知，默认为 `false`
- `limit` (可选): 返回数量限制，默认为 20

**响应示例：**
```json
{
  "success": true,
  "count": 5,
  "data": [
    {
      "id": 1,
      "type": "match",
      "title": "🎉 高匹配度！发现可能的失物",
      "content": "您的失物\"黑色钱包\"找到了高匹配度的招领信息（匹配度：85.5分），请尽快查看！",
      "is_read": false,
      "created_at": "2024-01-15T10:35:00",
      "related_item_id": 1,
      "related_match_id": 1
    },
    ...
  ]
}
```

**使用示例：**
```bash
# 获取所有通知
curl "http://localhost:5000/api/notifications?user_id=1"

# 只获取未读通知
curl "http://localhost:5000/api/notifications?user_id=1&unread_only=true"

# 限制返回数量
curl "http://localhost:5000/api/notifications?user_id=1&limit=10"
```

---

### 9. 标记通知为已读

**接口：** `POST /api/notifications/<notification_id>/read`

**说明：** 标记指定通知为已读

**路径参数：**
- `notification_id`: 通知ID

**请求体：**
```json
{
  "user_id": 1
}
```

**或使用查询参数：**
```
?user_id=1
```

**响应示例：**
```json
{
  "success": true,
  "message": "已标记为已读"
}
```

**使用示例：**
```bash
# 使用请求体
curl -X POST http://localhost:5000/api/notifications/1/read \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1}'

# 使用查询参数
curl -X POST "http://localhost:5000/api/notifications/1/read?user_id=1"
```

---

### 10. 获取未读通知数量

**接口：** `GET /api/notifications/unread-count`

**说明：** 获取用户的未读通知数量

**请求参数：**
- `user_id` (必需): 用户ID

**响应示例：**
```json
{
  "success": true,
  "unread_count": 3
}
```

**使用示例：**
```bash
curl "http://localhost:5000/api/notifications/unread-count?user_id=1"
```

---

### 11. 检查并发送提醒

**接口：** `POST /api/notifications/check-reminders`

**说明：** 检查未解决的失物/招领，并发送提醒通知（定期任务）

**响应示例：**
```json
{
  "success": true,
  "message": "提醒检查完成"
}
```

**使用示例：**
```bash
curl -X POST http://localhost:5000/api/notifications/check-reminders
```

---

## 🚀 客户端集成示例

### Python客户端示例

```python
import requests

# 服务器地址
BASE_URL = "http://localhost:5000"

# 获取所有失物
def get_all_lost_items(include_resolved=False):
    url = f"{BASE_URL}/api/lost"
    params = {"include_resolved": str(include_resolved).lower()}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            return data.get('data', [])
    return []

# 获取所有招领
def get_all_found_items(include_resolved=False):
    url = f"{BASE_URL}/api/found"
    params = {"include_resolved": str(include_resolved).lower()}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            return data.get('data', [])
    return []

# 使用示例
if __name__ == "__main__":
    lost_items = get_all_lost_items()
    print(f"获取到 {len(lost_items)} 条失物信息")
    for item in lost_items:
        print(f"- {item['item_name']} ({item['lost_location']})")
```

### JavaScript/TypeScript客户端示例

```javascript
// 服务器地址
const BASE_URL = "http://localhost:5000";

// 获取所有失物
async function getAllLostItems(includeResolved = false) {
  const url = `${BASE_URL}/api/lost?include_resolved=${includeResolved}`;
  try {
    const response = await fetch(url);
    const data = await response.json();
    if (data.success) {
      return data.data;
    }
  } catch (error) {
    console.error("获取失物列表失败:", error);
  }
  return [];
}

// 获取所有招领
async function getAllFoundItems(includeResolved = false) {
  const url = `${BASE_URL}/api/found?include_resolved=${includeResolved}`;
  try {
    const response = await fetch(url);
    const data = await response.json();
    if (data.success) {
      return data.data;
    }
  } catch (error) {
    console.error("获取招领列表失败:", error);
  }
  return [];
}

// 使用示例
async function syncData() {
  const lostItems = await getAllLostItems();
  const foundItems = await getAllFoundItems();
  console.log(`同步完成: ${lostItems.length} 条失物, ${foundItems.length} 条招领`);
}
```

---

## 📝 注意事项

1. **跨域访问：** 所有 `/api/*` 接口都支持CORS，允许跨域访问
2. **数据格式：** 所有时间字段使用ISO 8601格式（如：`2024-01-15T10:30:00`）
3. **错误处理：** 所有接口在出错时会返回 `{"success": false, "error": "错误信息"}`
4. **数据过滤：** 默认只返回未解决的失物/招领（`is_resolved=false`），可通过参数获取全部数据
5. **服务器地址：** 如果客户端不在同一台机器，需要将 `localhost` 替换为服务器的实际IP地址

---

## 🔧 启动服务器

```bash
# 安装依赖（如果还没安装）
pip install -r requirements.txt

# 启动服务器
python -m app.main
```

服务器将在 `http://0.0.0.0:5000` 上运行，客户端可以通过以下方式访问：
- 本地访问：`http://localhost:5000`
- 局域网访问：`http://<服务器IP>:5000`

---

**更新时间：** 2024-01-15

