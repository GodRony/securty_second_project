# 2차 프로젝트 서버 파트 코드


### 더조은컴퓨터 아카데미 2차 서버 파트 부분 자동화 코드입니다.

##### 목적
반복적인 서버 설정 작업을 코드로 자동화하여 인적 실수를 줄이고 구축 시간을 단축하는 것이 목표입니다.

##### 특징 
Rocky9과 Ubuntu를 구별하여 코드를 작성하였다.
함수 복잡도를 낮추고 유지보수성을 향상시키기 위해 클래스 단위 모듈화
각 기능을 기술별로 클래스로 구현하였고 메인 코드에서 이를 통합하여 실행
공통적으로 사용되는 기능은 별도의 함수로 분리하여 코드 재사용성과 가독성 제고하였다.
Paramiko를 이용해서 SSH로 서버에 접속하도록 하였다.
이를 위해선 

##### 기술 스택
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

##### 디렉토리 구조 
main.ipynb 
각 기술스택 class.py 
/ipynb_checkpoints
/__pycache__

##### 사용 예시 
main.ipynb에서 실행한다.
현재 OS 정보를 입력하고 1~18번까지 원하는 기술을 입력한다. 
이 과정은 0번을 누를때까지 반복된다.

##### 코드 흐름도
<img width="498" height="804" alt="image" src="https://github.com/user-attachments/assets/3c3b5506-3415-4c12-84a8-37509faedcd5" />

