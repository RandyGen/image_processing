import numpy as np
import cv2
from scipy.fftpack import dct

img = cv2.imread('img55.jpg', 0)
d = dct(dct(img, axis=0, norm='ortho'), axis=1, norm='ortho')
d = 20 * np.log(np.abs(d))

cv2.imwrite('dct5.jpg', d)

