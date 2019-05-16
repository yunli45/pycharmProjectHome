import requests
import re

#参数说明：第一个url是每天数据从首页取出来的地址，有的地址一取出来就是个http可以访问的下载地址，有的就是一个地址需要基础地址去拼接为完整的访问地址，附件在其全文中（注意：有可能附件的下载地址是其访问地址最后一个/ 加上相应a标签中的url）
#  title 用于将保存相应附件的名字
#
def DownloadData(Url,baseUrl,title,SavePath):

        header = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        print("这条数据存在附件，可能会很大，请稍等，已经自动开始下载.....")
        # rs = re.findall(re.compile(r'http://www.(.*?).pdf|PDF|doc|DOC|docx|DOCX|xlsx|XLSX|xls|XLS'), Url)
        # 说明这一条完整的网址，并且是一个附件的下载地址
        adjunctName = title
        if  str(Url).find("http://www.")!=-1 :
            print("不等于空")
            DownLoadUrl = Url
        # 说明需要拼接的地址
        else:
            Url1 = Url.replace("../../",'').replace("../",'').replace("./",'')
            DownLoadUrl = baseUrl+ Url1
        print("下载地址"+ str(DownLoadUrl))
        # 提取附件是那种类型
        rsDoc1 = re.findall(re.compile(r'.*?.doc', re.I), DownLoadUrl)
        rsDoc2 = re.findall(re.compile(r'.*?.docx', re.I), DownLoadUrl)
        rsPdF = re.findall(re.compile(r'.*?.pdf', re.I), DownLoadUrl)
        rsXlsx = re.findall(re.compile(r'.*?.xlsx', re.I), DownLoadUrl)
        rsXls = re.findall(re.compile(r'.*?.xlsx', re.I), DownLoadUrl)
        rsZip = re.findall(re.compile(r'.*?.zip', re.I), DownLoadUrl)
        rsRar = re.findall(re.compile(r'.*?.rar', re.I), DownLoadUrl)
        reJpg = re.findall(re.compile(r'.*?.jpg', re.I), DownLoadUrl)
        rePng = re.findall(re.compile(r'.*?.png', re.I), DownLoadUrl)

        # 下载word文档
        try:
            if rsDoc1 :
                adjunctName = adjunctName+".doc"
                adjunctName = adjunctName.replace("/", '_')
                SavePath = SavePath % (adjunctName)
                # print(DownLoadUrl)
                try:
                    r = requests.get(DownLoadUrl, headers=header)
                    with open(SavePath, "wb") as f:
                        f.write(r.content)
                    f.close()
                except:
                    pass
            if rsDoc2 :
                adjunctName = adjunctName+".docx"
                adjunctName = adjunctName.replace("/", '_')
                SavePath = SavePath % (adjunctName)
                try:
                    r = requests.get(DownLoadUrl, headers=header)
                    with open(SavePath, "wb") as f:
                        f.write(r.content)
                    f.close()
                except:
                    pass
            # 下载pdf文档
            elif rsPdF:
                adjunctName = adjunctName + ".PDF"
                adjunctName = adjunctName.replace("/", '_')
                SavePath = SavePath % (adjunctName)

                # print(DownLoadUrl)
                r = requests.get(DownLoadUrl,header)
                with open(SavePath, "wb") as f:
                    f.write(r.content)
                f.close()

            # 下载xls文件
            elif rsXlsx:
                adjunctName = adjunctName+".xlsx"
                adjunctName = adjunctName.replace("/", '_')
                SavePath = SavePath % (adjunctName)
                # print(DownLoadUrl)
                r = requests.get(DownLoadUrl, header)
                with open(SavePath, "wb") as f:
                    f.write(r.content)
                f.close()
            elif rsXls:
                adjunctName = adjunctName+'.xls'
                adjunctName = adjunctName.replace("/", '_')
                SavePath = SavePath % (adjunctName)
                # print(DownLoadUrl)
                r = requests.get(DownLoadUrl, header)
                with open(SavePath, "wb") as f:
                    f.write(r.content)
                f.close()

            # 下载zip文件
            elif rsZip:
                adjunctName = adjunctName + ".zip"
                adjunctName = adjunctName.replace("/", '_')
                SavePath = SavePath % (adjunctName)
                # print(DownLoadUrl)
                r = requests.get(DownLoadUrl, header)
                with open(SavePath, "wb") as f:
                    f.write(r.content)
                f.close()

            # 下载rar文件
            elif rsRar:
                adjunctName = adjunctName + ".rar"
                adjunctName = adjunctName.replace("/", '_')
                SavePath = SavePath % (adjunctName)
                # print(DownLoadUrl)
                r = requests.get(DownLoadUrl, header)
                with open(SavePath, "wb") as f:
                    f.write(r.content)
                f.close()

            # 下载jpg或者png图片
            elif reJpg:
                adjunctName = adjunctName + ".jpg"
                adjunctName = adjunctName.replace("/", '_')
                SavePath = SavePath % (adjunctName)
                # print(DownLoadUrl)
                r = requests.get(DownLoadUrl,header)
                with open(SavePath, "wb") as f:
                    f.write(r.content)
                f.close()
            elif rePng:
                adjunctName = adjunctName + ".png"
                adjunctName = adjunctName.replace("/", '_')
                SavePath = SavePath % (adjunctName)
                # print(DownLoadUrl)
                r = requests.get(DownLoadUrl, header)
                with open(SavePath, "wb") as f:
                    f.write(r.content)
                f.close()
        except:
            pass

def imgDownLoad(imgUrl,imgName,SavePath):
    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

    reJpg = re.findall(re.compile(r'.*?.jpg', re.I), imgUrl)
    rePng = re.findall(re.compile(r'.*?.png', re.I), imgUrl)
    # 下载jpg或者png图片
    # 如果存在图片就以图片的src最后一个 / 以后的数字或者文字为本地的名字
    try:
        if reJpg or rePng:
            imgName = imgName
            SavePath1 = SavePath % (imgName)
            # print(imgUrl)
            r = requests.get(imgUrl, header)
        with open(SavePath1, "wb") as f:
            f.write(r.content)
        f.close()
    except:
            pass
# imgDownLoad("http://www.sipo.gov.cn/images/content/2018-08/20180827075011376131.jpg","20180827075011376131.jpg","F:\知识产权\%s")



