import cv2

for i in range(5):
    img = cv2.imread('../input/img' + str(i+1) + '.jpg', 0)
    img2 = cv2.resize(img, (256, 256))
    cv2.imwrite('output/img' + str(i+1) + '.jpg', img2)

