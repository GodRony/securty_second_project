class FTP():
    def __init__(self, os):
        self.os = os
        self.ftp_group = "" 
        self.backup_dir = ""
        self.ftp_log = "" 
        self.ftp_user = ""
        self.ftp_home = ""
        
###################################################
#                       FTP                       # 
###################################################
    def install_ftp(self):
        cmd = ""
        if self.os == "Rocky":
            cmd = """
dnf install -y vsftpd
"""
        elif self.os == "Ubuntu" :  
            cmd = """
apt update
apt install -y vsftpd
"""
        else:
            print("지원하지 않는 OS입니다.")
        return cmd
        
    def on_off_ftp(self):
        print("1. FTP 서비스 시작")
        print("2. FTP 서비스 중지")
        choice = input("선택: ")
        
        if choice == "1":
            cmd = """
systemctl enable vsftpd
systemctl start vsftpd
"""
        elif choice == "2":
            cmd = """
systemctl stop vsftpd
systemctl disable vsftpd
"""
        else:
            return "echo '잘못된 선택입니다.'"
        
        return cmd
        
    def set_ftp_config(self):
        config_path = ""
        if self.os == "Rocky":
            config_path = "/etc/vsftpd/vsftpd.conf"
        
        elif self.os == "Ubuntu":
            config_path = "/etc/vsftpd.conf"
        
        anonymous_enable = input("아이디/비밀번호 없이 접속을 허용하겠습니까? YES or NO (ex. YES)")
        
        cmd = f"""
cp {config_path} {config_path}.backup

cat > {config_path} << 'EOF'
anonymous_enable={anonymous_enable}
local_enable=YES
write_enable=YES
local_umask=022
xferlog_enable=YES
connect_from_port_20=YES
xferlog_std_format=YES
chroot_local_user=NO
listen=NO
listen_ipv6=YES
pam_service_name=vsftpd
userlist_enable=NO
EOF
cat {config_path}
systemctl restart vsftpd
"""
        return cmd
        
    def add_ftpuser(self):
        self.ftp_user = input("ftp user 이름을 만듭니다. 이름을 입력해주세요. (ex. ftpuser): ")
        self.ftp_home = f"/home/{self.ftp_user}"

        # 사용자 없으면 생성
        return f"id -u {self.ftp_user} >/dev/null 2>&1 || useradd -m {self.ftp_user}"

    def set_ftpuser_passwd(self) :
        # Expect 스크립트 파일 생성
        cmd = f"""
cat <<EOF > /root/mk_ftpuser.exp
#!/usr/bin/expect -f
set timeout -1
spawn passwd {self.ftp_user}
expect "New password:"
send "asd123!@\\r"
expect "Retype new password:"
send "asd123!@\\r"
expect eof
EOF
chmod +x /root/mk_ftpuser.exp
/usr/bin/expect /root/mk_ftpuser.exp
"""
        return cmd
        
    def set_dir(self):
        cmd = f"""
        chown -R {self.ftp_user}:{self.ftp_user} {self.ftp_home}
        chmod -R 755 {self.ftp_home}
"""    
        return cmd
  
    def chk_log(self):
        cmd = f"""
tail -50 {self.ftp_log} 2>/dev/null || echo 'FTP 로그 파일이 없습니다.'
"""
        return cmd
        
###################################################
#                       SFTP                      # 
###################################################    
    
    def set_sftp_config(self):
        if self.os == "Rocky":
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

