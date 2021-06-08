# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import json
import sys
import os

# 数据示例
# 无锡,10~上海,20

#当前目录
baseDir = os.path.dirname(os.path.abspath(__file__))
# 导入
sys.path.append(baseDir)
from MoranI import moranI

record=sys.argv[1]

# 为了删除数据
nullArry=[]
#城市-数值字典
cityPm = {'city':[],'num':[]}

# 拆分
cityList = record.split("~")
for m in range(len(cityList)):
    listArry=[]
    listArry=cityList[m].split(",")
    for i in range(len(listArry)):
        nullArry.append(listArry[0])
        cityPm['city'].append(listArry[0])
        cityPm['num'].append(float(listArry[1]))

cityPm = pd.DataFrame(cityPm).set_index(['city'])

#构建空间权重矩阵
spaceMatrix = pd.read_excel(baseDir+'/城市距离矩阵.xlsx',index_col=0,engine='openpyxl')

#观测值矩阵 同时删除没有的行和列
spaceMatrix=pd.DataFrame(spaceMatrix,columns=nullArry)
print('spaceMatrix:{}==========================',spaceMatrix)
spaceMatrix=pd.DataFrame(spaceMatrix,index=nullArry)
print('spaceMatrix:{}==========================',spaceMatrix)
#取反距离，次幂可去1~3
spaceMatrix = spaceMatrix**-3

#计算莫兰指数
result = moranI(spaceMatrix,cityPm)

print(result)
