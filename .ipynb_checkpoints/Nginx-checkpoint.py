class Nginx:

    def __init__(self, os):
        self.os = os
        self.servername = ""

    def install_nginx(self):
        cmd = """
systemctl stop httpd
dnf install nginx -y
systemctl start nginx
dnf install php php-fpm php-mysqlnd php-gd php-xml php-mbstring php-json php-intl php-zip php-curl -y
systemctl enable --now php-fpm
        """
        return cmd
        
    def set_vhostconf(self,servername):
        print(f"test.{self.servername}, test2.{self.servername}, wp.{self.servername} 이 세개만 vhost 설정 하겠습니다.")
        print("설정 경로 : /etc/nginx/conf.d/vhost.conf")
        self.servername = servername
        cmd = f"""
cat << 'EOF' > /etc/nginx/conf.d/vhost.conf
server {{
    listen 80;
    server_name test.{self.servername};
    root /home/test;
}}

server {{
    listen 80;
    server_name test2.{self.servername};
    root /home/test2;
}}

server {{
    listen 80;
    server_name wp.{self.servername};
    root /home/wp;
    index index.php index.html;

    location / {{
        try_files $uri $uri/ /index.php?$args;
    }}

    location ~ \\.php$ {{
        include fastcgi_params;
        fastcgi_pass unix:/run/php-fpm/www.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $request_filename;
    }}

    location ~* \\.(js|css|png|jpg|jpeg|gif|ico)$ {{
        expires max;
        log_not_found off;
    }}
}}
EOF
"""

        return cmd
    def restart_nginx(self):
        return "systemctl restart nginx"
        return cmd