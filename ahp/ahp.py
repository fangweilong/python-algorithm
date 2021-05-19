import numpy as np
import pandas as pd
import sys
import json
import warnings

class AHP:
    def __init__(self, criteria, b):
        self.RI = (0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49)
        self.criteria = criteria
        self.b = b
        self.num_criteria = criteria.shape[0]
        self.num_project = b[0].shape[0]

    def cal_weights(self, input_matrix):
        input_matrix = np.array(input_matrix)
        n = input_matrix.shape[0]
        n1 = input_matrix.shape[1]
        # assert n == n1, '不是一个方阵'
        # for i in range(n):
        #     for j in range(n):
        #         if np.abs(input_matrix[i, j] * input_matrix[j, i] - 1) > 1e-7:
        #             raise ValueError('不是反互对称矩阵')

        eigenvalues, eigenvectors = np.linalg.eig(input_matrix)

        max_idx = np.argmax(eigenvalues)
        max_eigen = eigenvalues[max_idx].real
        eigen = eigenvectors[:, max_idx].real
        eigen = eigen / eigen.sum()

        if n > 9:
            CR = None
        else:
            CI = (max_eigen - n) / (n - 1)
            CR = CI / self.RI[n]
        return max_eigen, CR, eigen

    def run(self):
        max_eigen, CR, criteria_eigen = self.cal_weights(self.criteria)
#         print('准则层：最大特征值{:<5f},CR={:<5f},检验{}通过'.format(max_eigen, CR, '' if CR < 0.1 else '不'))
#         print('准则层权重={}\n'.format(criteria_eigen))

        max_eigen_list, CR_list, eigen_list = [], [], []
        for i in self.b:
            max_eigen, CR, eigen = self.cal_weights(i)
            max_eigen_list.append(max_eigen)
            CR_list.append(CR)
            eigen_list.append(eigen)

#         pd_print = pd.DataFrame(eigen_list,
#                                 index=['准则' + str(i) for i in range(self.num_criteria)],
#                                 columns=['方案' + str(i) for i in range(self.num_project)],
#                                 )
#         pd_print.loc[:, '最大特征值'] = max_eigen_list
#         pd_print.loc[:, 'CR'] = CR_list
#         pd_print.loc[:, '一致性检验'] = pd_print.loc[:, 'CR'] < 0.1
#         print('方案层')
#         print(pd_print)

        obj = np.dot(criteria_eigen.reshape(1, -1), np.array(eigen_list))
#         print('\n目标层', obj)
#         print('最优选择是方案{}'.format(np.argmax(obj)))

        result={}
        # 准则层权重
        result["criterionWeight"]=[float('{:.3f}'.format(i)) for i in criteria_eigen.tolist()]
        # 准则层自己的权重
        result["criterionList"]=[[float('{:.3f}'.format(y)) for y in i] for i in eigen_list]
        result["targetWeight"]=[[float('{:.3f}'.format(y)) for y in i] for i in obj.tolist()]
        result["optimal"]=np.argmax(obj)

        return result

if __name__ == '__main__':
  # 忽略警告
  warnings.filterwarnings('ignore')

  # 传入的值
  argv=sys.argv[1]
  matrix = argv.split("~")

  # 准则重要性矩阵
  importanceMatrix=[]
  # 准则层矩阵
  criterionMatrix=[]

  # 最大的矩阵
  matrixArry=[]
  for m in range(len(matrix)):
    listArry=[]
    listArry=matrix[m].split("-")
    for i in range(len(listArry)):
      listArry[i]=listArry[i].split(",")
      for y in range(len(listArry[i])):
          listArry[i][y]=float(listArry[i][y])
    # 拼接最大的组合矩阵
    matrixArry.append(np.array(listArry))

  print(AHP(matrixArry[0], np.delete(matrixArry,0,axis=0)).run())
