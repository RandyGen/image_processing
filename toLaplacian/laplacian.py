import cv2
import numpy as np


for i in range(5):
    # 入力画像を読み込み
    img = cv2.imread("../to256_grey/output/img" + str(i+1) + ".jpg")

    # カーネル（輪郭検出用）
    kernel = np.array([[1, 1,  1],
                    [1, -8, 1],
                    [1, 1,  1]])

    # カーネルサイズ
    m, n = kernel.shape

    # 畳み込み演算をしない領域の幅
    d = int((m-1)/2)
    h, w = img.shape[0], img.shape[1]

    # 出力画像用の配列（要素は全て0）
    dst = np.zeros((h, w))

    for y in range(d, h - d):
        for x in range(d, w - d):
            # 畳み込み演算
            dst[y][x] = np.sum(img[y-d:y+d+1, x-d:x+d+1]*kernel)

    # 結果を出力
    cv2.imwrite("output/lap" + str(i+1) + ".jpg", dst)