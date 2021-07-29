import cv2
import numpy as np
from matplotlib import pyplot as plt


for i in range(1):
    # 入力画像を読み込み
    img = cv2.imread('../toHough/output/ho1.jpg', 0)

    theta,r= np.where(img==0)
    len_r=len(r)
    tmp = np.zeros(256)
    result_x, result_y = np.empty(0), np.empty(0)
    len_result = len(tmp)

    for i in range(len_r):
        for l in range(len(theta)):
            for x in range(len_result):
                y = int(np.round(-1*np.cos(theta[l])/np.sin(theta[l])*x+r[i]/np.sin(theta[l])))
                tmp[x] = -y
            result_x = np.append(result_y, tmp)

            for y in range(len_result):
                x = int(np.round(-1*np.sin(theta[l])/np.cos(theta[l])*y+r[i]/np.cos(theta[l])))
                tmp[y] = -x
            result_y = np.append(result_x, tmp)

    result = result_x + result_y
    result = np.where(result<50)


    cv2.imwrite('output/rehough.jpg',result)