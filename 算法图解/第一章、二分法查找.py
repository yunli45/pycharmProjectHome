# 二分法查找的条件是：一个连续的数组

def erf(arr,res):

    low = 0
    hight = len(arr)-1
    mid_index = hight-low // 2
    mid = arr[mid_index]
    if mid <res:
        low = mid_index
    else:
        hight = mid_index
