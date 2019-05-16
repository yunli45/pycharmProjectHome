import requests
import re

def DownloadData(adjunct,SavePath,baseUrl):
    if adjunct:
        header = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        print("这条数据存在附件，可能会很大，请稍等，已经自动开始下载.....")
        for i in adjunct:
            print(i)
            rsDocuniqueSign = i[0]  # 附件标签中的url地址
            rsDocName = i[1]        # 附件的名i在
            xiaZai = str(i)
            # 提取附件是那种类型
            rsDoc1 = re.findall(re.compile(r'.*?.doc', re.I), xiaZai)
            rsDoc2 = re.findall(re.compile(r'.*?.docx', re.I), xiaZai)
            rsPdF = re.findall(re.compile(r'.*?.pdf', re.I), xiaZai)
            rsXlsx = re.findall(re.compile(r'.*?.xlsx', re.I), xiaZai)
            rsXls = re.findall(re.compile(r'.*?.xlsx', re.I), xiaZai)
            rsZip = re.findall(re.compile(r'.*?.zip', re.I), xiaZai)
            rsRar = re.findall(re.compile(r'.*?.rar', re.I), xiaZai)
            reJpg = re.findall(re.compile(r'.*?.jpg|png', re.I), xiaZai)
            rePng = re.findall(re.compile(r'.*?.png', re.I), xiaZai)

            # 下载word文档
            try:
                if rsDoc1 :
                    rsDocName = rsDocName+"doc"
                    rsDocName = rsDocName.replace("/", '_')

                    SavePath = SavePath % (rsDocName)

                    if rsDocuniqueSign.find("http") == -1:
                        rsDocuniqueSign = "%s" % (baseUrl) + rsDocuniqueSign
                    else:
                        rsDocuniqueSign = rsDocuniqueSign
                    # print(rsDocuniqueSign)
                    try:
                        r = requests.get(rsDocuniqueSign, headers=header, timeout=30)
                        with open(SavePath, "wb") as f:
                            f.write(r.content)
                        f.close()
                    except:
                        pass
                if rsDoc2 :
                    rsDocName = rsDocName+"docx"
                    rsDocName = rsDocName.replace("/", '_')

                    SavePath = SavePath % (rsDocName)

                    if rsDocuniqueSign.find("http") == -1:
                        rsDocuniqueSign = "%s" % (baseUrl) + rsDocuniqueSign
                    else:
                        rsDocuniqueSign = rsDocuniqueSign
                    # print(rsDocuniqueSign)
                    try:
                        r = requests.get(rsDocuniqueSign, headers=header, timeout=30)
                        with open(SavePath, "wb") as f:
                            f.write(r.content)
                        f.close()
                    except:
                        pass
                # 下载pdf文档
                elif rsPdF:
                    rsDocName = rsDocName + ".PDF"
                    rsDocName = rsDocName.replace("/", '_')
                    SavePath = SavePath % (rsDocName)

                    if rsDocuniqueSign.find("http") == -1:
                        rsDocuniqueSign = baseUrl + rsDocuniqueSign
                    else:
                        rsDocuniqueSign = rsDocuniqueSign
                    # print(rsDocuniqueSign)
                    r = requests.get(rsDocuniqueSign,header)
                    with open(SavePath, "wb") as f:
                        f.write(r.content)
                    f.close()

                # 下载xls文件
                elif rsXlsx:
                    rsDocName = rsDocName+".xlsx"
                    rsDocName = rsDocName.replace("/", '_')
                    SavePath = SavePath % (rsDocName)

                    if rsDocuniqueSign.find("http") == -1:
                        rsDocuniqueSign = baseUrl + rsDocuniqueSign
                    else:
                        rsDocuniqueSign = rsDocuniqueSign

                    # print(rsDocuniqueSign)
                    r = requests.get(rsDocuniqueSign, header)
                    with open(SavePath, "wb") as f:
                        f.write(r.content)
                    f.close()
                elif rsXls:
                    rsDocName = rsDocName+'.xls'
                    rsDocName = rsDocName.replace("/", '_')
                    SavePath = SavePath % (rsDocName)

                    if rsDocuniqueSign.find("http") == -1:
                        rsDocuniqueSign = baseUrl + rsDocuniqueSign
                    else:
                        rsDocuniqueSign = rsDocuniqueSign

                    # print(rsDocuniqueSign)
                    r = requests.get(rsDocuniqueSign, header)
                    with open(SavePath, "wb") as f:
                        f.write(r.content)
                    f.close()

                # 下载zip文件
                elif rsZip:
                    rsDocName = rsDocName + ".zip"
                    rsDocName = rsDocName.replace("/", '_')
                    SavePath = SavePath % (rsDocName)

                    if rsDocuniqueSign.find("http") == -1:
                        rsDocuniqueSign = baseUrl + rsDocuniqueSign
                    else:
                        rsDocuniqueSign = rsDocuniqueSign

                    # print(rsDocuniqueSign)
                    r = requests.get(rsDocuniqueSign, header)
                    with open(SavePath, "wb") as f:
                        f.write(r.content)
                    f.close()

                # 下载rar文件
                elif rsRar:
                    rsDocName = rsDocName + ".rar"
                    rsDocName = rsDocName.replace("/", '_')
                    SavePath = SavePath % (rsDocName)

                    if rsDocuniqueSign.find("http") == -1:
                        rsDocuniqueSign = baseUrl + rsDocuniqueSign
                    else:
                        rsDocuniqueSign = rsDocuniqueSign

                    # print(rsDocuniqueSign)
                    r = requests.get(rsDocuniqueSign, header)
                    with open(SavePath, "wb") as f:
                        f.write(r.content)
                    f.close()

                # 下载jpg或者png图片
                elif reJpg:
                    rsDocName = rsDocName + ".jpg"
                    rsDocName = rsDocName.replace("/", '_')
                    SavePath = SavePath % (rsDocName)

                    if rsDocuniqueSign.find("http") == -1:
                        rsDocuniqueSign = "%s" % (baseUrl) + rsDocuniqueSign
                    else:
                        rsDocuniqueSign = rsDocuniqueSign
                    # print(rsDocuniqueSign)
                    r = requests.get(rsDocuniqueSign,header, timeout=30)
                    with open(SavePath, "wb") as f:
                        f.write(r.content)
                    f.close()
                elif rePng:
                    rsDocName = rsDocName + ".png"
                    rsDocName = rsDocName.replace("/", '_')
                    SavePath = SavePath % (rsDocName)

                    if rsDocuniqueSign.find("http") == -1:
                        rsDocuniqueSign = "%s" % (baseUrl) + rsDocuniqueSign
                    else:
                        rsDocuniqueSign = rsDocuniqueSign
                    # print(rsDocuniqueSign)
                    r = requests.get(rsDocuniqueSign, header, timeout=30)
                    with open(SavePath, "wb") as f:
                        f.write(r.content)
                    f.close()
            except:
                pass


