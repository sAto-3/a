# TODO:
# ・reterun forward機能追加：文字の入力の取り消しや進める機能

import sys
import tkinter
import tkinter as tk
import socket

import cv2
import numpy as np
import pyautogui
import pykakasi
from PIL import Image, ImageOps, ImageTk

import handtrackingModule as htm
from module import cv2_putText_5

KEYBOARD_HIRA = [
    [["return", " ", " ", " ", " "], ["forward", " ", " ", " ", " "], ["←", " ", " ", " ", " "], ["→", " ", " ", " ", " "], ["delete", "×", " ", " ", " "]],
    [["カナ", " ", " ", " ", " "], ["あ", "い", "う", "え", "お"], ["か", "き", "く", "け", "こ"], ["さ", "し", "す", "せ", "そ"], ["BS", " ", " ", " ", " "]],
    [["英", " ", " ", " ", " "], ["た", "ち", "つ", "て", "と"], ["な", "に", "ぬ", "ね", "の"], ["は", "ひ", "ふ", "へ", "ほ"], ["変換", " ", " ", " ", " "], ],
    [["012", " ", " ", " ", " "], ["ま", "み", "む", "め", "も"], ["や", "「", "ゆ", "」", "よ"], ["ら", "り", "る", "れ", "ろ"], ["space", " ", " ", " ", " "], ],
    [["Quit", " ", " ", " ", " "], ["-", " ", " ", " ", " "],  ["わ", "を", "ん", " ", " "],  ["゛", " ", " ", " ", " "], ["Input", "Enter", "search", " ", " "]], ]
KEYBOARD_HIRA_1 = [
    [["return", " ", " ", " ", " "], ["forward", " ", " ", " ", " "], ["←", " ", " ", " ", " "], ["→", " ", " ", " ", " "], ["delete", "×", " ", " ", " "]],
    [["カナ", " ", " ", " ", " "], ["ぁ", "ぃ", "ぅ", "ぇ", "ぉ"], ["が", "ぎ", "ぐ", "げ", "ご"], ["ざ", "じ", "ず", "ぜ", "ぞ"], ["BS", " ", " ", " ", " "]],
    [["英", " ", " ", " ", " "], ["だ", "ぢ", "づ", "で", "ど"], [" ", " ", " ", " ", " "], ["ば", "び", "ぶ", "べ", "ぼ"], ["変換", " ", " ", " ", " "], ],
    [["012", " ", " ", " ", " "], ["ぱ", "ぴ", "ぷ", "ぺ", "ぽ"], ["ゃ", " ", "ゅ", " ", "ょ"], [" ", " ", " ", " ", " "], ["space", " ", " ", " ", " "], ],
    [["Quit", " ", " ", " ", " "], ["-", " ", " ", " ", " "],  [" ", " ", " ", " ", " "],  ["゛", " ", " ", " ", " "], ["Input", "Enter", "search", " ", " "]], ]
KEYBOARD_KATA = [
    [["return", " ", " ", " ", " "], ["forward", " ", " ", " ", " "], ["←", " ", " ", " ", " "], ["→", " ", " ", " ", " "], ["delete", "×", " ", " ", " "]],
    [["かな", " ", " ", " ", " "], ["ア", "イ", "ウ", "エ", "オ"], ["カ", "キ", "ク", "ケ", "コ"], ["サ", "シ", "ス", "セ", "ソ"], ["BS", " ", " ", " ", " "]],
    [["英", " ", " ", " ", " "], ["タ", "チ", "ツ", "テ", "ト"], ["ナ", "二", "ヌ", "ネ", "ノ"], ["ハ", "ヒ", "フ", "へ", "ホ"], ["変換", " ", " ", " ", " "], ],
    [["012", " ", " ", " ", " "], ["マ", "ミ", "ム", "メ", "モ"], ["ヤ", "「", "ユ", "」", "ヨ"], ["ラ", "リ", "ル", "レ", "ロ"], ["space", " ", " ", " ", " "], ],
    [["Quit", " ", " ", " ", " "], ["-", " ", " ", " ", " "], ["ワ", "ヲ", "ン", " ", " "], ["゛", " ", " ", " ", " "], ["Input", "Enter", "search", " ", " "]], ]
