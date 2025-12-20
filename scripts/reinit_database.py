"""
重新初始化数据库脚本
⚠️ 警告：此操作会删除现有数据库并重新创建，所有数据将丢失！
"""
import os
import sys

# 添加项目根目录到路径
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, os.path.abspath(project_root))

from app.database.db import DB_PATH, init_db
from app.database.db_manager import DatabaseManager

def reinit_database():
    """重新初始化数据库"""
    print("=" * 50)
    print("数据库重新初始化工具")
    print("=" * 50)
    
    # 检查数据库文件是否存在
    if os.path.exists(DB_PATH):
        print(f"\n⚠️  发现现有数据库文件: {DB_PATH}")
        response = input("是否删除现有数据库并重新创建？(yes/no): ")
        
        if response.lower() not in ['yes', 'y']:
            print("❌ 操作已取消")
            return
        
        try:
            # 删除现有数据库
            os.remove(DB_PATH)
            print(f"✅ 已删除旧数据库文件")
        except Exception as e:
            print(f"❌ 删除数据库文件失败: {e}")
            return
    else:
        print(f"\n📝 未找到现有数据库文件，将创建新数据库")
    
    # 重新初始化数据库
    print("\n正在初始化数据库...")
    try:
        init_db()
        print("✅ 数据库初始化成功！")
        print(f"\n数据库位置: {DB_PATH}")
        print("\n已创建的表:")
        print("  - users (用户表)")
        print("  - lost_items (失物表)")
        print("  - found_items (招领表)")
        print("  - match_records (匹配记录表)")
        print("  - notifications (通知表) ✨ 新增")
        
        # 测试数据库连接
        print("\n正在测试数据库连接...")
        db_manager = DatabaseManager()
        session = db_manager.get_session()
        try:
            from app.database import models_db
            # 检查表是否存在
            from sqlalchemy import inspect
            inspector = inspect(session.bind)
            tables = inspector.get_table_names()
            print(f"✅ 数据库连接正常，共 {len(tables)} 个表")
        finally:
            session.close()
            
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n" + "=" * 50)
    print("✅ 数据库重新初始化完成！")
    print("=" * 50)
    print("\n提示：")
    print("  - 现在可以运行程序了: python -m app.main")
    print("  - 或运行测试脚本: python scripts/test_db_init.py")

if __name__ == '__main__':
    reinit_database()

