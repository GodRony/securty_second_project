class Partition :
    def __init__(self):
#        self.os = os
        self.PARTITION = ""
        self.MOUNT_DIR = ""

######################## PARTITION ######################    

    def make_partition(self):
        self.PARTITION = input("무엇을 파티션할건지 적으세요 (ex. /dev/sda): ")
        script = f'''
#!/usr/bin/expect -f
spawn fdisk {self.PARTITION}
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
        self.PARTITION = input("아까 생성한 파티션을 입력하세요(ex. /dev/sda1): ")
        cmd = f"""
mkfs -t ext4 {self.PARTITION}
lsblk -f
        """
        return cmd
        ## lsblk시 sda           8:0    0  102M  0 part로 part 로 떠야합니다

    
######################## MOUNT ######################
    
    def mount(self) :
        self.MOUNT_DIR =  input("마운트 할 경로를 입력하세요 (ex. /mnt/test): ")
    
        cmd = f"""
        sudo mkdir -p {self.MOUNT_DIR}
        sudo mount -t ext4 {self.PARTITION} {self.MOUNT_DIR}
        ls {self.MOUNT_DIR}
        """
        return cmd
    
    def permanent_mount_config_remote(self):
        new_line = f"{self.PARTITION} {self.MOUNT_DIR} ext4    defaults,usrquota        0 0\n"
        print("fstab에 새 항목 추가함:", new_line)
        cmd = f"""
echo '{new_line}' >> /etc/fstab
systemctl daemon-reload
mount -o remount {self.MOUNT_DIR}
        """
        return cmd
    
    
    
        
