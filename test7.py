import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 80))
s.listen(5)
sock, addr=s.accept()
print(addr)
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
sock.send(b'hahahahahah')
sock.close()