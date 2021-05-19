# -*- coding: UTF-8 -*-
import numpy as np

def split_date(data_str):
    matrix=data_str.split(";")
    data=[]
    for m in range(len(matrix)):
        listArry=matrix[m].split(",")
        dealArry=[]
        for n in range(len(listArry)):
            dealArry.append(float(listArry[n]))
        data.append(dealArry)
    return np.array(data)