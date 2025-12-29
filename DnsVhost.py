class DnsVhost:
    def __init__(self,os):
        self.os = os
        
        if(self.os == "Rocky"):
            self.vhostconf = "/etc/httpd/conf.d/vhost.conf"
        elif(self.os == "Ubuntu"):
            self.vhostconf = "/etc/apache2/sites-available/vhost.conf"  
            
        self.servername = ""
        self.zonefile = ""
        self.ipaddr = ""
        self.third_domain = ""

############## http ###############    
    def install_http(self):
        cmd = ""
        if(self.os == "Rocky"):
            cmd = "dnf -y install httpd ; systemctl enable --now httpd ; dnf install expect -y; systemctl stop ufw"
        elif(self.os == "Ubuntu"):
            cmd = "apt update -y; apt install -y apache2"
        else : 
            print("지원하지 않는 OS입니다.")
            
        return cmd        


    def set_servername(self):
        self.servername = input("ServerName을 입력하세요. (예: test.com , ppp.com): ")

    def mk_vhostconf(self):
        return f"touch {self.vhostconf}"

    def test_vhost(self):
        return f"""mkdir -p /home/test && chmod 777 /home/test
echo '<h1>test</h1>' > /home/test/index.html"""

    def set_vhostconf(self,web_dir,third_domain):
        self.third_domain = third_domain
        ubuntu_cmd = " "
        http_dir = "httpd"
        if(self.os == "Ubuntu"):
            ubuntu_cmd = "a2ensite vhost.conf; a2dissite 000-default.conf; systemctl reload apache2;"
            http_dir = "apache2"
        cmd = f"""
cat <<EOF >> "{self.vhostconf}"
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    ServerName {third_domain}.{self.servername}
    DocumentRoot {web_dir}
    
    <Directory {web_dir}>
        AllowOverride None
        Options Indexes FollowSymLinks
        Require all granted
    </Directory>

    ErrorLog /var/log/{http_dir}/{third_domain}_error_log
    CustomLog /var/log/{http_dir}/{third_domain}_access_log combined
</VirtualHost>
EOF
{ubuntu_cmd}
"""
        return cmd

    def set_reverse_proxy_vhostconf(self,third_domain,port_num):
        ubuntu_cmd = " "
        http_dir = "httpd"
        if(self.os == "Ubuntu"):
            http_dir = "apache2"
            ubuntu_cmd = "a2ensite vhost.conf; a2dissite 000-default.conf; systemctl reload apache2; a2enmod proxy ; a2enmod proxy_http"
        cmd = f"""
cat << EOF >> "{self.vhostconf}"
<VirtualHost *:80>
    ServerName {third_domain}.{self.servername}
    ProxyRequests off 
    ProxyPass / http://localhost:{port_num}/ 
    ProxyPassReverse / http://localhost:{port_num}/
    ErrorLog /var/log/{http_dir}/{third_domain}_error_log
    CustomLog /var/log/{http_dir}/{third_domain}_access_log combined
</VirtualHost>
EOF
{ubuntu_cmd}
"""
        return cmd
        
    def restart_http(self):
        print("httpd restart 시작")
        cmd = ""
        if(self.os == "Rocky"):
            cmd = "systemctl restart httpd"
        elif(self.os == "Ubuntu"):
            cmd = "systemctl restart apache2" 
        return cmd

        
