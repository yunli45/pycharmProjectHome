import os
from os.path import join


def seachFile(Filepath):
    filList = []
    for root, dirs, files in os.walk(Filepath, topdown=True):
        for name in files:


            if file_size <= 10:
                filList.append(os.path.join(root, name))
            # else:
            #     print(r'{0}'.format(os.path.join(root, name)))
    return filList



