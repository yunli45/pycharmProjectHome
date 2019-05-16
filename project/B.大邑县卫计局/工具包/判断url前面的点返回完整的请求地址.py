import re
from 大邑县卫计局.工具包 import 附件下载程序
class returnSRC(object):
    def __init__(self):
        pass
    def findalls(self,arg ,arg1, start=0):
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

    def returnSrc(self,indexUrl,src,contentSrc):
        print("1")
        print("首页"+indexUrl)
        print("自己的"+src)
        print("全文的"+contentSrc)
        # http://www.nhfpc.gov.cn/caiwusi/s7785/201705/0eb5d499c0b9495a9f53bc48c6f2c0a0.shtml
        # "/ewebeditor/uploadfile/2017/05/20170531111020489.doc">卫生计生行业经济管理领军人才培养计划实施方案（2017版）</a>
        # http://www.nhfpc.gov.cn   +  /ewebeditor/uploadfile/2017/05/20170531111020489.doc
        if src[0] =="/":
            print("w")
            rsList = self.findalls(indexUrl, "/")
            print(rsList)
            src1 = src
            wholeSrc = indexUrl[:rsList[2]] + src1
            print(wholeSrc)
        # 地址前面以“.”开始的， ../  、../../、./
        elif src[0] ==".":
            if len(self.findalls(src,"../../")) ==1:
                print("2")
                rsList = self.findalls(indexUrl,"/")
                src1 = src[self.findalls(src,'../')[-1]+3:]
                print(src1)
                wholeSrc =indexUrl[:rsList[2]+1]+  src1

            if len(self.findalls(src,"../")) ==1:
                print("3")
                rsList = self.findalls(indexUrl,"/")
                src1 = src[self.findalls(src,'../')[-1]+3:]
                wholeSrc =indexUrl[:rsList[2]+1]+  src1

            # 假如本身就是一个完整的地址就不需要转化
            if len(self.findalls(src,"http://")) ==1:
                print("4")
                wholeSrc =src
        # 地址是第一个字符不是“.”、“/”，是一个字符,就需要传一个这条数据的完整访问地址
        # http://www.nhfpc.gov.cn/caiwusi/s7788c/201003/a48f6211ebce4aa79c0af9c85649fa42.shtml
        #                                               a48f6211ebce4aa79c0af9c85649fa42/files/d04520a311b646dda4c5c4a0a0d21875.xls
        # http://www.nhfpc.gov.cn/caiwusi/s7788c/201003/ + a48f6211ebce4aa79c0af9c85649fa42/files/d04520a311b646dda4c5c4a0a0d21875.xls
        else:
            wholeSrc = contentSrc[:contentSrc.rfind("/")+1] +src

        # if len(self.findalls(src,"./")) ==1:
        #     rsList = self.findalls(indexUrl,"/")
        #     src1 = src[self.findalls(src,'../')[-1]+2:]
        #     wholeSrc =indexUrl[:rsList[-3]+1]+  src1
        #     print(wholeSrc)
        return wholeSrc
    # 判断src地址是不是一个附件的地址，是附件就下载
    # def decideSrc(self,src):
    #     # rss = re.findall(re.compile(r'http://www.*?html|http://www.*?htm|http://www.*?shtml|http://www.*?shtm'),src)
    #     Rs = re.findall(re.compile(r'.*?.pdf|PDF|doc|DOC|docx|DOCX|xlsx|XLSX|xls|XLS'), src)
    #     if src.find("http://") != -1 or Rs != []:
    #         # 网址是一个http形式的
    #         if src.find("http://") != -1:
    #             Rs1 = re.findall(re.compile(r'.*?(pdf|PDF|doc|DOC|docx|DOCX|xlsx|XLSX|xls|XLS)'), src)
    #             # 先判断这条数据完整的网址是否是附件
    #             # 这条数据是一个附件
    #             if Rs1 != []:
    #                 suffix = "." + Rs1[0]
    #                 附件下载程序.DownloadData(src, '', title, SavePath)
    #                 Content = '<a href="/photo/img/%s%s">%s</a>' % (title, suffix, title)
    #                 来源处唯一标志_url = src
    #                 来源处完整的url = src
    #             # 这条数据存在跳转，跳转后怎么取标签
    #             else:
    #                 pass
    #
    #
    #
    #     pass

src = "/ewebeditor/uploadfile/2017/05/20170531111020489.doc"
indexUrl = "http://www.nhfpc.gov.cn/caiwusi/s7785/201705/0eb5d499c0b9495a9f53bc48c6f2c0a0.shtml"
# # returnSRC().findalls(src,"../")
print(returnSRC().returnSrc(indexUrl,src,''))