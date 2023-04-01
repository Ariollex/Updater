# -*- mode: python ; coding: utf-8 -*-
from main import version
import platform

#
# Parameters
#
if platform.system() == 'Windows':
    onefile = True
else:
    onefile = False
block_cipher = None


#
# Main spec file elements
#
a = Analysis(
        ['main.py'],
        pathex=[],
        binaries=[],
        datas=[('icons/Updater.ico', 'icons/.')],
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
        a.binaries if onefile else [],
        a.zipfiles if onefile else [],
        a.datas if onefile else [],
        exclude_binaries=not onefile,
        name='Updater',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon='icons/Updater.ico',
        version='version_file.txt',
    )
bundle_obj = exe

if not onefile:
    coll = COLLECT(
            exe,
            a.binaries,
            a.zipfiles,
            a.datas,
            strip=False,
            upx=True,
            upx_exclude=[],
            name='Updater',
        )
    bundle_obj = coll

app = BUNDLE(bundle_obj,
        name='Updater.app',
        icon='icons/Updater.icns',
        bundle_identifier="app.ariollex.updater",
        info_plist={
            'CFBundleShortVersionString': version,
        }
    )