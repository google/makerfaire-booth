import time
import numpy as np
import os
import sys
from object_detector import ObjectDetector
import cv2

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--movie", type=str, default="movie.mp4", help="Movie file to run prediction on")
parser.add_argument("--write_output", type=bool, default=False, help="Whether to write output")
parser.add_argument("--output_dir", type=str, default="movie", help="Directory to write output to")
args = parser.parse_args()

from layers import layers

if not os.path.exists(args.movie):
  print("Movie file %s missing" % args.movie)
  sys.exit(1)

cam = cv2.VideoCapture(args.movie)
width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
objdet = ObjectDetector()


counter = 0

ret, img = cam.read()
while ret == True:
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, _ = img.shape
    expand = np.expand_dims(img, axis=0)
    result = objdet.detect(expand)
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
    if cv2.waitKey(1) and ord('q'):
      break
    if args.write_output:
      cv2.imwrite(os.path.join(args.output_dir, "%05d.png" % counter), img)
    counter += 1
    ret, img = cam.read()
