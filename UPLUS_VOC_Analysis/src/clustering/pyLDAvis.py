from gensim.models.ldamodel import LdaModel
import pandas as pd
import pyLDAvis.gensim as gensimvis
import pyLDAvis
import math
import argparse
import pickle
from datetime import datetime


class Documents:
    def __init__(self, path):
        self.path = path

    def __iter__(self):
        with open(self.path, encoding='utf-8') as f:
            for doc in f:
                yield doc.strip().split()


class Corpus:
    def __init__(self, path, dictionary):
        self.path = path
        self.dictionary = dictionary
        self.length = 0

    def __iter__(self):
        with open(self.path, encoding='utf-8') as f:
            for doc in f:
                yield self.dictionary.doc2bow(doc.split())

    def __len__(self):
        if self.length == 0:
            with open(self.path, encoding='utf-8') as f:
                for i, doc in enumerate(f):
                    continue
            self.length = i + 1
        return self.length


def make_topictable_per_doc(ldamodel, corpus):
    topic_table = pd.DataFrame()

    # 몇 번째 문서인지를 의미하는 문서 번호와 해당 문서의 토픽 비중을 한 줄씩 꺼내온다.
    for i, topic_list in enumerate(ldamodel[corpus]):
        doc = topic_list[0] if ldamodel.per_word_topics else topic_list
        doc = sorted(doc, key=lambda x: (x[1]), reverse=True)
        # 각 문서에 대해서 비중이 높은 토픽순으로 토픽을 정렬한다.
        # EX) 정렬 전 0번 문서 : (2번 토픽, 48.5%), (8번 토픽, 25%), (10번 토픽, 5%), (12번 토픽, 21.5%),
        # Ex) 정렬 후 0번 문서 : (2번 토픽, 48.5%), (8번 토픽, 25%), (12번 토픽, 21.5%), (10번 토픽, 5%)
        # 48 > 25 > 21 > 5 순으로 정렬이 된 것.

        # 모든 문서에 대해서 각각 아래를 수행
        for j, (topic_num, prop_topic) in enumerate(doc): #  몇 번 토픽인지와 비중을 나눠서 저장한다.
            if j == 0:  # 정렬을 한 상태이므로 가장 앞에 있는 것이 가장 비중이 높은 토픽
                topic_table = topic_table.append(pd.Series([int(topic_num), round(prop_topic,4), topic_list]), ignore_index=True)
                # 가장 비중이 높은 토픽과, 가장 비중이 높은 토픽의 비중과, 전체 토픽의 비중을 저장한다.
            else:
                break
    return(topic_table)


# 오늘 날짜 불러오기
today = datetime.today()
today_year = today.year
today_quarter = math.ceil(today.month/3)


# parser 생성
parser = argparse.ArgumentParser(description='set option')
parser.add_argument("--file_name", type=str, default='service_center',
                    help="please enter file name   ex) service_center")
parser.add_argument("--optimal_n", type=int, default='5',
                    help="please enter optimal topic numbers")
parser.add_argument("--year", type=int, default=today_year, help="please input year")
parser.add_argument("--quarter", type=int, default=today_quarter, help="please input quarter")
args = parser.parse_args()
fname = args.file_name
n_topics = args.optimal_n


# 파일 불러오기
with open('/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/clustering_data/'+fname+'/pickle/corpus.pickle', 'rb') as f:
    corpus = pickle.load(f)
with open('/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/clustering_data/'+fname+'/pickle/dictionary.pickle', 'rb') as f2:
    dictionary = pickle.load(f2)
with open('/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/clustering_data/'+fname+'/pickle/documents.pickle', 'rb') as f3:
    documents = pickle.load(f3)



# 데이터 프레임 생성
output = pd.DataFrame(columns=['date', 'label', '클러스터 이름'])               # 분기별 클러스터 비율
output2 = pd.DataFrame(columns = ['분기', '클러스터 이름' , '등장 빈도가 높은 단어']) # 클러스터별 단어 비율


# LDA 모델 학습
lda_model = LdaModel(corpus, id2word=dictionary, num_topics=n_topics)
topics = lda_model.print_topics(num_words=10)

prepared_data = gensimvis.prepare(lda_model, corpus, dictionary)
pyLDAvis.display(prepared_data)




# 분기별 데이터 저장
original = pd.read_csv('/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/ELBERT_data/sentiment_analyzed/test.tsv')
df_two = pd.DataFrame(columns = ['분기', '클러스터 이름' , '등장 빈도가 높은 단어'])
date = args.year + '년 ' + args.quarter + '분기'
clu_name = args.year + '_' + args.quarter + '_'

for i in range(len(topics)):
  top = lda_model.show_topic(i)
  for j in range(10):
    fre = round(top[j][1] * 100)
    df_plus = pd.DataFrame({'분기':[date]*fre,
                            '클러스터 이름':[clu_name + str(i)]*fre,
                            '등장 빈도가 높은 단어':[top[j][0]]*fre})
    df_two = pd.concat([df_two, df_plus], ignore_index=False)


# topictable 생성

topictable = make_topictable_per_doc(lda_model, corpus)
topictable = topictable.reset_index() # 문서 번호을 의미하는 열(column)로 사용하기 위해서 인덱스 열을 하나 더 만든다.
topictable.columns = ['문서 번호', '가장 비중이 높은 토픽', '가장 높은 토픽의 비중', '각 토픽의 비중']


# 데이터 형식에 맞게 저장

#print('전체개수, 부정개수, 토픽테이블개수:', len(original), len(original[original.label==0]), len(topictable))

topictable.set_index(original[original.label==0].index, inplace=True)
original.loc[(original.label==0), '클러스터 이름'] = topictable['가장 비중이 높은 토픽']
for i in range(len(original)):
  if math.isnan(original.loc[i, '클러스터 이름']) == False:
    original.loc[i, '클러스터 이름'] = clu_name + str(int(original.loc[i, '클러스터 이름']))


output = original.drop(['text'], axis=1, inplace=True)
outpput2 = df_two


# output 저장
output.to_csv('/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/clustering_data/service_center/final_data/output1.csv', index=False)
output2.to_csv('/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/clustering_data/service_center/final_data/output2.csv', index=False)
