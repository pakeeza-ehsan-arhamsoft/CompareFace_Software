from PyQt5 import uic
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import images


class Start_Page4(QMainWindow):
    def __init__(self):
        super().__init__()

        self.window = uic.loadUi("UI_Designs/Page_4.ui", self)
        self.gif_img = self.findChild(QLabel, "label_2")

        # Display the GIF on the QLabel
        gif = QMovie("images/AIFace.gif")
        self.gif_img.setMovie(gif)
        gif.start()
