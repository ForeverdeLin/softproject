"""打包成exe的启动脚本"""
import sys
import os
import traceback

# 在文件顶部直接导入（不在try块中），确保PyInstaller能检测到
# 这些导入必须在文件顶部，让PyInstaller在分析时就能看到
import flask
import werkzeug
import sqlalchemy
import flask_cors

# 导入app模块，确保PyInstaller能检测到所有子模块
try:
    import app
    import app.main
    import app.models
    import app.web
    import app.web.routes
    import app.database
    import app.database.db_manager
    import app.database.models_db
    import app.auth
    import app.auth.auth_service
    import app.auth.session_manager
    import app.agent
    import app.agent.rule_agent
    import app.agent.matcher
    import app.agent.notification_agent
except ImportError:
    # 如果导入失败，在运行时再处理
    pass

# 先设置错误处理，确保能看到错误
def handle_exception(exc_type, exc_value, exc_traceback):
    """全局异常处理"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    error_msg = "\n" + "=" * 50 + "\n"
    error_msg += "发生错误！\n"
    error_msg += "=" * 50 + "\n"
    error_msg += f"错误类型: {exc_type.__name__}\n"
    error_msg += f"错误信息: {exc_value}\n"
    error_msg += "\n详细错误：\n"
    error_msg += "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    error_msg += "=" * 50 + "\n"
    
    print(error_msg)
    
    # 保存错误信息到文件
    try:
        exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.getcwd()
        error_file = os.path.join(exe_dir, "error.log")
        with open(error_file, 'w', encoding='utf-8') as f:
            f.write(error_msg)
        print(f"\n错误信息已保存到: {error_file}")
    except:
        pass
    
    print("\n按回车键退出...")
    try:
        input()
    except:
        pass

sys.excepthook = handle_exception

# 处理打包后的路径问题
if getattr(sys, 'frozen', False):
    # 如果是打包后的exe
    base_path = sys._MEIPASS
    # 设置工作目录为exe所在目录
    exe_dir = os.path.dirname(sys.executable)
    os.chdir(exe_dir)
    # 添加base_path到Python路径
    sys.path.insert(0, base_path)
else:
    # 如果是开发环境
    base_path = os.path.dirname(os.path.abspath(__file__))

print("正在导入模块...")
print(f"Python路径: {sys.path[:3]}...")  # 只显示前3个路径

# 确保能导入app模块
try:
    print("导入Flask...")
    import flask
    import flask.blueprints
    import flask.templating
    import werkzeug
    import werkzeug.security
    import sqlalchemy
    import flask_cors
    print("Flask及相关模块导入成功")
    
    print("导入app模块...")
    from app.main import create_app
    from app.models import LostItem, FoundItem, MatchRecord, User
    from app.database import db_manager, models_db
    from app.auth import auth_service, session_manager
    from app.agent import rule_agent, matcher, notification_agent
    print("app模块导入成功")
except Exception as e:
    print(f"\n导入错误: {e}")
    print(f"错误类型: {type(e).__name__}")
    traceback.print_exc()
    print("\n按回车键退出...")
    input()
    sys.exit(1)

def open_browser():
    """延迟打开浏览器"""
    import time
    time.sleep(1.5)  # 等待服务器启动
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    try:
        print("创建Flask应用...")
        # 创建应用
        app = create_app()
        print("Flask应用创建成功")
        
        # 启动服务器（服务器版本：不自动打开浏览器，停留在命令行）
        print("=" * 60)
        print("校园失物招领系统 - 服务器")
        print("=" * 60)
        print("服务器地址: http://0.0.0.0:5000")
        print("本地访问: http://localhost:5000")
        print("局域网访问: http://你的IP:5000")
        print()
        print("服务器运行中...")
        print("按 Ctrl+C 停止服务器")
        print("=" * 60)
        print()
        
        # 服务器监听所有网络接口，允许局域网访问
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        # 这个异常应该被全局异常处理捕获，但以防万一
        print(f"\n运行时错误: {e}")
        traceback.print_exc()
        print("\n按回车键退出...")
        input()

