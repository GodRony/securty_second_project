class DnsVhost:
    def __init__(self):
        print("DnsVhost init start")
        self.VHOST_CONF = ""
        self.SERVER_NAME = ""
        self.Third_domain = ["ns","wp","jl"]
        self.ZONE_FILE = ""
        self.IPADDR = ""
        self.httpd_install = False

    def getter_Third_domain(self) :
        return self.Third_domain

    def getter_VHOST_CONF(self) :
        return self.VHOST_CONF

    def getter_SERVER_NAME(self) :
        return self.SERVER_NAME

    def getter_ZONE_FILE(self) :
        return self.ZONE_FILE

    def test(self):
        return "touch test.text"

############## http ###############    
    def install_http(self):
        ## Rocky
        cmd = "dnf -y install httpd ; systemctl enable --now httpd ; dnf install expect -y"
        self.httpd_install = True
        return cmd        


    def set_vhostconf(self):
        self.VHOST_CONF = f"/etc/httpd/conf.d/vhost.conf"
        self.SERVER_NAME = input("ServerName을 입력하세요. (예: test.com , ppp.com): ")
        return f"touch {self.VHOST_CONF}"

    def show_vhostconf(self):
        print(f"현재 {self.VHOST_CONF}의 내용은 아래와 같습니다")
        return f"cat {self.VHOST_CONF}"
    
    def mod_vhostconf(self):
#        
        WEB_DOCUMENT_ROOT = input("사용할 웹 디렉토리를 입력하세요 (예: /home/team1 또는 /var/www/young): ").strip()
        third_domain = input("3차 도메인을 입력해주세요. ServerName 생성시 필요합니다. (예: ns, wp, jl 등..): ")
        self.Third_domain.append(third_domain)
        ERROR_LOG = input("ErrorLog 경로를 입력하세요 (예: /var/log/httpd/test_error.log): ")
        CUSTOM_LOG = input("CustomLog 경로를 입력하세요 (예: /var/log/httpd/test_access.log): ")
        
        cmd = f"""
mkdir -p {WEB_DOCUMENT_ROOT} && chmod 755 {WEB_DOCUMENT_ROOT}
echo '<h1>This is index.html for Test by mk_index func</h1>' > {WEB_DOCUMENT_ROOT}/index.html

cat <<EOF >> "{self.VHOST_CONF}"
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    ServerName {third_domain}.{self.SERVER_NAME}
    DocumentRoot {WEB_DOCUMENT_ROOT}
    
    <Directory {WEB_DOCUMENT_ROOT}>
        AllowOverride None
        Options Indexes FollowSymLinks
        Require all granted
    </Directory>

    ErrorLog {ERROR_LOG}
    CustomLog {CUSTOM_LOG} combined
</VirtualHost>
EOF

"""
        return cmd

    def set_reverse_proxy_vhostconf(self,third_domain):
        self.VHOST_CONF = f"/etc/httpd/conf.d/vhost.conf"
        self.SERVER_NAME = input("ServerName을 입력하세요. (예: test.com , ppp.com): ")
        
        cmd = f"""
cat << EOF >> "/etc/httpd/conf.d/vhost.conf"
<VirtualHost *:80>
    ServerName {third_domain}.{self.SERVER_NAME}
    ProxyRequests off 
    ProxyPass / http://localhost:8080/ 
    ProxyPassReverse / http://localhost:8080/ 
    ErrorLog "/var/log/httpd/tom_error_log"
    CustomLog "/var/log/httpd/tom_access_log" combined
</VirtualHost>
"""
        
    def restart_http(self):
        print("httpd restart 시작")
        return "sudo systemctl restart httpd"

        
############### dns ##################
    def install_named(self):
        print("dns를 위한 named를 설치하겠습니다")
        return "dnf -y install bind bind-utils"

    def set_named_conf(self):
        print("named.conf 파일을 수정합니다~")
        cmd = r"""
NAMED_CONF="/etc/named.conf"
sed -i 's/listen-on[[:space:]]*port 53[[:space:]]*{[[:space:]]*127\.0\.0\.1;[[:space:]]*};/listen-on port 53 { any; };/' "$NAMED_CONF"
sed -i 's/allow-query[[:space:]]*{[[:space:]]*localhost;[[:space:]]*};/allow-query { any; };/' "$NAMED_CONF"
    """
        return cmd

    def set_named_rfc(self):

        if(self.httpd_install == False) :
            self.SERVER_NAME = input("Server Name을 입력하세요. (ex. test.com) : ")
            self.ZONE_NAME = input("생성할 zone name을 입력하세요. (ex. test.com) : ")
            self.ZONE_FILE = f"{self.ZONE_NAME}.zone"
            print(f"ZONE_FILE 이름 {self.ZONE_FILE}로 생성하겠습니다.")
        
        else :    
            my_server_name = self.getter_SERVER_NAME()
            print(f"현재 당신이 사용하는 server name은 {my_server_name}입니다.")
            print(f"ZONE FILE 생성 : {my_server_name}.zone ")
            print(f"ZONE NAME : {my_server_name}")
            
            self.ZONE_FILE = f"{my_server_name}.zone"
            ZONE_NAME = my_server_name

        cmd = f'''
cat >> /etc/named.rfc1912.zones <<EOF
zone "{ZONE_NAME}" IN {{
    type master;
    file "{self.ZONE_FILE}";
    allow-update {{ none; }};
}};
EOF
'''
        print("zone이  /etc/named.rfc1912.zones에 추가되었습니다.")
        return cmd

    def mk_zone_file(self):
        print(f"zone 파일이 생성되었습니다: /var/named/{self.ZONE_FILE}")
        return  f"touch /var/named/{self.ZONE_FILE}"

    def set_zone_file(self):
        print("zone file의 내용을 수정하겠습니다.")
        domain = f"ns.{self.SERVER_NAME}"
        self.IPADDR = input("현재 사용하고 있는 DNS의 ip: ")
    
        contents = f"""$TTL    604800
@       IN      SOA     {domain}. root.adminemail.com. (
                              2         ; Serial
                         604800         ; Refresh
                          86400         ; Retry 
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@       IN      NS      {domain}.
ns       IN      A       {self.IPADDR}
@       IN      AAAA    ::1
"""

        print("zone file 내용 수정 완료")
    
        return f"""cat << 'EOF' > /var/named/{self.ZONE_FILE}
{contents}
EOF
"""

    

    def set_dns_Third_domain(self):
        third_domains = self.getter_Third_domain()
        contents = ""
        for third in third_domains:
            contents += f"{third}        IN        A        {self.IPADDR}\n"
        
        return f"""cat << 'EOF' >> /var/named/{self.ZONE_FILE}
{contents}
EOF
"""
    def set_dns_Third_domain_with_params(self,third_domain):
        self.IPADDR = input("사용할 DNS의 ip: ")
        contents += f"{third}        IN        A        {self.IPADDR}\n"
        self.ZONE_NAME = input("생성할 zone name을 입력하세요. (ex. test.com) : ")
        self.ZONE_FILE = f"{self.ZONE_NAME}.zone"
        return f"""
cat << 'EOF' >> /var/named/{self.ZONE_FILE}
{contents}
EOF
"""
        
    def start_dns(self):
        return "systemctl restart named"


