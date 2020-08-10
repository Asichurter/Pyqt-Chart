'''
    @Author: TangZhiJie 唐郅杰 2017141463155

    This file contains a self-defined class ColorFrame
    to replace the traditional QFrame to correctly
    detect and emit the color changing event of frame.

    When color is set to change, slot functions are obliged
    to call the "emit" method to transfer the new RGB value
    to the processing slot functions.
'''

from PyQt5 import QtWidgets as widgets
from PyQt5 import QtCore as core

class ColorFrame(widgets.QFrame):
    ColorChanged = core.pyqtSignal(tuple)       # RGb value is a tuple

    def __init__(self):
        super(ColorFrame, self).__init__()

    def connect(self, func):
        self.ColorChanged.connect(func)

    def emit(self, rgb):
        self.ColorChanged.emit(rgb)

