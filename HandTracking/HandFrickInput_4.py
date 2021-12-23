# TODO:
# ・reterun forward機能追加：文字の入力の取り消しや進める機能

import pickle
import sys
import tkinter
import tkinter as tk
# from tkinter import ttk as tk
import socket

import cv2
import numpy as np
import pyautogui
import pykakasi
from PIL import Image, ImageOps, ImageTk  # 画像データ用
import threading

import handtrackingModule as htm
from module import cv2_putText_4, cv2_putText_5, cv2_putText_6

KEYBOARD_HIRA = [
    [["return", " ", " ", " ", " "], ["forward", " ", " ", " ", " "], ["矢印", "←", "↑", "↓", "→"], ["→", " ", " ", " ", " "], ["delete", "×", " ", " ", " "]],
    [["カナ", " ", " ", " ", " "], ["あ", "い", "う", "え", "お"], ["か", "き", "く", "け", "こ"], ["さ", "し", "す", "せ", "そ"], ["BS", " ", " ", " ", " "]],
    [["英", " ", " ", " ", " "], ["た", "ち", "つ", "て", "と"], ["な", "に", "ぬ", "ね", "の"], ["は", "ひ", "ふ", "へ", "ほ"], ["変換", " ", " ", " ", " "], ],
    [["012", " ", " ", " ", " "], ["ま", "み", "む", "め", "も"], ["や", "「", "ゆ", "」", "よ"], ["ら", "り", "る", "れ", "ろ"], ["space", " ", " ", " ", " "], ],
    [["Quit", " ", " ", " ", " "], ["-", " ", " ", " ", " "],  ["わ", "を", "ん", " ", " "],  ["゛", " ", " ", " ", " "], ["Input", "Enter", "search", " ", " "]], ]
KEYBOARD_HIRA_1 = [
    [["return", " ", " ", " ", " "], ["forward", " ", " ", " ", " "], ["矢印", "←", "↑", "↓", "→"], ["→", " ", " ", " ", " "], ["delete", "×", " ", " ", " "]],
    [["カナ", " ", " ", " ", " "], ["ぁ", "ぃ", "ぅ", "ぇ", "ぉ"], ["が", "ぎ", "ぐ", "げ", "ご"], ["ざ", "じ", "ず", "ぜ", "ぞ"], ["BS", " ", " ", " ", " "]],
    [["英", " ", " ", " ", " "], ["だ", "ぢ", "づ", "で", "ど"], [" ", " ", " ", " ", " "], ["ば", "び", "ぶ", "べ", "ぼ"], ["変換", " ", " ", " ", " "], ],
    [["012", " ", " ", " ", " "], ["ぱ", "ぴ", "ぷ", "ぺ", "ぽ"], ["ゃ", " ", "ゅ", " ", "ょ"], [" ", " ", " ", " ", " "], ["space", " ", " ", " ", " "], ],
    [["Quit", " ", " ", " ", " "], ["-", " ", " ", " ", " "],  [" ", " ", " ", " ", " "],  ["゛", " ", " ", " ", " "], ["Input", "Enter", "search", " ", " "]], ]
KEYBOARD_KATA = [
    [["return", " ", " ", " ", " "], ["forward", " ", " ", " ", " "], ["矢印", "←", "↑", "↓", "→"], [" ", " ", " ", " ", " "], ["delete", "×", " ", " ", " "]],
    [["かな", " ", " ", " ", " "], ["ア", "イ", "ウ", "エ", "オ"], ["カ", "キ", "ク", "ケ", "コ"], ["サ", "シ", "ス", "セ", "ソ"], ["BS", " ", " ", " ", " "]],
    [["英", " ", " ", " ", " "], ["タ", "チ", "ツ", "テ", "ト"], ["ナ", "二", "ヌ", "ネ", "ノ"], ["ハ", "ヒ", "フ", "へ", "ホ"], ["変換", " ", " ", " ", " "], ],
    [["012", " ", " ", " ", " "], ["マ", "ミ", "ム", "メ", "モ"], ["ヤ", "「", "ユ", "」", "ヨ"], ["ラ", "リ", "ル", "レ", "ロ"], ["space", " ", " ", " ", " "], ],
    [["Quit", " ", " ", " ", " "], ["-", " ", " ", " ", " "], ["ワ", "ヲ", "ン", " ", " "], ["゛", " ", " ", " ", " "], ["Input", "Enter", "search", " ", " "]], ]
