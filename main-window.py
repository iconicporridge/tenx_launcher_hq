import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QGridLayout, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtSvg import QSvgWidget


class USB_Window(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Missile HQ'
        self.a_geo = QDesktopWidget().availableGeometry()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.size_window()
        self.initial_grid()
        self.add_svg()
        self.show()

    def size_window(self):
        self.height = self.a_geo.height()/2
        self.width = self.a_geo.width()/2
        self.resize(self.width, self.height)

    def centre_window(self):
        centre = self.a_geo.center()
        x = centre.x()
        y = centre.y()
        self.move(x-self.width/2, y-self.height/2)

    def initial_grid(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)


    def add_svg(self):
        self.usb_image = QSvgWidget('./Images/usb-0.svg')
        self.grid.addWidget(self.usb_image, 0, 1)
        max_Width = self.usb_image.width()/4
        max_Height = self.usb_image.height()/4
        self.usb_image.setMaximumWidth(max_Width)
        self.usb_image.setMaximumHeight(max_Height)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = USB_Window()
    sys.exit(app.exec_())
