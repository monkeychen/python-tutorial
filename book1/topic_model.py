import pandas as pd
import jieba
df=pd.read_csv("train.csv",encoding='gb18030')
#print(df.head())
#print(df.shape)
def chinese_word_cut(mytext):
    return " ".join(jieba.cut(mytext))
df["content_cutted"]=df.content.apply(chinese_word_cut)
print(df.content_cutted.head())
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
n_features=1000
tf_vectorizer=CountVectorizer(strip_accents='unicode',
                              max_features=n_features,
                              stop_words='english')
tf=tf_vectorizer.fit_transform(df.content_cutted)
#下面我们就要放出LDA这个大招了。先引入软件包：
#应用LDA方法，指定（或者叫瞎猜）主题个数是必须的。如果你只需要把文章粗略划分成几个大类，就可以把数字设定小一些；相反，如果你希望能够识别出非常细分的主题，就增大主题个数。
from sklearn.decomposition import LatentDirichletAllocation
n_topics=5
lda=LatentDirichletAllocation(n_components=n_topics,
                              learning_method='online',
                              learning_offset=50.,
                              random_state=0)
print(lda.fit(tf))
#定义输出函数
def print_top_words(model,feature_names,n_top_words):
    for topic_idx,topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()
n_top_words=20
tf_feature_names=tf_vectorizer.get_feature_names()
print_top_words(lda,tf_feature_names,n_top_words)
import pyLDAvis
import pyLDAvis.sklearn
pyLDAvis.enable_notebook()
pyLDAvis.sklearn.prepare(lda,tf,tf_vectorizer)