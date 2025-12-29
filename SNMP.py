class SNMP:
    def __init__(self,os):
        self.os = os
        self.local_community = ""
        self.my_community = ""
        self.NI = ""

    def install_snmp(self) :
        cmd = ""
        if(self.os == "Rocky") :
            cmd = "dnf -y install net-snmp*"
        elif(self.os == "Ubuntu") : 
            cmd = "apt install -y snmp snmpd"
        return cmd
        
    def set_snmp(self):
        conf = "/etc/snmp/snmpd.conf"
        print(f"{conf} 설정 시작합니다.")
        self.local_community = input("74번째 줄 : 설정할 local의 COMMUNITY 이름을 입력해주세요 ex. kong : ")
        self.my_community = input("74번째 줄 : 설정할 mynetwork의 COMMUNITY 이름을 입력해주세요 ex. tj : ")
        self.NI = input("75번째 줄 : 설정할 mynetwork의 대역을 입력해주세요. ex. 172.16.0.0/16 : ")
        
        cmd = f"""
sed -i "s|#com2sec local     localhost       COMMUNITY|com2sec local     localhost       {self.local_community}|g" {conf}
sed -i "s|#com2sec mynetwork NETWORK/24      COMMUNITY|com2sec mynetwork {self.NI}      {self.my_community}|g" {conf}

sed -i "s|#group MyRWGroup  any        local|group MyRWGroup  any        local|g" {conf}

sed -i "s|#group MyROGroup  any        mynetwork|group MyROGroup  any        mynetwork|g" {conf}

sed -i "s|#view all    included  .1                               80|view all    included  .1                               80|g" {conf}

sed -i 's|^#access MyROGroup.*|access MyROGroup ""      any       noauth    0      all    none   none|g' {conf}

sed -i 's|^#access MyRWGroup.*|access MyRWGroup ""      any       noauth    0      all    all    all|g' {conf}
"""
        return cmd

    def start_enable_snmpd(self):
        return "systemctl restart --now snmpd; systemctl enable --now snmpd"

    def test_snmpd_local(self) :
        print("자기자신에게 테스트합니다.")
        return f"snmpwalk -v2c -c {self.local_community} localhost system"