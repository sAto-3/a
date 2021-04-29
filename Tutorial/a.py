# OpenCVを使って画像の表示を行う

# python3用のOpenCvライブラリcv2をimprot
import cv2
# 画像"img_light.jpg"を読み込み　0:グレースケール
bgr = cv2.imread('img_lights.jpg', 1)

bgr[:,:,0]=0
# 画像を題名"image"で表示
cv2.imshow("image", bgr)
# キーボード入力待ち(0:無制限 0<:指定したフレーム数)
cv2.waitKey(0)
# ウィンドウをすべて閉じる
cv2.destroyAllWindows()
