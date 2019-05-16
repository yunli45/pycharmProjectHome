# coding = utf-8
"""
    程序说明：
        在pycharm中使用Anaconda，解决了各种包的安装
        本次使用的是Python机器学习的库：scikit-learn 来实现
            关于决策树scikit-learn已经实现好了，我们只需要去调用相应的方法就好了
        决策树对于输入的值（属性、标记）必须是数值型的值
            比如年龄分为 youth mid senor，对于一条数据有属性age（ youth mid senor）：youth 、income
            (high、medium、low)：high；使用数值型来表示为：
            youth   mid senor   high    medium  low
            1       0    0      1        0    0
        数值型: 对于一个属性分为yes（1）、no（0）来显示

"""


