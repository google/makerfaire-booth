import math
import signal                                    
signal.signal(signal.SIGINT, signal.SIG_DFL)
import os
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

image_base_dir = '/home/dek/makerfaire-booth/2018/burger/experimental/dek/train_object_detector/decoded'
canonical_dir = 'canonical'
# template = os.path.join(image_base_dir, 'bottombun.0.00.27.34.-24.61.0.81.png')
template = os.path.join(canonical_dir, 'patty.png')

img1 = imread(template)
img1_gray = rgb2gray(img1)

descriptor_extractor = ORB()

descriptor_extractor.detect_and_extract(img1_gray)
keypoints1 = descriptor_extractor.keypoints
descriptors1 = descriptor_extractor.descriptors

g = glob.glob(os.path.join(image_base_dir, 'patty*.nobox.png'))
for moving in g:
    img2 = imread(moving)
    img2_gray = rgb2gray(img2)

    descriptor_extractor.detect_and_extract(img2_gray)
    keypoints2 = descriptor_extractor.keypoints
    descriptors2 = descriptor_extractor.descriptors

    matches12 = match_descriptors(descriptors1, descriptors2, cross_check=True)

    src = keypoints2[matches12[:, 1]][:, ::-1]
    dst = keypoints1[matches12[:, 0]][:, ::-1]

    model_robust, inliers = \
        ransac((src, dst), SimilarityTransform,
               min_samples=4, residual_threshold=2)
    img2_transformed = transform.warp(img2, model_robust.inverse)
    
    # tf = SimilarityTransform()
    # tf.estimate(src, dst)
    # n = os.path.basename(moving)
    # img2_transformed = transform.warp(img2, inverse_map=tf.inverse)

    
    fig, axes = plt.subplots(2, 2, figsize=(7, 6), sharex=True, sharey=True)
    ax = axes.ravel()

    
    ax[0].imshow(img1)
    ax[1].imshow(img2)
    ax[1].set_title(os.path.basename(moving))
    ax[2].imshow(img2_transformed)
    ax[2].set_title("Matched image")

    # plt.gray()

    # ax = plt.gca()
    # plot_matches(ax, img1, img2, keypoints1, keypoints2, matches12)


    plt.show()
