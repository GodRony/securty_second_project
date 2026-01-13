class Cacti:
    def __init__(self,os):
        self.os = os
        self.cacti_user = ""
        self.cacti_db_pw = ""
        
    def install_cacti(self):
        cmd = ""
        if(self.os == "Rocky"):
            cmd = "dnf install cacti php-mysqlnd php-snmp rrdtool -y"
        elif(self.os == "Ubuntu"):
            cmd = " "
        else : 
            print("지원하지 않는 OS입니다.")
            
        return cmd      

    def set_mariadb_server_cnf(self):
        cmd = f"""
mv /etc/my.cnf.d/mariadb-server.cnf /etc/my.cnf.d/mariadb-server.cnf.bak
touch /etc/my.cnf.d/mariadb-server.cnf
cat << EOF > /etc/my.cnf.d/mariadb-server.cnf
[server]

[mysqld]
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
log-error=/var/log/mariadb/mariadb.log
pid-file=/run/mariadb/mariadb.pid
innodb_file_per_table = 1
innodb_flush_log_at_trx_commit = 2
innodb_buffer_pool_size = 512M
innodb_doublewrite = OFF
max_connections = 100

[galera]

[embedded]

[mariadb]

[mariadb-10.5]
EOF
"""
        return cmd

    def mk_local_cacti(self):
        islocal = input("local에서 cacti DB 및 계정을 생성하겠습니까? 맞으면 y, 로컬에서 이미 DB 및 계정을 만든경우에 n을 누르세요 (y or n) ex. y : ")
        mk_local_db_cmd = " "
        if(islocal == "y") :
            print("local일 경우에, 자동으로 DB를 만듭니다. db 이름 : cacti, user : cacti@localhost , pw : asd123!@")
            db_host_pw = input("DB 서버 pw ex. asd123!@ : ")
            mk_local_db_cmd = f"""
cat <<EOF > /root/set_cacti.exp
#!/usr/bin/expect -f

set timeout 10

spawn mysql -uroot -p
expect "Enter password:"
send "{db_host_pw}\\r"

expect "*MariaDB*"
send "create database cacti;\\r"

expect "*MariaDB*"
send "create user 'cacti'@'localhost' identified by 'asd123!@';\\r"

expect "*MariaDB*"
send "grant all privileges on cacti.* to 'cacti'@'localhost';\\r"

expect "*MariaDB*"
send "flush privileges;\\r"

expect "*MariaDB*"
send "quit;\\r"

expect eof
EOF

chmod +x /root/set_cacti.exp
/usr/bin/expect /root/set_cacti.exp
"""
        return mk_local_db_cmd

    
    def set_cacti(self):
        print("1. set_cacti 설정 시작")
        cmd = f"""
mysql -u root -p'asd123!@' cacti < /usr/share/doc/cacti/cacti.sql"""
        return cmd

    def set_cacti_db_php(self):
        print("2. /etc/cacti/db.php 설정 시작")
        conf = "/etc/cacti/db.php"
        cmd = f"""
sed -i "s|^\\$database_username.*|\\$database_username = 'cacti';|g" {conf}
sed -i "s|^\\$database_password.*|\\$database_password = 'asd123!@';|g" {conf}
"""
        return cmd

    def set_cacti_conf(self):
        print("3. /etc/httpd/conf.d/cacti.conf 설정 시작")
        conf = "/etc/httpd/conf.d/cacti.conf"
    
        cmd = f"""
    sed -i "s|^[[:space:]]*Require[[:space:]]\\+host[[:space:]]\\+localhost.*|                Require all granted|g" {conf}
    """
        return cmd
    ##########################################

    def set_my_cnf(self):
        print("4. /etc/my.cnf 설정 시작")
        cmd = f"""
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql
mv /etc/my.cnf /etc/my.cnf.bak
touch /etc/my.cnf
cat << EOF > /etc/my.cnf
[client-server]

[mysqld]
default_time_zone='Asia/Seoul'
!includedir /etc/my.cnf.d
EOF
"""    
        return cmd

    def set_timezone(self):
        print("5. timezone 설정 시작") 
        cmd = f"""
cat <<EOF > /root/set_cacti_time1.exp
#!/usr/bin/expect -f
set timeout -1
spawn mysql -u root -p -e "SET GLOBAL time_zone = 'Asia/Seoul'";
expect "Enter password:"
send "asd123!@\\r"
expect eof
EOF
chmod +x /root/set_cacti_time1.exp
/usr/bin/expect /root/set_cacti_time1.exp
"""
        return cmd
    
    def grant_timezone_to_user(self):
        print("6. timezone 설정2 시작")
        cmd = """
mariadb -u root -p'asd123!@' -e \
"GRANT SELECT ON mysql.time_zone_name TO 'cacti'@'localhost';"
"""
        return cmd

    def set_php_ini(self):
        print("7. /etc/php.ini  설정 시작")
        cmd = """
sed -i 's|;date.timezone =|date.timezone = Asia/Seoul|g' /etc/php.ini 
systemctl restart php-fpm
        """
        return cmd
    
    def restart_all(self):
        cmd = f"""
        systemctl restart mariadb&&
systemctl restart httpd &&
systemctl restart snmpd
"""
        return cmd
    def set_crond(self):
        print("8. /etc/php.ini  설정 시작")
        return "sed -i 's|^#*/5|*/5|' /etc/cron.d/cacti"


        