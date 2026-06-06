# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# ビルド実行時のカレントディレクトリ（build/）を取得
# PyInstaller実行時に --specpath を指定している場合も考慮
current_dir = Path(os.getcwd())
if current_dir.name != 'build':
    # もしプロジェクトルートで実行された場合は build ディレクトリを探す
    build_dir = current_dir / 'build'
else:
    build_dir = current_dir

project_root = build_dir.parent
src_path = project_root / 'src'

block_cipher = None

# 依存ライブラリの漏れを防ぐための設定
hidden_imports = [
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'PyQt6.QtNetwork',
    'httpx',
    'PIL',
    'PIL.ImageGrab',
    'psutil',
    'numpy',
    'fastapi',
    'uvicorn',
    'logging',
    'asyncio',
    'json',
]

# データファイルのパスを絶対パスで指定し、実行時のエラーを防止
datas = [
    (str(build_dir / 'models_config.json'), '.'),
    (str(project_root / 'README.txt'), '.'),
]

# アイコンファイルの存在確認
icon_file = str(build_dir / 'screenmind.ico')
if not os.path.exists(icon_file):
    icon_file = None

a = Analysis(
    [str(build_dir / 'screenmind_lite.py')],
    pathex=[str(src_path), str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ScreenMind',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,
)

# macOS 用の Bundle 設定
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='ScreenMind.app',
        icon=icon_file,
        bundle_identifier='com.manus.screenmind',
        info_plist={
            'NSHighResolutionCapable': 'True',
            'LSBackgroundOnly': 'False',
        },
    )
