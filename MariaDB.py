class MariaDB:
    def __init__(self,os):
        print("MariaDB init start")
        self.os = os

    def install_packages(self):
        print("필요 패키지들을 설치합니다")
        cmd = ""
        if(self.os == "Rocky"):
            cmd = """
        sudo dnf install -y expect
        dnf -y install dnf-plugins-core epel-release expect
        dnf install -y https://rpms.remirepo.net/enterprise/remi-release-9.rpm
        dnf module reset php -y
        dnf module enable php:remi-8.4 -y
"""
        elif(self.os == "Ubuntu"):
            cmd = """
        apt install -y expect
        apt install software-properties-common -y
        apt install dpkg -y
        add-apt-repository ppa:ondrej/php -y
        apt install php -y
        apt install php8.4 libapache2-mod-php8.4 -y
        a2enmod php8.4
"""
        else : 
            print("지원하지 않는 OS입니다.")
            
        return cmd    

    def install_apache_and_php(self):
        print("apache와 php도 같이 설치합니다.")
        cmd = ""
        if(self.os == "Rocky"):
            cmd = r"""
            bash -c 'dnf -y install httpd php php-fpm php-mysqlnd php-cli php-common php-devel \
            php-mbstring php-xml php-gd php-json php-intl php-zip php-opcache && \
            systemctl enable --now httpd php-fpm'
            """
        elif(self.os == "Ubuntu"):
            cmd = "apt -y install apache2"
        else : 
            print("지원하지 않는 OS입니다.")
            
        return cmd        

    
    def install_mariaDB(self):
        print("mariaDB를 설치합니다.")
        cmd = ""
        if(self.os == "Rocky"):
            cmd = """
            sudo dnf install -y mariadb-server
            sudo systemctl enable mariadb --now
            sudo dnf install -y mariadb-server-utils
            """
        elif(self.os == "Ubuntu"):
            cmd = """
            apt install -y apache2 mariadb-server
            apt install -y mariadb-client-compat
            sudo systemctl enable mariadb --now
            """
        return cmd
    def init_mariaDB(self):
        print("secure_installation 시작")
        MYSQL_ROOT_PASSWORD="asd123!@"
        cmd = f'''
cat <<EOF > /root/mysql_secure.exp
#!/usr/bin/expect -f
set timeout -1
set password [lindex $argv 0]
spawn mysql_secure_installation
expect "Enter current password for root (enter for none):"
send "\\r"
expect "Switch to unix_socket authentication"
send "Y\\r"
expect "Change the root password?"
send "y\\r"
expect "New password:"
send "{MYSQL_ROOT_PASSWORD}\\r"
expect "Re-enter new password:"
send "{MYSQL_ROOT_PASSWORD}\\r"
expect "Remove anonymous users?"
send "Y\\r"
expect "Disallow root login remotely?"
send "Y\\r"
expect "Remove test database and access to it?"
send "Y\\r"
expect "Reload privilege tables now?"
send "Y\\r"
expect eof
EOF

chmod +x /root/mysql_secure.exp
/usr/bin/expect /root/mysql_secure.exp "{MYSQL_ROOT_PASSWORD}"

'''
        return cmd

    def install_php_my_admin(self):
        cmd = ""
        if(self.os == "Rocky"):
            cmd = "dnf -y install phpmyadmin"
        elif(self.os == "Ubuntu"):
            cmd = "apt -y install phpmyadmin"
        return cmd

    def set_phpMyadmin_conf(self):
        print("phpMyadmin을 설치합니다. Rocky만 지원합니다. Ubuntu는 그래픽에서 설정해야하는게 있기 때문에 지원하지 않습니다.")
        cmd = f""" cat << EOF > /etc/httpd/conf.d/phpMyadmin.conf
Alias /phpMyAdmin /usr/share/phpMyAdmin
Alias /phpmyadmin /usr/share/phpMyAdmin

<Directory /usr/share/phpMyAdmin/>
   AddDefaultCharset UTF-8

   Require all granted
</Directory>
EOF
systemctl restart httpd
systemctl enable httpd
systemctl restart php-fpm
        """
        if(self.os == "Ubuntu"):
            print("Ubuntu이기 때문에 넘어갑니다.")
            cmd = " "
        return cmd