from pro_flask.app01 import app01
from flask import render_template, request,flash
import paramiko, sys


def connect_to_remote_host(hostip, username='root', password='jacob'):
    client = paramiko.client.SSHClient(
    )  # A high-level representation of a session with an SSH server
    client.load_system_host_keys()  # 读known hosts文件里的public key，没有再说
    client.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())  # 或者接受用WarningPolicy()
    try:
        client.connect(hostname=hostip, username=username, password=password, timeout=5)
        return client
    except Exception as e:
        print("连接服务器失败，错误信息：{}".format(e))
        sys.exit()


def excute_command(client, command):
    try:
        stdin, stdout, stderr = client.exec_command(command)

    except:
        err = stderr.read().decode('utf-8')
        print(err)
        client.close()
        exit(1)
        return err
    else:
        standout = stdout.read().decode('utf-8')
        return standout


@app01.route('/get-log.html', methods=['GET', 'POST'])
def get_log():
    if request.method == 'GET':
        return render_template('get-log.html')
    else:
        ip_address = request.form.get('ip_address')
        log_path = request.form.get('log_path')
        lines = request.form.get('lines')
        name = request.form.get('name')
        passwd = request.form.get('pass')
        if name and passwd:
            client = connect_to_remote_host(ip_address, username=name, password=passwd)
        else:
            client = connect_to_remote_host(ip_address)

        cmd = "tail -n {} {}".format(lines, log_path)
        output = excute_command(client, 'tail -n 5 /var/messages')
        flash('超时')
        client.close()
        print(output)
        return render_template('get-log.html', output=output)


