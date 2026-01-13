# 필요한 변수
#-----------------------------------------
#사용 OS
#쿼터를 설정할 파일 시스템 경로
#쿼터 적용 모드(유저 or 그룹)
#소프트 제한값
#하드 제한값
#소프트 제한 초과 후 허용 되는 기간
#------------------------------------------
#기능
#사용 os
#설치 상태 확인
#쿼터 기능 활성화
#쿼터 파일 생성 및 초기화
#쿼터 상태 확인
#사용자/그룹별 디스크 사용량 확인
#------------------------------------------
# 사용 OS
class Diskquota:

    def __init__(self, os):
        self.os = os
        self.partition = ""
        self.mount_point = ""
        self.diskquota_id = ""
        self.diskquota_group_id = ""

# quota 설치
    def diskquota_isntall(self):
        print("diskquota 서비스를 설치합니다.")
        if self.os == "Rocky":
            cmd ="dnf install -y quota"
        elif self.os == "Ubuntu":
            cmd = "apt install -y quota"
        else:
            cmd=""
            print("지원하지 않는 OS입니다.")
        return cmd

# quota 설치 상태 확인
    def diskquota_install_check(self):
        print("diskquota 설치 상태를 확인합니다.")
        cmd = ""
        if self.os == "Rocky":
            cmd ="rpm -qa | grep quota"
        elif self.os == "Ubuntu":
            cmd = "dpkg -l | grep quota"
        else:
            cmd=""
            print("지원하지 않는 OS입니다.")
        return cmd

# /etc/fstab 수정
    # def show_partition(self) :
    #     return "lsblk"

    def diskquota_modify(self):
        print("/etc/fstab을 수정합니다.")
        cmd = ""
        diskquota_on = input("자동마운트를 진행하겠습니까? (y or n) ex)y : ")
        if diskquota_on == "n" :
            return cmd
        if diskquota_on == "y" :
            self.partition = input("어떤 파티션을 diskquota 하겠습니까? ex) /dev/sda1 : ")
            self.mount_point = input("diskquota를 실행할 mount 디렉토리를 입력하세요. ex. /mnt/test")
            cmd = f"""
sed -i '\\|{self.partition}|d' /etc/fstab
mkdir -p {self.mount_point}
echo '{self.partition} {self.mount_point} ext4 defaults,usrquota,grpquota 0 0' | sudo tee -a /etc/fstab
systemctl daemon-reload
mount -o remount {self.mount_point}
"""

        return cmd
#ex)
#/dev/vda1 /home ext4 defaults,usrquota,grpquota 1 2
#/dev/vda1 /home ext4 defaults,usrquota,grpquota 0 2
#파티션 이름 디렉토리 위치에 마운트 하겠다. 파일시스템 종류 마운트옵션 덤프옵션(대부분 0또는 1, 보통 root는 1 나머지는 0) fsck 순서(1,2,0)


#쿼터 파일 생성 및 초기화
    def diskquota_mount_and_initalization(self):
        print("diskquota 파일을 생성하고 초기화합니다.")
        cmd =f"""
sudo bash -lc '
    umount {self.mount_point}
    tune2fs -O quota {self.partition}
    mount -a
    quotacheck -cu {self.mount_point}
    quotaon {self.mount_point}
    '        
"""
        return cmd
           
#-c: 쿼터 파일을 생성 (Create)
#-u: 사용자 쿼터 파일
#-g: 그룹 쿼터 파일
#-v: 진행 상황 출력 (Verbose)

#쿼터 설정
    def diskquota_settings(self):
        cmd = ""
        diskquota = input("diskquota 세팅을 하시겠습니까 (y or n) ex)y : ")

        if diskquota == "n":
            return cmd
        elif diskquota == "y":
            
            disk_user = input("설정할 계정명을 입력해주세요 : ")
            disk_group = input("설정할 그룹명을 입력해주세요 : ")
            disk_time = input("유예기간을 설정하세요 ex)1 :")
            setting = input("""제한 설정을 선택하세요
                               =================================
                                1. 사용자 제한 설정 
                                2. 그룹 제한 설정
                                3. 유예기간 설정
                                """)
            if setting == "1" :
                cmd = f"adduser {disk_user} ; edquota -u {self.diskquota_id}"
            elif setting == "2" :
                cmd = f"edquota -u {self.diskquota_group_id}"
            elif setting == "3" :
                print("유예 기간 설정은 에디터가 열리기 때문에 직접하셔요")
            else : 
                print("잘못된 입력입니다.")
        else :
            print("잘못된 입력입니다.")
        print(f"터미널에 들어가셔서 edquota {self.diskquota_id} 로 한번 확인해보셔요 ^^")
        return cmd
    
#    사용자 제한 설정 :edquota -u [계정명]
#    그룹 제한 설정 : edquota -g [그룹명]
#    유예기간 설정 :edquota -t(에디터가 열림)


#쿼터 기능 설정(on/off)
    def diskquota_systemctl(self):
        cmd = ""
        systemctl = input("""쿼터 기능을 선택하세요 (on/off) : )
                        ==============================================
                         1. on
                         2. off
                         """)
        if systemctl == "on" :
            cmd = f"quotaon {self.mount_point}"
        elif systemctl == "off" :
            cmd = f"quotaoff {self.mount_point} "
        else:
            print("잘못된 입력입니다.")    
        return cmd
    
    #쿼터 상태 확인 : edquota -p
    #quotaon [파일시스템 경로]
    #quotaoff [파일시스템 경로]
    
    
    #사용자/그룹별 디스크 사용량 확인
    #계정명 사용자 쿼터 상태 확인 : edquota -u [계정명]
    #모든 사용자 쿼터 상태 확인 : edquota -u [파일시스템 경로]