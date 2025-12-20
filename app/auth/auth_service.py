"""Authentication service for user registration and login"""
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from ..database.db_manager import DatabaseManager
from ..database import models_db
from ..models import User


class AuthService:
    """用户认证服务"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def register_user(self, session: Session, student_id: str, name: str, 
                     password: str, email: Optional[str] = None, 
                     phone: Optional[str] = None) -> Tuple[bool, Optional[str], Optional[models_db.UserDB]]:
        """
        用户注册
        返回: (是否成功, 错误信息, 用户对象)
        """
        # 检查学号是否已存在
        existing_user = self.db_manager.get_user_by_student_id(session, student_id)
        if existing_user:
            return False, "学号已注册", None
        
        # 验证输入
        if not student_id or not name or not password:
            return False, "学号、姓名和密码不能为空", None
        
        if len(password) < 6:
            return False, "密码长度至少6位", None
        
        # 创建用户对象
        user = User(
            user_id=None,
            student_id=student_id,
            name=name,
            email=email,
            phone=phone
        )
        
        # 加密密码
        password_hash = generate_password_hash(password)
        
        # 保存到数据库
        try:
            db_user = self.db_manager.create_user(session, user, password_hash)
            return True, None, db_user
        except Exception as e:
            return False, f"注册失败: {str(e)}", None
    
    def login_user(self, session: Session, student_id: str, password: str) -> Tuple[bool, Optional[str], Optional[models_db.UserDB]]:
        """
        用户登录
        返回: (是否成功, 错误信息, 用户对象)
        """
        # 查找用户
        user = self.db_manager.get_user_by_student_id(session, student_id)
        if not user:
            return False, "学号或密码错误", None
        
        # 验证密码
        if not check_password_hash(user.password_hash, password):
            return False, "学号或密码错误", None
        
        return True, None, user

