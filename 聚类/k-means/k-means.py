import numpy as np
from sklearn.cluster import KMeans
import sys
# 导入utils工具
sys.path.append(sys.path[0]+'../../../common')
import handle_data

# 数据示例
# py k-means.py 2 1,2;1.5,1.8;5,8;8,8;1,0.6;9,11 9,11

# 要分类的数据点
data = handle_data.split_date(sys.argv[2])

# 把上面数据点分组
clf = KMeans(n_clusters=int(sys.argv[1],0))
# 分组
clf.fit(data)

# 两组数据点的中心点
centers = clf.cluster_centers_
# 每个数据点所属分组
labels = clf.labels_
print('中心点',centers)
print('所属分组',labels)

# 预测
predict = handle_data.split_date(sys.argv[3])
label = clf.predict(predict)
print('预测',label)
