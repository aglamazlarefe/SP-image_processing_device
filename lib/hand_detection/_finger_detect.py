"""
The provided script is an advanced interactive application that combines hand tracking and image processing to create an educational game using a digital map. It allows users to answer geography-related questions by selecting countries on the map with hand gestures. Here's a breakdown of its functionality and the libraries used:
 
Functionality:
Map Interaction: The script uses a digital map where users can interact with different countries. It detects hand movements to select countries on the map.
Question-Answer Game: Users answer geography questions by pointing at countries on the map. The script checks if the selected country is the correct answer.
Image Warping: It warps the webcam feed to align with the map, allowing accurate selection of countries.
Hand Tracking: Utilizes hand gesture recognition to detect user interaction with the map.
Overlay Creation: Generates an overlay image to highlight selected countries and display game-related information.
Score Tracking: Keeps track of the user's score based on correct answers.
 
Libraries:
pickle: For loading serialized data (map points and country polygons).
cv2 (OpenCV): For image processing and computer vision tasks.
cvzone: A higher-level library built on top of OpenCV, used here for hand tracking and overlay text.
numpy (NumPy): For numerical operations, especially in image manipulation.
HandDetector from cvzone: For detecting and tracking hand movements.
FaceDetector from cvzone: Although imported, it's not used in the script. It's typically for face detection tasks.
 
Usage:
The script is run in a Python environment with a webcam.
Users interact with the map by moving their hands in front of the webcam to select countries.
The application poses questions, and users respond by pointing at the map.
The script provides feedback on the answers and keeps a score.
 
Note:
The script requires pre-processed data files for map points and country polygons.
It's designed for educational purposes, offering an interactive way to learn geography.
 
**Author:** Murtaza Hassan
**Website:** www.computervision.zone
 
"""
# Import necessary libraries
from calendar import c
import pickle  # Pickle library for serializing Python objects
import cv2  # OpenCV library for computer vision tasks
import cvzone
import numpy as np  # NumPy library for numerical operations
from cvzone.HandTrackingModule import HandDetector
import time
######################################
cam_id = 0
width, height = 1080,1920
map_file_path = "lib/hand_detection/map.p"
countries_file_path = "lib/hand_detection/rectangles.p"
######################################

file_obj = open(map_file_path, 'rb')
map_points = pickle.load(file_obj)
file_obj.close()
print(f"Loaded map coordinates.")

# Load previously defined Regions of Interest (ROIs) polygons from a file

file_obj = open(countries_file_path, 'rb')
polygons = pickle.load(file_obj)
print(polygons)
file_obj.close()
print(f"Loaded {len(polygons)} countries.")





# Open a connection to the webcam
cap = cv2.VideoCapture(cam_id)  # For Webcam
# Set the width and height of the webcam frame
cap.set(4, width)
cap.set(3, height)
# Counter to keep track of how many polygons have been created
counter = 0

# Initialize the HandDetector class with the given parameters
detector = HandDetector(staticMode=False,maxHands=1,modelComplexity=1,detectionCon=0.5,minTrackCon=0.5)

selected_country = None
country_entry_times = {}
start_counter=False
answer_color= (0,0,255)



def warp_image(img, points, size=[1920, 1080]):
    """
    Warp the input image based on the provided points to create a top-down view.

    Parameters:
    - img: Input image.
    - points: List of four points representing the region to be warped.
    - size: Size of the output image.

    Returns:
    - imgOutput: Warped image.
    - matrix: Transformation matrix.
    """
    # Convert points to NumPy array
   
    # Get the points
    

   
    # Explicitly convert the points to type numpy.float32
    points = points.astype(np.float32)

    # Compute the perspective transform matrix
    matrix = cv2.getPerspectiveTransform(points, np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32))

    # Apply the perspective transform
    imgOutput = cv2.warpPerspective(img, matrix, (height,width))
   
    
    # Rotate the result to the right
    #result = cv2.rotate(result, cv2.ROTATE_90_CLOCKWISE)
    #mirrored_result = cv2.flip(result, 1)

    # Display the result
    

    return imgOutput, matrix



def inverse_warp_image(img, imgOverlay, map_points):
    """
    Inverse warp an overlay image onto the original image using provided map points.
 
    Parameters:
    - img: Original image.
    - imgOverlay: Overlay image to be warped.
    - map_points: List of four points representing the region on the map.
 
    Returns:
    - result: Combined image with the overlay applied.
    """
    # Convert map_points to NumPy array
    h, w, _ = img.shape
    overlay_warped = np.zeros((h, w, 3), dtype=np.uint8)
 
    pts = np.array(map_points, dtype=np.float32)
    pts = pts.reshape(-1, 1, 2)
 
    overlay_pts = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype=np.float32)
    overlay_pts = overlay_pts.reshape(-1, 1, 2)
 
    matrix = cv2.getPerspectiveTransform(overlay_pts, pts)
    cv2.warpPerspective(imgOverlay, matrix, (w, h), overlay_warped, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)
 
    imgOverlayFinal = cv2.addWeighted(img, 0.7, overlay_warped, 0.3, 0)
    return imgOverlayFinal
    

    