KEYBOARD_KATA_1 = [
    [["return", " ", " ", " ", " "], ["forward", " ", " ", " ", " "], ["←", " ", " ", " ", " "], ["→", " ", " ", " ", " "], ["delete", "×", " ", " ", " "]],
    [["かな", " ", " ", " ", " "], ["ァ", "ィ", "ゥ", "ェ", "ォ"], ["ガ", "ギ", "グ", "ゲ", "ゴ"], ["ザ", "ジ", "ズ", "ゼ", "ゾ"], ["BS", " ", " ", " ", " "]],
    [["英", " ", " ", " ", " "], ["ダ", "ヂ", "ズ", "デ", "ド"], [" ", " ", " ", " ", " "], ["バ", "ビ", "ブ", "ベ", "ボ"], ["変換", " ", " ", " ", " "], ],
    [["012", " ", " ", " ", " "], ["パ", "ピ", "プ", "ペ", "ポ"], ["ャ", " ", "ュ", " ", "ョ"], [" ", " ", " ", " ", " "], ["space", " ", " ", " ", " "], ],
    [["Quit", " ", " ", " ", " "], ["-", " ", " ", " ", " "], [" ", " ", " ", " ", " "], ["゛", " ", " ", " ", " "], ["Input", "Enter", "search", " ", " "]], ]
KEYBOARD_ENGLISH_SM = [
    [["return", " ", " ", " ", " "], ["forward", " ", " ", " ", " "], ["←", " ", " ", " ", " "], ["→", " ", " ", " ", " "], ["delete", "×", " ", " ", " "]],
    [["A/a", " ", " ", " ", " "], ["a", "b", "c", " ", " "], ["d", "e", "f", " ", " "], ["g", "h", "i", " ", " "], ["BS", " ", " ", " ", " "]],
    [["かな", " ", " ", " ", " "], ["j", "k", "l", " ", " "], ["m", "n", "o", " ", " "], ["p", "q", "r", "s", " "], [" ", " ", " ", " ", " "], ],
    [["012", " ", " ", " ", " "], ["t", "u", "v", " ", " "], ["w", "x", "y", "z", " "], [" ", " ", " ", " ", " "], ["space", " ", " ", " ", " "], ],
    [["Quit", " ", " ", " ", " "], ["-", "_", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], ["Input", "Enter", "search", " ", " "]], ]
KEYBOARD_ENGLISH_BI = [
    [["return", " ", " ", " ", " "], ["forward", " ", " ", " ", " "], ["←", " ", " ", " ", " "], [" ", " ", " ", " ", " "], ["delete", "×", " ", " ", " "]],
    [["A/a", " ", " ", " ", " "], ["A", "B", "C", " ", " "], ["D", "E", "F", " ", " "], ["G", "H", "I", " ", " "], [" ", " ", " ", " ", " "]],
    [["かな", " ", " ", " ", " "], ["J", "K", "L", " ", " "], ["M", "N", "O", " ", " "], ["P", "Q", "R", "S", " "], [" ", " ", " ", " ", " "], ],
    [["012", " ", " ", " ", " "], ["T", "U", "V", " ", " "], ["W", "X", "Y", "Z", " "], [" ", " ", " ", " ", " "], ["space", " ", " ", " ", " "], ],
    [["Quit", " ", " ", " ", " "], [" ", " ", " ", " ", " "],  [" ", " ", " ", " ", " "],  [" ", " ", " ", " ", " "], ["Input", "Enter", "search", " ", " "]], ]
