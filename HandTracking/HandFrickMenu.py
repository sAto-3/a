# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import font
import PIL.Image
import PIL.ImageTk
from cv2 import exp


class App(tk.Tk):
    # 呪文
    def __init__(self, *args, **kwargs):
        # 呪文
        tk.Tk.__init__(self, *args, **kwargs)

        # ウィンドウタイトルを決定
        self.title("Tkinter change page")

        # ウィンドウの大きさを決定
        self.geometry("800x600")

        # ウィンドウのグリッドを 1x1 にする
        # この処理をコメントアウトすると配置がズレる
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
# -----------------------------------main_frame-----------------------------
        # メインページフレーム作成
        self.main_frame = tk.Frame()
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        # タイトルラベル作成
        self.titleLabel = tk.Label(self.main_frame, text="Mein_Menu", font=('Helvetica', '35'))
        self.titleLabel.pack(anchor='center', expand=True)
        # フレーム1に移動するボタン
        self.changePageButton = tk.Button(self.main_frame, text="Go to frame1", command=lambda: self.changePage(self.frame1))
        self.changePageButton.pack()
        # フレーム2に移動するボタン
        self.changePageButton = tk.Button(self.main_frame, text="Go to frame2", command=lambda: self.changePage(self.frame2))
        self.changePageButton.pack()
# --------------------------------------------------------------------------
# -----------------------------------frame1---------------------------------
        # 移動先フレーム作成
        self.frame1 = tk.Frame()
        self.frame1.grid(row=0, column=0, sticky="nsew")
        # タイトルラベル作成
        self.titleLabel = tk.Label(self.frame1, text="Input_Form", font=('Helvetica', '35'))
        self.titleLabel.pack(anchor='n', expand=True)
        # 描画用Canvasの作成
        self.canvas = tk.Canvas(self.frame1, highlightthickness=1)
        self.canvas.pack(expand=1, fill=tk.BOTH)
        # 文字入力フォームの作成
        self.entry1 = tk.Entry(self.frame1, font=("nsew", 20))
        self.entry1.focus_set()
        self.entry1.pack()
        # フレーム1からmainフレームに戻るボタン
        self.back_button = tk.Button(self.frame1, text="Back", command=lambda: self.changePage(self.main_frame))
        self.back_button.pack()
# --------------------------------------------------------------------------
# -----------------------------------frame2---------------------------------
        # 移動先フレーム作成
        self.frame2 = tk.Frame()
        self.frame2.grid(row=0, column=0, sticky="nsew")
        # タイトルラベル作成
        self.titleLabel = tk.Label(self.frame2, text="Input_Form", font=('Helvetica', '35'))
        self.titleLabel.pack(anchor='n', expand=True)
        # フレーム1からmainフレームに戻るボタン
        self.back_button = tk.Button(self.frame2, text="Back", command=lambda: self.changePage(self.main_frame))
        self.back_button.pack()
# --------------------------------------------------------------------------

        # main_frameを一番上に表示
        self.main_frame.tkraise()

     def changePage(self, page):
        '''
        画面遷移用の関数
        '''
        page.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
