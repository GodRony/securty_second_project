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
            """
            
        elif(self.os == "Ubuntu"):
            cmd = """ """
        else :
            print("지원하지 않는 OS입니다.")
        
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
        """
        return cmd