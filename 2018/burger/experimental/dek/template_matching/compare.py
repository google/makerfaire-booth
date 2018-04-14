import time
import io
import cairo
import numpy
import math
import signal                                    
signal.signal(signal.SIGINT, signal.SIG_DFL)
import os
import skimage
from skimage import transform
from skimage.transform import ProjectiveTransform, SimilarityTransform
from skimage.measure import ransac, compare_ssim, compare_mse
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
sys.path.insert(0, "../../../machine")
from burger_elements import BurgerElement
import rsvg
from PIL import Image

WIDTH = 512
HEIGHT = 512

handles = {}
for layer in BurgerElement.__members__:
  if layer != 'empty':
    layer_name = "../../../assets/%s.svg" % layer
    handles[layer] = rsvg.Handle(layer_name)
  else:
    handles[layer] = None

def get_random_orientation():
    rot = numpy.random.uniform(-math.pi/4, math.pi/4)
    tx = numpy.random.uniform(-50, 50)
    ty = numpy.random.uniform(-50, 50)
    scale = numpy.random.uniform(2, 8)
    return rot, tx, ty, scale
  
def draw_example(layer, width, height, rot, tx, ty, scale, clear_background=True):
    img = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(img)
    handle = handles[layer]
    if handle:
      dims = handle.get_dimension_data()[2:]
    else:
      dims = (0,0)
    if clear_background:
        ctx.set_source_rgb (255,255,255)
        ctx.paint()
    
    ctx.translate(width/2 - dims[0]/2, height/2 - dims[1]/2)
    ctx.translate(dims[0]/2, dims[1]/2)

    ctx.translate(tx, ty)
    ctx.rotate(rot)
    ctx.scale(scale, scale)
    
    ctx.translate(-dims[0]/2, -dims[1]/2)
    if handle:
      handle.render_cairo(ctx)

    a = numpy.ndarray(shape=(width, height, 4), dtype=numpy.uint8, buffer=img.get_data())
    a = a[...,[2,1,0]]
    return a

def main():
    image_base_dir = '/home/dek/makerfaire-booth/2018/burger/experimental/dek/train_object_detector/decoded'
    canonical_dir = 'canonical'
    # template = os.path.join(image_base_dir, 'bottombun.0.00.27.34.-24.61.0.81.png')
    fig, axes = plt.subplots(7, 7, figsize=(7, 6), sharex=True, sharey=True)

    fig.delaxes(axes[0][0])

    ssims = numpy.zeros( (len(BurgerElement.__members__), len(BurgerElement.__members__)), dtype=float)
    mses = numpy.zeros( (len(BurgerElement.__members__), len(BurgerElement.__members__)), dtype=float)
                         
    for i, layer in enumerate(BurgerElement.__members__):
        template = os.path.join(canonical_dir, '%s.png' % layer)

        img1 = imread(template)
        # img1_padded = numpy.zeros( (WIDTH, HEIGHT,3), dtype=numpy.uint8)
        img1_padded = numpy.resize( [255,255,255], (WIDTH, HEIGHT, 3))
        s = img1.shape
        w = s[0]
        h = s[1]
        nb = img1_padded.shape[0]
        na = img1.shape[0]
        lower1 = (nb) // 2 - (na // 2)
        upper1 = (nb // 2) + (na // 2)
        nb = img1_padded.shape[1]
        na = img1.shape[1]
        lower2 = (nb) // 2 - (na // 2)
        upper2 = (nb // 2) + (na // 2)
        img1_padded[lower1:upper1, lower2:upper2] = img1
        img1_padded_float = img1_padded.astype(numpy.float64)/255.
        print img1_padded_float.shape
        img1_gray = rgb2gray(img1_padded_float)

        descriptor_extractor = ORB()

        try:
            descriptor_extractor.detect_and_extract(img1_gray)
        except RuntimeError:
            continue
        
        keypoints1 = descriptor_extractor.keypoints
        descriptors1 = descriptor_extractor.descriptors

        axes[i][0].imshow(img1_padded_float)
        axes[i][0].set_title("Template image")

        for j, layer2 in enumerate(BurgerElement.__members__):

            rot, tx, ty, scale = get_random_orientation()
            img2 = draw_example(layer2, WIDTH, HEIGHT, rot, tx, ty, scale)

            # match = os.path.join(canonical_dir, '%s.png' % layer2)
            # img2 = imread(match)

            img2_padded = numpy.resize( [255,255,255], (WIDTH, HEIGHT, 3))
            s = img2.shape
            img2_padded[:s[0], :s[1]] = img2
            img2_padded_float = img2_padded.astype(numpy.float64)/255.
            img2_gray = rgb2gray(img2_padded_float)

            try:
                descriptor_extractor.detect_and_extract(img2_gray)
            except RuntimeError:
                continue

            keypoints2 = descriptor_extractor.keypoints
            descriptors2 = descriptor_extractor.descriptors

            matches12 = match_descriptors(descriptors1, descriptors2, cross_check=True)

            src = keypoints2[matches12[:, 1]][:, ::-1]
            dst = keypoints1[matches12[:, 0]][:, ::-1]

            model_robust, inliers = \
                ransac((src, dst), SimilarityTransform,
                       min_samples=4, residual_threshold=2)
            if not model_robust:
                print "bad"
                continue
            img2_transformed = transform.warp(img2_padded_float, model_robust.inverse, mode='constant', cval=1)
            sub = img2_transformed - img1_padded_float
            ssim = compare_ssim(img2_transformed, img1_padded_float, win_size=5, multichannel=True)
            mse = compare_mse(img2_transformed, img1_padded_float)
            ssims[i,j] = ssim
            mses[i,j] = mse

            axes[0][j].imshow(img2_padded_float)
            axes[0][j].set_title("Match image")

            axes[i][j].imshow(img2_transformed)
            axes[i][j].set_title("Transformed image")
            axes[i][j].set_xlabel("SSIM: %9.4f MSE: %9.4f" % (ssim, mse))

        # ax = plt.gca()
        # plot_matches(ax, img1, img2, keypoints1, keypoints2, matches12)

    print ssims
    print numpy.argmax(ssims, axis=1)
    print numpy.argmin(mses, axis=1)
                       
    plt.show()
if __name__ == '__main__':
    main()
