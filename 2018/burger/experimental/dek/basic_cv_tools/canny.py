from PyQt5 import QtGui
import cv2

def canny(img):
    edged = cv2.Canny(img, 40, 200)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    im2, contours, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours):
        c = contours[0]
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)
        cv2.drawContours(img, [approx], -1, (0, 255, 0), 1)

    w, h, _ = img.shape
    return QtGui.QImage(img.data, h, w, QtGui.QImage.Format_RGB888)

