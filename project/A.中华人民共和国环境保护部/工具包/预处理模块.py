# coding:utf-8
import re
from 中华人民共和国环境保护部.工具包 import 链接数据库,附件下载程序,判断url前面的点返回完整的请求地址
from bs4 import BeautifulSoup
# 演示文章
str1 ="""
<div class="TRS_Editor"><p align="center"><font face="楷体,楷体_GB2312">单志广 国家信息中心信息化研究部副主任 中国智慧城市发展研究中心秘书长 </font></p> <p>2015年8月19日，国务院总理李克强主持召开国务院常务会议，通过《<a href="http://zfs.mee.gov.cn/fg/gwyw/201509/t20150917_309927.htm">关于促进大数据发展的行动纲要</a>》（以下简称《行动纲要》）。9月5日，《国务院关于印发促进大数据发展行动纲要的通知》（国发〔2015〕50 号）正式发布，在全社会引起广泛影响。《行动纲要》由国家发展改革委牵头，会同工业和信息化部，自2014年初开展前期研究，历经深入的专题研究，并广泛征求了相关部门、专家学者的意见和建议，历时一年多时间编制完成。《行动纲要》是到目前为止我国促进大数据发展的第一份权威性、系统性文件，从国家大数据发展战略全局的高度，提出了我国大数据发展的顶层设计，是指导我国未来大数据发展的纲领性文件。</p> <p>下面从本人作为研究起草工作小组主要成员的角度，就《行动纲要》的个人基本认识和理解作一下解读。</p> <p><strong>一、从国家信息化发展的战略全局把握大数据的概念与范畴</strong></p> <p>新一轮信息技术革命与人类经济社会活动的交汇融合，引发了数据爆炸式增长，大数据的概念应运而生。然而到目前为止，全社会对“大数据”的认识并没有达成一致公认的程度。例如，维基百科提出“大数据”是指无法在一定时间内用常规软件工具对其内容进行抓取、管理和处理的数据集合。这种定义对于实际应用而言几乎没有意义，除了少数的互联网巨头和IT巨无霸企业谁也没有这种规模的数据。企业界通常是将自己可利用到的海量数据视为大数据。政府部门认为自身数据很多，将部门数据都整合起来会有几十倍的增长，堪称大数据了，所以他们心目中的“大数据”就是整合后的政府数据资源。一种在学术界广为人知的“4V”表述是：“大数据”是以体量巨大（Volume）、类型繁多（Variety）、存取速度快（Velocity）、价值密度低（Value）为基本特征的数据集。在这种界定下，大数据应用的本质是类似沙里淘金、大海捞鱼、废品利用的过程，大数据并不直接意味大价值，实际上是指经过分析发掘后可以释放潜在的价值。在这种“4V”界定下，传统意义上政府掌握的数据资源看起来不应归为“大数据”，因为它不符合“价值密度低”的界定，而且在数据类型上仍然以结构化数据为主，并且往往是常规数据处理技术就能够胜任的。</p> <p>人们对大数据概念理解的不一致和认识上的分歧实际上反映了现有的大数据概念与现实需求的脱节，特别是与政府需求的脱节。笔者认为，从推进国家信息化发展的角度看，对大数据进行严格定义或许并不重要，能够利用大数据提升全民数据意识、发展数据文化、释放数据红利、打造数据优势才是硬道理。大数据热强化了社会的数据意识，这对于中国才是至关重要的。长期以来中国社会文化一直缺乏精确的数据意识，中国人的传统习惯是定性思维而不是定量思维，正如胡适先生所说的是“差不多”文化，这种文化阻碍了科技在中国的发展，没有精确就没有现代科技。数据文化的本质就是尊重客观世界的实事求是精神，数据就是定量化的、表征精确的事实，重视数据就是强调用事实说话，按理性思维的科学精神，因此提升全社会的数据意识和数据精神是大数据热的巨大贡献。</p> <p>科学认识大数据的概念和范畴，对于准确理解和深刻把握《行动纲要》的主要内容和精神实质是非常重要的。我认为，应该从国家信息化发展的战略全局把握大数据的概念、本质与边界范畴。信息化的核心是数据，只有政府和公众都关注数据时，才能真正理解信息化的实质。数据是与物质、能源同等重要的基础性战略资源，数据的采集和分析涉及每一个行业，是带有全局性和战略性的工作。因此，从国家信息化发展的全局来看，我认为可以把“大数据”广义地界定为：我国现代信息化进程中产生的和可被利用的海量数据集合，是当代信息社会的数据资源总和，是信息时代的全数据，既包括互联网数据，也包括政府数据和行业数据。实际上，在《行动纲要》中，大数据就是采用了这种广义的界定方法。因此，大数据既是一类呈现数据容量大、增长速度快、数据类别多、价值密度低等特征的数据集；也是一项能够对数量巨大、来源分散、格式多样的数据进行采集、存储和关联性分析的新一代信息系统架构和技术；更代表了一种新的思维方式——大数据思维，是能够帮助人们从信息社会海量数据中发现新知识、创造新价值、提升新能力、形成新业态的强大的认知世界和改造世界的能力。</p> <p><strong>二、大数据是我国信息化发展步入深水区后的核心主题和战略抉择 </strong></p> <p>近年来，我国经济社会信息化建设快速推进，信息化水平不断提高。但随着经济社会发展进程的不断深化，我国日益面临诸如食品药品安全、公共安全与应急管理、社会信用体系、生态环境保护、民生公共服务等复杂、多维、并发的经济社会难题。过去以“金字”工程为代表的纵向烟囱式信息系统和以地方、部门信息化为代表的横向孤岛式信息系统，已经无法有效支撑经济社会发展难题的解决，“只管自家门前雪”的信息化管理模式已经严重不适应现代社会的治理需求，往往“按下葫芦浮起瓢”，信息化对经济社会发展的支撑和引领作为无法充分发挥，迫切需要打破部门割据和行业壁垒，促进互联互通、数据开放、信息共享和业务协同，切实以数据流引领技术流、物质流、资金流、人才流，强化统筹衔接和条块结合，实现跨部门、跨区域、跨层级、跨系统的数据交换与共享，构建全流程、全覆盖、全模式、全响应的信息化管理与服务体系。</p> <p>我国信息化发展已步入深水区。可以说，容易的、皆大欢喜的条块和局部的信息化系统已经完成了，正如习近平总书记所说“好吃的肉都吃掉了，剩下的都是难啃的硬骨头”。《行动纲要》的根本出发点和核心主题就是推动解决信息化进入深水区后的硬骨头、老大难问题，主要包括：第一，为解决经济社会难题亟需交换、融合、共享的各类数据和信息，在社会中依据类别、行业、部门、地域被孤立和隔离；第二，同一时空对象所属的各类数据和信息之间天然的关联性和耦合性被割裂和遗忘；第三，政府数据开放和政务信息共享程度受限，信息资源开发利用水平不高，其根源既有大数据处理方面的技术障碍，也有公共权力部门化、部门权力利益化，部门利益合法化带来的体制弊端；第四，数据和信息服务的便捷化、高效化、产业化、智能化水平不高。《行动纲要》的发布，彰显了我国信息化发展的核心已从前期分散化的网络和应用系统建设，回归和聚焦到充分发挥数据资源的核心价值，从而提升国家信息化发展的质量和水平。因此，大数据已成为国家信息化深化发展的核心主题，发展大数据已成为构建数据强国、推动大数据治国的必然选择。</p> <p><strong>三、《行动纲要》的核心是推动数据资源共享开放</strong></p> <p>《行动纲要》从内容架构上总体上呈现了“一体两翼一尾”的格局。“一体”即以“加快建设数据强国，释放数据红利、制度红利和创新红利”为宗旨，“两翼”是指以“加快政府数据开放共享，推动资源整合，提升治理能力”和“推动产业创新发展，培育新兴业态，助力经济转型”两方面内容为载体和依托，“一尾”是指以“强化安全保障、提高管理水平，促进健康发展”为保障和平衡。</p> <p>综观《行动纲要》的内容架构，其核心是推动各部门、各地区、各行业、各领域的数据资源共享开放。在《行动纲要》正文中，“共享”共出现59次，“开放”共出现36处，充分显示了数据共享开放对国家大数据发展的极端重要性。事实上，共享开放的大数据不仅是深化信息化发展的关键要素，也将成为激发大众创业、万众创新的重要源泉，为开创新应用、催生新业态、打造新模式提供新动力，有利于提升创新创业活力，改造升级传统产业，培育经济发展新引擎和国际竞争新优势。</p> <p>但是，从我国信息化发展的现实情况看，“不愿共享开放”、“不敢共享开放”、“不会共享开放”的情况依然较为普遍。特别是我国各级政府、公共机构汇聚了存量大、质量好、增长速度快、与社会公众关系密切的海量数据资源，除了部分自用和信息公开外，大部分没有充分发挥数据资源作为“生产要素、无形资产和社会财富”的应有作用。具体表现在：</p> <p>第一，不愿共享开放。这一方面是认识的问题，一些政府部门和公共机构尚未意识到数据共享开放的价值，另一方面也是利益分配的问题，有些政府部门和公共机构把自己掌握和获取的数据，作为自己利益和权力的一部分，甚至看成是私有财产不愿共享开放，造成不同部门之间甚至同一部门不同机构之间都难以实现数据共享开放。另外，我国在数据共享开放方面的法律法规、制度标准建设相对落后，没有形成数据共享开放的刚性约束，数据共享开放缺乏考核管理体系，数据共享开放价值不明确、市场不健全、动力不充足。</p> <p>第二，不敢共享开放。主要是由于我国当前尚缺乏严格规范数据共享开放的法规制度，相关人员担心政务数据共享开放会引起信息安全问题，担心数据泄密和失控，对数据共享开放具有恐惧感，不敢把自己掌握的数据资源向他人共享开放。在我国，对于保密文件以外的政府数据是否应该共享开放一直没有统一的规定，造成了定保密范围过大。我国《保密法》中对定密、解密程序、泄密处罚以及救济机制等重要制度设置已落后于实际发展的需要，导致政府部门对共享开放数据过度谨慎。</p> <p>第三，不会共享开放。政府数据共享开放是一个高度专业化的工作，需要分级分类、收放结合、科学把握。政府数据该共享开放而不共享开放会引发数据隔离与封闭、价值损耗、信息孤岛等一系列问题；相反，不该共享开放而共享开放、或者不该大范围共享开放而大范围共享开放也可能带来更大的损失，甚至危及国家安全。目前我国尚未出台法律对数据共享开放原则、数据格式、质量标准、可用性、互操作性等做出规范要求，导致政府部门和公共机构数据共享开放能力不强、水平不高、质量不佳，严重制约了大数据作为基础性战略资源的开发应用和价值释放。</p> <p><strong>四、《行动纲要》体现了国家层面对大数据发展的顶层设计和统筹布局</strong></p> <p>《行动纲要》作为我国推进大数据发展的战略性、指导性文件，充分体现了国家层面对大数据发展的顶层设计和统筹布局，为我国大数据应用、产业和技术的发展提供了行动指南。</p> <p>《行动纲要》对支撑大数据发展的国家级统一平台进行了总体规划布局。提出建设“国家政府数据统一开放平台”，构建跨部门的“政府数据统一共享交换平台”，“在地市级以上（含地市级）政府集中构建统一的互联网政务数据服务平台和信息惠民服务平台”，“中央层面构建形成统一的互联网政务数据服务平台”，建立“全国统一的信用信息共享交换平台”，“形成全国统一的中小微企业公共服务大数据平台”，建设“国家网络安全信息汇聚共享和关联分析平台”，建立“国家知识服务平台与知识资源服务中心”。</p> <p>《行动纲要》体现了对大数据发展的系统化、体系化建设思路。《行动纲要》正文共出现“体系”54处，包括构建“国家基础信息资源体系”、“国家宏观调控数据体系”、“国家知识服务体系”，以及建立“大数据应用体系”、“大数据技术体系”、“大数据产业体系”、“大数据产品体系”、“联网信息保存和信息服务体系”、“大数据监督和技术反腐体系”、“综合信息服务体系”、“资源要素数据监测体系”、“大数据产业公共服务支撑体系”、“大数据产业生态体系”、“大数据安全保障体系”、“大数据安全评估体系”、“大数据安全支撑体系”、“大数据产业标准体系”、“数据标准和统计标准体系”、“大数据市场交易标准体系”、“数据科学的学科体系”、“大数据人才培养体系”，等等。</p> <p>上述统筹布局明确了国家层面大数据相关平台、中心和重要系统的建设任务，厘清了不同层面平台的衔接配合关系，提出了系统化建设的重要考虑，将有力推动政府信息系统和公共数据互联共享，加快整合各类政府信息平台，消除信息孤岛，避免重复建设和数据“打架”，增强政府公信力，促进社会信用体系建设，对于促进国家大数据平台和重要系统的统筹规划、合理布局，避免一哄而上、重复建设具有重要而深远的现实意义。</p> <p><strong>五、《行动纲要》明确提出了我国大数据发展的目标体系</strong></p> <p>《行动纲要》立足我国国情和现实需要，提出了未来5—10年推动大数据发展和应用的目标，主要包括五个方面：第一，打造精准治理、多方协作的社会治理新模式；第二，建立运行平稳、安全高效的经济运行新机制；第三，构建以人为本、惠及全民的民生服务新体系；第四，开启大众创业、万众创新的创新驱动新格局；第五，培育高端智能、新兴繁荣的产业发展新生态。</p> <p>《行动纲要》不仅提出了我国大数据发展的宏观定性目标，还明确提出了阶段性、可考核的具体发展目标。按照年度划分，主要发展目标梳理如下：</p> <p>（一）到2017年底前</p> <p>明确各部门数据共享的范围边界和使用方式，跨部门数据资源共享共用格局基本形成。</p> <p>（二）到2018年底前</p> <p>1、建成国家政府数据统一开放平台，率先在信用、交通、医疗、卫生、就业、社保、地理、文化、教育、科技、资源、农业、环境、安监、金融、质量、统计、气象、海洋、企业登记监管等重要领域实现公共数据资源合理适度向社会开放。</p> <p>2、中央政府层面实现数据统一共享交换平台的全覆盖，实现金税、金关、金财、金审、金盾、金宏、金保、金土、金农、金水、金质等信息系统通过统一平台进行数据共享和交换。</p> <p>3、中央层面构建形成统一的互联网政务数据服务平台；国家信息惠民试点城市实现基础信息集中采集、多方利用，实现公共服务和社会信息服务的全人群覆盖、全天候受理和“一站式”办理。</p> <p>4、跨部门共享校核的国家人口基础信息库、法人单位信息资源库、自然资源和空间地理基础信息库等国家基础信息资源体系基本建成，实现与各领域信息资源的汇聚整合和关联应用。</p> <p>5、开展政府和社会合作开发利用大数据试点，完善金融、税收、审计、统计、农业、规划、消费、投资、进出口、城乡建设、劳动就业、收入分配、电力及产业运行、质量安全、节能减排等领域国民经济相关数据的采集和利用机制，推进各级政府按照统一体系开展数据采集和综合利用，加强对宏观调控决策的支撑。</p> <p>6、围绕实施区域协调发展、新型城镇化等重大战略和主体功能区规划，在企业监管、质量安全、质量诚信、节能降耗、环境保护、食品安全、安全生产、信用体系建设、旅游服务等领域探索开展一批应用试点，打通政府部门、企事业单位之间的数据壁垒，实现合作开发和综合利用。</p> <p>（三）到2020年底前</p> <p>1、逐步实现信用、交通、医疗、卫生、就业、社保、地理、文化、教育、科技、资源、农业、环境、安监、金融、质量、统计、气象、海洋、企业登记监管等民生保障服务相关领域的政府数据集向社会开放。</p> <p>2、形成一批具有国际竞争力的大数据处理、分析、可视化软件和硬件支撑平台等产品。</p> <p>3、培育10家国际领先的大数据核心龙头企业，500家大数据应用、服务和产品制造企业。</p> <p>4、在涉及国家安全稳定的领域采用安全可靠的产品和服务，实现关键部门的关键设备安全可靠。</p> <p>上述目标体系的设定，清晰地体现了国家发展大数据的愿景设计，但从实现的角度，其挑战性也是很大的，不仅需要大量的技术创新，而且更需要大量的法规、制度、管理、运行等体制机制方面的改革和创新。《行动纲要》对大数据发展目标的设计，充分体现了国家推动数据共享开放、提升国家数据能力和数据优势的坚强决心，也吹响了打造数据强国的冲锋号角。</p> <p><strong>六、《行动纲要》强调了大数据发展与相关政策的衔接配合 </strong></p> <p>近期，国家相继出台了物联网、云计算、宽带中国、智慧城市、信息消费、信息惠民、互联网+、中国制造2025，以及大众创业、万众创新等一系列信息化政策文件。从本质上讲，这些政策与《促进大数据发展行动纲要》都属于“中国信息化”这一同一事物的不同侧面，即通过新一代信息技术创新应用，切实促进国民经济和社会事业发展。因此，加强对上述政策文件的整体性解读和关联性分析，避免政策碎片化、孤立化和割裂化，是至关重要的。</p> <p>《行动纲要》很好地体现了大数据发展战略部署与其他信息化相关政策的衔接和融合。《行动纲要》明确提出“推动大数据与云计算、物联网、移动互联网等新一代信息技术融合发展，探索大数据与传统产业协同发展的新业态、新模式，促进传统产业转型升级和新兴产业发展，培育新的经济增长点。”“抓住互联网跨界融合机遇，促进大数据、物联网、云计算和三维（3D）打印技术、个性化定制等在制造业全产业链集成运用，推动制造模式变革和工业转型升级。”“推动大数据与移动互联网、物联网、云计算的深度融合，深化大数据在各行业的创新应用，积极探索创新协作共赢的应用模式和商业模式。”</p> <p><strong>七、健全《行动纲要》的政策保障机制乃当务之急</strong></p> <p>《行动纲要》设定的主要任务和发展目标，体现了大数据浪潮下我国在大数据应用和技术领域引领全球的战略机遇，但客观上也面临着条块分割、部门壁垒、利益束缚、信息安全等诸多现实挑战，健全高效的政策保障机制是实施《行动纲要》的基本前提和重要基石。</p> <p>《行动纲要》提出了组织实施机制、法规制度建设、市场发展机制、标准规范体系、财政金融支持、专业人才培养、国际交流合作等七方面的保障措施，这其中许多方面的内容都切实关乎《行动纲要》的落实程度，特别是很多方面的保障要求，尚需要有关部门深入细致研究，拿出切实可行的操作规范，避免政策措施“看起来很美”，但悬在半空中。例如，《行动纲要》中提出的有待“明确”的事项有：“加强顶层设计和统筹规划，明确各部门数据共享的范围边界和使用方式，厘清各部门数据管理及共享的义务和权利。”“明确数据采集、传输、存储、使用、开放等各环节保障网络安全的范围边界、责任主体和具体要求，切实加强对涉及国家利益、公共安全、商业秘密、个人隐私、军工科研生产等信息的保护。”“促进政府数据在风险可控原则下最大程度开放，明确政府统筹利用市场主体大数据的权限及范围。”“研究推动网上个人信息保护立法工作，界定个人信息采集应用的范围和方式，明确相关主体的权利、责任和义务，加强对数据滥用、侵犯个人隐私等行为的管理和惩戒。”</p> <p>可见，上述待“明确”事宜都是道理明显正确，但操作和实现挑战极大的“硬骨头”工程，其真正落实涉及到要“明确”每一项工作的责任主体、分工机制、规范形式、实施机制、效果评价等，都是说起来容易，做起来绝非易事。只有以改革创新的勇气攻坚克难，建立坚实的政策保障机制，破除制约大数据发展的瓶颈和障碍，才能真正开创“用数据说话、用数据决策、用数据管理、用数据创新”的新局面，才能真正释放数据红利、制度红利和创新红利，推进我国从数据大国走向数据强国。</p></div>


"""

