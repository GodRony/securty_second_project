class Pydio:
    def __init__(self, os):
        self.os = os

    def install_package(self) :
        if(self.os == "Rocky"):
            return "dnf install unzip"
        elif(self.os == "Ubuntu"):
            return "apt install unzip"
    
    def install_pydio(self):
        cmd = """
mkdir -p /home/pydio
useradd pydio
cd /home/pydio
wget https://download.pydio.com/pub/cells/release/4.4.9/linux-amd64/pydio-cells-4.4.9-linux-amd64.zip

unzip pydio-cells-4.4.9-linux-amd64.zip 
chmod +x cells
        """
        return cmd
    def set_pydio(self):
        cmd = """
/home/pydio/cells install
"""
    def mk_db(self):
        cmd = """

        """