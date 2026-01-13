class RAID:
    def __init__(self, os):
        self.os = os
        self.mount_disk1 = ""
        self.mount_disk2 = ""
        self.mount_disk3 = ""
        self.RAID_MOUNT_DIR = ""
        self.raid_num = ""

    def install_raid(self) :
        cmd = ""
        if(self.os == "Rocky"):
            cmd =  "dnf install -y mdadm"
        elif(self.os == "Ubuntu"):
            cmd =  "apt install -y mdadm"
        return cmd
            
    def raid_mk(self):
        self.raid_num = input("raid 0,1,5를 지원합니다. raid할 번호를 입력하세요. ex. 0 : ")
        self.mount_disk1 = input("mount할 디스크1을 입력해주세요 ex. /dev/sda: ")
        self.mount_disk2 = input("mount할 디스크2를 입력해주세요 ex. /dev/sdb: ")
        cmd = ""
        
        if(self.raid_num == "0" or self.raid_num == "1") : 
            cmd = f"""yes | mdadm --create /dev/md{self.raid_num} --level={self.raid_num} --raid-devices=2 {self.mount_disk1} {self.mount_disk2}"""
            
        elif(self.raid_num == "5"):
            self.mount_disk3 = input("mount할 디스크3를 입력해주세요 ex. /dev/sdc: ")
            cmd = f"""yes | mdadm --create /dev/md{self.raid_num} --level={self.raid_num} --raid-devices=3 {self.mount_disk1} {self.mount_disk2} {self.mount_disk3}"""
        
        else : 
            print("지원하지 않는 raid 숫자입니다.")
       
        return cmd
        
    def raid_mk_fs_mount(self):
        self.RAID_MOUNT_DIR = input("mount 할 디렉토리를 입력해주세요 ex./mnt/mirror : ")
        cmd = f"""
    mkdir -p {self.RAID_MOUNT_DIR}
    mkfs.ext4 -F /dev/md{self.raid_num}
    mount /dev/md{self.raid_num} {self.RAID_MOUNT_DIR}
    """
        return cmd
    
    def erase_raid(self) :
        md = input("raid로 합쳐진 디스크 이름을 입력해주세요. ex. /dev/md0: ").strip()
        
        self.mount_disk1 = input("raid로 mount된 디스크1을 입력해주세요 ex. /dev/sda: ")
        self.mount_disk2 = input("raid로 mount된 디스크2를 입력해주세요 ex. /dev/sdb: ")

        add_cmd = ""
        if(md == "/dev/md5"):
            self.mount_disk3 = input("raid로 mount된 디스크3를 입력해주세요 ex. /dev/sdc: ")
            add_cmd = f"""
            wipefs -a {self.mount_disk3}
            mdadm --zero-superblock {self.mount_disk3}
            """
        self.RAID_MOUNT_DIR = input("riad로 마운트 된 경로 입력해주세요 ex. /mnt/mirror: ")
        
        
        cmd = f"""
umount {self.RAID_MOUNT_DIR}

mdadm --stop {md}
mdadm --remove {md}

mdadm --zero-superblock {self.mount_disk1}
mdadm --zero-superblock {self.mount_disk2}

wipefs -a {self.mount_disk1}
wipefs -a {self.mount_disk2}

{add_cmd}
        """
        return cmd