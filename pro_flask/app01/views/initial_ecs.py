from pro_flask.app01 import app01
from flask import render_template, request
import paramiko
import threading
import time


def connect_to_remote_host(hostip, username, password):
    client = paramiko.client.SSHClient(
    )  # A high-level representation of a session with an SSH server
    client.load_system_host_keys()  # 读known hosts文件里的public key，没有再说
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 或者接受用WarningPolicy()
    client.connect(hostname=hostip, username=username, password=password, timeout=5)
    return client


def excute_command(client, command):
    try:
        stdin, stdout, stderr = client.exec_command(command)

    except Exception as e:
        client.close()
        print(e)
    else:
        standout = stdout.read().decode()
        return standout


def work_loop(y_host, y_user, y_passwd, host, t_user, t_passwd):
    # upload initial.sh,next.sh,python3.6 package
    client = connect_to_remote_host(hostip=y_host,
                                    username=y_user,
                                    password=y_passwd)

    excute_command(
        client=client,
        command=
        '/bin/bash /root/copy_jdk_shell/copy_initial_shell.sh {} > /root/copy_jdk_shell/copy_initial_shell.log 2>&1'
            .format(host))  # yunwei machine log
    client.close()

    # excute initial.sh
    client = connect_to_remote_host(hostip=host,
                                    username=t_user,
                                    password=t_passwd)
    excute_command(client,
                   command=
                   '/bin/bash /root/initial.sh > /root/initial.log 2>&1')  # target machine log
    client.close()

    # upload JDK,tomcat package
    client = connect_to_remote_host(hostip=y_host,
                                    username=y_user,
                                    password=y_passwd)
    excute_command(
        client,
        command=
        '/bin/bash /root/copy_jdk_shell/copy_pak.sh {} >> /root/copy_jdk_shell/copy_initial_shell.log 2>&1'.format(
            host))
    client.close()
    # excute next.sh
    client = connect_to_remote_host(hostip=host,
                                    username=t_user,
                                    password=t_passwd)
    excute_command(client, '/bin/bash /root/next.sh >> /root/initial.log 2>&1')
    client.close()

def transfer_sshkey(y_host,y_user,y_passwd,hostlist,check_chaoxie):
    client = connect_to_remote_host(hostip=y_host,
                                    username=y_user,
                                    password=y_passwd)
    for i in range(len(hostlist)):
        # 传密钥
        if check_chaoxie:
            excute_command(
                client=client,
                command=
                '/usr/bin/expect /root/copy_jdk_shell/id_rsa_chaoxie.sh {} >> /root/copy_jdk_shell/copy_initial_shell.log 2>&1'
                    .format(hostlist[i]))
        else:
            excute_command(
                client=client,
                command=
                '/usr/bin/expect /root/copy_jdk_shell/id_rsa_weibofenqi.sh {} >> /root/copy_jdk_shell/copy_initial_shell.log 2>&1'
                    .format(hostlist[i]))

    client.close()


def yunwei_log_catch(y_host, y_user, y_passwd):
    client = connect_to_remote_host(hostip=y_host,
                                    username=y_user,
                                    password=y_passwd)
    yunwei_log = excute_command(client,
                                command=
                                'cat /root/copy_jdk_shell/copy_initial_shell.log ')
    client.close()
    return yunwei_log


def target_machine_log_catch(host, t_user, t_passwd, log):
    client = connect_to_remote_host(hostip=host,
                                    username=t_user,
                                    password=t_passwd)
    output = excute_command(client,
                            command=
                            'cat /root/initial.log')
    target_machine_log = log + output
    client.close()
    return target_machine_log


@app01.route('/index.html', methods=['GET', 'POST'])
def login():
    return render_template('index.html')


"""
hostlist is the host you wanna deploy,after finishing setting, run python demo_connect_test.py
attention: ip & passwd
# base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
"""


@app01.route('/initial-ecs.html', methods=['GET', 'POST'])
def initial():
    if request.method == 'GET':
        return render_template('initial-ecs.html')
    else:
        ip_address = request.form.get('ip_address')
        check_chaoxie = request.form.get('check-chaoxie')
        hostlist = ip_address.split()
        faild_list = list()
        t_user = "root"
        t_passwd = "xY6#1WgBj2kR8l4fg"
        y_host = "121.40.94.165"
        y_user = "root"
        y_passwd = "xY6#1WgBj2kR8l4fg"

        for i1 in hostlist:
            try:
                client = paramiko.client.SSHClient(
                )  # A high-level representation of a session with an SSH server
                client.load_system_host_keys()  # 读known hosts文件里的public key，没有再说
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 或者接受用WarningPolicy()
                client.connect(i1, username='root', password='xY6#1WgBj2kR8l4fg', timeout=4)
            except Exception as e:
                print(e)
                faild_list.append(i1)
            else:
                client.close()

        for i2 in faild_list:
            hostlist.remove(i2)

        for i4 in hostlist:
            client = paramiko.client.SSHClient()  # A high-level representation of a session with an SSH server
            client.load_system_host_keys()  # 读known hosts文件里的public key，没有再说
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 或者接受用WarningPolicy()
            client.connect(i4, username='root', password='xY6#1WgBj2kR8l4fg', timeout=4)
            sftp = client.open_sftp()
            try:
                sftp.stat('/data/tinyplat/')
                print("*" * 100)
                print("机器已经初始化过了，很有可能正在生产环境使用，请检查ip是否输入正确,ip地址为{}".format(i4))
                print("*" * 100)
                client.close()
                hostlist.remove(i4)
            except Exception as e:
                print(e)
                client.close()
                pass

        host_num = len(hostlist)
        print(hostlist)
        if host_num != 0:
            for i3 in range(host_num):
                t = threading.Thread(name='process on {}'.format(hostlist[i3]),
                                     target=work_loop,
                                     args=(y_host, y_user, y_passwd, hostlist[i3],
                                           t_user, t_passwd))
                t.start()
            time.sleep(300)
            transfer_sshkey(y_host,y_user,y_passwd,hostlist,check_chaoxie)
            yunwei_log = yunwei_log_catch(y_host, y_user, y_passwd)
            target_machine_log = ""
            for i in range(len(hostlist)):
                target_machine_log = target_machine_log_catch(hostlist[i], t_user, t_passwd, target_machine_log)
            return render_template('initial-ecs.html', yunwei_log=yunwei_log, target_machine_log=target_machine_log)
        else:
            return render_template("initial-ecs.html")