def warp_single_point(point, matrix):
    """
    Warp a single point using the provided perspective transformation matrix.
 
    Parameters:
    - point: Coordinates of the point to be warped.
    - matrix: Perspective transformation matrix.
 
    Returns:
    - point_warped: Warped coordinates of the point.
    """
    # Convert the point to homogeneous coordinates
    point_homogeneous = np.array([[point[0], point[1], 1]], dtype=np.float32)
 
    # Apply the perspective transformation to the point
    point_homogeneous_transformed = np.dot(matrix, point_homogeneous.T).T
 
    # Convert back to non-homogeneous coordinates
    point_warped = point_homogeneous_transformed[0, :2] / point_homogeneous_transformed[0, 2]
 
    return point_warped
 
 
def get_finger_location(img,imgWarped):
    """
    Get the location of the index finger tip in the warped image.
 
    Parameters:
    - img: Original
 
 image.
 
    Returns:
    - warped_point: Coordinates of the index finger tip in the warped image.
    """
    # Find hands in the current frame
    hands, img = detector.findHands(img, draw=False, flipType=True)
    # Check if any hands are detected
    if hands:
        # Information for the first hand detected
        hand1 = hands[0]  # Get the first hand detected
        indexFinger = hand1["lmList"][8][0:2]  # List of 21 landmarks for the first hand
        # cv2.circle(img,indexFinger,5,(255,0,255),cv2.FILLED)
        warped_point = warp_single_point(indexFinger, matrix)
        warped_point = int(warped_point[0]), int(warped_point[1])
        cv2.circle(imgWarped, warped_point, 5, (255, 0, 0), cv2.FILLED)
    else:
        warped_point = None
 
    return warped_point
 

 
 
def create_overlay_image(polygons, warped_point, imgOverlay):
    """
    Create an overlay image with marked polygons based on the warped finger location.
 
    Parameters:
    - polygons: List of polygons representing countries.
    - warped_point: Coordinates of the index finger tip in the warped image.
    - imgOverlay: Overlay image to be marked.
 
    Returns:
    - imgOverlay: Overlay image with marked polygons.
    """
 
    country_selected = None
    # Set the duration threshold for making a country green
    green_duration_threshold = 2.0
    # for polygon, name in polygons:
    #     polygon_np = np.array(polygon, np.int32).reshape((-1, 1, 2))
    #     result = cv2.pointPolygonTest(polygon_np, warped_point, False)
    #     if result >= 0:
 
    #         # If the country is not in the dictionary, add it with the current time
    #         if name not in country_entry_times:
    #             country_entry_times[name] = time.time()
 
    #         # Calculate the time the finger has spent in the country
    #         time_in_country = time.time() - country_entry_times[name]
 
    #         # If the time is greater than the threshold, make the country green
    #         if time_in_country >= green_duration_threshold:
    #             color = (0, 255, 0)  # Green color
    #             country_selected = name
    #         else:
    #             country_selected = None
    #             color = (255, 0, 255)  # Blue color
    #             # Draw an arc around the finger point based on elapsed time
    #             angle = int((time_in_country / green_duration_threshold) * 360)
    #             cv2.ellipse(imgOverlay, (warped_point[0], warped_point[1] - 100),
    #                         (50, 50), 0, 0, angle, color,
    #                         thickness=-1)
 
    #         cv2.polylines(imgOverlay, [np.array(polygon)], isClosed=True, color=color, thickness=2)
    #         cv2.fillPoly(imgOverlay, [np.array(polygon)], color)
    #         cvzone.putTextRect(imgOverlay, name, tuple(polygon[0][0]), scale=1, thickness=1)
            
    
    
    return imgOverlay, country_selected
 

 
while True:
    # Read a frame from the webcam
    success, img = cap.read()
    imgWarped, matrix = warp_image(img, map_points)
    imgOutput = img.copy()
 
    # Find the hand and its landmarks
    warped_point = get_finger_location(img,imgWarped)
 
    h, w, _ = imgWarped.shape
    imgOverlay = np.zeros((h, w, 3), dtype=np.uint8)
    for polygon, name in polygons:
        cv2.polylines(imgOverlay, [np.array(polygon)], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.fillPoly(imgOverlay, [np.array(polygon)], (0, 255, 0))
 
    selected_country = None
    if warped_point:
        imgOverlay, selected_country = create_overlay_image(polygons, warped_point, imgOverlay)
        imgOutput = inverse_warp_image(img, imgOverlay, map_points)
 
 
    # Display the current question
    
 
 
    # imgStacked = cvzone.stackImages([img, imgWarped,imgOutput,imgOverlay], 2, 0.3)
    # cv2.imshow("Stacked Image", imgStacked)
        
    key = cv2.waitKey(1)




    # If the "q" key is pressed, save the polygons and exit the loop
    if key == ord("q"):
        break
 
    cv2.imshow("Warped Image", imgWarped)
 
    #cv2.imshow("Output Image", imgOutput)
    cv2.imshow("overlay Image", imgOverlay)
    key = cv2.waitKey(1)