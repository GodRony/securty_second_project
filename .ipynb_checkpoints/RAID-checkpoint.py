class RAID:
    def __init__(self, os):
        self.os = os
        self.mount_disk1 = ""
        self.mount_disk2 = ""
        self.RAID1_MOUNT_DIR = ""

    def install_raid(self) :
        return "dnf install -y mdadm"
    def raid1_mk(self):
        self.mount_disk1 = input("mount할 디스크1을 입력해주세요 ex. /dev/sda: ")
        self.mount_disk2 = input("mount할 디스크2를 입력해주세요 ex. /dev/sdb: ")
        cmd = f"yes | mdadm --create /dev/md0 --level=1 --raid-devices=2 {self.mount_disk1} {self.mount_disk2}"
        return cmd
        
    def raid1_mk_fs_mount(self):
        self.RAID1_MOUNT_DIR = input("mount 할 디렉토리를 입력해주세요 ex./mnt/mirror : ")
        cmd = f"""
    mkdir -p {self.RAID1_MOUNT_DIR}
    mkfs.ext4 -F /dev/md0
    mount /dev/md0 {self.RAID1_MOUNT_DIR}
    """
        return cmd

    def raid1_permanent_mount_config_remote(self):
        print("영구 마운트 하겠습니다")
        cmd = f"""
        mkdir -p {self.RAID1_MOUNT_DIR}
        echo '/dev/md0    {self.RAID1_MOUNT_DIR}    ext4    defaults,usrquota    0    0\n' >> /etc/fstab
        systemctl daemon-reload
        mount -o remount {self.RAID1_MOUNT_DIR}
        mount -a
        """
        return cmd
    
    def erase_raid(self) :
        self.mount_disk1 = input("raid로 mount된 디스크1을 입력해주세요 ex. /dev/sda: ")
        self.mount_disk2 = input("raid로 mount된 디스크2를 입력해주세요 ex. /dev/sdb: ")
        self.RAID1_MOUNT_DIR = input("riad로 마운트 된 경로 입력해주세요 ex. /mnt/mirror: ")
        md = input("raid로 합쳐진 디스크 이름을 입력해주세요. ex. /dev/md0: ")
        
        cmd = f"""
umount {self.RAID1_MOUNT_DIR}

mdadm --stop {md}
mdadm --remove {md}

mdadm --zero-superblock {self.mount_disk1}
mdadm --zero-superblock {self.mount_disk2}

wipefs -a {self.mount_disk1}
wipefs -a {self.mount_disk2}
        """
        return cmd