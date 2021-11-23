# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math
from tqdm import tqdm
import sys

def mk_conf(args):
    return {
        "img": "../dataset/" + str(args[1]),
        "method": str(args[2]),
        "magnification": float(args[3]),
        "angle": float(args[4])
    }
4
def dataloader(img_path):
    img = cv2.imread(img_path)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(f"\nimage loaded\n")
    return gray_img

def processing(img, config):
    if config['method'] == "bilinear":
        return bilinear(img, int(img.shape[1]*config['magnification']), int(img.shape[0]*config['magnification']))
    elif config['method'] == "nearest":
        return nearest(img, int(img.shape[1]*config['magnification']), int(img.shape[0]*config['magnification']))
    elif config['method'] == "affine":
        return rotation(img, config["magnification"], config['angle'])
    else:
        raise ValueError

# バイリニア補間法でリサイズ
def bilinear(src, hd, wd):
    h, w = src.shape[0], src.shape[1]
    dst = np.empty((hd, wd))
    print(f"originl image size: {src.shape}\n")
    # 拡大率を計算(拡大縮小画像/原画像)
    ax = wd / float(w)
    ay = hd / float(h)

    # バイリニア補間法
    for yd in tqdm(range(0, hd)): # 拡大縮小画像のy軸
        for xd in range(0, wd): # 拡大縮小画像のx軸
            x, y = xd/ax, yd/ay # 参照している拡大縮小画像のピクセル/拡大率
            ox, oy = int(x), int(y) # 上記の値の丸め込み

            # 存在しない座標の処理
            if ox > w - 2:
                ox = w - 2
            if oy > h - 2:
                oy = h - 2

            # 重みの計算
            # 参照している拡大縮小画像のピクセル/拡大率 - 上記の値の丸め込み
            dx = x - ox
            dy = y - oy

            # 出力画像の画素値を計算
            # 重みを加えることで同じ4近傍の参照でも出力の輝度が異なる
            dst[yd][xd] = (1 - dx) * (1-dy) * src[oy][ox] + dx * (1-dy) * \
                src[oy][ox+1] + (1-dx) * dy * src[oy][ox+1] + \
                dx * dy * src[oy+1][ox+1]

    print("\nresized :-)")
    print(f"\nfixed image size: {dst.shape}\n")

    return dst

# 最近傍補間法でリサイズ
def nearest(src, h, w):
    hi, wi = src.shape[0], src.shape[1]
    dst = np.empty((h,w))
    print(f"originl image size: {src.shape}\n")

    # 拡大率を計算
    ax = w / float(wi)
    ay = h / float(hi)

    # 最近傍補間
    for y in tqdm(range(0, h)):
        for x in range(0, w):
            xi, yi = int(round(x/ax)), int(round(y/ay))
            # 存在しない座標の処理
            if xi > wi -1: xi = wi -1
            if yi > hi -1: yi = hi -1

            dst[y][x] = src[yi][xi]

    print("\nresized :-)")
    print(f"\nfixed image size: {dst.shape}")

    return dst

# アフィン変換による回転
def rotation(src, magnification, theta):
    h, w = src.shape[0], src.shape[1]
    dst = np.zeros((h, w))
    print(f"originl image size: {src.shape}\n")

    cos = magnification*math.cos(math.radians(theta))
    sin = magnification*math.sin(math.radians(theta))
    center_x = w/2
    center_y = h/2

    # 回転行列
    rotate_matrix = np.array(
                [[cos, -sin, center_x-center_x*cos+center_y*sin],
                [sin, cos, center_y-center_x*sin-center_y*cos],
                [0, 0, 1]
                ])

    # 回転
    for yd in tqdm(range(0, h)): # 画像のy軸
        for xd in range(0, w): # 画像のx軸
            rotate_xy = rotate_matrix @ np.array([xd, yd, 1]) # 今の座標と回転行列の積 -> 回転後の座標を求める
            if 0 <= int(rotate_xy[0]) < w and 0 <= int(rotate_xy[1]) < h:
                dst[yd][xd] = src[int(rotate_xy[1])][int(rotate_xy[0])]

    print(f"\nfixed image size: {dst.shape}")
    print(f"rotated :-)\n")

    return dst

def output(img):
    cv2.imwrite("../dataset/result.png", img)
    print(f"fin!\n")

def main():
    config = mk_conf(sys.argv)
    img = dataloader(config['img'])
    dst = processing(img, config)
    output(dst)


if __name__ == "__main__":
    main()