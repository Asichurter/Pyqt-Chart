'''
    @Author: TangZhiJie 唐郅杰 2017141463155

    This module is for loading a file in binary and convert it to a sequence of
    numbers by extract several bits to decimal without overlapping.

    The window size of bits is fixed to 16 (means short).

    Any errors occured will not be processed inside and errors should be
    identified and processed outside this module to offer useful tips.
'''

import os
import numpy as np

def loading(pth, maxSize):

    if os.path. os.path.getsize(pth)/1024 > maxSize:
        raise ValueError('文件过大')
    elif os.path. os.path.getsize(pth)/1024 == 0:
        raise ValueError('文件为空')
    try:
        with open(pth, 'rb') as reader:
            file = np.fromfile(reader, dtype=np.int16)
            return file
    except:
        # print("Unknow error occurs when loading the file: %s" % pth)       # read fails
        raise ValueError('无法打开文件')


