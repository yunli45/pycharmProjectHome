from numpy import *  # 科学计算包
import operator   #  运算符模块,K-近邻算法执行排序操作的时候将使用这个模块提供的函数

# 创建数据集和标签
def createDtaSet():
    group=array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]]) # array()函数
    lables = ['A','A','B','B']
    return group,lables

group,lables=createDtaSet()
print(group)
"""
[[1.  1.1]
 [1.  1. ]
 [0.  0. ]
 [0.  0.1]]
"""
# print(lables)
# ['A', 'A', 'B', 'B']
def classify0(inX,dataSet,labels,k):
    dataSetSize = dataSet.shape[0]   #  ==》4   返回矩阵的行数（0）与列数（1） ，shape[0]，shape[1],分别返回值为矩阵的行数与矩阵的列数
    diffMat = tile(inX,(dataSetSize,1)) - dataSet # 构建一个维数和训练集一致的一个数组，减去训练集得到该数据与训练集中每一个数据每一维的差
    """
 [[1 1]     [[ 0.  -0.1]
 [1 1]       [ 0.   0. ]
 [1 1]       [ 1.   1. ]
 [1 1]]      [ 1.   0.9]]
    """
    sqDiffMat = diffMat**2  # 平方值
    """
[[0.   0.01]
 [0.   0.  ]
 [1.   1.  ]
 [1.   0.81]]

    """
    sqDistances = sqDiffMat.sum(axis=1)
    """
    按行求和
  [0.01  0.   2.   1.81]
    """
    distance = sqDistances**0.5 # 开根号
    sortedDistIndicies = distance.argsort() # 返回数组从小到大的索引值
    print(sortedDistIndicies)
    classCount ={}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0)+1  # 字典的get（key，default=None）返回指定键的值，如果值不在字典中返回默认值None,如果指定第二个参数，找不到的时候就返回第二个参数
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    # print(sortedClassCount[0][0]) # A
    return sortedClassCount[0][0]

classify0([1,1],group,lables,3)

# 将文件转化为矩阵（matrix）
# def file2matrix(filename):
#     fr = open(filename)
#     arrayOLines = fr.readlines()
#     numberOfLines = len(arrayOLines)
#     returnMat = zeros((numberOfLines, 3))  # lines_number行 3列
#     classLabelVector = []
#     index = 0
#     for line in arrayOLines:
#         line = line.strip()
#         listFromLine = line.split("\t")
#         returnMat[index,:] = listFromLine[0:3]
#         classLabelVector.append(int(listFromLine[-1]))
#         index +=1
#     # 关闭打开的文件
#     fr.close()
#     return returnMat,classLabelVector
#
# datingDataMat,datingLabels = file2matrix('E:\Python\PyCharm\project\AdministrativePenalty\代理池\datingTestSet2.txt')
# print(datingDataMat)
# print(datingLabels[0:20])


