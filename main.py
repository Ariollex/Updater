from tkinter import ttk, messagebox
import tkinter as tk
import platform
import argparse
import requests
import zipfile
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
        if filename == update_folder_name or os.path.basename(file_path) == current_file_path:
            continue
        elif os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            remove_old_files(file_path)
            os.rmdir(file_path)


def preparing_for_update():
    if platform.system() == 'Darwin':
        # Some "hack" to request access to the user storage on start
        os.listdir(root_path)
    # (Re-)creating Update folder
    if os.path.exists(update_folder_path):
        remove_old_files(update_folder_path)
        os.rmdir(update_folder_path)
    os.mkdir(update_folder_path)


def download_zip_file():
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


def extract_zip_file():
    text.config(text="Start of the update...")
    progress_bar['value'] = 0
    root.update()
    if is_debug:
        print(debug.i(), "Skipping remove old files!")
    else:
        remove_old_files(root_path)
    zip_file = zipfile.ZipFile(zip_file_path)
    files = zip_file.namelist()
    text.config(text="Updating... Please, wait.")
    if is_debug:
        print(debug.i(), "Unpacking new files...")
    for i, file in enumerate(files, start=1):
        zip_file.extract(file, path=root_path)
        progress_bar["value"] = i / len(files) * 100
        if platform.system() == 'Darwin':
            root.update_idletasks()
        else:
            root.update()
    zip_file.close()
    if os.path.exists(update_folder_path):
        remove_old_files(update_folder_path)
        os.rmdir(update_folder_path)
    messagebox.showinfo("Updater", "Update finished.\nPlease restart the program.")
    sys.exit()


# Getting arguments
parser = argparse.ArgumentParser(description='This is a simple Updater for Python programs.')
parser.add_argument('--url', type=str, help='URL for downloading the archive with the update.')
parser.add_argument('--archive_name', type=str, help='Name of the archive with the update')
args = parser.parse_args()

# Variables
url = args.url
archive_name = args.archive_name

if None not in (args.url, args.archive_name):
    # Creating window
    root = tk.Tk()
    root.title("Updater")
    root.geometry('500x100')
    root.resizable(False, False)
    text = ttk.Label(text="Updating... Please, wait.")
    text.pack(side='top', anchor='nw', padx=50, pady=10)
    progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
    progress_bar.pack(side='top', pady=10)

    # "Update" folder name
    update_folder_name = 'Update-' + str(random.randint(1000000, 10000000))
    update_folder_path = root_path + '/' + update_folder_name

    # Path to update archive
    zip_file_path = update_folder_path + '/' + archive_name

    # Current exe path
    current_file_path = os.path.basename(sys.executable)
    if platform.system() == 'Darwin':
        current_file_path = current_file_path + '.app'

    # Prepare
    preparing_for_update()

    # Download
    download_zip_file()

    # Update
    extract_zip_file()

    root.mainloop()
