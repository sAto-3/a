#12/02にち

#TODO:
#   reterun forward機能の追加：文字の入力の取り消しや進める機能
#   通信機能:キーワードと検索ジャンルを入力し、サーバーに送信
#           サーバーから検索結果配列を受け取り、
#           検索結果表示画面に遷移し、検索結果を表示する機能

import PIL.ImageTk
import PIL.Image
import tkinter.font as font
import sys
import tkinter
import tkinter as tk
import socket

import cv2
import numpy as np
import pyautogui
import pykakasi
from PIL import Image, ImageOps, ImageTk  # 画像データ用

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
class App(tk.Tk):
    # 呪文
    def __init__(self, *args, **kwargs):
        # 呪文
        tk.Tk.__init__(self, *args, **kwargs)

        # ウィンドウタイトルを決定
        self.title("Tkinter_cv2")

        # ウィンドウの大きさを決定
        self.geometry("800x700")

        # ウィンドウのグリッドを 1x1 にする
        # この処理をコメントアウトすると配置がズレる
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # MyVideoCaptureクラスをcapとして使う
        self.cap = MyVideoCapture()

#-----------------------------------main_frame---------------------------------
        # メインページフレーム作成
        self.main_frame = tk.Frame()
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        # タイトルラベル作成
        self.titleLabel = tk.Label(self.main_frame, text="Tkinter with cv2", font=('Helvetica', '35'))
        self.titleLabel.pack(anchor='center', expand=True)
        # ボタン生成
        ## カメラ1用フレームに移動
        self.cam1_button = tk.Button(self.main_frame, text="Show Cam1", command=lambda: self.changePage(self.cam1_frame))
        self.cam1_button.pack()
        ## カメラ2用フレームに移動
        self.cam2_button = tk.Button(self.main_frame, text="Show Cam2", command=lambda: self.changePage(self.cam2_frame))
        self.cam2_button.pack()

#-----------------------------------cam1_frame---------------------------------
        # カメラ1用フレーム作成
        self.cam1_frame = tk.Frame()
        self.cam1_frame.grid(row=0, column=0, sticky="nsew")
        # カメラ1用キャンバス作成
        self.cam1_canvas = tk.Canvas(self.cam1_frame, width=self.cap.width, height=self.cap.height)
        self.cam1_canvas.pack()
        # カメラ1用フレームからmainフレームに戻るボタン
        self.back_button = tk.Button(self.cam1_frame, text="Back", command=lambda: self.changePage(self.main_frame))
        self.back_button.pack()

#-----------------------------------cam2_frame---------------------------------
        # カメラ2用フレーム作成
        self.cam2_frame = tk.Frame()
        self.cam2_frame.grid(row=0, column=0, sticky="nsew")
        # カメラ2用キャンバス作成
        self.cam2_canvas = tk.Canvas(self.cam2_frame, width=self.cap.width2, height=self.cap.height2)
        self.cam2_canvas.pack()
        # カメラ2用フレームからmainフレームに戻るボタン
        self.back_button = tk.Button(self.cam2_frame, text="Back", command=lambda: self.changePage(self.main_frame))
        self.back_button.pack()

        #main_frameを一番上に表示
        self.main_frame.tkraise()

        # 更新作業
        self.update()

    def changePage(self, page):
        '''
        画面遷移用の関数
        '''
        page.tkraise()

    def update(self):
        '''
        各キャンバスへの画像書き込み(opencvのimshow()的な処理)
        '''
        # MyVideoCaptureクラスのget_frameでcam1の映像を取得
        try:
            ret, frame = self.cap.get_frame()
        # 取得できなかったら
        except:
            ret = False
            frame = 0

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            #cam1_canvasに映像表示
            self.cam1_canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # 100ミリ秒ごとにupdate関数を実行
        self.after(100, self.update)


class MyVideoCapture:
    '''
    cv2での映像取得用クラス
    '''

    def __init__(self):
        # camの設定
        self.vid = cv2.VideoCapture(0)
        if not self.vid.isOpened():
            print('camera1 is not Unable')

        #cam1の画面サイズ取得
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        '''
        cam1画像取得
        '''
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            # 画像が読み込めたらTrueと読み込んだ画像を返す
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            # 画像が読み込めてなかったらFalseとNoneを返す
            else:
                return (ret, None)
        else:
            return (ret, None)
        
    def disp_image(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
