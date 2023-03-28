# Updater
## This is a simple Updater for various programs.
This updater will download and unpack the archive previously downloaded by your program and replace all files in the current directory with new ones, except for itself.

### Supported OS:
- Windows
- macOS

### To use it, you need to specify:
- url to archive with update (`--url https://example.com/example.zip`)
- archive name (`--archive_name example.zip`)

### For example, this code may contain your program:
```
import subprocess
args = ["./Updater.exe",
        "--url https://example.com/example.zip",
        "--archive_name example.zip"
        ]
subprocess.Popen(args)
```

#### If you want to ignore some files when updating, you can use the --ignore_files argument
```
--ignore_files file.txt file.txt
```

### To find out the Updater version, you can use this code in your program:
For Windows:
```
# For Windows
import win32api

path = r'Updater.exe'
info = win32api.GetFileVersionInfo(path, '\\')
ms = info['FileVersionMS']
ls = info['FileVersionLS']
app_version = f"{win32api.HIWORD(ms)}.{win32api.LOWORD(ms)}.{win32api.HIWORD(ls)}.{win32api.LOWORD(ls)}"
print(app_version)
```

On macOS, you can use this code:
```
# For macOS
import plistlib

path = 'Updater.app/Contents/info.plist'

with open(path, 'rb') as fp:
    pl = plistlib.load(fp)

app_version = pl.get("CFBundleShortVersionString")
print(app_version)
```