import socket
import pandas
import pickle
import sys

# HOST_NAME = "0.0.0.0"  # ポート開放
HOST_NAME = "localhost"
PORT = 10541
max_num = 5
MAX_BIN = 1024
Data_File = "a\HandTracking\Data\dataset_20211201-1.csv"
Search_Word = ""
Search_Index = 1
Sort_Index = 10

# ソケット通信の準備
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST_NAME, PORT))

# csvファイルの準備
Data_Frame = pandas.read_csv(Data_File)
Data_Index = Data_Frame.columns.values


# 接続
sock.listen(max_num)
print("[]:connecting....")

client, remote_addr = sock.accept()
print("[]:accepted remote. remote_addr:{}".format(remote_addr))
client.sendall('[]:Connected!! :{}'.format(HOST_NAME).encode())


# 検索ワードの受信
rcv_data = client.recv(MAX_BIN)
rcv_data = rcv_data.decode("utf-8")
# データが無いなら
if not rcv_data:
    # 表示して終了
    print("[]:remote data don't exist.")
    client.close()
    sock.close()
    sys.exit()
print("[]:receve data :{}".format(rcv_data))

# 検索
# if rcv_data=="":
#     #空状態だと検索に時間がかかるため、エラー値を返す
#     client.send(0)
#     client.send(pickle.dumps(-1))
Search_Word = rcv_data
Search_Result = Data_Frame[Data_Frame[Data_Index[Search_Index]].str.contains(Search_Word)]
# print(len(Search_Result))
if not Search_Result.empty:
    # 送信
    # client.send(bytes(str(len(Search_Result)), "utf-8"))
    client.send(pickle.dumps(Search_Result.values.tolist()))
    print("[]:data was send.")

print("[]:close client communication")
client.close()
sock.close()
