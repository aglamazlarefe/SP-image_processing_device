import pickle
import time
import cv2
import numpy as np



#########################
# Camera settings
cam_id = 0  # Change this to your desired camera ID
cap = cv2.VideoCapture(cam_id)# For Webcam
#########################

# Initialize variables
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))# Change this to desired image resolution
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# cap.set(3, width)  # Set width
# cap.set(4, height)  # Set height
counter = 0  # Counter to track the number of clicked points

def find_largest_rectangle_contour(img):
    """
    Finds the largest rectangle contour in the image.

    Args:
        img: The input image

    Returns:
        largest_rect: Array containing four corner points of the largest rectangle
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    global thresh

    thresh = cv2.adaptiveThreshold(gray, 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 10)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_rect = None
    max_area = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            largest_rect = cv2.approxPolyDP(contour, epsilon, True)
            max_area = area

    return largest_rect


def warp(img):
    # Get the points
    fileObj = open(r"C:\Users\aglam\Documents\python_projeleri\SP-image_processing_device\map_realtime.p", "rb")
    points = pickle.load(fileObj)
    fileObj.close()
    
    # Explicitly convert the points to type numpy.float32
    points = points.astype(np.float32)
    
    # Compute the perspective transform matrix
    M = cv2.getPerspectiveTransform(points, np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32))
    
    # Apply the perspective transform
    result = cv2.warpPerspective(img, M, (width, height))
    # Display the result
    return result

last_warp_time = time.time()
points_saved = False  # points_saved değişkenini başlat

while True:
    success, img = cap.read()

    # Find the largest rectangle contour in the image
    largest_rect = find_largest_rectangle_contour(img)

    if largest_rect is not None and len(largest_rect) == 4:
        # Display the largest rectangle
        cv2.polylines(img, [largest_rect], True, (0, 255, 0), 2)

        # Draw circles at the corner points
        for point in largest_rect:
            cv2.circle(img, tuple(point[0]), 5, (255, 0, 0), -1)  # -1 fills the circle

        # Save selected points to file only if not saved before
        
        points = largest_rect.reshape(4, 2)
        fileObj = open("map_realtime.p", "wb")
        pickle.dump(points, fileObj)
        fileObj.close()
        print("Points saved to file: map_realtime.p")
        points_saved = True

    # Yalnızca bir kere kaydedildikten sonra ve 3 saniye geçtikten sonra warp fonksiyonunu çağır
    if points_saved and (time.time() - last_warp_time) >= 3:
        cv2.imshow("Transformed Image", warp(img))
        last_warp_time = time.time()  # Son çağrının zamanını güncelle

    cv2.imshow("Original Image ", img)
    cv2.imshow("threshold Image ", thresh)
    
    key = cv2.waitKey(1)  # Wait for a key press
    if key == 27:  # 27 is the ASCII code for the Esc key
        break

# Release resources
cap.release()
cv2.destroyAllWindows()