KEYBOARD_NUMPER = [
    [["return", " ", " ", " ", " "], ["forward", " ", " ", " ", " "], ["←", " ", " ", " ", " "], ["→", " ", " ", " ", " "], ["delete", "×", " ", " ", " "]],
    [["かな", " ", " ", " ", " "], ["1", " ", " ", " ", " "], ["2", " ", " ", " ", " "], ["3", " ", " ", " ", " "], ["BS", " ", " ", " ", " "]],
    [["英", " ", " ", " ", " "], ["4", " ", " ", " ", " "], ["5", " ", " ", " ", " "], ["6", " ", " ", " ", " "], ["変換", " ", " ", " ", " "], ],
    [["", " ", " ", " ", " "], ["7", " ", " ", " ", " "], ["8", " ", " ", " ", " "], ["9", " ", " ", " ", " "], ["space", " ", " ", " ", " "], ],
    [["Quit", " ", " ", " ", " "], ["ー", " ", " ", " ", " "], ["0", " ", " ", " ", " "], ["゛", " ", " ", " ", " "], ["Input", "Enter", "search", " ", " "]], ]


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("HandFrickInput")

        self.wRoot, self.hRoot = 700, 700
        self.geometry("{0}x{1}".format(self.wRoot, self.hRoot))     # ウィンドウサイズ(幅x高さ)
        # 初期画面 master0の作成

        # 入力画面 master1の作成
        self.master1 = tk.Frame()

        # self.wRoot, self.hRoot = 390, 400

        # Canvasの作成
        self.canvas = tk.Canvas(self.master1, highlightthickness=0)
        # Canvasにマウスイベント（左ボタンクリック）の追加
        self.canvas.bind('<Button-1>', self.canvas_click)
        # Canvasを配置
        self.canvas.pack(expand=1, fill=tk.BOTH)

        # 文字入力フォームの作成
        self.entry1 = tkinter.Entry(self.master1, font=("", 20))
        self.entry1.focus_set()
        self.entry1.pack()

        # カメラをオープンする
        self.capture = cv2.VideoCapture(0)
        # 画面入力フォームよりカメラの大きさを大きくしておく
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # カメラ画像の横幅を1280に設定
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)  # カメラ画像の縦幅を720に設定
        self.disp_id = None

        self.detector = htm.handDetectior(MaxHands=2, detectonCon=0.7)
        self.kakasi = pykakasi.kakasi()
        # 基本設定
        # ウィンドウの大きさの設定
        self.wCam, self.hCam = 1000, 700
        # 入力結果表示UI用スペース
        self.spaceH = 300
        self.spaceW = 150
        # 入力キーボード表示UIのスペース
        self.wVisal = self.wCam-self.spaceW
        self.hVisal = self.hCam-self.spaceH
        # 入力テキスト表示UI用変数
        self.INPUT_TEXTS = u""
        self.INPUT_TEXTS_UI = u""
        # キーボード選択リスト
        self.KEYBOARDLIST = np.full((5, 5), False).tolist()
        self.KEYBOARDREMEN = True
        self.xx, self.yy = 0, 0
        self.INPUT_FLAG = False
        self.font_size = 50
        self.font_Path = "C:\Windows\Fonts\HGRGM.TTC"
        # 初期キーボードはかな入力に
        self.KEYBOARD = KEYBOARD_HIRA

        # self.Flick_Frag = True

    def canvas_click(self, event):
        '''Canvasのマウスクリックイベント'''
        print(self.disp_id)
        if self.disp_id is None:
            # 動画を表示
            pyautogui.press("kanji")
            self.disp_image()
        else:
            # 動画を停止
            self.after_cancel(self.disp_id)
            self.disp_id = None

    def server_connect(self):
        # TCP通信関係
        #
        # HOSTNAME = "172.25.180.202"  # 自分のサーバーのIPアドレス
        HOSTNAME = "localhost"
        PORT = 10541

        # ipv4を使うので、AF_INET
        # tcp/ip通信を使いたいので、SOCK_STREAM
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOSTNAME, PORT))
        # self.sock=sock

    def disp_image(self):
        '''画像をCanvasに表示する'''
        # print(self.Flick_Frag)
        # if self.Flick_Flag:
        # フレーム画像の取得
        ret, frame = self.capture.read()
        frame = cv2.flip(frame, 1)
        # フレーム画像から操作画面を取得
        # 手を認識させる
        img = self.detector.findHands(frame, drawLandmark=False)
        # self.detectorから 手位置lmlist 手の大きさbbox 手の本数handを取得する
        lmlist, bbox, hand = self.detector.findPosition(img, drawPosition=False, Normalization=True)
        hand += 1
        img2 = np.full((self.hCam, self.wCam, 3), 255, dtype=np.uint8)

        if len(lmlist) != 0:
            # 指をおろしている判定を取得
            checkedList = self.detector.checkFinger()
            # フリック入力
            # self.KEYBOARDLIST
            # 実行
            # 親指を伸ばしたら選択状態になる

            if hand == 2:
                if checkedList[1] == [1, 1, 1, 1, 1]:
                    # 最初は位置を記憶して判別する
                    if self.KEYBOARDREMEN:
                        # if KEYBOSRDLIST[10]:
                        frick_x1, frick_y1 = lmlist[0][8][1], lmlist[0][8][2]
                        # 縦から
                        for ix in range(5):
                            for iy in range(5):
                                if ix * self.wVisal / 5 + self.spaceW <= frick_x1 < (ix + 1) * self.wVisal / 5 + self.spaceW and iy * self.hVisal / 5 <= frick_y1 < (iy + 1) * self.hVisal / 5:
                                    self.KEYBOARDLIST[ix][iy] = True
                                    self.xx, self.yy = ix, iy
                                    # print(ix,iy)
                        self.KEYBOARDREMEN = False
                        self.INPUT_FLAG = True
                # 親指を戻したら選択を確定してして初期化
                else:
                    if self.INPUT_FLAG:
                        # 選択を確定して文字列に出力
                        frick_now_x, frick_now_y = lmlist[0][8][1], lmlist[0][8][2]
                        text = ""
                        # 特別例
                        # space
                        if 4 * self.wVisal / 5 + self.spaceW <= frick_now_x < 5 * self.wVisal / 5 + self.spaceW and 3 * self.hVisal / 5 <= frick_now_y < 4 * self.hVisal / 5:
                            text = "　"  # 全角空白
                        # enter
                        # Quit
                        for ix in range(5):
                            for iy in range(5):
                                if ix * self.wVisal / 5 + self.spaceW <= frick_now_x < (ix + 1) * self.wVisal / 5 + self.spaceW and iy * self.hVisal / 5 <= frick_now_y < (iy + 1) * self.hVisal / 5:
                                    if ix == self.xx and iy == self.yy:
                                        # あ行
                                        text = self.KEYBOARD[self.yy][self.xx][0]
                                    elif ix + 1 == self.xx and iy == self.yy:
                                        # い行
                                        text = self.KEYBOARD[self.yy][self.xx][1]
                                    elif ix == self.xx and iy + 1 == self.yy:
                                        # う行
                                        text = self.KEYBOARD[self.yy][self.xx][2]
                                    elif ix - 1 == self.xx and iy == self.yy:
                                        # え行
                                        text = self.KEYBOARD[self.yy][self.xx][3]
                                    elif ix == self.xx and iy - 1 == self.yy:
                                        # お行
                                        text = self.KEYBOARD[self.yy][self.xx][4]
                                    break
                            else:
                                continue
                            break
                        if text != " ":
                            self.INPUT_TEXTS += text
                            self.INPUT_TEXTS_UI += text
                        if text == "ん" or text == "ン":
                            self.INPUT_TEXTS += "'"
                        elif text == "delete":
                            self.INPUT_TEXTS = self.INPUT_TEXTS[:-6]
                            self.INPUT_TEXTS_UI = self.INPUT_TEXTS_UI[:-6]
                            if self.INPUT_TEXTS:
                                self.INPUT_TEXTS = self.INPUT_TEXTS[:-1]
                                self.INPUT_TEXTS_UI = self.INPUT_TEXTS_UI[:-1]
                        elif text == "space":
                            self.INPUT_TEXTS = self.INPUT_TEXTS[:-5]
                            self.INPUT_TEXTS_UI = self.INPUT_TEXTS_UI[-5]
                            self.INPUT_TEXTS += "　"
                            self.INPUT_TEXTS_UI += "　"
                        elif text == "Enter":
                            self.INPUT_TEXTS = self.INPUT_TEXTS[:-5]
                            self.INPUT_TEXTS_UI = self.INPUT_TEXTS_UI[:-5]
                            pyautogui.press("Enter")
                        elif text == "Input":
                            self.INPUT_TEXTS = self.INPUT_TEXTS[:-5]
                            self.INPUT_TEXTS_UI = self.INPUT_TEXTS_UI[:-5]
                            # 文字を日本語文字からローマ字変換してから該当する文字を入力
                            romaji = self.kakasi.convert(self.INPUT_TEXTS)
                            # print(romaji)
                            for bun in romaji:
                                # print(bun["kunrei"])
                                for key in bun["kunrei"]:
                                    pyautogui.press(key)
                            self.INPUT_TEXTS = u""
                            self.INPUT_TEXTS_UI = u""
                        elif text == "search":
                            self.INPUT_TEXTS = self.INPUT_TEXTS[:-6]
                            self.INPUT_TEXTS_UI = self.INPUT_TEXTS_UI[:-6]
                            self.sock.send(bytes(self.entry1.get(), "utf-8"))

                        elif text == "×":
                            self.INPUT_TEXTS = u""
                            self.INPUT_TEXTS_UI = u""
                        elif text == "BS":
                            self.INPUT_TEXTS = self.INPUT_TEXTS[:-2]
                            self.INPUT_TEXTS_UI = ""
                            pyautogui.press("backspace")
                        # if text=="enter":
                        #     self.INPUT_TEXTS="\n"
                        elif text == "Quit":
                            sys.exit()
                        elif text == "゛":
                            self.INPUT_TEXTS = self.INPUT_TEXTS[:-1]
                            self.INPUT_TEXTS_UI = self.INPUT_TEXTS_UI[:-1]
                            # キーボード切り替え処理
                            if self.KEYBOARD == KEYBOARD_HIRA_1:
                                self.KEYBOARD = KEYBOARD_HIRA
                            elif self.KEYBOARD == KEYBOARD_HIRA:
                                self.KEYBOARD = KEYBOARD_HIRA_1
                            elif self.KEYBOARD == KEYBOARD_KATA:
                                self.KEYBOARD = KEYBOARD_KATA_1
                            elif self.KEYBOARD == KEYBOARD_KATA_1:
                                self.KEYBOARD = KEYBOARD_KATA
                        elif text == "かな":
                            self.INPUT_TEXTS = self.INPUT_TEXTS[:-2]
                            self.INPUT_TEXTS_UI = self.INPUT_TEXTS_UI[:-2]
                            self.KEYBOARD = KEYBOARD_HIRA
                            pyautogui.press("kanji")
                        elif text == "カナ":
                            self.INPUT_TEXTS = self.INPUT_TEXTS[:-2]
                            self.INPUT_TEXTS_UI = self.INPUT_TEXTS_UI[:-2]
                            self.KEYBOARD = KEYBOARD_KATA
                        elif text == "英":
                            self.INPUT_TEXTS = self.INPUT_TEXTS[:-1]
                            self.INPUT_TEXTS_UI = self.INPUT_TEXTS_UI[:-1]
                            self.KEYBOARD = KEYBOARD_ENGLISH_SM
                            pyautogui.press("kanji")

                        elif text == "A/a":
                            self.INPUT_TEXTS = self.INPUT_TEXTS[:-3]
                            self.INPUT_TEXTS_UI = self.INPUT_TEXTS_UI[:-3]
                            if self.KEYBOARD == KEYBOARD_ENGLISH_BI:
                                self.KEYBOARD = KEYBOARD_ENGLISH_SM
                            else:
                                self.KEYBOARD = KEYBOARD_ENGLISH_BI
                        elif text == "012":
                            self.INPUT_TEXTS = self.INPUT_TEXTS[:-3]
                            self.INPUT_TEXTS_UI = self.INPUT_TEXTS_UI[:-3]
                            self.KEYBOARD = KEYBOARD_NUMPER
                        elif text == "変換":
                            self.INPUT_TEXTS = self.INPUT_TEXTS[:-2]
                            self.INPUT_TEXTS_UI = self.INPUT_TEXTS_UI[:-2]
                            pyautogui.press("space")
                        elif text == "←":
                            self.INPUT_TEXTS = self.INPUT_TEXTS[:-1]
                            self.INPUT_TEXTS_UI = self.INPUT_TEXTS_UI[:-1]
                            pyautogui.press("left")
                        elif text == "→":
                            self.INPUT_TEXTS = self.INPUT_TEXTS[:-1]
                            self.INPUT_TEXTS_UI = self.INPUT_TEXTS_UI[:-1]
                            pyautogui.press("right")
                    # 初期化
                    self.KEYBOARDLIST = np.full((5, 5), False).tolist()
                    self.KEYBOARDREMEN = True
                    self.INPUT_FLAG = False
                # print(self.KEYBOARDLIST)

            # UI生成
            # 線
            for i in range(6):
                cv2.line(img2, (i * self.wVisal // 5+self.spaceW, 0), (i * self.wVisal // 5 + self.spaceW, self.hVisal), (255, 0, 0), 1)
                cv2.line(img2, (self.spaceW, i * self.hVisal // 5), (self.wVisal + self.spaceW, i * self.hVisal // 5), (255, 0, 0), 1)

            # 選択時の背景色 #FF6666
            for id_x in range(5):
                for id_y in range(5):
                    if self.KEYBOARDLIST[id_x][id_y]:
                        cv2.rectangle(img2, (id_x * self.wVisal // 5 + self.spaceW, id_y * self.hVisal // 5), ((id_x + 1) *
                                                                                                                self.wVisal // 5 + self.spaceW, (id_y + 1) * self.hVisal // 5), (102, 102, 255), thickness=-1)

            # 文字 #9999FF
            for id_x in range(1, 5):
                for id_y in range(1, 5):
                    if self.KEYBOARDLIST[id_x][id_y]:
                        cv2_putText_5(img2, self.KEYBOARD[id_y][id_x][0], ((2*id_x+1)*self.wVisal//10+self.spaceW, (2*id_y+1)*self.hVisal//10), self.font_Path, self.font_size, (255, 99, 99))
                        cv2_putText_5(img2, self.KEYBOARD[id_y][id_x][1], ((2*id_x-1)*self.wVisal//10+self.spaceW, (2*id_y+1)*self.hVisal//10), self.font_Path, self.font_size, (255, 99, 99))
                        cv2_putText_5(img2, self.KEYBOARD[id_y][id_x][2], ((2*id_x+1)*self.wVisal//10+self.spaceW, (2*id_y-1)*self.hVisal//10), self.font_Path, self.font_size, (255, 99, 99))
                        cv2_putText_5(img2, self.KEYBOARD[id_y][id_x][3], ((2*id_x+3)*self.wVisal//10+self.spaceW, (2*id_y+1)*self.hVisal//10), self.font_Path, self.font_size, (255, 99, 99))
                        cv2_putText_5(img2, self.KEYBOARD[id_y][id_x][4], ((2*id_x+1)*self.wVisal//10+self.spaceW, (2*id_y+3)*self.hVisal//10), self.font_Path, self.font_size, (255, 99, 99))
            if self.KEYBOARDREMEN:
                for i in range(5):
                    for j in range(5):
                        cv2_putText_5(img2, self.KEYBOARD[i][j][0], ((2*j+1)*self.wVisal//10+self.spaceW, (2*i+1)*self.hVisal//10), self.font_Path, self.font_size, (255, 99, 99))
                    # print(KEYBOARD[i][j][0],(2*j+1)*self.wVisal//10,(2*i+1)*self.hVisal//10)
                    # cv2.circle(img2,((2*j+1)*self.wVisal//10,(2*i+1)*self.hVisal//10),5,(255,99,99),cv2.FILLED)
            cv2.rectangle(img2, (10, 10+self.hCam-self.spaceH), (self.wCam-10, self.hCam-10), (102, 102, 255), 3)
            if self.INPUT_TEXTS_UI:
                cv2_putText_5(img2, self.INPUT_TEXTS_UI, (self.wCam//2, self.hCam - self.spaceH//2), self.font_Path, self.font_size, (255, 99, 99))

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

        # BGR→RGB変換
        cv_image = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        # NumPyのndarrayからPillowのImageへ変換
        pil_image = Image.fromarray(cv_image)

        # キャンバスのサイズを取得
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # 画像のアスペクト比（縦横比）を崩さずに指定したサイズ（キャンバスのサイズ）全体に画像をリサイズする
        pil_image = ImageOps.pad(pil_image, (canvas_width, canvas_height))

        # PIL.ImageからPhotoImageへ変換する
        self.photo_image = ImageTk.PhotoImage(image=pil_image)

        # 画像の描画
        self.canvas.create_image(
            canvas_width / 2,       # 画像表示位置(Canvasの中心)
            canvas_height / 2,
            image=self.photo_image  # 表示画像データ
        )

        # disp_image()を10msec後に実行する
        self.disp_id = self.after(10, self.disp_image)
        # else:
        #     # TODO:検索結果を表示する
        #     pass


if __name__ == "__main__":
    app = Application()
    app.server_connect()
    app.mainloop()
