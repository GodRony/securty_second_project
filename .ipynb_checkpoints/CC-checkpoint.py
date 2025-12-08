import paramiko

class CC:
    def __init__(self, ip, user, pw, port=22):
        print("실행")
        self.ip = ip
        self.user = user
        self.pw = pw
        self.port = port
        self.client = None

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(
            hostname=self.ip,
            username=self.user,
            password=self.pw,
            port=self.port
        )

    def run(self, cmd, print_output=True):
        if self.client is None:
            self.connect()

        stdin, stdout, stderr = self.client.exec_command(cmd, get_pty=True)
        out = stdout.read().decode()
        err = stderr.read().decode()

        if print_output:
            print(out if out else err)

        return out if out else err

    def close(self):
        if self.client:
            self.client.close()
            self.client = None

    def get_sftp(self):
        transport = paramiko.Transport((self.ip, self.port))
        transport.connect(username=self.user, password=self.pw)
        sftp = paramiko.SFTPClient.from_transport(transport)
        return sftp, transport

    def r_ssh(self, remote_path):
        sftp, transport = self.get_sftp()
        with sftp.open(remote_path, "r") as f:
            data = f.read().decode()
        sftp.close()
        transport.close()
        return data

    def w_ssh(self, remote_path, content):
        sftp, transport = self.get_sftp()
        with sftp.open(remote_path, "w") as f:
            f.write(content)
        sftp.close()
        transport.close()

    def a_ssh(self, remote_path, content):
        sftp, transport = self.get_sftp()
        with sftp.open(remote_path, "a") as f:
            f.write(content)
        sftp.close()
        transport.close()

