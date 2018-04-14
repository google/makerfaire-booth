import io
import cairo
import numpy
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
sys.path.insert(0, "../../../machine")
from burger_elements import BurgerElement
import rsvg
from PIL import Image
handles = {}
for layer in BurgerElement.__members__:
  if layer != 'empty':
    layer_name = "../../../assets/%s.svg" % layer
    handles[layer] = rsvg.Handle(layer_name)

def get_random_orientation():
    rot = numpy.random.uniform(-math.pi, math.pi)
    tx = numpy.random.uniform(-100, 100)
    ty = numpy.random.uniform(-100, 100)
    scale = numpy.random.uniform(0.75, 4)
    return rot, tx, ty, scale
  
def draw_example(layer, width, height, rot, tx, ty, scale, clear_background=True):
    img = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(img)
    handle = handles[layer]
    dims = handle.get_dimension_data()[2:]
    if clear_background:
        ctx.set_source_rgb (255,255,255)
        ctx.paint()
    
    ctx.translate(width/2 - dims[0]/2, height/2 - dims[1]/2)
    ctx.translate(dims[0]/2, dims[1]/2)

    ctx.translate(tx, ty)
    ctx.rotate(rot)
    ctx.scale(scale, scale)
    
    ctx.translate(-dims[0]/2, -dims[1]/2)
    handle.render_cairo(ctx)

    a = numpy.ndarray(shape=(width, height, 4), dtype=numpy.uint8, buffer=img.get_data())
    a = a[...,[2,1,0]]
    return a

def main():
    image_base_dir = '/home/dek/makerfaire-booth/2018/burger/experimental/dek/train_object_detector/decoded'
    canonical_dir = 'canonical'
    # template = os.path.join(image_base_dir, 'bottombun.0.00.27.34.-24.61.0.81.png')
    template = os.path.join(canonical_dir, 'patty.png')

    img1 = imread(template)
    print img1.shape, img1.dtype
    img1_gray = rgb2gray(img1)

    descriptor_extractor = ORB()

    descriptor_extractor.detect_and_extract(img1_gray)
    keypoints1 = descriptor_extractor.keypoints
    descriptors1 = descriptor_extractor.descriptors

    # g = glob.glob(os.path.join(image_base_dir, 'patty*.nobox.png'))
    # for moving in g:
    while True:
        rot, tx, ty, scale = get_random_orientation()
        # img2 = imread(moving)
        img2 = draw_example('patty', 256, 256, rot, tx, ty, scale)
        print img2.shape, img2.dtype
        img2_gray = rgb2gray(img2)

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
        img2_transformed = transform.warp(img2, model_robust.inverse)

        # tf = SimilarityTransform()
        # tf.estimate(src, dst)
        # n = os.path.basename(moving)
        # img2_transformed = transform.warp(img2, inverse_map=tf.inverse)


        fig, axes = plt.subplots(2, 2, figsize=(7, 6), sharex=True, sharey=True)
        ax = axes.ravel()


        ax[0].imshow(img1)
        ax[1].imshow(img2)
        ax[1].set_title("Template image")
        ax[2].imshow(img2_transformed)
        ax[2].set_title("Matched image")

        print scale
        # plt.gray()

        # ax = plt.gca()
        # plot_matches(ax, img1, img2, keypoints1, keypoints2, matches12)


        plt.show()
if __name__ == '__main__':
    main()
