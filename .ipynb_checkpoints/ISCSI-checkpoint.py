class ISCSI:
    
    def __init__(self, os):
        self.os = os
        
        #### server ###
        self.disk_name = ""
        self.disk_path = ""
        self.domain = ""

        #### client ####
        self.server_ip = ""

        #### 공용 ####
        self.server_iqn = ""

    def set_firewall(self):
        cmd = ""
        if self.os == "Rocky":
            cmd = """
firewall-cmd --add-port=3260/tcp --permanent
firewall-cmd --reload
systemctl stop firewalld
            """
            return cmd
        elif self.os == "Ubuntu":
            cmd = """
ufw allow 3260/tcp
ufw reload
systemctl stop ufw
            """
            return cmd
        else:
            "지원하지 않는 OS입니다."

        return cmd 

#########################################
#             ISCS SERVER               #
#########################################
    
    def install_target(self):
        print("[ISCSI 서버] ISCSI 서버를 설치합니다.")
        cmd = ""
        if self.os == "Rocky":
            cmd = """
dnf install targetcli -y
systemctl enable --now target         
            """
        elif self.os == "Ubuntu":
            cmd = """
apt install targetcli-fb -y
systemctl enable --now target         
            """
        else:
            print("지원하지 않는 OS입니다.")
        return cmd

    def iscsi_server_iqn_domain(self):
        return "cat /etc/iscsi/initiatorname.iscsi"            

    def targetcli(self,server_ip, client_iqn)
        print("[ISCSI 서버] ISCSI 서버를 세팅해보겠습니다. 이 작업은, client_iqn를 우선적으로 필요로합니다.")
        self.disk_name = input("디스크 이름 : ex)disk100")
        cc("lsblk")
        self.disk_path = input("위의 결과를 확인하시고 iSCSI로 제공할 디스크 경로를 입력하세요 : ex)/dev/sdb")
        domain = input("iSCSI 도메인을 입력해주세요. 원하는 대로 지어주세요~ 단, 이 값은 고유해야합니다. ex) 2025-11.local.r1:disk1 :")
        self.server_iqn = f"iqn.{domain}"
    
        cmd = f"""
cat <<EOF > ~/target_server_setting.exp
#!/usr/bin/expect -f
spawn targetcli

expect "/> " 
send "backstores/block create name={self.disk_name} dev={self.disk_path}\\r"

expect "/> "
send "iscsi/ create {self.server_iqn}\\r"

expect "/> "
send "iscsi/{self.server_iqn}/tpg1/luns create /backstores/block/{self.disk_name}\\r"

expect "/> "
send "iscsi/{self.server_iqn}/tpg1/acls create {client_iqn}\\r"

expect "/> "
send "iscsi/{self.server_iqn}/tpg1/portals delete 0.0.0.0 3260\\r"

expect "/> "
send "iscsi/{self.server_iqn}/tpg1/portals create {server_ip}\\r"

expect "/> "
send "exit\\r"
expect eof
EOF

chmod +x ~/target_server_setting.exp 
expect ~/target_server_setting.exp
    """
        return cmd

    def iscsi_server_restart():
        print("[ISCSI 서버] ISCSI 서버를 다시 실행하겠습니다")
        cmd = f"""
systemctl enable target
systemctl restart target
"""
        return cmd

#########################################
#             ISCS CLIENT               #
#########################################
    def iscsi_client_install(self,server_iqn,server_ip):  # iscsi 클라이언트 설치 및 IQN 파일 생성
        print("[ISCSI 클라이언트] ISCSI 클라이언트를 설치합니다.")
        if self.os == "Ubuntu":
            return "apt install -y open-iscsi && systemctl enable --now iscsid && systemctl start iscsid"
    
        elif self.os == "Rocky" :
            return "dnf install -y iscsi-initiator-utils && systemctl enable --now iscsid"
        print("지원하지 않는 OS입니다.")
        return "" 

    def iscsi_client_iqn(self):
        return "cat /etc/iscsi/initiatorname.iscsi"

    def iscsi_client_login_set_servers_iscsi():
        print("[ISCSI 클라이언트] ISCSI 서버에 로그인합니다.")
        cmd = f"""
systemctl enable --now iscsid
iscsiadm -m discovery -t st -p {server_ip}
iscsiadm -m node -T {server_iqn} -p {server_ip}  -l
lsblk
        """

    
    

























    


