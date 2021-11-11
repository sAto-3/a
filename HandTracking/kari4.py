from time import sleep
import pyautogui as pg

sleep(7)

text="kan'jinyuuryoku"

for key in text:
    pg.press(key)
pg.press("space")
sleep(1)
pg.press("Enter")
pg.press("Enter")
