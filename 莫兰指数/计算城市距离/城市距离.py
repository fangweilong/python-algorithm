# -*- coding: utf-8 -*-
from geopy.distance import geodesic
import pandas as pd
import numpy as np
import json
import os

#路径目录
baseDir = os.path.dirname(os.path.abspath(__file__))#当前目录

#读取省市字典
with open(baseDir+'/城市中心点.txt','r') as f:
    china = json.loads(f.read())


provincePm = {'city':[],'local':[]}
#读取各市pm2.5，求平均值作为整个省的pm2.5值
for city in china:
    print(city)
    print(china[city])
    provincePm['city'].append(city)
    provincePm['local'].append(china[city])
provincePm = pd.DataFrame(provincePm).set_index(['city'])

#构建空间权重矩阵
spaceMatrix = pd.DataFrame({},index=provincePm.index,columns=provincePm.index)

print(spaceMatrix)

for province1 in spaceMatrix.index:
    for province2 in spaceMatrix.columns:
        if not np.isnan(spaceMatrix.loc[province1,province2]):
            continue
        #两地距离
        #这里输入纬度在前，经度在后，所以做一下反转
        distance = geodesic(china[province1][::-1],china[province2][::-1]).m#距离(米)
        spaceMatrix.loc[province1,province2] = distance
        spaceMatrix.loc[province2,province1] = distance
        print(distance)
        #地点相同，距离取无穷大，不然后面的倒数会报错
        if not distance:
            spaceMatrix.loc[province1,province2] = 1e+10

print(spaceMatrix)
#删除空行和列
# spaceMatrix = spaceMatrix.drop(['西藏藏族自治区','海南省'],axis=0)
# spaceMatrix = spaceMatrix.drop(['西藏藏族自治区','海南省'],axis=1)
spaceMatrix.to_excel(baseDir+'/城市距离矩阵.xlsx')