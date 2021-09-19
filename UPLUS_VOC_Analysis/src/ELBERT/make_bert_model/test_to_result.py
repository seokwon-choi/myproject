import pandas as pd
import argparse

# parser 생성
parser = argparse.ArgumentParser(description='set option')
parser.add_argument("--file_name", type=str,
                    default='test',
                    help="please input file name   ex) If you use only test, please input 'test'")
parser.add_argument("--train", default="False", help="True: only input data, false: latest to input data")
args = parser.parse_args()
train = True if args.train == 'True' else False
output_path = '/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/ELBERT_data/sentiment_analyzed/'+args.file_name+'.tsv'


# 파일 불러오기

if train: # train mode일 경우,
    test = pd.read_csv(
        '/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/ELBERT_data/fine_tuned_model/test_results.tsv',
        sep='\t', header=None)
    original = pd.read_csv('/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/labeling_data/'+args.file_name+'.tsv',
                           sep='\t', header=None)
else:
    test = pd.read_csv(
        '/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/ELBERT_data/sentiment_analyzed/test_results.tsv',
        sep='\t', header=None)
    original = pd.read_csv('/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/crawling_data/test.tsv',
                           sep='\t', header=None)

original = original.drop(original.index[0]).reset_index(drop=True)

# 형식 맞추기
df_predict = pd.DataFrame({ 'date':original[1]
                            ,'text':original[3]
                            ,'label':test.idxmax(axis=1).convert_dtypes()
                            })

df_predict.to_csv(output_path, index=False)