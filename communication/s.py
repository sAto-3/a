from datetime import datetime
import socket


print('The server started at', datetime.now())
print('Waiting...')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('127.0.0.1', 50000))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print('data: ', data, 'addr: ', addr)
                conn.sendall(b'Receive: ' + data)
