import pickle
from unittest import result
import cv2
import numpy as np

# Load previously defined Regions of Interest (ROIs) polygons from a file



fileObj = open("lib/hand_detection/rectangles.p", "rb")
polygons = pickle.load(fileObj)  
fileObj.close()




# Set the width and height of the webcam frame
width, height = 1080,1920

# Open a connection to the webcam
cam_id = 0
cap = cv2.VideoCapture(cam_id)  # For Webcam
cap.set(4, width)
cap.set(3, height)




# Function to warp image based on map points
def warp_image(img):
    # Get the points
    fileObj = open("lib/hand_detection/map.p", "rb")
    points = pickle.load(fileObj)  
    fileObj.close()

    # Explicitly convert the points to type numpy.float32
    points = points.astype(np.float32)

    # Compute the perspective transform matrix
    M = cv2.getPerspectiveTransform(points, np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32))

    # Apply the perspective transform
    result = cv2.warpPerspective(img, M, ( height,width))
    cv2.imshow("Transformed Image", cv2.resize(result, (600, 900)))
    
    # Rotate the result to the right
    #result = cv2.rotate(result, cv2.ROTATE_90_CLOCKWISE)
    #mirrored_result = cv2.flip(result, 1)

    # Display the result
    
    return result, M

# Function to handle mouse events (used to mark points for polygons)






while True: 
    # Read a frame from the webcam
    success, img = cap.read()
    imgWarped, _ = warp_image(img)

    key = cv2.waitKey(1)




    # If the "q" key is pressed, save the polygons and exit the loop
    if key == ord("q"):
        break

    overlay = imgWarped.copy()
    # Draw the collected polygons on the image
    for polygon, name in polygons:
        cv2.polylines(imgWarped, [np.array(polygon)], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.fillPoly(overlay, [np.array(polygon)], (0, 255, 0))

    cv2.addWeighted(overlay, 0.35, imgWarped, 0.65, 0, imgWarped)

    # Display the image with marked polygons
    cv2.imshow("Warped Image", cv2.flip(imgWarped, 1))
    cv2.imshow("Original Image", img)
# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
