from comtypes import DISPPROPERTY
import pyautogui
import keyboard
import time
(wWin, hWin) = pyautogui.size()
nowtime = 0
tmp = 0
sum=0
sumfps=0
frames=0
x = 0
y = 0
dx = 1
dy = 1
while True:
    frames+=1
    nowtime = time.time()
    print(nowtime-tmp,1/(nowtime-tmp))
    sum+=nowtime-tmp
    sumfps+=1/(nowtime-tmp)
    if x == 0:
        dx = 1
    elif x == wWin-1:
        dx = -1
    if y == 0:
        dy = 1
    elif y == hWin-1:
        dy = -1

    x += dx
    y += dy

    pyautogui.moveTo(x, y)
    # key入力
    # key = keyboard.read_key()
    # if key == "q":
    #     print("You pressed q.")
    #     break
    tmp = nowtime
print(sum/frames,sumfps/frames)