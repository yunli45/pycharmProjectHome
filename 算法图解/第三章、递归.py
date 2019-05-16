# 递归著主要有两个条件：线性条件、递归条件

def dg(num):
    print(num)
    num = num-1
    if num < 1:
        return num
    else:
        dg(num)
dg(10)