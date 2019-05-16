# 第二章 选择排序：选择排序用于将数据按照大小进行排序

# 该方法用于找到一个数组中最小的元素，选择排序的核心
def findSmallest(arr):
    samllest = arr[0] # 存储最小的值
    smallest_index = 0 # 存储最小的值的索引
    for i in range(1,len(arr)):
        if arr[i] < samllest:
            smallest_index = i
            smallest = arr[i]
    return smallest_index

# 该方法是选择排序
def selectionSort(arr): # 对数组进行排序
    newArr = []
    for i in range(len(arr)):
        smallest  = findSmallest(arr) # 找出数组中最小的元素的索引，并将其假如到新的数组中，在原数组将其索引去掉，方便依次找最小的值
        newArr.append(arr.pop(smallest))
    return  newArr

print(selectionSort([3,2,5,10]))


