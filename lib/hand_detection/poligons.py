import cv2
import numpy as np
import pickle
from mapping_offtime import mirrored_result

map_file_path = "map.p"
countries_file_path= "countries.p"
cam_id = 0
width, height= 1920, 1080
# Open a connection to the webcam
cap = cv2.VideoCapture(cam_id) # For Webcam
# Set the width and height of the webcam frame
cap.set(3, width)
cap.set(4, height)



file_obj = open(map_file_path, 'rb')
map_points = pickle.load(file_obj)
file_obj.close()
print(f"Loaded map coordinates.", map_points)

while True:
    # Read a frame from the webcam
    success, img = cap.read()
    # Display the image with marked polygons
    cv2.imshow("Original Image", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()