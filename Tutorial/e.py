# Canny法を用いた輪郭検出
# カメラを使った画面表示
import cv2

# VideoCapture オブジェクト(0~カメラ番号)
capture = cv2.VideoCapture(0)

while(True):
    # カメラから画像を読み込む
    ret, frame = capture.read()

    # 具体的な動作
    edges = cv2.Canny(frame, 100, 100)

    # 画像を表示
    cv2.imshow("frame", frame)
    cv2.imshow("edges", edges)
    # qが押されたら停止
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
# カメラの動作を停止
capture.release()
cv2.destroyAllWindows()
