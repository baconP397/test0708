import socket
import threading 
import queue
import re

host = socket.gethostname()
port = 12345

client = socket.socket()

client.connect((host, port))
print('已经和服务端建立连接')

# 获取自身IP和端口号
client_ip, client_port = client.getsockname()
print(f"本客户端的IP地址: {client_ip}, 端口号: {client_port}")


def validate_ip(ip):
    ip_pattern = re.compile(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    return ip_pattern.match(ip)


def validate_port(port):
    port_pattern = re.compile(r"^[0-9]{1,5}$")
    return port_pattern.match(port) and 0 < int(port) < 65536

def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                print("服务器断开连接")
                break
            source_address,source_port,msg = message.decode().split(",",2)
            print(f"-------收到来自{source_address} : {source_port}的新消息啦！！！--------------")
            print("接收到的内容是：" + msg)
            print("------------------------------------------------------------")
        except ConnectionAbortedError:
            print("连接终止")
            break
        except msg == 'bye':
            print("连接终止")
            client.close()
            break



def send_message():
    target_ip = input("请输入目标的IP地址:")
    while not validate_ip(target_ip):
        print("无效的ip地址,请重新输入")
        target_ip = input("请输入目标的IP地址:")

    target_port = input("请输入目标的端口号:")
    while not validate_port(target_port):
        print("无效的端口号，请重新输入")
        target_port = input("请输入目标的端口号:")

    send_data = input("请输入要发送的内容 :")
    print("-------------------------------------------")
    message = f"{target_ip},{target_port},{send_data}"
    client.send(message.encode())
    if send_data.lower() == 'bye':
        client.close()


# 启动接收消息线程
receive_thread = threading.Thread(target=receive_message, args=(client,))
receive_thread.daemon = True
receive_thread.start()
while True:
    send_message()