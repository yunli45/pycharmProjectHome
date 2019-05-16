import os, os.path,shutil
import sys


def seachFile(Filepath):
    filList = []
    for root, dirs, files in os.walk(Filepath, topdown=True):
        for name in files:
            filList.append(os.path.join(root, name))
    return filList


def excel(excelFileList,Filepath):
    fileList = seachFile(Filepath)
    for (execlPath ) in   (excelFileList):
        for filePath in fileList:
            # print(b)
            if execlPath[execlPath.rfind("\\")+1:] == filePath[filePath.rfind("\\")+1:] and execlPath !=filePath:
                newFilePath = execlPath[:execlPath.rfind("\\")+1]
                # newFilePath =  execlPath
                # 目录不存在就创建
                mkdir(newFilePath)
                shutil.move(filePath , newFilePath)


# 创建目录
def mkdir(path):
    # 去除首位空格
    path = path.strip()

    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path+"创建成功")
    else:
        print(path+"目录已存在")





excelFileList = [r'G:\卫计局\2\4\13.docx',r'G:\卫计局\2\4\57.docx',r'G:\卫计局\2\4\90.docx']

excel(excelFileList,'G:\卫计局')
