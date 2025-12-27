class WP:
    def __init__(self,os):
        self.os = os

    def install_prev_packages(self):
        cmd = ""
        if self.os == "Rocky":
            cmd ="dnf -y install wget; dnf -y install unzip"
        elif self.os == "Ubuntu":
            cmd = "apt -y install wget; apt -y install unzip; apt install php-mysql"
        else:
            cmd=""
            print("지원하지 않는 OS입니다.")
        return cmd

    def install_and_move_dir(self):
        print("wp를 설치합니다.")
        commands = """
cd ~
wget https://ko.wordpress.org/latest-ko_KR.zip
mkdir -p wp
mv latest-ko_KR.zip ./wp
cd wp
unzip latest-ko_KR.zip
cd wordpress
useradd wp
mkdir -p /home/wp
mv * /home/wp
cd /home
chmod 755 -R wp
chown -R wp:wp wp
        """
        return commands

    def set_wp_config_php_client(self):
        db_name = input("만들 db 이름을 입력해주세요. ex) test : ")
        user_name = input("만들 db 유저의 이름을 입력해주세요 ex) test : ")
        user_pw = input("password를 입력해주세요 ex. asd123!@ : ")
        ip = input("DB에 연결할 DB_HOST IP를 입력해주세요 (원격의 경우 172.16.254.20) : ")
        commands = f"""
cd /home/wp
mv wp-config-sample.php wp-config.php
sed -i "s|define( 'DB_NAME', 'database_name_here' );|define( 'DB_NAME', '{db_name}' );|" wp-config.php
sed -i "s|define( 'DB_USER', 'username_here' );|define( 'DB_USER', '{user_name}' );|" wp-config.php
sed -i "s|define( 'DB_PASSWORD', 'password_here' );|define( 'DB_PASSWORD', '{user_pw}' );|" wp-config.php
sed -i "s|define( 'DB_HOST', 'localhost' );|define( 'DB_HOST', '{ip}' );|" wp-config.php
"""
        return commands

