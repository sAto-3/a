# フリック入力をpyautoguiの入力機能
# Windowsの変換機能を使って入力する


# coding: UTF-8
from ctypes.wintypes import INT
import itertools
import math
import sys
import time
from ctypes import POINTER, cast

import cv2
import mouse
import numpy as np
import pyautogui
import pykakasi
import pyperclip
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import handtrackingModule as htm
from module import cv2_putText_4, cv2_putText_5

# 基本設定
# ウィンドウの大きさの設定
wCam, hCam = 1000, 700
spaceH = 300
spaceW = 150
wVisal = wCam-spaceW
hVisal = hCam-spaceH


# ディスプレイの大きさの測定
(wWin, hWin) = pyautogui.size()
print("横：{0} 縦：{1}".format(wWin, hWin))

# 動画関係設定
# cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) #DshowにするとFPS12程度に落ちてしまう
cap = cv2.VideoCapture(0, cv2.CAP_MSMF)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # カメラ画像の横幅を1280に設定
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)  # カメラ画像の縦幅を720に設定
# cap.set(cv2.CAP_PROP_FPS, 60)
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
detector = htm.handDetectior(MaxHands=2, detectonCon=0.7)

# 操作関連
INPUT_TEXTS = ""
INPUT_TEXTS_UI = ""
frame = 0
f = 0
hand = 0
wframe = 0

