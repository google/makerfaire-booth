import cv2

img1 = cv2.imread('patty_rotated.png')          # queryImage
surf = cv2.xfeatures2d.SURF_create(400)
surf.setUpright(True)

kp1, des1 = surf.detectAndCompute(img1, None)
out = cv2.drawKeypoints(img1, kp1, None)
cv2.imshow('img', out)
# cv2.waitKey(0)

img1 = cv2.imread('patty.png')          # queryImage
surf = cv2.xfeatures2d.SURF_create(400)
surf.setUpright(True)

kp1, des1 = surf.detectAndCompute(img1, None)
out = cv2.drawKeypoints(img1, kp1, None)
cv2.imshow('img2', out)
cv2.waitKey(0)
