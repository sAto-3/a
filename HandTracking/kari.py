from ctypes import FormatError
from ctypes.wintypes import POINT
from typing import ItemsView
from PIL.ImageDraw import ImageDraw
import cv2
import time
import numpy as np
import math
import sys

import pyautogui
import handtrackingModule as htm
import module


# 初期設定
# ウィンドウの大きさの設定
wCam, hCam = 800, 450
frameR = 100


# ディスプレイの大きさの測定
(wWin, hWin) = pyautogui.size()
print("横：{0} 縦：{1}".format(wWin, hWin))

# 動画関係設定
print("カメラ読み込み開始")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
print("カメラ読み込み終了")
cap.set(3, wCam)
cap.set(4, hCam)
cap.set(cv2.CAP_PROP_FPS, 60)
pTime, cTime = 0, 0

# 画像処理関係
detector = htm.handDetectior(MaxHands=2, detectonCon=0.7)
font_Path = "C:\Windows\Fonts\HGRGM.TTC"

# 判定フラグ初期値設定
MENU_FLAG = False
MODE01_FLAG = False
MODE02_FLAG = False
MODE03_FLAG = False
MODE04_FLAG = False
COMFIG_FLAG = False


print("本動作開始")


# 本動作(1Fごとの動作)
while True:
    # 画像の読み込み
    success, img = cap.read()
    if success is not True:
        print("画像読み込み失敗")
        break
    img2 = np.full((hCam, wCam, 3), 255, dtype=np.uint8)

    # 手を認識させる
    img = detector.findHands(img)
    # detectorの手listを取得する
    lmlist, bbox = detector.findPosition(img2, drawPosition=False)

    # if 手が認識した
    if len(lmlist) != 0:
        # print(lmlist)

        # 指をおろしている判定を取得
        checkedList = detector.checkFinger()
        # print(checkedList)

        if MENU_FLAG is not True and checkedList[0] == [1, 1, 1, 1, 1]:
            print("MENU")
            MENU_FLAG = True

        if MENU_FLAG is True and checkedList[0] == [0, 0, 0, 0, 0]:
            print("CLEAR")
            MENU_FLAG = False

        # if MENU_FLAG is not True and checkedList[0] == [0, 1, 0, 0, 0]:
        #     print("POINT")
        #     POINT_FLAG = True

            # フラグが立っているならメニュー動作をする。
        if MENU_FLAG:
            # 動作
            if checkedList[0] == [0, 1, 1, 1, 1]:
                MODE01_FLAG = True
            else:
                MODE01_FLAG = False
            if checkedList[0] == [1, 0, 1, 1, 1]:
                MODE02_FLAG = True
            else:
                MODE02_FLAG = False
            # if checkedList[0] == [0, 0, 0, 0, 0]:
            #     MODE01_FLAG = True
            if checkedList[0] == [1, 1, 1, 1, 0]:
                COMFIG_FLAG = True
            else:
                COMFIG_FLAG = False
            # if checkedList[0] == [0, 1, 0, 0, 0]:
            # if checkedList[0] == [0, 0, 1, 0, 0]:
            # if checkedList[0] == [0, 0, 0, 1, 0]:
            # if checkedList[0] == [0, 0, 0, 0, 1]:

            # UI
            # タイトル
            module.cv2_putText_4(img2, "タイトル(仮)", (1, 50),
                                 font_Path, 30, (0, 0, 0))

            # モード選択
            FONT_SIZE = 20
            if MODE01_FLAG:
                module.cv2_putText_4(
                    img2, "モード１", (lmlist[0][4][1], lmlist[0][4][2]), font_Path, FONT_SIZE, (0, 0, 255))
            else:
                module.cv2_putText_4(
                    img2, "モード１", (lmlist[0][4][1], lmlist[0][4][2]), font_Path, FONT_SIZE, (0, 0, 0))
            if MODE02_FLAG:
                module.cv2_putText_4(
                    img2, 'モード２', (lmlist[0][8][1], lmlist[0][8][2]), font_Path, FONT_SIZE, (0, 0, 255))
            else:
                module.cv2_putText_4(
                    img2, 'モード２', (lmlist[0][8][1], lmlist[0][8][2]), font_Path, FONT_SIZE, (0, 0, 0))
            if COMFIG_FLAG:
                module.cv2_putText_4(
                    img2, "設定", (lmlist[0][20][1], lmlist[0][20][2]), font_Path, FONT_SIZE, (0, 0, 255))
            else:
                module.cv2_putText_4(
                    img2, "設定", (lmlist[0][20][1], lmlist[0][20][2]), font_Path, FONT_SIZE, (0, 0, 0))

    # FPS表示設定
    cTime = time.time()
    fps = 1//(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {fps}', (40, 50),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    # 画像の表示
    cv2.imshow("Image", img)
    cv2.imshow("Point", img2)

    # 入力待ち 1F
    k = cv2.waitKey(1)
    # 入力がEscの場合閉じる
    if k == 27:
        print("終了処理")
        sys.exit()
