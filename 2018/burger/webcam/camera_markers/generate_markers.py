import cv2

aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_1000)
for i in range(5):
    img = cv2.aruco.drawMarker(aruco_dict, i, 1024)
    cv2.imwrite("test_marker.%d.jpg" % i, img)
