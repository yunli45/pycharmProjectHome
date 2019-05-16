# -*- coding=gbk -*-


import re
import os,shutil
import openpyxl
import requests
from bs4 import BeautifulSoup

from 卫计局数据校正 import 链接数据库,预处理模块,附件下载程序
from 卫计局数据校正.判断url前面的点返回完整的请求地址 import returnSRC

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

def parePage (contenSrc):
    print(contenSrc)
    # contenSrc = 'http://www.nhfpc.gov.cn/zwgk/jdjd/201804/96ab7d7da43f45068d2afca782873d69.shtml'
    resposn = requests.get(contenSrc,headers=header)
    response = resposn.content.decode('utf-8', errors='ignore')
    soup = BeautifulSoup(response, 'lxml')

    soupCont1 = soup.find_all('div', attrs={'class': 'content'})  # z正文
    soupCont2 = soup.find_all('div', attrs={'class': 'xw_box'})
    soupCont3= soup.find_all('div', attrs={'id': 'xw_box'})
    print(soupCont3)
    if soupCont3 !=[]:
        soupCont = soupCont3
    else:
        print("xw_box还有起的格式")
    # if soupCont1 != [] or soupCont2 != [] :
    #     if soupCont1 != []:
    #         soupCont = soupCont1
    #     elif soupCont2 != []:
    #         soupCont = soupCont2
    #     # print("soupCont2" + str(soupCont2))
    # else:
    #     print("除了content、con还有其他的格式")
    print("soupCont"+str(soupCont))
    超链接本地地址 = '/datafolder/卫计局数据校正/卫生健康委员会/热点栏目/解读'
    SavePath = r"F:\卫计局\卫计局附件\卫生健康委员会\热点栏目\解读\%s"
    indexUrl ='http://www.nhfpc.gov.cn/zwgk/jdjd/ejlist.shtml'
    content = 预处理模块.disposeOfData(indexUrl, contenSrc, str(soupCont[0]), SavePath, 超链接本地地址)

    print(content)
    return content


def eachFileName(Filepath):
    # 获取本地附件的名字
    fileNameList = []
    for root, dirs, files in os.walk(Filepath, topdown=True):
        for name in files:
            file = os.path.join(root, name)
            file1 = file[file.rfind("\\")+1:]
            fileNameList.append(file1)
    return fileNameList

def seachFilePath(Filepath):
    # 获取本地附件完整的地址
    filePathList = []
    for root, dirs, files in os.walk(Filepath, topdown=True):
        for name in files:
            filePathList.append(os.path.join(root, name))
    return filePathList

def mkdir(path):
    # 判断传进来的路径是否存在，不存在就创建
    # 去除首位空格
    path = path.strip()

    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + "创建成功")
    else:
        pass
        # print(path + "目录已存在")

