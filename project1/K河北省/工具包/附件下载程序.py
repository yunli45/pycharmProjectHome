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
        # 说明需要拼接的地址
        else:
             print("附件地址有问题，请看下"+str(url))
        print("下载地址"+str(download_ur_1))
        # 提取附件是那种类型
        rs_doc_1 = re.findall(re.compile(r'.*?.doc',  re.I),  download_ur_1)
        rs_doc_2 = re.findall(re.compile(r'.*?.docx',  re.I),  download_ur_1)
        rs_pdf = re.findall(re.compile(r'.*?.pdf',  re.I),  download_ur_1)
        rs_xlsx = re.findall(re.compile(r'.*?.xlsx',  re.I),  download_ur_1)
        rs_xls = re.findall(re.compile(r'.*?.xls',  re.I),  download_ur_1)
        rs_zip = re.findall(re.compile(r'.*?.zip',  re.I),  download_ur_1)
        rs_rar = re.findall(re.compile(r'.*?.rar',  re.I),  download_ur_1)
        re_jpg = re.findall(re.compile(r'.*?.jpg',  re.I),  download_ur_1)
        re_png = re.findall(re.compile(r'.*?.png',  re.I),  download_ur_1)
        re_jpeg = re.findall(re.compile(r'.*?.jpeg',  re.I),  download_ur_1)
        re_gif = re.findall(re.compile(r'.*?.gif',  re.I),  download_ur_1)
        re_exe = re.findall(re.compile(r'.*?.exe',  re.I),  download_ur_1)
        re_txt = re.findall(re.compile(r'.*?.txt',  re.I),  download_ur_1)
        re_7z = re.findall(re.compile(r'.*?.7z',  re.I),  download_ur_1)
        re_gz = re.findall(re.compile(r'.*?.gz',  re.I),  download_ur_1)

        # 下载word文档
        try:
            if re_gz:
                print("这是一个gz")
                adjunct_name = adjunct_name
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                try:
                    r = requests.get(download_ur_1,  headers=header)
                    with open(save_path,  "wb") as f:
                        f.write(r.content)
                    f.close()
                except:
                    pass

            if re_7z:
                print("这是一个7z")
                adjunct_name = adjunct_name
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                try:
                    r = requests.get(download_ur_1,  headers=header)
                    with open(save_path,  "wb") as f:
                        f.write(r.content)
                    f.close()
                except:
                    pass

            if re_txt:
                print("这是一个txt")
                adjunct_name = adjunct_name
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                try:
                    r = requests.get(download_ur_1,  headers=header)
                    with open(save_path,  "wb") as f:
                        f.write(r.content)
                    f.close()
                except:
                    pass

            if re_gif:
                print("这是一个gif")
                adjunct_name = adjunct_name
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                try:
                    r = requests.get(download_ur_1,  headers=header)
                    with open(save_path,  "wb") as f:
                        f.write(r.content)
                    f.close()
                except:
                    pass

            if re_jpeg:
                print("这是一个jpeg")
                adjunct_name = adjunct_name
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                try:
                    r = requests.get(download_ur_1,  headers=header)
                    with open(save_path,  "wb") as f:
                        f.write(r.content)
                    f.close()
                except:
                    pass

            if re_exe:
                print("这是一个exe")
                adjunct_name = adjunct_name
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                try:
                    r = requests.get(download_ur_1,  headers=header)
                    with open(save_path,  "wb") as f:
                        f.write(r.content)
                    f.close()
                except:
                    pass

            if rs_doc_1:
                print("这是一个rs_doc_1")
                adjunct_name = adjunct_name
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                try:
                    r = requests.get(download_ur_1,  headers=header)
                    with open(save_path,  "wb") as f:
                        f.write(r.content)
                    f.close()
                except:
                    pass

            if rs_doc_2:
                print("这是一个rs_doc_2")
                adjunct_name = adjunct_name
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                try:
                    r = requests.get(download_ur_1,  headers=header)
                    with open(save_path,  "wb") as f:
                        f.write(r.content)
                    f.close()
                except:
                    pass

            # 下载pdf文档
            elif rs_pdf:
                print("这是一个pdf")
                adjunct_name = adjunct_name
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                r = requests.get(download_ur_1, header)
                with open(save_path,  "wb") as f:
                    f.write(r.content)
                f.close()

            # 下载xls文件
            elif rs_xlsx:
                print("这是一个rs_xlsx")
                adjunct_name = adjunct_name
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                r = requests.get(download_ur_1,  header)
                with open(save_path,  "wb") as f:
                    f.write(r.content)
                f.close()

            elif rs_xls:
                print("这是一个rs_xls")
                adjunct_name = adjunct_name
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                r = requests.get(download_ur_1,  header)
                with open(save_path,  "wb") as f:
                    f.write(r.content)
                f.close()

            # 下载zip文件
            elif rs_zip:
                print("这是一个rs_zip")
                adjunct_name = adjunct_name
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                r = requests.get(download_ur_1,  header)
                with open(save_path,  "wb") as f:
                    f.write(r.content)
                f.close()

            # 下载rar文件
            elif rs_rar:
                print("这是一个rs_rar")
                adjunct_name = adjunct_name
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                r = requests.get(download_ur_1,  header)
                with open(save_path,  "wb") as f:
                    f.write(r.content)
                f.close()

            # 下载jpg或者png图片
            elif re_jpg:
                print("这是一张图片：jpg")
                adjunct_name = adjunct_name
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                r = requests.get(download_ur_1, header)
                with open(save_path,  "wb") as f:
                    f.write(r.content)
                f.close()

            elif re_png:
                print("这是一张图片：png")
                adjunct_name = adjunct_name
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path + "\\" + adjunct_name
                # print(download_ur_1)
                r = requests.get(download_ur_1,  header)
                with open(save_path,  "wb") as f:
                    f.write(r.content)
                f.close()
        except:
            pass


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
# download_data('http://www.mee.gov.cn/gkml/hbb/bwj/201704/W020170414581772760139.pdf','W020170414581772760139.pdf','F:\\环保局相关附件\\1004\\“十三五”国家环境保护标准工作\\%s')



# save_path = "E:\行政案例附件\datafolder\河北省\廊坊市"
# url = "http://www.tangshan.gov.cn/u/cms/www/201612/23171426r848.xlsx"
# adjunct_name = "23171426r848.xlsx"
# download_data(url, adjunct_name, save_path)