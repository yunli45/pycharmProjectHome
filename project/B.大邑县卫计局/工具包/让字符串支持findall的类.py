class super_str(str):
    def __init__(self, arg):
        super(super_str, self).__init__()
        self.body = arg

    def findall(self, arg, start=0):
        body = self.body
        result = []
        while True:
            pos = body.find(arg, start)
            if pos >= 0:
                result.append(pos)
                start = pos + len(arg)
                # body = body[pos+len(arg):]
                continue
            break
        return result




s = super_str('indexUrl = "http://www.nhfpc.gov.cn/zwgk/jdjd/ejlist_2.shtml"')
print(s.findall('/'))