# 读取excel中文件路径和本地已有的文件的路径进行比较，路径错误的就将文件移到正确的路径下，本地不存在的就打印出来
def readExcelFile(Filepath,excelPath1,excelPath2):
    # 读取excel中文件路径和本地已有的文件的路径进行比较，路径错误的就将文件移到正确的路径下，本地不存在的就打印出来
    data = openpyxl.load_workbook(excelPath1)
    active = data.active
    table = data['Sheet1']
    rows = table.max_row

    data2 = openpyxl.load_workbook(excelPath2)
    active2 = data2.active
    table2 = data2['Sheet1']
    rows2 = table2.max_row
    # 获取本地所有相关文件名的完整路径
    FilePathList = seachFilePath(Filepath)
    # 获取本地本地所有相关文件名名称
    FileNameList = eachFileName(Filepath)

    for row in range(2,rows+1) :
        # print("正在读取第："+str(row)+"的数据")
        rowC = 'C%s'%(row) # 标题
        rowC_Va = table[rowC].value
        # print(rowC_Va)

        rowJ = 'J%s'%(row) # 全文
        rowJ_Va = table[rowJ].value

        rowK = 'K%s' % (row)  # 全文
        rowK_Va = table[rowK].value

        rsFile = re.findall(r'<a.*?href="/(.*?)".*?>',str(rowJ_Va))
        # print(rsFile)

        # 比较本地保存的附件和全文内容上面的附件，该附件在本地是否存在，不存在就会在控制台打印出相应的标题和附件位置
        # if rsFile!=[]:
        #     rs = rsFile[0].replace("卫计局数据校正",'')
        #     rs1 = r"F:\\卫计局数据校正\\卫计局附件"+rs.replace("/",r'\\')
        #     if rs1 in filList:
        #         pass
        #     else:
        #         print("这条数据貌似在本地没有相应的附件，请查看下。相应的标题为："+str(rowC_Va))
        #         print("这条数据的附件名字为："+rs1)
        #         print("\n")
        # #
        #  比较本地所有的文件的和excel中文件
        #     先比较完整的路径，在比较完整路劲匹配不上的情况
                # 在完整路径匹配不到的情况下，比较文件名，如果本地存在相应的文件名，那就是位置村错误了，本地没有相应的文件名那就是缺失文件

        # """"""
        if rsFile !=[]:
            rs = rsFile[0]
            if rs.find("@") != -1 or rs.find("www") != -1:
                pass
            else:
                # print(rs)
                # print(rowC_Va)
                # F:\\卫计局数据校正\\卫计局附件\\食品安全标准与检测评估司\\政策文件\\doc9458.doc
                # print("rs"+rs)
                附件本地完整地址拼接 = rs .replace("卫计局数据校正/",'')
                附件本地完整地址拼接 = "F:\\卫计局数据校正\\卫计局附件\\"+附件本地完整地址拼接.replace("/","\\") # 将超链接中 / 替换为 \，拼接为一个完整的本地附件地址
                附件本地完整地址拼接 = 附件本地完整地址拼接.replace('\\',r'\\')  # 将拼接出来的完整地址中 \ 替换为 \\ ;F:\\卫计局数据校正\\卫计局附件\\食品安全标准与检测评估司\\政策文件\\doc9458.doc
                附件本地完整地址 = 附件本地完整地址拼接

                if 附件本地完整地址 in FilePathList:
                    # print("该文件已存在1")
                    pass
                else:
                    # 现在开始比较文件名
                    fileName = 附件本地完整地址[附件本地完整地址.rfind("\\")+1:]
                    # print("fileName"+fileName)
                    if fileName in FileNameList:
                        pass
                        # 在本地存在相应的文件名
                        newPath = 附件本地完整地址[:附件本地完整地址.rfind(r"\\")+2]
                        mkdir(newPath)
                        # print("newPath"+newPath)
                        if os.path.exists(newPath):
                            # print("该文件已存在2")
                            pass
                        else:
                            for  path in FilePathList:
                                # 将本地相应的文件名的完整路径找出来
                                if path.find(fileName) !=-1:
                                    oldFilepath = path
                                    shutil.move(oldFilepath,newPath)
                            break
                    else:
                        SQL = "select 标题,这条数据的完整请求url,来源模块首页url,这条数据的url,来源库名称 from 大邑县卫生局数据 where 标题='%s'" % (
                            str(rowC_Va).strip())
                        # SQL = "select 标题,这条数据的完整请求url,来源模块首页url,这条数据的url,来源库名称 from 大邑县卫生局数据 where 标题='%s' and 来源库名称='宣传司>政策文件'" % (
                        #     str(rowC_Va).strip())
                        RS = 链接数据库.getConnect(SQL)[2]
                        # print(RS)
                        keyId = 2
                        if RS != None:
                            # print(RS)
                            标题 = RS[0]
                            完整的URL = RS[1]
                            indexUrl = RS[2]
                            url = RS[3]
                            来源库名称 = RS[4]
                            print(来源库名称)
                            if 来源库名称 !="中华人民共和国国家卫生健康委员会>热点栏目>解读":
                                print("则正在爬取 " + rowC_Va)
                                print(完整的URL)
                                # rowA2 = 'A%s' % (keyId)  # 标题
                                # rowA2_Va = table2[rowA2].value
                                #
                                # rowB2 = 'B%s' % (keyId)  # 标题
                                # rowB2_Va = table2[rowB2].value

                                # cont = parePage(完整的URL)
                                # table2[rowA2] = rowA2_Va
                                # table2[rowB2] = cont
                                # keyId +=1
                        else:
                            print("这不是我的  "+str(rowC_Va))
    data2.save(excelPath2)


    print(keyId)

