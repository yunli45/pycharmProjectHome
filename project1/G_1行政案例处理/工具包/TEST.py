import re

content = """

<p>各地在执行中遇到的问题，请及时反馈我站工程质量监督科，联系人：王劲宏，<a name="_GoBack"></a>联系电话：0771-5881296，电子邮箱：gxzljd@126.com。</p><br/>
<p>
<p>附件：《住房城乡建设部关于印发工程质量安全手册（试行）的通知》（建质〔2018〕95号）<img border="0" src="/webeditnew/sysimage/icon16/pdf.gif"><a href="/datafolder/行政案例数据/广西建设网文件通知/20181123170122277.pdf" >住房城乡建设部关于印发工程质量安全手册（试行）的通知.pdf</a></p><br/>

"""
# def dispose_of_img_gif_label_1(content):
content = str(content)
rs = re.findall(r'<img.*? src=".*?.gif".*?>', content)
print(rs)