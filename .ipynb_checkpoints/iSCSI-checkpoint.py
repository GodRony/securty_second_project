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























    


