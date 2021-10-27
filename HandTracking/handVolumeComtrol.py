import cv2
import time
import numpy as np
import math
import sys
import itertools
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from module import cv2_putText_4
# from HandFrickinput import FlickInput
import pyautogui
import mouse
import handtrackingModule as htm

# 基本設定
# ウィンドウの大きさの設定@
wCam, hCam = 1000, 800
frameR = 100


# ディスプレイの大きさの測定
(wWin, hWin) = pyautogui.size()
print("横：{0} 縦：{1}".format(wWin, hWin))

# 動画関係設定
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
cap.set(3, wCam)
cap.set(4, hCam)
# cap.set(cv2.CAP_PROP_FPS, 60)
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
detector = htm.handDetectior(MaxHands=2, detectonCon=0.7)

# 音量関係設定
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPar = 0

# 操作関連
volumeFlag = False
volumeCounter = 0
volumeConfirmFrag = False
mouseFlag = False
mouseCounter = 0
clickCounter = 0
dragFlag = False
INPUT_TEXTS = ""
textinputFlag = False
allOffCounter = 0
frame = 0
f = 0
hand = 0
wframe=0


# fontPath = "C:\Windows\Fonts\CENTAUR.TTF"  # Centaur 標準
# fontPath = "C:\Windows\Fonts\HGRME.TTC"  # HGP明朝　標準
font_Path = "C:\Windows\Fonts\HGRGM.TTC"

textlist = ["あ"]