KEYBOARD_KATA_1 = [
    [["return", " ", " ", " ", " "], ["forward", " ", " ", " ", " "], ["矢印", "←", "↑", "↓", "→"], [" ", " ", " ", " ", " "], ["delete", "×", " ", " ", " "]],
    [["かな", " ", " ", " ", " "], ["ァ", "ィ", "ゥ", "ェ", "ォ"], ["ガ", "ギ", "グ", "ゲ", "ゴ"], ["ザ", "ジ", "ズ", "ゼ", "ゾ"], ["BS", " ", " ", " ", " "]],
    [["英", " ", " ", " ", " "], ["ダ", "ヂ", "ズ", "デ", "ド"], [" ", " ", " ", " ", " "], ["バ", "ビ", "ブ", "ベ", "ボ"], ["変換", " ", " ", " ", " "], ],
    [["012", " ", " ", " ", " "], ["パ", "ピ", "プ", "ペ", "ポ"], ["ャ", " ", "ュ", " ", "ョ"], [" ", " ", " ", " ", " "], ["space", " ", " ", " ", " "], ],
    [["Quit", " ", " ", " ", " "], ["-", " ", " ", " ", " "], [" ", " ", " ", " ", " "], ["゛", " ", " ", " ", " "], ["Input", "Enter", "search", " ", " "]], ]
KEYBOARD_ENGLISH_SM = [
    [["return", " ", " ", " ", " "], ["forward", " ", " ", " ", " "], ["矢印", "←", "↑", "↓", "→"], [" ", " ", " ", " ", " "], ["delete", "×", " ", " ", " "]],
    [["A/a", " ", " ", " ", " "], ["a", "b", "c", " ", " "], ["d", "e", "f", " ", " "], ["g", "h", "i", " ", " "], ["BS", " ", " ", " ", " "]],
    [["かな", " ", " ", " ", " "], ["j", "k", "l", " ", " "], ["m", "n", "o", " ", " "], ["p", "q", "r", "s", " "], [" ", " ", " ", " ", " "], ],
    [["012", " ", " ", " ", " "], ["t", "u", "v", " ", " "], ["w", "x", "y", "z", " "], [" ", " ", " ", " ", " "], ["space", " ", " ", " ", " "], ],
    [["Quit", " ", " ", " ", " "], ["-", "_", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], ["Input", "Enter", "search", " ", " "]], ]
KEYBOARD_ENGLISH_BI = [
    [["return", " ", " ", " ", " "], ["forward", " ", " ", " ", " "], ["矢印", "←", "↑", "↓", "→"], [" ", " ", " ", " ", " "], ["delete", "×", " ", " ", " "]],
    [["A/a", " ", " ", " ", " "], ["A", "B", "C", " ", " "], ["D", "E", "F", " ", " "], ["G", "H", "I", " ", " "], [" ", " ", " ", " ", " "]],
    [["かな", " ", " ", " ", " "], ["J", "K", "L", " ", " "], ["M", "N", "O", " ", " "], ["P", "Q", "R", "S", " "], [" ", " ", " ", " ", " "], ],
    [["012", " ", " ", " ", " "], ["T", "U", "V", " ", " "], ["W", "X", "Y", "Z", " "], [" ", " ", " ", " ", " "], ["space", " ", " ", " ", " "], ],
    [["Quit", " ", " ", " ", " "], [" ", " ", " ", " ", " "],  [" ", " ", " ", " ", " "],  [" ", " ", " ", " ", " "], ["Input", "Enter", "search", " ", " "]], ]
