import cv2
import time
import numpy as np
import math
import sys
import itertools
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from module import cv2_putText_4,cv2_putText_5
import pyautogui
import mouse
import handtrackingModule as htm

# 基本設定
# ウィンドウの大きさの設定
wCam, hCam = 1000,800
frameR = 300
wVisal=wCam
hVisal=hCam-frameR


# ディスプレイの大きさの測定
(wWin, hWin) = pyautogui.size()
print("横：{0} 縦：{1}".format(wWin, hWin))

# 動画関係設定
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # カメラ画像の横幅を1280に設定
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 900) # カメラ画像の縦幅を720に設定
# cap.set(cv2.CAP_PROP_FPS, 60)
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
detector = htm.handDetectior(MaxHands=2, detectonCon=0.7)

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
wframe = 0

KEYBOARDLIST=np.full((5,5),False).tolist()
KEYBOARDREMEN=True
xx,yy=0,0
INPUT_FLAG=False
KEYBOARD_HIRA = [
    [[" "," "," "," "," "],[" "," "," "," "," "],     [" "," "," "," "," "],    [" "," "," "," "," "],    ["delete"," "," "," "," "]],
    [["カナ"," "," "," "," "],["あ","い","う","え","お"], ["か","き","く","け","こ"],["さ","し","す","せ","そ"],[" "," "," "," "," "]],
    [["英"," "," "," "," "],["た","ち","つ","て","と"], ["な","に","ぬ","ね","の"],["は","ひ","ふ","へ","ほ"],[" "," "," "," "," "],],
    [[" "," "," "," "," "],["ま","み","む","め","も"], ["や","「","ゆ","」","よ"],["ら","り","る","れ","ろ"],["space"," "," "," "," "],],
    [["Quit"," "," "," "," "],[" "," "," "," "," "],  ["わ","を","ん"," "," "],  [" "," "," "," "," "],    ["Enter"," "," "," "," "]],
]
KEYBOARD_KATA = [
    [[" "," "," "," "," "],[" "," "," "," "," "],     [" "," "," "," "," "],    [" "," "," "," "," "],    ["delete"," "," "," "," "]],
    [["かな"," "," "," "," "],["ア","イ","ウ","エ","オ"], ["カ","キ","ク","ケ","コ"],["サ","シ","ス","セ","ソ"],[" "," "," "," "," "]],
    [["英"," "," "," "," "],["タ","チ","ツ","テ","ト"], ["ナ","二","ヌ","ネ","ノ"],["ハ","ヒ","フ","へ","ホ"],[" "," "," "," "," "],],
    [[" "," "," "," "," "],["マ","ミ","ム","メ","モ"], ["ヤ","「","ユ","」","ヨ"],["ラ","リ","ル","レ","ロ"],["space"," "," "," "," "],],
    [["Quit"," "," "," "," "],[" "," "," "," "," "],  ["ワ","ヲ","ン"," "," "],  [" "," "," "," "," "],    ["Enter"," "," "," "," "]],
]
KEYBOARD_ENGLISH_SM=[
    [[" "," "," "," "," "],[" "," "," "," "," "],     [" "," "," "," "," "],    [" "," "," "," "," "],    ["delete"," "," "," "," "]],
    [["a/A"," "," "," "," "],["a","b","c","d"," "], ["e","f","g","h"," "],["i","j","k","l"," "],[" "," "," "," "," "]],
    [["かな"," "," "," "," "],["m","n","o","p"," "], ["q","r","s","t"," "],["u","v","w","x"," "],[" "," "," "," "," "],],
    [[" "," "," "," "," "],["y","z"," "," "," "], [" "," "," "," "," "],[" "," "," "," "," "],["space"," "," "," "," "],],
    [["Quit"," "," "," "," "],[" "," "," "," "," "],  [" "," "," "," "," "],  [" "," "," "," "," "],    ["Enter"," "," "," "," "]],
]
KEYBOARD_ENGLISH_BI=[
    [[" "," "," "," "," "],[" "," "," "," "," "],     [" "," "," "," "," "],    [" "," "," "," "," "],    ["delete"," "," "," "," "]],
    [["A/a"," "," "," "," "],["A","B","C","D"," "], ["E","F","G","H"," "],["I","J","K","L"," "],[" "," "," "," "," "]],
    [["かな"," "," "," "," "],["M","N","O","P"," "], ["Q","R","S","T"," "],["U","V","W","X"," "],[" "," "," "," "," "],],
    [[" "," "," "," "," "],["Y","Z"," "," "," "], [" "," "," ","  "," "],[" "," "," "," "," "],["space"," "," "," "," "],],
    [["Quit"," "," "," "," "],[" "," "," "," "," "],  [" "," "," "," "," "],  [" "," "," "," "," "],    ["Enter"," "," "," "," "]],
]
KEYBOARD=KEYBOARD_HIRA
# KEYBOARDLIST=[False]*11
# KEYBOARDLIST[10]=True

