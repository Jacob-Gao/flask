from pro_flask.app01 import app01
from flask import render_template, request,flash
import paramiko, sys
from pro_flask.app01.tools.sendmail import send_mail

def connect_to_remote_host(hostip, username='root', password='XXXXXXXXXX'):
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



@app01.route('/vpn.html', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('vpn.html')
    else:
        UserName = request.form.get('aname')
        pwd = request.form.get('apwd')
        mail = request.form.get('amail')
        UserName2 = request.form.get('bname')
        if UserName and pwd and mail:
            client = connect_to_remote_host('172.16.1.67')
            output = excute_command(client=client, command='/root/anaconda3/envs/flask/bin/python /root/add_VPN/add_user1.0.py {} {}'
                                    .format(UserName, pwd))
            # client = connect_to_remote_host('172.16.10.111')
            # output = excute_command(client=client, command='python /root/add_user1.0.py {} {}'
            #                         .format(UserName, pwd))
            client.close()
            #构建邮件
            content = """
            VPN账号为{}，
            VPN密码为{},
            """.format(UserName, pwd)
            subject = '%s 您好，运维帮你开通VPN的信息如下' % UserName
            result = send_mail(subject=subject, content=content, mail=mail)
            output = output + result
            return render_template('vpn.html', aoutput=output)
        if UserName or pwd or mail:
            return render_template('vpn.html', aoutput='请将用户名，密码和邮箱填写完整！')
        if UserName2:
            client = connect_to_remote_host('172.16.1.67')
            output2 = excute_command(client=client,
                                command='userdel -r {}'
                                .format(UserName2))
            client.close()
            if not output2:
                return render_template('vpn.html', output2='{} 删除成功'.format(UserName2))
            else:
                return render_template('vpn.html', output2=output2)

