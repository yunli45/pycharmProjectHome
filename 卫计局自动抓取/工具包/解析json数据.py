"""
import json
# 这一组市用于解析json
json_text = response.strip('() \n\t\r').strip('[ ]')
obj = json.loads(json_text)
rs_list = data_list = obj['punishList']
for  ids,i in enumerate(rs_list):
    src_list.append(i['id'])
    book_num_list.append(i['wsh'])
"""