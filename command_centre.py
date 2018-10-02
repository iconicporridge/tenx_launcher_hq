import sys
import signal
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtWidgets import QLabel, QGridLayout, QSizePolicy, QMessageBox
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QColor, QPalette, QIcon, QFont
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QThread, Qt, QRect
from launcher import tenx
from my_window import my_window

# TODO themeing, picture and about
# TODO if it's possible to implement a continous turn

class connection_thread(QThread):
# This thread checks if the state of the USB connection has
# changed. If it has changed, the USB_insert window changes
    signal = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.launcher = self.parent().launcher

    def run(self):
        self.state = self.launcher.check_connection()

        while self.parent().connection_thread_running:
            self.new_state = self.launcher.check_connection()
            if (self.new_state == self.state):
                self.sleep(0.1)
            else:
                self.state = self.new_state
                self.signal.emit()
                self.sleep(0.1)

class change_window_thread(QThread):
# This thead checks to see if the launcher has been plugged
# in for some number of seconds. If so, the window changes.
        signal = pyqtSignal()

        def __init__(self, parent):
            super().__init__(parent)
            self.launcher = self.parent().launcher

        def run(self):
            self.parent().change_window_thread_runnning = True
            while self.parent().change_window_thread_runnning:
                if (self.launcher.dev is not None):
                    self.launcher.tripped = False
                    self.sleep(1)
                    if (self.launcher.tripped == False):
                        self.signal.emit()
                        self.parent().change_window_thread_runnning = False
                    else:
                        self.sleep(0.1)
                else:
                    self.sleep(0.1)


