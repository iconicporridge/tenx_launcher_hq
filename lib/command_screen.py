from PyQt5.QtGui import QPixmap, QTransform, QIcon, QMovie
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QPushButton, QLabel

from .my_window import my_window


class command_screen(my_window):

    def __init__(self, parent, launcher):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setStyleSheet("""QPushButton {background-color: #DEDEDE;
                                            outline: none;
                                            border: none;
                                            border-radius: 4px
                                        }
                            QPushButton:hover {background-color: white;
                                                }
                            QPushButton:pressed {background-color: red}
        """)

        self.launcher = launcher
        icon_str = "./images/missile.png"
        window_str = "Missile Command"
        self.setWindowTitle(window_str)
        self.add_icon(icon_str)
        self.determine_geometry()
        self.arrow = QPixmap("./images/arrow.svg")
        self.initUI(2, 3)

    def add_widgets(self):
        button_height = self.height()/4
        self.button_size = QSize(int(button_height), int(button_height))
        self.create_grid()
        self.add_gif()
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

    def add_gif(self):
        self.movie = QMovie("./images/launcher.gif")
        self.launcher_gif = QLabel(parent=self)
        self.launcher_gif.setMovie(self.movie)
        self.grid.addWidget(self.launcher_gif, 2, 1, 3, 1)
        self.movie.start()

    def add_spacing(self):
        self.grid.setRowStretch(1, 1)
        self.grid.setRowStretch(5, 1)

    def add_left(self):
        self.left_button = QPushButton(parent=self)
        self.left_button.setIconSize(self.button_size)
        self.left_button.setIcon(self.arrow_icon(180))
        self.grid.addWidget(self.left_button, 3, 2)
        self.left_button.pressed.connect(self.left)
        self.left_button.released.connect(self.stop)

    def add_right(self):
        self.right_button = QPushButton(parent=self)
        self.right_button.setIconSize(self.button_size)
        arrow_icon = QIcon(self.arrow)
        self.right_button.setIcon(arrow_icon)
        self.grid.addWidget(self.right_button, 3, 4)
        self.right_button.pressed.connect(self.right)
        self.right_button.released.connect(self.stop)

    def add_up(self):
        self.up_button = QPushButton(parent=self)
        self.up_button.setIconSize(self.button_size)
        self.up_button.setIcon(self.arrow_icon(270))
        self.grid.addWidget(self.up_button, 2, 3)
        self.up_button.pressed.connect(self.up)
        self.up_button.released.connect(self.stop)

    def add_rightup(self):
        self.rightup_button = QPushButton(parent=self)
        self.rightup_button.setIconSize(self.button_size)
        self.rightup_button.setIcon(self.arrow_icon(315))
        self.grid.addWidget(self.rightup_button, 2, 4)
        self.rightup_button.pressed.connect(self.rightup)
        self.rightup_button.released.connect(self.stop)

    def add_leftup(self):
        self.leftup_button = QPushButton(parent=self)
        self.leftup_button.setIconSize(self.button_size)
        self.leftup_button.setIcon(self.arrow_icon(225))
        self.grid.addWidget(self.leftup_button, 2, 2)
        self.leftup_button.pressed.connect(self.leftup)
        self.leftup_button.released.connect(self.stop)

    def add_down(self):
        self.down_button = QPushButton(parent=self)
        self.down_button.setIconSize(self.button_size)
        self.down_button.setIcon(self.arrow_icon(90))
        self.grid.addWidget(self.down_button, 4, 3)
        self.down_button.pressed.connect(self.down)
        self.down_button.released.connect(self.stop)

    def add_leftdown(self):
        self.leftdown_button = QPushButton(parent=self)
        self.leftdown_button.setIconSize(self.button_size)
        self.leftdown_button.setIcon(self.arrow_icon(135))
        self.grid.addWidget(self.leftdown_button, 4, 2)
        self.leftdown_button.pressed.connect(self.leftdown)
        self.leftdown_button.released.connect(self.stop)

    def add_rightdown(self):
        self.rightdown_button = QPushButton(parent=self)
        self.rightdown_button.setIconSize(self.button_size)
        self.rightdown_button.setIcon(self.arrow_icon(45))
        self.grid.addWidget(self.rightdown_button, 4, 4)
        self.rightdown_button.pressed.connect(self.rightdown)
        self.rightdown_button.released.connect(self.stop)

    def add_fire(self):
        self.fire_button = QPushButton(parent=self)
        explosion_icon = QIcon("./images/explosion.svg")
        self.fire_button.setIcon(explosion_icon)
        self.fire_button.setIconSize(self.button_size)
        self.grid.addWidget(self.fire_button, 3, 3)
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
