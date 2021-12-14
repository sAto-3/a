# tkinterのインポート
import tkinter as tk
import tkinter.ttk as ttk


def change_app(window):
    window.tkraise()


if __name__ == "__main__":
    # rootメインウィンドウの設定
    root = tk.Tk()
    root.title("tkinter application")
    root.geometry("300x150")

    # メインフレームの作成と設置
    frame = ttk.Frame(root)
    frame.grid(row=0, column=0, sticky="nsew", pady=20)

    # 各種ウィジェットの作成
    label1_frame = ttk.Label(frame, text="メインウィンドウ")
    entry1_frame = ttk.Entry(frame)
    button_change = ttk.Button(frame, text="アプリウィンドウに移動", command=lambda: change_app(frame_app))

    # 各種ウィジェットの設置
    label1_frame.pack()
    entry1_frame.pack()
    button_change.pack()
    
    # アプリフレームの作成と設置
    frame_app = ttk.Frame(root)
    frame_app.grid(row=0, column=0, sticky="nsew", pady=20)

    # 各種ウィジェットの作成
    label1_frame_app = ttk.Label(frame_app, text="アプリウィンドウ")
    entry1_frame_app = ttk.Entry(frame_app)
    button_change_frame_app = ttk.Button(frame_app, text="メインウィンドウに移動", command=lambda: change_app(frame))
    
    # 各種ウィジェットの設置
    label1_frame_app.pack()
    entry1_frame_app.pack()
    button_change_frame_app.pack()
    
    # frameを前面にする
    frame.tkraise()
    root.mainloop()
