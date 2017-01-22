import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 80))
s.listen(5)
sock, addr=s.accept()
harder=body=host=b''
while True:
        harder = sock.recv(1024)
#         print(data)
#         print(data[-4:])
        if harder.find(b'\r\n\r\n')>=0 :
            body=harder[harder.find(b'\r\n\r\n')+4:]
            harder=harder[:harder.find(b'\r\n\r\n')+4]
            length=harder.find(b'Host:')
            host=harder[length:length+100][harder[length:length+100].find(b':')+1:harder[length:length+100].find(b'\r\n')].decode("UTF-8").strip()
            if harder.find(b'Content-Length:')>=0 :
               length=harder.find(b'Content-Length:')
               length=int(harder[length:length+20][harder[length:length+20].find(b':')+1:harder[length:length+20].find(b'\r\n')].decode("UTF-8").strip())
               while len(body)<length:
                   body += sock.recv(1024)
        break              
#         s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(harder,body,host)
host=host.split(":")
port=host[1] if len(host)>1  else "80"
# # 创建一个socket:
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # 建立连接:
s1.connect((host[0], int(port)))
print(harder+body)
s1.send(harder+body)
buffer = []
while True:
    # 每次最多接收1k字节:
    d = s1.recv(1024)
    if d:
        buffer.append(d)
    else:
        break
data = b''.join(buffer)
print(data)
s1.close()
sock.send(data)
sock.close()


# s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s1.connect(("www.sunrui123.com", 80))
# s1.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')
# buffer = []
# while True:
#     # 每次最多接收1k字节:
#     d = s1.recv(1024)
#     if d:
#         buffer.append(d)
#     else:
#         break
# data = b''.join(buffer)
# print(data)
