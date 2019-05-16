import re

# 'Content-Type': 'image/gif',
# 'Content-Type': 'application/vnd.ms-excel'
# adj_type = 'image/gif'
adj_type = 'image/gif'
# ss = re.findall('.*?(pdf|docx|doc|xlsx|xls|rar|zip|jpeg|jpg|png|gif|txt|7z|gz)', str(adj_type))
ss = re.findall('.*?(pdf|docx|doc|excel|rar|zip|jpeg|jpg|png|gif|txt|7z|gz)', str(adj_type))
if ss:
    print(ss[0])