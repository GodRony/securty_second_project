import paramiko

#===================================================================
# import값 대신 사용할 임시 변수들 (클래스 밖)
#===================================================================

GATEWAY = "172.16.0.1"

MIN_RENT = 100        
MAX_RENT = 600    
NETWORK_NI = "172.16.5.0"
NETWORK_SUB = "255.255.0.0"

RANGE_IP = [
    ("172.16.5.40", "172.16.5.42"),
    ("172.16.5.46", "172.16.5.50")
]

STATIC_HOSTS = [
    ("1.1.1.1", "aa:bb:cc:dd:ee:ff"),
    ("1.1.1.2", "11:22:33:44:55:66")
]

#===================================================================
# DHCP 클래스
#===================================================================
class Dhcp():
    
    def __init__(self):
        
        self.gateway = GATEWAY
        self.min_rent = MIN_RENT
        self.max_rent = MAX_RENT
        self.network_ni = NETWORK_NI
        self.network_sub = NETWORK_SUB
        self.range_ip = RANGE_IP
        self.static_hosts = STATIC_HOSTS
        
#===================================================================
    
    def chk_os(self):
        cmd = """
cat /etc/os-release | grep PRETTY_NAME
hostnamectl
ip addr
"""
        return cmd        
        
#===================================================================
    
    def install(self):
        cmd = """
dnf install -y dhcp-server
rpm -qa | grep dhcp-server
"""
        return cmd
        
#===================================================================        
    
    def on_off(self):
        print("1. DHCP 서비스 시작")
        print("2. DHCP 서비스 중지")
        choice = input("선택: ")
        
        if choice == "1":
            cmd = """
systemctl enable dhcpd
systemctl start dhcpd
systemctl status dhcpd
"""
        elif choice == "2":
            cmd = """
systemctl stop dhcpd
systemctl disable dhcpd
systemctl status dhcpd
"""
        else:
            return "echo '잘못된 선택입니다.'"
        
        return cmd
        
#===================================================================        
    
    def option(self):
        pass
        
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
systemctl restart dhcpd
"""
        return cmd
        
#===================================================================        
    
    def ins_pool(self):
        # Range IP 추가 로직 구현
        pass
        
#===================================================================        
    
    def del_pool(self):
        print("현재 Range 목록:")
        
        for i in range(len(self.range_ip)):
            print(f"  {i+1}. {self.range_ip[i][0]} ~ {self.range_ip[i][1]}")
        
        choice = int(input("삭제할 번호: ")) - 1
        
        if 0 <= choice < len(self.range_ip):
            target_start = self.range_ip[choice][0]
            target_end = self.range_ip[choice][1]
            
            cmd = f"""
sed -i '/range {target_start} {target_end}/d' /etc/dhcp/dhcpd.conf
cat /etc/dhcp/dhcpd.conf
systemctl restart dhcpd
"""
            
            del self.range_ip[choice]
            print(f"\n{target_start} ~ {target_end} Range 삭제 완료")
            return cmd
        else:
            return "echo '잘못된 번호입니다.'"
        
#===================================================================        
    
    def chk_pool(self):
        cmd = """
echo '=== DHCP 설정 파일 ==='
cat /etc/dhcp/dhcpd.conf
echo ''
echo '=== Lease 정보 ==='
cat /var/lib/dhcpd/dhcpd.leases | tail -20
"""
        return cmd
        
#===================================================================        
    
    def backup(self):
        cmd = """
mkdir -p /root/backup/dhcp
cp /etc/dhcp/dhcpd.conf /root/backup/dhcp/dhcpd.conf.backup
cp /var/lib/dhcpd/dhcpd.leases /root/backup/dhcp/dhcpd.leases.backup
ls -lh /root/backup/dhcp/
"""
        return cmd
        
#===================================================================

    def set_log(self):
        cmd = """
grep -i dhcp /var/log/messages > /var/log/dhcpd.log
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

    
        
# 필요한 변수
# ======================
# 사용 OS
# DHCP 구성 요소
#     본인 IP
#     기본 임대 시간
#     최대 임대 시간
#     구성할 대역(NI와 서브넷)
#     제외할 대역
#     고정 IP / 반영하는 MAC 주소
# 옵션 라우터
# 옵션 DNS서버
# ======================
# 메소드


# OS 구분
#     Rocky or Ubuntu?

# 설치 / 중복 확인
#     중복 확인

#     if  dpkg -l | grep [패키지명] / dnf list installed | grep [패키지명] is true:
#         pass
#     else
#         apt install / dnf install
#     설치

# 기능 활성화 / 정지
#     활성화
#     비활성화
#     재시작

# 기본 설정 / 동작
#     기본 옵션
#     특정 부분 편집 / 추가

# 설정파일 백업
#     설정 디렉터리.bak

# 풀 생성 / 삭제
    
#     풀 설정 디렉터리

#     생성 OR 삭제 여부

#     구성 대역 설정    
#     제외 대역 설정    
#     고정 IP(반영할 MAC주소)
#     내용 양식 추가

#     이름 중복시 경고

# 풀 수정
    
#     풀 설정 디렉터리
    
#     구성 대역 설정    
#     제외 대역 설정    
#     고정 IP(반영할 MAC주소)
#     내용 양식 추가

#     수정 확인

# 풀 확인

# 로그 설정
#     로그를 저장할 디렉터리 설정

# 로그 확인
#     확인하고 싶은 로그 부분 설정


