# 2차 프로젝트 서버 파트 코드


### 더조은컴퓨터 아카데미 2차 서버 파트 부분 자동화 코드입니다.


<img width="474" height="158" alt="image" src="https://github.com/user-attachments/assets/62df6a1d-a724-45b0-9b8b-3e5cbe711b7b" />



#### 목적 ####
반복적인 서버 설정 작업을 코드로 자동화하여 인적 실수를 줄이고 구축 시간을 단축하는 것이 목표입니다.

#### 특징 
Rocky9과 Ubuntu를 구별하여 코드를 작성하였다.
함수 복잡도를 낮추고 유지보수성을 향상시키기 위해 클래스 단위 모듈화
각 기능을 기술별로 클래스로 구현하였고 메인 코드에서 이를 통합하여 실행
공통적으로 사용되는 기능은 별도의 함수로 분리하여 코드 재사용성과 가독성 제고하였다.
Paramiko를 이용해서 SSH로 서버에 접속하여 각 기능을 실행하도록 구현했다.
대화형 입력이 필요한 부분은 expect를 사용하여 자동화하였다.

#### 전제조건
기본적인 ssh 설정을 맞춰야한다. 또 ssh 기능을 켜주어야한다.

#### 기술 스택
- FTP
- MariaDB
- DnsVhost
- DHCP
- Firewall
- NFS
- SMB
- PARTITION
- RAID
- ISCSI
- Diskquota
- WP
- JL
- Nginx
- Tomcat
- SNMP 
- Cacti 
- Mails

#### 디렉토리 구조 
main.ipynb 
각 기술스택 class.py 
/ipynb_checkpoints
/__pycache__

#### 사용 방법
main.ipynb에서 실행한다.
SSH 객체 생성 파트에서 서버의 ip와 계정정보를 변경한 후에 코드를 실행한다.
현재 OS 정보를 입력하고 1~18번까지 원하는 기술을 입력한다. 
이 과정은 0번을 누를때까지 반복된다.

#### 코드 흐름도
<img width="498" height="804" alt="image" src="https://github.com/user-attachments/assets/3c3b5506-3415-4c12-84a8-37509faedcd5" />

#### 사용 예시
Mails.py (Class : Mails)를 활용하여 메인에서 postfix, dovecot, roundcube, mutt을 설치하고 브라우저에서 실행하는 과정입니다.

1. 주피터 노트북을 실행하여 main.ipynb 파일에 들어갑니다.
<img width="474" height="153" alt="image" src="https://github.com/user-attachments/assets/b458bad6-6b7a-4c9b-a9d6-20136a340d84" />

2. SSH 객체 생성 파트에서 원격으로 실행할 서버의 ip와 계정 정보를 입력합니다.
<img width="480" height="149" alt="image" src="https://github.com/user-attachments/assets/7094b446-951f-4675-8da9-17125760c7fa" />

<img width="467" height="150" alt="image" src="https://github.com/user-attachments/assets/4b0c4c3b-d16b-4677-a945-e8a64c946b96" />

3. Ctrl + Enter로 main.ipynb를 실행합니다.

4. 현재 OS를 입력하세요.
<img width="717" height="46" alt="image" src="https://github.com/user-attachments/assets/673ec72d-3d13-4e0f-9aec-ba9ddded4f96" />

5. 원하는 기능 번호를 입력합니다. 메일을 설치할 것이기 때문에 18을 입력합니다.
<img width="413" height="325" alt="image" src="https://github.com/user-attachments/assets/c2bc5118-d928-4f6f-8678-e13e5dc6e373" />

6. 기능을 설치하기 위해 필요한 값들을 input으로 받습니다. 예시를 참고하시면 혼동없이 이용할 수 있습니다. 
<img width="727" height="64" alt="image" src="https://github.com/user-attachments/assets/0a51b7ca-7c79-4c02-994b-47e10ac2172e" />
<img width="545" height="320" alt="image" src="https://github.com/user-attachments/assets/3be5bc2f-d576-4beb-98c0-ad16356dfb4e" />
<img width="652" height="94" alt="image" src="https://github.com/user-attachments/assets/10bd2617-7dfc-4303-99e3-961c620d2cfc" />
<img width="624" height="473" alt="image" src="https://github.com/user-attachments/assets/aec6c38b-e4fe-4df8-8489-2ea38d06bd11" />


*대화형 입력이 필요한 부분은 expect를 사용한 모습*


<img width="288" height="180" alt="image" src="https://github.com/user-attachments/assets/824839ab-a948-45a7-835f-37d4848a4861" />


*실제 원격 서버에 DB가 생성된 모습*

7. print문을 준수하여 설치가 잘 되었고 기능을 사용할 수 있는지 확인합니다.
<img width="882" height="595" alt="image" src="https://github.com/user-attachments/assets/4a4381d6-441e-40ba-a7d8-ff4d5c3b59a1" />

