import cv2
import time
import numpy as np
import math
import sys
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from numpy.lib.polynomial import polyfit
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import handtrackingModule as htm

# ウィンドウの大きさの設定
wCam, hCam = 640, 480

# 動画関係設定
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetectior(detectonCon=0.7)

# 音量関係設定
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPar = 0
volumeChange = False

# 本動作
while True:
    # 画像の読み込み
    success, img = cap.read()
    img2 = np.full((hCam, wCam, 3), 255, dtype=np.uint8)

    # 手を認識させる
    img = detector.findHands(img)
    # detectorの手listを取得する
    lmlist = detector.findPosition(img, draw=False)
    # if 手が認識した
    if len(lmlist) != 0:
        # print(lmlist)
        # 指の根元の座標listxを取得
        Xmax, Ymax = 0, 0
        Xmin, Ymin = 10e8, 10e8
        for id, lm in enumerate(lmlist):
            Xmax, Ymax = max(Xmax, lm[1]), max(Ymax, lm[2])
            Xmin, Ymin = min(Xmin, lm[1]), min(Ymin, lm[2])
            if 5 <= id <= 17 and id % 4 == 1:
                cv2.circle(img2, (lm[1], lm[2]), 1, (0, 255, 0), cv2.FILLED)
            else:
                cv2.circle(img2, (lm[1], lm[2]), 1, (255, 0, 0), cv2.FILLED)

        # 4:親指の先端の座標を取得
        # 8:人差し指の先端の座標を取得
        x4, y4 = lmlist[4][1], lmlist[4][2]
        x8, y8 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x4 + x8) // 2, (y4 + y8) // 2

        cv2.rectangle(img2, (Xmin, Ymin), (Xmax, Ymax), 2)

        cv2.circle(img, (x4, y4), 5, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x8, y8), 5, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x4, y4), (x8, y8), (255, 10, 255), 3)

        length = math.sqrt((x4-x8)**2 + (y4-y8)**2)
        # print(length)
        if length > 50:
            cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        # hand range 50-300
        # volume range -65-0
        if volumeChange:
            vol = np.interp(length, [50, 300], [minVol, maxVol])
            volBar = np.interp(length, [50, 300], [400, 150])
            volPar = np.interp(length, [50, 300], [0, 100])
            # print(int(length), vol)
            volume.SetMasterVolumeLevel(vol, None)

        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400),
                      (0, 255, 0), cv2.FILLED)
        # if 指をおろしている判定 指の根元の直線から判別できる？
        if lmlist[8][2] < lmlist[6][2] and lmlist[0][2] < lmlist[6][2]:
            cv2.putText(img2, "人差し指曲げた", (20, 30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 3)

        # TODO:音量を確定する

    # FPS表示設定
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cv2.putText(img, f'{int(volPar)} %', (40, 450),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    # 画像の表示
    cv2.imshow("Image", img)
    cv2.imshow("Point", img2)

    # 入力待ち 1F
    k = cv2.waitKey(1)
    # 入力がEscの場合閉じる
    if k == 27:
        sys.exit()
