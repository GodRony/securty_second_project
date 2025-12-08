#계정관리
#==========================================================================
#필요한 변수 

#아이피    --> ip
#계정이름  --> user
#계정패스워드  --> pw
#그룹명    --> grp
cmd = ""

#==========================================================================
#메소드 

#계정목록보여주기    tail -n 5 /etc/passwd


#특정계정만 확인     grep 계정명 /etc/passwd  --> 반환 : 존재함, 존재하지 않음

#계정추가                   useradd 계정명
#--> #계정 중복확인   grep -c "^계정명:" /etc/passwd 없는 경우에만 추가
#계정패스워스설정               passwd 계정명  같음    #비밀번호 변경          passwd 계정명

#계정+홈디렉토리 삭제   userdel -r 계정명  <-- 이거로 함 #계정삭제              userdel 계정명 

#그룹에 추가      usermod -aG 그룹명 계정명

#그룹에서 제거       gpasswd -d 계정명 그룹명

#계정 비활성화      usermod -L 계정명

#계정 활성화     usermod -U 계정명

#계정 존재여부 확인    id 계정명



#그룹 기반 권한 - 그룹에 따라 공동 접근 권한 설정 가능   groupadd 그룹명 
#                                                      chgrp 그룹명 파일명
#                                                      chmod 770 파일명


# u = User(ip, user, pw, grp)   <-- 생성  


class User:
    #그룹명    --> 
    grp = ""
    new_user = ""
    new_group = ""
    cmd = ""
    def __init__(self):
        print("User동작")

    #계정목록보여주기
    def list_user(self):
        # /etc/passwd 파일 중 마지막 5줄만 출력
        return "tail -n 5 /etc/passwd"

    #특정계정만 확인
    def check_user(self):
        if f"grep '{user}' /etc/passwd":
            return "존재함"   #True
        else:
            return "존재하지 않음"   # False

    #계정 중복 확인
    def account_check(self):
        new_user = input("새로 생성할 계정명을 알려주세요:")
        return f'grep -c \"^{new_user}:\" /etc/passwd'
        
    #계정 추가 : 계정 중복 확인 후 실행
    def account_add(self):
        return f'useradd -m {new_user}'

    #그룹 추가 : 그룹 중복 확인 후 실행
    def group_add(self):
        return f'groupadd {new_group}'
  
    #계정 비밀번호
    def account_pw(self):
        new_pw = input("%s의 비밀번호를 알려주세요 :"%(new_user))
        expect_script = f'''
                        expect -c " 
                        set timeout 3
                        spawn passwd {new_user}
                        expect \\"New password:\\"
                        send \\"{new_pw}\\r\\"
                        expect \\"Retype new password:\\"
                        send \\"{new_pw}\\r\\"
                        expect eof"
                        '''
        return expect_script

    #계정삭제: 계정 중복 확인 후 실행
    def account_del(self):
        del_user = input("삭제할 계정명을 알려주세요:")
        return f'userdel -r {del_user}'

    def account_status(self, user):
        self.user = user
        c = input("활성(Y)/비활성(N)")
        if c == "Y" or c == "y":
            return f'usermod -U {user}'
        else:
            return f'usermod -L {user}'

    #그룹 중복 확인
    def account_group_check(self):
        new_group = input("새로 생성할 그룹명을 알려주세요:")
        return f'grep -c \"^{new_group}:\" /etc/group'

    #그룹에 추가      usermod -aG 그룹명 계정명
    def account_add_group(self, new_group, new_user):
        return f'groupadd -aG {new_group} {new_user}'

     #그룹에서 제거       gpasswd -d 계정명 그룹명

    def account_del_group(self, user, grp):
        return f'gpasswd -d {user} {grp}'


if __name__=="__main__":
    print("테스트 모드로 실행되었습니다.")
    a = User()
    print(a.account_add_group("kkk", "kong"))




















