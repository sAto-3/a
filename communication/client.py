# coding: utf-8

# ソケット通信(クライアント側)
import socket

# ip1 = '172.25.180.202' #自分のipアドレス
ip1=socket.gethostname() #こっちも可：何ならこっちのほうがいい説
print(ip1)
# ip2 = "192.168.11.4"
# ip1 = '127.0.0.1'
port1 = 8775
server1 = (ip1, port1)

socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket1.connect(server1)
print("connected!")

line = ''
while line != 'bye':
    # 標準入力からデータを取得
    print('好きな文字を入力してください（終了は"bye"）')
    line = input('>>>')
    # サーバに送信
    socket1.send(line.encode("UTF-8"))
    # サーバから受信
    data1 = socket1.recv(2048).decode()
    # サーバから受信したデータを出力
    print('サーバーからの回答: ' + str(data1))

socket1.close()
print('クライアント側終了です')
