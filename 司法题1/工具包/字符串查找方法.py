# -*- coding: utf-8 -*-
"""
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""

# 参数说明：arg(全文)、arg1（查找的内容）
def findalls(arg, arg1, start=0):
    body = arg
    result = []
    while True:
        pos = body.find(arg1, start)
        if pos >= 0:
            result.append(pos)
            start = pos + len(arg1)
            # body = body[pos+len(arg):]
            continue
        break
    # print(result)
    return result