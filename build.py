# Tools for build
import PyInstaller.__main__
import pyinstaller_versionfile
from main import version
import platform
import shutil
import os

# Variables
app_name = "Updater"
app_description = "This is a simple Updater for Python programs."

# Removing dist
if os.path.exists('dist'):
    shutil.rmtree('dist')

if platform.system() == 'Windows':
    # Make version file for exe
    pyinstaller_versionfile.create_versionfile(
        output_file="build_configuration/version_file.txt",
        version=version,
        file_description=app_description,
        internal_name=app_name,
        original_filename=app_name + ".exe",
        product_name=app_name,
        translations=[1033, 1252, 1251]
    )

# Build application
PyInstaller.__main__.run([
    'main.spec'
])

# Make .dmg
if platform.system() == 'Darwin':
    import dmgbuild

    # build dmg
    dmgbuild.build_dmg(
        filename='dist/' + app_name + '.dmg',
        volume_name=app_name,
        settings={
            'files': ['dist/' + app_name + '.app'],
            'icon': 'icons/' + app_name + '.icns',
        }
    )
