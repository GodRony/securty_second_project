import paramiko

#===================================================================
# import값 대신 사용할 임시 변수들 (클래스 밖)
#===================================================================

FTP_USER = "ftpuser"
FTP_PASS = "asd123!@"
FTP_HOME = "/home/ftpuser"
ANONYMOUS_ENABLE = "NO"
CHROOT_ENABLE = "YES"
FTP_GROUP = "ftpgroup"

#===================================================================
# FTP 클래스
#===================================================================
class Ftp():
    
    def __init__(self):
        # FTP 전역 변수에서 복사
        self.ftp_user = FTP_USER
        self.ftp_pass = FTP_PASS
        self.ftp_home = FTP_HOME
        self.anonymous_enable = ANONYMOUS_ENABLE
        self.chroot_enable = CHROOT_ENABLE
        
        # SFTP 전역 변수에서 복사
        self.sftp_user = SFTP_USER
        self.sftp_pass = SFTP_PASS
        self.sftp_home = SFTP_HOME
        self.sftp_group = SFTP_GROUP
        
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
dnf install -y vsftpd
rpm -qa | grep vsftpd
systemctl enable vsftpd
systemctl start vsftpd
systemctl status vsftpd
"""
        return cmd
        
#===================================================================        
    
    def on_off(self):
        print("1. FTP 서비스 시작")
        print("2. FTP 서비스 중지")
        choice = input("선택: ")
        
        if choice == "1":
            cmd = """
systemctl enable vsftpd
systemctl start vsftpd
systemctl status vsftpd
"""
        elif choice == "2":
            cmd = """
systemctl stop vsftpd
systemctl disable vsftpd
systemctl status vsftpd
"""
        else:
            return "echo '잘못된 선택입니다.'"
        
        return cmd
        
#===================================================================        
    
    def set_ftp_config(self):
        cmd = f"""
cp /etc/vsftpd/vsftpd.conf /etc/vsftpd/vsftpd.conf.backup

cat > /etc/vsftpd/vsftpd.conf << 'EOF'
anonymous_enable={self.anonymous_enable}
local_enable=YES
write_enable=YES
local_umask=022
dirmessage_enable=YES
xferlog_enable=YES
connect_from_port_20=YES
xferlog_std_format=YES
chroot_local_user={self.chroot_enable}
listen=YES
pam_service_name=vsftpd
userlist_enable=YES
tcp_wrappers=YES
EOF

cat /etc/vsftpd/vsftpd.conf
systemctl restart vsftpd
"""
        return cmd
        
#===================================================================        
    
    def add_ftp_user(self):
        cmd = f"""
useradd ftpuser -d /home/ftpuser -s /sbin/nologin
echo 'ftpuser:{self.ftp_pass}' | chpasswd
chown -R ftpuser:ftpuser /home/ftpuser
chmod -R 755 /home/ftpuser
echo 'FTP 사용자 생성 완료'
"""
        return cmd
        
#===================================================================        
    
    def set_sftp_config(self):
        cmd = f"""
groupadd sftpgroup

useradd -g sftpgroup -s /sbin/nologin -d /home/sftpuser sftpuser
echo 'sftpuser:{self.sftp_pass}' | chpasswd

mkdir -p /home/sftpuser/upload
chown root:root /home/sftpuser
chmod 755 /home/sftpuser
chown sftpuser:sftpgroup /home/sftpuser/upload
chmod 755 /home/sftpuser/upload

cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

cat >> /etc/ssh/sshd_config << 'EOF'

Match Group sftpgroup
    ChrootDirectory /home/%u
    ForceCommand internal-sftp
    AllowTcpForwarding no
    X11Forwarding no
EOF

sshd -t
systemctl restart sshd
echo 'SFTP 설정 완료'
"""
        return cmd
        
#===================================================================        
    
    def chk_ftp_config(self):
        cmd = """
echo '=== FTP 설정 파일 ==='
cat /etc/vsftpd/vsftpd.conf
echo '=== FTP 서비스 상태 ==='
systemctl status vsftpd
"""
        return cmd
        
#===================================================================        
    
    def chk_sftp_config(self):
        cmd = """
echo '=== SSH/SFTP 설정 파일 (마지막 5줄) ==='
tail -5 /etc/ssh/sshd_config
echo '=== SFTP 서비스 상태 ==='
systemctl status sshd
echo '=== SFTP 사용자 확인 ==='
getent group sftpgroup
"""
        return cmd
        
#===================================================================        
    
    def chk_ftp_log(self):
        cmd = """
echo '=== FTP 로그 ==='
tail -50 /var/log/vsftpd.log 2>/dev/null || echo 'FTP 로그 파일이 없습니다.'
"""
        return cmd
        
#===================================================================        
    
    def chk_sftp_log(self):
        cmd = """
echo '=== SFTP 로그 ==='
tail -50 /var/log/secure 2>/dev/null | grep -i sftp || echo 'SFTP 로그가 없습니다.'
"""
        return cmd
        
#===================================================================        
    
    def backup(self):
        cmd = """
mkdir -p /root/backup/ftp_sftp
cp /etc/vsftpd/vsftpd.conf /root/backup/ftp_sftp/vsftpd.conf.backup 2>/dev/null || echo 'FTP 설정 파일 없음'
cp /etc/ssh/sshd_config /root/backup/ftp_sftp/sshd_config.backup
ls -lh /root/backup/ftp_sftp/
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