from jamo import h2j, j2hcj

def get_jongsung_TF(sample_text):
    sample_text_list = list(sample_text)
    last_word = sample_text_list[-1]
    last_word_jamo_list = list(j2hcj(h2j(last_word)))
    last_jamo = last_word_jamo_list[-1]

    jongsung_TF = "T"
    if last_jamo in ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅘ', 'ㅚ', 'ㅙ', 'ㅝ', 'ㅞ', 'ㅢ', 'ㅐ,ㅔ', 'ㅟ', 'ㅖ',
                     'ㅒ']:
        jongsung_TF = "F"

    return jongsung_TF

word_list = ['엘티이', '도돌', '젤리빈', '고객센터', '해외로밍', '부가서비스', '다운그레이드', '하루종일', '장기고객',
             '본인인증', '플레이스토어', '원스토어', '비밀번호', '주민번호', '인증번호','상태바', '티월드', '자급제']

with open("/content/mecab-ko-dic-2.1.1-20180720/user-dic/nnp.csv", 'r', encoding='utf-8') as f:
    file_data = f.readlines()

for word in word_list:
    jongsung_TF = get_jongsung_TF(word)

    line = '{},,,,NNP,*,{},{},*,*,*,*,*\n'.format(word, jongsung_TF, word)

    file_data.append(line)

with open("/content/mecab-ko-dic-2.1.1-20180720/user-dic/nnp.csv", 'w', encoding='utf-8') as f:
    for line in file_data:
        f.write(line)