print("ポインタの位置")
# 本動作
while True:
    # 画像の読み込み
    success, img = cap.read()
    img2 = np.full((hCam, wCam, 3), 255, dtype=np.uint8)
    img = cv2.flip(img, 1)

    # 手を認識させる
    img = detector.findHands(img, drawLandmark=False)
    # detectorから 手位置lmlist 手の大きさbbox 手の本数handを取得する
    lmlist, bbox, hand = detector.findPosition(img, drawPosition=False, Normalization=True)

    conformText = ""
    textren = 0
    hand+=1
    # if 手が認識した
    # 認識したら
    # ・ボリューム操作
    # ・マウス操作
    # ・文字入力操作
    # をする

    if len(lmlist) != 0:
        # print(lmlist)
        # print(bbox)
        # 指の根元の座標listxを取得
        for box in bbox:
            Xmax, Ymax = box[2], box[3]
            Xmin, Ymin = box[0], box[1]
            cv2.rectangle(img2, (Xmin, Ymin), (Xmax, Ymax), 2)

        cv2.circle(img, (lmlist[0][0][1], lmlist[0][0][2]), 5, (0, 0, 255), cv2.FILLED)
        # 指をおろしている判定を取得
        checkedList = detector.checkFinger()
        # print(checkedList)　#確認

        # ***フラグ処理***
        # ・volumeFlag：ボリューム操作をするフラグ
        # ・mouseFlag：マウス操作をするフラグ
        # ・textinputFlag；テキスト入力をするフラグ
        # ・

        # 親指と人差し指を上げるとボリューム操作がON
        if (volumeFlag or mouseFlag or textinputFlag) is False and checkedList[0] == [1, 1, 0, 0, 0]:
            volumeFlag = True
            volumeConfirmFrag = False
            volumeCounter = 30

        # ボリューム操作がONのとき、親指と人差し指、小指を上げるとボリュームが確定する
        elif volumeFlag and checkedList[0] == [1, 1, 0, 0, 1]:
            volumeConfirmFrag = True
            volumeFlag = False

        # 人差し指と中指を上げるとマウス動作を開始
        elif (volumeFlag or mouseFlag or textinputFlag) is False and checkedList[0] == [0, 1, 1, 0, 0]:
            mouseFlag = True
            if mouseCounter==0:
                mouseCounter = 30

        # マウス動作時に親指を上げるとクリック動作
        if mouseFlag and checkedList[0][0]:
            # print('\r'+str(dl))
            if clickCounter == 0:
                conformText += "ClickLeft!!\n"
                textren += 1
                clickCounter = 20
                mouse.click("left")

        # 両手を上げると文字入力モードに
        if textinputFlag is False and checkedList == [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]:
            conformText += "Textinput\n"
            textren += 1
            textinputFlag = True
            INPUT_TEXTS = ""
        # 両手から片手にすると入力モード停止
        if hand != 2:
            textinputFlag = False

        # 小指だけを上げているとボリューム操作がOFF マウス動作もOFF
        # 音量を確定する
        if (volumeFlag or mouseFlag or textinputFlag) and checkedList[0] == [0, 0, 0, 0, 1]:
            volumeFlag = False
            mouseFlag = False
            textinputFlag = False
            allOffCounter = 30

        # 手の長さの範囲 50-300
        # volume range -65-0

        # 音量調節Flag
        if volumeFlag:
            # x4 y4: 親指の先端の座標を取得
            # x8 y8: 人差し指の先端の座標を取得
            # cx cy: 親指と人差指の先端の中点
            # length:親指と人差指の先端の長さ
            x4, y4 = lmlist[0][4][1], lmlist[0][4][2]
            x8, y8 = lmlist[0][8][1], lmlist[0][8][2]
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
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
            cv2.rectangle(img2, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
            # 座標計算
            x, y = lmlist[0][12][1] - frameR, lmlist[0][12][2] - frameR
            x, y = (int(x / (wCam - (frameR * 2)) * wWin),int(y / (hCam - (frameR * 2)) * hWin),)
            cv2.circle(img2, (lmlist[0][12][1], lmlist[0][12][2]), 10, (255, 0, 0), cv2.FILLED,)
            # 移動
            # print("\rX: "+str(x)+" Y: "+str(y), end="")
            # 画面内なら動かして　それ以外なら動かさない
            if 0 <= x < wWin and 0 <= y < hWin:
                # pyautogui.moveTo(x, y)
                mouse.move(x, y)
    # TODO:
    # 数字入力操作Flag (両手限定)
        if textinputFlag and hand==2:
            # 文字確定Flag (片手を握ったら)
            if checkedList[1] == [0, 0, 0, 0, 0] and wframe==0:
                print(*checkedList)
                if checkedList[0] == [0, 0, 0, 0, 0]:
                    INPUT_TEXTS+="0"
                elif checkedList[0] == [1, 0, 0, 0, 0]:
                    INPUT_TEXTS+="1"
                elif checkedList[0] == [0, 1, 0, 0, 0]:
                    INPUT_TEXTS+="2"
                elif checkedList[0] == [1, 1, 0, 0, 0]:
                    INPUT_TEXTS+="3"
                elif checkedList[0] == [0, 0, 1, 0, 0]:
                    INPUT_TEXTS+="4"
                elif checkedList[0] == [1, 0, 1, 0, 0]:
                    INPUT_TEXTS+="5"
                elif checkedList[0] == [0, 1, 1, 0, 0]:
                    INPUT_TEXTS+="6"
                elif checkedList[0] == [1, 1, 1, 0, 0]:
                    INPUT_TEXTS+="7"
                elif checkedList[0] == [0, 0, 0, 1, 0]:
                    INPUT_TEXTS+="8"
                elif checkedList[0] == [1, 0, 0, 1, 0]:
                    INPUT_TEXTS+="9"
                elif checkedList[0] == [1, 1, 1, 1, 1]:
                    pyautogui.typewrite(INPUT_TEXTS)
                else:
                    print("NO_INPUT")
                wframe=10
            print(INPUT_TEXTS)

        # # 入力確定動作-->左親指を閉じる
        # if checkedList[0][0] == 0:
        #     pyautogui.write(INPUT_TEXTS)

        #フリック入力動作

    # 文字関係
    if 0 < volumeCounter and volumeFlag:
        volumeCounter -= 1
        conformText += "Changed >> Volume ON {0}\n".format(volumeCounter)
        textren += 1

    if 0 < mouseCounter and mouseFlag:
        mouseCounter -= 1
        conformText += "Changed >> Mouse ON {0}\n".format(mouseCounter)
        textren += 1

    if 0 < allOffCounter and (mouseFlag is False or volumeFlag is False):
        allOffCounter -= 1
        conformText += "Changed >> ALL OFF {0}\n".format(allOffCounter)
        textren += 1

    if textinputFlag:
        conformText += "INPUTTEXT:{0}\n".format(INPUT_TEXTS)

    if volumeFlag:
        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)

    # print(conformText)
    cv2_putText_4(img2, conformText, (1, 50 * textren), font_Path, 10, (255, 0, 0))

    cv2.putText(img, f"{int(volPar)} %", (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    wframe=max(0,wframe-1)

    # FPS表示設定
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    # 画像の表示
    cv2.imshow("Image", img)
    cv2.imshow("Point", img2)

    # 入力待ち 1F
    k = cv2.waitKey(1)
    # 入力がEscの場合閉じる
    if k == 27:
        sys.exit()
