# printer_app.spec
# PyInstaller build specification for Posterita Printer Utility
# --------------------------------------------------------------

# You can rebuild this with:
#   pyinstaller printer_app.spec
# or directly:
#   pyinstaller --onefile --noconsole --icon app.ico --add-data "config.properties;." main.py

import os
import sys
from pathlib import Path

block_cipher = None

# Get the current working directory
current_dir = Path(os.getcwd()).absolute()

# Path to the VERSIONINFO text file used by PyInstaller
version_file = str(current_dir / 'version_info.txt')

a = Analysis(
    ['main.py'],  # Use relative path since we're in the correct directory
    pathex=[str(current_dir)],
    binaries=[],
    datas=[
        ('config.properties', '.'),  # ✅ include your config file
        ('app.ico', '.'),           # ✅ include your app icon
        ('version_info.txt', '.'),  # ✅ include version info
    ],
    hiddenimports=[
        'win32print', 'win32api', 'win32ui',  # ensure pywin32 modules are included
    ],
    hookspath=[],
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
    name='PosteritaPrinterUtility',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                   # ✅ compress the output to reduce size
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,              # ✅ hide the console window (GUI only)
    icon='app.ico',            # ✅ your app icon
    version=version_file,      # embed version info from version_info.txt
    company_name='Posterita Ltd',
    product_name='Posterita Printer Utility',
    description='Posterita POS Printer Utility using pywebview',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PosteritaPrinterUtility'
)
