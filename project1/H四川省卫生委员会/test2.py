# coding:utf-8
cont="""

<div align="center">川卫规〔2018〕3号</div><br/>
<div align="center">川卫发〔2018〕46号</div><br/>
<p align="center"><strong>川卫办发〔2018〕46号</strong></p><br/>
"""


import re
rs = re.findall(".*?川卫[办 发 规].*?\d号", cont)
print(rs)