KEYBOARDLIST = np.full((5, 5), False).tolist()
KEYBOARDREMEN = True
xx, yy = 0, 0
INPUT_FLAG = False
frick_Flag = True
font_size = 50
#
KEYBOARD_HIRA = [
    [[" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], ["delete", "×", " ", " ", " "]],
    [["カナ", " ", " ", " ", " "], ["あ", "い", "う", "え", "お"], ["か", "き", "く", "け", "こ"], ["さ", "し", "す", "せ", "そ"], ["BS", " ", " ", " ", " "]],
    [["英", " ", " ", " ", " "], ["た", "ち", "つ", "て", "と"], ["な", "に", "ぬ", "ね", "の"], ["は", "ひ", "ふ", "へ", "ほ"], ["変換", " ", " ", " ", " "], ],
    [["012", " ", " ", " ", " "], ["ま", "み", "む", "め", "も"], ["や", "「", "ゆ", "」", "よ"], ["ら", "り", "る", "れ", "ろ"], ["space", " ", " ", " ", " "], ],
    [["Quit", " ", " ", " ", " "], ["ー", " ", " ", " ", " "],  ["わ", "を", "ん", " ", " "],  ["゛", " ", " ", " ", " "], ["Input", "Enter", " ", " ", " "]], ]
KEYBOARD_HIRA_1 = [
    [[" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], ["delete", "×", " ", " ", " "]],
    [["カナ", " ", " ", " ", " "], ["ぁ", "ぃ", "ぅ", "ぇ", "ぉ"], ["が", "ぎ", "ぐ", "げ", "ご"], ["ざ", "じ", "ず", "ぜ", "ぞ"], ["BS", " ", " ", " ", " "]],
    [["英", " ", " ", " ", " "], ["だ", "ぢ", "づ", "で", "ど"], [" ", " ", " ", " ", " "], ["ば", "び", "ぶ", "べ", "ぼ"], ["変換", " ", " ", " ", " "], ],
    [["012", " ", " ", " ", " "], ["ぱ", "ぴ", "ぷ", "ぺ", "ぽ"], ["ゃ", " ", "ゅ", " ", "ょ"], [" ", " ", " ", " ", " "], ["space", " ", " ", " ", " "], ],
    [["Quit", " ", " ", " ", " "], ["ー", " ", " ", " ", " "],  [" ", " ", " ", " ", " "],  ["゛", " ", " ", " ", " "], ["Input", "Enter", " ", " ", " "]], ]
KEYBOARD_KATA = [
    [[" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], ["delete", "×", " ", " ", " "]],
    [["かな", " ", " ", " ", " "], ["ア", "イ", "ウ", "エ", "オ"], ["カ", "キ", "ク", "ケ", "コ"], ["サ", "シ", "ス", "セ", "ソ"], ["BS", " ", " ", " ", " "]],
    [["英", " ", " ", " ", " "], ["タ", "チ", "ツ", "テ", "ト"], ["ナ", "二", "ヌ", "ネ", "ノ"], ["ハ", "ヒ", "フ", "へ", "ホ"], ["変換", " ", " ", " ", " "], ],
    [["012", " ", " ", " ", " "], ["マ", "ミ", "ム", "メ", "モ"], ["ヤ", "「", "ユ", "」", "ヨ"], ["ラ", "リ", "ル", "レ", "ロ"], ["space", " ", " ", " ", " "], ],
    [["Quit", " ", " ", " ", " "], ["ー", " ", " ", " ", " "], ["ワ", "ヲ", "ン", " ", " "], ["゛", " ", " ", " ", " "], ["Input", "Enter", " ", " ", " "]], ]
KEYBOARD_KATA_1 = [
    [[" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], ["delete", "×", " ", " ", " "]],
    [["かな", " ", " ", " ", " "], ["ァ", "ィ", "ゥ", "ェ", "ォ"], ["ガ", "ギ", "グ", "ゲ", "ゴ"], ["ザ", "ジ", "ズ", "ゼ", "ゾ"], ["BS", " ", " ", " ", " "]],
    [["英", " ", " ", " ", " "], ["ダ", "ヂ", "ズ", "デ", "ド"], [" ", " ", " ", " ", " "], ["バ", "ビ", "ブ", "ベ", "ボ"], ["変換", " ", " ", " ", " "], ],
    [["012", " ", " ", " ", " "], ["パ", "ピ", "プ", "ペ", "ポ"], ["ャ", " ", "ュ", " ", "ョ"], [" ", " ", " ", " ", " "], ["space", " ", " ", " ", " "], ],
    [["Quit", " ", " ", " ", " "], ["ー", " ", " ", " ", " "], [" ", " ", " ", " ", " "], ["゛", " ", " ", " ", " "], ["Input", "Enter", " ", " ", " "]], ]
KEYBOARD_ENGLISH_SM = [
    [[" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], ["delete", "×", " ", " ", " "]],
    [["A/a", " ", " ", " ", " "], ["a", "b", "c", " ", " "], ["d", "e", "f", " ", " "], ["g", "h", "i", " ", " "], ["BS", " ", " ", " ", " "]],
    [["かな", " ", " ", " ", " "], ["j", "k", "l", " ", " "], ["m", "n", "o", " ", " "], ["p", "q", "r", "s", " "], [" ", " ", " ", " ", " "], ],
    [["012", " ", " ", " ", " "], ["t", "u", "v", " ", " "], ["w", "x", "y", "z", " "], [" ", " ", " ", " ", " "], ["space", " ", " ", " ", " "], ],
    [["Quit", " ", " ", " ", " "], ["-", "_", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], ["Input", "Enter", " ", " ", " "]], ]
KEYBOARD_ENGLISH_BI = [
    [[" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], ["delete", "×", " ", " ", " "]],
    [["A/a", " ", " ", " ", " "], ["A", "B", "C", " ", " "], ["D", "E", "F", " ", " "], ["G", "H", "I", " ", " "], [" ", " ", " ", " ", " "]],
    [["かな", " ", " ", " ", " "], ["J", "K", "L", " ", " "], ["M", "N", "O", " ", " "], ["P", "Q", "R", "S", " "], [" ", " ", " ", " ", " "], ],
    [["012", " ", " ", " ", " "], ["T", "U", "V", " ", " "], ["W", "X", "Y", "Z", " "], [" ", " ", " ", " ", " "], ["space", " ", " ", " ", " "], ],
    [["Quit", " ", " ", " ", " "], [" ", " ", " ", " ", " "],  [" ", " ", " ", " ", " "],  [" ", " ", " ", " ", " "], ["Input", "Enter", " ", " ", " "]], ]
KEYBOARD_NUMPER = [
    [[" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], ["delete", "×", " ", " ", " "]],
    [["かな", " ", " ", " ", " "], ["1", " ", " ", " ", " "], ["2", " ", " ", " ", " "], ["3", " ", " ", " ", " "], ["BS", " ", " ", " ", " "]],
    [["英", " ", " ", " ", " "], ["4", " ", " ", " ", " "], ["5", " ", " ", " ", " "], ["6", " ", " ", " ", " "], ["変換", " ", " ", " ", " "], ],
    [["", " ", " ", " ", " "], ["7", " ", " ", " ", " "], ["8", " ", " ", " ", " "], ["9", " ", " ", " ", " "], ["space", " ", " ", " ", " "], ],
    [["Quit", " ", " ", " ", " "], ["ー", " ", " ", " ", " "], ["0", " ", " ", " ", " "], ["゛", " ", " ", " ", " "], ["Input", "Enter", " ", " ", " "]], ]
kakasi = pykakasi.kakasi()

KEYBOARD = KEYBOARD_HIRA
# KEYBOARDLIST=[False]*11
# KEYBOARDLIST[10]=True

# fontPath = "C:\Windows\Fonts\CENTAUR.TTF"  # Centaur 標準
# fontPath = "C:\Windows\Fonts\HGRME.TTC"  # HGP明朝　標準
font_Path = "C:\Windows\Fonts\HGRGM.TTC"
# fontPath = "C: \Windows\Fonts\msmincho.ttc"
# font_Path = "C:\Windows\Fonts\Yu Gothic UI\YuGothL.ttc" #游ゴシックL
# font_Path = "C:\Windows\Fonts\メイリオ\meiryo.ttc" #メイリオ


# print("ポインタの位置")
# 本動作
while True:
    # 画像の読み込み
    success, img = cap.read()
    # img=cv2.resize(img,dsize=(wCam,hCam))
    img2 = np.full((hCam, wCam, 3), 255, dtype=np.uint8)
    img = cv2.flip(img, 1)

    # 手を認識させる
    img = detector.findHands(img, drawLandmark=False)
    # detectorから 手位置lmlist 手の大きさbbox 手の本数handを取得する
    lmlist, bbox, hand = detector.findPosition(img, drawPosition=False, Normalization=True)
    hand += 1
    conformText = ""
    textren = 0

    # if 手が認識した
    # 認識したら
    # ・ボリューム操作
    # ・マウス操作
    # ・文字入力操作
    # をする

    if len(lmlist) != 0:
        # 指をおろしている判定を取得
        checkedList = detector.checkFinger()
        # フリック入力
        # KEYBOARDLIST
        # KEYBOARDは初期位置+50音の位置
        # 実行
        # 親指を伸ばしたら選択状態になる
        if not frick_Flag:
            cv2_putText_5(img2, "手を読み込んでください", (wCam//2, hCam//2), font_Path, 1, (255, 0, 0))
        else:
            if hand == 2:
                if checkedList[1] == [1, 1, 1, 1, 1]:
                    # 最初は位置を記憶して判別する
                    if KEYBOARDREMEN:
                        # if KEYBOSRDLIST[10]:
                        frick_x1, frick_y1 = lmlist[0][8][1], lmlist[0][8][2]
                        # 縦から
                        for ix in range(5):
                            for iy in range(5):
                                if ix * wVisal / 5 + spaceW <= frick_x1 < (ix + 1) * wVisal / 5 + spaceW and iy * hVisal / 5 <= frick_y1 < (iy + 1) * hVisal / 5:
                                    KEYBOARDLIST[ix][iy] = True
                                    xx, yy = ix, iy
                                    # print(ix,iy)
                        KEYBOARDREMEN = False
                        INPUT_FLAG = True
                # 親指を戻したら選択を確定してして初期化
                else:
                    if INPUT_FLAG:
                        # 選択を確定して文字列に出力
                        frick_now_x, frick_now_y = lmlist[0][8][1], lmlist[0][8][2]
                        text = ""
                        # 特別例
                        # space
                        if 4 * wVisal / 5 + spaceW <= frick_now_x < 5 * wVisal / 5 + spaceW and 3 * hVisal / 5 <= frick_now_y < 4 * hVisal / 5:
                            text = "　"  # 全角空白
                        # enter
                        # Quit
                        for ix in range(5):
                            for iy in range(5):
                                if ix * wVisal / 5 + spaceW <= frick_now_x < (ix + 1) * wVisal / 5 + spaceW and iy * hVisal / 5 <= frick_now_y < (iy + 1) * hVisal / 5:
                                    if ix == xx and iy == yy:
                                        # あ行
                                        text = KEYBOARD[yy][xx][0]
                                    elif ix + 1 == xx and iy == yy:
                                        # い行
                                        text = KEYBOARD[yy][xx][1]
                                    elif ix == xx and iy + 1 == yy:
                                        # う行
                                        text = KEYBOARD[yy][xx][2]
                                    elif ix - 1 == xx and iy == yy:
                                        # え行
                                        text = KEYBOARD[yy][xx][3]
                                    elif ix == xx and iy - 1 == yy:
                                        # お行
                                        text = KEYBOARD[yy][xx][4]
                                    break
                            else:
                                continue
                            break
                        if text != " ":
                            INPUT_TEXTS += text
                            INPUT_TEXTS_UI += text
                        if text == "ん" or text == "ン":
                            INPUT_TEXTS += "'"
                        elif text == "delete":
                            INPUT_TEXTS = INPUT_TEXTS[:-6]
                            INPUT_TEXTS_UI = INPUT_TEXTS_UI[:-6]
                            if INPUT_TEXTS:
                                INPUT_TEXTS = INPUT_TEXTS[:-1]
                                INPUT_TEXTS_UI = INPUT_TEXTS_UI[:-1]
                        elif text == "space":
                            INPUT_TEXTS = INPUT_TEXTS[:-5]
                            INPUT_TEXTS_UI = INPUT_TEXTS_UI[-5]
                            INPUT_TEXTS += "　"
                            INPUT_TEXTS_UI += "　"
                        elif text == "Enter":
                            INPUT_TEXTS = INPUT_TEXTS[:-5]
                            INPUT_TEXTS_UI = INPUT_TEXTS_UI[:-5]
                            pyautogui.press("Enter")
                        elif text == "Input":
                            INPUT_TEXTS = INPUT_TEXTS[:-5]
                            INPUT_TEXTS_UI = INPUT_TEXTS_UI[:-5]
                            # 文字を日本語文字からローマ字変換してから該当する文字を入力
                            romaji = kakasi.convert(INPUT_TEXTS)
                            # print(romaji)
                            for bun in romaji:
                                # print(bun["kunrei"])
                                for key in bun["kunrei"]:
                                    print(key)
                                    pyautogui.press(key)
                            INPUT_TEXTS = ""
                            INPUT_TEXTS_UI = ""
                        elif text == "×":
                            INPUT_TEXTS = ""
                            INPUT_TEXTS_UI = ""
                        elif text == "BS":
                            INPUT_TEXTS = INPUT_TEXTS[:-2]
                            INPUT_TEXTS_UI = ""
                            pyautogui.press("backspace")
                        # if text=="enter":
                        #     INPUT_TEXTS="\n"
                        elif text == "Quit":
                            sys.exit()
                        elif text == "゛":
                            INPUT_TEXTS = INPUT_TEXTS[:-1]
                            INPUT_TEXTS_UI = INPUT_TEXTS_UI[:-1]
                            # キーボード切り替え処理
                            if KEYBOARD == KEYBOARD_HIRA_1:
                                KEYBOARD = KEYBOARD_HIRA
                            elif KEYBOARD == KEYBOARD_HIRA:
                                KEYBOARD = KEYBOARD_HIRA_1
                            elif KEYBOARD == KEYBOARD_KATA:
                                KEYBOARD = KEYBOARD_KATA_1
                            elif KEYBOARD == KEYBOARD_KATA_1:
                                KEYBOARD = KEYBOARD_KATA
                        elif text == "かな":
                            INPUT_TEXTS = INPUT_TEXTS[:-2]
                            INPUT_TEXTS_UI = INPUT_TEXTS_UI[:-2]
                            KEYBOARD = KEYBOARD_HIRA
                            pyautogui.press("kana")
                        elif text == "カナ":
                            INPUT_TEXTS = INPUT_TEXTS[:-2]
                            INPUT_TEXTS_UI = INPUT_TEXTS_UI[:-2]
                            KEYBOARD = KEYBOARD_KATA
                        elif text == "英":
                            INPUT_TEXTS = INPUT_TEXTS[:-1]
                            INPUT_TEXTS_UI = INPUT_TEXTS_UI[:-1]
                            KEYBOARD = KEYBOARD_ENGLISH_SM
                        elif text == "A/a":
                            INPUT_TEXTS = INPUT_TEXTS[:-3]
                            INPUT_TEXTS_UI = INPUT_TEXTS_UI[:-3]
                            if KEYBOARD == KEYBOARD_ENGLISH_BI:
                                KEYBOARD = KEYBOARD_ENGLISH_SM
                            else:
                                KEYBOARD = KEYBOARD_ENGLISH_BI
                            pyautogui.press("kana")
                        elif text == "012":
                            INPUT_TEXTS = INPUT_TEXTS[:-3]
                            INPUT_TEXTS_UI = INPUT_TEXTS_UI[:-3]
                            KEYBOARD = KEYBOARD_NUMPER
                        elif text == "変換":
                            INPUT_TEXTS = INPUT_TEXTS[:-2]
                            INPUT_TEXTS_UI = INPUT_TEXTS_UI[:-2]
                            pyautogui.press("space")

                        print(INPUT_TEXTS)

                    # 初期化
                    KEYBOARDLIST = np.full((5, 5), False).tolist()
                    KEYBOARDREMEN = True
                    INPUT_FLAG = False
                # print(KEYBOARDLIST)

        # UI生成
        # 線
        for i in range(6):
            cv2.line(img2, (i * wVisal // 5+spaceW, 0), (i * wVisal // 5 + spaceW, hVisal), (255, 0, 0), 1)
            cv2.line(img2, (spaceW, i * hVisal // 5), (wVisal + spaceW, i * hVisal // 5), (255, 0, 0), 1)

        # 選択時の背景色 #FF6666
        for id_x in range(5):
            for id_y in range(5):
                if KEYBOARDLIST[id_x][id_y]:
                    cv2.rectangle(img2, (id_x * wVisal // 5 + spaceW, id_y * hVisal // 5), ((id_x + 1) * wVisal // 5 + spaceW, (id_y + 1) * hVisal // 5), (102, 102, 255), thickness=-1)

        # 文字 #9999FF
        for id_x in range(1, 5):
            for id_y in range(1, 5):
                if KEYBOARDLIST[id_x][id_y]:
                    cv2_putText_5(img2, KEYBOARD[id_y][id_x][0], ((2*id_x+1)*wVisal//10+spaceW, (2*id_y+1)*hVisal//10), font_Path, font_size, (255, 99, 99))
                    cv2_putText_5(img2, KEYBOARD[id_y][id_x][1], ((2*id_x-1)*wVisal//10+spaceW, (2*id_y+1)*hVisal//10), font_Path, font_size, (255, 99, 99))
                    cv2_putText_5(img2, KEYBOARD[id_y][id_x][2], ((2*id_x+1)*wVisal//10+spaceW, (2*id_y-1)*hVisal//10), font_Path, font_size, (255, 99, 99))
                    cv2_putText_5(img2, KEYBOARD[id_y][id_x][3], ((2*id_x+3)*wVisal//10+spaceW, (2*id_y+1)*hVisal//10), font_Path, font_size, (255, 99, 99))
                    cv2_putText_5(img2, KEYBOARD[id_y][id_x][4], ((2*id_x+1)*wVisal//10+spaceW, (2*id_y+3)*hVisal//10), font_Path, font_size, (255, 99, 99))
        if KEYBOARDREMEN:
            for i in range(5):
                for j in range(5):
                    cv2_putText_5(img2, KEYBOARD[i][j][0], ((2*j+1)*wVisal//10+spaceW, (2*i+1)*hVisal//10), font_Path, font_size, (255, 99, 99))
                # print(KEYBOARD[i][j][0],(2*j+1)*wVisal//10,(2*i+1)*hVisal//10)
                # cv2.circle(img2,((2*j+1)*wVisal//10,(2*i+1)*hVisal//10),5,(255,99,99),cv2.FILLED)
        cv2.rectangle(img2, (10, 10+hCam-spaceH), (wCam-10, hCam-10), (102, 102, 255), 3)
        if INPUT_TEXTS_UI:
            cv2_putText_5(img2, INPUT_TEXTS_UI, (wCam//2, hCam - spaceH//2), font_Path, font_size, (255, 99, 99))

            # ポインタ処理
        for i in range(hand):
            if lmlist[i][0][4]:
                cv2.circle(img, (lmlist[i][0][1], lmlist[i][0][2]), 3, (0, 0, 255), cv2.FILLED)
            else:
                cv2.circle(img, (lmlist[i][0][1], lmlist[i][0][2]), 3, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (int(lmlist[0][8][1]), int(lmlist[0][8][2])), 3, (0, 0, 255), cv2.FILLED)
            cv2.circle(img2, (int(lmlist[0][8][1]), int(lmlist[0][8][2])), 4, (0, 0, 0), cv2.FILLED)
        if hand == 2:
            if checkedList[1] == [1, 1, 1, 1, 1]:
                cv2.circle(img2, (int(lmlist[0][8][1]), int(lmlist[0][8][2])), 3, (0, 0, 255), cv2.FILLED)
            else:
                cv2.circle(img2, (int(lmlist[0][8][1]), int(lmlist[0][8][2])), 3, (0, 255, 0), cv2.FILLED)
    # if volumeFlag:
    #     cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    #     cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)

    # print(conformText)
    cv2_putText_4(img2, conformText, (1, 50 * textren), font_Path, 10, (255, 0, 0))

    # cv2.putText(
    #     img, f"{int(volPar)} %", (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3
    # )

    # FPS表示設定
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # cv2.putText(img, f"FPS: {int(fps)}", (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cv2.putText(img2, r"{0}".format(int(fps)), (10, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)
    wframe = max(0, wframe - 1)
    frame += 1
    # 画像の表示
    # cv2.imshow("Image", img)
    cv2.imshow("Point", img2)

    # 入力待ち 1F
    k = cv2.waitKey(1)
    # 入力がEscの場合閉じる
    if k == 27:
        sys.exit()
