import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import pickle  # Pickle library for serializing Python objects
import cv2  # OpenCV library for computer vision tasks
import cvzone
import numpy as np  # NumPy library for numerical operations
from cvzone.HandTrackingModule import HandDetector
import time
from lib.hand_detection.pdf import write_to_pdf

#from pdf import write_to_pdf


# Örnek kullanım

# pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

button_x, button_y, button_width, button_height = 11, 11, 75, 35
button_text = "Exit"
exit_flag = False


######################################
cam_id = 0
width, height = 1080,1920
map_file_path = "lib/hand_detection/map.p"
countries_file_path = "lib/hand_detection/rectangles.p"
######################################
polygons = []
file_obj = open(map_file_path, 'rb')
map_points = pickle.load(file_obj)
file_obj.close()
print(f"Loaded map coordinates.")

# Load previously defined Regions of Interest (ROIs) polygons from a file

file_obj = open(countries_file_path, 'rb')
polygons = pickle.load(file_obj)

file_obj.close()
print(f"Loaded {len(polygons)} rectangles.")





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
selected_countries = []



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
    - country_selected: Name of the selected country.
    """
 
    country_selected = None
    
    green_duration_threshold = 3
    is_selected= False
        

    for polygon, name in polygons:
        

        polygon_np = np.array(polygon, np.int32).reshape((-1, 1, 2))
        result = cv2.pointPolygonTest(polygon_np, warped_point, False)
        if result >= 0:
            # If the country is not in the dictionary, add it with the current time
            if name not in country_entry_times:
                country_entry_times[name] = time.time()
 
            # Calculate the time the finger has spent in the country
            time_in_country = time.time() - country_entry_times[name]
 
            # If the time is greater than the threshold, make the country green
            if time_in_country >= green_duration_threshold:
                
                color = (255, 0, )  # blue color
                country_selected = name
                if name not in selected_countries:
                    selected_countries.append(name)
            else:
                color = (255, 0, 255)  #pink color
                # Draw an arc around the finger point based on elapsed time
                angle = int((time_in_country / green_duration_threshold) * 360)
                cv2.ellipse(imgOverlay, (warped_point[0], warped_point[1] - 100),(50, 50), 0, 0, angle, color,thickness=-1)
 
            cv2.polylines(imgOverlay, [np.array(polygon)], isClosed=True, color=color, thickness=2)
            cv2.fillPoly(imgOverlay, [np.array(polygon)], color)
            cvzone.putTextRect(imgOverlay, name, tuple(polygon[0][0]), scale=1, thickness=1)
        


 
    return imgOverlay, country_selected

def draw_exit_button(img):
    cv2.rectangle(img, (button_x, button_y), (button_x + button_width, button_y + button_height), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, button_text, (button_x + 10, button_y + 17), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)


def mouse_callback(event, x, y, flags, param):
    global exit_flag

    if event == cv2.EVENT_LBUTTONDOWN:
        if button_x < x < button_x + button_width and button_y < y < button_y + button_height:
            exit_flag = True




cv2.namedWindow("Output Image", cv2.WINDOW_FULLSCREEN)
cv2.setMouseCallback("Output Image", mouse_callback)


while True:
    # Read a frame from the webcam
    success, img = cap.read()
    img = cv2.rotate(img, cv2.ROTATE_180)
    imgWarped, matrix = warp_image(img, map_points)
    
    imgOutput = imgWarped.copy()
 
    # Find the hand and its landmarks
    warped_point = get_finger_location(img,imgWarped)
 
    h, w, _ = imgWarped.shape
    imgOverlay = np.zeros((h, w, 3), dtype=np.uint8)
    imgOverlay = cv2.flip(imgOverlay, 1) 
    
    for polygon, name in polygons:
        cv2.polylines(imgOverlay, [np.array(polygon)], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.fillPoly(imgOverlay, [np.array(polygon)], (0, 255, 0))
    selected_country = None
    if warped_point:
        imgOverlay, selected_country = create_overlay_image(polygons, warped_point, imgOverlay)
        imgOutput = cv2.addWeighted(imgWarped, 1, imgOverlay, 0.7, 0)

    
    imgOutput = cv2.flip(imgOutput, 1)
    imgOutput= cv2.resize(imgOutput, (480, 320))

    #imgOutput = cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE )
    draw_exit_button(imgOutput)
    # Display the current question
    key = cv2.waitKey(1)

    # If the "q" key is pressed, save the polygons and exit the loop
    if exit_flag:
        break

    cv2.imshow("Output Image", imgOutput)# cv2.resize(imgOutput, (480, 320)

    key = cv2.waitKey(1)

# ...

cv2.destroyAllWindows()




    # If the "q" key is pressed, save the polygons and exit the loop
   

    



cap.release()
cv2.destroyAllWindows()


metin ="\n"
if selected_countries:
    for kelime in selected_countries:
        metin=metin+kelime
    


    output_path = "selected_countries.pdf"

    write_to_pdf(output_path, metin)
    print(f"PDF dosyası oluşturuldu: {output_path}")
    