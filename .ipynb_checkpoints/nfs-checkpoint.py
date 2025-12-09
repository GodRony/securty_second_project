class Nfs:

    def __init__(self, os, server_ip):
        self.os = os
        self.server_ip = ""
        self.nfs_share_folder = ""

    def nfs_isntall(self):
            print("nfs 패키지를 설치합니다.")
        if self.os == "Rocky":
            cmd ="dnf install -y nfs-utils"
        elif self.os == "Ubuntu":
            cmd = "apt install nfs-kernel-server nfs-common"
        else:
            cmd=""
            print("지원하지 않는 OS입니다.")
        return cmd

#공유 디렉터리 생성
    def nfs_share_folder_make(self):
        self.nfs_share_folder = input("공유할 폴더 이름을 입력해주세요. ex)/srv/nfs/share : ")
        cmd = f"mkdir {self.nfs_share_folder}" 
        return cmd

# 디렉터리 권한 설정
    def share_folder_authority(self):
        cmd1 = f"chmod 777 {self.nfs_share_folder}"
        return cmd1
        
# nfs 공유 목록 작성 및 설정 적용        
    def nfs_settiongfile_add(self):   
        cmd1 = f"""
        sudo tee -a /etc/exports << EOF
            {self.nfs_share_fodler} 172.16.0.0/16(rw,sync,no_root_squash)
        EOF
        """
        cmd2 = "exportfs -rav"#설정 적용
        return cmd1, cmd2    
        
===============================================================
   def nfs_client_mount(self):

    nfs_server_ip = input("접속할 smb 서버의 ip주소를 입력하세요. ex)172.16.12.100 or 도메인:") #접속할 smb 서버의 ip 주소 or 도메인
    nfs_share_folder = input("서버에 지정된 공유 폴더의 이름을 입력하세요. ex)share : ") #서버에 지정된 공유 폴더의 이름
    nfs_client_mount_point = input("본인 서버에 연결할 위치를 지정하세요. ex) /mnt/win_share : ")# 연결할 위치(클라이언트)
    auto = input("/etc/fstab에 부팅 시 자동마운트 설정을 하시겠습니까?  ex) y/n : ")

    if self.os == "Ubuntu" :
        cmd1 = (f"apt -y update && apt -y upgrade")
        cmd2 = (f"mkdir -p {slef.nfs_mount_point}")
        cmd3 = (f"""mount -t nfs {nfs_server_ip}:{nfs_share_folder} {nfs_client_mount_point}""")
        
        if auto == "y":
            cmd4 = (f"{nfs_server_ip}:{nfs_share_folder} {nfs_client_mount_point} nfs defaults 0 0 | sudo tee -a /etc/fstab")
            cmd5 = (f"mount -a") # 마운트 설정 적용
            cmd6 = (f"df") # 마운트 확인
        return cmd1, cmd2, cmd3, cmd4, cmd5, cmd6
  
    else:
        cmd7 = (f"apt -y update && apt -y upgrade")
        cmd8 = (f"mkdir -p {nfs_mount_point}")
        cmd9 = (f"""mount -t nfs {nfs_server_ip}:{nfs_share_folder} {nfs_client_mount_point}""")
        auto = input("/etc/fstab에 부팅 시 자동마운트 설정을 하시겠습니까?  ex) y/n : ")
        if auto == "y":
            cmd10 = (f"{nfs_server_ip}:{nfs_share_folder} {nfs_client_mount_point} nfs defaults 0 0 | sudo tee -a /etc/fstab")
            cmd11 = (f"mount -a") # 마운트 설정 적용
            cmd12 = (f"df") # 마운트 확인
        return cmd7, cmd8, cmd9, cmd10, cmd11, cmd12
     
=============================================================
#재시작 및 자동활성화 
    def nfs_systemctl():
        if self.os == "Rocky" :
            smb_service_name = "nfs-server"
        else self.os == "Ubuntu" :
            smb_service_name = "nfs-kernel-server"
        
        systemctl = int(input("""시스템 상태 확인 및 관리 메뉴를 선택하세요 ex)1 : )
                    ==============================================
                     1. start
                     2. stop
                     3. restart
                     4. reload
                     5. status
                     6. enable --now"""))
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
        elif systemctl == 6 :
           cmd = "systemctl enable --now %s" %smb_service_name
        else:
            print("잘못된 입력입니다.")    
        return cmd

