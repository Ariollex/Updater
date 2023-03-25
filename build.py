# Tools for build
import PyInstaller.__main__
import pyinstaller_versionfile
from main import version
import shutil
import os

# Removing dist
if os.path.exists('dist'):
    shutil.rmtree('dist')

# Make version file
pyinstaller_versionfile.create_versionfile(
    output_file="version_file.txt",
    version=version,
    file_description="This is a simple Updater for Python programs.",
    internal_name="Updater",
    original_filename="Updater.exe",
    product_name="Updater",
    translations=[1033, 1252, 1251]
)

# Build app
PyInstaller.__main__.run([
    'main.spec'
])
