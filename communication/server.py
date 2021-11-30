# coding: utf-8

# ソケット通信(サーバー側)
import socket

# host1 = '127.0.0.1'  # localhostと同義 str
host1 = "0.0.0.0"  # ポート開放
port1 = 8775  # すきなポート番号

# ipv4を使う=>socket.AF_INET
# tcp/ip通信を使う=>socket.SOCK_STREAM
socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# アドレスとポート名を指定
socket1.bind((host1, port1))
# サーバーを付けて待つ
socket1.listen(1)
print('クライアントからの入力待ち状態')

# コネクションとアドレスを取得
connection, address = socket1.accept()
print(connection)
print('接続したクライアント情報:' + str(address))

# 無限ループ　byeの入力でループを抜ける
# 文字変数の設定
while True:
    # クライアントからデータを受信
    receive = connection.recv(2048).decode()
    if receive == "bye":
        break
    print("received -> message:{}".format(receive))
    send_message = "あなたが送信した文章は'{}'ですね".format(receive)
    # サーバー側から文章を送信
    connection.send(send_message.encode("utf-8"))
# クローズ　通信の終了
# 通信の終了
connection.close()
# サーバーの終了
socket1.close()
print('サーバー側終了です')
