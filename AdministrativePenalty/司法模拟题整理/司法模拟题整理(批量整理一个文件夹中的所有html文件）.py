#coding=utf-8
import re
from bs4 import BeautifulSoup
import openpyxl
import  os

class ProcessData(object):
    # 获取某个路径下的全部文件加入到一个list中去
    def __init__(self):
        str ="用来闹着玩玩的，嘻嘻 ==---==="
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

# StemLabel
    def Process(self, SavePath=None,file_dir=None,SheetName=None,BigTitleLabel=None,BigTitleLabelSpecies=None,BigTitleLabelSpeciesName=None,TestTypeLabe= None,TestTypeLabeSpecies=None,TestTypeLabeSpeciesName=None,source=None,ProvenanceTime=None,StemLabel=None,StemLabelSpecies=None,StemLabelSpeciesName=None,SmallStemLabel=None,SmallStemLabelSpecies=None,SmallStemLabelSpeciesName=None,SmallTitleLabel=None,SmallTitleLabelSpecies=None,SmallLabelSpeciesName=None,OptionsA=None,OptionsB=None,OptionsC=None,OptionsD=None,Answer=None,ScoreParsingLabel=None,ScoreParsingLabelSpecies=None,ScoreParsingLabelSpeciesName=None,Score=None):

        files = self.file_name(file_dir)
        data = openpyxl.load_workbook(SavePath)
        active = data.active
        table = data[SheetName]
        tableId = 2
        for file in files:
            print("正在处理："+file)
            filePath = file_dir + "\\"+file
            with open(filePath, 'r', encoding='utf-8',errors='ignore') as f:
                s = f.read()
                # print(s)
                Soup1 = BeautifulSoup(s, 'lxml')
                Soup = Soup1.findAll(BigTitleLabel, attrs={BigTitleLabelSpecies: BigTitleLabelSpeciesName})
                TitleSoup = Soup1.findAll(TestTypeLabe, attrs={TestTypeLabeSpecies: TestTypeLabeSpeciesName})
                考试种类 = TitleSoup[-1].text.strip()
                来源 =source
                出处时间 =ProvenanceTime
                出处目录 = re.sub('分类.*', '', 考试种类).replace("司法", '')  # 自动在目录中提取

                for Content in Soup:
                    SoupContent = BeautifulSoup(str(Content), 'lxml')
                    TitleSoup = SoupContent.findAll(StemLabel, attrs={StemLabelSpecies:StemLabelSpeciesName}) # 每道大题题干的标签，包含了整个大题的所有内容
                    单选多选 = TitleSoup[-1].text.strip()
                    if 单选多选.find("单项")!=-1:
                        单选多选 = '单选题'
                    elif 单选多选.find("多项")!=-1:
                        单选多选 = '多选题'
                    else:
                        print("还不知道是什么题型")
                    print("大题目的种类"+单选多选)
                    每道题的所有选项和答案和分值与解析 = SoupContent.findAll( SmallStemLabel, attrs={SmallStemLabelSpecies:SmallStemLabelSpeciesName}) # 每道小题题干的标签，包含了该小题的所有内容

                    每道题的题目 = SoupContent.findAll(SmallTitleLabel, attrs={SmallTitleLabelSpecies: SmallLabelSpeciesName})  # 每道小题的题目标签

                    选项A = re.findall(re.compile(OptionsA), str(每道题的所有选项和答案和分值与解析))
                    选项B = re.findall(re.compile(OptionsB), str(每道题的所有选项和答案和分值与解析))
                    选项C = re.findall(re.compile(OptionsC), str(每道题的所有选项和答案和分值与解析))
                    选项D = re.findall(re.compile(OptionsD), str(每道题的所有选项和答案和分值与解析))
                    答案 = re.findall(re.compile(Answer), str(每道题的所有选项和答案和分值与解析))

                    分值与解析 = SoupContent.findAll(ScoreParsingLabel, attrs={ScoreParsingLabelSpecies:ScoreParsingLabelSpeciesName})
                    分值 = re.findall(re.compile(Score), str(分值与解析))
                    print("分值的长度是不是对应相应html文件个数是否相等"+str(len(分值)))
                    print("每个题干的分值"+str(分值))
                    for ids, x in enumerate(每道题的题目):
                        table['A%s' % (tableId)] = 考试种类  # 考试种类
                        table['C%s' % (tableId)] = 来源  # 来源
                        table['D%s' % (tableId)] = 单选多选  # 单选多选
                        table['E%s' % (tableId)] = 出处时间  # 出处1
                        table['F%s' % (tableId)] = 出处目录  # 出处2
                        # table['G%s' % (tableId)] = 每道题的题目[ids].text.strip()  # 需要题干包含题号时取消注释，记得注释下面的两行
                        每道题的题目1= re.sub('.*. ','',每道题的题目[ids].text.strip())
                        table['G%s' % (tableId)] = 每道题的题目1  # 题干
                        # table['H%s' % (tableId)] = 分值[ids].replace(":", '')  # 分值  暂时不需要，需要的时候取消注释就好了

                        table['I%s' % (tableId)] = 答案[ids]  # 答案
                        # table['J%s' % (tableId)] = 选项A[ids]  # 选项A  需要选项包含A B C D 的时候取消注释
                        选项A1 = re.sub('A ', '', 选项A[ids])
                        table['J%s' % (tableId)] = 选项A1  # 选项A

                        # table['K%s' % (tableId)] = 选项B[ids]  # 选项B
                        选项B1 = re.sub('B ', '', 选项B[ids])
                        table['K%s' % (tableId)] = 选项B1  # 选项B

                        # table['L%s' % (tableId)] = 选项C[ids]  # 选项C
                        选项C1 = re.sub('C ', '', 选项C[ids])
                        table['L%s' % (tableId)] = 选项C1  # 选项C

                        # table['M%s' % (tableId)] = 选项D[ids]  # 选项D
                        选项D1 = re.sub('D ', '', 选项D[ids])
                        table['M%s' % (tableId)] = 选项D1  # 选项C
                        # if 每道题的题目1.find("A")!=-1 and 每道题的题目1.find("B")!=-1 and 每道题的题目1.find("C")!=-1 and 每道题的题目1.find("D")!=-1 :


                        tableId += 1

        data.save(SavePath)

if __name__ =="__main__":
    # 参数说明
   # 注意： 需要提前先建好保存数据的表格
    #SavePath：保存处理后相应xls文件的路径   file_dir：是每卷文件所在的目录（比如卷一 这个目录下有很多相应的卷一的试卷）  SheetName :保存处理后舒徐需要插入到的xls文件中那个Sheet的名字，
    SavePath = r'E:\Python\PyCharm\project\AdministrativePenalty\司法模拟题整理\司法考试模拟题卷二.xlsx'
    file_dir = r'E:\基本软件\QQ\qq数据\787190277\FileRecv\萌小子下载-司考模拟题\卷二'
    SheetName = '选择题'

    # 这组是包含每道大题的描述相应标签（一般是div）：包含该大题下所有的小题的题目、选项、答案、解析、分值。
    # BigTitleLabel :包含每道大题的相应标签（一般是div）  BigTitleLabelSpecies ：包含每道大题的相应标签的种类（一般是class或者ID）BigTitleLabelSpeciesName :包含每道大题的相应标签的种类的唯一名字（class的值或者id的值）
    BigTitleLabel = 'div'
    BigTitleLabelSpecies ='class'
    BigTitleLabelSpeciesName ='SubType'

    # 相应考试种类的标签：可提取考试的种类  ，TestTypeLabe：该标签的种类（div) TestTypeLabeSpecies:该标签的定位方式（class 或者id） TestTypeLabeSpeciesName ：该标签的种类的唯一名字（class的值或者id的值）
    TestTypeLabe = 'div'
    TestTypeLabeSpecies = 'class'
    TestTypeLabeSpeciesName = 'mTitle'

    # source：来源（模拟题、真题），手动指定，全文不能判断出来   ProvenanceTime：出处时间，手动指定全文判断不出来
    source = '模拟题'
    ProvenanceTime ='2018年'

    # 这组是大题的题干：单项选择题、多项选择题（注意:目前只有这两种，后面还有其他的修改代码）
    StemLabel =  'div'
    StemLabelSpecies='class'
    StemLabelSpeciesName = 'SubTypeDesc'

    #这组是每道小题题干的标签，包含了该小题的所有内容：包括该小题的选项、答案、分值
    SmallStemLabel = 'div'
    SmallStemLabelSpecies = 'class'
    SmallStemLabelSpeciesName = 'Qst'


    # 这组是每道小题的题目，用于提取题目
    SmallTitleLabel = 'div'
    SmallTitleLabelSpecies = 'class'
    SmallLabelSpeciesName  = 'SubDesc'

    # 提取每道小题选项的正则表达式
    OptionsA=r'<input.*?value="1"/>(A.*?)<'
    OptionsB=r'<input.*?value="2"/>(B.*?)<'
    OptionsC=r'<input.*?value="3"/>(C.*?)<'
    OptionsD=r'<input.*?value="4"/>(D.*?)<'
    # 提取每道小题答案的正则表达式
    Answer =r'<span class="da">答案:</span>(.*?)<br/></div>'

    # 这组用于提取分值与解析的标签
    ScoreParsingLabel = 'div'
    ScoreParsingLabelSpecies = 'class'
    ScoreParsingLabelSpeciesName = 'Solution null'
    # 提取分值
    Score = r'>该题您未回答:х</span>    该问题分值(.*?)</span><div class="Answer">'


    ProcessData = ProcessData()
    ProcessData.Process(SavePath,file_dir,SheetName,BigTitleLabel,BigTitleLabelSpecies,BigTitleLabelSpeciesName,TestTypeLabe,TestTypeLabeSpecies,TestTypeLabeSpeciesName,source,ProvenanceTime,StemLabel,StemLabelSpecies,StemLabelSpeciesName,SmallStemLabel,SmallStemLabelSpecies,SmallStemLabelSpeciesName,SmallTitleLabel,SmallTitleLabelSpecies,SmallLabelSpeciesName,OptionsA,OptionsB,OptionsC,OptionsD,Answer,ScoreParsingLabel,ScoreParsingLabelSpecies,ScoreParsingLabelSpeciesName,Score)

