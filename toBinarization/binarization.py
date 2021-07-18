#-*- coding:utf-8 -*-
import cv2
import numpy as np


for i in range(5):
    # 入力画像を読み込み
    img = cv2.imread("../toLaplacian/output/lap" + str(i+1) + ".jpg")

    # 画像の高さと幅
    h, w = img.shape[0], img.shape[1]
    
    # 出力画像用の配列（要素は全て255）
    dst = np.empty((h,w))
    dst.fill(255)

    # 閾値
    t = 50

    for y in range(0, h):
        for x in range(0, w):
            # 閾値で二値化処理
            if img[x][y][0] < t:
                dst[x][y] = 0
            else:
                dst[x][y] = 255

    # 結果を出力
    cv2.imwrite("output/bina" + str(i+1) + ".jpg", dst)

