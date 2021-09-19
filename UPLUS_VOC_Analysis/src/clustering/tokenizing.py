import json
import pandas as pd
import argparse
from konlpy.tag import Mecab


# parser 생성
parser = argparse.ArgumentParser(description='set option')
parser.add_argument("--file_name", type=str,
                    default='service_center',
                    help="please set file name   ex) service_center")
args = parser.parse_args()
fname = args.file_name


# 치환 사전 불러오기
with open('/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/clustering_data/'+fname+'/substitution_dict.txt', 'r') as file:
    substitution_dict = json.load(file)


df = pd.read_csv('/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/ELBERT_data/sentiment_analyzed/test.tsv')
df['text'] = df['text'].str.upper()

negative = df[df.label==0]

print('긍정 및 중립 개수:', len(df))
print('부정 개수:', len(negative))

# 단어 치환 하기
for key in substitution_dict:
    for word in substitution_dict[key]:
        negative['text'] = negative['text'].str.replace(word, key)


# txt 파일로 저장
negative['text'].to_csv('/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/clustering_data/service_center/txt/'+fname+'.txt',
                        index=False, header=False)


# tokenizing 하기
f = open('/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/clustering_data/service_center/txt/'+fname+'.txt', 'r')
f2 = open('/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/clustering_data/service_center/tokenized_data/'+fname+'.txt', 'w')

mecab = Mecab()
lines = f.readlines()[1:]

for line in lines:
    nouns = mecab.nouns(line)
    f2.write(" ".join(nouns) + '\n')

f.close()
f2.close()

