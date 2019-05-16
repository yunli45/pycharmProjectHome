import requests
import re
from J湖南省.工具包 import 动态访问

# 参数说明：第一个url是每条数据从首页取出来的地址，有的地址一取出来就是个http可以访问的下载地址，有的就是一个地址需要基础地址去拼接为完整的访问地址，附件在其全文中（注意：有可能附件的下载地址是其访问地址最后一个/ 加上相应a标签中的url）
#  title 用于将保存相应附件的名字, 取附件超链接最后一个反斜杠后面的字符串


def download_data(url, adjunct_name, save_path):

        header = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML,  like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        print("这条数据存在附件，可能会很大，请稍等，已经自动开始下载.....")
        # rs = re.findall(re.compile(r'http://www.(.*?).pdf|PDF|doc|DOC|docx|DOCX|xlsx|XLSX|xls|XLS'),  url)
        # 说明这一条完整的网址，并且是一个附件的下载地址

        if str(url).find("http://")!=-1:
            print("不等于空")
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
                print("这是一个txt")
                adjunct_name = adjunct_name
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path % (adjunct_name)
                # print(download_ur_1)
                try:
                    r = requests.get(download_ur_1,  headers=header)

                    with open(save_path,  "wb") as f:
                        f.write(r.content)
                    f.close()
                except:
                    pass

            if re_7z:
                print("这是一个txt")
                adjunct_name = adjunct_name
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path % (adjunct_name)
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
                save_path = save_path % (adjunct_name)
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
                save_path = save_path % (adjunct_name)
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
                save_path = save_path % (adjunct_name)
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
                save_path = save_path % (adjunct_name)
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
                save_path = save_path % (adjunct_name)
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
                save_path = save_path % (adjunct_name)
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
                save_path = save_path % (adjunct_name)
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
                save_path = save_path % (adjunct_name)
                # print(download_ur_1)
                r = requests.get(download_ur_1,  header)
                with open(save_path,  "wb") as f:
                    f.write(r.content)
                f.close()

            elif rs_xls:
                print("这是一个rs_xls")
                adjunct_name = adjunct_name
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path % (adjunct_name)
                # print(download_ur_1)
                r = requests.get(download_ur_1,  header)
                rs = 动态访问.get_index_page(download_ur_1)
                with open(save_path,  "wb") as f:
                    f.write(r.rs)
                f.close()

            # 下载zip文件
            elif rs_zip:
                print("这是一个rs_zip")
                adjunct_name = adjunct_name
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path % (adjunct_name)
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
                save_path = save_path % (adjunct_name)
                # print(download_ur_1)
                r = requests.get(download_ur_1,  header)
                with open(save_path,  "wb") as f:
                    f.write(r.content)
                f.close()

            # 下载jpg或者png图片
            elif re_jpg:
                adjunct_name = adjunct_name
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path % (adjunct_name)
                # print(download_ur_1)
                r = requests.get(download_ur_1, header)
                with open(save_path,  "wb") as f:
                    f.write(r.content)
                f.close()

            elif re_png:
                adjunct_name = adjunct_name
                adjunct_name = adjunct_name.replace("/",  '_')
                save_path = save_path % (adjunct_name)
                # print(download_ur_1)
                r = requests.get(download_ur_1,  header)
                with open(save_path,  "wb") as f:
                    f.write(r.content)
                f.close()
        except:
            pass



# imgDownLoad("http://www.sipo.gov.cn/images/content/2018-08/20180827075011376131.jpg", "20180827075011376131.jpg", "F:\知识产权\%s")



