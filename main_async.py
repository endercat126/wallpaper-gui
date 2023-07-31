from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QThreadPool, QRunnable, pyqtSignal, QObject
import sys
import subprocess
import os

import gui

wallpapers = []
next_wallpaper = ""  # global variable

class ImageLoaderSignals(QObject):
    imageLoaded = pyqtSignal(str)

class ImageLoader(QRunnable):
    def __init__(self, image_filenames):
        super().__init__()
        self.image_filenames = image_filenames
        self.signals = ImageLoaderSignals()

    def run(self):
        for filename in self.image_filenames:
            self.signals.imageLoaded.emit(filename)

class ImageGridWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.image_list = QVBoxLayout()
        self.image_list.setAlignment(Qt.AlignTop)
        self.setLayout(self.image_list)

    def add_thumbnail(self, filename):
        item = QListWidgetItem()
        label = QLabel()

        # Convert filename to absolute path using os.path.expanduser
        filename = os.path.expanduser(filename)

        # Check if the file exists before loading the pixmap
        if os.path.exists(filename):
            pixmap = QPixmap(filename).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(pixmap)
            label.setFixedSize(100, 100)
            self.image_list.addWidget(label)
            item.setData(Qt.UserRole, filename)
        else:
            print(f"Error: File not found - {filename}")

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
    global next_wallpaper  # Declare next_wallpaper as global in the main function
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

    window.set_btn.clicked.connect(set_wallpaper)  # Connect directly to set_wallpaper function

    window.image_list_widget = ImageGridWidget()
    window.scroll_box.setWidget(window.image_list_widget)

    print(wallpapers)

    # Create and start the image loader thread
    image_loader = ImageLoader(wallpapers)
    image_loader.signals.imageLoaded.connect(window.image_list_widget.add_thumbnail)

    thread_pool = QThreadPool.globalInstance()
    thread_pool.setMaxThreadCount(10)
    thread_pool.start(image_loader)

    window.show()
    app.exec()

def on_image_clicked(item, image_list):
    global next_wallpaper  # Declare next_wallpaper as global in the function
    selected_filename = item.data(Qt.UserRole)
    print("Selected image:", selected_filename)

    next_wallpaper = selected_filename

def set_wallpaper():
    global next_wallpaper  # Declare next_wallpaper as global in the function
    print(next_wallpaper)
    args_list = ['swww', 'img', next_wallpaper, '--transition-type', 'grow', '--transition-duration', '2']
    print(args_list)
    subprocess.run(args_list)

if __name__ == "__main__":
    main()
