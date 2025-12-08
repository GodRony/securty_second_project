from dhcp import Dhcp

def main():
    print("="*60)
    print("DHCP 서버 자동 구성 프로그램")
    print("="*60)
    
    # 사용자 입력으로 객체 생성
    print("\n서버 정보를 입력하세요:")
    os_type = input("OS 종류 (예: Rocky9): ")
    server_ip = input("서버 IP 주소: ")
    interface = input("네트워크 인터페이스 (예: ens160): ")
    
    # DHCP 객체 생성
    dhcp = Dhcp(os_type, server_ip, interface)
    
    while True:
        menu = """
============================================================
메뉴를 선택하세요:
============================================================
1. OS 정보 확인
2. DHCP 서버 설치
3. DHCP 서비스 시작/중지
4. DHCP 옵션 설정
5. IP 풀 설정
6. IP Range 추가
7. IP Range 삭제
8. 현재 설정 확인
9. 설정 백업
10. 로그 파일 생성
11. 로그 확인
0. 종료
============================================================
"""
        print(menu)
        choice = input("선택: ")
        
        if choice == "1":
            print("\n[OS 정보 확인]")
            dhcp.chk_os()
            
        elif choice == "2":
            print("\n[DHCP 서버 설치]")
            dhcp.install()
            
        elif choice == "3":
            print("\n[DHCP 서비스 시작/중지]")
            dhcp.on_off()
            
        elif choice == "4":
            print("\n[DHCP 옵션 설정]")
            dhcp.option()
            
        elif choice == "5":
            print("\n[IP 풀 설정]")
            dhcp.set_pool()
            
        elif choice == "6":
            print("\n[IP Range 추가]")
            dhcp.ins_pool()
            
        elif choice == "7":
            print("\n[IP Range 삭제]")
            dhcp.del_pool()
            
        elif choice == "8":
            print("\n[현재 설정 확인]")
            dhcp.chk_pool()
            
        elif choice == "9":
            print("\n[설정 백업]")
            dhcp.backup()
            
        elif choice == "10":
            print("\n[로그 파일 생성]")
            dhcp.set_log()
            
        elif choice == "11":
            print("\n[로그 확인]")
            dhcp.chk_log()
            
        elif choice == "0":
            print("\n프로그램을 종료합니다.")
            break
            
        else:
            print("\n잘못된 선택입니다. 다시 선택하세요.")
        
        input("\n계속하려면 Enter를 누르세요...")

if __name__ == "__main__":
    main()