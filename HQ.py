

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtWidgets import QLabel, QGridLayout, QSizePolicy
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QRect
from launcher import tenx


class usb_window(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Missile HQ'
        self.a_geo = QDesktopWidget().availableGeometry()
        self.launcher = tenx()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.size_window()
        self.centre_window()
        self.show()
        self.initial_grid()
        self.add_svg()
        self.animate_svg()

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
        print (self.launcher.dev)
        if (self.launcher.dev is None):
            self.usb_image = QSvgWidget('./Images/usb-0.svg')
        else:
            self.usb_image = QSvgWidget('./Images/usb-1.svg')
        self.grid.addWidget(self.usb_image, 0, 1)
        # max_Width = self.usb_image.width()/4
        # max_Height =self.usb_image.height()/4
        # self.usb_image.setMaximumWidth(max_Width)
        # self.usb_image.setMaximumHeight(max_Height)

    def animate_svg(self):
        opac_eff = QGraphicsOpacityEffect()
        self.animation = QPropertyAnimation(opac_eff, b"opacity")
        self.usb_image.setGraphicsEffect(opac_eff)

        self.animation.setDuration(2000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.InQuad)
        self.animation.start()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = usb_window()
    sys.exit(app.exec_())
