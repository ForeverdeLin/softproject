"""
测试弹窗功能
"""
import sys
import os
import requests

BASE_URL = "http://localhost:5000"

def test_image_file():
    """测试图片文件是否存在"""
    print("=" * 60)
    print("测试图片文件...")
    print("=" * 60)
    
    image_path = "app/web/static/images/advertisement.jpg"
    if os.path.exists(image_path):
        file_size = os.path.getsize(image_path)
        print(f"✅ 图片文件存在: {image_path}")
        print(f"   文件大小: {file_size} 字节")
        return True
    else:
        print(f"❌ 图片文件不存在: {image_path}")
        return False

def test_static_url():
    """测试静态资源URL"""
    print("\n" + "=" * 60)
    print("测试静态资源URL...")
    print("=" * 60)
    
    try:
        # 测试图片URL
        image_url = f"{BASE_URL}/static/images/advertisement.jpg"
        response = requests.get(image_url, timeout=5)
        if response.status_code == 200:
            print(f"✅ 图片URL可访问: {image_url}")
            print(f"   内容类型: {response.headers.get('Content-Type', 'unknown')}")
            return True
        else:
            print(f"❌ 图片URL返回状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法访问图片URL: {e}")
        return False

def test_homepage():
    """测试首页是否包含弹窗代码"""
    print("\n" + "=" * 60)
    print("测试首页HTML...")
    print("=" * 60)
    
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            html = response.text
            if 'imageModal' in html:
                print("✅ 首页包含 imageModal")
            else:
                print("❌ 首页不包含 imageModal")
            
            if 'adModal' in html:
                print("✅ 首页包含 adModal")
            else:
                print("❌ 首页不包含 adModal")
            
            if 'advertisement.jpg' in html:
                print("✅ 首页包含图片路径")
            else:
                print("❌ 首页不包含图片路径")
            
            return True
        else:
            print(f"❌ 首页返回状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法访问首页: {e}")
        return False

def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("弹窗功能测试")
    print("=" * 60)
    
    # 测试图片文件
    test_image_file()
    
    # 测试静态资源
    test_static_url()
    
    # 测试首页
    test_homepage()
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
    print("\n提示：")
    print("  - 如果图片文件存在但URL无法访问，检查Flask静态资源配置")
    print("  - 如果HTML不包含弹窗代码，检查模板是否正确渲染")
    print("  - 打开浏览器控制台（F12）查看是否有JavaScript错误")

if __name__ == '__main__':
    main()

