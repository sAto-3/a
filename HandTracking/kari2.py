from os import startfile
import sys
import tkinter

from cv2 import detail_BlocksCompensator

wRoot = 400
hRoot = 300

root = tkinter.Tk()
# 実行内容を記載
root.title(u"Title")  # タイトル
root.geometry("{0}x{1}".format(wRoot, hRoot))  # 大きさ 横x縦

# ラベル１(検索キーワード)
Static1 = tkinter.Label(text=u"検索ワード", foreground="#333333", background=None)
Static1.pack()

# １行入力ボックス
enpty = 20
EditBox = tkinter.Entry(width=50)
EditBox.pack()

# ボタン
# 関数
# ボタン1
def search(event):
    keyword = EditBox.get()
    print(u"***検索中***：word:{}".format(keyword))
# ボタン２
def delete(event):
    print(u"***削除中***")
    EditBox.delete(0, tkinter.END)

# ボタン１
Button1 = tkinter.Button(text=u"検索")
Button1.bind("<Button-1>", search)
Button1.pack()

# ボタン２
Button2 = tkinter.Button(text=u"削除")
Button2.bind("<Button-1>", delete)
Button2.pack()

#チェックボックス
Val1=tkinter.BooleanVar()
Val1.set(False)
CheckBox1=tkinter.Checkbutton(text=u"項目１",variable=Val1)
CheckBox1.pack()

# Static1.place(x=150,y=200)#位置が指定できる
# 実行内容を記載（終了）
root.mainloop()
