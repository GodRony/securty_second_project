class DnsVhost:
    def __init__(self,os):
        self.os = os
        self.vhostconf = "/etc/httpd/conf.d/vhost.conf"
        self.servername = ""
        self.zonefile = ""
        self.ipaddr = ""
        self.third_domain = ""

############## http ###############    
    def install_http(self):
        cmd = ""
        if(self.os == "Rocky"):
            cmd = "dnf -y install httpd ; systemctl enable --now httpd ; dnf install expect -y"
        elif(self.os == "Ubuntu"):
            cmd = " "
        else : 
            print("지원하지 않는 OS입니다.")
            
        return cmd        


    def set_servername(self):
        self.servername = input("ServerName을 입력하세요. (예: test.com , ppp.com): ")

    def mk_vhostconf(self):
        return f"touch {self.vhostconf}"

    def test_vhost(self):
        return f"""mkdir -p /home/test && chmod 755 /home/test
echo '<h1>test</h1>' > /home/test/index.html"""

    def set_vhostconf(self,web_dir,third_domain,error_log ,custom_log):
        self.third_domain = third_domain
        
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

    ErrorLog {error_log}
    CustomLog {custom_log} combined
</VirtualHost>
EOF
"""
        return cmd

    def set_reverse_proxy_vhostconf(self,third_domain,error_log ,custom_log):
        self.VHOST_CONF = f"/etc/httpd/conf.d/vhost.conf"
        cmd = f"""
cat << EOF >> "{self.VHOST_CONF}"
<VirtualHost *:80>
    ServerName {third_domain}.{self.servername}
    ProxyRequests off 
    ProxyPass / http://localhost:8080/ 
    ProxyPassReverse / http://localhost:8080/ 
    ErrorLog "{error_log}"
    CustomLog "{custom_log}" combined
</VirtualHost>
"""
        return cmd
        
    def restart_http(self):
        print("httpd restart 시작")
        return "sudo systemctl restart httpd"

        
############### dns ##################
    def install_named(self):
        print("dns를 위한 named를 설치하겠습니다")
        return "dnf -y install bind bind-utils"

    def init_set_named_conf(self):
        print("named.conf 파일을 수정합니다~")
        cmd = r"""
NAMED_CONF="/etc/named.conf"
sed -i 's/listen-on[[:space:]]*port 53[[:space:]]*{[[:space:]]*127\.0\.0\.1;[[:space:]]*};/listen-on port 53 { any; };/' "$NAMED_CONF"
sed -i 's/allow-query[[:space:]]*{[[:space:]]*localhost;[[:space:]]*};/allow-query { any; };/' "$NAMED_CONF"
    """
        return cmd

    def init_set_named_rfc(self):
        self.zonefile = f"{self.servername}.zone"
        
        cmd = f'''
cat >> /etc/named.rfc1912.zones <<EOF
zone "{self.servername}" IN {{
    type master;
    file "{self.zonefile}";
    allow-update {{ none; }};
}};
EOF
'''
        print("zone이  /etc/named.rfc1912.zones에 추가되었습니다.")
        return cmd

    def mk_zone_file(self):
        self.zonefile = f"{self.servername}.zone"
        print(f"zone 파일이 생성되었습니다: /var/named/{self.zonefile}")
        return  f"touch /var/named/{self.zonefile}"

    def init_set_zone_file(self):
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
    
        return f"""cat << 'EOF' > /var/named/{self.zonefile}
{contents}
EOF
"""
    
    ## 설치하고 나서 새롭게 DnsVhost 클래스를 사용할 경우에 set_servername 해야함.
    def set_dns_Third_domain(self,third_domain):
        self.zonefile = f"{self.servername}.zone"
        self.ipaddr = input("사용할 DNS의 ip: ")
        contents = f"{third_domain}        IN        A        {self.ipaddr}\n"
        return f"""
cat << 'EOF' >> /var/named/{self.zonefile}
{contents}
EOF
"""
        
    def restart_dns(self):
        return "systemctl restart named"


