#===================================================================
# DHCP 클래스
#===================================================================
class DHCP():
    
    def __init__(self, os):
        self.os = os
        self.gateway = ""
        self.min_rent = ""
        self.max_rent = ""
        self.network_ni = ""
        self.network_sub = ""
        self.range_ip = ""
        self.static_hosts = ""
        self.service_name = "" 
        self.NI = ""
        
#===================================================================
# 메소드        
#===================================================================
    
    def install(self):
        if self.os == "Rocky":
            cmd = """
dnf install -y dhcp-server
rpm -qa | grep dhcp-server
ip a
"""
            self.service_name = "dhcpd"
        elif self.os == "Ubuntu" :
            cmd = """
apt update
apt install -y isc-dhcp-server
dpkg -l | grep isc-dhcp-server
ip a
"""
            self.service_name = "isc-dhcp-server"
        return cmd
        
#===================================================================        
    
    def on_off(self):
        print("1. DHCP 서비스 시작")
        print("2. DHCP 서비스 중지")
        choice = input("선택: ")
        if choice == "1":
            cmd = f"""
systemctl enable {self.service_name}
systemctl restart {self.service_name}
"""
        elif choice == "2":
            cmd = f"""
systemctl stop {self.service_name}
systemctl disable {self.service_name}
"""
        else:
            print("잘못된 선택입니다.")
        
        return cmd
        
#===================================================================        
            
    def set_pool(self):
        # 사용자 입력
        self.NI = input("위에서 확인한 네트워크 인터페이스를 입력하세요 ex. ens33: ")
        self.network_ni = input("위에서 확인한 subnet을 입력하세요 ex. 172.16.0.0: ")
        self.network_sub = input("위에서 확인한 netmask을 입력하세요 ex. 255.255.0.0: ")
        self.gateway = input("게이트웨이를 입력하세요 ex. 172.16.0.1: ")
        
        self.exclusion_start = input("제외할 ip 시작 주소를 적으세요 ex. 172.16.16.100: ")
        self.exclusion_end = input("제외할 ip 마지막 주소를 적으세요 ex. 172.16.16.200: ")
        
        self.domain = input("도메인 서버를 입력하세요 ex. 8.8.8.8: ")
        self.pool = input("pool의 이름을 지정하세요 ex. example.local: ")

        ch_NI_cmd = ""

        if self.os == "Ubuntu":
            ch_NI_cmd = f"""
            ip a
sed -i 's|^INTERFACESv4=.*$|INTERFACESv4="{self.NI}"|' /etc/default/isc-dhcp-server
"""
            print("해당 os는 우분투이므로 /etc/default/isc-dhcp-server 파일을 해당 NI로 변경했습니다.")
            
        # dhcpd.conf 업데이트
        add_dhcp_file_cmd = f"""
echo '
default-lease-time 600;
max-lease-time 7200;
authoritative;

subnet {self.network_ni} netmask {self.network_sub} {{
    range {self.exclusion_start} {self.exclusion_end};
    option routers {self.gateway};
    option subnet-mask {self.network_sub};
    option domain-name-servers {self.domain};
    option domain-name "{self.pool}";
}}
' >> /etc/dhcp/dhcpd.conf
"""
  
        print("/etc/dhcp/dhcpd.conf 파일 업데이트 완료")
        cmd = f"""
        {ch_NI_cmd}
        {add_dhcp_file_cmd}
        """
        return cmd
        

#===================================================================        
    
    def chk_pool(self):
        if self.os == "Rocky":
            lease_path = "/var/lib/dhcpd/dhcpd.leases"
        elif self.os == "Ubuntu" :
            lease_path = "/var/lib/dhcp/dhcpd.leases"
        
        cmd = f"""
echo '=== DHCP 설정 파일 ==='
cat /etc/dhcp/dhcpd.conf
echo ''
echo '=== Lease 정보 ==='
cat {lease_path} | tail -20
"""
        return cmd
        
#===================================================================        
    
    def backup(self):
        if self.os == "Rocky":
            lease_path = "/var/lib/dhcpd/dhcpd.leases"
        elif self.os == "Ubuntu" :
            lease_path = "/var/lib/dhcp/dhcpd.leases"
        
        cmd = f"""
mkdir -p /root/backup/dhcp
cp /etc/dhcp/dhcpd.conf /root/backup/dhcp/dhcpd.conf.backup
cp {lease_path} /root/backup/dhcp/dhcpd.leases.backup
ls -lh /root/backup/dhcp/
"""
        return cmd
        
#===================================================================

    def set_log(self):
        if self.os == "Rocky":
            log_source = "/var/log/messages"
        elif self.os == "Ubuntu" :
            log_source = "/var/log/syslog"
        
        cmd = f"""
grep -i dhcp {log_source} > /var/log/dhcpd.log
echo 'DHCP 로그 파일 생성 완료: /var/log/dhcpd.log'
"""
        return cmd
            
#===================================================================        
    
    def chk_log(self):
        cmd = """
echo '=== DHCP 로그 ==='
tail -50 /var/log/dhcpd.log 2>/dev/null || echo '로그 파일이 없습니다.'
"""
        return cmd

