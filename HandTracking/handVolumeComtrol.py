import cv2
import time
import numpy as np
import math
import sys
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui
import handtrackingModule as htm

# 基本設定
# ウィンドウの大きさの設定
wCam, hCam = 1280, 720
frameR = 100


# ディスプレイの大きさの測定
(wWin, hWin) = pyautogui.size()
print("横：{0} 縦：{1}".format(wWin, hWin))

# 動画関係設定
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
cap.set(cv2.CAP_PROP_FPS, 60)
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
detector = htm.handDetectior(MaxHands=1, detectonCon=0.7)

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
volumeFlag = False
volumeCounter = 0
volumeConfirmFrag = False
mouseFlag = False
mouseCounter = 0
allOffCounter = 0
x8, y8 = 0, 0
frame = 0
f = 0
print("ポインタの位置")
# 本動作
while True:
    # 画像の読み込み
    success, img = cap.read()
    img2 = np.full((hCam, wCam, 3), 255, dtype=np.uint8)

    # 手を認識させる
    img = detector.findHands(img, drawLandmark=False)
    # detectorの手listを取得する
    lmlist, bbox = detector.findPosition(img)

    # if 手が認識した
    if len(lmlist) != 0:
        # print(lmlist)

        # 指の根元の座標listxを取得
        Xmax, Ymax = bbox[2], bbox[3]
        Xmin, Ymin = bbox[0], bbox[1]

        cv2.rectangle(img2, (Xmin, Ymin), (Xmax, Ymax), 2)

        # 指をおろしている判定を取得
        checkedList = detector.checkFinger()
        # print(checkedList)

        # 親指と人差し指を上げるとボリューム操作がON
        if (volumeFlag or mouseFlag) is False and checkedList == [1, 1, 0, 0, 0]:
            volumeFlag = True
            mouseFlag = False
            volumeCounter = 0
            volumeConfirmFrag = False

        # ボリューム操作がONのとき、親指と人差し指、小指を上げるとボリュームが確定する
        if volumeFlag and checkedList == [1, 1, 0, 0, 1]:
            volumeConfirmFrag = True
            volumeFlag = False

        # 人差し指を上げるとマウス動作を開始
        if volumeFlag is False and checkedList == [0, 1, 0, 0, 0]:
            mouseFlag = True
            volumeFlag = False
            mouseCounter = 0

        # クリック動作
        if mouseFlag and checkedList == [0, 1, 1, 0, 0]:
            dl = ((lmlist[8][1]-lmlist[12][1])**2 +
                  (lmlist[8][2]-lmlist[12][2])**2)**0.5
            print('\r'+str(dl))
            if dl > 50 and mouseCounter == 60:
                cv2.putText(img2, "CLICK", (20, 20),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (155, 155, 155), 1)
                pyautogui.click()

        # 小指だけを上げているとボリューム操作がOFF マウス動作もOFF
        # TODO:音量を確定する
        if (volumeFlag or mouseFlag) and checkedList == [0, 0, 0, 0, 1]:
            volumeFlag = False
            mouseFlag = False
            allOffCounter = 0

        # 手の長さの範囲 50-300
        # volume range -65-0

        # 音量調節Flag
        if volumeFlag:
            # x4 y4: 親指の先端の座標を取得
            # x8 y8: 人差し指の先端の座標を取得
            # cx cy: 親指と人差指の先端の中点
            # length:親指と人差指の先端の長さ
            x4, y4 = lmlist[4][1], lmlist[4][2]
            x8, y8 = lmlist[8][1], lmlist[8][2]
            cx, cy = (x4 + x8) // 2, (y4 + y8) // 2
            cv2.circle(img, (x4, y4), 5, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x8, y8), 5, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x4, y4), (x8, y8), (255, 10, 255), 3)
            length = math.sqrt((x4 - x8) ** 2 + (y4 - y8) ** 2)
            # print(length)
            if length > 50:  # 長さが50以上
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            if volumeConfirmFrag is False:
                # 音量調整
                vol = np.interp(length, [50, 300], [minVol, maxVol])
                volBar = np.interp(length, [50, 300], [400, 150])
                volPar = np.interp(length, [50, 300], [0, 100])
                # print(int(length), vol)
                volume.SetMasterVolumeLevel(vol, None)

        # マウス操作Flag
        if mouseFlag:
            # frameR[100] dot分の余裕をもたせてマウス操作ウィンドウを表示
            cv2.rectangle(img, (frameR, frameR),
                          (wCam-frameR, hCam-frameR), (255, 0, 255), 2)
            cv2.rectangle(img2, (frameR, frameR),
                          (wCam-frameR, hCam-frameR), (255, 0, 255), 2)
            # 座標計算
            x, y = lmlist[8][1]-frameR, lmlist[8][2]-frameR
            x, y = int(x/(wCam-(frameR*2))*wWin), int(y/(hCam-(frameR*2))*hWin)
            cv2.circle(img2, (lmlist[8][1], lmlist[8][2]),
                       10, (255, 0, 0), cv2.FILLED)
            # 移動
            # print("\rX: "+str(x)+" Y: "+str(y), end="")
            # 画面内なら動かして　それ以外なら動かさない
            if 0 <= x < wWin and 0 <= y < hWin:
                pyautogui.moveTo(x, y)

        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400),
                      (0, 255, 0), cv2.FILLED)

    # UI関係
    if volumeCounter < 60 and volumeFlag:
        volumeCounter += 1
        cv2.putText(img2, "changed >> Volume ON", (20, 20),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (155, 155, 155), 1)

    if mouseCounter < 60 and mouseFlag:
        mouseCounter += 1
        cv2.putText(img2, "changed >> Mouse ON", (20, 20),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (155, 155, 155), 1)

    if allOffCounter < 60 and (mouseFlag is False or volumeFlag is False):
        allOffCounter += 1
        cv2.putText(img2, "changed >> ALL OFF", (20, 20),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (155, 155, 155), 1)

    cv2.putText(img, f'{int(volPar)} %', (40, 450),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    # FPS表示設定
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    # 画像の表示
    cv2.imshow("Image", img)
    cv2.imshow("Point", img2)

    # 入力待ち 1F
    k = cv2.waitKey(1)
    # 入力がEscの場合閉じる
    if k == 27:
        sys.exit()

    frame += 1
