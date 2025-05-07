# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['general_ledger.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='General Ledger V3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico',
)

app = BUNDLE(
    exe,
    name='General Ledger V3.app',
    icon='app_icon.ico',
    bundle_identifier='com.generalledger.v3',
    info_plist={
        'CFBundleShortVersionString': '1.0.2',
        'CFBundleVersion': '1.0.2',
        'NSHighResolutionCapable': 'True',
        'LSBackgroundOnly': 'False',
        'CFBundleName': 'General Ledger V3',
        'CFBundleDisplayName': 'General Ledger V3',
        'CFBundleGetInfoString': 'General Ledger V3 Accounting Application',
        'CFBundleIdentifier': 'com.generalledger.v3',
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': '????',
        'LSMinimumSystemVersion': '10.13',
    },
) 