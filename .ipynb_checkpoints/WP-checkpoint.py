class WP:
    def __init__(self):
        print("WP init 시작")

    def install_prev_packages(self):
        return "dnf -y install wget; dnf -y install unzip"

    def install_and_move_dir():
        commands = """
cd ~
wget https://ko.wordpress.org/latest-ko_KR.zip
mkdir wp
mv latest-ko_KR.zip ./wp
cd wp
unzip latest-ko_KR.zip
cd wordpress
useradd wp
mv * /home/wp
cd /home
chmod 755 -R wp
chown -R wp:wp wp
        """
        return commands

    def set_wp_config_php_client():
        db_name = input("만들 db 이름을 입력해주세요. ex) test_db : ")
        user_name = input("만들 db 유저의 이름을 입력해주세요 ex) test_user : ")
        user_pw = input("password를 입력해주세요 ex. test_passwd : ")
        ip = input("DB에 연결할 DB_HOST IP를 입력해주세요 : ")
        commands = f"""
cd /home/wp
mv wp-config-sample.php wp-config.php
sed -i "s|define( 'DB_NAME', 'database_name_here' );|define( 'DB_NAME', '{db_name}' );|" wp-config.php
sed -i "s|define( 'DB_USER', 'username_here' );|define( 'DB_USER', '{user_name}' );|" wp-config.php
sed -i "s|define( 'DB_PASSWORD', 'password_here' );|define( 'DB_PASSWORD', '{user_pw}' );|" wp-config.php
sed -i "s|define( 'DB_HOST', 'localhost' );|define( 'DB_HOST', '{ip}' );|" wp-config.php
"""
        return commands

    def allow_mariadb_at_remote_server():
        
        mariadb_check = input("mariadb와 php가 존재해야합니다 있으면 yes를 입력해주세요.")
        
        if(mariadb_check != "yes") :
            return
        commands = """
        cat << EOF >> /etc/my.cnf
        [mysqld]
        bind-address = 0.0.0.0 
        EOF
        systemctl restart mariadb
        """
        return commands
