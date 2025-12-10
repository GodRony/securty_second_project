class Iscsi:
    
    def __init__(self, os):
        self.os = os
        
    def 입력받을변수(self):
        self.server_ip = input("서버ip 입력 : ")
        self.client_ip = input("클라이언트ip 입력 : ")
        self.a = input("디렉터리 생성 mkdir -p : ")
        self.b = input("포맷할 디스크를 입력하세요 ex) /dev/sda : ")
        
    def 방화벽해제(self):
        if self.os == "Rocky":
            cmd1 = "firewall-cmd --add-port=3260/tcp --permanent"
            cmd2 = "firewall-cmd --reload"
            cmd3 = "systemctl stop firewalld"
            return cmd1, cmd2, cmd3
        elif self.os == "Ubuntu":
            cmd1 = "ufw allow 3260/tcp"
            cmd2 = "ufw reload"
            cmd3 = "systemctl stop ufw"
            return cmd1, cmd2, cmd3
        else:
            return "지원하지 않는 OS입니다."

    def install_target(self):
        if self.os == "Rocky":
            cmd1 = "dnf install targetcli -y"              
            cmd2 = "systemctl enable --now target"         
            cmd3 = "systemctl status target"               
            return cmd1, cmd2, cmd3
        elif self.os == "Ubuntu":
            cmd1 = "apt install targetcli-fb -y"           
            cmd2 = "systemctl enable --now target"         
            cmd3 = "systemctl status target"               
            return cmd1, cmd2, cmd3
        else:
            return "지원하지 않는 OS입니다."

    def iscsi_server_iqn(self):
        return "cat /etc/iscsi/initiatorname.iscsi"            

    def targetcli(self, client_iqn, server_iqn)
        disk_name = input("디스크 이름 : ex)disk100")
        disk_path = input("디스크 경로 : ex)/dev/sdb")
       
        cmd = [
                "targetcli",
                f"/backstores/block create {disk_name} {disk_path}",
                f"/iscsi create {server_iqn}",
                f"/iscsi/{server_iqn}/tpg1/luns create /backstores/block/{disk_name}",
                f"/iscsi/{server_iqn}/tpg1/acls create {client_iqn}",
                f"/iscsi/{server_iqn}/tpg1/portals create 0.0.0.0",
                f"targetcli saveconfig",
                f"ls",
                "exit"
                ]
        for c in cmd:
            return c
 =================================================================================       
    def iscsi_client_install(self):  # iscsi 클라이언트 설치 및 IQN 파일 생성
      
        if self.os == "Ubuntu":
            return "apt install -y open-iscsi && systemctl enable iscsid && systemctl start iscsid"
    
        else:
            return "dnf install -y iscsi-initiator-utils && systemctl enable --now iscsid"
            
        print("iSCSI 클라이언트 설치 및 IQN 생성 완료\n")

    def iscsi_client_iqn(self):
        return "cat /etc/iscsi/initiatorname.iscsi"

    def target_search(self):
        return f"iscsiadm -m discovery -t st -p {self.server_ip}"
    
    def taget_server_link(self): #타겟서버연결
        return f"iscsiadm -m discovery -t sendtargets -p {self.server_ip} -l"
    
    def mount_point_directory_make(self): #마운트포인트디렉터리생성
        return f"mkdir -p {a}"
    
    def iscsi_authority(): #권한부여
        a = input("권한부여 ex)755 : ")
        b = input("권한부여 위치 : ")
        return f"chmod {a} {b}"
    
    def disk_check(): #디스크확인
        return "fdisk -l" #디스크확인
    
    def disk_fomat(self): 
        return f"mkfs -t ext4 {self.b}" #디스크포멧
    
    def iscsi_mount(self):
        return f"mount -t ext4 {self.b} {self.a}" #마운트
    
    def iscsi_uuid_check(self):
        return f"blkid {self.b}"
    
    def auto_mount(self, uuid): #자동마운트
         auto = input("/etc/fstab에 부팅 시 자동마운트 설정을 하시겠습니까? n 입력시 수동마운트 적용 ex) y/n : ")
        if (auto == "y"):
            cmd = (f"uuid={self.uuid} {self.a} ext4 defaults 0 0")
            return cmd
        else :
            print("/etc/fstab에 미등록\n")
        return ""
    
    def mount_check():
        return "df"

























    


