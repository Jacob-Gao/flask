from pro_flask.app01 import app01
from flask import render_template, request,flash
import paramiko, sys


def connect_to_remote_host(hostip, username='root', password='xY6#1WgBj2kR8l4fg'):
    client = paramiko.client.SSHClient(
    )  # A high-level representation of a session with an SSH server
    client.load_system_host_keys()  # 读known hosts文件里的public key，没有再说
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 或者接受用WarningPolicy()
    client.connect(hostip, username=username, password=password, timeout=4)
    return client


def excute_command(client, command):
    try:
        stdin, stdout, stderr = client.exec_command(command)

    except Exception as e:
        client.close()
        return e
    else:
        standout = stdout.read().decode('utf-8')
        stderr = stderr.read().decode('utf-8')
        STR = standout + stderr
        return STR


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

        try:
            client = paramiko.client.SSHClient(
            )  # A high-level representation of a session with an SSH server
            client.load_system_host_keys()  # 读known hosts文件里的public key，没有再说
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 或者接受用WarningPolicy()
            client.connect(ip_address, username='root', password='XXXXX', timeout=4)
        except Exception as e:
            print(e)
            return render_template('get-log.html', output="输入的机器ip错误或者无法连接！")
        else:
            if name and passwd:
                client = connect_to_remote_host(ip_address, username=name, password=passwd)
            else:
                client = connect_to_remote_host(ip_address)

            cmd = "tail -n {} {}".format(lines, log_path)
            output = excute_command(client, cmd)
            client.close()
            print(output)
            return render_template('get-log.html', output=output)


