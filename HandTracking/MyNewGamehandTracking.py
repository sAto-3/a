import cv2
import mediapipe as mp
import time
import sys
import handtrackingModule as htm
pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    #
    print("Error:カメラが接続されていません！！")
    sys.exit()


detector = htm.handDetectior()
while True:
    # 画像の読み込み
    success, img = cap.read()
    print(success)
    img = detector.findHands(img)
    lmlist = detector.findPosition(img)
    if len(lmlist) != 0:
        print(lmlist)
    # FPS
    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
    # 表示
    cv2.imshow("Image", img)
    k = cv2.waitKey(1)
    if k == 27:
        break
cv2.destroyAllWindows()
