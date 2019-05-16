page_url = "http://www.cbrc.gov.cn/chinese/home/docViewPage/60200406&current=1"
for page_no in range(1, 4):
    src_list, company_list, title_list = [], [], []
    if page_no == 1:
        page_url_1 = page_url
    else:
        page_url_1 = page_url[:page_url.rfind("=") + 1] + str(page_no)
    print(page_url_1)