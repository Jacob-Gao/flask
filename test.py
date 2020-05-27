import paramiko
import sys,threading,time

hostlist=['192.168.1.252', '192.168.1.1','192.168.1.254','192.168.1.253']
faild_list1 = list()
faild_list2 = list()
def connect_to_remote_host(hostip, username='root', password='jacob'):
    client = paramiko.client.SSHClient(
    )  # A high-level representation of a session with an SSH server
    client.load_system_host_keys()  # 读known hosts文件里的public key，没有再说
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 或者接受用WarningPolicy()
    client.connect(hostname=hostip, username=username, password=password, timeout=3)
    return client
    # try:
    #     client.connect(hostname=hostip, username=username, password=password, timeout=3)
    #     return client
    # except Exception as e:
    #     print("连接服务器失败，错误信息：{}".format(e))
    #     exit(1)

#
# def excute_command(client, command):
#     try:
#         stdin, stdout, stderr = client.exec_command(command)
#     except Exception as e:
#         client.close()
#         return e
#     else:
#         standout = stdout.read().decode('utf-8')
#         return standout




def check():
    for i in hostlist:
        try:
            client = paramiko.client.SSHClient(
            )  # A high-level representation of a session with an SSH server
            client.load_system_host_keys()  # 读known hosts文件里的public key，没有再说
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 或者接受用WarningPolicy()
            client.connect(i, username='root', password='jacob',timeout=4)
        except Exception as e:
            print(e)
            faild_list1.append(i)
            print(faild_list1)
        finally:
                client.close()

    for i in faild_list1:
        hostlist.remove(i)

    for i in hostlist:
        client = paramiko.client.SSHClient()  # A high-level representation of a session with an SSH server
        client.load_system_host_keys()  # 读known hosts文件里的public key，没有再说
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 或者接受用WarningPolicy()
        client.connect(i, username='root', password='jacob',timeout=4)
        sftp = client.open_sftp()
        try:
            sftp.stat('/data/tinyplat/')
            print("*" * 100)
            print("机器已经初始化过了，很有可能正在生产环境使用，请检查ip是否输入正确,ip地址为{}")
            print("*" * 100)
            client.close()
            hostlist.remove(i)
        except Exception as e:
            print(e)
            pass





check()
print("**********************************")
print(hostlist)
