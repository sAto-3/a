import cv2
import mediapipe as mp
import time
import sys


class handDetectior():
    def __init__(self, mode=False, MaxHands=2, detectonCon=0.5, trackCon=0.5):
        #class内変数selfに諸値を代入してclass上で使えるようにしておく
        self.mode = mode
        self.maxHands = MaxHands
        self.detectionCon = detectonCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # BGR>RGB
        self.results = self.hands.process(imgRGB)
        # print(self.results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myhand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                # print(id, cx, cy)
                lmlist.append([id, cx, cy])
                # if id ==0:
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                    cv2.putText(img, str(id), (cx, cy),
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
        return lmlist


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        #
        print("Error:カメラが接続されていません！！")
        sys.exit()
    detector = handDetectior()
    while True:
        # 画像の読み込み
        success, img = cap.read()
        # print(success)
        img = detector.findHands(img)
        #手の情報リストlmlistを取得
        lmlist = detector.findPosition(img)
        if len(lmlist) != 0:
            print(lmlist[4])#lmlistを表示
        # FPSを表示
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
        # 表示
        cv2.imshow("Image", img)
        k = cv2.waitKey(1)
        if k == 27:
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
