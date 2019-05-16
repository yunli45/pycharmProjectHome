import requests
import sys
import time
file_url = "http://codex.cs.yale.edu/avi/db-book/db4/slide-dir/ch1-2.pdf"

# 屏蔽warning信息，因为下面verify=False会报警告信息
requests.packages.urllib3.disable_warnings()
# verify=False 这一句是为了有的网站证书问题，为True会报错
r = requests.get(file_url, stream=True, verify=False)
length = float(r.headers['content-length'])
print(length)
# 既然要实现下载进度，那就要知道你文件大小啊，下面这句就是得到总大小
total_size = int(r.headers['Content-Length'])
count  = 0
time1 = time.time()
with open("F:\python.pdf", "wb") as f:

    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            f.write(chunk)
            count += len(chunk)
            ############# 花哨的下载进度部分 ###############
            count += len(chunk)
            if time.time() - time1 > 2:
                p = count / length * 100
                speed = (count - count_tmp) / 1024 / 1024 / 2
                count_tmp = count
                print("python" + ': ' + '{:.2f}'.format(p) + '%' + ' Speed: ' + '{:.2f}'.format(speed) + 'M/S')
                time1 = time.time()


 

