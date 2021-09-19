with open("/content/mecab-ko-dic-2.1.1-20180720/user-nnp.csv", 'r', encoding='utf-8') as f:
    file_data = f.readlines()

for i in range(len(file_data)):
    lst = file_data[i].split(',')
    lst[3] = '0'  # 우선 순위를 0번째로 부여
    file_data[i] = ",".join(lst)

with open("/content/mecab-ko-dic-2.1.1-20180720/user-nnp.csv", 'w', encoding='utf-8') as f:
    for line in file_data:
        f.write(line)
