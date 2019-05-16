import _thread
import time


# 为线程定义一个函数
def print_time(th_name, delay):
    count = 0
    while count<5:
        time.sleep(delay)
        count+=1
        print("%s: %s" % (th_name, time.ctime(time.time())))

# 创建两个线程
try:
    _thread.start_new_thread(print_time,("th-1",2))
    _thread.start_new_thread(print_time,("th-2",4))
except:
    print("无法启动西安测绘给你")
while 1:
    pass


# # 创建两个线程
# try:
#    _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
#    _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
# except:
#    print ("Error: 无法启动线程")
#
# while 1:
#    pass