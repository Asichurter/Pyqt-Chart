'''
    @Author: TangZhiJie 唐郅杰 2017141463155

    This file contains utility functions for "Engine" to
    calculate the differential values and integrate
    values based on the values read.

    Values input should be a Numpy array but not a list,
    returning type is list instead.
'''

def cal_differential(vals):
    minuend = vals[:-1]
    subtrahend = vals[1:]

    # substract difference
    diff = (subtrahend-minuend).tolist()
    # first differential value should be 0 anytime
    diff.insert(0,0)
    return diff

def cal_integrate(vals):
    integrate = []
    curVal = 0

    for val in vals:
        curVal += val
        integrate.append(curVal)

    return integrate