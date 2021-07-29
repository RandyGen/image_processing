import cv2
import numpy as np


# 画像のリサイズ
def resize(img):
    return cv2.resize(img, (256, 256))


def laplacian(img):
    # カーネル（輪郭検出用）
    kernel = np.array([[1, 1,  1],
                    [1, -8, 1],
                    [1, 1,  1]])

    # カーネルサイズ
    m = kernel.shape[0]

    # 畳み込み演算をしない領域の幅
    d = int((m-1)/2)
    h, w = img.shape[0], img.shape[1]

    # 出力画像用の配列（要素は全て0）
    dst = np.zeros((h, w))

    for y in range(d, h - d):
        for x in range(d, w - d):
            # 畳み込み演算
            dst[y][x] = np.sum(img[y-d:y+d+1, x-d:x+d+1]*kernel)

    return dst


# 画像の二値化
def binarization(img, t=100):
    return np.where(img < t, 0, 255)


# ハフ変換
def hough(input):
    # 画素値255の部分の抽出
    y,x = np.where(input == 255)
    len_x = len(x)

    # 出力用
    result = np.zeros((256, 180))

    # シータの作成
    theta_do = np.arange(0, 180)
    theta_rad = np.deg2rad(theta_do)

    for i in range(len_x):
        for l in range(len(theta_do)):
            r = int(np.round((x[i] - 127)*np.cos(theta_rad[l]) + (-1*y[i] + 128)*np.sin(theta_rad[l]))) + 127
            if 0<=r<=255:
                result[r][l] += 1

    return result


# ハフ逆変換
def rehough(input, img):
    # 画素値255の部分の抽出
    r,theta_do= np.where(input==255)

    # シータの設定
    theta_rad=np.deg2rad(theta_do)

    # 変換部の算出/描画
    for i in range(len(r)):
        a = np.cos(theta_rad[i])
        b = np.sin(theta_rad[i])
        x0 = a * r[i]
        y0 = b * r[i]
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(img,(255-x1,y1),(255-x2,y2),(0,0,255),2)

    return img


def main():
    # 画像の読み込み/グレースケー化
    original_image = cv2.imread('../input/img2.jpg', 0)
    cv2.imwrite("output/original2.jpg", original_image)

    # 画像のリサイズ/エッジ検出/二値化
    image = resize(original_image)
    image = laplacian(image)
    image = binarization(image)
    cv2.imwrite("output/a2.jpg", image)

    # ハフ変換
    image = hough(image)
    cv2.imwrite("output/b2.jpg", image)

    # ハフ逆変換
    image = binarization(image, 60)
    image = rehough(image, original_image)
    cv2.imwrite("output/c2.jpg", image)


if __name__ == '__main__':
    main()  