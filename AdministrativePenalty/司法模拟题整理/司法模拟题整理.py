#coding=utf-8
import re
from bs4 import BeautifulSoup
import openpyxl
import  os

class ProcessData(object):
    # 获取某个路径下的全部文件加入到一个list中去
    def __init__(self):
        str =1
    def file_name(self,file_dir=None):
        print(file_dir)
        for root, dirs, files in os.walk(file_dir):
            # print(root)  # 当前目录路径
            # print("前路径下所有非目录子文件："+str(files))  # 当前路径下所有非目录子文件
            files =files
            # print(dirs)  # 当前路径下所有子目录
            # dirs = dirs
        # print(files)
        return files

   # 参数说明 SavePath：保存处理后相应xls文件的路径   file_dir：是每卷文件所在的目录（比如卷一 这个目录下有很多相应的卷一的试卷）
   # SheetName :保存处理后的xls文件中那个Sheet的名字

    def Process(self, SavePath=None,file_dir=None,):

        files = self.file_name(file_dir)
        data = openpyxl.load_workbook(SavePath)
        active = data.active
        table = data['选择题']
        tableId = 2
        for file in files:
            print("正在处理："+file)
            filePath = file_dir + "\\"+file
            with open(filePath, 'r', encoding='utf-8',errors='ignore') as f:
                s = f.read()
                # print(s)
                Soup1 = BeautifulSoup(s, 'lxml')
                Soup = Soup1.findAll('div', attrs={'class': 'SubType'})
                TitleSoup = Soup1.findAll('div', attrs={'class': 'mTitle'})
                考试种类 = TitleSoup[-1].text.strip()
                来源 = '模拟题'
                出处1 = '2018'
                出处2 = re.sub('分类.*', '', 考试种类).replace("司法", '')

                for Content in Soup:
                    SoupContent = BeautifulSoup(str(Content), 'lxml')
                    TitleSoup = SoupContent.findAll('div', attrs={'class': 'SubTypeDesc'})
                    单选多选 = TitleSoup[-1].text.strip()
                    print("大题目的种类"+单选多选)
                    每道题的所有选项和答案和分值与解析 = SoupContent.findAll('div', attrs={'class': 'Qst'})
                    每道题的题目 = SoupContent.findAll('div', attrs={'class': 'SubDesc'})
                    选项A = re.findall(re.compile(r'<input.*?value="1"/>(A.*?)<'), str(每道题的所有选项和答案和分值与解析))
                    选项B = re.findall(re.compile(r'<input.*?value="2"/>(B.*?)<'), str(每道题的所有选项和答案和分值与解析))
                    选项C = re.findall(re.compile(r'<input.*?value="3"/>(C.*?)<'), str(每道题的所有选项和答案和分值与解析))
                    选项D = re.findall(re.compile(r'<input.*?value="4"/>(D.*?)<'), str(每道题的所有选项和答案和分值与解析))
                    答案 = re.findall(re.compile(r'<span class="da">答案:</span>(.*?)<br/></div>'), str(每道题的所有选项和答案和分值与解析))
                    分值与解析 = SoupContent.findAll('div', attrs={'class': 'Solution null'})
                    分值 = re.findall(re.compile(r'>该题您未回答:х</span>    该问题分值(.*?)</span><div class="Answer">'), str(分值与解析))
                    print("分值的长度是不是对应相应html文件个数是否相等"+len(分值))
                    print("每个题干的分值"+分值)
                    for ids, x in enumerate(每道题的题目):
                        table['A%s' % (tableId)] = 考试种类  # 考试种类
                        table['C%s' % (tableId)] = 来源  # 来源
                        table['D%s' % (tableId)] = 单选多选  # 单选多选
                        table['E%s' % (tableId)] = 出处1  # 出处1
                        table['F%s' % (tableId)] = 出处2  # 出处2
                        table['G%s' % (tableId)] = 每道题的题目[ids].text.strip()  # 题干
                        # table['H%s' % (tableId)] = 分值[ids].replace(":", '')  # 分值  暂时不需要，需要的时候取消注释就好了
                        table['I%s' % (tableId)] = 答案[ids]  # 答案
                        table['J%s' % (tableId)] = 选项A[ids]  # 选项A
                        table['K%s' % (tableId)] = 选项B[ids]  # 选项B
                        table['L%s' % (tableId)] = 选项C[ids]  # 选项C
                        table['M%s' % (tableId)] = 选项D[ids]  # 选项D
                        tableId += 1
        data.save(SavePath)

if __name__ =="__main__":
    # ProcessData = ProcessData()
    # ProcessData.file_name(r'E:\基本软件\QQ\qq数据\787190277\FileRecv\萌小子下载-司考模拟题\卷一')
    SavePath = r'E:\Python\PyCharm\project\AdministrativePenalty\司法模拟题整理\司法考试模拟题卷三.xlsx'
    file_dir = r'E:\基本软件\QQ\qq数据\787190277\FileRecv\萌小子下载-司考模拟题\卷三'
    ProcessData = ProcessData()
    ProcessData.Process(SavePath,file_dir)

