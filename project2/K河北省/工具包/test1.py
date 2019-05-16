# coding:utf-8
import re

str1 = """
totalRecord =  17707 ;totalPage =  1771 ;dataStore = ["CF$49A60C397D382713BBB484D600AA65B806224734F0FB3ABD911170869C17627186A1D4B9581B473D$赵望兴损坏他人财物案$永州市祁阳县县公安局$2018/12/16$2018/12/16","CF$389F447C42834B050667E7279D363380FDD7C054A08BF7B8858C871C36792BEF4B2C6C1462F9AEB3$蓝山县祥之葳健康体验中心虚假宣传案$永州市蓝山县县市场和质量监督管理局$2018/12/14$2018/12/14","CF$22A53DDEC0D87616DD527C71A49F9E523649AFAC387AB7ED7A4C05F617E5DB555772E6BF146355F5$陈志军冒用他人身份$永州市祁阳县县公安局$2018/12/14$2018/12/14","CF$0562FBF416645A77313BE2A3ED827262BAB0607FCD3DB07C1EBE0C9A3BA2CE17CFDAFB696553883B$杨加琴无证驾驶$永州市祁阳县县公安局$2018/12/14$2018/12/14","CF$DD2443677C412FF6B12351380CD6E094F8E8DE6B7622004B39679F0FDA515C40CD309417559746EA$百姓诊所$永州市江华县县卫计委$2018/12/13$2018/12/13","CF$CA95643BA0C0523E7974777F5C3852C8CC9DFB8399C2E2FAA7A1D189A29142CDB74ACDFAAAD48436$[2018]年度宁第345号$永州市宁远县县烟草专卖局$2018/12/13$2018/12/13","CF$88EFA9EB887738CC1154714873C7F51384DED6E9D18C8E48CA209A882D482582EFFC710CEAD2EE2A$东安湘江焊材有限公司擅自施工建设的违法事实,存在建设法定手续不完备$永州市东安县住建局$2018/12/11$2018/12/11","CF$14B5B4E840824F39DA6EFCE1D32DF4D81DB9F37B5AE893B01F2D3FC255AA65257DF35ED56EE65363$违反大气污染防治法$永州市宁远县县环保局$2018/12/06$2018/12/06","CF$6C559BF7297934B32DE756E592AB9892AAC20837A83F9DA8E797A4849FACAA85928CA6256C20B695$周得胜等人吸毒案$永州市祁阳县县公安局$2018/12/04$2018/12/04","CF$9B999DA49E1B5F74B1879EC87F8C0A2B6E8C74D0D49308E018865A68D87434AFC9AC08FE77CBD9C2$祁阳县帅俊高硅沙场有限公司违反环评制度案$永州市祁阳县县环保局$2018/12/03$2018/12/03",]
"""

# rs = re.findall(r'var initData = \[(.*?)\]',str1)
rss = re.findall(r'"CF\$(.*?)\$(.*?)\$(.*?)\$(.*?)\$(.*?)"',str(str1))
print(rss)

from bs4 import BeautifulSoup
# str_s = BeautifulSoup(str1, 'lxml')
# str_s = str_s.find_all('td', attrs={'valign':'top'})
# str_ss = BeautifulSoup(str(str_s), 'lxml')
# str_sss = str_ss.find_all('td', attrs={'class':'xzcf_xx'})
# str_sss = re.findall('<td.*?class="xzcf_jds".*?>(.*?)</td>',str(str1), flags=re.S|re.M)
# str_ssss = re.findall('<td.*?class="xzcf_xx".*?>(.*?)</td>',str(str1))
# str_ssss = str_ss.find_all('td', attrs={'class':'xzcf_jds'})
# print(str_sss)
# print(str_ssss)
# # if str_ssss:
# #     per = str_ssss[1].replace("&nbsp;", '')
# #     per_1 = per[:per.find("<span")]
# #     per_2 = per[per.find("</span>")+7:]
# #     print(per_2)