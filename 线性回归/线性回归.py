from sklearn import datasets,linear_model
import sys

# 数据示例
#[[100,4,9.3],[50,3,4.8],[100,4,8.9],[100,2,6.5],[50,2,4.2],[80,2,6.2],[75,3,7.4],[65,4,6],[90,3,7.6],[90,2,6.1]]
#100,4,9.3;50,3,4.8;100,4,8.9;100,2,6.5;50,2,4.2;80,2,6.2;75,3,7.4;65,4,6;90,3,7.6;90,2,6.1

#当前目录
baseDir = os.path.dirname(os.path.abspath(__file__))
# 导入utils工具
sys.path.append(baseDir+'../../common')
import handle_data


# 定义训练数据
data = handle_data.split_date(sys.argv[1])

Y = data[:,0]
X = data[:,1:]

# 训练数据
regr = linear_model.LinearRegression()
regr.fit(X,Y)
print('系数:',regr.coef_)
print('截距:',regr.intercept_)
print('R方：',regr.score(X,Y))
