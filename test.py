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
        client.connect(hostname=hostip, username=username, password=password, timeout=3)
        return client
    except Exception as e:
        print("连接服务器失败，错误信息：{}".format(e))
        exit(1)


def excute_command(client, command):
    try:
        stdin, stdout, stderr = client.exec_command(command)
    except Exception as e:
        client.close()
        return e
    else:
        standout = stdout.read().decode('utf-8')
        return standout

def action2(max):
    for i in range(max):
        if i == 30:
            sys.exit(1)
        print(threading.current_thread().getName()+ " "+str(i))


def action(max):
    for i in range(max):
        print(threading.current_thread().getName()+ " "+str(i))

threading.Thread(target=action, args=(80,), name="新线程").start()
for i in range(100):
    if i == 20:
        jt = threading.Thread(
                             target=action2,
                             args=(80,),name="被join的线程"
        )

        jt.start()
        jt.join()
print(threading.current_thread().name + " " + str(i))
print("子程序执行完了")