class command_centre(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.launcher = tenx()
        self.launcher.connect_launcher()
        self.boot_screen = boot_screen(None, self.launcher)
        self.command_screen = command_screen(None, self.launcher)
        self.boot_screen.destroyed.connect(self.close)
        self.command_screen.destroyed.connect(self.close)
        self.screen = "boot"
        self.boot_screen.show()
        self.spawn_monitors()

    def close(self):
        try:
            self.change_window_thread_runnning = False
            self.connection_thread_running = False
            self.connection_thread.wait()
            self.change_window_thread.wait()
            self.boot_screen.close()
            self.command_screen.close()
        except Exception as e:
            pass

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
            self.change_window_thread.start()
        else:
            self.screen = "control"
            self.boot_screen.hide()
            self.command_screen.show()

    def spawn_monitors(self):
        self.connection_thread_running = True
        self.change_window_thread_runnning = True
        self.connection_thread = connection_thread(parent=self)
        self.connection_thread.signal.connect(self.usb_toggle)
        self.change_window_thread = change_window_thread(parent=self)
        self.change_window_thread.signal.connect(self.change_window)
        self.connection_thread.start()
        self.change_window_thread.start()


class boot_screen(my_window):

    def __init__(self, parent, launcher):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
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
        self.usb_image.image0 = './Images/usb-0.svg'
        self.usb_image.image1 = './Images/usb-1.svg'
        self.usb_image.max_height = self.height/2
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
        self.usb_image.setFixedWidth(width)
        self.usb_image.setFixedHeight(height)
        self.animate_svg(self.usb_image)

    def update_boot_label(self):
        if (self.launcher.dev is None):
            self.boot_label.setText("Please insert your Tenx launcher")
        else:
            self.boot_label.setText("Welcome Commander")

class command_screen(my_window):

        def __init__(self, parent, launcher):
            super().__init__(parent)
            self.setAttribute(Qt.WA_DeleteOnClose)
            self.setStyleSheet("QPushButton {background-color: red}")
            self.launcher = launcher
            icon_str = "./Images/missile.png"
            window_str = "Missile Command"
            self.setWindowTitle(window_str)
            self.add_icon(icon_str)
            self.determine_geometry()
            self.arrow = QPixmap("./Images/arrow.svg")
            self.initUI(1.5, 1.5)

        def add_widgets(self):
            self.create_grid()
            self.add_spacing()
            self.add_fire()
            self.add_down()
            self.add_up()
            self.add_left()
            self.add_right()
            self.add_leftup()
            self.add_rightup()
            self.add_leftdown()
            self.add_rightdown()

        def add_spacing(self):
            self.grid.setRowStretch(1, 1)
            self.grid.setRowStretch(5, 1)

        def add_left(self):
            self.left_button = QPushButton(parent=self)
            self.left_button.setIcon(self.arrow_icon(180))
            self.grid.addWidget(self.left_button, 3, 2, Qt.AlignCenter)
            self.left_button.pressed.connect(self.left)
            self.left_button.released.connect(self.stop)

        def add_right(self):
            self.right_button = QPushButton(parent=self)
            arrow_icon = QIcon(self.arrow)
            self.right_button.setIcon(arrow_icon)
            self.grid.addWidget(self.right_button, 3, 4, Qt.AlignCenter)
            self.right_button.pressed.connect(self.right)
            self.right_button.released.connect(self.stop)

        def add_up(self):
            self.up_button = QPushButton(parent=self)
            self.up_button.setIcon(self.arrow_icon(270))
            self.grid.addWidget(self.up_button, 2, 3, Qt.AlignCenter)
            self.up_button.pressed.connect(self.up)
            self.up_button.released.connect(self.stop)

        def add_rightup(self):
            self.rightup_button = QPushButton(parent=self)
            self.rightup_button.setIcon(self.arrow_icon(315))
            self.grid.addWidget(self.rightup_button, 2, 4, Qt.AlignCenter)
            self.rightup_button.pressed.connect(self.rightup)
            self.rightup_button.released.connect(self.stop)

        def add_leftup(self):
            self.leftup_button = QPushButton(parent=self)
            self.leftup_button.setIcon(self.arrow_icon(225))
            self.grid.addWidget(self.leftup_button, 2, 2, Qt.AlignCenter)
            self.leftup_button.pressed.connect(self.leftup)
            self.leftup_button.released.connect(self.stop)

        def add_down(self):
            self.down_button = QPushButton(parent=self)
            self.down_button.setIcon(self.arrow_icon(90))
            self.grid.addWidget(self.down_button, 4, 3, Qt.AlignCenter)
            self.down_button.pressed.connect(self.down)
            self.down_button.released.connect(self.stop)

        def add_leftdown(self):
            self.leftdown_button = QPushButton(parent=self)
            self.leftdown_button.setIcon(self.arrow_icon(135))
            self.grid.addWidget(self.leftdown_button, 4, 2, Qt.AlignCenter)
            self.leftdown_button.pressed.connect(self.leftdown)
            self.leftdown_button.released.connect(self.stop)

        def add_rightdown(self):
            self.rightdown_button = QPushButton(parent=self)
            self.rightdown_button.setIcon(self.arrow_icon(45))
            self.grid.addWidget(self.rightdown_button, 4, 4, Qt.AlignCenter)
            self.rightdown_button.pressed.connect(self.rightdown)
            self.rightdown_button.released.connect(self.stop)

        def add_fire(self):
            self.fire_button = QPushButton(parent=self)
            self.fire_button.setText("Fire")
            self.grid.addWidget(self.fire_button, 3, 3, Qt.AlignCenter)
            self.fire_button.clicked.connect(self.launcher.fire_launcher)

        def arrow_icon(self, degrees):
            transform = QTransform()
            transform.rotate(degrees)
            arrow = self.arrow.transformed(transform)
            icon = QIcon(arrow)
            return icon

        def down(self):
            self.launcher.move(self.launcher.down)

        def up(self):
            self.launcher.move(self.launcher.up)

        def left(self):
            self.launcher.move(self.launcher.left)

        def right(self):
            self.launcher.move(self.launcher.right)

        def rightup(self):
            self.launcher.move(self.launcher.rightup)

        def leftup(self):
            self.launcher.move(self.launcher.leftup)

        def leftdown(self):
            self.launcher.move(self.launcher.leftdown)

        def rightdown(self):
            self.launcher.move(self.launcher.rightdown)

        def stop(self):
            self.launcher.move(self.launcher.stop)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    myapp = command_centre()
    sys.exit(app.exec())
