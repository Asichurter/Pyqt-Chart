'''
    @Author: TangZhiJie 唐郅杰 2017141463155

    This module is for configuring the program settings by a config manager.
    The manager is responsable to read configurations from config file and
    save the changes to file. Config values are accessible through config
    manager.

    The usable settings will be contained in an independent class called
    ConfigSet and the management of configs belong to a class called
    ConfigManager.
'''

import json

class ConfigSet:

    def __init__(self):
        self.MaxFileSize = 50
        self.ValueVisible = True
        self.DifferentialVisible = True
        self.IntegrateVisible = True
        self.ValueMarker = True
        self.DifferentialMarker = True
        self.IntegrateMarker = True
        self.ShowGrid = True
        self.PlotBgColor = [0, 0, 0]  # white bg in default
        self.PlotCurveColor = [255, 255, 255]  # black curve in default
        self.Marker = 'o'
        self.MarkerColor = [0, 0, 255]
        self.WindowWidth = 1800
        self.WindowHeight = 1400
        self.PlotWidth = 1500
        self.PlotHeight = 400
        self.LabelOneFontStyle = "QLabel{color:rgb(0,0,200);font-size:20px;font-weight:normal;font-family:Arial;}"
        self.LabelTwoFontStyle = "QLabel{color:rgb(0,0,0);font-size:15px;font-weight:normal;font-family:Arial;}"
        self.LabelThreeFontStyle = "QLabel{color:rgb(0,0,0);font-size:18px;font-weight:normal;font-family:Arial;}"
        self.IconPath = 'icon.png'

    def isVisible(self, plotName):
        '''
            fast way to read visibility information
            :param plotName: the name of plot, only allow 'Value',
                    'Differential' and 'Integrate'
        '''
        # assert plotName in ['Value','Differential', 'Integrate']
        return self.__getattribute__(plotName+'Visible')
    
    def items(self):
        return self.__dict__.items()

    def keys(self):
        return self.__dict__.keys()

    def set(self, k, v):
        self.__dict__[k] = v

class CongfigManager:

    def __init__(self, configPath='config.json'):
        self.defaultConfig = ConfigSet()
        self.readConfig = self.loadConfig(configPath)


    def loadConfig(self, path):
        if not path.endswith('.json'):
            return ConfigSet().__dict__
        try:
            with open(path, 'r') as f:
                configs = json.load(f)
                configs = self.checkAndCorrectConfig(configs)
                return configs
        except:
            return ConfigSet().__dict__



    def checkAndCorrectConfig(self, config):
        '''
            Check the attributes and values in read config, correct the
            illegal value and complement the missing attributes.
        '''
        checkedConfig = config

        for k,dv in self.defaultConfig.items():
            if k not in checkedConfig.keys():       # expected value not exist in read configs
                checkedConfig[k] = dv

            elif type(checkedConfig[k]) != type(dv):        # illegal data type found in read configs
                print('illegal key in config',k)
                checkedConfig[k] = dv

        for ck in checkedConfig.keys():
            if ck not in self.defaultConfig.keys():     # remove the redundant items
                del checkedConfig[ck]
        
        return checkedConfig

    def get(self, name):
        return self.readConfig[name]

        

            