# fontPath = "C:\Windows\Fonts\CENTAUR.TTF"  # Centaur 標準
# fontPath = "C:\Windows\Fonts\HGRME.TTC"  # HGP明朝　標準
font_Path = "C:\Windows\Fonts\HGRGM.TTC"

textlist = ["あ"]

print("ポインタの位置")
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
        # print(lmlist)
        # print(bbox)
        # 指の根元の座標listxを取得
        for box in bbox:
            Xmax, Ymax = box[2], box[3]
            Xmin, Ymin = box[0], box[1]
            # cv2.rectangle(img2, (Xmin, Ymin), (Xmax, Ymax), 2)

        cv2.circle(img, (lmlist[0][0][1], lmlist[0][0][2]), 5, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (int(lmlist[0][8][1]), int(lmlist[0][8][2])), 5, (0, 0, 255), cv2.FILLED)
        cv2.circle(img2, (int(lmlist[0][8][1]), int(lmlist[0][8][2])), 5, (0, 0, 255), cv2.FILLED)
        # 指をおろしている判定を取得
        checkedList = detector.checkFinger()
        # print(checkedList)　#確認

        # ***フラグ処理***
        # ・volumeFlag：ボリューム操作をするフラグ
        # ・mouseFlag：マウス操作をするフラグ
        # ・textinputFlag；テキスト入力をするフラグ
        # ・

        # # 親指と人差し指を上げるとボリューム操作がON
        # if (volumeFlag and mouseFlag and textinputFlag) is False and checkedList[0] == [1, 1, 0, 0, 0]:
        #     volumeFlag = True
        #     volumeConfirmFrag = False
        #     volumeCounter = 30

        # # ボリューム操作がONのとき、親指と人差し指、小指を上げるとボリュームが確定する
        # elif volumeFlag and checkedList[0] == [1, 1, 0, 0, 1]:
        #     volumeConfirmFrag = True
        #     volumeFlag = False

        # # 人差し指と中指を上げるとマウス動作を開始
        # elif (volumeFlag or mouseFlag or textinputFlag) is False and checkedList[0] == [0, 1, 1, 0, 0]:
        #     mouseFlag = True
        #     if mouseCounter==0:
        #         mouseCounter = 30

        # # マウス動作時に親指を上げるとクリック動作
        # if mouseFlag and checkedList[0][0]:
        #     # print('\r'+str(dl))
        #     if clickCounter == 0:
        #         conformText += "ClickLeft!!\n"
        #         textren += 1
        #         clickCounter = 20
        #         mouse.click("left")

        # # 両手を上げると文字入力モードに
        # if textinputFlag is False and checkedList == [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]:
        #     conformText += "Textinput\n"
        #     textren += 1
        #     textinputFlag = True
        #     INPUT_TEXTS = ""
        # # 両手から片手にすると入力モード停止
        # if hand == 1:
        #     textinputFlag = False

        # # 小指だけを上げているとボリューム操作がOFF マウス動作もOFF
        # if (volumeFlag or mouseFlag or textinputFlag) and checkedList[0] == [0, 0, 0, 0, 1]:
        #     # volumeFlag = False
        #     # mouseFlag = False
        #     textinputFlag = False
        #     allOffCounter = 30


        # フリック入力()
        #KEYBOARDLIST
        # KEYBOARDは初期位置+50音の位置
        # 実行
        #親指を伸ばしたら選択状態になる
        if checkedList[0][0]:
            #最初は位置を記憶して判別する
            if KEYBOARDREMEN:
            # if KEYBOSRDLIST[10]:
                flick_x,flick_y=lmlist[0][8][1],lmlist[0][8][2]
                #縦から
                for ix in range(5):
                    for iy in range(5):
                        if ix*wVisal/5<=flick_x<(ix+1)*wVisal/5 and iy*hVisal/5<=flick_y<(iy+1)*hVisal/5:
                            KEYBOARDLIST[ix][iy]=True
                            xx,yy=ix,iy
                            # print(ix,iy)
                KEYBOARDREMEN=False
                INPUT_FLAG=True
        #親指を戻したら選択を確定してして初期化
        else:
            if INPUT_FLAG:
                #選択を確定して文字列に出力
                flick_now_x,flick_now_y=lmlist[0][8][1],lmlist[0][8][2]
                text=""
                # 特別例
                # delete
                # space
                if 4*wVisal/5<=flick_now_x<5*wVisal/5 and 3*hVisal/5<=flick_now_y<4*hVisal/5:
                    text="　"
                # enter
                # Quit

                for ix in range(5):
                    for iy in range(5):
                        if ix*wVisal/5<=flick_now_x<(ix+1)*wVisal/5 and iy*hVisal/5<=flick_now_y<(iy+1)*hVisal/5:
                            if ix==xx and iy==yy:
                                #あ行
                                text=KEYBOARD[yy][xx][0]
                            elif ix+1==xx and iy==yy:
                                #い行
                                text=KEYBOARD[yy][xx][1]
                            elif ix==xx and iy+1==yy:
                                #う行
                                text=KEYBOARD[yy][xx][2]
                            elif ix-1==xx and iy==yy:
                                #え行
                                text=KEYBOARD[yy][xx][3]
                            elif ix==xx and iy-1==yy:
                                #お行
                                text=KEYBOARD[yy][xx][4]
                            break
                    else:
                        continue
                    break
                if text!=" ":
                    INPUT_TEXTS+=text
                if text=="space":
                    INPUT_TEXTS=INPUT_TEXTS[:-6]
                    INPUT_TEXTS+="　"
                if text=="delete":
                    INPUT_TEXTS=INPUT_TEXTS[:-6]
                    if INPUT_TEXTS:
                        INPUT_TEXTS=INPUT_TEXTS[:-1]
                if text=="Enter":
                    INPUT_TEXTS=INPUT_TEXTS[:-5]
                    pyautogui.typewrite(INPUT_TEXTS)
                    INPUT_TEXTS=""

                # if text=="enter":
                #     INPUT_TEXTS="\n"
                print(INPUT_TEXTS)
                if text=="Quit":
                    INPUT_TEXTS=""
                if text=="かな":
                    INPUT_TEXTS=INPUT_TEXTS[:-2]
                    KEYBOARD=KEYBOARD_HIRA
                elif text=="カナ":
                    INPUT_TEXTS=INPUT_TEXTS[:-2]
                    KEYBOARD=KEYBOARD_KATA
                elif text=="英":
                    INPUT_TEXTS=INPUT_TEXTS[:-1]
                    KEYBOARD=KEYBOARD_ENGLISH_SM

            #初期化
            KEYBOARDLIST=np.full((5,5),False).tolist()
            KEYBOARDREMEN=True
            INPUT_FLAG=False
        # print(KEYBOARDLIST)

        # UI生成
        # 線
        for i in range(5):
            cv2.line(img2,(i*wVisal//5,0),(i*wVisal//5,hVisal),(255,0,0),1)
            cv2.line(img2, (0, i * hVisal // 5), (wVisal, i * hVisal // 5), (255, 0, 0), 1)

        # 選択時の背景色 #FF6666
        for id_x in range(5):
            for id_y in range(5):
                if KEYBOARDLIST[id_x][id_y]:
                    cv2.rectangle(img2,(id_x*wVisal//5,id_y*hVisal//5),((id_x+1)*wVisal//5,(id_y+1)*hVisal//5),(102,102,255),thickness=-1)

        # 文字 #9999FF
        for id_x in range(1,4):
            for id_y in range(1,4):
                if KEYBOARDLIST[id_x][id_y]:
                    cv2_putText_5(img2,KEYBOARD[id_y][id_x][0],((2*id_x+1)*wVisal//10,(2*id_y+1)*hVisal//10),font_Path, 50, (255, 99, 99))
                    cv2_putText_5(img2,KEYBOARD[id_y][id_x][1],((2*id_x-1)*wVisal//10,(2*id_y+1)*hVisal//10),font_Path, 50, (255, 99, 99))
                    cv2_putText_5(img2,KEYBOARD[id_y][id_x][2],((2*id_x+1)*wVisal//10,(2*id_y-1)*hVisal//10),font_Path, 50, (255, 99, 99))
                    cv2_putText_5(img2,KEYBOARD[id_y][id_x][3],((2*id_x+3)*wVisal//10,(2*id_y+1)*hVisal//10),font_Path, 50, (255, 99, 99))
                    cv2_putText_5(img2,KEYBOARD[id_y][id_x][4],((2*id_x+1)*wVisal//10,(2*id_y+3)*hVisal//10),font_Path, 50, (255, 99, 99))
        if KEYBOARDLIST[4][2]:
            #ワ行
            cv2_putText_5(img2,KEYBOARD[4][2][0],((2*4+1)*wVisal//10,(2*3+1)*hVisal//10),font_Path, 50, (255, 99, 99))
            cv2_putText_5(img2,KEYBOARD[4][2][1],((2*4+1)*wVisal//10,(2*2+1)*hVisal//10),font_Path, 50, (255, 99, 99))
            cv2_putText_5(img2,KEYBOARD[4][2][2],((2*4+1)*wVisal//10,(2*4+1)*hVisal//10),font_Path, 50, (255, 99, 99))
        if KEYBOARDREMEN:
            for i in range(5):
                for j in range(5):
                    cv2_putText_5(img2,KEYBOARD[i][j][0],((2*j+1)*wVisal//10,(2*i+1)*hVisal//10),font_Path, 50, (255, 99, 99))
                # print(KEYBOARD[i][j][0],(2*j+1)*wVisal//10,(2*i+1)*hVisal//10)
                # cv2.circle(img2,((2*j+1)*wVisal//10,(2*i+1)*hVisal//10),5,(255,99,99),cv2.FILLED)
        cv2.rectangle(img2,(10,hCam-frameR),(wCam-10,hCam-10),(102,102,255),3)
        if INPUT_TEXTS:
            cv2_putText_5(img2,INPUT_TEXTS,(wCam//2,hCam-frameR//2),font_Path, 50, (255, 99, 99))

        # 手の長さの範囲 50-300
        # volume range -65-0

        # # 音量調節Flag
        # if volumeFlag:
        #     # x4 y4: 親指の先端の座標を取得
        #     # x8 y8: 人差し指の先端の座標を取得
        #     # cx cy: 親指と人差指の先端の中点
        #     # length:親指と人差指の先端の長さ
        #     x4, y4 = lmlist[0][4][1], lmlist[0][4][2]
        #     x8, y8 = lmlist[0][8][1], lmlist[0][8][2]
        #     cx, cy = (x4 + x8) // 2, (y4 + y8) // 2
        #     cv2.circle(img, (x4, y4), 5, (255, 0, 255), cv2.FILLED)
        #     cv2.circle(img, (x8, y8), 5, (255, 0, 255), cv2.FILLED)
        #     cv2.line(img, (x4, y4), (x8, y8), (255, 10, 255), 3)
        #     length = math.sqrt((x4 - x8) ** 2 + (y4 - y8) ** 2)
        #     # print(length)
        #     if length > 50:  # 長さが50以上
        #         cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        #     if volumeConfirmFrag is False:
        #         # 音量調整
        #         vol = np.interp(length, [50, 300], [minVol, maxVol])
        #         volBar = np.interp(length, [50, 300], [400, 150])
        #         volPar = np.interp(length, [50, 300], [0, 100])
        #         # print(int(length), vol)
        #         volume.SetMasterVolumeLevel(vol, None)

        # # マウス操作Flag
        # if mouseFlag:
        #     # frameR[100] dot分の余裕をもたせてマウス操作ウィンドウを表示
        #     cv2.rectangle(
        #         img, (frameR, frameR), (wVisal - frameR, hVisal - frameR), (255, 0, 255), 2
        #     )
        #     cv2.rectangle(
        #         img2, (frameR, frameR), (wVisal - frameR, hVisal - frameR), (255, 0, 255), 2
        #     )
        #     # 座標計算
        #     x, y = lmlist[0][12][1] - frameR, lmlist[0][12][2] - frameR
        #     x, y = (
        #         int(x / (wVisal - (frameR * 2)) * wWin),
        #         int(y / (hVisal - (frameR * 2)) * hWin),
        #     )
        #     cv2.circle(
        #         img2, (lmlist[0][12][1], lmlist[0][12][2]), 10, (255, 0, 0), cv2.FILLED,
        #     )
        #     # 移動
        #     # print("\rX: "+str(x)+" Y: "+str(y), end="")
        #     # 画面内なら動かして　それ以外なら動かさない
        #     if 0 <= x < wWin and 0 <= y < hWin:
        #         # pyautogui.moveTo(x, y)
        #         mouse.move(x, y)
        # TODO:
        # 数字入力操作Flag (両手限定)
        if textinputFlag and hand == 2:
            # 文字確定Flag (片手を握ったら)
            if checkedList[1] == [0, 0, 0, 0, 0] and wframe == 0:
                # print(*checkedList)
                if checkedList[0] == [0, 0, 0, 0, 0]:
                    INPUT_TEXTS += "0"
                elif checkedList[0] == [1, 0, 0, 0, 0]:
                    INPUT_TEXTS += "1"
                elif checkedList[0] == [0, 1, 0, 0, 0]:
                    INPUT_TEXTS += "2"
                elif checkedList[0] == [1, 1, 0, 0, 0]:
                    INPUT_TEXTS += "3"
                elif checkedList[0] == [0, 0, 1, 0, 0]:
                    INPUT_TEXTS += "4"
                elif checkedList[0] == [1, 0, 1, 0, 0]:
                    INPUT_TEXTS += "5"
                elif checkedList[0] == [0, 1, 1, 0, 0]:
                    INPUT_TEXTS += "6"
                elif checkedList[0] == [1, 1, 1, 0, 0]:
                    INPUT_TEXTS += "7"
                elif checkedList[0] == [0, 0, 0, 1, 0]:
                    INPUT_TEXTS += "8"
                elif checkedList[0] == [1, 0, 0, 1, 0]:
                    INPUT_TEXTS += "9"
                elif checkedList[0] == [1, 1, 1, 1, 1]:
                    pyautogui.typewrite(INPUT_TEXTS)
                else:
                    print("NO_INPUT")
                wframe = 10
            print(INPUT_TEXTS)

        # # 入力確定動作-->左親指を閉じる
        # if checkedList[0][0] == 0:
        #     pyautogui.write(INPUT_TEXTS)

        #ポインタ処理
        cv2.circle(img2, (int(lmlist[0][8][1]), int(lmlist[0][8][2])), 5, (0, 0, 255), cv2.FILLED)


    # 文字関係
    # if 0 < volumeCounter and volumeFlag:
    #     volumeCounter -= 1
    #     conformText += "Changed >> Volume ON {0}\n".format(volumeCounter)
    #     textren += 1

    # if 0 < mouseCounter and mouseFlag:
    #     mouseCounter -= 1
    #     conformText += "Changed >> Mouse ON {0}\n".format(mouseCounter)
    #     textren += 1

    if 0 < allOffCounter and (mouseFlag is False or volumeFlag is False):
        allOffCounter -= 1
        conformText += "Changed >> ALL OFF {0}\n".format(allOffCounter)
        textren += 1

    if textinputFlag:
        conformText += "INPUTTEXT:{0}\n".format(INPUT_TEXTS)

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
    cv2.putText(
        img, f"FPS: {int(fps)}", (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3
    )
    wframe = max(0, wframe - 1)
    # 画像の表示
    cv2.imshow("Image", img)
    cv2.imshow("Point", img2)

    # 入力待ち 1F
    k = cv2.waitKey(1)
    # 入力がEscの場合閉じる
    if k == 27:
        sys.exit()
