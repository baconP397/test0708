import socket
import  threading

# 本机ip和端口号
host = socket.gethostname()
port = 12345

# 创建socket，绑定，监听，接受客户端连接请求
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen(5)
print("服务端已启动，等待客户端连接")

clients = {}
lock = threading.Lock()

def send_to_target(message,target_address,client_address):
    with lock:
        if target_address in clients:
            msg = f"{client_address},{message}"
            clients[target_address].send(msg.encode())


def handle_clients(client_socket,client_address):
    print(f"已连接 {client_address} ")
    with lock:
        clients[client_address] = client_socket
    while True:
        try:
        # 接受客户端信息
            message = client_socket.recv(1024)
            if not message:
                break

            # 拆分信息
            target_ip,target_port,msg = message.decode().split(',',2)
            target_address = (target_ip,int(target_port))
            print(f"已收到 {client_address} 的消息：{msg},发送到 {target_address}")
            send_to_target(msg,target_address,client_address)
        except ConnectionAbortedError:
            print(f"客户端 {client_address} 已断开连接")
            break

    print(f"客户端 {client_address} 已断开连接")
    with lock:
        del clients[client_address]
    client_socket.close()
    

 
while True:
    # 接受connect 和ip地址
    client_socket,client_address = server.accept()
    thread = threading.Thread(target=handle_clients,args=(client_socket,client_address))
    thread.start()


