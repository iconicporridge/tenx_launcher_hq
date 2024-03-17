from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtWidgets import QLabel
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt

from .my_window import my_window


class boot_screen(my_window):

    def __init__(self, parent, launcher):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.launcher = launcher
        icon_str = "./images/missile.png"
        window_str = "Missile Command"
        self.setWindowTitle(window_str)
        self.add_icon(icon_str)
        self.determine_geometry()
        self.initUI(2, 2)

    def add_widgets(self):
        self.create_grid()
        self.add_usb_image()
        self.add_boot_label()

    def add_boot_label(self):
        self.boot_label = QLabel(parent=self)
        font = QFont('Droid Sans', 16)
        font.setBold(True)
        self.boot_label.setFont(font)
        text_color = QColor()
        text_color.setNamedColor(self.grey)
        pal = QPalette()
        pal.setColor(QPalette.WindowText, text_color)
        self.boot_label.setPalette(pal)
        self.grid.addWidget(self.boot_label, 0, 0, Qt.AlignCenter)
        self.update_boot_label()

    def add_usb_image(self):

        self.usb_image = QSvgWidget(parent=self)
        self.usb_image.image0 = './images/usb-0.svg'
        self.usb_image.image1 = './images/usb-1.svg'
        self.usb_image.max_height = self.h/2
        self.grid.addWidget(self.usb_image, 1, 0, Qt.AlignHCenter)
        self.spacing_label = QLabel(parent=self)
        self.grid.addWidget(self.spacing_label, 2, 0, Qt.AlignCenter)
        self.update_usb_image()

    def update_usb_image(self):

        if (self.launcher.dev is None):
            self.usb_image.load(self.usb_image.image0)
            self.usb_image.aspect_ratio = 1.0
        else:
            self.usb_image.load(self.usb_image.image1)
            self.usb_image.aspect_ratio = 1.0

        height = self.usb_image.max_height
        width = height*self.usb_image.aspect_ratio
        self.usb_image.setFixedWidth(int(width))
        self.usb_image.setFixedHeight(int(height))
        self.animate_svg(self.usb_image)

    def update_boot_label(self):
        if (self.launcher.dev is None):
            self.boot_label.setText("Please insert your Tenx launcher")
        else:
            self.boot_label.setText("Welcome Commander")
