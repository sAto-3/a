import pyautogui
import sys
print('Press Ctrl-C to quit.')
try:
    while True:
        x, y = pyautogui.position()
        F = pyautogui.onScreen(x, y)
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4) + " " + str(F)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
except KeyboardInterrupt:
    print('\n')
