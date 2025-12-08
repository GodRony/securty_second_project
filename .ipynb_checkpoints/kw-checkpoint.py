def nfs_client_mount(self):

    nfs_server_ip = input("접속할 smb 서버의 ip주소를 입력하세요. ex)172.16.12.100 or 도메인:") #접속할 smb 서버의 ip 주소 or 도메인
    nfs_share_folder = input("서버에 지정된 공유 폴더의 이름을 입력하세요. ex)share : ") #서버에 지정된 공유 폴더의 이름
    nfs_client_mount_point = input("본인 서버에 연결할 위치를 지정하세요. ex) /mnt/win_share : ")# 연결할 위치(클라이언트)
    auto = input("/etc/fstab에 부팅 시 자동마운트 설정을 하시겠습니까?  ex) y/n : ")

    if self.os == "Ubuntu" :
        cmd1 = (f"apt -y update && apt -y upgrade")
        cmd2 = (f"mkdir -p {slef.nfs_mount_point}")
        cmd3 = (f"""mount -t nfs {nfs_server_ip}:{nfs_share_folder} {nfs_client_mount_point}""")
        
        if auto == "y":
            cmd4 = (f"{nfs_server_ip}:{nfs_share_folder} {nfs_client_mount_point} nfs defaults 0 0 | sudo tee -a /etc/fstab")
            cmd5 = (f"mount -a") # 마운트 설정 적용
            cmd6 = (f"df") # 마운트 확인
        return cmd1, cmd2, cmd3, cmd4, cmd5, cmd6
  
    else:
        cmd7 = (f"apt -y update && apt -y upgrade")
        cmd8 = (f"mkdir -p {nfs_mount_point}")
        cmd9 = (f"""mount -t nfs {nfs_server_ip}:{nfs_share_folder} {nfs_client_mount_point}""")
        auto = input("/etc/fstab에 부팅 시 자동마운트 설정을 하시겠습니까?  ex) y/n : ")
        if auto == "y":
            cmd10 = (f"{nfs_server_ip}:{nfs_share_folder} {nfs_client_mount_point} nfs defaults 0 0 | sudo tee -a /etc/fstab")
            cmd11 = (f"mount -a") # 마운트 설정 적용
            cmd12 = (f"df") # 마운트 확인
        return cmd7, cmd8, cmd9, cmd10, cmd11, cmd12

형식: mount <서버IP>:<공유경로> <로컬_마운트_포인트>
mount -t nfs 172.16.254.2:/srv/nfs_share /mnt/nfs_server

cmd = (f"//{smb_server_ip}/{smb_share_folder}    {smb_client_mount_point}    cifs    defaults    0 0 | sudo tee -a /etc/fstab")