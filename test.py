import paramiko
import sys,threading,time

hostlist=['192.168.1.1', '192.168.1.252']

def connect_to_remote_host(hostip, username='root', password='jacob'):
    client = paramiko.client.SSHClient(
    )  # A high-level representation of a session with an SSH server
    client.load_system_host_keys()  # 读known hosts文件里的public key，没有再说
    client.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())  # 或者接受用WarningPolicy()
    try:
        client.connect(hostname=hostip, username=username, password=password, timeout=5)
        for i in range(10):
            print(i)
            time.sleep(1)

        return client
    except Exception as e:
        print("连接服务器失败，错误信息：{}".format(e))
        sys.exit()


