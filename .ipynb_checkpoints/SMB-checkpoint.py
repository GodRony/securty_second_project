# # 필요한 변수
# -----------------------------------------
# #사용 OS
# #마운트 지정할 폴더 이름
# #윈도우 서버 IP
# #SMB 계정명
# #SMB 비밀번호
# ------------------------------------------
# #기능
# #사용 os
# #서비스 상태 확인, 시작, 중지
# #smb 서버 or 클라이언트
# #공유 폴더 경로가 겹치는지 확인
# # 계정 생성, 수정, 삭제
# # 비밀번호 재설정
# # smb 계정 접근 여부 확인
# # 설정 파일 구문 검사
# # 방화벽 규칙 설정(포트 개방/차단)
# # 로그 파일 확인(연결 실패 or 오류 시 로그 파일 확인하여 원인진단)
# # 권한 설정 변경(chmod 777부분)
# ------------------------------------------
# # 사용 OS
class SMB():
    def __init__(self, os):
        self.os = os
        
        #### server ####
        self.smb_server_share_folder = ""
        
        #### client ####
        self.smb_server_ip = ""
        self.smb_client_mount_point = ""
        
        #### 공통 ####
        self.share_name = ""
        self.smb_id = ""
        self.smb_password = ""
            
# SMB 설치
    def smb_install(self):
        print("smb 패키지를 설치합니다.")
        if self.os == "Rocky":
            cmd ="dnf -y install samba samba-client cifs-utils"
        elif self.os == "Ubuntu":
            cmd = "apt install cifs-utils smbclient -y"
        else:
            cmd=""
            print("지원하지 않는 OS입니다.")
        return cmd

# SMB 설치 상태 확인
    def smb_intsll_status_check(self):
        print("설치된 smb 패키지를 확인합니다.")
        cmd = "rpm -qa | grep samba"
        return cmd

    
#########################################
#              SMB SERVER               #
#########################################
    
# 윈도우와 공유할 폴더 생성
    def smb_share_folder_make(self):
        self.smb_server_share_folder = input("공유할 폴더 이름을 입력해주세요. ex)/srv/samba (/mnt 경로에 하지마세요.): ")
        cmd = f"mkdir -p {self.smb_server_share_folder}" 
        return cmd

    def smb_mk_smb_id(self):
        self.smb_id = input("smb 전용 계정 아이디를 입력해주세요. ex)smb")
        cmd = f"useradd -s /sbin/nologin {self.smb_id}"
        return cmd

    def smb_set_smb_id_passwd(self):
        self.smb_password = input("smb 전용 계정 비밀번호를 입력해주세요. ex)1234")

        cmd = f'''
expect -c "
set timeout 10
spawn smbpasswd -a {self.smb_id}
expect \\"New SMB password:\\"
send \\"{self.smb_password}\\r\\"
expect \\"Retype new SMB password:\\"
send \\"{self.smb_password}\\r\\"
expect eof
"
'''
        return cmd
## smb id 생성 및 passwd 설정 분리

    #smb 계정 확인 명령어
    def smb_id_check(self):
        cmd = "pdbedit --list"
        return cmd
        

#공유 파일 권한 조정
    def smb_share_folder_authority(self):
        cmd = f"""
chmod 777 {self.smb_server_share_folder}
chown {self.smb_id}:{self.smb_id} {self.smb_server_share_folder}        
        """
        return cmd

# #계정명으로 접근확인
#     def smb_client_check(self):
#         host_ip = input("확인할 호스트 주소를 입력하세요 ex)172.16.12.100 : ")
#         cmd = f"smbclient -U {self.smb_id} -L {host_ip}"
#         return cmd



# samba 설정파일 접근 하여 기존 파일 백업 파일 생성
    def smb_mk_back(self):
        cmd = "cd /etc/samba && cp -ap smb.conf smb.conf.bak"
        return cmd
 

# 설정 파일 내용 추가 
    def smb_set(self):
        self.share_name = input("share name을 입력하세요 ex. share")
        
        cmd = f"""
sudo tee -a /etc/samba/smb.conf << EOF
[{self.share_name}]
    comment = {self.smb_id}'s SMB
    path = {self.smb_server_share_folder}
    valid users = {self.smb_id}
    read only = no
    browseable = yes
    writable = yes
    guest ok = no
EOF
"""
        return cmd

    def smb_server_start(self):
        cmd = f"""
systemctl stop firewalld
setenforce 0
systemctl start smb
        """
        return cmd
#########################################
#              SMB CLIENT               #
#########################################

    def smb_client_login(self) :
        self.smb_server_ip = input("접속할 smb 서버의 ip주소를 입력하세요. ex)172.16.12.100 or 도메인:") 
        self.smb_client_mount_point = input("본인(클라이언트) 서버에 연결할 디렉토리를 지정하세요. ex) /mnt/win_share : ")
        # 연결할 위치(클라이언트)
        self.smb_id = input("smb id를 입력하세요. ex)smb : ") # smb 접속 계정과 비밀번호
        self.smb_password = input("smb password를 입력하세요. ex)1234 : ")
    
        print("SMB 서버에 로그인하겠습니다")
        
        cmd = f"""
mkdir -p {self.smb_client_mount_point}
cat <<EOF > /root/smb_login.exp
#!/usr/bin/expect -f
set timeout -1
spawn smbclient -U {self.smb_id} -L {self.smb_server_ip}
expect "Password for"
send "{self.smb_password}\\r"
expect eof
EOF
chmod +x /root/smb_login.exp
/usr/bin/expect /root/smb_login.exp
    """
        return cmd
    
    def smb_client_mount(self) :
        self.smb_share = input("서버에 지정된 공유 폴더의 이름을 입력하세요. ex)share : ")  #서버에 지정된 공유 폴더의 이름
        auto = input("/etc/fstab에 부팅 시 자동마운트 설정을 하시겠습니까? n 입력시 수동마운트 적용 ex) y/n : ")
        if(auto == "n") :
            cmd = f' mount -v -t cifs //{self.smb_server_ip}/{self.smb_share} {self.smb_client_mount_point} -o username={self.smb_id},password="{self.smb_password}",vers=3.0'
            return cmd
    
        if (auto == "y"):
            cmd = (f"//{self.smb_server_ip}/{self.smb_share}    {self.smb_client_mount_point}    cifs    defaults    0 0 | sudo tee -a /etc/fstab")
            return cmd
        else :
            print("잘못 입력하셨습니다")
        return ""
    

    
# 재시작 및 자동활성화
    def smb_systemctl(self):
        systemctl = int(input("""시스템 상태 확인 및 관리 메뉴를 선택하세요 ex)1 : )
                    ==============================================
                     1. start
                     2. stop
                     3. restart
                     4. reload
                     5. status """))
        if systemctl == 1 :
            cmd = "systemctl start smb"
        elif systemctl == 2 :
            cmd = "systemctl stop smb"
        elif systemctl == 3 :
            cmd = "systemctl restart smb"
        elif systemctl == 4 :
            cmd = "systemctl reload smb"
        elif systemctl == 5 :
           cmd = "systemctl status smb"
        else:
            print("잘못된 입력입니다.")    
        return cmd



