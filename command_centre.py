# the .py file for the main loop and its threads
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import pyqtSignal, QThread

import sys
import signal

from launcher import tenx
from my_window import my_window
from boot_screen import boot_screen
from command_screen import command_screen

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

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    myapp = command_centre()
    sys.exit(app.exec())
