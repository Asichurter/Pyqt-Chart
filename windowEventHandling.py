'''
    @Author: TangZhiJie 唐郅杰 2017141463155

    Handling events of main window, including all GUI
    logic processing.

    This module is loose-coupled with main window so
    that apis are functionally general. Closure is widely
    used to encapsulate the extern widget as the parameter
    when slot function is called without widget provided.

    Any modifications will not be written back to configs.
'''

from PyQt5 import QtWidgets as widgets
from PyQt5 import QtCore as core
from PyQt5 import QtGui as gui
import pyqtgraph as pg


def resize_plots_adaptively(plot_widgets, plot_total_cnt, plot_cnt, plot_w, plot_h):
    '''
    Adjust the size of plot widget to adapt the change.

    Widget and size are offered so the modification can be done independently
    in this method.
    :param plot_widgets: all widgets
    :param plot_total_cnt: total count of plots
    :param plot_cnt: count of visible plots
    :param plot_w: preset width
    :param plot_h: preset height
    '''
    if plot_cnt != 0:
        plotHeight = plot_h * plot_total_cnt / plot_cnt
        for plot in plot_widgets:
            plot.resize(plot_w, plotHeight)
            plot.setFixedSize(plot_w, plotHeight)

def get_show_color_dialog_handler(frame):
    '''
    Get a slot function to show color dialog.

    This method assumes that the frame is a self-defined ColorFrame which
    contains a ColorChangeSignal and this will emit the new RGB to call
    functions handling the color changing event.
    '''
    # closure
    def color_onchange():
        col = widgets.QColorDialog.getColor()

        if col.isValid():
            frame.setPalette(gui.QPalette(col))

            # emitting the event of color changing
            frame.emit(col.getRgb())

    return color_onchange

def visible_panel_onchange(widget, label, state, cnt):
    '''
        Reset the visibility of widget and its label.
    '''
    if state == core.Qt.Checked:
        widget.setVisible(True)
        label.setVisible(True)
        return cnt + 1
    else:
        widget.setVisible(False)
        label.setVisible(False)
        return cnt - 1

def get_bgcolor_reset_handler(plotWidget):
    '''
        Get the handler as slot to process event when background color changes.

        This contains the real processing logic which is separated from
        MainWindow.
    '''
    # use closure to encapsulate the target widget
    def resetBgColor(rgb):
        # print('in resetBgColor: ', rgb)
        plotWidget.setBackground(rgb)
    return resetBgColor

def get_cuvColor_reset_handler(plotItem):
    '''
        Get the handler as slot to process event when curve color changes.

        This contains the real processing logic which is separated from
        MainWindow.
    '''
    def resetCurveColor(rgb):
        # pen is to paint curve
        pen = pg.mkPen(color=rgb)
        plotItem.setPen(pen)

    return resetCurveColor

def get_markerColor_reset_handler(plotItem):
    '''
        Get the handler as slot to process event when marker color changes.

        This contains the real processing logic which is separated from
        MainWindow.
    '''
    def resetMarkerColor(rgb):
        brush = pg.mkBrush(color=rgb)
        plotItem.setSymbolBrush(brush)

    return resetMarkerColor

def get_marker_visible_handler(plotItem):
    '''
        Get the handler as slot to process event when marker visibility changes.

        This contains the real processing logic which is separated from
        MainWindow.
    '''
    def set_marker_visibility(state):
        if state == core.Qt.Checked:
            plotItem.setSymbol('o')
        else:
            plotItem.setSymbol(None)
    return set_marker_visibility

def get_grid_visible_handler(plotWidget):
    '''
        Get the handler as slot to process event when grid visibility changes.

        This contains the real processing logic which is separated from
        MainWindow.
    '''
    def set_grid_visibility(state):
        show = state == core.Qt.Checked
        plotWidget.showGrid(x=show, y=show)
    return set_grid_visibility


def get_open_file_handler(window, processor):
    '''
        Get the handler as slot to process event when the loading file is called.

        This only offers file selection dialog box and the real processing logic relies
        on the processor in the parameter.
    '''
    def showFileDialog():
        # print('avoking showFileDialog !')
        fname = widgets.QFileDialog.getOpenFileName(window, 'Open file', '/')  # 第一个返回值是文件路径，第二个是文件类型
        return processor(fname[0])
    return showFileDialog