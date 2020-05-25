import paramiko


#
# # 实例化一个transport对象
# trans = paramiko.Transport(('192.168.1.252', 22))
# # 建立连接
# trans.connect(username='root', password='jacob')
#
# # 将sshclient的对象的transport指定为以上的trans
# ssh = paramiko.SSHClient()
# ssh._transport = trans
# # 执行命令，和传统方法一样
# stdin, stdout, stderr = ssh.exec_command('cd /root/shell')
# print(stdout.read().decode())
# stdin, stdout, stderr = ssh.exec_command('pwd')
# print(stdout.read().decode())
# stdin, stdout, stderr = ssh.exec_command('touch /root/ouhu')
# print(stdout.read().decode())

trans = paramiko.Transport(('192.168.1.252', 22))
trans.start_client()
trans.auth_password(username='root', password='jacob')
channel = trans.open_session()


