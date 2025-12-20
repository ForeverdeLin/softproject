"""测试数据库初始化"""
from app.database.db import init_db
from app.database.db_manager import DatabaseManager
from app.models import User
from app.auth.auth_service import AuthService

print("开始初始化数据库...")
try:
    # 初始化数据库
    init_db()
    print("✅ 数据库初始化成功")
    
    # 测试创建用户
    db_manager = DatabaseManager()
    auth_service = AuthService(db_manager)
    session = db_manager.get_session()
    
    try:
        success, error_msg, user = auth_service.register_user(
            session, 
            student_id="2021001",
            name="测试用户",
            password="123456",
            email="test@example.com",
            phone="13800138000"
        )
        
        if success:
            print(f"✅ 用户创建成功: {user.name} (ID: {user.id})")
        else:
            print(f"❌ 用户创建失败: {error_msg}")
    finally:
        session.close()
        
except Exception as e:
    print(f"❌ 错误: {str(e)}")
    import traceback
    traceback.print_exc()

