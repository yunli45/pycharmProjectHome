import re

str1 ="""
2017-12-1我是一个大傻逼2017-1-1我是一个大傻逼2017-2-1我是一个大傻逼
"""
list1 = re.findall('\d{4}-\d{1,2}-\d{1,2}', str1)
for i in (list1):
    # str1 = str1.replace(str(i), '\n{0}'.format(str(i)))
    str1 = re.sub(str(i), '\n'+str(i), str1)
print(str1)