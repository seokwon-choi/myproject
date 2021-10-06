### 1. EOSIO 설치 조건

● 2코어 이상의 CPU, 8GB 이상의 RAM, 20GB 이상의 디스크 용량이 필요하다.


### 2. KT 클라우드 접속

● PUTTY설치 후 Host name에 KT 클라우드의 공용 IP를 입력하고 SSH를 사용하기 때문에 Port에 22를 입력한다.

● KT 클라우드 콘솔에서는 해당 IP의 방화벽을 열어준다.


### 3. EOSIO 설치

● 우분투 환경에서 root권한을 갖는 새 계정을 생성한다.

https://developers.eos.io/welcome/latest/getting-started/development-environment/before-you-begin 참조(1.2, 1.3)


### 4. EOS관련 예제 실습

● 노드 생성, 계정 생성, wallet생성, contract작성 및 배포 등

https://developers.eos.io/welcome/latest/getting-started/development-environment/before-you-begin 참조(1.4 ~ 2.5), 2.5절에 multi-index 설명 있음



### 5. Multi-Index 문법 및 hash_table작성

● smart contract 작성 문법 https://deveos.tistory.com/5?category=847371 참조

● touch hashbook.cpp로 계약서 작성 파일 생성


### 6. eosjs 설치 및 api확인

● 서버에 node.js 설치 https://promobile.tistory.com/381 참조(10 버전으로 설치)

● eosjs 설치(최신버전으로 설치하면 오류남) 

https://github.com/mayajuni/eosjs-wallet 참조(16버전으로 설치)

● curl http://127.0.0.1:8888/v1/chain/get_info 사용으로 api open 확인

● nodejs express기반 Rest Api

설치 및 hello world예제 https://velog.io/@smooth97/Node.js-Restful-API-wok2wqo7yu 참조

● rest api post 구현 
https://hyun1205.tistory.com/30 참조


● eosjs(block chain - server)와 Rest Api(server - client) 연결

● touch (파일명).js로 파일 생성 

● hashbook.js (코드 링크) : time, hash값을 받아 블록체인에 저장

● get.js (코드 링크) : time값을 입력받아 저장된 해당 time, hash값 출력

● node (파일명).js로 실행


### 7. curl 사용 및 외부 접속허용

● curl -X POST ‘(공인 IP):(포트 번호)(설정 URL)’ -d “입력변수=입력값” -v
ex)   curl -X POST ‘211.184.187.131:3000/hash’ -d “time=20210127&hash=am212ds” -v
ex)   curl -X POST ‘211.184.187.131:5000/find’ -d “time=20210127” -v

● 외부 접속허용

  서버 내부의 우분투 환경에서는 
  ○ firewall-cmd --permanent --add-port=포트/tcp firewall-cmd --reload를  
    사용하여 설정
  ○ KT 클라우드에서는 방화벽 설정에서 해당 포트를 열어주면 된다.
  
  
  ![벡엔드 걀과](https://user-images.githubusercontent.com/85105917/136183419-6f2f9740-88e6-4985-8e44-ffeae019ae76.JPG)

