from skimage.feature import CENSURE
from skimage.color import rgb2gray
from skimage.color import rgb2gray
from skimage.io import imread

import matplotlib.pyplot as plt

img1 = rgb2gray(imread('/home/dek/makerfaire-booth/2018/burger/experimental/dek/train_object_detector/images/bottombun.0.00.27.34.-24.61.0.81.png'))
img2 = rgb2gray(imread('/home/dek/makerfaire-booth/2018/burger/experimental/dek/train_object_detector/images/bottombun.0.02.-49.74.26.68.1.83.png'))

detector = CENSURE()

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

detector.detect(img1)
ax[0].imshow(img1, cmap=plt.cm.gray)
ax[0].scatter(detector.keypoints[:, 1], detector.keypoints[:, 0],
              2 ** detector.scales, facecolors='none', edgecolors='r')
ax[0].set_title("Original Image")

detector.detect(img2)

ax[1].imshow(img2, cmap=plt.cm.gray)
ax[1].scatter(detector.keypoints[:, 1], detector.keypoints[:, 0],
              2 ** detector.scales, facecolors='none', edgecolors='r')
ax[1].set_title('Transformed Image')

for a in ax:
    a.axis('off')

plt.tight_layout()
plt.show()
