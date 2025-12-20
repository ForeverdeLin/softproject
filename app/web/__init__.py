"""Web interface module for campus lost-and-found system"""
from flask import Blueprint

# 创建Web蓝图
# 设置 static_url_path='/static' 使静态资源路径为 /static/ 而不是 /web/static/
web_bp = Blueprint('web', __name__, 
                   template_folder='templates',
                   static_folder='static',
                   static_url_path='/static')

# 导入路由（避免循环导入）
from . import routes

