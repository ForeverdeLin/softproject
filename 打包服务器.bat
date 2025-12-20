@echo off
chcp 65001 >nul
echo ========================================
echo 打包服务器为EXE文件
echo ========================================
echo.

cd /d %~dp0

REM 激活虚拟环境
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo 错误：未找到虚拟环境 .venv
    echo 请先创建虚拟环境：python -m venv .venv
    pause
    exit /b 1
)

REM 安装PyInstaller（如果还没安装）
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 正在安装PyInstaller...
    pip install pyinstaller
)

echo.
echo 开始打包...
echo.

REM 使用PyInstaller打包
pyinstaller --name="失物招领系统-服务器" ^
    --onefile ^
    --console ^
    --add-data "app;app" ^
    --hidden-import=flask ^
    --hidden-import=werkzeug ^
    --hidden-import=sqlalchemy ^
    --hidden-import=flask_cors ^
    --hidden-import=app.main ^
    --hidden-import=app.web ^
    --hidden-import=app.database ^
    --hidden-import=app.database.db_manager ^
    --hidden-import=app.database.models_db ^
    --hidden-import=app.auth ^
    --hidden-import=app.auth.auth_service ^
    --hidden-import=app.auth.session_manager ^
    --hidden-import=app.agent ^
    --hidden-import=app.agent.rule_agent ^
    --hidden-import=app.agent.matcher ^
    --hidden-import=app.agent.notification_agent ^
    --hidden-import=app.models ^
    --collect-all flask ^
    --collect-all werkzeug ^
    --collect-all sqlalchemy ^
    build_exe.py

if errorlevel 1 (
    echo.
    echo 打包失败！
    pause
    exit /b 1
)

echo.
echo ========================================
echo 打包完成！
echo ========================================
echo EXE文件位置: dist\失物招领系统-服务器.exe
echo.
echo 使用方法：
echo   1. 双击运行 dist\失物招领系统-服务器.exe
echo   2. 服务器将运行在 http://0.0.0.0:5000
echo   3. 客户端可以连接到服务器的IP地址
echo.
pause

