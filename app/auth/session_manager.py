"""Session management for Flask"""
from functools import wraps
from flask import session, redirect, url_for, request
from typing import Optional
from ..database.db_manager import DatabaseManager
from ..database import models_db


def login_required(f):
    """登录检查装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('web.login'))
        return f(*args, **kwargs)
    return decorated_function


def get_current_user(db_manager: DatabaseManager) -> Optional[models_db.UserDB]:
    """获取当前登录用户"""
    if 'user_id' not in session:
        return None
    
    db_session = db_manager.get_session()
    try:
        user = db_manager.get_user_by_id(db_session, session['user_id'])
        return user
    finally:
        db_session.close()

