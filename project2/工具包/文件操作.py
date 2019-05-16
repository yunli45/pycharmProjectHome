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


# 说明：这个是扫描一个文件夹下所有文件小于某一个值的文件
# Filepath: 需要扫描的文件所在的目录
# fileSize：你筛选文件的大小基准，比如 10
# storage_capacity：存储的单位(kb , mb, ),默认为kb
def seachFile_size(Filepath, fileSize, storage_capacity='kb'):
    filList = []
    if storage_capacity == 'kb':
        storage_capacity_size = float(1024)
    elif storage_capacity == 'mb':
        storage_capacity_size = float(1024*1024)
    else:
        raise Exception("传入的参数不正确，存储的单位目前只支持mb、kb，默认为kb")

    for root, dirs, files in os.walk(Filepath, topdown=True):
        for name in files:
            file_size = os.path.getsize(r'{0}'.format(os.path.join(root, name)))
            file_size = file_size /storage_capacity_size   # 大小以kb为基准，小于10kb的全部不要
            if file_size <= fileSize:
                filList.append(os.path.join(root, name))
    return filList

def do():
    seachFile_size()

