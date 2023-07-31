from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import sys
import subprocess
import os

import gui


wallpapers = []

next_wallpaper = "" # global variable

def add_minimalistic_wallpapers():
    folder = "~/Pictures/minimalistic-wallpaper-collection/images"
    folder = os.path.expanduser(folder)

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)

        if os.path.isfile(file_path):
            print("Adding to wallpapers:", file_path)
            wallpapers.append(file_path)

def start_daemon() -> bool:
    try:
        subprocess.run(['swww', 'init'], check=True)
        print("starting swww")
    except subprocess.CalledProcessError as e:
        print("swww already running")
        return True
    
    return False

def main():
    start_daemon()

    print("getting minimalistic wallpaper collection (300+ wallpapers), this may take a while...")
    add_minimalistic_wallpapers()

    min_wallpaper_name = os.path.basename(wallpapers[0])
    min_wallpaper_name, _ = os.path.splitext(min_wallpaper_name)

    print(f"done! {len(wallpapers)} wallpapers added. example: {min_wallpaper_name}")

    if len(wallpapers) >= 1:
        next_wallpaper = wallpapers[0]

    app = QApplication([])
    window = gui.MainWindow()

    window.set_btn.clicked.connect(lambda: set_wallpaper())

    window.image_list.itemClicked.connect(lambda item: on_image_clicked(item, window.image_list))

    print(wallpapers)

    window.image_list.clear()

    for filename in wallpapers:
        add_thumbnail(window.image_list, wallpapers, filename)

    window.show()
    app.exec()

def add_thumbnail(image_list, image_filenames, filename):
    print(f"Loading image: {filename}")
    item = QListWidgetItem()
    label = QLabel()

    # Convert filename to absolute path using os.path.expanduser
    filename = os.path.expanduser(filename)

    # Check if the file exists before loading the pixmap
    if os.path.exists(filename):
        pixmap = QPixmap(filename).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        label.setFixedSize(100, 100)
        image_list.addItem(item)
        image_list.setItemWidget(item, label)
        item.setData(Qt.UserRole, filename)
        print(f"Image loaded: {filename}")
    else:
        print(f"Error: File not found - {filename}")


def on_image_clicked(item, image_list):
    global next_wallpaper

    selected_filename = item.data(Qt.UserRole)
    print("Selected image:", selected_filename)
    
    next_wallpaper = selected_filename # local variable

def set_wallpaper():
    # img_path = os.path.expanduser(next_wallpaper)
    print(next_wallpaper)
    args_list = ['swww', 'img', next_wallpaper, '--transition-type', 'grow', '--transition-duration', '2']
    print(args_list)
    subprocess.run(args_list)


if __name__ == "__main__":
    main()