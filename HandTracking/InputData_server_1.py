from os import access
import socket
import threading
import pandas
import pickle
import sys


def main_mortion(accept):
    Buffer_SIZE = 4096
    id = threading.get_ident()
    while True:
        # 検索ワードの受信
        try:
            print("ワードの受信中")
            rcv_data = accept.recv(Buffer_SIZE)
        except InterruptedError as e:
            print("recv:{}".format(e))

        # 検索ワードの変換
        rcv_data = rcv_data.decode("utf-8")
        if len(rcv_data) == 0:
            # EOFエラー
            print("[{}]recv:EOF".format(id))

        # 検索
        print("検索")
        Search_Word = rcv_data
        # 種類を指定している場合
        Search_Result = Data_Frame[Data_Frame[Data_Index[Search_Index]].str.contains(Search_Word)]
        # 全部検索する場合
        # Search_Result = Data_Frame[Data_Frame["タイトル"].str.contains(Search_Word)
        #                            and Data_Frame["タイトル（ふりがな）"].str.contains((Search_Word))
        #                            and Data_Frame["著者"].str.contains(Search_Word, case=False)
        #                            and Data_Frame["出版社"].str.contains(Search_Word, case=False)
        #                            and Data_Frame["出版社（ふりがな）"].str.contains(Search_Word, case=False)
        #                            ]
        # print(len(Search_Result))
        if not Search_Result.empty:
            # 送信
            print("送信")
            print("[ ]:{} datas matched.".format(len(Search_Result)))
            Search_Result_lens = pickle.dumps(Search_Result.values.tolist())
            # client.send(bytes(str(len(Search_Result_lens)), "utf-8"))
            print(Search_Result)
            accept.send(pickle.dumps(Search_Result.values.tolist()))
            print("[ ]:data was send.")

        print("[ ]:close client communication")
        accept.close()


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
print("[ ]:connecting....")
# client.send('[○]:Connected!! :{}'.format(HOST_NAME).encode())

while True:
    try:
        client, remote_address = sock.accept()
        host_data = socket.gethostname()
        Client_Thread = threading.Thread(target=main_mortion, args=[client])
        Client_Thread.start()

    except InterruptedError as e:
        print("[ ]accept:{}".format(e))

    except RuntimeError as e:
        print("[ ]thread:{}".format(e))
