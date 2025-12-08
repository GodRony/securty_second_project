info = []
# os 구분
    info = cmd("cat /etc/os-release")
    if "Rocky" in info:
        return "Rocky"
    elif "Ubuntu" in info:
        return "Ubuntu"
    return "Unknown"

# def 업데이트, 업그레이드
    if info == "Rocky":
        dnf update && dnf upgrade -y
    elif info == "Ubutnu":
        apt update && apt upgrade -y

# def 방화벽해제
    만약 os가 로키라면 
    firewall-cmd --add-port=3260/tcp --permanent
    firewall-cmd --reload
    systemctl stop firewalld

    만약 os가 우분투라면
    ufw allow 3260/tcp
    ufw disable
    ufw reload

# 아이스카시 타겟 설치
    만약 로키라면
    dnf install targetcli -y #타겟서버 설치
    systemctl enable --now target
    systemctl status target

    우분투라면
    apt install targetcli-fb -y #타겟서버설치
    systemctl enable --now target
    systemctl status target

# targetcli설정
    targetcli
    /backstores/block create disk100 /dev/sdb
    /iscsi create iqn.2025-10.com.total1:storage.target1
    /iscsi /iqn.2025-10.com.total1:storage.target1/tpg1/luns create /backstores/block/disk100
    /iscsi /iqn.2025-10.com.total1:storage.target1/tpg1/acls create {이니시에이터 서버 iqn}
    /iscsi /iqn.2025-10.com.total1:storage.target1/tpg1/portals create 0.0.0.0
    saveconfig
    exit 

# 타겟 설정 확인
    targetclit
    argetcli /> ls

***************************************************************************************

# 이니시에이터 서버 설치
    로키라면
    dnf install iscsi-initiator-utils
    systemctl enable --now iscsid
    systemctl status iscsid

    우분투라면
    apt install -y open-iscs
    systemctl enable --now iscsid
    systemctl status iscsid

# 이니시에이터 서버 iqn확인
cat /etc/iscsi/initiatorname.iscsi

# 타겟서버 검색
iscsiadm -m discovery -t st -p 타겟서버IP

# 타겟서버 연결
iscsiadm -m discovery -t sendtargets -p 타겟서버ip -l

# 디렉터리 생성 및 권한 부여
mkdir -p /mnt/a
chmod 777 /mnt/a

# 마운트
fdisk -l #디스크확인
mkfs -t ext4 /dev/sda #디스크포멧
mount -t ext4 /dev/sda /mnt/a #마운트
blkid /dev/sda #uuid확인
vim /etc/fstab 들어가서 내용 추가 #영구마운트
uuid=uuid /mnt/a ext4 defaults 0 0
df # 마운트확인
================================================================================================================================

def iscsi_server_setup():  # iSCSI 서버 방화벽 해제 및 패키지 설치
    os_type = detect_os(ISCSI_SERVER_IP)
    print(f"감지된 서버 OS: {os_type}")

    if os_type == "Ubuntu":
        cmd(ISCSI_SERVER_IP, "ufw disable || true")
        cmd(ISCSI_SERVER_IP, "apt update -y && apt install -y targetcli-fb expect || apt install -y targetcli expect")
    else:
        cmd(ISCSI_SERVER_IP, "setenforce 0 || true")
        cmd(ISCSI_SERVER_IP, "systemctl stop firewalld || true")
        cmd(ISCSI_SERVER_IP, "dnf -y install epel-release || dnf -y install epel-next-release")
        cmd(ISCSI_SERVER_IP, "dnf install -y targetcli expect || dnf install -y targetcli-fb expect")

    print("iSCSI 서버 및 Expect 설치 완료")


def iscsi_server_target_config():  # iSCSI 타깃 구성
    if not os.path.exists(IQN_FILE):
        print(f"클라이언트 IQN 파일 없음: {IQN_FILE}")
        return

    with open(IQN_FILE, "r", encoding="utf-8") as f:
        client_iqn = f.read().strip()
    print(f"불러온 클라이언트 IQN: {client_iqn}")

    cmds = [
        "mkdir -p /iscsi_disks && chmod 777 /iscsi_disks",
        "targetcli /backstores/block delete disk100 || true",
        f"targetcli /iscsi delete {TARGET_IQN} || true",
        f"targetcli /backstores/block create disk100 {BLOCK_DEVICE}",
        f"targetcli /iscsi create {TARGET_IQN}",
        f"targetcli /iscsi/{TARGET_IQN}/tpg1/luns create /backstores/block/disk100",
        f"targetcli /iscsi/{TARGET_IQN}/tpg1/acls create {client_iqn}",
        f"targetcli /iscsi/{TARGET_IQN}/tpg1/portals create 0.0.0.0",
        "targetcli saveconfig"
    ]
    for c in cmds:
        cmd(ISCSI_SERVER_IP, c)

    print("iSCSI 타깃 생성 완료")


