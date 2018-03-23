import glob
import numpy as np
from keras.models import load_model
import cv2
model = load_model('model.h5')
notburgers = glob.glob("data/validation/notburgers/notburger*.png")
notburgers.sort()
burgers = glob.glob("data/validation/burgers/burger*.png")
burgers.sort()

for i in range(len(notburgers)):
  img = cv2.imread(notburgers[i])
  img = np.reshape(img,[1,72,120,3])
  print i, model.predict_classes(img)
for i in range(len(burgers)):
  img = cv2.imread(burgers[i])
  img = np.reshape(img,[1,72,120,3])
  print i, model.predict_classes(img)
