import numpy as np
import cv2
from cv2 import aruco

# project cube or model
def render(bbox, img, obj):
    top_left = bbox[0][0][0], bbox[0][0][1]
    top_right = bbox[0][1][0], bbox[0][1][1]
    bottom_right = bbox[0][2][0], bbox[0][2][1]
    bottom_left = bbox[0][3][0], bbox[0][3][1]
    
    height, width, _, = obj.shape
    
    points1 = np.array([top_left, top_right, bottom_right, bottom_left])
    points2 = np.array([[0, 0], [width, 0], [width, height], [0, height]])
    
    matrix,_ = cv2.findHomography(points2, points1)
    img_out = cv2.warpPerspective(obj, matrix, (img.shape[1],img.shape[0]))
    cv2.fillConvexPoly(img, points1.astype(int), (0, 0, 0))
    
    img_out = img + img_out
    return img_out

# imaginea generata nu are in exterior un chenar alb,
# ceea ce face imposibila detectia markerului
def white_box(img):
    w,h = img.shape
    img_white = np.zeros((w+100,h+100), dtype=np.uint8)
    img_white.fill(255)
    img_white[50:w+50,50:h+50] = img
    
    return img_white


aruco_params =  aruco.DetectorParameters_create()
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

# genereaza un marker cu id-ul 2
img = aruco.drawMarker(aruco_dict, 2, 700)
img = white_box(img)
cv2.imwrite("marker.png", img)

# load image
obj = cv2.imread("image2.png")

video = cv2.VideoWriter('ex2_video.avi', cv2.VideoWriter_fourcc(*'3IVD'), 30, (640, 480))
# 30 fps, 3 secunde
frame_len  = 30 * 3
frame_it = 0

vid = cv2.VideoCapture(0)
while(frame_it < frame_len):
    ret, frame = vid.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)
    
    if( len(corners) != 0 and ids[0,0] == 2):
        frame = render(np.array(corners[0]),frame, obj)
 
    video.write(frame)
    frame_it += 1

video.release()
cv2.destroyAllWindows()
    
    
    
    
    