############### dns ##################
    def install_named(self):
        print("dns를 설치하겠습니다")
        cmd = ""
        if(self.os == "Rocky"):
            cmd = "dnf -y install bind bind-utils"
        elif(self.os == "Ubuntu"):
            cmd = "apt-get update -y; apt-get install -y bind9 bind9-utils bind9-dnsutils" 
        return cmd


    def init_set_named_conf(self):
        print("named.conf 파일을 수정합니다~")
        cmd = ""        
        if(self.os == "Rocky"):
            cmd = r"""
NAMED_CONF="/etc/named.conf"
sed -i 's/listen-on[[:space:]]*port 53[[:space:]]*{[[:space:]]*127\.0\.0\.1;[[:space:]]*};/listen-on port 53 { any; };/' "$NAMED_CONF"
sed -i 's/allow-query[[:space:]]*{[[:space:]]*localhost;[[:space:]]*};/allow-query { any; };/' "$NAMED_CONF"
    """
        elif(self.os == "Ubuntu"):
            cmd = """cp -ap /etc/bind/named.conf.options /etc/bind/named.conf.options.bak
cat << EOF >  /etc/bind/named.conf.options
options {
        directory "/var/cache/bind";
        dnssec-validation auto;
        recursion yes;
        allow-query { any; };
        listen-on { any; };
        listen-on-v6 { any; };
};
EOF
            
            """ 
        return cmd


    ## Rocky용입니다. 
    def init_set_named_zone(self):
        named_zone = " "
        rocky_added_code = ""
        if(self.os == "Rocky"):
            named_zone = "/etc/named.rfc1912.zones"
            
            self.zonefile = f"/var/named/{self.servername}.zone"
        elif(self.os == "Ubuntu"):
            named_zone = "/etc/bind/named.conf.local"
            self.zonefile = f"/etc/bind/{self.servername}.zone"        
        
        cmd = f'''
cat >> {named_zone} <<EOF
zone "{self.servername}" IN {{
    type master;
    file "{self.zonefile}";
}};
EOF
'''
        print(f"zone이 {named_zone}에 추가되었습니다.")
        return cmd

    def mk_zone_file(self):
        if(self.os == "Rocky"):
            self.zonefile = f"/var/named/{self.servername}.zone"
        elif(self.os == "Ubuntu"):
            self.zonefile = f"/etc/bind/{self.servername}.zone"

        print(f"zone 파일이 생성되었습니다: {self.zonefile}")
        return  f"touch {self.zonefile}"

    def init_set_zone_file(self):
        if(self.os == "Rocky"):
            self.zonefile = f"/var/named/{self.servername}.zone"
        elif(self.os == "Ubuntu"):
            self.zonefile = f"/etc/bind/{self.servername}.zone"
        
        print("zone file의 내용을 수정하겠습니다.")
        domain = f"ns.{self.servername}"
        self.ipaddr = input("현재 사용하고 있는 DNS의 ip: ")
    
        contents = f"""$TTL    604800
@       IN      SOA     {domain}. root.adminemail.com. (
                              2         ; Serial
                         604800         ; Refresh
                          86400         ; Retry 
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@       IN      NS      {domain}.
ns       IN      A       {self.ipaddr}
@       IN      AAAA    ::1
"""

        print("zone file 내용 수정 완료")
    
        return f"""cat << 'EOF' > {self.zonefile}
{contents}
EOF
"""
    
    ## 설치하고 나서 새롭게 DnsVhost 클래스를 사용할 경우에 set_servername 해야함.
    def set_dns_Third_domain(self,third_domain):
        print("DNS 설정을 합니다. 3차 도메인을 추가합니다.")
        if(self.os == "Rocky"):
            self.zonefile = f"/var/named/{self.servername}.zone"
        elif(self.os == "Ubuntu"):
            self.zonefile = f"/etc/bind/{self.servername}.zone"

        self.ipaddr = input(f"3차 도메인인 {third_domain}을 사용할 DNS의 ip를 입력해주세요. : ")
        contents = f"{third_domain}        IN        A        {self.ipaddr}"
        return f"""
cat << 'EOF' >> {self.zonefile}
{contents}
EOF
"""
        
    def restart_dns(self):
        print("dns를 재시작하겠습니다.")
        cmd = ""
        if(self.os == "Rocky"):
            cmd = "systemctl restart named"
        elif(self.os == "Ubuntu"):
            cmd = "systemctl restart bind9" 
        return cmd


