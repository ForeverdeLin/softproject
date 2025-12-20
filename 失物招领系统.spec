# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_all, collect_submodules

# 强制收集Flask及其所有依赖
flask_datas, flask_binaries, flask_hiddenimports = collect_all('flask')
werkzeug_datas, werkzeug_binaries, werkzeug_hiddenimports = collect_all('werkzeug')
sqlalchemy_datas, sqlalchemy_binaries, sqlalchemy_hiddenimports = collect_all('sqlalchemy')

# 合并数据文件
datas = [
    ('app/web/templates', 'app/web/templates'),
    ('app/web/static', 'app/web/static')
] + flask_datas + werkzeug_datas + sqlalchemy_datas

# 合并二进制文件
binaries = flask_binaries + werkzeug_binaries + sqlalchemy_binaries

# 合并隐藏导入
hiddenimports = (
    flask_hiddenimports + 
    werkzeug_hiddenimports + 
    sqlalchemy_hiddenimports + [
        'app',
        'app.main',
        'app.web',
        'app.web.routes',
        'app.database',
        'app.database.db',
        'app.database.db_manager',
        'app.database.models_db',
        'app.agent',
        'app.agent.rule_agent',
        'app.agent.matcher',
        'app.auth',
        'app.auth.auth_service',
        'app.auth.session_manager',
        'app.models',
    ]
)

a = Analysis(
    ['build_exe.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='失物招领系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
