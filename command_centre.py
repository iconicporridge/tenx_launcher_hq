import sys
import signal
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtWidgets import QLabel, QGridLayout, QSizePolicy
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QColor, QPalette, QIcon, QFont
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QThread, Qt, QRect
from launcher import tenx


# TODO closing behaviour (close both windows)
# TODO change way that other classes access launcher (through "parent")
# TODO thread or otherwise deal with the moving of rockets that requires a
#      sleep event

class monitor_thread(QThread):
# This thread checks if the state of the USB connection has
# changed. If it has changed, the USB_insert window changes
    signal = pyqtSignal()

    def __init__(self, launcher):
        super().__init__()
        self.launcher = launcher

    def run(self):

        self.state = self.launcher.check_connection()

        while True:
            self.new_state = self.launcher.check_connection()
            if (self.new_state == self.state):
                self.sleep(0.1)
            else:
                self.state = self.new_state
                self.signal.emit()
                self.sleep(0.1)

class boot_window_monitor(QThread):
# This thead checks to see if the launcher has been plugged
# in for some number of seconds. If so, the window changes.

        signal = pyqtSignal()

        def __init__(self, launcher):
            super().__init__()
            self.launcher = launcher

        def run(self):
            running = True
            while running:
                if (self.launcher.dev is not None):
                    self.launcher.tripped = False
                    self.sleep(1)
                    if (self.launcher.tripped == False):
                        self.signal.emit()
                        running = False
                    else:
                        self.sleep(0.1)
                else:
                    self.sleep(0.1)

class my_window(QWidget):

    def __init__(self):
        super().__init__()

    def initUI(self, w_factor, h_factor):
        self.size_window(w_factor, h_factor)
        self.centre_window()
        self.define_colors()
        self.color_window()
        self.add_widgets()

    def determine_geometry(self):
        self.geo = QDesktopWidget().availableGeometry()

    def add_icon(self, string):
        self.icon = QIcon()
        self.icon.addFile(string)
        self.setWindowIcon(self.icon)

    def define_colors(self):
        self.window_color = "#DEDEDE"
        self.rocket_red = "#C20024"
        self.grey = "#4D4D4D"

    def color_window(self):
        pal = QPalette()
        my_window_color = QColor()
        my_window_color.setNamedColor(self.window_color)
        pal.setColor(QPalette.Window, my_window_color)
        self.setPalette(pal)

    def size_window(self, w_factor, h_factor):
        self.width = self.geo.width()/w_factor
        self.height = self.geo.height()/h_factor
        self.resize(self.width, self.height)

    def centre_window(self):
        centre = self.geo.center()
        x = centre.x()
        y = centre.y()
        self.move(x-self.width/2, y-self.height/2)

    def create_grid(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

    def animate_svg(self, svg_image):
        svg_image.opac_eff = QGraphicsOpacityEffect()
        svg_image.setGraphicsEffect(svg_image.opac_eff)
        svg_image.animation = QPropertyAnimation(svg_image.opac_eff, b"opacity")
        svg_image.animation.setDuration(2000)
        svg_image.animation.setStartValue(0.1)
        svg_image.animation.setEndValue(1)
        svg_image.animation.setEasingCurve(QEasingCurve.OutCirc)
        svg_image.animation.start()

class command_centre(QWidget):

    def __init__(self):
        super().__init__()
        self.launcher = tenx()
        self.launcher.connect_launcher()
        self.boot_screen = boot_screen(self.launcher)
        self.command_screen = command_screen(self.launcher)
        self.screen = "boot"
        self.boot_screen.show()
        self.spawn_monitors()
        self.connection_monitor.start()
        self.boot_window_monitor.start()

    def usb_toggle(self):
        self.launcher.connect_launcher()
        self.launcher.tripped = True
        self.boot_screen.update_usb_image()
        self.boot_screen.update_boot_label()
        if (self.screen == "control"):
            self.change_window()

    def change_window(self):
        if (self.screen == "control"):
            self.screen = "boot"
            self.command_screen.hide()
            self.boot_screen.show()
            self.boot_window_monitor.start()
        else:
            self.screen = "control"
            self.boot_screen.hide()
            self.command_screen.show()

    def spawn_monitors(self):
        self.connection_monitor = monitor_thread(self.launcher)
        self.connection_monitor.signal.connect(self.usb_toggle)
        self.boot_window_monitor = boot_window_monitor(self.launcher)
        self.boot_window_monitor.signal.connect(self.change_window)


class boot_screen(my_window):

    def __init__(self, launcher):
        super().__init__()
        self.launcher = launcher
        icon_str = "./Images/missile.png"
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
        self.boot_label = QLabel()
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

        self.usb_image = QSvgWidget()
        self.usb_image.image0 = './Images/usb-0.svg'
        self.usb_image.image1 = './Images/usb-1.svg'
        self.usb_image.max_height = self.height/2
        self.grid.addWidget(self.usb_image, 1, 0, Qt.AlignHCenter)
        self.spacing_label = QLabel()
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
        self.usb_image.setFixedWidth(width)
        self.usb_image.setFixedHeight(height)
        self.animate_svg(self.usb_image)

    def update_boot_label(self):
        if (self.launcher.dev is None):
            self.boot_label.setText("Please insert your Tenx launcher")
        else:
            print("text should be welcome commander")
            self.boot_label.setText("Welcome Commander")

class command_screen(my_window):

        def __init__(self, launcher):
            super().__init__()
            self.launcher = launcher
            icon_str = "./Images/missile.png"
            window_str = "Missile Command"
            self.setWindowTitle(window_str)
            self.add_icon(icon_str)
            self.determine_geometry()
            self.initUI(1.5, 1.5)

        def add_widgets(self):
            self.create_grid()
            self.add_spacing()
            self.add_fire()
            self.add_down()
            self.add_up()
            # self.add_left()
            # self.add_right()

        def add_spacing(self):
            # self.top_label = QLabel()
            # self.bottom_label = QLabel()
            # self.grid.addWidget(self.top_label, 1, 1, Qt.AlignCenter)
            self.grid.setRowStretch(1, 1)
            self.grid.setRowStretch(5, 1)

        def add_up(self):
            self.up_button = QPushButton()
            self.up_button.setText("Up")
            self.grid.addWidget(self.up_button, 2, 1, Qt.AlignCenter)
            self.up_button.clicked.connect(lambda:self.launcher.move(self.launcher.up))


        def add_fire(self):
            self.fire_button = QPushButton()
            self.fire_button.setText("Fire")
            self.grid.addWidget(self.fire_button, 3, 1, Qt.AlignCenter)
            self.fire_button.clicked.connect(self.launcher.fire_launcher)

        def add_down(self):
            self.down_button = QPushButton()
            self.down_button.setText("Down")
            self.grid.addWidget(self.down_button, 4, 1, Qt.AlignCenter)
            self.down_button.clicked.connect(lambda:self.launcher.move(self.launcher.down))





        # def add_fire_button(self):
        #     self.fire_button = QPushButton()
        #     self.fire_button.setText("Fire")
        #     self.grid.addWidget(self.fire_button, 1, 1)
        #     self.fire_button.clicked.connect(self.launcher.fire_launcher)
        #
        # def add_fire_button(self):
        #     self.fire_button = QPushButton()
        #     self.fire_button.setText("Fire")
        #     self.grid.addWidget(self.fire_button, 1, 1)
        #     self.fire_button.clicked.connect(self.launcher.fire_launcher)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    myapp = command_centre()
    sys.exit(app.exec_())
