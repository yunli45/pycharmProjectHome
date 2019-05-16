def findll(arg ,arg1, start=0):
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
    print(result)
    return result

src = "../../zwgk/jdjd/201809/9eb3f794162046a3a9305f5bd1fe9cc4.shtml"
indexUrl = "http://www.nhfpc.gov.cn/zwgk/jdjd/ejlist_2.shtml"
findll(src,"/")





