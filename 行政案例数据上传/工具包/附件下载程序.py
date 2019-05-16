import requests
import re
import os, os.path,shutil
# 参数说明：
#       url 下载地址
#       adjunct_name 附件名字



def download_data(url, adjunct_name, save_path):
        mkdir(save_path)
        header = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML,  like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        print("这条数据存在附件，可能会很大，请稍等，已经自动开始下载.....")
        # rs = re.findall(re.compile(r'http://www.(.*?).pdf|PDF|doc|DOC|docx|DOCX|xlsx|XLSX|xls|XLS'),  url)
        # 说明这一条完整的网址，并且是一个附件的下载地址

        if str(url).find("http://")!=-1:
            # print("不等于空")
            download_ur_1 = url
            # download_ur_1_1 = download_ur_1 + ".png"
        # 说明需要拼接的地址
        else:
             print("附件地址有问题，请看下"+str(url))
        print("下载地址"+str(download_ur_1))

        # 现在开始使用浏览器头部中的  Content-Type 属性来判断文件的类型
        """
        现在已经知道两种类型，一种是gif，一种excel（可以保存为xls或者xlsx，只验证过一次，来自与http://www.hnwsjsw.gov.cn/channels/458.shtml）
         # 'Content-Type': 'image/gif',
         # 'Content-Type': 'application/vnd.ms-excel'
        """
        head = requests.get(download_ur_1).headers  # 返回的是一个字典形式
        adj_type = head['Content-Type']
        adj_hz = re.findall('.*?(pdf|docx|doc|excel|rar|zip|jpeg|jpg|png|gif|txt|7z|gz)', str(adj_type))

        # 从下载地址的后缀去提取附件是那种类型
        download_ur_2 = download_ur_1[download_ur_1.rfind("."):]
        rs_doc_1 = re.findall(re.compile(r'.*?.doc',  re.I),  download_ur_2)
        rs_doc_2 = re.findall(re.compile(r'.*?.docx',  re.I),  download_ur_2)
        rs_pdf = re.findall(re.compile(r'.*?.pdf',  re.I),  download_ur_2)
        rs_xlsx = re.findall(re.compile(r'.*?.xlsx',  re.I),  download_ur_2)
        rs_xls = re.findall(re.compile(r'.*?.xls',  re.I),  download_ur_2)
        rs_zip = re.findall(re.compile(r'.*?.zip',  re.I),  download_ur_2)
        rs_rar = re.findall(re.compile(r'.*?.rar',  re.I),  download_ur_2)
        re_jpg = re.findall(re.compile(r'.*?.jpg',  re.I),  download_ur_2)
        re_png = re.findall(re.compile(r'.*?.png',  re.I),  download_ur_2)
        # re_png = re.findall(re.compile(r'.*?.png',  re.I),  download_ur_2)
        re_jpeg = re.findall(re.compile(r'.*?.jpeg',  re.I),  download_ur_2)
        re_gif = re.findall(re.compile(r'.*?.gif',  re.I),  download_ur_2)
        re_exe = re.findall(re.compile(r'.*?.exe',  re.I),  download_ur_2)
        re_txt = re.findall(re.compile(r'.*?.txt',  re.I),  download_ur_2)
        re_7z = re.findall(re.compile(r'.*?.7z',  re.I),  download_ur_2)
        re_gz = re.findall(re.compile(r'.*?.gz',  re.I),  download_ur_2)

        # 下载word文档
        try:
            if re_gz :
                print("这是一个gz")
                adjunct_name = adjunct_name
                # 防止类似于信用河南上面图片匹配出来的名字不带有后缀
                if adjunct_name.rfind(".gz") == -1:
                    adjunct_name = adjunct_name+".gz"
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                
                public_down(download_ur_1, save_path)
                # print(download_ur_1)
                # try:
                #     r = requests.get(download_ur_1,  headers=header)
                #     with open(save_path,  "wb") as f:
                #         f.write(r.content)
                #     f.close()
                # except:
                #     pass

            if re_7z:
                print("这是一个7z")
                adjunct_name = adjunct_name
                if adjunct_name.rfind(".7z") == -1:
                    adjunct_name = adjunct_name+".7z"
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                public_down(download_ur_1, save_path)

            if re_txt:
                print("这是一个txt")
                adjunct_name = adjunct_name
                if adjunct_name.rfind(".txt") == -1:
                    adjunct_name = adjunct_name+".txt"
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                public_down(download_ur_1, save_path)

            if re_gif:
                print("这是一个gif")
                adjunct_name = adjunct_name
                if adjunct_name.rfind(".gif") == -1:
                    adjunct_name = adjunct_name+".gif"
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                public_down(download_ur_1, save_path)

            if re_jpeg:
                print("这是一个jpeg")
                adjunct_name = adjunct_name
                if adjunct_name.rfind(".jpeg") == -1:
                    adjunct_name = adjunct_name+".jpeg"
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                public_down(download_ur_1, save_path)

            if re_exe:
                print("这是一个exe")
                adjunct_name = adjunct_name
                if adjunct_name.rfind(".exe") == -1:
                    adjunct_name = adjunct_name+".exe"
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                public_down(download_ur_1, save_path)

            if rs_doc_1:
                print("这是一个rs_doc_1")
                adjunct_name = adjunct_name
                if adjunct_name.rfind(".doc") == -1:
                    adjunct_name = adjunct_name+".doc"
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                public_down(download_ur_1, save_path)

            if rs_doc_2:
                print("这是一个rs_doc_2")
                adjunct_name = adjunct_name
                if adjunct_name.rfind(".docx") == -1:
                    adjunct_name = adjunct_name+".docx"
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                public_down(download_ur_1, save_path)

            # 下载pdf文档
            elif rs_pdf:
                print("这是一个pdf")
                adjunct_name = adjunct_name
                if adjunct_name.rfind(".pdf") == -1:
                    adjunct_name = adjunct_name+".pdf"
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                print(download_ur_1)
                public_down(download_ur_1, save_path)

            # 下载xls文件
            elif rs_xlsx:
                print("这是一个rs_xlsx")
                adjunct_name = adjunct_name
                if adjunct_name.rfind(".xlsx") == -1:
                    adjunct_name = adjunct_name+".xlsx"
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                public_down(download_ur_1, save_path)

            elif rs_xls:
                print("这是一个rs_xls")
                adjunct_name = adjunct_name
                if adjunct_name.rfind(".xls") == -1:
                    adjunct_name = adjunct_name+".xls"
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                public_down(download_ur_1, save_path)
             


            # 下载zip文件
            elif rs_zip:
                print("这是一个rs_zip")
                adjunct_name = adjunct_name
                if adjunct_name.rfind(".zip") == -1:
                    adjunct_name = adjunct_name+".zip"
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                public_down(download_ur_1, save_path)

            # 下载rar文件
            elif rs_rar:
                print("这是一个rs_rar")
                adjunct_name = adjunct_name
                if adjunct_name.rfind(".rar") == -1:
                    adjunct_name = adjunct_name+".rar"
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                public_down(download_ur_1, save_path)

            # 下载jpg或者png图片
            elif re_jpg:
                print("这是一张图片：jpg")
                adjunct_name = adjunct_name
                if adjunct_name.rfind(".jpg") == -1:
                    adjunct_name = adjunct_name+".jpg"
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                public_down(download_ur_1, save_path)

            elif re_png:
                print("这是一张图片：png")
                adjunct_name = adjunct_name
                if adjunct_name.rfind(".png") == -1:
                    adjunct_name = adjunct_name+".png"
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                public_down(download_ur_1, save_path)
            else:
                raise  Exception("未匹配出这种格式！！！！")
        except:
            pass


# 这种方法是用于下载的具体的方法，没有传入header，不知道为什么，再有的时候传入header之后下载下来的文件存在问题 ：http://xxgk.hainan.gov.cn/qhxxgk/wtj/201901/P020190114624769074502.xls
def public_down(url, save_path):
    # try:
    r = requests.get(url)
    with open(save_path, "wb") as f:
        f.write(r.content)
    # f.close()
    # except:
    #     pass
# 创建目录
def mkdir(path):
    # 去除首位空格
    path = path.strip()

    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path+"创建成功")
    else:
        print(path+"目录已存在")
#http://xxgk.hainan.gov.cn/qhxxgk/hbj/201811/P020181129666759970247.pdf
# http://xxgk.hainan.gov.cn/qhxxgk/wtj/201901/P020190114624769074502.xls
# ad = "知识产权局/政策法规/政策法规解读"
# save_path = r"E:\datafolder\\" + ad.replace("/", '\\')
# download_data('http://www.cnipa.gov.cn/tz/2017nqgzldlrzgkscjwtjd.pdf', 'nqgzldlrzgkscjwtjd.pdf',save_path)