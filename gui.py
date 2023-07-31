from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 380, 540)
        self.setWindowTitle("Wallpaper")

        self.v_layout = QVBoxLayout(self)

        self.label = QLabel("Select a Wallpaper")
        self.label.setFont(QFont("Cantarell", 16))
        self.label.setAlignment(Qt.AlignCenter)

        self.scroll_box = QScrollArea()
        self.scroll_widget = QWidget()

        self.scroll_box.setWidget(self.scroll_widget)
        self.scroll_box.setWidgetResizable(True)

        self.image_list = QListWidget(self.scroll_widget)

        self.bottom_btns = QHBoxLayout()
        self.bottom_btns.setSpacing(2)

        self.set_btn = QPushButton("Set Wallpaper")
        self.browse_btn = QPushButton("Add")
        self.browse_btn.setMaximumWidth(70)

        self.bottom_btns.addWidget(self.set_btn)
        self.bottom_btns.addWidget(self.browse_btn)

        self.v_layout.addWidget(self.label)
        self.v_layout.addWidget(self.scroll_box)
        self.v_layout.addLayout(self.bottom_btns)

        self.setLayout(self.v_layout)