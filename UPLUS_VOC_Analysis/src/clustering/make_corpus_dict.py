import gensim
from collections import Counter
import pandas as pd
import numpy as np
import argparse
import pickle


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



# parser 생성
parser = argparse.ArgumentParser(description='set option')
parser.add_argument("--file_name", type=str, default='service_center',
                    help="please enter file name   ex) service_center")
parser.add_argument("--min_count", type=int, default='5',
                    help="please enter min count to create dictionary")
args = parser.parse_args()
fname = args.file_name
min_count = args.min_count


#1. document 생성

original = pd.read_csv('/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/ELBERT_data/sentiment_analyzed/test.tsv')
corpus_path = '/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/clustering_data/service_center/tokenized_data/'+fname+'.txt'
documents = Documents(corpus_path)

#2. dictionary 생성

dictionary = gensim.corpora.Dictionary(documents)
word_counter = Counter((word for words in documents for word in words))
removal_word_idxs = {
    dictionary.token2id[word] for word, count in word_counter.items() if count < min_count
}
dictionary.filter_tokens(removal_word_idxs)
dictionary.compactify()

#3. 불용어 처리

df_dictionary = pd.read_csv('/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/clustering_data/'+fname+'/stop_word_dictionary.tsv',
                            sep='\t', header=None)   # 불용어 사전 불러오기
stop_word = list(np.array(df_dictionary[0].tolist()))

dict_list = list(dictionary.values())
removal_word_idxs2 = {
    dictionary.token2id[word] for word in dict_list
    if word in stop_word
}

dictionary.filter_tokens(removal_word_idxs2)
dictionary.compactify()
print('dictionary size : %d' % len(dictionary))

#4. corpus 생성

corpus = Corpus(corpus_path, dictionary)

#5. pickle 로 corpus 저장

with open('/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/clustering_data/'+fname+'/pickle/corpus.pickle', 'wb') as f:
    pickle.dump(corpus, f, pickle.HIGHEST_PROTOCOL)

with open('/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/clustering_data/'+fname+'/pickle/dictionary.pickle', 'wb') as f2:
    pickle.dump(dictionary, f2, pickle.HIGHEST_PROTOCOL)

with open('/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/clustering_data/'+fname+'/pickle/documents.pickle', 'wb') as f:
    pickle.dump(documents, f, pickle.HIGHEST_PROTOCOL)