# 比较excel中超链接的文件名和本地文件
def compareExcelAndFile(Filepath,excelPath):
    data = openpyxl.load_workbook(excelPath)
    active = data.active
    table = data['Sheet1']
    rows = table.max_row
    keyId = 1

    # 获取本地所有相关文件名的完整路径
    FilePathList = seachFilePath(Filepath)
    # 获取本地本地所有相关文件名名称
    FileNameList = eachFileName(Filepath)
    # titleList =['《结核病防治管理办法》修订将于2013年3月24日起实施', '《国家卫生计生委关于做好农村留守儿童健康关爱工作的通知》解读', '《关于进一步加强抗菌药物临床应用管理遏制细菌耐药的通知》解读', '《医师执业注册管理办法》解读', '《国家卫生计生委办公厅关于启用新版无偿献血证的通知》的解读', '《关于临床检验项目管理有关问题的通知》解读', '一图读懂：“互联网+医疗健康”便民惠民活动', '《关于加强公立医院党的建设工作的意见》政策解读', '《食品安全国家标准 植物油》标准等解读材料', '2018年度住院医师规范化培训和助理全科医生培训招收与结业考核工作政策解读', '一图读懂《关于促进“互联网+医疗健康”发展的意见》', '《国家卫生计生委办公厅关于印发感染性疾病相关个体化医学分子检测技术指南和个体化医学检测微阵列基因芯片技术规范的通知》解读', '关于2017年纠正医药购销和医疗服务中不正之风专项治理工作要点的解读', '关于医用耗材专项整治活动方案的解读', '一图读懂|短缺药保障，国家要做这些事', '《医用X射线治疗放射防护要求》解读', '2017年住院医师规范化培训结业考核工作政策解读', '《食品安全国家标准 食品中真菌毒素限量》（GB 2761-2017）及《食品安全国家标准 食品中污染物限量》(GB 2762-2017)解读', '图解食品安全标准与监测评估“十三五”规划（2016-2020年）', '《“十三五”全国结核病防治规划》图解', '关于医学影像诊断中心等独立设置医疗机构基本标准和管理规范解读', '《关于加强心理健康服务的指导意见》一图读懂', '图表：国务院印发《“十三五”卫生与健康规划》', '关于《涉及人的生物医学研究伦理审查办法》的解读', '一图读懂“健康中国2030”规划纲要', '解读：三级和二级妇幼保健院评审标准及实施细则（2016年版）', '《关于促进和规范健康医疗大数据应用发展的指导意见》解读', '国家药品价格谈判有关情况说明', '图解：中医药发展战略规划纲要（2016—2030年）', '《关于妇幼健康服务机构标准化建设与规范化管理的指导意见》及相关文件解读', '图解：进一步改善医疗服务行动计划', '图解：中国卫生应急工作', '人力资源社会保障部和国家卫生计生委联合印发《关于进一步改革完善基层卫生专业技术人员职称评审工作的指导意见》', '《地震灾区预防性消毒卫生要求》解读', '《关于印发传染病信息报告管理规范（2015年版）的通知》文件解读', '图解：我国计划生育工作历程', '图解：“十三五”健康新战略', '《中国癌症防治三年行动计划（2015-2017年）》解读', '图解：中国居民营养与慢性病状况报告（2015年）', '图解：全国精神卫生工作规划（2015—2020年）', '图解：国务院办公厅关于城市公立医院综合改革试点的指导意见', '图解：深化医药卫生体制改革2015年重点工作任务', '图解：深化医药卫生体制改革2014年工作总结', '图解：关于全面推开县级公立医院综合改革的实施意见', '图解：整治“两非”专项行动实施方案', '图解：国务院办公厅转发民政部等部门关于进一步完善医疗救助制度全面开展重特大疾病医疗救助工作意见的通知', '《临床常用生化检验项目参考区间第5部分：血清尿素、肌酐》等4项推荐性卫生行业标准解读', '图解：职业健康检查管理办法(国家卫生和计划生育委员会令第5号)', '图解：卫生计生科技教育工作2014年进展与2015年工作部署', '图解：中国疾病预防控制工作进展（2015年）', '图解：孕产妇健康管理服务', '图解：打击代孕专项行动工作方案', '图解：全国妇幼健康工作的新成绩、新形势与新重点', '图解：认识国家基本公共卫生服务', '消毒产品卫生安全评价规定和消毒产品卫生监督工作规范解读', '白酒产品中塑化剂风险评估结果解读', '《人口健康信息管理办法（试行）》（征求意见稿）解读', '国家卫生计生委副主任王培安就坚持计划生育基本国策启动实施单独两孩政策答记者问', '国家卫生计生委通知严禁医疗机构及其人员推销宣传母乳代用品', '卫生计生委回应社会抚养费征收管理有关问题', '国家卫生计生委决定开展卫生计生监督执法专项稽查', '国家卫生计生委就《涉及人体的医学科学技术研究管理办法》公开征求意见', '国家卫生计生委发布食品安全国家标准《食品生产通用卫生规范》（GB14881-2013）', '国家卫生计生委“三定”规定答问', '卫生计生委规范连续肾脏替代治疗技术管理工作', '《精神卫生法》宣传要点及相关解释', '《职业病诊断与鉴定管理办法》解读', '《食品中污染物限量》（GB2762-2012）问答', '关于《职业病分类和目录》调整的答问', '卫生部等6部门联合印发《高值医用耗材集中采购工作规范（试行）》', '《结核病防治管理办法（修订征求意见稿）》编写说明', '关于禁止餐饮服务单位采购、贮存和使用亚硝酸盐的说明', '关于《中国吸烟危害健康报告》的答问', '《托儿所幼儿园卫生保健工作规范》修订说明', '关于《托儿所幼儿园卫生保健工作规范》的答问', '《关于推进新型农村合作医疗支付方式改革工作的指导意见》问答', '《抗菌药物临床应用管理办法》有关问题答疑', '《关于商业保险机构参与新型农村合作医疗经办服务的指导意见》问答', '卫生部批准紫甘薯色素等9种食品添加剂', '卫生部公布硼酸等301种食品包装材料用添加剂名单', '食用燕窝中亚硝酸盐知识问答', '卫生部发布《食品营养强化剂使用标准》(GB 14880-2012）', '全国消除麻疹和消除疟疾工作会议暨中国全球基金结核病和疟疾项目启动会在贵阳召开', '卫生部监督局关于开展卫生监督专项稽查工作的通知', '卫生部办公厅关于开展医用辐射防护监测网试点工作的通知', '2009年卫生统计公报数据解读', '预防接种知识热点问题答问材料（续）', '“特殊管理药品培训项目”核心图形寓意诠释', '有关负责人就建立国家基本药物制度答问', '卫生部办公厅关于征求《电子病历基本架构与数据标准（征求意见稿）》意见的通知', '深化医药卫生体制改革部际协调工作小组负责人负责人就医改方案征求意见稿答问', '卫生部、教育部印发《医学教育临床实践管理暂行规定》', '卫生部印发《乡村医生考核办法》', '卫生部“三定”规定公布', '《汶川地震灾区疾病预防控制对口支援工作意见》印发', '卫生部印发《世界卫生组织人体细胞、组织和器官移植指导原则（草案）》', '卫生部印发埃博拉出血热等6种传染病预防控制指南和临床诊疗方案', '卫生部、国家发改委发布2008～2010年正电子发射型断层扫描仪配置规划', '采供血机构从业人员要实行岗位培训考核制度', '卫生部疾病预防控制局负责人和流感防治专家接受中国政府网专访谈流行性感冒的防治', '重性精神疾病监管治疗项目开始实施', '卫生部疾病预防控制局和中国疾病预防控制中心发布中国慢性病报告', '卫生部公布2005年“礼来杯”健康传播使者暨精神健康传播使者评选结果', '2005年全国十大卫生新闻今日揭晓', '佘靖副部长：做好卫生标准工作?促进卫生事业发展《卫生政务通报》第22期']
