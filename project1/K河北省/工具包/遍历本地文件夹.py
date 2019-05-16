import os.path
import re

# def eachFile(filePath):
#     allFileList=[]
#     pathDir = os.listdir(filePath) # 返回filePath指定的文件夹包含的文件或文件夹的名字的列表。
#     for allDir in pathDir:         # 遍历出父目录下的所有子目录，并从子目录中提取下一级的目录
#         child = os.path.join('%s\%s'%(filePath,allDir))
#         # print(child)
#         if os.path.isfile(child):
#             allFileList.append(child)
#             print(str(allFileList)+"\n\n")
#         else:
#         # return  allFileList
#             eachFile(child)
#
#     return allFileList
#     # print(pathDir)

def eachFile(path):
    filList = []
    for root, dirs, files in os.walk(path, topdown=True):

        for name in files:
            filList.append(os.path.join(root, name))
    return filList


print(eachFile(r'F:\卫计局\卫计局附件'))