# 处理全文的格式问题
def disposeOfData(indexUrl,conentSrc,conent,SavePath,超链接本地地址):
    处理中的全文 = conent
    print("提取出来的全文内容"+处理中的全文)
    # 处理中的全文 = re.sub(r'<span.*?>', '', str(处理中的全文), flags=re.I).replace('</span>', '').replace('</SPAN>', '')
    # 这一组是去除<FONT> ....</FONT>
    # 处理中的全文 = re.sub(r'<font.*?>', '', 处理中的全文, flags=re.I).replace('</FONT>', '').replace('</font>', '')
    # 这一组是去除<p style="text-align:center;line-height:38px">...</p>
    # 处理中的全文 = re.sub(r'<p.*?>', '<p>', 处理中的全文,flags=re.I).replace("</P>",'</p>')
    """
    　　<span><strong>
    """
    处理中的全文= 处理中的全文.replace("　", '').replace("	", '').replace(" ", '')
    处理中的全文 = re.sub('<ul.*?>.*?</ul>', '', 处理中的全文, flags=re.S | re.I)
    # 处理中的全文 = re.sub(r'\(', '【', 处理中的全文)
    # 处理中的全文 = re.sub(r'\)', '】', 处理中的全文)
    # 处理中的全文 = re.sub(r'\（', '【', 处理中的全文)
    # 处理中的全文 = re.sub(r'\）', '】', 处理中的全文)
    处理中的全文 = re.sub(r'\f', '/', 处理中的全文)
    处理中的全文 = re.sub(r'\\', '/', 处理中的全文)
    """
        找到所有的p标签，在所有p标签的集合中再匹配出<p.*?text-align>、<p.*?align>、<p.*?style=".*?(text-align|align)
        最终替换掉原文中的p标签
    """
    所有的p = re.findall('<p.*?>', 处理中的全文, flags=re.I)
    if 所有的p != []:
        for ids, p in enumerate(所有的p):
            P标签格式1 = re.findall('<p.*?(text-align|align)="(.*?)".*?>', p, re.I)
            P标签格式2 = re.findall('<p.*?style=".*?(text-align|align):.*?".*?>', p, re.I)
            if P标签格式1 != []:
                处理中的全文 = re.sub(p, '<p align="%s">' % (P标签格式1[0][1]), 处理中的全文)
            elif P标签格式2 != []:
                for pp in P标签格式2:
                    P标签格式2_1 = re.findall('<p.*?style=".*?(text-align|align):(right|left|center).*?".*?>', p, re.I)
                    if P标签格式2_1:
                        处理中的全文 = re.sub(p, '<p align="%s">' % (P标签格式2_1[0][1]), 处理中的全文)
                    else:
                        # print(p)
                        处理中的全文 = re.sub(p, '<p>', 处理中的全文)
            else:
                处理中的全文 = re.sub(p, '<p>', 处理中的全文)

    所有的div = re.findall('<div.*?>', 处理中的全文, flags=re.I)
    if 所有的div != []:
        for ids, div in enumerate(所有的div):
            div标签格式1 = re.findall('<div.*?(text-align|align)="(.*?)".*?>', div,  flags=re.I)
            div标签格式2 = re.findall('<div.*?style=".*?(text-align|align):.*?".*?>', div, flags=re.I)
            if div标签格式1 != []:
                处理中的全文 = re.sub(div, '<div align="%s">' % (div标签格式1[0][1]), 处理中的全文)
            elif div标签格式2 != []:
                for divdiv in div标签格式2:
                    div标签格式2_1 = re.findall('<div.*?style=".*?(text-align|align):(right|left|center).*?".*?>', div,
                                            flags= re.I)
                    if div标签格式2_1:
                        处理中的全文 = re.sub(div, '<div align="%s">' % (div标签格式2_1[0][1]), 处理中的全文)
                    else:
                        # divrint(div)
                        处理中的全文 = re.sub(div, '<div>', 处理中的全文)
            else:
                处理中的全文 = re.sub(div, '<div>', 处理中的全文)

    """
    先取出掉<span class="wzxq2_lianjie">分享的情况
    
    """
    处理中的全文 = re.sub('<span.*?class="wzxq2_lianjie".*?>.*?</span>','',处理中的全文, flags=re.I|re.S)

    所有的span = re.findall('<span.*?>', 处理中的全文,  flags=re.I)
    if 所有的span != []:
        for ids, span1 in enumerate(所有的span):
            span标签格式1 = re.findall('<span.*?(text-align|align)="(.*?)".*?>', span1, flags= re.I)
            span标签格式2 = re.findall('<span.*?style=".*?(text-align|align):.*?".*?>', span1, flags= re.I)
            if span标签格式1 != []:
                处理中的全文 = re.sub(span1, '<span align="%s">' % (span标签格式1[0][1]), 处理中的全文)
            elif span标签格式2 != []:
                for span2 in span标签格式2:
                    span标签格式2_1 = re.findall('<span.*?style=".*?(text-align|align):(right|left|center).*?".*?>', span1,
                                             flags=re.I)
                    if span标签格式2_1:
                        处理中的全文 = re.sub(span1, '<span align="%s">' % (span标签格式2_1[0][1]), 处理中的全文)
                    else:
                        # print(p)
                        处理中的全文 = re.sub(span1, '<span>', 处理中的全文)
            else:
                处理中的全文 = re.sub(span1, '<span>', 处理中的全文)


    """
    因为全文在一个div中<div class="content" id="ContentRegion" style="overflow-x:auto;width:920;padding-bottom:30px">  且该div中有一个table包含了分享的链接，所以先去掉这个class的table
    <table class="dth14l22" width="804" height="20" cellspacing="0" cellpadding="0" border="0">
    
    """
    处理中的全文 = re.sub('<table.*?class="dth14l22".*?>.*?</table>', '', 处理中的全文, flags=re.S)

    所有的table = re.findall('<table.*?>', 处理中的全文,  flags=re.I)
    if 所有的table != []:
        for ids, table1 in enumerate(所有的table):
            table标签格式1 = re.findall('<table.*?(text-align|align)="(.*?)".*?>', table1, flags= re.I)
            table标签格式2 = re.findall('<table.*?style=".*?(text-align|align):.*?".*?>', table1,  flags=re.I)
            if table标签格式1 != []:
                处理中的全文 = re.sub(table1, '<table align="%s">' % (table标签格式1[0][1]), 处理中的全文)
            elif table标签格式2 != []:
                for table2 in table标签格式2:
                    table标签格式2_1 = re.findall('<table.*?style=".*?(text-align|align):(right|left|center).*?".*?>',
                                              table1, flags=re.I)
                    if table标签格式2_1:
                        处理中的全文 = re.sub(table1, '<table align="%s">' % (table标签格式2_1[0][1]), 处理中的全文)
                    else:
                        # print(p)
                        处理中的全文 = re.sub(table1, '<table>', 处理中的全文)
            else:
                处理中的全文 = re.sub(table1, '<table>', 处理中的全文)

    所有的tr = re.findall('<tr.*?>', 处理中的全文, flags= re.I)
    if 所有的tr != []:
        for ids, tr1 in enumerate(所有的tr):
            tr标签格式1 = re.findall('<tr.*?(text-align|align)="(.*?)".*?>', tr1, flags= re.I)
            tr标签格式2 = re.findall('<tr.*?style=".*?(text-align|align):.*?".*?>', tr1,  flags=re.I)
            if tr标签格式1 != []:
                处理中的全文 = re.sub(tr1, '<tr align="%s">' % (tr标签格式1[0][1]), 处理中的全文)
            elif tr标签格式2 != []:
                for tr2 in tr标签格式2:
                    tr标签格式2_1 = re.findall('<tr.*?style=".*?(text-align|align):(right|left|center).*?".*?>', tr1,
                                           flags=re.I)
                    if tr标签格式2_1:
                        处理中的全文 = re.sub(tr1, '<tr align="%s">' % (tr标签格式2_1[0][1]), 处理中的全文)
                    else:
                        # print(p)
                        处理中的全文 = re.sub(tr1, '<tr>', 处理中的全文)
            else:
                处理中的全文 = re.sub(tr1, '<tr>', 处理中的全文)

    所有的td = re.findall('<td.*?>', 处理中的全文, flags= re.I)
    if 所有的td != []:
        for ids, td1 in enumerate(所有的td):
            td标签格式1 = re.findall('<td.*?(text-align|align)="(.*?)".*?>', td1,  flags=re.I)
            td标签格式2 = re.findall('<td.*?style=".*?(text-align|align):.*?".*?>', td1,  flags=re.I)
            if td标签格式1 != []:
                处理中的全文 = re.sub(td1, '<td align="%s">' % (td标签格式1[0][1]), 处理中的全文)
            elif td标签格式2 != []:
                for td2 in td标签格式2:
                    td标签格式2_1 = re.findall('<td.*?style=".*?(text-align|align):(right|left|center).*?".*?>', td1,
                                           flags= re.I)
                    if td标签格式2_1:
                        处理中的全文 = re.sub(td1, '<td align="%s">' % (td标签格式2_1[0][1]), 处理中的全文)
                    else:
                        # print(p)
                        处理中的全文 = re.sub(td1, '<td>', 处理中的全文)
            else:
                处理中的全文 = re.sub(td1, '<td>', 处理中的全文)


    # 这一组是去除<?xml:namespace prefix = o ns = "urn:schemas-microsoft-com:office:office" /><o:p></o:p>
    处理中的全文 = re.sub(r'<?xml:namespace .*?>', '', 处理中的全文,flags=re.I)
    处理中的全文 = re.sub(r'<o:p.*?>', '', 处理中的全文,flags=re.I)
    处理中的全文 = re.sub(r'</o:p>', '', 处理中的全文,flags=re.I)
    # 这一组是去除<strong> ..../<strong>
    # 处理中的全文 = re.sub(r'<strong.*?>', '', 处理中的全文, flags=re.I)
    # 处理中的全文 = re.sub(r'</strong>', '', 处理中的全文, flags=re.I)

    # <st1:chsdate year="2017" month="3" day="30" islunardate="False" isrocdate="False" w:st="on">...</st1:chsdate>
    处理中的全文 = re.sub(r'<st1:chsdate .*?>', '', 处理中的全文, flags=re.I)
    处理中的全文 = re.sub(r'</st1:chsdate>', '', 处理中的全文, flags=re.I)

    # 去除掉财务司数据的分享链接  http://www.nhfpc.gov.cn/caiwusi/s7788c/201809/14967bc6df764c0b843472712ace91aa.shtml
    处理中的全文 = re.sub('<div class="fx fr">.*?<script>.*?</div>', '', 处理中的全文, flags= re.I|re.S)
    处理中的全文 = re.sub('<div class="clear"></div>', '', 处理中的全文, flags= re.I)
    处理中的全文 = re.sub('<script.*?>.*?</script>', '', 处理中的全文, flags= re.I|re.S)
    处理中的全文 = re.sub('<style.*?>.*?</style>', '', 处理中的全文, flags= re.I|re.S)

    # print("fx fr +clear+ script "+处理中的全文)
    # 表格处理：保留表格但不保留样式
    # 处理中的全文= re.sub(r'<table.*?>','<table>',处理中的全文,flags=re.S | re.I)
    # 处理中的全文= re.sub(r'<tr.*?>','<tr>',处理中的全文,flags=re.S | re.I).replace('</TR>','</tr>')
    # 处理中的全文 = re.sub(r'<td.*?>','<tr>',处理中的全文,flags=re.S | re.I).replace('</TD>','</td>')
    # 处理中的全文 = re.sub(r'<th.*?>','<tr>',处理中的全文,flags=re.S | re.I).replace('</TH>','</th>')

    # 处理<div style="TEXT-ALIGN: center; LINE-HEIGHT: 150%; FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 16pt" id="allStyleDIV">
    # 处理中的全文 = re.sub(r'<div.*?id="allStyleDIV".*?>','',处理中的全文,flags=re.S | re.I)

    # print('allStyleDIV'+ 处理中的全文)
    # <v:line></v:line> 什么鬼的直接链接符啥？啥玩意儿这是，一脸懵逼
    处理中的全文= re.sub(r'<v:line.*?>.*?</v:line>','',处理中的全文,flags=re.S | re.I)

    # 处理单引号问题，文中单引号往数据库插入数据是行不通的
    处理中的全文 = re.sub(r"'", '"', 处理中的全文, flags=re.I)
    # 处理 a表签问题
    处理中的全文 = re.sub(r'<aname=.*?>', '', 处理中的全文 , flags=re.I)
    print("处理A标签前的全文内容1" + 处理中的全文)
    处理中的全文 = re.sub(r'<A', '<a', 处理中的全文 , flags=re.I).replace("</A>",'</a>')
    print("处理A标签前的全文内容2" + 处理中的全文)
    # 处理掉网页带有其他网页的链接
    # 处理中的全文 = re.sub(re.compile(r'链接[: ：]<a.*?href="(.*?)">.*?</a>|相关链接[: ：]<a.*?href="(.*?)">.*?</a>', flags=re.I), '',
    #                 处理中的全文)

    # 处理a标签问题：是填转的情况就去掉超链接直接去掉
    # 处理中的全文 = re.sub('<a.*?href="http://www.*?.(shtml|shtm|html|htm)".*?>.*?</a>', '', 处理中的全文)


    #处理a标签问题：
    """
    这里是是处理a标签跳转的情况：是跳转的情况就去掉超链接，但是要保留<a>标签中的正文内容
    先匹配出所有的a标签，再循环这个集合，再把每个a进行匹配是不是跳转的情况，是的话处理，不是那就只剩下附件的形式，在下文会处理附件
    """
    print("处理A标签前的全文内容3"+处理中的全文)
    所有的A标签 = re.findall(re.compile(r'<a.*?>.*</a>', flags=re.I), 处理中的全文)
    if 所有的A标签!=[]:
        for ids, a in enumerate(所有的A标签):
            跳转A = re.findall(re.compile(r'<a.*?href="http://.*?.(shtml|shtm|html|htm)".*?>(.*?)</a>', flags=re.I), a)
            if 跳转A != []:
                for aa in 跳转A:
                    print("aa"+str(aa))
                    print("a"+a)
                    print("跳转A[0][1]"+跳转A[0][1])
                    print("处理A标签前的全文内容4" + 处理中的全文)
                    处理中的全文 = 处理中的全文.replace(a, 跳转A[0][1])


    # 附件的形式,调用下载程序进行下载
    print("处理中的全文0"+处理中的全文)
    # 先看全文有没有附件
    adjunct = re.findall(r'.*?(pdf|docx|doc|xlsx|xls|rar|zip)', 处理中的全文, flags=re.I)
    if adjunct!=[]:
        print("存在附件a标签")
        # 匹配附件一共有几个，进行循环下载和替换格式，先匹配附件的整个a标签的内容用于后面使用
        adjunct1 = re.findall(re.compile(r' ', re.I | re.S), 处理中的全文)
        print("所有的附件A标签"+str(adjunct1))
        if adjunct1:
            for src in adjunct1:
                print("需要替换的超链接"+str(src))
                # 匹配出每一个a标签的超链接和文件名
                adjunc2 = re.findall(re.compile(r'<a.*?href="(.*?)".*?>(.*?)</a>', re.I | re.S), src)
                print("adjunc2"+str(adjunc2))
                if adjunc2 != []:

                    intactALink = adjunc2[0][0]
                    intactALink =  判断url前面的点返回完整的请求地址.returnSRC().returnSrc(conentSrc,intactALink,conentSrc)
                    intactAName = adjunc2[0][1]
                    intactALink1 = intactALink[intactALink.rfind("/")+1:]
                    附件下载程序.DownloadData(intactALink,'',intactALink1,SavePath)
                    # 替换成本地的格式
                    nweA = r'<a href="%s%s">%s</a>' % (超链接本地地址, intactALink1, intactAName)
                    print("老的a标签"+str(src))
                    print("新的A标签"+str(nweA))
                    处理中的全文 = 处理中的全文.replace(src, nweA)
    print("处理A标签之后的全文"+处理中的全文)
    # 处理全文图片，先改地址，并下载到本地
    imgList = re.findall(r'<img.*?src=".*?".*?>',处理中的全文,flags=re.I)
    if imgList !=[]:
        for imgPhoto in imgList:
            img1 = re.findall(re.compile(r'<img.*?src="(.*?)".*?>', re.I), imgPhoto)
            if img1!=[]:
                imgAlink = img1[0]
                imgAlink = 判断url前面的点返回完整的请求地址.returnSRC().returnSrc(indexUrl,imgAlink,conentSrc)
                imgAlink1 = imgAlink[imgAlink.rfind("/")+1:]
                附件下载程序.DownloadData(imgAlink,'',imgAlink1,SavePath)
                # 替换成本地地址
                newImg = r'<img src="%s%s">'%(超链接本地地址 , imgAlink1)
                处理中的全文 = 处理中的全文.replace(imgPhoto,newImg)

    处理后的全文 = 处理中的全文
    # print(处理后的全文)
    return 处理后的全文
# print(disposeOfData('','',str1,'',''))

# 将中文时间转化为阿拉伯数字
# def disposeOftime(conent):



