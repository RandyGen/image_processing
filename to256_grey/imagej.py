import cv2

img = cv2.imread('img5.jpg', 0)
h = img.shape[0]
w = img.shape[1]
img2 = cv2.resize(img, (256, 256))
cv2.imwrite('img55.jpg', img2)

