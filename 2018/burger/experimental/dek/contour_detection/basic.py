import cv2
#reading the image
cam = cv2.VideoCapture(0)
width = long(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = long(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
while True:
    ret, image = cam.read()

    edged = cv2.Canny(image, 40, 200)

    #applying closing function 
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow("Closed", closed)

    #finding_contours 
    im2, contours, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
    cv2.imshow("Output", closed)
    cv2.waitKey(1)