#

    # for row in range(2200, rows+1):
    # for row in range(2500, rows+1):
    for row in range(1, rows+1):

        print("正在读取第："+str(row)+"的数据")
        rowC = 'C%s' % (row)  # 标题
        rowC_Va = table[rowC].value
        # print(rowC_Va)

        rowJ = 'J%s' % (row)  # 全文
        rowJ_Va = table[rowJ].value

        rowK = 'K%s' % (row)  # 全文
        rowK_Va = table[rowK].value
        print(1)
        rsA = re.findall(r'<a href="(.*?)"(.*?)>(.*?)</a>', rowJ_Va)
        print(1.1)
        if rsA !=[] :
            print(2)
            print("这是第几行  "+ str(row))
            for A in rsA:
                print(row)
                print(rowC_Va)
                print(A)
                # 替换掉相关链接
                if str(A[0]).find("shtml") != -1 or str(A[0]) == str(A[2]) or str(A[0]).find("htm") != -1 or str(
                        A[0]).find(
                        "html") != -1 or "http://"+str(A[2]) == str(A[0]) :
                    rowJ_Va = rowJ_Va.replace(r'<a href="%s"%s>%s</a>' % (str(A[0]), str(A[1]), str(A[2])),
                                              "%s" % (str(A[2])))
            table[rowJ] = rowJ_Va
            print("已经处理了该条数据" + str(rowC_Va))
            print(rowJ_Va)
        else:
            print(3)
            pass

    data.save(excelPath)





Filepath = r'F:\卫计局\卫计局附件'
# fileList = seachFile(Filepath)
# print(fileList)
excelPath1 = 'E:\Python\PyCharm\project\project1\卫计局\(20181031).xlsx'
excelPath2 = 'E:\Python\PyCharm\project\project1\卫计局\(110).xlsx'
readExcelFile(Filepath,excelPath1,excelPath2)
# parePage('')

# 获取本地所有相关文件名的完整路径
# FilePathList = seachFilePath(Filepath)
# 获取本地本地所有相关文件名名称
# FileNameList = eachFileName(Filepath)