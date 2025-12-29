class NFS:

    def __init__(self, os):
        self.os = os
        
        #### server ####
        self.server_ip = ""
        self.server_nfs_dir = ""
        self.client_nfs_NI = ""
        
        #### client ####
        self.nfs_server_ip = "" 
        self.nfs_client_mount_point = ""        
        
        #### 공통 ####
        self.server_nfs_dir = ""

    def nfs_isntall(self):
        print("nfs 패키지를 설치합니다.")
        cmd=""
        if (self.os == "Rocky"):
            cmd ="dnf install -y nfs-utils"
        elif (self.os == "Ubuntu"):
            cmd = "apt install -y nfs-kernel-server nfs-common"
        else:
            print("지원하지 않는 OS입니다.")
        return cmd

#########################################
#              NFS SERVER               #
#########################################
#공유 디렉터리 생성
    def nfs_share_folder_make(self):
        self.server_nfs_dir = input("공유해줄 폴더 이름을 입력해주세요. ex)/data/nfs_share : ")
        return f"mkdir -p {self.server_nfs_dir}" 

# 디렉터리 권한 설정
    def nfs_share_folder_authority(self):
        cmd = f"chmod 777 {self.server_nfs_dir}"
        return cmd
        
# nfs 공유 목록 작성 및 설정 적용        
    def server_nfs_set_exports_config(self):
      #  global CLIENT_NFS_NI
        self.client_nfs_NI = input("NFS 공유를 허용할 클라이언트의 NI를 입력해주세요 (예: 172.16.0.0/16): ")
        print(f"클라이언트 {self.client_nfs_NI} NI 대역에게 읽기/쓰기 권한을 부여합니다.")

        cmd = f"""
echo '{self.server_nfs_dir} {self.client_nfs_NI}(rw,sync,no_subtree_check)' >> /etc/exports
exportfs -ra
        """
        return cmd
        
    def server_nfs_start(self):
        cmd=""
        if (self.os == "Rocky"):
            cmd = """
systemctl stop firewalld
setenforce 0
systemctl restart nfs-server
"""
        elif (self.os == "Ubuntu"):
            cmd = """
systemctl stop ufw
sudo systemctl restart nfs-kernel-server
"""
        else:
            print("지원하지 않는 OS입니다.")

        return cmd
        
#########################################
#              NFS CLIENT               #
#########################################

    def nfs_client_mount_temporary(self):
        print("마운트를 시작합니다")
        self.nfs_server_ip = input("접속할 NFS 서버의 ip주소를 입력하세요. ex)172.16.12.100 or 도메인:") #접속할 smb 서버의 ip 주소 or 도메인
        self.server_nfs_dir  = input("서버의 nfs 디렉토리 입력 . ex)/data/nfs_share : ") #서버에 지정된 공유 폴더의 이름
        self.nfs_client_mount_point = input("본인 서버에 연결할 위치를 지정하세요. ex) /mnt/nfs_share : ")# 연결할 위치(클라이언트)
        cmd = f"""
mkdir -p {self.nfs_client_mount_point}
mount -t nfs {self.nfs_server_ip}:{self.server_nfs_dir} {self.nfs_client_mount_point}
             """
        return cmd
           
    def nfs_clinet_mount_permanent(self):
        auto = input("/etc/fstab에 부팅 시 자동마운트 설정을 하시겠습니까?  ex) y/n : ")
        cmd = ""
        if(auto == "y"):
            cmd = f"echo '{self.nfs_server_ip}:{self.server_nfs_dir} {self.nfs_client_mount_point} nfs rw,hard,intr,_netdev 0 0' | sudo tee -a /etc/fstab"

        return cmd
    
#재시작 및 자동활성화 
    def nfs_systemctl(self):
        if self.os == "Rocky" :
            smb_service_name = "nfs-server"
        if self.os == "Ubuntu" :
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

