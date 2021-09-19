import pandas as pd
import argparse

# parser 생성
parser = argparse.ArgumentParser(description='set option')
parser.add_argument("--file_name", type=str,
                    default='service_center',
                    help="please input file name   ex) service_center")
args = parser.parse_args()
input_path = '/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/crawling_data/'+args.file_name+'.tsv'
output_path = '/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/labeling_data/'+args.file_name+'.tsv'


# 데이터 라벨링
file = pd.read_csv(input_path)
file.drop(columns = {"Unnamed: 0": "No"}, inplace = True)

new = file
LABEL = []
for row in new['STAR']:
    if int(row[10]) < 3:  # 별점 3점 이상은 긍정, 3점 미만은 부정으로 분류
        LABEL.append(0)
    else:
        LABEL.append(1)

new['LABEL'] = LABEL

# tsv 파일로 변환
new.to_csv(output_path, sep='\t', mode='w', encoding='utf-8-sig')