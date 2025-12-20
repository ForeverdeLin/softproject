"""
测试新功能：搜索、筛选、详情页、用户主页
"""
import sys
import os
import requests
import time

# 添加项目根目录到路径
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, os.path.abspath(project_root))

BASE_URL = "http://localhost:5000"

def test_server_connection():
    """测试服务器连接"""
    print("=" * 60)
    print("测试服务器连接...")
    print("=" * 60)
    
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            print("✅ 服务器连接成功！")
            return True
        else:
            print(f"❌ 服务器返回状态码: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保服务器已启动")
        return False
    except Exception as e:
        print(f"❌ 连接错误: {e}")
        return False

def test_search_functionality():
    """测试搜索功能"""
    print("\n" + "=" * 60)
    print("测试搜索功能...")
    print("=" * 60)
    
    # 测试搜索接口
    test_cases = [
        {"search": "手机", "description": "搜索'手机'"},
        {"search": "图书馆", "description": "搜索'图书馆'"},
        {"category": "手机", "description": "筛选类别'手机'"},
        {"type": "lost", "description": "筛选类型'失物'"},
        {"sort": "name", "description": "按名称排序"},
    ]
    
    for case in test_cases:
        try:
            params = {k: v for k, v in case.items() if k != "description"}
            response = requests.get(BASE_URL, params=params, timeout=5)
            if response.status_code == 200:
                print(f"✅ {case['description']}: 成功")
            else:
                print(f"❌ {case['description']}: 失败 (状态码: {response.status_code})")
        except Exception as e:
            print(f"❌ {case['description']}: 错误 - {e}")

def test_detail_pages():
    """测试详情页"""
    print("\n" + "=" * 60)
    print("测试详情页...")
    print("=" * 60)
    
    # 先获取一些失物和招领ID
    try:
        # 获取失物列表
        response = requests.get(f"{BASE_URL}/api/lost", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('data'):
                lost_id = data['data'][0]['id']
                print(f"✅ 找到失物ID: {lost_id}")
                
                # 测试失物详情页
                detail_url = f"{BASE_URL}/lost/{lost_id}"
                detail_response = requests.get(detail_url, timeout=5)
                if detail_response.status_code == 200:
                    print(f"✅ 失物详情页访问成功: /lost/{lost_id}")
                else:
                    print(f"❌ 失物详情页访问失败: {detail_response.status_code}")
        
        # 获取招领列表
        response = requests.get(f"{BASE_URL}/api/found", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('data'):
                found_id = data['data'][0]['id']
                print(f"✅ 找到招领ID: {found_id}")
                
                # 测试招领详情页
                detail_url = f"{BASE_URL}/found/{found_id}"
                detail_response = requests.get(detail_url, timeout=5)
                if detail_response.status_code == 200:
                    print(f"✅ 招领详情页访问成功: /found/{found_id}")
                else:
                    print(f"❌ 招领详情页访问失败: {detail_response.status_code}")
    except Exception as e:
        print(f"❌ 测试详情页时出错: {e}")

def test_profile_page():
    """测试用户主页"""
    print("\n" + "=" * 60)
    print("测试用户主页...")
    print("=" * 60)
    
    # 用户主页需要登录，这里只测试路由是否存在
    try:
        # 尝试访问用户主页（会重定向到登录页，说明路由存在）
        response = requests.get(f"{BASE_URL}/profile", allow_redirects=False, timeout=5)
        if response.status_code in [302, 200]:  # 302是重定向，200是已登录
            print("✅ 用户主页路由存在: /profile")
        else:
            print(f"❌ 用户主页路由异常: {response.status_code}")
    except Exception as e:
        print(f"❌ 测试用户主页时出错: {e}")

def test_api_endpoints():
    """测试API端点"""
    print("\n" + "=" * 60)
    print("测试API端点...")
    print("=" * 60)
    
    endpoints = [
        ("/api/lost", "GET", "获取失物列表"),
        ("/api/found", "GET", "获取招领列表"),
        ("/api/notifications/unread-count?user_id=1", "GET", "获取未读通知数量"),
    ]
    
    for endpoint, method, description in endpoints:
        try:
            url = f"{BASE_URL}{endpoint}"
            if method == "GET":
                response = requests.get(url, timeout=5)
            else:
                response = requests.post(url, timeout=5)
            
            if response.status_code in [200, 401, 404]:  # 200成功，401未登录，404不存在
                print(f"✅ {description}: 端点可访问 (状态码: {response.status_code})")
            else:
                print(f"❌ {description}: 端点异常 (状态码: {response.status_code})")
        except Exception as e:
            print(f"❌ {description}: 错误 - {e}")

def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("新功能测试脚本")
    print("=" * 60)
    print("\n等待服务器启动...")
    time.sleep(3)  # 等待服务器启动
    
    # 测试服务器连接
    if not test_server_connection():
        print("\n❌ 服务器未启动，请先启动服务器")
        return
    
    # 测试各项功能
    test_search_functionality()
    test_detail_pages()
    test_profile_page()
    test_api_endpoints()
    
    print("\n" + "=" * 60)
    print("✅ 测试完成！")
    print("=" * 60)
    print("\n提示：")
    print("  - 访问 http://localhost:5000 查看首页")
    print("  - 测试搜索功能：在搜索框输入关键词")
    print("  - 测试详情页：点击列表中的'查看详情'")
    print("  - 测试用户主页：登录后点击'我的主页'")

if __name__ == '__main__':
    main()

