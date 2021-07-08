from typing import ChainMap
import cv2
import mediapipe as mp
from google.protobuf.json_format import MessageToDict, MessageToJson
import time
import sys

import module


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class handDetectior():
    def __init__(self, mode=False, MaxHands=2, detectonCon=0.5, trackCon=0.5):
        # class内変数selfに諸値を代入してclass上で使えるようにしておく
        self.mode = mode
        self.maxHands = MaxHands
        self.detectionCon = detectonCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, drawLandmark=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # BGR>RGB
        self.results = self.hands.process(imgRGB)
        # print(self.results.multi_handedness)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if drawLandmark:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS)
                    # print(self.results.multi_handdeness.classification.label)
        return img

    def findPosition(self, img, drawPosition=False, Normalization=True):
        '''
        input  
            img：入力画像 
            drawPosition：画像に手の位置を描画するか（初期値False） 
            Normalization：手の座標を標準化するか 
        output 
            self.lmlist:送られた画像の手と手のランドマーク座標の情報[[[id,x,y,z,LR]]] 
                id：手のランドマークのid 
                x,y,z：手のランドマークの座標 
                LR：手の右左推定（0:右 1:左） 
            bbox:各手の大きさの最大・最小座標を返す[[xmin,ymin,xmax,ymax]] 
        '''
        # 初期化
        xlist = []
        ylist = []
        self.lmlist = []
        bbox = []
        if self.results.multi_handedness:
            # 各手ごとに取り出す
            for handNo, hand_handedness in enumerate(self.results.multi_handedness):
                # print(idx)
                # 手の右左情報の取得
                handedness_dict = MessageToDict(
                    hand_handedness)  # Message=>list
                # print(handedness_dict['classification'][0]['index'])
                HandLR = handedness_dict['classification'][0]['index']

                # 手の情報を入れる配列の準備
                xlist.append([])
                ylist.append([])
                self.lmlist.append([])
                bbox.append([])

                if self.results.multi_hand_landmarks:
                    # myhand = self.results.multi_hand_landmarks[handNo]
                    # print(myhand)
                    #
                    for i, hand in enumerate(self.results.multi_hand_landmarks):
                        # print(hand)
                        # 手のランドマークごとに取り出す
                        for id, lm in enumerate(hand.landmark):
                            # print(id, lm.z)
                            # print(lm.landmark[0].x)
                            # print(id, cx, cy)

                            cx, cy, cz = lm.x, lm.y, lm.z

                            # 画像の幅、高さで正規化する
                            if Normalization:
                                h, w, c = img.shape
                                cx, cy, cz = int(
                                    lm.x*w), int(lm.y*h), int(lm.z*w)

                            # 配列に入れる
                            xlist[handNo].append(cx)
                            ylist[handNo].append(cy)
                            self.lmlist[handNo].append(
                                [id, cx, cy, cz, HandLR])

                            # x,y座標を描画
                            if drawPosition:
                                # cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                                cv2.putText(img, str(id), (cx, cy),
                                            cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
                        # 配列bboxの生成
                        xmin, xmax = min(xlist[handNo]), max(xlist[handNo])
                        ymin, ymax = min(ylist[handNo]), max(ylist[handNo])
                        bbox[handNo] = xmin, ymin, xmax, ymax
        # self.lmlistとbboxで返す
        return self.lmlist, bbox

    def checkFinger(self):
        '''
        threepoint_angleをもちいて
        （改善：３次元ランドマーク座標からなるベクトルの角度を求める）
        親指：1,2,3
        人差し指：5,6,7
        中指：9,10,11
        薬指：13,14,15
        小指：17,18,19
        各指の距離を計算して指が閉じているか開いているかを01で検出する
        return
        '''
        # しきい値thread
        thread = [305, 300, 300, 300, 300]
        lmlist = self.lmlist
        ans = []
        # 各手ごとに行う
        for hand in range(len(lmlist)):
            rads = [0]*5
            # 第３関節は手の付け根との角度
            for id in range(1, 20, 4):
                # print(lmlist[hand][0][1:4])
                rads[(id-1)//4] += module.threepoint_angle(
                    lmlist[hand][0][1:4], lmlist[hand][id][1:4], lmlist[hand][id+1][1:4])
            # 第１・２関節は前後の関節との角度
            for id in range(2, 20, 4):
                rads[(id-1)//4] += module.threepoint_angle(
                    lmlist[hand][id-1][1:4], lmlist[hand][id][1:4], lmlist[hand][id+1][1:4])
            # print(rads)
            # 各指がしきい値以上なら手が開いていると判断
            for i in range(5):
                if rads[i] > thread[i]:
                    rads[i] = 1
                else:
                    rads[i] = 0
            ans.append(rads)

        # print("\r", rads)

        return ans

    # def checkFinger(self):
    #     '''
#         各指の距離を計算して指が閉じているか開いているかを01で検出する
#         return
#         '''
    #     lmlist = self.lmlist
    #     ans = [0]*5
    #     for id in range(1, 6):
    #             L1 = ((lmlist[id * 4][1] - lmlist[0][1]) ** 2 +
    #                 (lmlist[id * 4][2] - lmlist[0][2]) ** 2) ** 0.5
    #             L2 = ((lmlist[id * 4 - 2][1] - lmlist[0][1]) ** 2 +
    #                 (lmlist[id * 4 - 2][2] - lmlist[0][2]) ** 2) ** 0.5
    #             if L1 > L2:
    #                 ans[id-1] = 1

    #         return ans


def main():
    # メイン動作は終了時に指の位置を3次元散布図として出力する
    showIMG = []
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        #
        print("Error:カメラが接続されていません！！")
        sys.exit()

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    detector = handDetectior(MaxHands=2)
    while True:
        # 画像の読み込み
        success, img = cap.read()
        # print(success)
        img = detector.findHands(img)

        # 手の情報リストlmlistを取得
        lmlist, bbox = detector.findPosition(img)
        # print(len(lmlist))
        if len(lmlist) != 0:
            #     print(lmlist[0][4])  # lmlistを表示
            checkedlist = detector.checkFinger()
            # print(checkedlist)

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
        # Spaceキーで座標を登録
        elif k == 32:
            # 初期化
            showIMG = []
            # データの入力
            for hand in range(len(lmlist)):
                showIMG.append([])
                showIMG[hand].append([row[1] for row in lmlist[hand]])
                showIMG[hand].append([row[2] for row in lmlist[hand]])
                showIMG[hand].append([row[3] for row in lmlist[hand]])
            print("SAVED")
    # 保存した座標を表示
    if showIMG:
        # print(len(showIMG[0]), len(showIMG[0][0]))
        for id in range(len(showIMG[0][0])):
            if id % 4 == 0:
                ax.scatter(showIMG[0][0][id], showIMG[0][1]
                           [id], showIMG[0][2][id], color="#DD0000")
            elif id % 4 == 1:
                ax.scatter(showIMG[0][0][id], showIMG[0][1]
                           [id], showIMG[0][2][id], color="#AA4400")
            elif id % 4 == 2:
                ax.scatter(showIMG[0][0][id], showIMG[0][1]
                           [id], showIMG[0][2][id], color="#778800")
            elif id % 4 == 3:
                ax.scatter(showIMG[0][0][id], showIMG[0][1]
                           [id], showIMG[0][2][id], color="#33CC00")
        plt.show()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
