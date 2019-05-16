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
        # 地址前面以“.”开始的， ../  、../../、./、../../../
        elif src[0] ==".":
            if len(self.findalls(src,"./")) ==1:
                # print("这是。/形式的")
                rsList = self.findalls(indexUrl,"/")
                src1 = src[self.findalls(src,'./')[-1]+2:]
                wholeSrc =indexUrl[:rsList[-1]+1]+  src1
                # print("这是。/形式的返回地址为"+str(wholeSrc))

            if len(self.findalls(src,"../../../")) ==1:
                # print("这是。。/。。/。。/形式的")
                rsList = self.findalls(indexUrl,"/")
                src1 = src[self.findalls(src,'../')[-1]+3:]
                wholeSrc =indexUrl[:rsList[2]+1]+  src1
                # print("这是。。/。。/。。/形式的返回地址为"+str(wholeSrc))
            if len(self.findalls(src,"../../")) ==1:
                # print("这是../../形式的返回地址为")
                rsList = self.findalls(indexUrl,"/")
                src1 = src[self.findalls(src,'../')[-1]+3:]
                wholeSrc =indexUrl[:rsList[2]+1]+  src1
                # print("这是../../形式的返回地址为" + str(wholeSrc))
            # if len(self.findalls(src,"../")) ==1:
            #     # print("这是../形式的返回地址为" )
            #     rsList = self.findalls(indexUrl,"/")
            #     src1 = src[self.findalls(src,'../')[-1]+3:]
            #     wholeSrc =indexUrl[:rsList[2]+1]+  src1
            #     # print("这是../形式的返回地址为" + str(wholeSrc))

            """  标准文本使用 
            """
            if len(self.findalls(src,"../")) ==1:
                print("这是../形式的返回地址为" )
                rsList = self.findalls(indexUrl,"/")
                print("rsList"+str(rsList))
                src1 = src[self.findalls(src,'../')[-1]+3:]
                wholeSrc =indexUrl[:rsList[-2]+1]+  src1
                # print("这是../形式的返回地址为" + str(wholeSrc))



        # 地址是第一个字符不是“.”、“/”，是一个字符,就需要传一个这条数据的完整访问地址
        # http://www.nhfpc.gov.cn/caiwusi/s7788c/201003/a48f6211ebce4aa79c0af9c85649fa42.shtml
        #                                               a48f6211ebce4aa79c0af9c85649fa42/files/d04520a311b646dda4c5c4a0a0d21875.xls
        # http://www.nhfpc.gov.cn/caiwusi/s7788c/201003/ + a48f6211ebce4aa79c0af9c85649fa42/files/d04520a311b646dda4c5c4a0a0d21875.xls

        # 假如本身就是一个完整的地址就不需要转化
        elif  len(self.findalls(src,"http://")) ==1:
                print("4")
                wholeSrc =src
        else:
            wholeSrc = contentSrc[:contentSrc.rfind("/")+1] +src

        # if len(self.findalls(src,"./")) ==1:
        #     rsList = self.findalls(indexUrl,"/")
        #     src1 = src[self.findalls(src,'../')[-1]+2:]
        #     wholeSrc =indexUrl[:rsList[-3]+1]+  src1
        #     print(wholeSrc)
        print("最终的返回地址为"+str(wholeSrc))
        return wholeSrc


# src = "../jcffbz/200910/t20091010_162150.shtml"
# indexUrl = "http://kjs.mee.gov.cn/hjbhbz/bzwb/shjbh/index.shtml"
# "http://www.mee.gov.cn/gkml/sthjbgw/qt/201712/t20171229_428952.htm"
# "http://www.mee.gov.cn/gkml/sthjbgw/qt/201805/t20180504_435974.htm"
# # returnSRC().findalls(src,"../")
# print(returnSRC().returnSrc(indexUrl,src,''))