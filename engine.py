'''
    @Author: TangZhiJie 唐郅杰 2017141463155

    Program launching engine class, use a class named Engine
    to dispatch the interaction between components. Main function
    is also in this file. Moreover, class Engine contains some
    functions that will be used in MainWindow to load datas.
'''

from PyQt5 import QtWidgets as widgets
import sys

from fileLoader import loading
from window import MainWindow
from config import CongfigManager
from windowEventHandling import get_open_file_handler
from compute import cal_differential, cal_integrate

class Engine:
    def __init__(self):
        initInfo = widgets.QWidget()

        try:
            self.Data = None
            self.Names = ['Value', 'Differential', 'Integrate']
            self.CfgManager = CongfigManager()
            self.Datas = self.load_init()
            self.Window = MainWindow('Chart', self.Names, self.CfgManager.readConfig, self.Datas, self.load)

        # catch all unexpected exceptions and exit
        except:
            widgets.QMessageBox.information(initInfo, 'Message', "遇到了意料之外的错误，程序退出")
            exit(-1)

    def load_init(self):
        flag = True
        top = widgets.QWidget()
        while flag:
            path = get_open_file_handler(top, lambda x:x)()
            if path == '':        # nothing selected, exit
                exit(0)
            datas = self.load(path, auto=False)
            flag = (datas is None)

        return datas

    def load(self, path, auto=True):
        top = widgets.QWidget()
        try:
            vals = loading(path, self.CfgManager.get('MaxFileSize'))

        # bad config
        except AttributeError:
            widgets.QMessageBox.information(top, 'Message',
                                            "使用了损坏的配置文件！")
            exit(-1)

        # loading fails
        except ValueError as exc:
            msg = str(exc)
            widgets.QMessageBox.information(top, 'Message',
                                            "%s，请选择其他文件！"%msg)
            return None

        diffs = cal_differential(vals)
        ints = cal_integrate(vals)

        datas = {name:val for name,val in zip(self.Names, [vals,diffs,ints])}

        if auto:
            self.Window.load_datas(datas)
            # update data in engine
            self.Datas = datas
        else:
            return datas

if __name__ == '__main__':
    app = widgets.QApplication(sys.argv)
    e = Engine()
    sys.exit(app.exec_())