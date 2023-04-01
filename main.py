from tkinter import ttk, messagebox
import tkinter as tk
import subprocess
import platform
import argparse
import requests
import zipfile
import shutil
import random
import debug
import sys
import os

# Version
version = '1.0.1.0'
is_debug = False

# Base path
if platform.system() == 'Darwin':
    if getattr(sys, 'frozen', False):
        root_path = os.path.abspath(sys.executable)
        for _ in range(4):
            root_path = root_path[:root_path.rfind('/')]
    else:
        root_path = os.path.dirname(os.path.abspath(__file__))
else:
    root_path = os.getcwd()


def remove_old_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename in ignore_files:
            continue
        elif os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


def extract_zip_file():
    progress_bar['value'] = 0
    zip_file = zipfile.ZipFile(update_file_path)
    files = zip_file.namelist()
    text.config(text="Updating... Please, wait.")
    for i, file in enumerate(files, start=1):
        zip_file.extract(file, path=root_path)
        progress_bar["value"] = i / len(files) * 100
        if platform.system() == 'Darwin':
            root.update_idletasks()
        else:
            root.update()
    zip_file.close()


def install_from_dmg():
    text.config(text="Installing updates...")
    progress_bar['value'] = 0
    root.update()
    mount_cmd = ['hdiutil', 'attach', update_file_path, '-nobrowse', '-noverify', '-noautoopen']
    mount_output = subprocess.check_output(mount_cmd, stderr=subprocess.STDOUT).decode('utf-8')
    mount_point = update_folder_name

    # Extract the mount point from the output
    for line in mount_output.split('\n'):
        if 'Volumes' in line:
            mount_point = line.split('\t')[-1]
            break
    root.update()

    # Copy all files from the mounted volume to the destination directory
    total_size = sum(os.path.getsize(os.path.join(current_dir, filename)) for current_dir, _, filenames in
                     os.walk(mount_point) for filename in filenames)
    copied_size = 0
    for current_dir, _, filenames in os.walk(mount_point):
        for filename in filenames:
            src_file = os.path.join(current_dir, filename)
            rel_path = os.path.relpath(src_file, mount_point)
            dst_file = os.path.join(root_path, rel_path)

            os.makedirs(os.path.dirname(dst_file), exist_ok=True)

            # Use shutil.copy2() for preserving file metadata
            shutil.copy2(src_file, dst_file)

            copied_size = copied_size + os.path.getsize(src_file)
            progress_bar["value"] = copied_size / total_size * 100
            if platform.system() == 'Darwin':
                root.update_idletasks()
            else:
                root.update()

    # Unmount the .dmg file
    subprocess.run(['hdiutil', 'detach', mount_point, '-force'])


def preparing_for_update():
    if platform.system() == 'Darwin':
        # Some "hack" to request access to the user storage on start
        os.listdir(root_path)
    # (Re-)creating Update folder
    if os.path.exists(update_folder_path):
        shutil.rmtree(update_folder_path)
    os.mkdir(update_folder_path)


def download_update_file():
    text.config(text="Downloading updates...")
    progress_bar['value'] = 0
    root.update()
    response = requests.get(url, stream=True, timeout=None)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024  # 1 Kb
    count_downloaded_size = 0
    with open(update_folder_path + '/' + archive_name, "wb") as file:
        for count, data in enumerate(response.iter_content(block_size), start=1):
            file.write(data)
            count_downloaded_size = count_downloaded_size + block_size
            if total_size > 0:
                progress_bar['value'] = count_downloaded_size / total_size * 100
                if platform.system() == 'Darwin':
                    root.update_idletasks()
                else:
                    root.update()
    text.config(text="The update has been downloaded")


def apply_update():
    text.config(text="Start of the update...")
    progress_bar['value'] = 0
    root.update()
    # Skip removing files if not compiled
    if getattr(sys, 'frozen', False):
        remove_old_files(root_path)
    if update_file_path[update_file_path.rfind(".") + 1:] == 'dmg':
        # Install from dmg
        install_from_dmg()
    else:
        # Extract zip
        extract_zip_file()


def finishing_the_update():
    if os.path.exists(update_folder_path):
        shutil.rmtree(update_folder_path)
    text.config(text="The update is complete.")
    if open_app is not None:
        if platform.system() == 'Darwin':
            open_command = ['open', '-a', root_path + '/' + open_app]
        else:
            open_command = ['./' + open_app]
        if is_debug:
            print(debug.i(), 'Starting ' + open_app + '...')
        messagebox.showinfo("Updater", "Update finished.\nThe program will be opened automatically.")
        subprocess.Popen(open_command)
    else:
        messagebox.showinfo("Updater", "Update finished.\nPlease restart the program.")
    sys.exit()


# Getting arguments
parser = argparse.ArgumentParser(description='This is a simple Updater for Python programs.')
parser.add_argument('--url', type=str, help='URL for downloading the archive with the update.')
parser.add_argument('--archive_name', type=str, help='Name of the archive with the update')
parser.add_argument('--ignore_files', metavar='file', type=str, nargs='+', help='File names that the program will '
                                                                                'ignore when updating.')
parser.add_argument('--open', type=str, help='The name of the file needed to open the application after the update. '
                                             'Note that the file can be located either in the directory where the '
                                             'Updater is located, or below.')
args = parser.parse_args()

# Variables
url = args.url
archive_name = args.archive_name
ignore_files = [] + args.ignore_files if args.ignore_files is not None else []
open_app = args.open

if None not in (args.url, args.archive_name):
    # Creating window
    root = tk.Tk()
    root.title("Updater")
    if platform.system() == 'Windows':
        root.iconbitmap(os.path.dirname(os.path.realpath(__file__)) + '/icons/' + 'Updater.ico')
    root.geometry('500x100')
    root.resizable(False, False)
    text = ttk.Label(text="Updating... Please, wait.")
    text.pack(side='top', anchor='nw', padx=50, pady=10)
    progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
    progress_bar.pack(side='top', pady=10)

    # "Update" folder name
    update_folder_name = 'Update-' + str(random.randint(1000000, 10000000))
    update_folder_path = root_path + '/' + update_folder_name
    ignore_files = ignore_files + [update_folder_name]

    # Path to update archive
    update_file_path = update_folder_path + '/' + archive_name

    # Current executable file name
    executable_file_name = os.path.basename(sys.executable)
    if platform.system() == 'Darwin':
        executable_file_name = executable_file_name + '.app'
    ignore_files = ignore_files + [executable_file_name]

    # Prepare
    preparing_for_update()

    # Download
    download_update_file()

    # Update
    apply_update()

    # Finish
    finishing_the_update()

    root.mainloop()
