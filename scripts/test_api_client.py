"""
测试API客户端 - 用于测试服务器数据共享功能
"""
import requests
import json
from datetime import datetime

# 服务器地址（根据实际情况修改）
BASE_URL = "http://localhost:5000"


def test_get_all_lost():
    """测试获取所有失物列表"""
    print("\n=== 测试：获取所有失物列表 ===")
    try:
        response = requests.get(f"{BASE_URL}/api/lost")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ 成功获取 {data.get('count', 0)} 条失物信息")
                items = data.get('data', [])
                for i, item in enumerate(items[:5], 1):  # 只显示前5条
                    print(f"  {i}. {item['item_name']} - {item['lost_location']} ({item['category']})")
                if len(items) > 5:
                    print(f"  ... 还有 {len(items) - 5} 条")
                return True
            else:
                print(f"❌ 失败: {data.get('error', '未知错误')}")
        else:
            print(f"❌ HTTP错误: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    return False


def test_get_all_found():
    """测试获取所有招领列表"""
    print("\n=== 测试：获取所有招领列表 ===")
    try:
        response = requests.get(f"{BASE_URL}/api/found")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ 成功获取 {data.get('count', 0)} 条招领信息")
                items = data.get('data', [])
                for i, item in enumerate(items[:5], 1):  # 只显示前5条
                    print(f"  {i}. {item['item_name']} - {item['found_location']} ({item['category']})")
                if len(items) > 5:
                    print(f"  ... 还有 {len(items) - 5} 条")
                return True
            else:
                print(f"❌ 失败: {data.get('error', '未知错误')}")
        else:
            print(f"❌ HTTP错误: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    return False


def test_get_lost_by_id(lost_id=1):
    """测试获取单个失物信息"""
    print(f"\n=== 测试：获取失物ID={lost_id} ===")
    try:
        response = requests.get(f"{BASE_URL}/api/lost/{lost_id}")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                item = data.get('data', {})
                print(f"✅ 成功获取失物信息:")
                print(f"  名称: {item.get('item_name')}")
                print(f"  类别: {item.get('category')}")
                print(f"  地点: {item.get('lost_location')}")
                print(f"  时间: {item.get('lost_time')}")
                return True
            else:
                print(f"❌ 失败: {data.get('error', '未知错误')}")
        elif response.status_code == 404:
            print(f"⚠️  失物ID={lost_id} 不存在")
        else:
            print(f"❌ HTTP错误: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    return False


def test_get_found_by_id(found_id=1):
    """测试获取单个招领信息"""
    print(f"\n=== 测试：获取招领ID={found_id} ===")
    try:
        response = requests.get(f"{BASE_URL}/api/found/{found_id}")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                item = data.get('data', {})
                print(f"✅ 成功获取招领信息:")
                print(f"  名称: {item.get('item_name')}")
                print(f"  类别: {item.get('category')}")
                print(f"  地点: {item.get('found_location')}")
                print(f"  时间: {item.get('found_time')}")
                return True
            else:
                print(f"❌ 失败: {data.get('error', '未知错误')}")
        elif response.status_code == 404:
            print(f"⚠️  招领ID={found_id} 不存在")
        else:
            print(f"❌ HTTP错误: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    return False


def test_include_resolved():
    """测试包含已解决的数据"""
    print("\n=== 测试：获取包含已解决的数据 ===")
    try:
        # 测试失物
        response = requests.get(f"{BASE_URL}/api/lost?include_resolved=true")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ 失物总数（含已解决）: {data.get('count', 0)}")
        
        # 测试招领
        response = requests.get(f"{BASE_URL}/api/found?include_resolved=true")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ 招领总数（含已解决）: {data.get('count', 0)}")
        return True
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    return False


def main():
    """运行所有测试"""
    print("=" * 50)
    print("API客户端测试工具")
    print("=" * 50)
    print(f"服务器地址: {BASE_URL}")
    print("\n提示: 请确保服务器已启动 (python -m app.main)")
    
    # 测试服务器连接
    try:
        response = requests.get(f"{BASE_URL}/api/lost", timeout=3)
        print("✅ 服务器连接正常\n")
    except Exception as e:
        print(f"❌ 无法连接到服务器: {e}")
        print("\n请检查:")
        print("1. 服务器是否已启动? (python -m app.main)")
        print("2. 服务器地址是否正确? (当前: {BASE_URL})")
        return
    
    # 运行测试
    results = []
    results.append(("获取所有失物", test_get_all_lost()))
    results.append(("获取所有招领", test_get_all_found()))
    results.append(("获取单个失物", test_get_lost_by_id(1)))
    results.append(("获取单个招领", test_get_found_by_id(1)))
    results.append(("包含已解决数据", test_include_resolved()))
    
    # 汇总结果
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    print("=" * 50)
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
    
    success_count = sum(1 for _, result in results if result)
    print(f"\n总计: {success_count}/{len(results)} 测试通过")


if __name__ == "__main__":
    main()