def iscsi_server_restart():  # iSCSI 서비스 및 포트 확인
    cmd(ISCSI_SERVER_IP, "systemctl enable target || systemctl enable rtslib-fb-targetctl || true")
    cmd(ISCSI_SERVER_IP, "systemctl restart target || systemctl restart rtslib-fb-targetctl || true")
    cmd(ISCSI_SERVER_IP, "setenforce 0 || true")
    cmd(ISCSI_SERVER_IP, "systemctl stop firewalld || true")
    port_check = cmd(ISCSI_SERVER_IP, "ss -tuln | grep 3260 || echo 'Port 3260 not open'")
    print(port_check)
    print("iSCSI 서버 재시작 및 포트 확인 완료")


def iscsi_client_install():  # iSCSI 클라이언트 설치 및 IQN 파일 생성
    os_type = detect_os(ISCSI_CLIENT_IP)
    print(f"감지된 클라이언트 OS: {os_type}")
    if os_type == "Ubuntu":
        cmd(ISCSI_CLIENT_IP, "apt update -y && apt install -y open-iscsi")
        cmd(ISCSI_CLIENT_IP, "systemctl enable iscsid && systemctl start iscsid")
        cmd(ISCSI_CLIENT_IP, "ufw disable || true")
    else:
        cmd(ISCSI_CLIENT_IP, "dnf install -y iscsi-initiator-utils iscsi-initiator-utils-iscsiuio")
        cmd(ISCSI_CLIENT_IP, "systemctl enable iscsid && systemctl start iscsid")
        cmd(ISCSI_CLIENT_IP, "systemctl enable iscsi && systemctl start iscsi")
        cmd(ISCSI_CLIENT_IP, "systemctl stop firewalld || true")

    print("iSCSI 클라이언트 설치 및 IQN 생성 완료\n")

def iscsi_client_iqn():  
    print("잠시 대기")
    time.sleep(10)
    print("대기 끝")
    exist_check = cmd(ISCSI_CLIENT_IP, "test -f /etc/iscsi/initiatorname.iscsi && echo EXIST || echo MISSING")
    if "EXIST" in exist_check:
        iqn = cmd(ISCSI_CLIENT_IP, "grep InitiatorName /etc/iscsi/initiatorname.iscsi | cut -d= -f2").strip()
        if iqn:
            print(f"기존 IQN 감지됨: {iqn}")
        else:
            print("기존 파일은 있지만 IQN이 비어 있습니다. 재생성합니다.")
            iqn = cmd(ISCSI_CLIENT_IP, "/usr/sbin/iscsi-iname").strip()
            cmd(ISCSI_CLIENT_IP, f"echo 'InitiatorName={iqn}' > /etc/iscsi/initiatorname.iscsi")
    else:
        print("IQN 파일이 존재하지 않아 새로 생성합니다.")
        iqn = cmd(ISCSI_CLIENT_IP, "/usr/sbin/iscsi-iname").strip()
        cmd(ISCSI_CLIENT_IP, f"mkdir -p /etc/iscsi && echo 'InitiatorName={iqn}' > /etc/iscsi/initiatorname.iscsi")

    if not iqn:
        print("IQN 생성 실패 — 수동 확인 필요 (/usr/sbin/iscsi-iname 실행 결과 확인)")
        return None

    with open(IQN_FILE, "w", encoding="utf-8") as out:
        out.write(iqn)

    print(f"IQN 생성/저장 완료 → {IQN_FILE}")
    print(f"   IQN: {iqn}")
    return iqn

def iscsi_client_login():
    cmd(ISCSI_CLIENT_IP, "iscsiadm -m node -u || true")
    cmd(ISCSI_CLIENT_IP, f"iscsiadm -m discovery -t sendtargets -p {ISCSI_SERVER_IP}")
    cmd(ISCSI_CLIENT_IP, f"iscsiadm -m node -T {TARGET_IQN} -p {ISCSI_SERVER_IP} --login")
    cmd(ISCSI_CLIENT_IP, "sleep 2; iscsiadm -m session --rescan; udevadm trigger --subsystem-match=scsi --action=add")
    print("iSCSI 로그인 및 디스크 재탐색 완료")

def iscsi_client_mount():
    print("iSCSI 디스크 파티션/마운트")
    cmd(ISCSI_CLIENT_IP, "iscsiadm -m session --rescan || true")
    cmd(ISCSI_CLIENT_IP, "udevadm trigger --subsystem-match=scsi --action=add || true")
    time.sleep(3)
    bypath = cmd(ISCSI_CLIENT_IP, "ls /dev/disk/by-path | grep -i iscsi | grep 'lun-0' | head -n 1").strip()
    if not bypath:
        print("iSCSI 디스크 탐지 실패")
        return
    dev = cmd(ISCSI_CLIENT_IP, f"readlink -f /dev/disk/by-path/{bypath}").strip()
    part = f"{dev}1"

    part_exist = cmd(ISCSI_CLIENT_IP, f"ls {part} 2>/dev/null || echo NONE").strip()
    if "NONE" in part_exist:
        print(cmd(ISCSI_CLIENT_IP, f"parted -s {dev} mklabel gpt mkpart primary ext4 0% 100%"))
        cmd(ISCSI_CLIENT_IP, "partprobe; udevadm settle; sleep 2")

    fs_check = cmd(ISCSI_CLIENT_IP, f"blkid {part} | grep ext4 || echo NONE").strip()
    if "NONE" in fs_check:
        print(cmd(ISCSI_CLIENT_IP, f"mkfs.ext4 -F {part}"))
    cmd(ISCSI_CLIENT_IP, f"mkdir -p {MOUNT_POINT}")
    cmd(ISCSI_CLIENT_IP, f"mount {part} {MOUNT_POINT}")
    print(cmd(ISCSI_CLIENT_IP, f"df -h | grep {MOUNT_POINT} || echo '마운트 실패'"))
