class Tomcat:
    def __init__(self,os):
        self.os = os
    def install_java(self):
        # JDK 다운로드
        cmd = ""
        if(self.os == "Rocky"):
            cmd = """
            wget https://download.oracle.com/java/25/latest/jdk-25_linux-x64_bin.rpm   
            dnf -y install jdk-25_linux-x64_bin.rpm
            dnf -y install unzip 
            """
            
        elif(self.os == "Ubuntu"):
            cmd = """ 
            wget https://download.oracle.com/java/25/latest/jdk-25_linux-x64_bin.deb
            apt install ./jdk-25_linux-x64_bin.deb
            wget https://dlcdn.apache.org/tomcat/tomcat-11/v11.0.15/bin/apache-tomcat-11.0.15.zip
            """
        else :
            print("지원하지 않는 OS입니다.")
        print("Tomcat 설치합니다.")
        return cmd


    def set_tomcat(self):
        cmd = """
mkdir -p /home/tomcat
useradd tomcat
cd /home/tomcat

wget  https://dlcdn.apache.org/tomcat/tomcat-11/v11.0.15/bin/apache-tomcat-11.0.15.zip
unzip apache-tomcat-11.0.15.zip

cd /home/tomcat/apache-tomcat-11.0.15
mv * /home/tomcat
chmod 777 -R /home/tomcat
chown -R tomcat:tomcat /home/tomcat
        """
        return cmd

    def set_service(self):
        add_cmd = ""
        if(self.os == "Rocky"):
            add_cmd = """
systemctl restart named
systemctl restart httpd
            """
            
        elif(self.os == "Ubuntu"):
            add_cmd = """ 
systemctl restart bind9
systemctl restart apache2
            """
            
        cmd = f"""
sed -i '/<Connector / s/port="8080"/port="8088"/' /home/tomcat/conf/server.xml
cat <<EOF >> "/etc/systemd/system/tomcat.service"
[Unit]
Description=Apache Tomcat Web Application Container
After=network.target
# 네트워크가 먼저 준비된 후 실행
[Service]
Type=forking
User=tomcat
Group=tomcat
# 설치 디렉토리
Environment="JAVA_HOME=/usr/lib/jvm/jdk-25.0.1-oracle-x64"
Environment="CATALINA_HOME=/home/tomcat"
Environment="CATALINA_BASE=/home/tomcat"
# 서비스 시작/종료 스크립트 경로
ExecStart=/home/tomcat/bin/startup.sh
ExecStop=/home/tomcat/bin/shutdown.sh
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now tomcat
systemctl restart tomcat
{add_cmd}
        """
        return cmd


