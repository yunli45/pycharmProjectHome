import re

def img(content, save_path):
    annex_local_url = save_path[save_path.find("datafolder")-1:-2].replace("\\", "/")
    all_img = re.findall('<img.*?src=".*?".*?>', content)
    if all_img:
        for img in all_img:
            picture = re.findall('<img.*?src=".*?(jpeg|jpg|png|gif)".*?>', img)
            if picture:
                rs_img = re.findall('<img.*?src="(.*?)".*?>', img)
                img_hyper = rs_img[0]
                img_annex_name = img_hyper[img_hyper.rfind("/") + 1:]

                # 下载图片
                # img_download_url = 判断url前面的点返回完整的请求地址.returnSRC().returnSrc(page_url, img_hyper, content_src)
                # img_download_url = 判断url前面的点返回完整的请求地址.returnSRC().returnSrc(content_src, img_hyper, content_src)
                # 附件下载程序.download_data(img_download_url, img_annex_name, save_path)

                # 替换图片链接
                old_img = img
                new_img = '<img src="{0}">'.format(annex_local_url + img_annex_name)  # 新的img标签
                content = content.replace(old_img, new_img)  # 替换
            else:
                print("这个img标签不是附件，是跳转" + str(img) + "\n" + "\n")
                old_img = img
                new_img1 = ''
                content = content.replace(old_img, new_img1)
    print(content)
# content = """<img id="obj" src="/eportal/fileDir/lyszjj/template/common/head/1-3.png" width="650" height="300" border="0">"""
# save_path = "E:\行政案例附件\datafolder\湖南省\浏阳市-住建\%s"
# img(content, save_path)



def src(page_url):
    for page_no in range(1, 516):
        src_list, date_list, title_list = [], [], []
        if page_no == 1:
            page_url_1 = page_url
        else:
            page_url_1 = page_url[:page_url.rfind(".")] + "_" + str(page_no) + ".jhtml"
        print(page_url_1)

src("http://218.76.40.80:9000/hnxyfw/xzcf/index.jhtml")




# title = "浏森公林行决字[2017]第0174号"
# rs_book_num = re.findall('.*?\d号', title)
# if rs_book_num != []:
#     book_number = title
# else:
#     book_number = ''
# print(book_number)