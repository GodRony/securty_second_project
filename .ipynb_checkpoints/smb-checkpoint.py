# 필요한 변수
-----------------------------------------
#사용 OS
#마운트 지정할 폴더 이름
#윈도우 서버 IP
#SMB 계정명
#SMB 비밀번호
------------------------------------------
#기능
#사용 os
#서비스 상태 확인, 시작, 중지
#smb 서버 or 클라이언트
#공유 폴더 경로가 겹치는지 확인
# 계정 생성, 수정, 삭제
# 비밀번호 재설정
# smb 계정 접근 여부 확인
# 설정 파일 구문 검사
# 방화벽 규칙 설정(포트 개방/차단)
# 로그 파일 확인(연결 실패 or 오류 시 로그 파일 확인하여 원인진단)
# 권한 설정 변경(chmod 777부분)
------------------------------------------
# 사용 OS
class SMB():
    def __init__(self, os, ip):
        self.os = os
        self.smb_share_folder = smb_share_folder
        self.smb_id = smb_id
        self.smb_password = smb_password
            
# SMB 설치
    def smb_install(self):
        print("smb 패키지를 설치합니다.")
        if self.os == "Rocky":
            cmd ="dnf -y install samba samba-client -y"
        elif self.os == "Ubuntu":
            cmd = "apt install cifs-utils smbclient -y"
        else:
            cmd=""
            print("지원하지 않는 OS입니다.")
        return cmd

# SMB 설치 상태 확인
    def smb_intsll_status_check():
        print("설치된 smb 패키지를 확인합니다.")
        cmd = "rpm -qa | grep samba"
        return cmd

# smb 서버 or 클라이언트
    def smb_server_or_client(choose):
        choose = input("smb 서버와 클라이언트 중 선택하세요.(S/C) ex)S : ")
        return choose
    
-------------------서버--------------------
# 윈도우와 공유할 폴더 생성
    def smb_share_folder_make(self):
        self.smb_share_folder = input("공유할 폴더 이름을 입력해주세요. ex)/mnt/win_share : ")
        cmd = f"mkdir {self.smb_share_folder}" 
        return cmd

#SMB전용 계정 생성과 비밀번호 설정
    def smb_id_password_make(self):
        self.smb_id = input("smb 전용 계정 아이디를 입력해주세요. ex)smb")
        self.smb_password = input("smb 전용 계정 비밀번호를 입력해주세요. ex)1234")
        cmd1 = f"useradd -s /sbin/nologin {self.smb_id}"
        cmd2 = f"smbpasswd -a {self.smb_password}"
        return cmd1, cmd2

# 계정정보 출력(계정이 이 시스템에 존재하는지, 해당 계정의 uid 셸 설정 등을 확인)
    def id_password_info(self):
        cmd = f"cat /etc/passwd | grep {self.smb_id}"
        return cmd

#공유 파일 권한 조정
    def share_folder_authority(self):
        cmd1 = f"chmod 777 {self.smb_share_folder}"
        cmd2 = f"chown {self.smb_id}:{self.smb_id} {self.smb_share_folder}"
        return cmd1, cmd2

#계정명으로 접근확인
    def access_check():
        host_ip = input("확인할 호스트 주소를 입력하세요 ex)172.16.12.100 : ")
        cmd = f"smbclient -U {self.smb_id} -L {host_ip}"
        return cmd

#smb 계정 확인 명령어
    def id_check():
        cmd = "pdbedit —list"
        return cmd

# samba 설정파일 접근 하여 기존 파일 백업 파일 생성
    def settingfile_backup():
        cmd = "cd /etc/samba && cp -ap smb.conf smb.conf.bak"
        return cmd
 

# 설정 파일 내용 추가 
    def settingfile_add(self):
        cmd = f"""
        sudo tee -a /etc/samba/smb.conf << EOF
        [share]
                comment = {self.smb_id}'s SMB
                hosts allow = 172.16.0.0/16
                path = {self.smb_share_folder}
                read only = No
                valid users = {self.smb_id}
                write list = self.smb_id}
        EOF
        """
        return cmd

------------클라이언트------------------------
def smb_mount():
    cmd2 = ""
    smb_server_ip = input("접속할 smb 서버의 ip주소를 입력하세요. ex)172.16.12.100 or 도메인:") #접속할 smb 서버의 ip 주소 or 도메인
    smb_share_folder = input("서버에 지정된 공유 폴더의 이름을 입력하세요. ex)share : ") #서버에 지정된 공유 폴더의 이름
    smb_client_mount_point = input("본인 서버에 연결할 위치를 지정하세요. ex) /mnt/win_share : ")# 연결할 위치(클라이언트)
    smb_user_id = input("smb 계정을 입력하세요. ex)smb : ") # smb 접속 계정과 비밀번호
    smb_user_password = input("smb 계정을 입력하세요. ex)smb : ")
    auto = input("/etc/fstab에 부팅 시 자동마운트 설정을 하시겠습니까?  ex) y/n : ")
    cmd1 = (f"""mount -t cifs //{smb_server_ip}/{smb_share_folder} {smb_client_mount_point} -o username={smb_user_id},password={smb_user_password}""")
    print(cmd1)
    if auto == "y":
        cmd2 = (f"//{smb_server_ip}/{smb_share_folder}    {smb_client_mount_point}    cifs    defaults    0 0 | sudo tee -a /etc/fstab")
        print(cmd2)
    return cmd1 ,cmd2
--------------------------------------------------------------------
# 재시작 및 자동활성화
    def smb_systemctl():
        if self.os == "Rocky" :
            smb_service_name = "smb"
        else self.os == "Ubuntu" :
            smb_service_name = "smbd nmbd"
        
        systemctl = int(input("""시스템 상태 확인 및 관리 메뉴를 선택하세요 ex)1 : )
                    ==============================================
                     1. start
                     2. stop
                     3. restart
                     4. reload
                     5. status """))
        if systemctl == 1 :
            cmd = "systemctl start %s" %smb_service_name
        elif systemctl == 2 :
            cmd = "systemctl stop %s" %smb_service_name
        elif systemctl == 3 :
            cmd = "systemctl restart %s" %smb_service_name
        elif systemctl == 4 :
            cmd = "systemctl reload %s" %smb_service_name
        elif systemctl == 5 :
           cmd = "systemctl status %s" %smb_service_name
        else:
            print("잘못된 입력입니다.")    
        return cmd
---------------------------------------------------------------------



