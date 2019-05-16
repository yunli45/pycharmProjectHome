import os
for root, dirs, files in os.walk('E:\Python\PyCharm\project\AdministrativePenalty\司法模拟题整理'):
    # print(root)  # 当前目录路径
    # print("前路径下所有非目录子文件："+str(files))  # 当前路径下所有非目录子文件
    files = files
    # print(dirs)  # 当前路径下所有子目录
    # dirs = dirs
    print(files)