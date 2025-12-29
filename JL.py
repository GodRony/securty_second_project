class JL:
    def __init__(self,os):
        self.os = os

    def install_pacakages(self):
        cmd = ""
        if(self.os == "Rocky"):
            cmd = """
            dnf install -y php-xml php-zip php-mysql php-intl php-gd php-curl php-mbstring
            dnf -y install unzip"""
        elif(self.os == "Ubuntu"):
            cmd = """
            apt install -y php-xml php-zip php-mysql php-intl php-gd php-curl php-mbstring
            apt -y install unzip"""
        else :
            print("지원하지 않는 OS 입니다.")
        return cmd
        
    def install_JL(self):
        cmd = """
cd /home
useradd jl
mkdir -p /home/jl
wget https://downloads.joomla.org/cms/joomla6/6-0-0/Joomla_6-0-0-Stable-Full_Package.zip?format=zip

mv 'Joomla_6-0-0-Stable-Full_Package.zip?format=zip' /home/jl

cd /home/jl

unzip 'Joomla_6-0-0-Stable-Full_Package.zip?format=zip'

cd ..
chmod 777 -R jl
chown -R jl:jl jl
        """
        return cmd

    