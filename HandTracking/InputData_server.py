import socket

HOST_NAME = "0.0.0.0"  # ポート開放
PORT = 10541
max_num = 5
MAX_BIN = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((HOST_NAME, PORT))

sock.listen(max_num)
print("connecting....")

client, remote_addr = sock.accept()
print("accepted remote. remote_addr:{}".format(remote_addr))
client.sendall('Connected!! :{}'.format(HOST_NAME).encode())

while True:
    rcv_data = client.recv(MAX_BIN)
    #データが無いなら
    if not rcv_data:
        #表示して終了
        print("remote data don't exist.")
        break
    print("receve data :{}".format(rcv_data.decode("utf-8")))


print("close client communication")
client.close()
sock.close()
