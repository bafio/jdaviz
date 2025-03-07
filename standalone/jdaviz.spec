# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path
import os

from PyInstaller.building.build_main import Analysis
from PyInstaller.building.api import COLLECT, EXE, PYZ
from PyInstaller.building.osx import BUNDLE

import jdaviz
from jdaviz.configs import Specviz, Specviz2d, Cubeviz, Mosviz, Imviz
codesign_identity = os.environ.get("DEVELOPER_ID_APPLICATION")

# this copies over the nbextensions enabling json and the js assets
# for all the widgets
datas = [
    (Path(sys.prefix) / "share" / "jupyter", "./share/jupyter"),
    (Path(sys.prefix) / "etc" / "jupyter", "./etc/jupyter"),
]

block_cipher = None


a = Analysis(
    ["jdaviz-cli-entrypoint.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=["rich.logging"],
    hookspath=["hooks"],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    # executable name: dist/jdaviz/jdaviz-cli
    # note: cannot be called jdaviz, because there is a directory called jdaviz
    name="jdaviz-cli",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=codesign_identity,
    entitlements_file="entitlements.plist",
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    # directory name: dist/jdaviz
    name="jdaviz",
)
app = BUNDLE(
    exe,
    coll,
    name="jdaviz.app",
    icon=None,
    entitlements_file="entitlements.plist",
    bundle_identifier="edu.stsci.jdaviz",
    version=jdaviz.__version__,
)
