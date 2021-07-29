import cv2
import numpy as np
from matplotlib import pyplot as plt


for i in range(1):
    # 入力画像を読み込み
    img = cv2.imread('../toBinarization/output/bina1.jpg', 0)

    y,x= np.where(img==255)
    len_x=len(x)
    x=x-128
    y=128-y
    B=np.zeros((256, 180))
    theta_do=np.arange(0, 180)
    theta_rad=np.deg2rad(theta_do)

    for i in range(len_x):
        for l in range(len(theta_do)):
            r=int(np.round(x[i]*np.cos(theta_rad[l])+y[i]*np.sin(theta_rad[l])))
            B[128-r][l]+=1


    cv2.imwrite('output/hou2.jpg',B)