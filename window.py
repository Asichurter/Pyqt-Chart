'''
    @Author: TangZhiJie 唐郅杰 2017141463155

    Main window class for GUI of the program.

    In essence, this class is a PyQt MainWindow so it must be
    used with a QtApp together. This class contains widget
    management, layout management, style management and
    it only manages components but their processing logic,
    which is included in windowEventHandling.py.

    To achieve loose-coupling requirement, the api about
    processing logic knows nothing about the window and
    the control is in main window, the caller who decides
    the argments of api calling.
'''

from PyQt5 import QtWidgets as widgets
from PyQt5 import QtCore as core
from PyQt5 import QtGui as gui
import pyqtgraph as pg
import numpy as np

from windowEventHandling import resize_plots_adaptively, get_show_color_dialog_handler, \
                                    visible_panel_onchange, get_bgcolor_reset_handler, \
                                    get_cuvColor_reset_handler, get_marker_visible_handler,\
                                    get_grid_visible_handler, get_markerColor_reset_handler, \
                                    get_open_file_handler
from components import ColorFrame

class MainWindow(widgets.QMainWindow):
    '''
        This class provide the window to display the values and processing
        logics are integrated inside to provide interactions.
    '''
    def __init__(self, title, names, cfg, datas, reloadProcessor):
        super(MainWindow, self).__init__()
        self.Cfg = cfg
        self.setWindowTitle(title)
        self.setWindowIcon(gui.QIcon(self.Cfg['IconPath']))

        self.PlotNames = names
        self.PlotWidgets = {}.fromkeys(self.PlotNames)
        self.PlotCheckBoxes = {}.fromkeys(self.PlotNames)
        self.PlotLabels = {}.fromkeys(self.PlotNames)
        self.PlotItems = {}.fromkeys(self.PlotNames)
        self.VisiblePlotCnt = 0
        self.Datas = datas
        self.ReloadProcessor = reloadProcessor          # the handler processing file loading event

        self.UIinit()

    def UIinit(self):
        '''
            Initialization of UI widgets.
        '''

        # resize the window and fix
        self.resize(self.Cfg['WindowWidth'], self.Cfg['WindowHeight'])
        self.setFixedSize(self.Cfg['WindowWidth'], self.Cfg['WindowHeight'])

        # global layout
        self.global_layout()

        # add plot widget to plot layout
        for name in self.PlotNames:
            self.add_plot_widget(name, self.Cfg['PlotWidth'], self.Cfg['PlotHeight'])

        # loading data before control panel constructed, after widgets ready
        self.load_datas(self.Datas)

        # add visible widget to panel layout
        self.add_visible_widget()

        # add adjusting panel to panel layout
        for name in self.PlotNames:
            self.add_adjust_panel(name)

        # add opening file menu
        self.add_file_menu()

        self.show()



    def global_layout(self):
        '''
            global layout setting, containing two layouts:
            plotLayout to hold plot widgets, panelLayout to hold panel widgets.
        '''
        self.plotLayout = widgets.QVBoxLayout()
        self.panelLayout = widgets.QVBoxLayout()
        self.globalLayout = widgets.QHBoxLayout()

        # self.panelLayout.addStretch(1)
        self.globalLayout.addLayout(self.panelLayout)
        self.globalLayout.addLayout(self.plotLayout)

        self.Widget = widgets.QWidget()
        self.Widget.setLayout(self.globalLayout)
        self.setCentralWidget(self.Widget)



    def add_visible_widget(self):
        '''
            add the visible setting panel to panelLayout.
            This method will reuse the checkbox widget adding method providing
            label, checked value, handler and parent layout.
        '''

        visLayout = widgets.QVBoxLayout()

        # create widget label
        visLabel = widgets.QLabel('Visible setting', self)
        visLabel.setStyleSheet(self.Cfg['LabelOneFontStyle'])
        visLabel.setAlignment(core.Qt.AlignBottom | core.Qt.AlignLeft)
        visLayout.addWidget(visLabel)
        visLayout.setAlignment(core.Qt.AlignTop)

        # create check boxes

        for name in self.PlotNames:
            self.add_checkbox_widget(label=name,
                                     checked=self.Cfg[name + 'Visible'],
                                     handler=self.visible_panel_onchange_adapter,
                                     parent=visLayout)

        # add the visible panel to the pabel layout
        self.panelLayout.addLayout(visLayout)



    def add_plot_widget(self, label, w, h):
        '''
            Add a plot widget to plotLayout without filling a plotItem in it.
            Showgrid attribute and style are set according to configs. The "label"
            parameter is the name of the plot widget and w,h refer to plot width and
            height respectively that are decided by configs.
        '''

        plotWidget = pg.PlotWidget()
        plotLabel = widgets.QLabel(label, self)

        # set grid
        showGrid = self.Cfg['ShowGrid']
        plotWidget.showGrid(x=showGrid, y=showGrid)

        # plot label is set big one font style
        plotLabel.setStyleSheet(self.Cfg['LabelOneFontStyle'])

        # adjust the size of plot
        plotWidget.resize(w, h)
        plotWidget.setFixedSize(w, h)

        # visible setting
        isVisible = self.Cfg[label+'Visible']
        if isVisible:
            plotWidget.setVisible(True)
            self.VisiblePlotCnt += 1

        # add to layout
        self.plotLayout.addWidget(plotLabel)
        self.PlotLabels[label] = plotLabel
        self.plotLayout.addWidget(plotWidget)
        self.PlotWidgets[label] = plotWidget



    def add_adjust_panel(self, label):
        '''
            Add an adjusting panel to the panelLayout, this module is in equal level
            of visible panel. All child controling panels are in this layout including
            label tag, background color panel, curve color panel, marker color panel,
            marker visibility panel and grid visibility panel.

            The alignment is set inside this method, and the order of the code somehow
            decides the order of widgets. The skeleton of all color changing panels rely
            on "add_color_adjust_widget" which encapsulates UI composition and only some
            parameters like handler, default color and content etc. should be determined.
            All slot functions are from windowEventHandling.py which is loose-coupled with
            window.
        '''

        # panel trivials and labeling
        adjustPanel = widgets.QVBoxLayout()
        adjustPanelLabel = widgets.QLabel(label, self)
        adjustPanelLabel.setStyleSheet(self.Cfg['LabelOneFontStyle'])
        adjustPanelLabel.setAlignment(core.Qt.AlignLeft | core.Qt.AlignBottom)
        adjustPanel.addWidget(adjustPanelLabel)

        # for bg color panel
        bgColorPanel = widgets.QVBoxLayout()
        bgColorRGB = self.Cfg['PlotBgColor']
        bgColorOnChangeHandler = get_bgcolor_reset_handler(self.PlotWidgets[label])
        labelContent = 'background color'
        self.add_color_adjust_widget(labelContent, bgColorRGB, bgColorOnChangeHandler, bgColorPanel)
        bgColorPanel.setAlignment(core.Qt.AlignBottom)

        # for cuv color panel
        cuvColorPanel = widgets.QVBoxLayout()
        cuvColorRGB = self.Cfg['PlotCurveColor']
        cuvColorOnChangeHandler = get_cuvColor_reset_handler(self.PlotItems[label])
        labelContent = 'curve color'
        self.add_color_adjust_widget(labelContent, cuvColorRGB, cuvColorOnChangeHandler, cuvColorPanel)
        cuvColorPanel.setAlignment(core.Qt.AlignBottom)

        # for marker color panel
        mkColorPanel = widgets.QVBoxLayout()
        mkColorRGB = self.Cfg['MarkerColor']
        print(mkColorRGB)
        mkColorOnChangeHandler = get_markerColor_reset_handler(self.PlotItems[label])
        mkContent = 'marker color'
        self.add_color_adjust_widget(mkContent, mkColorRGB, mkColorOnChangeHandler, mkColorPanel)
        mkColorPanel.setAlignment(core.Qt.AlignBottom)

        # for marker visibility
        self.add_marker_visible_widget(label, adjustPanel)

        # for grid visibility
        self.add_grid_visible_widget(label, adjustPanel)

        adjustPanel.addLayout(bgColorPanel)
        adjustPanel.addLayout(cuvColorPanel)
        adjustPanel.addLayout(mkColorPanel)

        self.panelLayout.addStretch(50)
        self.panelLayout.addLayout(adjustPanel)



    def add_color_adjust_widget(self, labelCont, defaultRGB, colorOnChangeHandler, parentPanel):
        '''
            Providing content, color, handler and layout, offers a color changing UI template.
            This method relies on slot function "get_show_color_dialog_handler" to call dialog box.

            Also, this module uses self-defined ColorFrame to receive the color changing event and
            emit new color to handlers where changing event is indeed processed.
        '''
        r,g,b = defaultRGB

        # layout
        bgColorLayout = widgets.QHBoxLayout()

        # label
        bgColorLabel = widgets.QLabel(labelCont, self)
        bgColorLabel.setStyleSheet(self.Cfg['LabelTwoFontStyle'])
        # let the label attach to the widget
        bgColorLabel.setAlignment(core.Qt.AlignBottom | core.Qt.AlignLeft)

        # palette
        bgColorPalette = gui.QPalette(gui.QColor(r,g,b))

        # color frame
        # self-defined color frame, to receive color changing event
        bgColorFrame = ColorFrame()
        bgColorFrame.setPalette(bgColorPalette)
        bgColorFrame.setAutoFillBackground(True)

        # button
        bgColorButton = widgets.QPushButton('change', self)

        # bunding color dialog event handler
        bgColorButton.clicked.connect(get_show_color_dialog_handler(bgColorFrame))

        # bunding real color changing event handler
        bgColorFrame.connect(colorOnChangeHandler)

        bgColorLayout.addWidget(bgColorFrame)
        bgColorLayout.addWidget(bgColorButton)

        parentPanel.addWidget(bgColorLabel)
        parentPanel.addLayout(bgColorLayout)



    def add_marker_visible_widget(self, name, parent):
        '''
            Add marker visibility widget to widget panel. Only a checkbox bunding
            slot function is used and the handler is defined outside and the name
            of the editting plot should be provided.
        '''

        handler = get_marker_visible_handler(self.PlotItems[name])
        checked = self.Cfg['ShowGrid']
        self.add_checkbox_widget(label='show marker', checked=checked, handler=handler, parent=parent)



    def add_grid_visible_widget(self, name, parent):
        '''
            Add grid visibility widget to widget panel, almost the same as "add_marker_visible_widget"
            except the handler. This method also uses the checkbox template to create widget quickly.
        '''
        handler = get_grid_visible_handler(self.PlotWidgets[name])
        checked = self.Cfg[name + 'Marker']
        self.add_checkbox_widget(label='show grid', checked=checked, handler=handler, parent=parent)



    def add_checkbox_widget(self, label, checked, handler, parent):
        '''
            Template method to create a checkbox widget with label, handler and parent
            layout provided.
        '''
        checkBox = widgets.QCheckBox(label, self)
        checkBox.setChecked(checked)
        checkBox.stateChanged.connect(handler)
        parent.addWidget(checkBox)



    def add_file_menu(self):
        '''
            Add file option to menu and bund it with a slot function handling the file
            changing event. The slot function provided by "get_open_file_handler" only
            start a dialog box, and the specific handling logic should be provided
            by ReloadProcessor which is offered by upper level caller "Engine".
        :return:
        '''
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileOpenAction = widgets.QAction('&Open', self)
        fileOpenAction.triggered.connect(get_open_file_handler(self, self.ReloadProcessor))
        fileMenu.addAction(fileOpenAction)




    def visible_panel_onchange_adapter(self, s):
        '''
            Adapter method to change visibility of plot widget. Because the plotcount
            value will be updated after the calling of this method, extern slot functions
            are hard to adopt which is replaced by this adapter.

            This adapter uses two extern handling funciton to do main logic and little
            work is done by this method in fact. Two steps are taken:
            1. change the visibility of plot
            2. resize the plot to adapt to the change
        '''

        label = self.sender().text()

        # set plot visibility of plot and update count
        self.VisiblePlotCnt = visible_panel_onchange(self.PlotWidgets[label],
                                                     self.PlotLabels[label],
                                                     s,
                                                     self.VisiblePlotCnt)

        # resize the plot size after the size changing
        resize_plots_adaptively(self.PlotWidgets.values(),
                                len(self.PlotWidgets.values()),
                                self.VisiblePlotCnt,
                                self.Cfg['PlotWidth'],
                                self.Cfg['PlotHeight'])
        widgets.QApplication.processEvents()



    def load_datas(self, plotDatas):
        '''
            Load datas from "Engine" to plot, fill the datas to corresponding
            PlotItem.

            If this method is called when a file has already been loaded, it
            will not construct new PlotItems and only update data in them.

            First loading will use configs to plot.
        '''

        for name in plotDatas.keys():
            length = len(plotDatas[name])
            x = np.linspace(0, length, length)

            if self.PlotItems[name] is None:
                plotItem = pg.PlotDataItem(x, plotDatas[name], symbol=self.Cfg['Marker'])
                plotItem.setSymbolBrush(pg.mkBrush(color=self.Cfg['MarkerColor']))

                self.PlotItems[name] = plotItem
                self.PlotWidgets[name].addItem(self.PlotItems[name])

                # init the visibility based on config
                self.PlotWidgets[name].setVisible(self.Cfg[name+"Visible"])
                self.PlotLabels[name].setVisible(self.Cfg[name+'Visible'])

            # already exists PlotItem, only update the data in it
            else:
                self.PlotItems[name].setData(x, plotDatas[name])








