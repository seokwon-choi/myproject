# AI 기반 VOC 텍스트 데이터 분석을 통한 서비스 개선
![image](https://user-images.githubusercontent.com/85105917/132142355-84c45906-ae23-4df6-ae18-5a310c8a452f.png)

### 1. 담당 업무 : 구글 스토어에서 앱 리뷰 크롤링, 데이터 라벨링, BERT모델을 이용한 감성분류, 클러스터링(단어 치환 제외)

### 2. 개발 기획(WBS를 작성해 프로젝트 일정 계획)
![image](https://user-images.githubusercontent.com/85105917/132142463-8a53e428-7235-48e9-bba7-5fb3fb13a47e.png)

#### 2-1. 데이터 흐름도
![image](https://user-images.githubusercontent.com/85105917/132142496-ad670b61-940c-4a7a-9bb0-5410c3bec6a0.png)


### 3. 프로젝트 진행과정
● 본 프로젝트에서 개발한 모델은 리뷰 분석 플렛폼으로 데이터 수집부터 결과 시각화까지 자동화하여 서비스한다. 데이터 수집 대상은 LGU+ 관련 어플리케이션의 리뷰이고, 수집된 데이터를 이용해 자체적으로 fine-tuning한 BERT모델인 ELBERT의 감성 분류를 사용하여 부정 리뷰만을 추출한다. 이후 LDAvis를 이용해 topic별로 분류한 결과를 대시보드 형식으로 시각화하여 사용자에게 인사이트를 제공한다.
<img src="https://user-images.githubusercontent.com/44887886/127100459-a41ed79b-674a-470f-bc93-d67ecead2883.png" width="700"></img>   





## 1. 데이터 수집

구글 플레이스토에 있는 U+ 고객센터, U+ 멤버스, U+ 모바일 TV, U+ 뮤직벨링, U+ 스마트홈 총 5개 어플에서 리뷰를 추출

- U+ 멤버스: 약 14397개
- U+ 모바일 TV: 약 16361개
- U+ 고객센터: 약 13149개
- U+ 뮤직벨링: 약 7571개
- U+ 스마트홈: 약 2148개


=> 총 5개의 어플 중 **U+ 고객센터 앱**만으로 학습 진행

* 라벨링 기준    

  <img src="https://user-images.githubusercontent.com/44887886/127094850-01da9bd7-5e59-4f99-aea6-072d4d82eb7f.png" width=600px, height=200px, title="라벨링 설정"></img>

***              
       
## 2. 감성 분류

<img src="https://user-images.githubusercontent.com/44887886/127101862-8e45355a-ffcd-49e4-bd0e-d344af606bd2.png" width="600"></img>

- pre-training   
  - T academy에서 제공하는 Wiki 백과사전 한국어 데이터로 재학습된 BERT 모델을 사용 
  - 출처: https://drive.google.com/drive/u/0/folders/1QQphR2tmk5g6BheZKZ5q8WhX5yixV8xZ

- fine-tuning
  - 크롤링한 U+ 고객센터 데이터로 학습
  - 최종 정확도 **89.7%**   
    <img width="300" alt="스크린샷 2021-07-27 오후 1 53 35" src="https://user-images.githubusercontent.com/44887886/127097513-77b0f28f-d6c1-47a5-a297-d246438732a1.png"></img>

=> **ELBERT (Elegant Friends BERT)** 자체 모델 생성
  
***

## 3. 클러스터링

- 전처리
  1. 문법 교정
  2. 단어 치환 (치환 사전 구축)
  3. 토큰화 (Mecab 사용)
  4. 불용어 처리 (불용어 사전 구축)

- gensim을 활용한 LDA 모델 학습
  - 토픽 수 결정   
    
    <img src="https://user-images.githubusercontent.com/44887886/127098192-950ca7cd-1375-4089-96fa-8eb7b5371f04.png" width="400" height="250"></img>   
    1. 최적의 토픽 개수를 알아내기 위해 coherence score를 계산하여 주제 일관성을 판단하는 오픈 소스를 활용하였다.
    2. 그래프 상에서 처음으로 가장 급격한 경사가 나타나는 점을 기준으로 토픽 수를 정함  
    3. 클러스터 결과를 확인하며 수치를 조정하여 최종적으로 토픽 수 확정   
         
    
  - 토픽 벡터 시각화  
  
    ![image](https://user-images.githubusercontent.com/44887886/127099618-5dfbc168-1385-4563-9681-e1dfa5b2abb8.png)    
    
***

## 4. 시각화

- 엑셀 대시보드를 활용
  - 분기별 리뷰 데이터 추이
  - 분기별 긍정/부정/기타 비율
  - 클러스터 비율
  - 클러스터별 등장 빈도수가 높은 단어
  - 분기별 클러스터 추이

  <img src="https://user-images.githubusercontent.com/44887886/131998213-9a9d78db-e31b-43d2-8bc6-37e309017d67.png" width="800"></img>     

  U+고객센터 앱의 2016년도 1분기 ~ 2021년도 1분기까지의 리뷰에 대한 정보를 담고 있는 대시보드이다. 필터가 있어 분기별, 주제별로 원하는 정보를 선택적으로 얻을 수 있다. 분기 별 불만 사항으로 앞으로 어떤 문제를 해결해야 하는지의 방향성을 도출할 수 있다.     
  
  

> 한국외국어대학교 컴퓨터전자시스템공학부 우아한프렌즈팀    
  > 팀원: 김소미, 이승윤, 제서윤, 최석원
