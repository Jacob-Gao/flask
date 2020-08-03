from pro_flask.app01 import app01
from flask import render_template, request,flash
import paramiko, sys, threading


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
        standout = stdout.read().decode('utf-8')
        stderr = stderr.read().decode('utf-8')
        STR = standout + stderr
        return STR



def work_loop(y_host, y_user, y_passwd, host):
    # upload initial.sh,next.sh,python3.6 package
    client = connect_to_remote_host(hostip=y_host,
                                    username=y_user,
                                    password=y_passwd)

    excute_command(
        client=client,
        command=
        '/bin/bash /app/srv/salt/files/tianyan/zabbix/install.sh {}'.format(host))  # yunwei machine log
    client.close()






@app01.route('/install-zabbix.html', methods=['GET', 'POST'])
def install_zabbix():
    if request.method == 'GET':
        return render_template('install-zabbix.html')
    else:
        ip_address = request.form.get('ip_address')
        hostlist = ip_address.split()
        faild_list = list()
        # t_user = "root"
        # t_passwd = "XXXXXXXXXX"
        y_host = "XXXXXXXXXX"
        y_user = "root"
        y_passwd = "XXXXXXXXXX"

        for i1 in hostlist:
            try:
                client = paramiko.client.SSHClient(
                )  # A high-level representation of a session with an SSH server
                client.load_system_host_keys()  # 读known hosts文件里的public key，没有再说
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 或者接受用WarningPolicy()
                client.connect(i1, username='root', password='XXXXXXXXXX', timeout=4)
            except Exception as e:
                print(e)
                faild_list.append(i1)
            else:
                client.close()

        for i2 in faild_list:
            hostlist.remove(i2)

        host_num = len(hostlist)
        print(hostlist)
        if host_num != 0:
            for i3 in range(host_num):
                t = threading.Thread(name='process on {}'.format(hostlist[i3]),
                                     target=work_loop,
                                     args=(y_host, y_user, y_passwd, hostlist[i3],
                                           ))
                t.start()
                print("hhh")
            return render_template('install-zabbix.html', output="安装zabbix客户端成功！")
        else:
            return render_template("install-zabbix.html", output="输入的机器ip错误或者无法连接！")
