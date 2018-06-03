import time
import numpy as np
import os
import sys
from object_detector import ObjectDetector
import cv2

filename="/home/dek/VID_20180601_095421738.mp4"

from layers import layers

WIDTH=1080
HEIGHT=1920

# cam = cv2.VideoCapture(0)
# cam.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
cam = cv2.VideoCapture(filename)
width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
objdet = ObjectDetector()


counter = 0

ret, img = cam.read()
while ret == True:
    t0 = time.time()
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img = cv2.resize(img, None, fx=0.25, fy=0.25)
    h, w, _ = img.shape
    expand = np.expand_dims(img, axis=0)
    t1 = time.time()
    result = objdet.detect(expand)
    t2 = time.time()
    boxes = []
    for i in range(result['num_detections']):
        if result['detection_scores'][i] > 0.75:
            class_ = result['detection_classes'][i]
            box = result['detection_boxes'][i]
            score = result['detection_scores'][i]
            y1, x1 = int(box[0] * h), int(box[1] * w)
            y2, x2 = int(box[2] * h), int(box[3] * w)
            boxes.append((class_, score, x1, y1, x2, y2))

    for box in boxes:
        class_, score, x1, y1, x2, y2 = box
        w1 = x2-x1
        h1 = y2-y1
        cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2)
        cv2.putText(img, "%s: %5.2f" % (layers[class_-1], score), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow('image', img)
    cv2.waitKey(1)
    t3 = time.time()
    cv2.imwrite("movie/%05d.png" % counter, img)
    counter += 1
    ret, img = cam.read()
    t4 = time.time()
    print("%5.2f,%5.2f,%5.2f,%5.2f" % (t1-t0, t2-t1, t3-t2, t4-t3))

