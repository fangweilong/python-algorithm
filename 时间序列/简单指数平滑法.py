import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
from statsmodels.tsa.api import SimpleExpSmoothing

# 2020/01/01-10~2020/01/02-11~2020/01/03-15~2020/01/04-16~2020/01/05-17~2020/01/06-10
# 2020/02/01-20~2020/02/02-24~2020/02/03-20~2020/02/04-13~2020/02/05-30~2020/02/01-25
# 2020/03/01-0~2020/03/02-0

# 训练数据
matrix = sys.argv[1].split("~")
train={'time':[],'Count':[]}
for m in range(len(matrix)):
    listArry=matrix[m].split("-")
    train['time'].append(listArry[0])
    train['Count'].append(float(listArry[1]))
train=pd.DataFrame(train)

# 测试数据
matrix = sys.argv[2].split("~")
test={'time':[],'Count':[]}
for m in range(len(matrix)):
    listArry=matrix[m].split("-")
    test['time'].append(listArry[0])
    test['Count'].append(float(listArry[1]))

test=pd.DataFrame(test)

#预测数据
matrix = sys.argv[3].split("~")
prediction={'time':[],'Count':[]}
for m in range(len(matrix)):
    listArry=matrix[m].split("-")
    prediction['time'].append(listArry[0])
    prediction['Count'].append(float(listArry[1]))
prediction=pd.DataFrame(prediction)

train['Timestamp'] = pd.to_datetime(train['time'], format='%Y/%m/%d')
train.index = train['Timestamp']
train = train.resample('D').mean()

test['Timestamp'] = pd.to_datetime(test['time'], format='%Y/%m/%d')
test.index = test['Timestamp']
test = test.resample('D').mean()

#Plotting data
train.Count.plot(figsize=(15,8), title= 'Daily Ridership', fontsize=14)
test.Count.plot(figsize=(15,8), title= 'Daily Ridership', fontsize=14)

# 简单指数平滑法
fit = SimpleExpSmoothing(np.asarray(train['Count'])).fit(smoothing_level=0.6, optimized=False)
# 保留三位小数
prediction['SES'] = [round(i,3) for i in fit.forecast(len(prediction))]

print(prediction.to_json())