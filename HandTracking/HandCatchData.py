
from os import write
import cv2
import numpy as np
import sys
import csv
import json

import pyautogui
import handtrackingModule as htm
import module
import matplotlib.pyplot as plt

# 初期設定
# ウィンドウの大きさの設定
wCam, hCam = 800, 450

# ディスプレイの大きさの測定
(wWin, hWin) = pyautogui.size()
print("横：{0} 縦：{1}".format(wWin, hWin))

# 動画関係設定
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
pTime, cTime = 0, 0

# 画像処理関係
detector = htm.handDetectior(MaxHands=2, detectonCon=0.7)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

HandData = []
time = 0


# 本動作(1Fごとの動作)
print("本動作開始")
while True:
    # 画像の読み込み
    success, img = cap.read()
    if success is not True:
        print("画像読み込み失敗")
        break

    # 手を認識させる
    img = detector.findHands(img)
    # detectorの手listを取得する
    lmlist, bbox = detector.findPosition(img)

    # if 手が認識した
    if len(lmlist) != 0:
        # print(lmlist)
        # 指をおろしている判定を取得
        checkedList = detector.checkFinger()
        # print(checkedList)
        # print(len(lmlist))

    # 画像の表示
    cv2.imshow("Image", img)

    # 入力待ち 1F
    k = cv2.waitKey(1)
    # 入力がEscの場合閉じる
    if k == 27:
        print("終了処理")
        break
    # 1キーで座標を登録
    elif k == 49:
        # データの追加
        HandData.append(lmlist)
        time += 1
        print("SAVEING")
    # 2キーを押したら初期化
    elif k == 50:
        HandData = []
print(HandData)
# [frame][hand][xyz][id]
# 保存した座標を表示
if HandData:
    # print(len(showIMG[0]), len(showIMG[0][0]))
    for frame in range(len(HandData)):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        for hand in range(len(HandData[frame])):
            for id in range(21):
                if id % 4 == 0:
                    ax.scatter(HandData[frame][hand][id][1], HandData[frame][hand]
                               [id][2], HandData[frame][hand][id][3], color="#DD0000")
                elif id % 4 == 1:
                    ax.scatter(HandData[frame][hand][id][0], HandData[frame][hand]
                               [id][2], HandData[frame][hand][id][3], color="#AA4400")
                elif id % 4 == 2:
                    ax.scatter(HandData[frame][hand][id][0], HandData[frame][hand]
                               [id][2], HandData[frame][hand][id][3], color="#778800")
                elif id % 4 == 3:
                    ax.scatter(HandData[frame][hand][id][0], HandData[frame][hand]
                               [id][2], HandData[frame][hand][id][3], color="#33CC00")
        plt.show()

# 　numpy.save でnpy形式で出力
num = 0
np.save("NPY/HandData{0}.tsv".format(str(num)), HandData,delimiter="t")
#テキストファイルで見たいときはこれ
with open("NPY/HandData{0}.tsv".format(str(num)), "w") as outfile:
    for slice3D in HandData:
        for slice2D in slice3D:
            np.savetxt(outfile, slice2D)
            outfile.write('# New 2Dslice\n')
        outfile.write('# New 3Dslice\n')
    # json形式で出力
    # with open("JSON/HandData{0}.json".format(str(time)), 'w') as f:
    #     l = HandData.tolist()
    #     s = json.dumps(l, indent=4)
    #     f.write(s)
