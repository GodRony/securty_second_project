import paramiko
from CC import CC

#===================================================================
# 생성자 예시
#===================================================================
"""
ftp = Ftp(
    os="rocky9",
    ftp_user="ftpuser",
    ftp_pass="asd123!@",
    ftp_home="/home/ftpuser",
    anonymous_enable="NO",
    chroot_enable="YES",
    ftp_group="ftpgroup",
    backup_dir="/root/backup/ftp_sftp",
    ftp_log="/var/log/vsftpd.log"
)
"""

#===================================================================
# FTP 클래스
#===================================================================
class Ftp():
    
    def __init__(self, os, ftp_user, ftp_pass, ftp_home, anonymous_enable, chroot_enable, ftp_group, backup_dir, ftp_log):
        self.os = os
        self.ftp_user = ftp_user
        self.ftp_pass = ftp_pass
        self.ftp_home = ftp_home
        self.anonymous_enable = anonymous_enable
        self.chroot_enable = chroot_enable
        self.ftp_group = ftp_group
        self.backup_dir = backup_dir
        self.ftp_log = ftp_log
        
#===================================================================
    
    def install(self):
        if self.os == "rocky9":
            cmd = """
dnf install -y vsftpd
rpm -qa | grep vsftpd
systemctl enable vsftpd
systemctl start vsftpd
systemctl status vsftpd
"""
        else:  # ubuntu
            cmd = """
apt update
apt install -y vsftpd
dpkg -l | grep vsftpd
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
        if self.os == "rocky9":
            config_path = "/etc/vsftpd/vsftpd.conf"
        else:
            config_path = "/etc/vsftpd.conf"
        
        cmd = f"""
cp {config_path} {config_path}.backup

cat > {config_path} << 'EOF'
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

cat {config_path}
systemctl restart vsftpd
"""
        return cmd
        
#===================================================================        
    
    def add_user(self):
        if self.os == "rocky9":
            nologin_path = "/sbin/nologin"
        else:
            nologin_path = "/usr/sbin/nologin"
        
        cmd = f"""
useradd {self.ftp_user} -d {self.ftp_home} -s {nologin_path}
echo '{self.ftp_user}:{self.ftp_pass}' | chpasswd
chown -R {self.ftp_user}:{self.ftp_user} {self.ftp_home}
chmod -R 755 {self.ftp_home}
echo 'FTP 사용자 생성 완료'
"""
        return cmd
        
#===================================================================        
    
    def set_sftp_config(self):
        if self.os == "rocky9":
            nologin_path = "/sbin/nologin"
        else:
            nologin_path = "/usr/sbin/nologin"
        
        cmd = f"""
groupadd {self.ftp_group}

useradd -g {self.ftp_group} -s {nologin_path} -d /home/sftpuser sftpuser
echo 'sftpuser:{self.ftp_pass}' | chpasswd

mkdir -p /home/sftpuser/upload
chown root:root /home/sftpuser
chmod 755 /home/sftpuser
chown sftpuser:{self.ftp_group} /home/sftpuser/upload
chmod 755 /home/sftpuser/upload

cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

cat >> /etc/ssh/sshd_config << 'EOF'

Match Group {self.ftp_group}
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
        if self.os == "rocky9":
            config_path = "/etc/vsftpd/vsftpd.conf"
        else:
            config_path = "/etc/vsftpd.conf"
        
        cmd = f"""
echo '=== FTP 설정 파일 ==='
cat {config_path}
echo '=== FTP 서비스 상태 ==='
systemctl status vsftpd
"""
        return cmd
        
#===================================================================        
    
    def chk_sftp_config(self):
        cmd = f"""
echo '=== SSH/SFTP 설정 파일 ==='
tail -5 /etc/ssh/sshd_config
echo '=== SFTP 서비스 상태 ==='
systemctl status sshd
echo '=== SFTP 사용자 확인 ==='
getent group {self.ftp_group}
"""
        return cmd
        
#===================================================================        
    
    def chk_log(self):
        cmd = f"""
echo '=== FTP 로그 ==='
tail -50 {self.ftp_log} 2>/dev/null || echo 'FTP 로그 파일이 없습니다.'
"""
        return cmd
        
#===================================================================        
    
    def chk_sftp_log(self):
        if self.os == "rocky9":
            log_path = "/var/log/secure"
        else:
            log_path = "/var/log/auth.log"
        
        cmd = f"""
echo '=== SFTP 로그 ==='
tail -50 {log_path} 2>/dev/null | grep -i sftp || echo 'SFTP 로그가 없습니다.'
"""
        return cmd
        
#===================================================================        
    
    def backup(self):
        if self.os == "rocky9":
            config_path = "/etc/vsftpd/vsftpd.conf"
        else:
            config_path = "/etc/vsftpd.conf"
        
        cmd = f"""
mkdir -p {self.backup_dir}
cp {config_path} {self.backup_dir}/vsftpd.conf.backup 2>/dev/null || echo 'FTP 설정 파일 없음'
cp /etc/ssh/sshd_config {self.backup_dir}/sshd_config.backup
ls -lh {self.backup_dir}/
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