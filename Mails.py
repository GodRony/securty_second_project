class Mails:
    def __init__(self, os):
        self.os = os
        self.domain = "" 
    
    def setter_domain(self,domain):
        self.domain = domain
        
    def install_mails(self) :
        print("postfix, dovecot, roundcube, mutt 모두 설치합니다.")
        if(self.os == "Rocky"):
            return "dnf install -y postfix; dnf install -y dovecot; dnf install -y roundcubemail; dnf install -y mutt; dnf install -y expect"
        elif(self.os == "Ubuntu"):
            return "apt install unzip"
    

    def set_postfix_conf(self):
        print("postfix 설정파일을 설정합니다")
        conf = "/etc/postfix/main.cf"
        cmd = f"""
useradd post || true
echo "post:post" | chpasswd

sed -i "s|#myhostname = host.domain.tld|myhostname = post.{self.domain}|g" {conf}
sed -i "s|#mydomain = domain.tld|mydomain = {self.domain}|g" {conf}
sed -i "s|#myorigin = \\$mydomain|myorigin = \\$mydomain|g" {conf}
sed -i "s|#inet_interfaces = all|inet_interfaces = ipv4|g" {conf}
sed -i "s|mydestination = \\$myhostname, localhost.\\$mydomain, localhost|mydestination = \\$myhostname, localhost.\\$mydomain, localhost, \\$mydomain|" {conf}
sed -i "s|#home_mailbox = Maildir/|home_mailbox = Maildir/|g" {conf}

systemctl enable --now postfix
"""
        return cmd


    def set_dovecot_conf(self):
        print("dovecot 설정파일을 설정합니다, 테스트용 mutt도 설치합니다.")
        conf_dovecot = "/etc/dovecot/dovecot.conf"
        conf_10_mail = "/etc/dovecot/conf.d/10-mail.conf"
        conf_10_auth = "/etc/dovecot/conf.d/10-auth.conf"
        cmd = f"""
sed -i "s|#protocols = imap pop3 lmtp submission|protocols = imap pop3 lmtp submission|g" {conf_dovecot}
sed -i "s|#   mail_location = maildir:~/Maildir|    mail_location = maildir:~/Maildir|g" {conf_10_mail}
sed -i "s|#disable_plaintext_auth = yes|disable_plaintext_auth = no|g" {conf_10_auth}
systemctl enable --now dovecot
dnf install -y mutt
        """
        print(f'mutt -s "Mail Test" post@{self.domain}로 테스트 해보세요. y, Enter, Enter, :wq')
        return cmd

    def set_roundcube(self):
        print("dovecot 설정파일을 설정합니다, 테스트용 mutt도 설치합니다.")
        conf =  "/etc/roundcubemail/config.inc.php"
        islocal = input("local에서 테스트 합니까? 맞으면 y, 원격 DB이면 n을 누르세요 (y or n) ex. y : ")
        mk_local_db_cmd = " "
        
        db_host_ip = " "
        db_host_pw =  " "
        
        if(islocal == "y") :
            print("local일 경우에, 자동으로 DB를 만듭니다. db 이름 : cube, user : cube@localhost , pw : asd123!@")
            db_host_pw = input("DB 서버 pw ex. asd123!@ : ")
            db_name = "cube"
            mk_local_db_cmd = f"""
cat <<EOF > /root/set_roundcube.exp
#!/usr/bin/expect -f

set timeout 10

spawn mysql -uroot -p
expect "Enter password:"
send "{db_host_pw}\\r"

expect "*MariaDB*"
send "create database cube;\\r"

expect "*MariaDB*"
send "create user 'cube'@'localhost' identified by 'asd123!@';\\r"

expect "*MariaDB*"
send "grant all privileges on cube.* to 'cube'@'localhost';\\r"

expect "*MariaDB*"
send "flush privileges;\\r"

expect "*MariaDB*"
send "quit;\\r"

expect eof
EOF

chmod +x /root/set_roundcube.exp
/usr/bin/expect /root/set_roundcube.exp
"""

            set_db_cmd = f"mysql -uroot -p'{db_host_pw}' cube < /usr/share/roundcubemail/SQL/mysql.initial.sql"
            db_host_pw = "asd123%21%40"

        elif(islocal == "n") :
            db_host_ip = input("DB host 서버 ip ex. 172.16.16.100 : ")
            db_host_pw = input("DB host 서버 pw ex. asd123 (**주의 이때 비밀번호에 특수문자가 포함되어있으면 안됩니다. 다시 DB서버 담당자에게 비밀번호 변경요청 바랍니다.): ")
            db_name = input("DB 이름을 입력해주세요")
            set_db_cmd = f"mysql -h {db_host_ip} -P 3306 -u {db_name} -p'{db_host_pw}' {db_name} < /usr/share/roundcubemail/SQL/mysql.initial.sql"
        else : 
            print("잘못된 입력입니다.")
            return " "
        cmd = f"""
        dnf install -y roundcubemail
        {mk_local_db_cmd}
        {set_db_cmd}
mv /etc/roundcubemail/config.inc.php.sample /etc/roundcubemail/config.inc.php
sed -i "s|mysql://roundcube:pass@localhost/roundcubemail|mysql://{db_name}:{db_host_pw}@localhost/cube|g" {conf}


sed -i 's/Require local/Require all granted/g' /etc/httpd/conf.d/roundcubemail.conf
systemctl restart httpd
        """
        return cmd
        
    