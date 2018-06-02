import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtWidgets import QLabel, QGridLayout, QSizePolicy
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtGui import QIcon, QColor, QPalette
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QThread
from launcher import tenx

class connect_thread(QThread):

    def __init__(self, launcher):
        super().__init__()
        self.launcher = launcher

    def run(self):
        while (self.launcher.dev is None):
            self.sleep(0.1)
            self.launcher.connect_to_launcher()

class monitor_thread(QThread):

    def __init__(self, launcher):
        super().__init__()
        self.launcher = launcher

    def run(self):
        while (self.launcher.dev is not None):
            self.sleep(0.1)
            self.launcher.connect_to_launcher()

class usb_window(QWidget):

    def __init__(self):
        super().__init__()
        self.launcher = tenx()
        self.launcher.connect_to_launcher()
        self.spawn_threads()
        self.initUI()

    def initUI(self):
        self.a_geo = QDesktopWidget().availableGeometry()
        self.setWindowTitle("Missile HQ")
        self.size_window()
        self.centre_window()
        self.define_colors()
        self.color_window()
        self.initial_grid()
        self.add_usb_image()
        self.show()
        #self.start_monitoring()
        self.launcher.send_cmd(self.launcher.fire)
        print("Missile Away")

    def spawn_threads(self):
        self.wait = connect_thread(self.launcher)
        self.monitor = monitor_thread(self.launcher)
        self.wait.finished.connect(self.usb_toggle)
        self.monitor.finished.connect(self.usb_toggle)

    def start_monitoring(self):
        if (self.launcher.dev is None):
            self.wait.start()
        else:
            self.monitor.start()

    def define_colors(self):
        self.window_color = "#DEDEDE"

    def color_window(self):
        self.pal = QPalette()
        my_window_color = QColor()
        my_window_color.setNamedColor(self.window_color)
        self.pal.setColor(QPalette.Window, my_window_color)
        self.setPalette(self.pal)

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

    def add_usb_image(self):

        self.usb_image = QSvgWidget()
        self.usb_image.image0 = './Images/usb-0.svg'
        self.usb_image.image1 = './Images/usb-1.svg'
        self.usb_image.max_height = self.height/3
        self.update_usb_image()
        self.grid.addWidget(self.usb_image, 0, 1)

    def animate_svg(self, svg_image):
        svg_image.opac_eff = QGraphicsOpacityEffect()
        svg_image.setGraphicsEffect(svg_image.opac_eff)

        svg_image.animation = QPropertyAnimation(svg_image.opac_eff, b"opacity")
        svg_image.animation.setDuration(2000)
        svg_image.animation.setStartValue(0.1)
        svg_image.animation.setEndValue(1)
        svg_image.animation.setEasingCurve(QEasingCurve.OutCirc)
        svg_image.animation.start()

    def update_usb_image(self):

        if (self.launcher.dev is None):
            self.usb_image.load(self.usb_image.image0)
            self.usb_image.aspect_ratio = 1.0
        else:
            self.usb_image.load(self.usb_image.image1)
            self.usb_image.aspect_ratio = 1.0

        max_height = self.usb_image.max_height
        max_width = max_height*self.usb_image.aspect_ratio
        self.usb_image.setMaximumWidth(max_width)
        self.usb_image.setMaximumHeight(max_height)
        min_width = max_width/4
        min_height = max_height/4
        self.usb_image.setMinimumWidth(min_width)
        self.usb_image.setMinimumHeight(min_height)

        self.animate_svg(self.usb_image)

    def usb_toggle(self):
        self.update_usb_image()
        self.start_monitoring()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = usb_window()
    sys.exit(app.exec_())
