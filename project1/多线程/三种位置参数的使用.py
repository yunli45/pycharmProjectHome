
# arg(单个参数)、 *args（元组参数）、**kwargs（字典参数）三个参数的位置必须是一定的。必须是(arg,*args,**kwargs)这个顺序，否则程序会报错。


# 一、*args的使用方法

#     *args 用来将参数打包成tuple给函数体调用

def function_1(*args):
    print(args, type(args))

function_1(1)


def function_2(x, y,  *args):
    print(x, y, args)

function_2(1, 2, 3, 4, 5)


# 二、**kwargs的使用方法

#     **kwargs 打包关键字参数成dict给函数体调用


def function_3(**kwargs):
    print(kwargs, type(kwargs))


function_3(a=3)


def function_3(**kwargs):
    print(kwargs)


function_3(a=3, b=4, c=6)


def function_4(arg, *args, **kwargs):
    print(arg, args, kwargs)


function_4(6, 7, 8, 9, a=1, b=2, c=3)