=======================================================================================================================
class Iscsi:
    def __init__(self, os, ip):
        self.os = os
        self.ip = ip

    # def upup(self):
    #     if self.os == "Rocky":
    #         return "dnf update && dnf upgrade -y"
    #     elif self.os == "Ubuntu":
    #         return "apt update && apt upgrade -y"
    #     else:
    #         return "지원하지 않는 OS입니다."

    def 방화벽해제(self):
        if self.os == "Rocky":
            cmd1 = "firewall-cmd --add-port=3260/tcp --permanent"
            cmd2 = "firewall-cmd --reload"
            cmd3 = "systemctl stop firewalld"
            return cmd1, cmd2, cmd3
        elif self.os == "Ubuntu":
            cmd1 = "ufw allow 3260/tcp"
            cmd2 = "ufw reload"
            cmd3 = "systemctl stop ufw"
            return cmd1, cmd2, cmd3
        else:
            return "지원하지 않는 OS입니다."

 def install_target(self):
        if self.os == "Rocky":
            cmd1 = "dnf install targetcli -y"              # 타겟 서버 설치
            cmd2 = "systemctl enable --now target"         # 서비스 켜기
            cmd3 = "systemctl status target"               # 상태 확인
            return cmd1, cmd2, cmd3
        elif self.os == "Ubuntu":
            cmd1 = "apt install targetcli-fb -y"           # 타겟 서버 설치
            cmd2 = "systemctl enable --now target"         # 서비스 켜기
            cmd3 = "systemctl status target"               # 상태 확인
            return cmd1, cmd2, cmd3
        else:
            return "지원하지 않는 OS입니다."

def targetcli(self)
    disk_name = input("디스크 이름 : ex)disk100")
    disk_path = input("디스크 경로 : ex)/dev/sdb")
    iqn_target = "iqn.2025-10.com.total1:storage.target1"
    iqn_initiator = "iqn.2025-10.com.client:init1"

 cmd = [
            "targetcli",
            f"/backstores/block create {disk_num} {disk_path}",
            f"/iscsi create {iqn_target}",
            f"/iscsi/{iqn_target}/tpg1/luns create /backstores/block/{disk_num}",
            f"/iscsi/{iqn_target}/tpg1/acls create {iqn_initiator}",
            f"/iscsi/{iqn_target}/tpg1/portals create 0.0.0.0",
            f"targetcli saveconfig",
            f"ls",
            "exit"
        ]

***************************************************************************************

# 이니시에이터 서버 설치
    로키라면
    dnf install iscsi-initiator-utils
    systemctl enable --now iscsid
    systemctl status iscsid

    우분투라면
    apt install -y open-iscs
    systemctl enable --now iscsid
    systemctl status iscsid

# 이니시에이터 서버 iqn확인
cat /etc/iscsi/initiatorname.iscsi

# 타겟서버 검색
iscsiadm -m discovery -t st -p 타겟서버IP

# 타겟서버 연결
iscsiadm -m discovery -t sendtargets -p 타겟서버ip -l

# 디렉터리 생성 및 권한 부여
mkdir -p /mnt/a
chmod 777 /mnt/a

# 마운트
fdisk -l #디스크확인
mkfs -t ext4 /dev/sda #디스크포멧
mount -t ext4 /dev/sda /mnt/a #마운트
blkid /dev/sda #uuid확인
vim /etc/fstab 들어가서 내용 추가 #영구마운트
uuid=uuid /mnt/a ext4 defaults 0 0
df # 마운트확인


--------------------------------------------------------------------------------------------

def iscsi_client_install(self):  # iscsi 클라이언트 설치 및 IQN 파일 생성
  
    if self.os == "Ubuntu":
        cmd(f"apt install -y open-iscs")
        cmd(f"systemctl enable iscsid && systemctl start iscsid")

 
    else:
        cmd(ISCSI_CLIENT_IP, "dnf install -y iscsi-initiator-utils iscsi-initiator-utils-iscsiuio")
        cmd(ISCSI_CLIENT_IP, "systemctl enable iscsid && systemctl start iscsid")
        cmd(ISCSI_CLIENT_IP, "systemctl enable iscsi && systemctl start iscsi")

    print("iSCSI 클라이언트 설치 및 IQN 생성 완료\n")

























    


