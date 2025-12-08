class MariaDB:
    def __init__(self):
        print("MariaDB init start")

    def install_packages(self):
        print("필요 패키지들을 설치합니다")
        cmd =  """
        sudo dnf install -y expect
        dnf -y install dnf-plugins-core epel-release expect
        dnf install -y https://rpms.remirepo.net/enterprise/remi-release-9.rpm
        dnf module reset php -y
        dnf module enable php:remi-8.4 -y
        """
        return cmd

    def install_apache_and_php(self):
        print("apache와 php도 같이 설치합니다.")
        cmd = r"""
        bash -c 'dnf -y install httpd php php-fpm php-mysqlnd php-cli php-common php-devel \
        php-mbstring php-xml php-gd php-json php-intl php-zip php-opcache && \
        systemctl enable --now httpd php-fpm'
        """
        return cmd
    
    def install_mariaDB(self):
        print("mariaDB를 설치합니다.")
        cmd = """
        sudo dnf install -y mariadb-server
        sudo systemctl enable mariadb --now
        sudo dnf install -y mariadb-server-utils
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
        cmd = f"""
sudo systemctl restart mariadb
dnf -y install phpmyadmin
"""
        return cmd
    def set_phpMyadmin_conf(self):
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
        return cmd