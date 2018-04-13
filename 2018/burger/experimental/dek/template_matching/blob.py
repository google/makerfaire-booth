from skimage import transform
from skimage.transform import ProjectiveTransform, SimilarityTransform
from skimage.measure import ransac
from scipy.misc import imshow

import sys
import glob
from skimage import data
from skimage import transform as tf
from skimage.feature import (match_descriptors, corner_harris,
                             corner_peaks, ORB, plot_matches)
from skimage.color import rgb2gray
from skimage.io import imread
import matplotlib.pyplot as plt

img1 = rgb2gray(imread('/home/dek/makerfaire-booth/2018/burger/experimental/dek/train_object_detector/images/bottombun.0.00.27.34.-24.61.0.81.png'))
g = glob.glob('/home/dek/makerfaire-booth/2018/burger/experimental/dek/train_object_detector/images/bottombun*png')
for i in g:
    img2 = rgb2gray(imread(i))

    descriptor_extractor = ORB(n_keypoints=2000, n_scales=20)

    descriptor_extractor.detect_and_extract(img1)
    keypoints1 = descriptor_extractor.keypoints
    descriptors1 = descriptor_extractor.descriptors

    descriptor_extractor.detect_and_extract(img2)
    keypoints2 = descriptor_extractor.keypoints
    descriptors2 = descriptor_extractor.descriptors

    matches12 = match_descriptors(descriptors1, descriptors2, cross_check=True)

    src = keypoints2[matches12[:, 1]][:, ::-1]
    dst = keypoints1[matches12[:, 0]][:, ::-1]

    model_robust, inliers = \
        ransac((src, dst), ProjectiveTransform,
               min_samples=4, residual_threshold=2)
    
    tf = SimilarityTransform()
    tf.estimate(src, dst)
    result = transform.warp(img2, inverse_map=tf.inverse)

    imshow(result)
    # plt.gray()
    # ax = plt.gca()
    # plot_matches(ax, img1, img2, keypoints1, keypoints2, matches12)


    # plt.show()
