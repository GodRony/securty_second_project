class Partition :
    def __init__(self,os):
        self.os = os
        self.partition = ""


    def make_partition(self):
        self.partition = input("무엇을 파티션할건지 적으세요 (ex. /dev/sda): ")

        script = f'''
#!/usr/bin/expect -f
spawn fdisk {self.partition}
expect "Command (m for help):"
send "n\\r"
expect "Select (default p):"
send "\\r"
expect "Partition number (1-4, default 1):"
send "\\r"
expect "First sector"
send "\\r"
expect "Last sector"
send "\\r"
expect "Command (m for help):"
send "w\\r"
expect eof
'''
    cmd = f"""
echo '{script}' > /tmp/mkpart.exp
chmod +x /tmp/mkpart.exp
expect /tmp/mkpart.exp
lsblk
    """
    ## lsblk시 sda           8:0    0  102M  0 disk로 disk 로 떠야합니다
    return cmd

    def format_partition(self):
        self.partition = input("아까 생성한 파티션을 입력하세요(ex. /jupyter or /dev/sda1): ")
        return f'mkfs -t ext4 {partition}'
        ## lsblk시 sda           8:0    0  102M  0 part로 part 로 떠야합니다

    
    ## 나중에 Main에서 할거라 삭제할것
    def add_user(self) :
        # 사용자 계정 생성
        cmd = """
        # team1 계정이 존재하지 않으면 생성
        if ! id team1 &>/dev/null; then
            useradd -m -d /jupyter/team1 team1
        else
            # 이미 존재하면 홈디렉토리만 확인 또는 새로 만듦
            mkdir -p /jupyter/team1
            usermod -d /jupyter/team1 team1
        fi
        """
        return cmd

    def set_password(self):
        script = '''
        spawn passwd team1
        expect "New password:"
        send "asd123!@\\r"
        expect "Retype new password:"
        send "asd123!@\\r"
        expect eof
        '''
        cmd = f"""
echo '{script}' > /tmp/mkuser.exp
chmod +x /tmp/mkuser.exp
expect /tmp/mkuser.exp
        """
        return cmd



    
