import socket
from cv2 import textureFlattening
import pandas
import pickle
import sys

# TCP通信関係
#
# HOSTNAME = "172.25.180.202"  # 自分のサーバーのIPアドレス
HOSTNAME = "localhost"
PORT = 10541
MAXBITE = 4098


search_Word = "shfjshjfhsdj"
Search_Index = 1

# ipv4を使うので、AF_INET
# tcp/ip通信を使いたいので、SOCK_STREAM
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOSTNAME, PORT))
if search_Word == "":
    print("Error:何も入っていない")
    sys.exit()
sock.send(bytes(search_Word, "utf-8"))

# data = sock.recv(MAXBITE)
# if data == 0:
#     sock.recv(1)
#     print("Error:1 文字が入っていません")
#     sys.exit()

# print(data)
datas = b""
times = int(sock.recv(MAXBITE).decode("utf-8"))
if times == -1:
    datas = int(sock.recv(MAXBITE).decode("utf-8"))
else:
    time = 0
    print("受信開始")
    while True:
        data = sock.recv(MAXBITE)
        print(len(data))
        if len(data) == 0:
            break
        datas += data
        time += len(data)
        print("\r {:.2f} % was finished.".format(time/times*100), end=" ")
    print("受信完了")
    datas = pickle.loads(datas)

    print([d[Search_Index] for d in datas])

    print(len(datas))

print(datas)
sock.close()
