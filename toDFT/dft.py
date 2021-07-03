import numpy as np
import cv2
 

img = cv2.imread('img55.jpg', 0)
f = np.fft.fft2(img)
f_shift = np.fft.fftshift(f)
dft = 20 * np.log(np.abs(f_shift))

cv2.imwrite('dft5.jpg', dft)

