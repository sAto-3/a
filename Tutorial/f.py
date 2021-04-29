import cv2
import numpy as np
# カメラを使った画面表示

# VideoCapture オブジェクト(0~カメラ番号)
capture = cv2.VideoCapture(0)
lower = np.array([0, 30, 80], dtype="uint8")
upper = np.array([20, 255, 255], dtype="uint8")
while(True):
    # カメラから画像を読み込む
    ret, frame = capture.read()

    hsvim = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # BGR>HSV

    skinRegionHSV = cv2.inRange(hsvim, lower, upper)
    blurred = cv2.blur(skinRegionHSV, (2, 2))
    ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = max(contours, key=lambda x: cv2.contourArea(x))
    cv2.drawContours(frame, [contours], -1, (255, 255, 0), 2)
    hull = cv2.convexHull(contours)
    cv2.drawContours(frame, [hull], -1, (0, 255, 255), 2)
    hull = cv2.convexHull(contours, returnPoints=False)
    defects = cv2.convexityDefects(contours, hull)
    if defects is not None:
        cnt = 0
    for i in range(defects.shape[0]):  # calculate the angle
        s, e, f, d = defects[i][0]
        start = tuple(contours[s][0])
        end = tuple(contours[e][0])
        far = tuple(contours[f][0])
        a = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
        b = np.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
        c = np.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
        angle = np.arccos((b ** 2 + c ** 2 - a ** 2) /
                          (2 * b * c))  # cosine theorem
        if angle <= np.pi / 2:  # angle less than 90 degree, treat as fingers
            cnt += 1
            cv2.circle(frame, far, 4, [0, 0, 255], -1)
    if cnt > 0:
        cnt = cnt + 1
    cv2.putText(frame, str(cnt), (0, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 0, 0), 2, cv2.LINE_AA)
    # 画像を表示
    cv2.imshow("frame", frame)
    # qが押されたら停止
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
# カメラの動作を停止
capture.release()
cv2.destroyAllWindows()
