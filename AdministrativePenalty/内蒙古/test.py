# coding:utf-8
import re
list1 = [('/cms/info/preview.jsp?SiteID=lhqzf&amp;ColumnID=88&amp;KeyID=20180816105720502428983', '巴彦淖尔市虹燕粮油批发部', '2018-08-16'), ('/cms/info/preview.jsp?SiteID=lhqzf&amp;ColumnID=88&amp;KeyID=20180816110341342689181', '巴彦淖尔市临河区家家欢日用百货店', '2018-08-16'), ('/cms/info/preview.jsp?SiteID=lhqzf&amp;ColumnID=88&amp;KeyID=20180816111043747372199', '巴彦淖尔市临河区红爵烟酒零售店', '2018-08-16'), ('/cms/info/preview.jsp?SiteID=lhqzf&amp;ColumnID=88&amp;KeyID=20180816111902226459070', '巴彦淖尔市临河区春雨烤吧', '2018-08-16'), ('/cms/info/preview.jsp?SiteID=lhqzf&amp;ColumnID=88&amp;KeyID=20180816112140945904167', '巴彦淖尔市临河区伊味儿零食店', '2018-08-16'), ('/cms/info/preview.jsp?SiteID=lhqzf&amp;ColumnID=88&amp;KeyID=20180816152111881114227', '巴彦淖尔市临河区果蔬宝生活便利店', '2018-08-16'), ('/cms/info/preview.jsp?SiteID=lhqzf&amp;ColumnID=88&amp;KeyID=20180816152534751421893', '巴彦淖尔市恒泰烟酒经销店', '2018-08-16'), ('/cms/info/preview.jsp?SiteID=lhqzf&amp;ColumnID=88&amp;KeyID=20180815090854929190738', '临河区发展和改革局 “双随机”抽查工作实施细则', '2018-08-02'), ('/cms/info/preview.jsp?SiteID=lhqzf&amp;ColumnID=88&amp;KeyID=20180814162617437464283', '内蒙古自治区巴彦淖尔市临河区人民医院', '2018-07-27'), ('/cms/info/preview.jsp?SiteID=lhqzf&amp;ColumnID=88&amp;KeyID=20180814171434865193560', '联邦制药（内蒙古）有限公司', '2018-07-27'), ('/cms/info/preview.jsp?SiteID=lhqzf&amp;ColumnID=88&amp;KeyID=20180814172125806767468', '内蒙古巴彦淖尔市迅驰新能源有限公司', '2018-07-27'), ('/cms/info/preview.jsp?SiteID=lhqzf&amp;ColumnID=88&amp;KeyID=20180815103954430105357', '巴彦淖尔市临河区信义工程机械租赁部', '2018-07-27'), ('/cms/info/preview.jsp?SiteID=lhqzf&amp;ColumnID=88&amp;KeyID=20180815104628903127569', '临河区富兴水泥制品厂', '2018-07-27'), ('/cms/info/preview.jsp?SiteID=lhqzf&amp;ColumnID=88&amp;KeyID=20180815105406068153668', '内蒙古芸驰商贸有限公司', '2018-07-27'), ('/cms/info/preview.jsp?SiteID=lhqzf&amp;ColumnID=88&amp;KeyID=20180815105940149998577', '巴彦淖尔市华泰拆迁有限公司', '2018-07-27')]
# list2= []
# for n in  list1:
#     list2.append(n)
# print(len(list1))
# print(list2)
# for i in list2:
#     title = i[1]
#     if title.find("店")!=-1:
#         list1.remove(i)
# print(list1 )
# print(len(list1))
str1 ="""
<div class="zwxw_nr_title2">
<!-- 
					<h4>人体胎盘倒卖事件经报道后，北京妇产医院立即成立调查小组对医院胎盘管理情况进行了调查管理情况进行了调查管理情况进行了调查</h4>
					<div style=" width:auto; margin:0 auto;">
						<img src="/sites/lhqzf/images/img_11.jpg" style="text-align:center">
					</div>
				 -->
<div style="float:left;width:832px; text-align:left;">
<p style="text-indent:43px;line-height:36px"><strong><span style="font-size:21px;font-family:仿宋_GB2312">第一条</span></strong><span style="font-size:21px;font-family:仿宋"> </span><span style="font-size: 21px;font-family:仿宋_GB2312">为贯彻自治区、市、区政府的决策部署，进一步转变监管理念，创新监管方式，提升监管效能，规范市场执法行为。根据《内蒙古自治区人民政府办公厅关于印发自治区推广随机抽查规范事中事后监管实施方案的通知》精神，结合发改部门职能实际，制定本细则。</span></p><p style="text-indent:43px;line-height:36px"><strong><span style="font-size:21px;font-family:仿宋_GB2312">第二条</span></strong><strong><span style="font-size:21px;font-family:仿宋"> </span></strong><span style="font-size:21px;font-family:仿宋_GB2312">“双随机”抽查工作是发改部门依据价格法律、法规规定，按照级别和属地管辖原则，随机抽取检查对象，随机选派执法检查人员，并将随机抽查工作全流程公开的监管方式。</span></p><p style="text-indent:43px;line-height:36px"><strong><span style="font-size:21px;font-family:仿宋_GB2312">第三条</span></strong><strong><span style="font-size:21px;font-family:仿宋"> </span></strong><span style="font-size:21px;font-family:仿宋_GB2312">各价格行政执法人员应认真履行所担负的监管任务，严格遵守依法行政及相关制度规定要求，按照分工负责、协调配合、各负其责的原则，依法进行抽查监管。</span></p><p style="text-indent:43px;line-height:36px"><strong><span style="font-size:21px;font-family:仿宋_GB2312">第四条</span></strong><strong><span style="font-size:21px;font-family:仿宋"> </span></strong><span style="font-size:21px;font-family:仿宋_GB2312">制定公布随机抽查事项清单。随机抽查事项必须以法律法规为依据，并及时根据法律法规修订情况和简政放权工作实际进行动态调整更新公布。随机抽查事项清单由检查所按照职责分工，根据法律法规及上级主管部门要求，及时以书面形式报告进行调整公布。</span></p><p style="text-indent:43px;line-height:36px"><strong><span style="font-size:21px;font-family:仿宋_GB2312">第五条</span></strong><strong><span style="font-size:21px;font-family:仿宋"> </span></strong><span style="font-size:21px;font-family:仿宋_GB2312">建立价格执法抽查人员名录库。价格执法人员库应录入执法抽查人员的基础信息，包括姓名、性别、联系方式和执法证号码等，并根据价格执法资格证管理相关规定，实行动态管理，对执法人员有变动的适时进行更新公布。</span></p><p style="text-indent:43px;line-height:36px"><strong><span style="font-size:21px;font-family:仿宋_GB2312">第六条</span></strong><span style="font-size:21px;font-family:仿宋"> </span><span style="font-size: 21px;font-family:仿宋_GB2312">建立随机抽查市场主体名录库。按照行政区域划分和级别管辖权限要求，建立本级随机抽查市场主体名录库，条件成熟的也可进一步建立区分不同行业领域，满足不同执法需求的随机抽查市场主体名录库。市场主体名录库实行动态更新，由检查所根据简政放权和上级要求等及时提供更新公布。</span></p><p style="text-indent:43px;line-height:36px"><strong><span style="font-size:21px;font-family:仿宋_GB2312">第七条</span></strong><span style="font-size:21px;font-family:仿宋"> </span><span style="font-size: 21px;font-family:仿宋_GB2312">建立“双随机”抽查机制。根据公布的随机抽查清单、市场主体名录库和执法人员名录库，在开展抽查前，通过抽签、摇号等形式，确定随机抽查的市场主体对象和执法抽（检）查人员。抽查过程应书面记录，并经现场参加人员签字后存档。</span></p><p style="text-indent:43px;line-height:36px"><strong><span style="font-size:21px;font-family:仿宋_GB2312">第八条</span></strong><span style="font-size:21px;font-family:仿宋"> </span><span style="font-size: 21px;font-family:仿宋_GB2312">随机抽查方式。开展随机抽查，可以根据监管工作需要，采取比例抽查和条件抽查方式。比例抽查是指在检查对象数量较大、相似度较高的情况下，选定百分比进行抽查。条件抽查是指按照抽查依据的要求设定检查对象的类型、行业、性质等条件进行抽查。比例抽查和条件抽查可以结合应用，提高执法效率。</span></p><p style="text-indent:43px;line-height:36px"><strong><span style="font-size:21px;font-family:仿宋_GB2312">第九条</span></strong><strong><span style="font-size:21px;font-family:仿宋"> </span></strong><span style="font-size:21px;font-family:仿宋_GB2312">合理确定随机抽查的比例和频次。要根据当地经济、社会发展和监管领域实际情况，合理确定随机抽查的比例和频次，既要保证必要的抽查覆盖面和工作力度，又要防止检查过多和执法扰民。对于法律法规规章有规定的，按规定实施；法律法规规章没有规定的，随机抽查比例原则上不低于辖区内市场主体的5%，抽查频次原则上每年不少于2次。可根据抽查主体数量和抽查事项繁杂程度，作适当调整。对投诉举报多、列入经营异常名录或有严重违法违规记录等情况的市场主体，要加大随机抽查力度。</span></p><p style="text-indent:43px;line-height:36px"><strong><span style="font-size:21px;font-family:仿宋_GB2312">第十条</span></strong><strong><span style="font-size:21px;font-family:仿宋"> </span></strong><span style="font-size:21px;font-family:仿宋_GB2312">加强抽查结果运用。实行“一抽查一通报”制度，检查所对抽查结果的合法性、准确性和及时性负责，自抽查结束之日起20个工作日内向社会公示。抽查情况及查处结果按相关部门规定要求录入并提交向社会公示，接受社会监督，形成有效震慑，增强市场主体守法的自觉性。对抽查检查中发现不属于本部门职责范围的违法行为，按照要求应当及时把违法线索移送相应部门依法处理。</span></p><p style="text-indent:43px;line-height:36px"><strong><span style="font-size:21px;font-family:仿宋_GB2312">第十一条</span></strong><span style="font-size:21px;font-family:仿宋"> </span><span style="font-size: 21px;font-family:仿宋_GB2312">开展专项检查和联合抽查。根据工作需要，配合上级部门开展专项检查和联合抽查。同时，按照区政府的统一部署，与有关部门开展联合抽查，共同制定并实施联合抽查计划，依照各自职责处理检查发现的问题，互通执法结果，形成执法合力。</span></p><p style="text-indent:43px;line-height:36px"><strong><span style="font-size:21px;font-family:仿宋_GB2312">第十二条</span></strong><span style="font-size:21px;font-family:仿宋"> </span><span style="font-size: 21px;font-family:仿宋_GB2312">强化责任落实。各有关股所室要根据本实施细则，各司其职、相互配合，对随机抽查事项、抽查的情况和结果等及时通过门户网站等平台向社会公开；价格执法人员要严格依法行政，自觉遵守各项规定，确保此项工作落到实处，取得实效。</span></p><p style="text-indent:43px;line-height:36px"><strong><span style="font-size:21px;font-family:仿宋_GB2312">第十三条</span></strong><span style="font-size:21px;font-family:仿宋"> </span><span style="font-size: 21px;font-family:仿宋_GB2312">本实施细则自发布之日起施行。</span></p><p style="line-height:22px"><span style="font-size:21px;font-family:仿宋"> </span></p><p style="line-height:22px"><span style="font-size:21px;font-family:仿宋">                                                          </span></p><p style="line-height:22px"><span style="font-size: 21px; font-family: 仿宋_GB2312;">                                                                                             临河区发展和改革局</span><span style="font-size: 21px; font-family: 仿宋;">  </span><span style="font-size: 21px; font-family: 仿宋_GB2312;">   </span></p><p style="text-align:center;line-height:22px">                                                                                                  </p><p style="line-height: 22px;"><span style="font-size: 21px;">                                                                                                  2016</span><span style="font-size: 21px; font-family: 宋体;">年</span><span style="font-size: 21px;">12</span><span style="font-size: 21px; font-family: 宋体;">月</span><span style="font-size: 21px;">14</span><span style="font-size: 21px; font-family: 宋体;">日</span><span style="font-size: 21px;"> </span></p><p><br/></p></div>


"""

if str1.find("许可机关")!=-1:
    print("yes")
else:
    print("No")