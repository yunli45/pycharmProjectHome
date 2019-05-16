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

    """
        参数说明：
            indexUrl ： 首页地址 http://www.hnwsjsw.gov.cn/
            src ：首页提取该条数据的地址
            contentSrc ： 这条数据全文访问地址,如果是首页的取出来就是一个附件那么直接将这页的地址传递过来
        返回参数：
            wholeSrc ： 返回最终的附件下载地址或者全文访问地址
        Html中相对路径:
        ../”表示上一级目录开始。

        “./”表示当前同级目录开始。
        
        “/”表示根目录开始。
        
         ../../ ：代表文件所在的父级目录的父级目录
        https://zhidao.baidu.com/question/502217922767387244.html
        https://baijiahao.baidu.com/s?id=1606046350230601762&wfr=spider&for=pc
    """
    def returnSrc(self, indexUrl, src, contentSrc):
        if indexUrl[-1] != "/":
            indexUrl = indexUrl+"/"
        if indexUrl == contentSrc:
            contentSrc = indexUrl
        if src[0] == "/":
            print("w")
            rsList = self.findalls(indexUrl, "/")
            src1 = src
            wholeSrc = indexUrl[:rsList[2]] + src1
            # print(wholeSrc)
        # 地址前面以“.”开始的， ../  、../../、./
        elif src[0] == ".":

            #  貌似和 ../../../ 是一样的  参照：http://www.mee.gov.cn/gzfw_13107/zcfg/zcfgjd/index.shtml
            if src[:6] == '../../':
                # print(222)
                rsList = self.findalls(contentSrc, "/")
                src1 = src[self.findalls(src, '../')[-1]+3:]
                wholeSrc =contentSrc[:rsList[-3]+1] + src1
                # print(wholeSrc)
            else:

                # if src[:3] == '../':
                #     # print("333")
                #     rsList = self.findalls(indexUrl, "/")
                #     src1 = src[self.findalls(src, '../')[-1]+3:]
                #     wholeSrc = indexUrl[:rsList[-2]+1] + src1

                if src[:3] == '../':
                    # print("333")
                    rsList = self.findalls(contentSrc, "/")
                    src1 = src[self.findalls(src, '../')[-1]+3:]
                    wholeSrc = contentSrc[:rsList[-2]+1] + src1
                    # print(wholeSrc)

                """
                如果附件是以 。/ 来的，那么附件的下载地址就是本条数据页面最后一个反斜杠后面替换为附件的地址
                网页数据url: http://xxgk.hainan.gov.cn/qhxxgk/wtj/201901/t20190114_3062489.htm
                附件：<a href="./P020190114624769074502.xls">海南省琼海市-_行政处罚(2018.12月份).xls</a>
                附件下载地址 ： http://xxgk.hainan.gov.cn/qhxxgk/wtj/201901/P020190114624769074502.xls
                """
                #

                # if src[:2] == './':
                #     # print(444)
                #     rsList = self.findalls(indexUrl, "/")
                #     src1 = src[self.findalls(src, './')[-1]+2:]
                #     wholeSrc = indexUrl[:rsList[-1]+1] + src1

                if src[:2] == './':
                    # print(444)

                    rsList = self.findalls(contentSrc, "/")
                    src1 = src[self.findalls(src, './')[-1] + 2:]
                    wholeSrc = contentSrc[:rsList[-1] + 1] + src1
                    # print(wholeSrc)

        # 假如本身就是一个完整的地址就不需要转化
        elif len(self.findalls(src, "http://")) == 1:
            print("4")
            wholeSrc = src

        # 遇到一种 附件中src没有任何的前缀，src第一个反斜杠前面和本条数据最后的内容一样，就是以这条数据的访问地址去除掉 点（.）的内容。
        # index-src =http://www.nhc.gov.cn/wjw/zcjd/list.shtml   一图读懂：医疗卫生机构厕所整洁专项行动 
        # consrc = http://www.nhc.gov.cn/guihuaxxs/s7786/201903/c39908ea135d4216b7d343f66605962b.shtml
        # a标签src = c39908ea135d4216b7d343f66605962b/images/aaf79e3397c7430f809e1511ba7dc504.jpg
        # 正确的下载地址 = http://www.nhc.gov.cn/guihuaxxs/s7786/201903/c39908ea135d4216b7d343f66605962b/images/aaf79e3397c7430f809e1511ba7dc504.jpg
        else:
            consrc_adj = contentSrc[contentSrc.rfind("/") + 1:contentSrc.rfind(".")]
            src_1 = src[:src.find("/")]
            # 如果这条数据的访问地址中最后一个反斜杠后边到后缀（.shtml .html等网页的后缀）等于a标签第一个反斜杠之前的内容，且a标签第一个字符不是反斜杠 或者./ ../ http 等
            if consrc_adj == src_1:
                wholeSrc = contentSrc[:contentSrc.rfind("/") + 1] + src
            else:
                raise Exception("遇到了前所未有的地址，之前没有遇到过，请自行查看并添加这种地址的拼接情况")
        return wholeSrc

# http://kjs.mee.gov.cn/hjbhbz/sywbzgz/
# http://kjs.mee.gov.cn/hjbhbz/sywbzgz/201005/P020110307496397939031.pdf
# src = "../xxgk2018/xxgk/xxgk15/201904/t20190405_698738.html"
# indexUrl = "http://www.mee.gov.cn"
# cont = "http://www.mee.gov.cn/gzfw_13107/zcfg/zcfgjd/index.shtml"
# print(returnSRC().returnSrc(indexUrl,src,cont))




"""
拼接规则来源（目前只有 ’/‘这种情况还没被证实，但是在以前的记录中现在的规则是完全正确的）
十三五
首页： http://kjs.mee.gov.cn/hjbhbz/sywbzgz/index.shtml
取值：./201005/P020110307496397939031.pdf
实际    http://kjs.mee.gov.cn/hjbhbz/sywbzgz/201005/P020110307496397939031.pdf
		http://kjs.mee.gov.cn/hjbhbz/sywbzgz/201005/P020110307496397939031.pdf


取值： ../bzgl/200707/t20070717_106824.shtml
实际： http://kjs.mee.gov.cn/hjbhbz/bzgl/200707/t20070717_106824.shtml
	   http://kjs.mee.gov.cn/hjbhbz/bzgl/200707/t20070717_106824.shtml
       http://kjs.mee.gov.cn/bzgl/200707/t20070717_106824.shtml

地方环境
首页：http://kjs.mee.gov.cn/hjbhbz/dfhjbhbzba/index.shtml
取值：./201807/t20180711_446455.shtml
实际：http://kjs.mee.gov.cn/hjbhbz/dfhjbhbzba/201807/t20180711_446455.shtml


标准管理：
首页：http://kjs.mee.gov.cn/hjbhbz/bzgl/index_1.shtml
取值：./201308/t20130820_257705.shtml
实际：http://kjs.mee.gov.cn/hjbhbz/bzgl/201308/t20130820_257705.shtml


政策法规解读
首页：http://www.mee.gov.cn/gzfw_13107/zcfg/zcfgjd/index.shtml
取值：../../../xxgk2018/xxgk/xxgk15/201812/t20181210_683948.html
实际：http://www.mee.gov.cn/xxgk2018/xxgk/xxgk15/201812/t20181210_683948.html


"""