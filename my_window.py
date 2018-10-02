from PyQt5.QtWidgets import QDesktopWidget, QWidget, QGridLayout
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtGui import QIcon, QColor, QPalette
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve

class my_window(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

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
