# encoding=utf-8

import jieba
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer


def cut_sentence(sentence):
    """
    分句
    :param sentence:
    :return:
    """
    if not isinstance(sentence, unicode):
        sentence = sentence.decode('utf-8')
    delimiters = frozenset(u'。！？')
    buf = []
    for ch in sentence:
        buf.append(ch)
        if delimiters.__contains__(ch):
            yield ''.join(buf)
            buf = []
    if buf:
        yield ''.join(buf)


def load_stopwords(path='/root/zmp/stopword.txt'):
    """
    加载停用词
    :param path:
    :return:
    """
    with open(path) as f:
        stopwords = filter(lambda x: x, map(lambda x: x.strip().decode('utf-8'), f.readlines()))
    stopwords.extend([' ', '\t', '\n'])
    return frozenset(stopwords)


def cut_words(sentence):
    """
    分词
    :param sentence:
    :return:
    """
    stopwords = load_stopwords()
    return filter(lambda x: not stopwords.__contains__(x), jieba.cut(sentence))


def get_abstract(content, size=3):
    """
    利用textrank提取摘要
    :param content:
    :param size:
    :return:
    """
    docs = list(cut_sentence(content))
    tfidf_model = TfidfVectorizer(tokenizer=jieba.cut, stop_words=load_stopwords())
    tfidf_matrix = tfidf_model.fit_transform(docs)
    normalized_matrix = TfidfTransformer().fit_transform(tfidf_matrix)
    similarity = nx.from_scipy_sparse_matrix(normalized_matrix * normalized_matrix.T)
    scores = nx.pagerank(similarity)
    tops = sorted(scores.iteritems(), key=lambda x: x[1], reverse=True)
    size = min(size, len(docs))
    indices = map(lambda x: x[0], tops)[:size]
    return map(lambda idx: docs[idx], indices)


s = u'要说现在当红的90后男星，那就不得不提鹿晗、吴亦凡、杨洋、张艺兴、黄子韬、陈学冬、刘昊然，2016年他们带来不少人气爆棚的影视剧。这些90后男星不仅有颜值、有才华，还够努力，2017年他们又有哪些傲娇的作品呢？到底谁会成为2017霸屏男神，让我们拭目以待吧。鹿晗2016年参演《盗墓笔记》、《长城》、《摆渡人》等多部电影，2017年他将重心转到了电视剧。他和古力娜扎主演的古装奇幻电视剧《择天记》将在湖南卫视暑期档播出，这是鹿晗个人的首部电视剧，也是其第一次出演古装题材。该剧改编自猫腻的同名网络小说，讲述在人妖魔共存的架空世界里，陈长生(鹿晗饰演)为了逆天改命，带着一纸婚书来到神都，结识了一群志同道合的小伙伴，在国教学院打开一片新天地。吴亦凡在2017年有更多的作品推出。周星驰监制、徐克执导的春节档《西游伏魔篇》，吴亦凡扮演“有史以来最帅的”唐僧。师徒四人在取经的路上，由互相对抗到同心合力，成为无坚不摧的驱魔团队。吴亦凡还和梁朝伟、唐嫣合作动作片《欧洲攻略》，该片讲述江湖排名第一、第二的林先生(梁朝伟饰)和王小姐(唐嫣饰)亦敌亦友，二人与助手乐奇(吴亦凡饰)分别追踪盗走“上帝之手”地震飞弹的苏菲，不想却引出了欧洲黑帮、美国CIA、欧盟打击犯罪联盟特工们的全力搜捕的故事。吴亦凡2017年在电影方面有更大突破，他加盟好莱坞大片《极限特工3：终极回归》，与范·迪塞尔、甄子丹、妮娜·杜波夫等一众大明星搭档，为电影献唱主题曲《JUICE》。此外，他还参演吕克·贝松执导的科幻电影《星际特工：千星之城》，该片讲述一个发生在未来28世纪星际警察穿越时空的故事，影片有望2017年上映。'
t = u'中新网北京12月1日电(记者 张曦) 30日晚，高圆圆和赵又廷在京举行答谢宴，诸多明星现身捧场，其中包括张杰(微博)、谢娜(微博)夫妇、何炅(微博)、蔡康永(微博)、徐克、张凯丽、黄轩(微博)等。30日中午，有媒体曝光高圆圆和赵又廷现身台北桃园机场的照片，照片中两人小动作不断，尽显恩爱。事实上，夫妻俩此行是回女方老家北京举办答谢宴。群星捧场 谢娜张杰亮相当晚不到7点，两人十指紧扣率先抵达酒店。这间酒店位于北京东三环，里面摆放很多雕塑，文艺气息十足。高圆圆身穿粉色外套，看到大批记者在场露出娇羞神色，赵又廷则戴着鸭舌帽，十分淡定，两人快步走进电梯，未接受媒体采访。随后，谢娜、何炅也一前一后到场庆贺，并对一对新人表示恭喜。接着蔡康永满脸笑容现身，他直言：“我没有参加台湾婚礼，所以这次觉得蛮开心。”曾与赵又廷合作《狄仁杰之神都龙王》的导演徐克则携女助理亮相，面对媒体的长枪短炮，他只大呼“恭喜！恭喜！”作为高圆圆的好友，黄轩虽然拍杂志收工较晚，但也赶过来参加答谢宴。问到给新人带什么礼物，他大方拉开外套，展示藏在包里厚厚的红包，并笑言：“封红包吧！”但不愿透露具体数额。值得一提的是，当晚10点，张杰压轴抵达酒店，他戴着黑色口罩，透露因刚下飞机所以未和妻子谢娜同行。虽然他没有接受采访，但在进电梯后大方向媒体挥手致意。《我们结婚吧》主创捧场黄海波(微博)获释仍未出席在电视剧《咱们结婚吧》里，饰演高圆圆母亲的张凯丽，当晚身穿黄色大衣出席，但只待了一个小时就匆忙离去。同样有份参演该剧，并扮演高圆圆男闺蜜的大左(微信号：dazuozone) 也到场助阵，28日，他已在台湾参加两人的盛大婚礼。大左30日晚接受采访时直言当时场面感人，“每个人都哭得稀里哗啦，晚上是吴宗宪(微博)(微信号：wushowzongxian) 主持，现场欢声笑语，讲了好多不能播的事，新人都非常开心”。最令人关注的是在这部剧里和高圆圆出演夫妻的黄海波。巧合的是，他刚好于30日收容教育期满，解除收容教育。答谢宴细节宾客近百人，获赠礼物记者了解到，出席高圆圆、赵又廷答谢宴的宾客近百人，其中不少都是女方的高中同学。答谢宴位于酒店地下一层，现场安保森严，大批媒体只好在酒店大堂等待。期间有工作人员上来送上喜糖，代两位新人向媒体问好。记者注意到，虽然答谢宴于晚上8点开始，但从9点开始就陆续有宾客离开，每个宾客都手持礼物，有宾客大方展示礼盒，只见礼盒上印有两只正在接吻的烫金兔子，不过工作人员迅速赶来，拒绝宾客继续展示。'
for i in get_abstract(t):
    print i