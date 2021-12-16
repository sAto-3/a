import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont


def pil2cv(imgPIL):
    # imgCV_RGB = np.array(imgPIL, dtype = np.uint8)
    imgCV_BGR = np.array(imgPIL)[:, :, ::-1]
    return imgCV_BGR


def cv2pil(imgCV):
    imgCV_RGB = imgCV[:, :, ::-1]
    imgPIL = Image.fromarray(imgCV_RGB)
    return imgPIL

# 左下をorgとして設定


def cv2_putText_4(img, text, org, fontFace, fontScale, color):
    """
    文字を表示する関数 org:左下
    img:表示する画像
    text:表示するテキスト
    org:表示する位置
    fontFace:文字のフォント
    fontScale:文字の大きさ
    color:文字の色
    """

    x, y = org
    height, width, dim = img.shape
    fontPIL = ImageFont.truetype(font=fontFace, size=fontScale)
    dummy_draw = ImageDraw.Draw(Image.new("RGB", (0, 0)))
    w, h = dummy_draw.textsize(text, font=fontPIL)
    if 0 < x+w < width and 0 < y-h < height:
        imgPIL = Image.fromarray(img[y - h: y, x: x + w, :])
        draw = ImageDraw.Draw(imgPIL)
        draw.text(xy=(0, 0), text=text, fill=color, font=fontPIL)
        img[y - h: y, x: x + w, :] = np.array(imgPIL, dtype=np.uint8)
    return img


def cv2_putText_5(img, text, org, fontFace, fontScale, color):
    """
    文字を表示する関数 org:中心
    img:表示する画像
    text:表示するテキスト
    org:表示する位置
    fontFace:文字のフォント
    fontScale:文字の大きさ
    color:文字の色
    """
    if text == "" and text == " ":
        return False
    x, y = org
    height, width, dim = img.shape
    fontPIL = ImageFont.truetype(font=fontFace, size=fontScale)
    dummy_draw = ImageDraw.Draw(Image.new("RGB", (0, 0)))
    w, h = dummy_draw.textsize(text, font=fontPIL)
    if 0 < x - w/2 < width and 0 < x + w/2 < width and 0 < y - h/2 < height and 0 < y + h/2 < height:
        imgPIL = Image.fromarray(img[int(y - h/2): int(y + h/2), int(x - w/2): int(x + w/2), :])
        draw = ImageDraw.Draw(imgPIL)
        draw.text(xy=(0, 0), text=text, fill=color, font=fontPIL)
        img[int(y - h/2): int(y + h/2), int(x - w/2): int(x + w/2), :] = np.array(imgPIL, dtype=np.uint8)
        return img
    else:
        return False  # 文字が範囲外


def cv2_putText_6(img, text, org, fontFace, fontScale, color):
    """
    文字を表示する関数 org:左上
    img:表示する画像
    text:表示するテキスト
    org:表示する位置
    fontFace:文字のフォント
    fontScale:文字の大きさ
    color:文字の色
    """
    if text == "" and text == " ":
        return False
    x, y = org
    height, width, dim = img.shape
    fontPIL = ImageFont.truetype(font=fontFace, size=fontScale)
    dummy_draw = ImageDraw.Draw(Image.new("RGB", (0, 0)))
    w, h = dummy_draw.textsize(text, font=fontPIL)
    if 0 < x < width and 0 < x + w < width and 0 < y < height and 0 < y + h < height:
        imgPIL = Image.fromarray(img[y: y + h, x: x + w, :])
        draw = ImageDraw.Draw(imgPIL)
        draw.text(xy=(0, 0), text=text, fill=color, font=fontPIL)
        img[y: y + h, x: x + w, :] = np.array(imgPIL, dtype=np.uint8)
        return img
    else:
        return False  # 文字が範囲外


def threepoint_angle(p1, p2, p3):
    a = np.array(p1)
    b = np.array(p2)
    c = np.array(p3)
    vec_ba = a - b
    vec_bc = c - b

    length_vec_ba = np.linalg.norm(vec_ba)
    length_vec_bc = np.linalg.norm(vec_bc)

    inner_product = np.inner(vec_ba, vec_bc)

    cos = inner_product / (length_vec_ba * length_vec_bc)
    rad = np.arccos(cos)
    degree = np.rad2deg(rad)

    return degree
