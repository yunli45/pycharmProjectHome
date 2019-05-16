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

    def returnSrc(self, indexUrl, src, contentSrc):
        if src[0] == "/":
            print("w")
            rsList = self.findalls(indexUrl, "/")
            src1 = src
            wholeSrc = indexUrl[:rsList[2]] + src1
            # print(wholeSrc)
        # 地址前面以“.”开始的， ../  、../../、./
        elif src[0] == ".":
            # if len(self.findalls(src, "../../")) == 1:
            if src[:6] == '../../':
                rsList = self.findalls(indexUrl, "/")
                src1 = src[self.findalls(src, '../')[-1]+3:]
                wholeSrc =indexUrl[:rsList[2]+1] + src1

            else:
                # if len(self.findalls(src, "../")) == 1:
                if src[:3] == '../':
                    rsList = self.findalls(indexUrl, "/")
                    src1 = src[self.findalls(src, '../')[-1]+3:]
                    wholeSrc = indexUrl[:rsList[2]+1] + src1

                # if len(self.findalls(src, "./")) == 1:
                if src[:2] == './':
                    rsList = self.findalls(indexUrl, "/")
                    src1 = src[self.findalls(src, './')[-1]+2:]
                    wholeSrc = indexUrl[:rsList[-1]+1] + src1

                # 假如本身就是一个完整的地址就不需要转化
                if len(self.findalls(src, "http://")) ==1:
                    print("4")
                    wholeSrc = src

        else:
            wholeSrc = contentSrc[:contentSrc.rfind("/")+1] + src

        return wholeSrc

# src = "/shenyfh/108074/108127/108208/3657761/2018110517581658194.xls"
# indexUrl = "http://shenyang.pbc.gov.cn/shenyfh/108074/108127/108208/8267/index2.html"
# returnSRC().findalls(src,"../")
# print(returnSRC().returnSrc(indexUrl,src,''))