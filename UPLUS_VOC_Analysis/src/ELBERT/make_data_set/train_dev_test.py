import pandas as pd
from sklearn.model_selection import train_test_split
import argparse

# parser 생성
parser = argparse.ArgumentParser(description='set option')
parser.add_argument("--file_name", type=str,
                    default='service_center',
                    help="please input file name   ex) service_center")
args = parser.parse_args()
input_path = '/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/labeling_data/'+args.file_name+'.tsv'
output_path = '/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/ELBERT_data/train_data/'+args.file_name+'/'


# csv 파일 불러오기
file = pd.read_csv(input_path)
file.drop(columns = {"Unnamed: 0"}, inplace = True)


# train과 dev+test으로 1차 분할
train, dev_test, = train_test_split(file, test_size=0.2,
                                    shuffle=True,
                                    random_state=1004)
print("train: ", len(train), ", dev+test: ", len(dev_test))


# dev+test dev와 test로 2차 분할
dev, test, = train_test_split(dev_test, test_size=0.5,
                                    shuffle=True,
                                    random_state=1004)
print("train: ", len(dev), ", dev+test: ", len(test))


# tsv 파일로 저장
train.to_csv(output_path+'train.tsv', sep='\t', header=False)
dev.to_csv(output_path+'dev.tsv', sep='\t', header=False)
test.to_csv(output_path+'test.tsv', sep='\t')