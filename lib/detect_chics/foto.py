import cv2
import numpy as np

def detect_circles(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)



    # Apply a Gaussian blur to the grayscale image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    thresh1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 199, 5) 

    
    

    # Use Canny edge detectionz
    canny = cv2.Canny(thresh1, 50, 150)

    # Use the HoughCircles method to detect circles
    circles = cv2.HoughCircles(thresh1, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=20, minRadius=10, maxRadius=50)

    # Draw circles on the original image
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, (0, 255, 0), 4)

    # Return the original image with circles drawn on it
    return thresh1

# Read the image from file
image = cv2.imread('can_shape_3.jpg')

# Detect circles in the image
detected_image = detect_circles(image)

# Display the original image with circles drawn on it

cv2.imshow('Detected Circles', detected_image)
cv2.waitKey(0)
cv2.destroyAllWindows()