import paramiko
from CC import CC

#===================================================================
# 생성자 예시
#===================================================================
"""
dhcp = Dhcp(
    os="rocky9",
    gateway="172.16.0.1",
    min_rent=100,
    max_rent=600,
    network_ni="172.16.5.0",
    network_sub="255.255.0.0",
    range_ip=[
        ("172.16.5.40", "172.16.5.42"),
        ("172.16.5.46", "172.16.5.50")
    ],
    static_hosts=[
        ("1.1.1.1", "aa:bb:cc:dd:ee:ff"),
        ("1.1.1.2", "11:22:33:44:55:66")
    ]
)
"""

#===================================================================
# DHCP 클래스
#===================================================================
class Dhcp():
    
    def __init__(self, os, gateway, min_rent, max_rent, network_ni, network_sub, range_ip, static_hosts):
        self.os = os
        self.gateway = gateway
        self.min_rent = min_rent
        self.max_rent = max_rent
        self.network_ni = network_ni
        self.network_sub = network_sub
        self.range_ip = range_ip
        self.static_hosts = static_hosts
        
#===================================================================
    
# 메소드        
        
#===================================================================
    
    def install(self):
        if self.os == "rocky9":
            cmd = """
dnf install -y dhcp-server
rpm -qa | grep dhcp-server
"""
        else:  # ubuntu
            cmd = """
apt update
apt install -y isc-dhcp-server
dpkg -l | grep isc-dhcp-server
"""
        return cmd
        
#===================================================================        
    
    def on_off(self):
        print("1. DHCP 서비스 시작")
        print("2. DHCP 서비스 중지")
        choice = input("선택: ")
        
        if self.os == "rocky9":
            service_name = "dhcpd"
        else:
            service_name = "isc-dhcp-server"
        
        if choice == "1":
            cmd = f"""
systemctl enable {service_name}
systemctl start {service_name}
systemctl status {service_name}
"""
        elif choice == "2":
            cmd = f"""
systemctl stop {service_name}
systemctl disable {service_name}
systemctl status {service_name}
"""
        else:
            return "echo '잘못된 선택입니다.'"
        
        return cmd
        
#===================================================================        
            
    def set_pool(self):
        # range 부분 만들기
        range_text = ""
        for i in range(len(self.range_ip)):
            range_text += f"    range {self.range_ip[i][0]} {self.range_ip[i][1]};\n"
        
        # static host 부분 만들기
        host_text = ""
        for i in range(len(self.static_hosts)):
            host_text += f"host static-{self.static_hosts[i][0]} {{\n"
            host_text += f"    hardware ethernet {self.static_hosts[i][1]};\n"
            host_text += f"    fixed-address {self.static_hosts[i][0]};\n"
            host_text += f"}}\n\n"
        
        if self.os == "rocky9":
            service_name = "dhcpd"
        else:
            service_name = "isc-dhcp-server"
        
        # 전체 설정
        cmd = f"""
cat >> /etc/dhcp/dhcpd.conf << 'EOF'

subnet {self.network_ni} netmask {self.network_sub} {{
    option routers {self.gateway};
    option subnet-mask {self.network_sub};
{range_text}}}

{host_text}
EOF

cat /etc/dhcp/dhcpd.conf
dhcpd -t -cf /etc/dhcp/dhcpd.conf
systemctl restart {service_name}
"""
        return cmd
        
#===================================================================        
    
    def del_pool(self):
        print("현재 Range 목록:")
        
        for i in range(len(self.range_ip)):
            print(f"  {i+1}. {self.range_ip[i][0]} ~ {self.range_ip[i][1]}")
        
        choice = int(input("삭제할 번호: ")) - 1
        
        if 0 <= choice < len(self.range_ip):
            target_start = self.range_ip[choice][0]
            target_end = self.range_ip[choice][1]
            
            if self.os == "rocky9":
                service_name = "dhcpd"
            else:
                service_name = "isc-dhcp-server"
            
            cmd = f"""
sed -i '/range {target_start} {target_end}/d' /etc/dhcp/dhcpd.conf
cat /etc/dhcp/dhcpd.conf
systemctl restart {service_name}
"""
            
            del self.range_ip[choice]
            print(f"\n{target_start} ~ {target_end} Range 삭제 완료")
            return cmd
        else:
            return "echo '잘못된 번호입니다.'"
        
#===================================================================        
    
    def chk_pool(self):
        if self.os == "rocky9":
            lease_path = "/var/lib/dhcpd/dhcpd.leases"
        else:
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
        if self.os == "rocky9":
            lease_path = "/var/lib/dhcpd/dhcpd.leases"
        else:
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
        if self.os == "rocky9":
            log_source = "/var/log/messages"
        else:
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


#===================================================================
# 임시 SSH 연결 코드
#===================================================================

# SSH_USER = "root"
# SSH_PASSWORD = "password"
# cli = paramiko.SSHClient()
# connected = False

# def cc(cmd):
#     global cli, connected
    
#     if not connected:
#         cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         cli.connect(SERVER_IP, username=SSH_USER, password=SSH_PASSWORD, port=22, timeout=30)
#         connected = True
#         print("SSH 연결 성공\n")
    
#     (stdin, stdout, stderr) = cli.exec_command(cmd)
#     return stdout

# def pp(stdout):
#     for i in stdout:
#         print(i, end='')