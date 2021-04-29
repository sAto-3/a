# OpenCVのCascade型分類器を使った顔検出をする
# Cascade型のファイル　は OpenCVのライブラリファイル上にあるため取得がメンドウ => ファイルを作ってそこに作成する
import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier(
    'cascadefiles\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(
    'cascadefiles\haarcascade_eye.xml')
grass_cascade = cv2.CascadeClassifier(
    'cascadefiles\haarcascade_eye_tree_eyeglasses.xml')

# VideoCapture オブジェクト(0~カメラ番号)
capture = cv2.VideoCapture(0)

while(True):
    # カメラから画像を読み込む
    ret, frame = capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    size = frame.shape[:2][::-1]
    # 画像を拡大したあと縮小してモザイク画像を作成する
    resize = cv2.resize(frame, (size[0]/10, size[1]/10))
    mozic = cv2.resize(resize, size, interpolation=cv2.INTER_NEAREST)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # roi_gray = gray[y:y+h, x:x+w]
        # roi_color = frame[y:y+h, x:x+w]
        # 目検知
        # eyes = eye_cascade.detectMultiScale(roi_gray)
        # for (ex, ey, ew, eh) in eyes:
        #     cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
        # 目検知（メガネ装着）
        # grasses = grass_cascade.detectMultiScale(roi_gray)
        # for (gx, gy, gw, gh) in grasses:
        #     cv2.rectangle(roi_color, (gx, gy), (gx+gw, gy+gh), (0, 0, 255), 2)
        # モザイク化
        frame[y:y+h][x:x+w] = mozic[y:y+h][x:x+w]

    # 画像を表示
    cv2.imshow("frame", frame)
    # qが押されたら停止
    if cv2.waitKey(1) & 0xff == ord("q"):
        break

# カメラの動作を停止 ウィンドウを閉じる
capture.release()
cv2.destroyAllWindows()