KEYBOARD_NUMPER = [
    [["return", " ", " ", " ", " "], ["forward", " ", " ", " ", " "], ["矢印", "←", "↑", "↓", "→"], [" ", " ", " ", " ", " "], ["delete", "×", " ", " ", " "]],
    [["かな", " ", " ", " ", " "], ["1", " ", " ", " ", " "], ["2", " ", " ", " ", " "], ["3", " ", " ", " ", " "], ["BS", " ", " ", " ", " "]],
    [["英", " ", " ", " ", " "], ["4", " ", " ", " ", " "], ["5", " ", " ", " ", " "], ["6", " ", " ", " ", " "], ["変換", " ", " ", " ", " "], ],
    [["", " ", " ", " ", " "], ["7", " ", " ", " ", " "], ["8", " ", " ", " ", " "], ["9", " ", " ", " ", " "], ["space", " ", " ", " ", " "], ],
    [["Quit", " ", " ", " ", " "], ["ー", " ", " ", " ", " "], ["0", " ", " ", " ", " "], ["゛", " ", " ", " ", " "], ["Input", "Enter", "search", " ", " "]], ]


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        # self.wRoot, self.hRoot = 390, 400
        self.wRoot, self.hRoot = 800, 500
        self.master.title(u"OpenCVの動画表示")       # ウィンドウタイトル
        self.master.geometry("{0}x{1}".format(self.wRoot, self.hRoot))     # ウィンドウサイズ(幅x高さ)

        # Canvasの作成
        self.canvas = tk.Canvas(self.master, highlightthickness=0)
        # Canvasにマウスイベント（左ボタンクリック）の追加
        self.canvas.bind('<Button-1>', self.canvas_click)
        # Canvasを配置
        self.canvas.pack(expand=1, fill=tk.BOTH)

        # 文字入力フォームの作成
        self.entry1 = tkinter.Entry(self.master, font=("", 20))
        self.entry1.focus_set()
        self.entry1.pack()

        # カメラをオープンする
        self.capture = cv2.VideoCapture(0)
        # 画面入力フォームよりカメラの大きさを大きくしておく
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # カメラ画像の横幅を1280に設定
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # カメラ画像の縦幅を720に設定
        self.disp_id = None

        self.detector = htm.handDetectior(MaxHands=2, detectonCon=0.7)
        self.kakasi = pykakasi.kakasi()

        # 基本設定
        # ウィンドウの大きさの設定
        self.wCam, self.hCam = 1000, 700
        self.spaceH = 300
        self.spaceW = 150
        self.wVisal = self.wCam-self.spaceW
        self.hVisal = self.hCam-self.spaceH
        self.INPUT_TEXTS = u""
        self.INPUT_TEXTS_UI = u""
        self.KEYBOARDLIST = np.full((5, 5), False).tolist()
        self.KEYBOARDREMEN = True
        self.xx, self.yy = 0, 0
        self.INPUT_FLAG = False
        self.font_size = 50
        # self.font_Path = "C:\Windows\Fonts\メイリオ\meiryo.ttc"
        # self.font_Path_Bold = "C:\Windows\Fonts\メイリオ\meiryob.ttc"
        self.font_Path = "C:\Windows\Fonts\游ゴシック\YuGothR.ttc"
        self.font_Path_Bold = "C:\Windows\Fonts\游ゴシック\YuGothB.ttc"
        # 初期キーボードはかな入力に
        self.KEYBOARD = KEYBOARD_HIRA

        self.EVENT_Flag = 0
        self.search_text = ""

        self.Dict_num = 0
        self.Result_Button_pressed = [False]*4
        self.Detail_Button_pressed = [False]
        self.Books_num = -1

        self.savedIMG_Result = []
        self.savedIMG_Detail = []

        self.Visiter = [False]*4

    def canvas_click(self, event):
        '''Canvasのマウスクリックイベント'''
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
        # HOSTNAME = "172.25.180.202" #自分のサーバーのIPアドレス
        HOSTNAME = "localhost"
        PORT = 10541

        # ipv4を使うので、AF_INET
        # tcp/ip通信を使いたいので、SOCK_STREAM
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOSTNAME, PORT))
        # self.sock=sock

    def disp_image(self):
        '''画像をCanvasに表示する'''
        # フレーム画像の取得
        ret, frame = self.capture.read()
        if not ret:
            print("画像が読み込まれなかった")
            sys.exit()
        frame = cv2.flip(frame, 1)
        # フレーム画像から操作画面を取得
        # 手を認識させる
        img = self.detector.findHands(frame, drawLandmark=False)
        # self.detectorから 手位置lmlist 手の大きさbbox 手の本数handを取得する
        lmlist, bbox, hand = self.detector.findPosition(img, drawPosition=False, Normalization=True)
        hand += 1
        img2 = np.full((self.hCam, self.wCam, 3), 255, dtype=np.uint8)

        if len(lmlist) != 0:
            checkedList = self.detector.checkFinger()
            if self.EVENT_Flag == 0:
                # 指をおろしている判定を取得
                # フリック入力
                # self.KEYBOARDLIST
                # KEYBOARDは初期位置+50音の位置
                # 実行
                # 親指を伸ばしたら選択状態になる
                if not self.Visiter[0]:
                    self.Visiter[0] = True
                # Textboxを有効にする
                if not self.entry1.winfo_exists():
                    print("textbox復元")
                    self.entry1 = tkinter.Entry(self.master, font=("", 20))
                    self.entry1.insert(0, self.search_text)
                    self.entry1.focus_set()
                    self.entry1.pack()

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
                    # 手を戻したら選択を確定してして初期化
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
                                self.INPUT_TEXTS_UI = self.INPUT_TEXTS_UI[:-5]
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
                                self.search_text = self.entry1.get()
                                if self.search_text == "":
                                    print("中にはなにもない")
                                    # TODO:表示をつける
                                else:
                                    self.server_connect()
                                    self.sock.send(bytes(self.entry1.get(), "utf-8"))

                                    self.EVENT_Flag = 1
                                    self.Visiter[0] = False

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
                            elif text == "↑":
                                self.INPUT_TEXTS = self.INPUT_TEXTS[:-1]
                                self.INPUT_TEXTS_UI = self.INPUT_TEXTS_UI[:-1]
                                pyautogui.press("up")
                            elif text == "↓":
                                self.INPUT_TEXTS = self.INPUT_TEXTS[:-1]
                                self.INPUT_TEXTS_UI = self.INPUT_TEXTS_UI[:-1]
                                pyautogui.press("down")
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

            # データの受信処理
            elif self.EVENT_Flag == 1:
                # Visiter処理
                if not self.Visiter[1]:
                    self.Visiter[1] = True
                # ボタンを隠す
                # データの受信 TODO:並列化threadingして画面を表示させる
                img2 = np.full((self.hCam, self.wCam, 3), 255, dtype=np.uint8)
                print("Search_Mode")
                self.result_data = b""
                time = 0
                # データの長さを取得
                self.Num_books = int(self.sock.recv(1024).decode("utf-8"))
                print("{}bites".format(self.Num_books))
                # データ
                if self.Num_books == 0:
                    # -1を受信
                    self.result_data = int(self.sock.recv(1024).decode("utf-8"))
                else:
                    print("==受信開始==")
                    while True:
                        data = self.sock.recv(1024)
                        if len(data) <= 0:
                            break
                        self.result_data += data
                        time += len(data)
                        print("\r {:.2f} %".format(time/self.Num_books*100), end="        ")
                        # cv2_putText_5(img2, "{:.2f} % 完了".format(time/self.Num_books*100), (self.wCam//2, self.hCam//2), self.font_Path, 50, (100, 100, 100))

                        # print(data)
                    # print(self.result_data)
                    self.result_data = pickle.loads(self.result_data)
                    print("==受信終了==")
                # TODO:UI処理
                self.EVENT_Flag = 2
                self.Visiter[1] = False
                # データの表示
                # print(self.result_data)

            # 結果表示画面
            elif self.EVENT_Flag == 2:
                books = 15
                font = 20
                space = 10
                header_space = 50
                if not self.Visiter[2]:
                    self.Visiter[2] = 1
                # Textboxを隠す
                if self.entry1.winfo_exists():
                    self.entry1.pack_forget()
                    self.entry1.destroy()
                    self.canvas.pack(expand=1, fill=tk.BOTH)

                # モードの切替
                if hand == 2:
                    # (self.wCam//50, self.hCam//50), (self.wCam//50*10, self.hCam//50*5)
                    if checkedList[1] == [1, 1, 1, 1, 1] and self.wCam//50 <= lmlist[0][8][1] < self.wCam//50*10 and self.hCam//50 <= lmlist[0][8][2] < self.hCam//50*5:
                        # 戻るボタン
                        self.Result_Button_pressed[0] = True
                    elif checkedList[1] == [1, 1, 1, 1, 1] and self.wCam//100 <= lmlist[0][8][1] < self.wCam//100*98 and self.hCam//100*12 + header_space <= lmlist[0][8][2] < self.hCam//100*12 + header_space + (font+space) * (books+1):
                        self.Result_Button_pressed[1] = True
                        for i in range(books):
                            if hand == 2:
                                if self.Result_Button_pressed[1] and self.wCam//100 <= lmlist[0][8][1] < self.wCam//100*98 and self.hCam//100 * 12 + header_space + (font+space)*i <= lmlist[0][8][2] < self.hCam//100*12+header_space+(font+space)*(i+1):
                                    self.Num_books = i+self.Dict_num*books
                    elif checkedList[1] == [1, 1, 1, 1, 1] and self.wCam//100*55 <= lmlist[0][8][1] < self.wCam//100*85 and self.hCam//100*90 <= lmlist[0][8][2] < self.hCam//100*98:
                        # ページ戻り
                        self.Result_Button_pressed[2] = True
                    elif checkedList[1] == [1, 1, 1, 1, 1] and self.wCam//100*30 <= lmlist[0][8][1] < self.wCam//100*45 and self.hCam//100*90 <= lmlist[0][8][2] < self.hCam//100*98:
                        # ページ進み
                        self.Result_Button_pressed[3] = True
                    # ボタンがおされているかチェック
                    if self.Result_Button_pressed[0]:
                        self.EVENT_Flag = 0
                        self.savedIMG_Result = []
                        self.Visiter[2] = False
                    elif self.Result_Button_pressed[1]:
                        # 詳細画面
                        # 押した位置を記録
                        self.EVENT_Flag = 3
                        self.sevedIMG = []
                        self.Visiter[2] = False
                    elif self.Result_Button_pressed[2]:
                        # ページ戻り
                        self.Dict_num = max(0, self.Dict_num-1)
                    elif self.Result_Button_pressed[3]:
                        # ページ進み
                        self.Dict_num = min(self.Dict_num+1, len(self.result_data))
                    # 初期化
                    self.Result_Button_pressed = [False]*5
                    # frick_x1, frick_y1 = lmlist[0][8][1], lmlist[0][8][2]
                # UIの設定
                # 検索結果がなかった(-1が帰ってくる)とき
                # 画面更新がない場合は以前の画像を使う
                if not self.Visiter or self.Result_Button_pressed[2] or self.Result_Button_pressed[3]:
                    if self.result_data == -1:
                        cv2_putText_5(img2, "キーワードと一致する結果がございません\nキーワードを変えてお試しください", (self.wCam//2, self.hCam//2), self.font_Path, 30, (50, 50, 50))
                    else:
                        # 検索結果を表示
                        # print("表示")
                        # 検索結果Text
                        cv2_putText_6(img2, "「{}」の検索結果 {}件".format(self.search_text, len(self.result_data)), (self.wCam//50*12, self.hCam//50), self.font_Path, 40, (30, 30, 30))
                        # 検索結果UI
                        # 本の情報を表示する
                        # font:30?
                        cv2.rectangle(img2, (self.wCam//100, self.hCam//100*12), (self.wCam//100*98, self.hCam//100*12+header_space+(font+space)*(books)), (150, 150, 150), 2)
                        cv2_putText_6(img2, "{:3}|{:20}|{:10}".format("No", "タイトル", "著者"), (self.wCam//100+3, self.hCam//100*12 + header_space-font-space), self.font_Path, font, (100, 100, 100))
                        for i in range(books):
                            # print("{0}|{1}…|{2}…".format(i+1, self.result_data[i][1][:20], self.result_data[i][6][:15]))
                            id = self.Dict_num*books+i
                            # データ範囲外は表示しない
                            if id >= len(self.result_data):
                                break
                            if len(self.result_data[i][1]) > 20:
                                cv2_putText_6(img2, "{:3}|{:20}…|{:10}".format(id+1, self.result_data[id][1], self.result_data[id][6]),
                                              (self.wCam//100+3, self.hCam//100*12 + header_space+(font+space)*i), self.font_Path, font, (50, 50, 50))
                            else:
                                cv2_putText_6(img2, "{:3}|{:20}|{:10}".format(id+1, self.result_data[id][1], self.result_data[id][6]),
                                              (self.wCam//100+3, self.hCam//100*12 + header_space+(font+space)*i), self.font_Path, font, (50, 50, 50))

                            # 線
                            cv2.line(img2, (self.wCam//100, self.hCam//100*12 + header_space + (font+space)*i-space//2),
                                     (self.wCam//100*98, self.hCam//100*12 + header_space + (font+space)*i-space//2), (100, 100, 100), 1)
                        # 線
                        # cv2.line(img2, (self.wCam//100, self.hCam+header_space), (self.wCam//100*98, self.hCam+header_space), (100, 100, 100), 3)
                        cv2.line(img2, (self.wCam//100, self.hCam//100*12+header_space+(font+space)*books), (self.wCam//100*98, self.hCam//100*12+header_space+(font+space)*books), (100, 100, 100), 2)
                        # ページ戻りボタン
                        cv2.rectangle(img2, (self.wCam//100*30, self.hCam//100*85), (self.wCam//100*45, self.hCam//100*98), (175, 40, 40), 2)
                        cv2_putText_5(img2, "<<", (int(self.wCam/100*(30+45)/2), int(self.hCam/100*(85+98)/2)), self.font_Path, 50, (175, 40, 40))
                        # ページ進みボタン
                        cv2.rectangle(img2, (self.wCam//100*55, self.hCam//100*85), (self.wCam//100*70, self.hCam//100*98), (175, 40, 40), 2)
                        cv2_putText_5(img2, ">>", (int(self.wCam/100*(55+70)/2), int(self.hCam//100*(85+98)/2)), self.font_Path, 50, (175, 40, 40))
                    # 戻るボタン
                    cv2_putText_5(img2, "戻る", (int(self.wCam//50*11/2), int(self.hCam//50*3)), self.font_Path, 20, (127, 127, 127))
                    cv2.rectangle(img2, (self.wCam//50, self.hCam//50), (self.wCam//50*10, self.hCam//50*5), (125, 125, 125), 1)
                    # 画像を保存
                #     self.savedIMG_Result = img2.copy()

                # img2 = self.savedIMG_Result.copy()
                # print("{}|{}".format(id(img2),id(self.savedIMG_Result)))
                # 画像にポインタを追加する
                # ポインタ
                for i in range(hand):
                    # if lmlist[i][0][4]:
                    #     cv2.circle(img, (lmlist[i][0][1], lmlist[i][0][2]), 3, (0, 0, 255), cv2.FILLED)
                    # else:
                    #     cv2.circle(img, (lmlist[i][0][1], lmlist[i][0][2]), 3, (0, 255, 0), cv2.FILLED)
                    # cv2.circle(img, (int(lmlist[0][8][1]), int(lmlist[0][8][2])), 3, (0, 0, 255), cv2.FILLED)
                    cv2.circle(img2, (int(lmlist[0][8][1]), int(lmlist[0][8][2])), 4, (0, 0, 0), cv2.FILLED)
                if hand == 2:
                    if checkedList[1] == [1, 1, 1, 1, 1]:
                        cv2.circle(img2, (int(lmlist[0][8][1]), int(lmlist[0][8][2])), 3, (0, 0, 255), cv2.FILLED)
                    else:
                        cv2.circle(img2, (int(lmlist[0][8][1]), int(lmlist[0][8][2])), 3, (0, 255, 0), cv2.FILLED)

            # 詳細画面表示
            elif self.EVENT_Flag == 3:
                if not self.Visiter[3]:
                    self.Visiter[3] = True
                if hand == 2:
                    # (self.wCam//50, self.hCam//50), (self.wCam//50*10, self.hCam//50*5)
                    if checkedList[1] == [1, 1, 1, 1, 1] and self.wCam//50 <= lmlist[0][8][1] < self.wCam//50*10 and self.hCam//50 <= lmlist[0][8][2] < self.hCam//50*5:
                        # 戻るボタン
                        self.Detail_Button_pressed[0] = True
                    else:
                        if self.Detail_Button_pressed[0]:
                            self.EVENT_Flag = 2
                            self.Visiter[3] = False
                        self.Detail_Button_pressed[0] = False
                Data_Num = self.Books_num
                # 1タイトル 2タイトル（ふりがな） 6著者 7出版社 10出版年(W3CDTF) 11ISBN
                # 19公開範囲 0URL(クリックでサイトに飛べても可)
                font = 20
                Title_font = 30
                space = 15
                if not self.Visiter[3]:
                    cv2.rectangle(img2, (self.wCam//100, self.hCam//100*12), (self.wCam//100*98, self.hCam//100*98), (150, 150, 150), 2)
                    cv2_putText_6(img2, "{:14}".format(self.result_data[Data_Num][1]), (self.wCam//100, self.hCam//100*12), self.font_Path_Bold, Title_font, (100, 100, 100))
                    cv2_putText_6(img2, "{:20}".format(self.result_data[Data_Num][2]), (self.wCam//100, self.hCam//100*12+Title_font+space), self.font_Path_Bold, font, (100, 100, 100))
                    cv2_putText_6(img2, "著者    :{:20}".format(self.result_data[Data_Num][6]), (self.wCam//100, self.hCam//100*12+Title_font+font+space), self.font_Path, font, (100, 100, 100))
                    cv2_putText_6(img2, "出版社  :{:20}".format(self.result_data[Data_Num][7]), (self.wCam//100, self.hCam//100*12+Title_font+(font+space)*2), self.font_Path, font, (100, 100, 100))
                    cv2_putText_6(img2, "出版年  :{:20}".format(self.result_data[Data_Num][10]), (self.wCam//100, self.hCam//100*12+Title_font+(font+space)*3), self.font_Path, font, (100, 100, 100))
                    cv2_putText_6(img2, "ISBN   :{:20}".format(self.result_data[Data_Num][11]), (self.wCam//100, self.hCam//100*12+Title_font+(font+space)*4), self.font_Path, font, (100, 100, 100))
                    cv2_putText_6(img2, "公開範囲:{:20}".format(self.result_data[Data_Num][18]), (self.wCam//100, self.hCam//100*12+Title_font+(font+space)*5), self.font_Path, font, (100, 100, 100))
                    cv2_putText_6(img2, "URL    :{:40}\n        {:40}".format(self.result_data[Data_Num][0], self.result_data[Data_Num][0][20:]),
                                  (self.wCam//100, self.hCam//100*12+Title_font+(font+space)*6), self.font_Path, font, (100, 100, 100))
                    # 戻るボタン
                    cv2_putText_5(img2, "戻る", (int(self.wCam//50*11/2), int(self.hCam//50*3)), self.font_Path, 20, (127, 127, 127))
                    cv2.rectangle(img2, (self.wCam//50, self.hCam//50), (self.wCam//50*10, self.hCam//50*5), (125, 125, 125), 1)
                    self.savedIMG_Detali = img2.copy()
                img2 = self.savedIMG_Detail.copy()
                # ポインタ
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

        self.master.geometry("{0}x{1}".format(self.wRoot, self.hRoot))     # ウィンドウサイズ(幅x高さ)

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

        # disp_image()を1msec後に実行する
        self.disp_id = self.after(5, self.disp_image)


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.server_connect()
    app.mainloop()
