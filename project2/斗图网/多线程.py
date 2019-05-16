# coding = utf-8
import requests
import re
import os, os.path,shutil
from bs4 import BeautifulSoup

# 创建目录
def mk_dir(save_path):
    # 去除首位空格
    save_path = save_path.strip()

    # 去除尾部 \ 符号
    save_path = save_path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(save_path)
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(save_path)
        print(save_path + "创建成功")
    else:
        print(save_path + "目录已存在")

def req(url,save_path):
    mk_dir(save_path)
    response = requests.get(url)
    response = response.content.decode('utf-8')
    res_soup = BeautifulSoup(response, 'lxml')
    res_soup = res_soup.find_all("div", attrs={"class": "pic-content"})
    if res_soup:
        rs_list = re.findall("""<img.*?src="(.*?)".*?alt="(.*?)".*?>""", str(res_soup), flags= re.M|re.S)
    if rs_list:
        for ids,i in enumerate(rs_list):
            print(i)
            r = requests.get(str(i[0]))
            save_path_1 = save_path + str(ids) + ".jpg"
            print(save_path_1)
            with open(save_path_1, "wb") as f:
                f.write(r.content)
            f.close()


if __name__ == '__main__':
    url = "https://www.doutula.com/article/detail/7124915"
    save_path = "E:\测试\图片"
    req(url, save_path)